"""Isolate the two v5 changes, because together they were a regression.

v5 bundled an int8 refractory counter with a lane-split scatter and came out
slower than v3. Bundled changes cannot be attributed, so each kernel is timed
on its own here, with a sweep over the lane count that the balanced scatter
introduced.
"""

import argparse
import json
import sys
from pathlib import Path

import torch
import triton

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph, subgraph
from fast_kernels import membrane_compact, scatter_spikes
from fast_kernels2 import membrane_compact2, scatter_balanced
from precision_error import calibrate, DT, U_RESET, U_TH, REFRAC
from opt_bench import FastSim, timeit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--out", default="out/tune2.json")
    a = ap.parse_args()

    crow, col, val, _ = load_graph(a.graph)
    n = len(crow) - 1
    tonic, rate, _ = calibrate(crow, col, val, "cuda", a.scale, 5.0, 4.0, verbose=False)
    print(f"{n:,} neurons, batch {a.batch}, {rate:.2f} Hz\n")

    sim = FastSim(crow, col, val, torch.float32, "cuda", tonic, a.scale, batch=a.batch)
    sim.setup_fast(rate_hint=max(rate, 1.0))
    for _ in range(100):
        sim.step_fast()
    torch.cuda.synchronize()
    k = int(sim.fast.cnt.item())
    mean_deg = len(col) / n
    events = k * mean_deg
    print(f"{k:,} spikes/step, ~{events:,.0f} synaptic events\n")

    r8 = torch.zeros_like(sim.r, dtype=torch.int8)
    steps_ref = int(round(REFRAC / DT))
    state12 = 3 * 2 * a.batch * n * 4
    state9 = 2 * a.batch * n * (4 + 4 + 1) * 2 / 2      # v,g fp32 + r int8, r+w
    res = {}

    print("membrane kernel, refractory storage:")
    for label, fn, rbuf, extra, bytes_moved in (
            ("fp32 refractory (v3)", membrane_compact, sim.r,
             (float(REFRAC), float(DT)), state12),
            ("int8 refractory (v5)", membrane_compact2, r8,
             (steps_ref,), 2 * a.batch * n * 9)):
        def run(fn=fn, rbuf=rbuf, extra=extra):
            sim.fast.cnt.zero_()
            fn[sim.fast.grid_m](
                sim.u, sim.g, rbuf, sim.tonic, sim.fast.spikes, sim.fast.cnt,
                sim.fast.over, n, sim.cap, float(sim.decay), float(sim.alpha),
                float(U_RESET), float(U_TH), *extra, BLOCK=256)
        us = timeit(run, a.steps)
        res[label] = round(us, 1)
        print(f"  {label:24s} {us:8.1f} us   {bytes_moved/us*1e6/1e9:6.1f} GB/s")

    print("\nscatter kernel:")
    sim.fast.cnt.zero_()
    membrane_compact[sim.fast.grid_m](
        sim.u, sim.g, sim.r, sim.tonic, sim.fast.spikes, sim.fast.cnt,
        sim.fast.over, n, sim.cap, float(sim.decay), float(sim.alpha),
        float(U_RESET), float(U_TH), float(REFRAC), float(DT), BLOCK=256)
    torch.cuda.synchronize()

    def run_plain(eblk):
        scatter_spikes[(sim.cap,)](sim.fast.spikes, sim.fast.cnt, sim.fast.crow,
                                   sim.fast.col, sim.fast.val, sim.g, n, EBLOCK=eblk)
    us = timeit(lambda: run_plain(512), a.steps)
    res["scatter plain EBLOCK=512"] = round(us, 1)
    print(f"  plain, one program per spike, EBLOCK=512   {us:8.1f} us"
          f"   {events/us*1e6/1e9:5.2f} G ev/s")

    for lanes in (1, 2, 4, 8, 16):
        for eblk in (128, 512):
            def run(lanes=lanes, eblk=eblk):
                scatter_balanced[(sim.cap, lanes)](
                    sim.fast.spikes, sim.fast.cnt, sim.fast.crow, sim.fast.col,
                    sim.fast.val, sim.g, n, EBLOCK=eblk, LANES=lanes)
            us = timeit(run, a.steps)
            res[f"scatter lanes={lanes} EBLOCK={eblk}"] = round(us, 1)
            print(f"  lanes={lanes:3d} EBLOCK={eblk:4d}"
                  f"   {us:8.1f} us   {events/us*1e6/1e9:5.2f} G ev/s")

    print("\ncap (spike-slot grid size) matters: every slot launches a program")
    print(f"  cap = {sim.cap:,} slots for {k:,} actual spikes "
          f"-> {sim.cap/max(k,1):.1f}x empty programs")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
