"""Fused kernels for the LIF step, written to remove three specific costs.

1. `nonzero` materialises a dense [B, N] mask and synchronises with the host,
   to find the ~0.05% of cells that spiked. The membrane kernel instead
   appends spiking cells to a compact list through an atomic counter, so the
   mask never exists.
2. The synaptic scatter was eight separate launches plus a second host sync
   (cumsum, two repeat_interleaves, an arange, a gather, index_add_). It is
   one kernel here, each program walking one spiking cell's out-edges.
3. The membrane kernel used a modulo per element to find the per-cell drive.
   A 2D grid gives the neuron index directly.

No host synchronisation remains in the step, and every grid is a fixed size,
so the whole step is capturable as a CUDA graph.
"""

import torch
import triton
import triton.language as tl


@triton.jit
def membrane_compact(U, G, R, TONIC, SPIKES, CNT, OVER, n, cap,
                     decay, alpha, u_reset, u_th, refrac, dt,
                     BLOCK: tl.constexpr):
    """Advance one block of cells and append any spikes to a compact list."""
    b = tl.program_id(1)
    n_off = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    nmask = n_off < n
    offs = b * n + n_off

    u = tl.load(U + offs, mask=nmask, other=0.0).to(tl.float32)
    g = tl.load(G + offs, mask=nmask, other=0.0).to(tl.float32)
    r = tl.load(R + offs, mask=nmask, other=0.0).to(tl.float32)
    t = tl.load(TONIC + n_off, mask=nmask, other=0.0).to(tl.float32)

    g = g * decay
    live = r <= 0.0
    u = tl.where(live, u + alpha * (-u + g + t), u)
    s = (u >= u_th) & live & nmask
    u = tl.where(s, u_reset, u)
    r = tl.where(s, refrac, r - dt)

    tl.store(U + offs, u.to(U.dtype.element_ty), mask=nmask)
    tl.store(G + offs, g.to(G.dtype.element_ty), mask=nmask)
    tl.store(R + offs, r.to(R.dtype.element_ty), mask=nmask)

    # Compact the spikes: one atomic per block, not one per spike.
    si = s.to(tl.int32)
    num = tl.sum(si, axis=0)
    if num > 0:
        base = tl.atomic_add(CNT, num)
        pos = base + tl.cumsum(si, axis=0) - si
        fits = s & (pos < cap)
        tl.store(SPIKES + pos, offs.to(tl.int32), mask=fits)
        if base + num > cap:
            tl.atomic_max(OVER, base + num)


@triton.jit
def scatter_spikes(SPIKES, CNT, CROW, COL, VAL, G, n,
                   EBLOCK: tl.constexpr):
    """One program per spiking cell; walk its out-edges and accumulate."""
    pid = tl.program_id(0)
    cnt = tl.load(CNT)
    if pid >= cnt:
        return
    idx = tl.load(SPIKES + pid)
    b = idx // n
    src = idx - b * n
    lo = tl.load(CROW + src)
    hi = tl.load(CROW + src + 1)
    boff = b * n
    for start in range(lo, hi, EBLOCK):
        e = start + tl.arange(0, EBLOCK)
        m = e < hi
        tgt = tl.load(COL + e, mask=m, other=0)
        w = tl.load(VAL + e, mask=m, other=0.0)
        tl.atomic_add(G + boff + tgt, w, mask=m)


@triton.jit
def tally(SPIKES, CNT, COUNTS, n, BLOCK: tl.constexpr):
    """Per-neuron spike tally for replica 0, straight off the compact list."""
    offs = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    cnt = tl.load(CNT)
    m = offs < cnt
    idx = tl.load(SPIKES + offs, mask=m, other=-1)
    m = m & (idx >= 0) & (idx < n)          # replica 0 occupies [0, n)
    tl.atomic_add(COUNTS + idx, 1.0, mask=m)


class FastStep:
    """Holds the buffers and launch configuration for one network."""

    def __init__(self, n, batch, cap, block=256, eblock=128, device="cuda"):
        self.n, self.b, self.cap = n, batch, cap
        self.block, self.eblock = block, eblock
        dev = torch.device(device)
        self.spikes = torch.zeros(cap, dtype=torch.int32, device=dev)
        self.cnt = torch.zeros(1, dtype=torch.int32, device=dev)
        self.over = torch.zeros(1, dtype=torch.int32, device=dev)
        self.grid_m = (triton.cdiv(n, block), batch)
        self.grid_s = (cap,)
        self.grid_t = (triton.cdiv(cap, 1024),)

    def __call__(self, u, g, r, tonic, decay, alpha, u_reset, u_th, refrac, dt,
                 counts=None):
        self.cnt.zero_()
        membrane_compact[self.grid_m](
            u, g, r, tonic, self.spikes, self.cnt, self.over,
            self.n, self.cap, float(decay), float(alpha), float(u_reset),
            float(u_th), float(refrac), float(dt), BLOCK=self.block)
        scatter_spikes[self.grid_s](
            self.spikes, self.cnt, self.crow, self.col, self.val, g,
            self.n, EBLOCK=self.eblock)
        if counts is not None:
            tally[self.grid_t](self.spikes, self.cnt, counts, self.n, BLOCK=1024)

    def bind_graph(self, crow, col, val):
        self.crow, self.col, self.val = crow, col, val
        return self

    def overflowed(self):
        return int(self.over.item())
