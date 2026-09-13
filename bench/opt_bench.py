"""Take the step apart, replace one cost at a time, and check it still agrees.

Variants, each differing from the previous by exactly one change:
  v0  torch.compile membrane + torch scatter        (previous best)
  v1  triton membrane            + torch scatter
  v2  triton membrane + compaction + torch scatter  (no dense mask, no nonzero)
  v3  v2 + triton scatter                           (no host sync at all)
  v4  v3 captured as a CUDA graph                   (no per-step launch cost)

Correctness is checked against v0 on per-neuron firing rates, which is the
right comparison: atomic accumulation reorders sums, so bit-equality is not
available and chaos amplifies the difference. The fp32-vs-fp32 chaos floor
from bench/precision_error.py is the yardstick.
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
from kernels import membrane_triton
from fast_kernels import FastStep, membrane_compact, scatter_spikes, tally
from fast_kernels2 import membrane_compact2, scatter_balanced
from precision_error import Sim, drive, calibrate, DT, U_RESET, U_TH, REFRAC


class FastSim(Sim):
    """Same model, compact spike list and single-kernel scatter."""

    def setup_fast(self, cap_factor=8.0, rate_hint=5.0, block=256, eblock=128,
                   use_triton_scatter=True, v2=False, lanes=8):
        expected = max(64, int(self.b * self.n * rate_hint * DT / 1000.0))
        self.cap = int(triton.next_power_of_2(int(expected * cap_factor)))
        self.fast = FastStep(self.n, self.b, self.cap, block, eblock,
                             str(self.dev)).bind_graph(self.crow.int(), self.col.int(),
                                                       self.val)
        self.use_triton_scatter = use_triton_scatter
        self.v2, self.lanes, self.eblock = v2, lanes, eblock
        if v2:
            self.r = torch.zeros_like(self.r, dtype=torch.int8)
            self.refrac_steps = int(round(REFRAC / DT))
            self.grid_s2 = (self.cap, lanes)
        self.counts_buf = torch.zeros(self.n, device=self.dev, dtype=torch.float32)
        return self

    def step_fast(self, record=False):
        self.fast.cnt.zero_()
        if self.v2:
            membrane_compact2[self.fast.grid_m](
                self.u, self.g, self.r, self.tonic, self.fast.spikes,
                self.fast.cnt, self.fast.over, self.n, self.cap,
                float(self.decay), float(self.alpha), float(U_RESET),
                float(U_TH), self.refrac_steps, BLOCK=self.fast.block)
            scatter_balanced[self.grid_s2](
                self.fast.spikes, self.fast.cnt, self.fast.crow, self.fast.col,
                self.fast.val, self.g, self.n,
                EBLOCK=self.eblock, LANES=self.lanes)
            if record:
                tally[self.fast.grid_t](self.fast.spikes, self.fast.cnt,
                                        self.counts_buf, self.n, BLOCK=1024)
            return
        membrane_compact[self.fast.grid_m](
            self.u, self.g, self.r, self.tonic, self.fast.spikes, self.fast.cnt,
            self.fast.over, self.n, self.cap, float(self.decay), float(self.alpha),
            float(U_RESET), float(U_TH), float(REFRAC), float(DT),
            BLOCK=self.fast.block)
        if self.use_triton_scatter:
            scatter_spikes[self.fast.grid_s](
                self.fast.spikes, self.fast.cnt, self.fast.crow, self.fast.col,
                self.fast.val, self.g, self.n, EBLOCK=self.fast.eblock)
        else:
            k = int(self.fast.cnt.item())              # host sync, on purpose
            if k:
                idx = self.fast.spikes[:k].long()
                sb, sn = idx // self.n, idx % self.n
                start = self.crow[sn]
                cnt = self.crow[sn + 1] - start
                total = int(cnt.sum())
                if total:
                    base = torch.repeat_interleave(start, cnt, output_size=total)
                    off = torch.cumsum(cnt, 0) - cnt
                    rank = (torch.arange(total, device=self.dev)
                            - torch.repeat_interleave(off, cnt, output_size=total))
                    e = base + rank
                    bb = torch.repeat_interleave(sb, cnt, output_size=total)
                    self.g.view(-1).index_add_(0, bb * self.n + self.col[e],
                                               self.val[e])
        if record:
            tally[self.fast.grid_t](self.fast.spikes, self.fast.cnt,
                                    self.counts_buf, self.n, BLOCK=1024)

    def run_fast(self, ms):
        self.counts_buf.zero_()
        for _ in range(int(round(ms / DT))):
            self.step_fast(record=True)
        return self.counts_buf.cpu().numpy() / (ms / 1000.0)


def rates_reference(sim, ms):
    return sim.run(ms)[0]


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
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--verify-ms", type=float, default=200.0)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--target-rate", type=float, default=5.0)
    ap.add_argument("--sigma", type=float, default=4.0)
    ap.add_argument("--out", default="out/opt_bench.json")
    a = ap.parse_args()

    crow, col, val, kind = load_graph(a.graph)
    if a.subsample:
        crow, col, val = subgraph(crow, col, val, a.subsample)
    n = len(crow) - 1
    print(f"graph {kind}: {n:,} neurons, {len(col):,} edges, batch {a.batch}")

    print("calibrating:")
    tonic, rate, mu = calibrate(crow, col, val, "cuda", a.scale,
                                a.target_rate, a.sigma, verbose=False)
    print(f"  mu={mu:.3f} -> {rate:.2f} Hz\n")

    f32 = torch.float32
    mk = lambda batch=1: Sim(crow, col, val, f32, "cuda", tonic, a.scale, batch=batch)

    # ---- correctness ---------------------------------------------------
    print(f"correctness over {a.verify_ms:.0f} ms (per-neuron rates, replica 0):")
    ref = rates_reference(mk(), a.verify_ms)
    fast = FastSim(crow, col, val, f32, "cuda", tonic, a.scale, batch=1)
    fast.setup_fast(rate_hint=max(rate, 1.0))
    got = fast.run_fast(a.verify_ms)
    ok_corr = float(np.corrcoef(ref, got)[0, 1])
    print(f"  reference mean {ref.mean():.4f} Hz   fast mean {got.mean():.4f} Hz")
    print(f"  population rate error {100*abs(got.mean()-ref.mean())/ref.mean():.3f}%"
          f"   per-neuron corr {ok_corr:.5f}")
    print(f"  spike-list overflow: {fast.fast.overflowed()} (0 means the cap held)\n")

    # ---- speed ---------------------------------------------------------
    print(f"speed at batch {a.batch}, us/step:")
    rows = []

    s0 = mk(a.batch)
    t0 = timeit(s0.step, a.steps)
    rows.append(("v0  torch.compile + torch scatter", t0))

    s1 = mk(a.batch)
    s1.kernel = "triton"
    t1 = timeit(s1.step, a.steps)
    rows.append(("v1  triton membrane + torch scatter", t1))

    s2 = FastSim(crow, col, val, f32, "cuda", tonic, a.scale, batch=a.batch)
    s2.setup_fast(rate_hint=max(rate, 1.0), use_triton_scatter=False)
    t2 = timeit(lambda: s2.step_fast(), a.steps)
    rows.append(("v2  + compact spike list", t2))

    s3 = FastSim(crow, col, val, f32, "cuda", tonic, a.scale, batch=a.batch)
    s3.setup_fast(rate_hint=max(rate, 1.0), use_triton_scatter=True)
    t3 = timeit(lambda: s3.step_fast(), a.steps)
    rows.append(("v3  + triton scatter (no host sync)", t3))

    s5 = FastSim(crow, col, val, f32, "cuda", tonic, a.scale, batch=a.batch)
    s5.setup_fast(rate_hint=max(rate, 1.0), v2=True, eblock=512, lanes=8)
    t5 = timeit(lambda: s5.step_fast(), a.steps)
    rows.append(("v5  int8 refractory + balanced scatter", t5))

    v5 = FastSim(crow, col, val, f32, "cuda", tonic, a.scale, batch=1)
    v5.setup_fast(rate_hint=max(rate, 1.0), v2=True, eblock=512, lanes=8)
    got5 = v5.run_fast(a.verify_ms)
    print(f"  v5 check: mean {got5.mean():.4f} Hz vs reference {ref.mean():.4f} Hz, "
          f"error {100*abs(got5.mean()-ref.mean())/ref.mean():.3f}%, "
          f"corr {float(np.corrcoef(ref, got5)[0,1]):.5f}\n")

    # ---- CUDA graph ----------------------------------------------------
    try:
        s4 = FastSim(crow, col, val, f32, "cuda", tonic, a.scale, batch=a.batch)
        s4.setup_fast(rate_hint=max(rate, 1.0), v2=True, eblock=512, lanes=8)
        for _ in range(20):
            s4.step_fast()
        torch.cuda.synchronize()
        gph = torch.cuda.CUDAGraph()
        with torch.cuda.graph(gph):
            s4.step_fast()
        t4 = timeit(gph.replay, a.steps)
        rows.append(("v4  + CUDA graph", t4))
    except Exception as exc:
        print(f"  (CUDA graph capture failed: {type(exc).__name__}: {exc})")

    base = rows[0][1]
    out = []
    for label, us in rows:
        print(f"  {label:38s} {us:8.1f}   {base/us:5.2f}x")
        out.append({"variant": label, "us_per_step": round(us, 1),
                    "speedup_vs_v0": round(base / us, 3),
                    "aggregate_x_realtime": round(DT / 1000.0 / (us / 1e6) * a.batch, 2)})

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"neurons": n, "edges": len(col), "batch": a.batch,
         "mean_rate_hz": rate, "verify_corr": ok_corr, "rows": out}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
