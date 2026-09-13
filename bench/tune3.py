"""Sweep the grid shape of the strided scatter, which is now the whole game."""

import argparse
import json
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph
from fast_kernels import membrane_compact, scatter_spikes
from fast_kernels3 import scatter_stride
from precision_error import calibrate, DT, U_RESET, U_TH, REFRAC
from opt_bench import FastSim, timeit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--out", default="out/tune3.json")
    a = ap.parse_args()

    crow, col, val, _ = load_graph(a.graph)
    n = len(crow) - 1
    tonic, rate, _ = calibrate(crow, col, val, "cuda", a.scale, 5.0, 4.0, verbose=False)
    sim = FastSim(crow, col, val, torch.float32, "cuda", tonic, a.scale, batch=a.batch)
    sim.setup_fast(rate_hint=max(rate, 1.0))
    for _ in range(100):
        sim.step_fast()
    torch.cuda.synchronize()
    k = int(sim.fast.cnt.item())
    events = k * (len(col) / n)
    print(f"{n:,} neurons, batch {a.batch}: {k:,} spikes/step, "
          f"~{events:,.0f} synaptic events (~{events*12/2**20:.1f} MiB of traffic)\n")

    base = timeit(lambda: scatter_spikes[(sim.cap,)](
        sim.fast.spikes, sim.fast.cnt, sim.fast.crow, sim.fast.col,
        sim.fast.val, sim.g, n, EBLOCK=512), a.steps)
    print(f"baseline (one program per buffer slot, EBLOCK=512): {base:.1f} us\n")

    res = {"baseline_us": round(base, 1), "spikes": k, "sweep": {}}
    best = (base, "baseline")
    for grid in (128, 256, 512, 1024, 2048):
        line = []
        for lanes in (1, 4, 16):
            for eblk in (32, 64, 128):
                def run(grid=grid, lanes=lanes, eblk=eblk):
                    scatter_stride[(grid, lanes)](
                        sim.fast.spikes, sim.fast.cnt, sim.fast.crow,
                        sim.fast.col, sim.fast.val, sim.g, n, sim.cap,
                        EBLOCK=eblk, GRID=grid, LANES=lanes)
                us = timeit(run, a.steps)
                key = f"grid={grid} lanes={lanes} EBLOCK={eblk}"
                res["sweep"][key] = round(us, 1)
                line.append(f"l{lanes:2d}/e{eblk:3d}:{us:7.1f}")
                if us < best[0]:
                    best = (us, key)
        print(f"  grid={grid:5d}  " + "  ".join(line))

    print(f"\nbest: {best[1]} at {best[0]:.1f} us "
          f"({base/best[0]:.2f}x over baseline, "
          f"{events/best[0]*1e6/1e9:.2f} G synaptic events/s)")
    res["best"] = {"config": best[1], "us": round(best[0], 1),
                   "speedup_vs_baseline": round(base / best[0], 2)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=2) + "\n")


if __name__ == "__main__":
    main()
