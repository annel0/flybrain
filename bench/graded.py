"""Graded, non-spiking output for cells that do not spike in the animal.

Some antennal lobe local interneurons transcribe the voltage-gated sodium
channel gene para but do not translate it, so they carry no sodium current and
release transmitter by graded potential rather than by action potential
(eNeuro 2022, ENEURO.0109-22.2022). Our model makes them spike, and they are
the hottest cells in it at around 350 Hz, smearing activity across glomeruli
and blurring the labelled line down to a 2-6x preference for the driven
glomerulus.

A graded cell releases continuously as a function of its membrane potential
instead of discretely on threshold crossings. The transfer used here is
rectified-linear above rest with a gain in Hz per mV, so the quantity
delivered per step is the same form a spiking cell would deliver at that rate:
weight x rate x dt. The gain is set so that a cell sitting at spike threshold
releases at a chosen reference rate, which makes the graded and spiking
versions comparable rather than arbitrarily rescaled.

Release is delayed by the same axonal delay as a spike, through a small ring
of per-cell output values -- with a few hundred graded cells that ring costs
nothing. What the paper does not give, and we therefore do not know, is what
fraction of local interneurons are non-spiking; that is a parameter here, not
a measurement.
"""

import triton
import triton.language as tl


@triton.jit
def graded_release(U, IDX, RING, CROW, COL, VAL, G, n, n_graded, slot, D,
                   gain, dt_ms, EBLOCK: tl.constexpr, GRID: tl.constexpr,
                   LANES: tl.constexpr):
    """Each program walks one graded cell's out-edges, delivering a continuous
    amount proportional to how far that cell sits above rest."""
    p = tl.program_id(0)
    lane = tl.program_id(1)
    i = p
    while i < n_graded:
        src = tl.load(IDX + i)
        u = tl.load(U + src).to(tl.float32)
        rate = tl.maximum(u, 0.0) * gain          # Hz
        amount = rate * dt_ms / 1000.0
        if amount > 1e-9:
            lo = tl.load(CROW + src)
            hi = tl.load(CROW + src + 1)
            start = lo + lane * EBLOCK
            while start < hi:
                e = start + tl.arange(0, EBLOCK)
                m = e < hi
                tgt = tl.load(COL + e, mask=m, other=0)
                w = tl.load(VAL + e, mask=m, other=0.0)
                tl.atomic_add(G + tgt, w * amount, mask=m)
                start += LANES * EBLOCK
        i += GRID


@triton.jit
def graded_buffer(U, IDX, RING, n_graded, slot, D, BLOCK: tl.constexpr):
    """Record each graded cell's current level into its delay slot."""
    offs = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    m = offs < n_graded
    src = tl.load(IDX + offs, mask=m, other=0)
    u = tl.load(U + src, mask=m, other=0.0).to(tl.float32)
    tl.store(RING + slot * n_graded + offs, u, mask=m)


@triton.jit
def graded_deliver(RING, IDX, CROW, COL, VAL, G, n, n_graded, slot,
                   gain, dt_ms, EBLOCK: tl.constexpr, GRID: tl.constexpr,
                   LANES: tl.constexpr):
    """Deliver what each graded cell released one axonal delay ago."""
    p = tl.program_id(0)
    lane = tl.program_id(1)
    i = p
    while i < n_graded:
        u = tl.load(RING + slot * n_graded + i)
        amount = tl.maximum(u, 0.0) * gain * dt_ms / 1000.0
        if amount > 1e-9:
            src = tl.load(IDX + i)
            lo = tl.load(CROW + src)
            hi = tl.load(CROW + src + 1)
            start = lo + lane * EBLOCK
            while start < hi:
                e = start + tl.arange(0, EBLOCK)
                m = e < hi
                tgt = tl.load(COL + e, mask=m, other=0)
                w = tl.load(VAL + e, mask=m, other=0.0)
                tl.atomic_add(G + tgt, w * amount, mask=m)
                start += LANES * EBLOCK
        i += GRID
