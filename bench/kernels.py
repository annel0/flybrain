"""One hand-written fused kernel for the membrane update.

torch.compile refuses to generate a good kernel when the state arrays
disagree in dtype, which made the numerically better mixed-precision layout
2.5x slower than plain fp32. Writing the kernel directly removes that
constraint: loads widen to fp32 in registers, stores narrow back to whatever
each array happens to be, and the whole step is one pass over memory.

Triton ships with PyTorch, so this needs no extra dependency. NVIDIA's
numba-cuda or Warp would express the same thing; see README.
"""

import torch
import triton
import triton.language as tl


@triton.jit
def _membrane(U, G, R, TONIC, S, n_elem, n, decay, alpha,
              u_reset, u_th, refrac, dt, BLOCK: tl.constexpr):
    offs = tl.program_id(0) * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n_elem

    # Load at whatever precision the arrays are stored in, work in fp32.
    u = tl.load(U + offs, mask=mask, other=0.0).to(tl.float32)
    g = tl.load(G + offs, mask=mask, other=0.0).to(tl.float32)
    r = tl.load(R + offs, mask=mask, other=0.0).to(tl.float32)
    t = tl.load(TONIC + (offs % n), mask=mask, other=0.0).to(tl.float32)

    g = g * decay
    live = r <= 0.0
    u = tl.where(live, u + alpha * (-u + g + t), u)
    s = (u >= u_th) & live
    u = tl.where(s, u_reset, u)
    r = tl.where(s, refrac, r - dt)

    # Narrow back on the way out.
    tl.store(U + offs, u.to(U.dtype.element_ty), mask=mask)
    tl.store(G + offs, g.to(G.dtype.element_ty), mask=mask)
    tl.store(R + offs, r.to(R.dtype.element_ty), mask=mask)
    tl.store(S + offs, s.to(tl.int8), mask=mask)


def membrane_triton(u, g, r, tonic, s_buf, decay, alpha,
                    u_reset, u_th, refrac, dt, block=1024):
    n_elem = u.numel()
    n = u.shape[-1]
    grid = (triton.cdiv(n_elem, block),)
    _membrane[grid](u, g, r, tonic, s_buf, n_elem, n,
                    float(decay), float(alpha), float(u_reset), float(u_th),
                    float(refrac), float(dt), BLOCK=block)
    return s_buf
