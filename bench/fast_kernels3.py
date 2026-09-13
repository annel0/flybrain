"""Third pass. The lane split was the wrong fix, so it is replaced.

The scatter was launching one program per *slot* of the spike buffer, and the
buffer is sized for the worst case: 65,536 slots for the ~1,200 spikes a step
actually produces. Fifty-four out of every fifty-five programs existed only to
load the counter and exit, and adding lanes multiplied that waste -- which is
why the "load-balanced" version measured slower.

Here the grid is a fixed, tuned size and every program stays busy: it strides
over spikes in the outer loop and over that cell's edge chunks in the inner
one. Both dimensions are grid-strided, so a 7,000-edge cell is shared across
lanes without any program being launched for nothing.

Note also that the work is small in absolute terms -- ~184k synaptic events,
about 2 MB of traffic. At that size the kernel is bound by how much of the
card it can keep busy, not by bandwidth, so the grid shape is the parameter
that matters.
"""

import triton
import triton.language as tl


@triton.jit
def scatter_stride(SPIKES, CNT, CROW, COL, VAL, G, n, cap,
                   EBLOCK: tl.constexpr, GRID: tl.constexpr, LANES: tl.constexpr):
    p = tl.program_id(0)
    lane = tl.program_id(1)
    # Clamp: the membrane kernel reports how many spikes it *saw*, which can
    # exceed what fitted in the buffer. Reading past the buffer would be an
    # out-of-bounds access, so trust the capacity, not the counter.
    cnt = tl.minimum(tl.load(CNT), cap)
    i = p
    while i < cnt:
        idx = tl.load(SPIKES + i)
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
