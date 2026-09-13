"""The optimised step, verified and swept.

Combines what survived measurement: a fused membrane kernel that compacts
spikes through an atomic counter, an int8 refractory counter, and a strided
scatter at the grid shape the sweep picked. Everything that did not survive
(lane splitting by buffer slot, CUDA graphs, mixed-dtype torch.compile) is
gone.

Correctness is checked against the original torch implementation on
per-neuron firing rates before any timing is reported.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import triton

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph, subgraph
from fast_kernels import tally
from fast_kernels2 import membrane_compact2
from fast_kernels3 import scatter_stride
from precision_error import Sim, calibrate, DT, U_RESET, U_TH, REFRAC

GRID, LANES, EBLOCK, BLOCK = 1024, 4, 128, 256


class FinalSim(Sim):
    def setup(self, cap, rate_hint):
        self.cap = cap
        self.r = torch.zeros_like(self.r, dtype=torch.int8)
        self.refrac_steps = int(round(REFRAC / DT))
        self.spikes = torch.zeros(cap, dtype=torch.int32, device=self.dev)
        self.cnt = torch.zeros(1, dtype=torch.int32, device=self.dev)
        self.over = torch.zeros(1, dtype=torch.int32, device=self.dev)
        self.counts = torch.zeros(self.n, device=self.dev, dtype=torch.float32)
        self.crow32 = self.crow.int()
        self.col32 = self.col.int()
        self.grid_m = (triton.cdiv(self.n, BLOCK), self.b)
        self.grid_t = (triton.cdiv(cap, 1024),)
        return self

    def step(self, record=False):
        self.cnt.zero_()
        membrane_compact2[self.grid_m](
            self.u, self.g, self.r, self.tonic, self.spikes, self.cnt, self.over,
            self.n, self.cap, float(self.decay), float(self.alpha),
            float(U_RESET), float(U_TH), self.refrac_steps, BLOCK=BLOCK)
        scatter_stride[(GRID, LANES)](
            self.spikes, self.cnt, self.crow32, self.col32, self.val, self.g,
            self.n, self.cap, EBLOCK=EBLOCK, GRID=GRID, LANES=LANES)
        if record:
            tally[self.grid_t](self.spikes, self.cnt, self.counts, self.n, BLOCK=1024)

    def rates(self, ms):
        self.counts.zero_()
        for _ in range(int(round(ms / DT))):
            self.step(record=True)
        return self.counts.cpu().numpy() / (ms / 1000.0)


def timeit(fn, steps, warmup=60):
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(steps):
        fn()
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / steps * 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--subsample", type=int, default=0)
    ap.add_argument("--batches", default="1,4,16,64,128,256")
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--verify-ms", type=float, default=200.0)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--out", default="out/final.json")
    a = ap.parse_args()

    crow, col, val, kind = load_graph(a.graph)
    if a.subsample:
        crow, col, val = subgraph(crow, col, val, a.subsample)
    n = len(crow) - 1
    tonic, rate, mu = calibrate(crow, col, val, "cuda", a.scale, 5.0, 4.0, verbose=False)
    print(f"graph: {n:,} neurons, {len(col):,} edges, {rate:.2f} Hz\n")

    f32, f16 = torch.float32, torch.float16
    cap = 1 << 16

    print(f"correctness vs original torch path, {a.verify_ms:.0f} ms:")
    ref = Sim(crow, col, val, f32, "cuda", tonic, a.scale, batch=1).run(a.verify_ms)[0]
    for label, dt in (("fp32", f32), ("fp16 u+g", (f16, f16, f16))):
        s = FinalSim(crow, col, val, dt, "cuda", tonic, a.scale, batch=1).setup(cap, rate)
        got = s.rates(a.verify_ms)
        err = 100 * abs(got.mean() - ref.mean()) / max(ref.mean(), 1e-9)
        print(f"  {label:9s} mean {got.mean():.4f} vs {ref.mean():.4f} Hz  "
              f"error {err:.3f}%  corr {float(np.corrcoef(ref, got)[0,1]):.5f}  "
              f"overflow {int(s.over.item())}")

    print(f"\nthroughput sweep (aggregate = replicas x simulated-s per wall-s):")
    rows = []
    for b in [int(x) for x in a.batches.split(",")]:
        for label, dt in (("fp32", f32), ("fp16", (f16, f16, f16))):
            try:
                s = FinalSim(crow, col, val, dt, "cuda", tonic, a.scale,
                             batch=b).setup(cap, rate)
                us = timeit(s.step, a.steps)
                agg = DT / 1000.0 / (us / 1e6) * b
                rows.append({"batch": b, "dtype": label, "us_per_step": round(us, 1),
                             "aggregate_x_realtime": round(agg, 2),
                             "gpu_mem_GiB": round(torch.cuda.max_memory_allocated() / 2**30, 2)})
                print(f"  batch {b:4d}  {label:5s} {us:8.1f} us/step   "
                      f"{agg:7.2f}x realtime")
                del s
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats()
            except torch.cuda.OutOfMemoryError:
                print(f"  batch {b:4d}  {label:5s} OOM")
                break

    best = max(rows, key=lambda r: r["aggregate_x_realtime"])
    print(f"\nbest: {best['aggregate_x_realtime']}x realtime at batch "
          f"{best['batch']} ({best['dtype']})")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"neurons": n, "edges": len(col),
                                       "rate_hz": rate, "rows": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
