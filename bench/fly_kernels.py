"""Kernels with synaptic delay, and drive that enters through sensory cells.

Two changes from the previous step, both aimed at the same symptom: the
activity had no spatial structure, because every cell was driven by its own
private noise and every spike arrived everywhere instantly.

**Delay.** A spike is no longer scattered when it is emitted. The membrane
kernel appends the spiking cell to a ring slot `(t + delay[i]) mod D`, and the
scatter kernel delivers whatever is due in slot `t mod D`. Because the delay
is per source cell rather than per synapse, the ring holds spike indices, not
conductances: cost is proportional to spikes, not to the population, so delay
is nearly free. A dense `[D, batch, n]` conductance ring -- the usual
implementation -- would have roughly doubled the step's memory traffic.

Maximum delay must stay below D or a slot would hold two delivery times at
once; delays are clamped to 31 steps against D = 32.

**Drive.** `TONIC` is supplied per step, so a stimulus can be presented to
sensory cells while the rest of the network receives only a small baseline.
Whether activity then reaches the central brain is the question, not an
assumption.

**Noise.** A constant background cannot produce graded spontaneous activity:
a cell sits either above threshold and fires forever or below it and never
fires, which is exactly the silent-majority/hot-minority split the first runs
showed. Background is a per-step Gaussian instead, scaled as Euler-Maruyama
for the membrane time constant, standing in for the channel and synaptic
noise that makes real cells fire irregularly at rest.
"""

import triton
import triton.language as tl

RING_SLOTS = 32          # must exceed the largest delay in steps


@triton.jit
def membrane_delay(U, G, R, TONIC, FORCE, GRADED, DELAY, RING, RING_CNT,
                   n, cap, t, decay, alpha, u_reset, u_th, refrac_steps,
                   sigma, seed, BLOCK: tl.constexpr, D: tl.constexpr):
    b = tl.program_id(1)
    n_off = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    nmask = n_off < n
    offs = b * n + n_off

    u = tl.load(U + offs, mask=nmask, other=0.0).to(tl.float32)
    g = tl.load(G + offs, mask=nmask, other=0.0).to(tl.float32)
    r = tl.load(R + offs, mask=nmask, other=0)
    drive = tl.load(TONIC + n_off, mask=nmask, other=0.0).to(tl.float32)

    g = g * decay
    live = r == 0
    noise = tl.randn(seed + t, offs) * sigma   # fresh stream each step
    u = tl.where(live, u + alpha * (-u + g + drive) + noise, u)
    # Poisson forcing, as optogenetic activation is modelled in the source
    # paper: a driven cell spikes at its own rate regardless of its input.
    pf = tl.load(FORCE + n_off, mask=nmask, other=0.0).to(tl.float32)
    coin = tl.rand(seed + t + 7919, offs)
    # Graded cells integrate and release continuously; they never spike, so
    # they are also never reset and never enter refractoriness.
    gr = tl.load(GRADED + n_off, mask=nmask, other=0)
    s = ((u >= u_th) | (coin < pf)) & live & nmask & (gr == 0)
    u = tl.where(s, u_reset, u)
    g = tl.where(s, 0.0, g)          # published model clears g on a spike
    r = tl.where(s, refrac_steps, tl.maximum(r - 1, 0))

    tl.store(U + offs, u.to(U.dtype.element_ty), mask=nmask)
    tl.store(G + offs, g.to(G.dtype.element_ty), mask=nmask)
    tl.store(R + offs, r.to(tl.int8), mask=nmask)

    # Schedule each spike for its own arrival time.
    d = tl.load(DELAY + n_off, mask=nmask, other=1).to(tl.int32)
    slot = (t + d) % D
    pos = tl.atomic_add(RING_CNT + slot, 1, mask=s)
    tl.store(RING + slot * cap + pos, offs.to(tl.int32),
             mask=s & (pos < cap))


@triton.jit
def deliver(RING, RING_CNT, CROW, COL, VAL, G, n, cap, slot,
            EBLOCK: tl.constexpr, GRID: tl.constexpr, LANES: tl.constexpr):
    """Scatter the spikes whose delay expires on this step."""
    p = tl.program_id(0)
    lane = tl.program_id(1)
    cnt = tl.minimum(tl.load(RING_CNT + slot), cap)
    base_slot = slot * cap
    i = p
    while i < cnt:
        idx = tl.load(RING + base_slot + i)
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
        i += GRID


@triton.jit
def tally_slot(RING, RING_CNT, COUNTS, n, cap, slot, BLOCK: tl.constexpr):
    offs = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    cnt = tl.minimum(tl.load(RING_CNT + slot), cap)
    m = offs < cnt
    idx = tl.load(RING + slot * cap + offs, mask=m, other=-1)
    m = m & (idx >= 0) & (idx < n)
    tl.atomic_add(COUNTS + idx, 1.0, mask=m)
