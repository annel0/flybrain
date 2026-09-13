"""Second pass over the step, driven by what the profile actually showed.

The measurement said two things. The membrane kernel runs at 258 GB/s against
a measured card ceiling of 290, so it is done being tuned and can only be made
faster by moving fewer bytes. And the scatter carries a 44x load imbalance:
the busiest spiking cell has 7053 out-edges against a median of 113, so one
program holds the whole kernel open.

Two changes follow:

* The refractory timer was an fp32 array, a third of the membrane traffic, to
  hold a countdown that never exceeds 22. It is an int8 step counter here.
  That is exact -- integer steps, no rounding -- and removes 25% of the bytes.
* The scatter gets a second grid dimension over edge chunks, so a long
  out-edge list is split across programs instead of serialising in one.
"""

import torch
import triton
import triton.language as tl


@triton.jit
def membrane_compact2(U, G, R, TONIC, SPIKES, CNT, OVER, n, cap,
                      decay, alpha, u_reset, u_th, refrac_steps,
                      BLOCK: tl.constexpr):
    b = tl.program_id(1)
    n_off = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    nmask = n_off < n
    offs = b * n + n_off

    u = tl.load(U + offs, mask=nmask, other=0.0).to(tl.float32)
    g = tl.load(G + offs, mask=nmask, other=0.0).to(tl.float32)
    r = tl.load(R + offs, mask=nmask, other=0)          # int8 countdown
    t = tl.load(TONIC + n_off, mask=nmask, other=0.0).to(tl.float32)

    g = g * decay
    live = r == 0
    u = tl.where(live, u + alpha * (-u + g + t), u)
    s = (u >= u_th) & live & nmask
    u = tl.where(s, u_reset, u)
    r = tl.where(s, refrac_steps, tl.maximum(r - 1, 0))

    tl.store(U + offs, u.to(U.dtype.element_ty), mask=nmask)
    tl.store(G + offs, g.to(G.dtype.element_ty), mask=nmask)
    tl.store(R + offs, r.to(tl.int8), mask=nmask)

    si = s.to(tl.int32)
    num = tl.sum(si, axis=0)
    if num > 0:
        base = tl.atomic_add(CNT, num)
        pos = base + tl.cumsum(si, axis=0) - si
        tl.store(SPIKES + pos, offs.to(tl.int32), mask=s & (pos < cap))
        if base + num > cap:
            tl.atomic_max(OVER, base + num)


@triton.jit
def scatter_balanced(SPIKES, CNT, CROW, COL, VAL, G, n,
                     EBLOCK: tl.constexpr, LANES: tl.constexpr):
    """Grid is (spike slot, lane). Lanes share one cell's out-edge list."""
    pid = tl.program_id(0)
    cnt = tl.load(CNT)
    if pid >= cnt:
        return
    lane = tl.program_id(1)
    idx = tl.load(SPIKES + pid)
    b = idx // n
    src = idx - b * n
    lo = tl.load(CROW + src)
    hi = tl.load(CROW + src + 1)
    boff = b * n
    start = lo + lane * EBLOCK
    while start < hi:
        e = start + tl.arange(0, EBLOCK)
        m = e < hi
        tgt = tl.load(COL + e, mask=m, other=0)
        w = tl.load(VAL + e, mask=m, other=0.0)
        tl.atomic_add(G + boff + tgt, w, mask=m)
        start += LANES * EBLOCK
