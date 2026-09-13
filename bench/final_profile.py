"""Where the optimised step spends its time now, and what is left to attack."""

import sys
from pathlib import Path

import torch
import triton

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph
from fast_kernels2 import membrane_compact2
from fast_kernels3 import scatter_stride
from precision_error import calibrate, DT, U_RESET, U_TH, REFRAC
from final import FinalSim, timeit, GRID, LANES, EBLOCK, BLOCK

crow, col, val, _ = load_graph("data/malecns_v1/graph.npz")
n = len(crow) - 1
tonic, rate, _ = calibrate(crow, col, val, "cuda", 0.05, 5.0, 4.0, verbose=False)

for batch in (16, 64):
    for label, dt in (("fp32", torch.float32),
                      ("fp16", (torch.float16,) * 3)):
        s = FinalSim(crow, col, val, dt, "cuda", tonic, 0.05,
                     batch=batch).setup(1 << 16, rate)
        for _ in range(80):
            s.step()
        torch.cuda.synchronize()

        full = timeit(s.step, 200)
        def memb_only():
            s.cnt.zero_()
            membrane_compact2[s.grid_m](
                s.u, s.g, s.r, s.tonic, s.spikes, s.cnt, s.over, s.n, s.cap,
                float(s.decay), float(s.alpha), float(U_RESET), float(U_TH),
                s.refrac_steps, BLOCK=BLOCK)

        memb = timeit(memb_only, 200)
        scat = timeit(lambda: scatter_stride[(GRID, LANES)](
            s.spikes, s.cnt, s.crow32, s.col32, s.val, s.g, s.n, s.cap,
            EBLOCK=EBLOCK, GRID=GRID, LANES=LANES), 200)
        zero = timeit(s.cnt.zero_, 200)

        w = 2 if label == "fp16" else 4
        bytes_state = 2 * batch * n * (w + w + 1)
        print(f"batch {batch:3d} {label}: full {full:7.1f} us | "
              f"membrane {memb:7.1f} ({100*memb/full:4.1f}%, "
              f"{bytes_state/memb*1e6/1e9:5.1f} GB/s) | "
              f"scatter {scat:6.1f} ({100*scat/full:4.1f}%) | "
              f"cnt.zero_ {zero:5.1f} ({100*zero/full:4.1f}%)")
        del s
        torch.cuda.empty_cache()
