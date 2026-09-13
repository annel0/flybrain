"""Split the optimised step and sweep the launch parameters I guessed at.

Block sizes were picked without evidence when the kernels were written. This
measures each kernel alone across a grid of them, and reports the achieved
memory bandwidth and atomic rate so it is clear which kernel is near its
limit and which is not.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import torch
import triton

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph, subgraph
from fast_kernels import membrane_compact, scatter_spikes
from precision_error import Sim, calibrate, DT, U_RESET, U_TH, REFRAC
from opt_bench import FastSim, timeit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--subsample", type=int, default=0)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--target-rate", type=float, default=5.0)
    ap.add_argument("--sigma", type=float, default=4.0)
    ap.add_argument("--out", default="out/tune.json")
    a = ap.parse_args()

    crow, col, val, kind = load_graph(a.graph)
    if a.subsample:
        crow, col, val = subgraph(crow, col, val, a.subsample)
    n = len(crow) - 1
    tonic, rate, mu = calibrate(crow, col, val, "cuda", a.scale,
                                a.target_rate, a.sigma, verbose=False)
    print(f"graph: {n:,} neurons, {len(col):,} edges, batch {a.batch}, {rate:.2f} Hz")

    sim = FastSim(crow, col, val, torch.float32, "cuda", tonic, a.scale, batch=a.batch)
    sim.setup_fast(rate_hint=max(rate, 1.0))
    for _ in range(100):
        sim.step_fast()
    torch.cuda.synchronize()

    state_bytes = 3 * 2 * a.batch * n * 4          # v,g,r read+write
    spikes = int(sim.fast.cnt.item())
    print(f"spikes per step: {spikes:,}  (~{spikes*153:,} synaptic events)\n")

    res = {"spikes_per_step": spikes, "membrane": {}, "scatter": {}}

    print("membrane_compact, BLOCK sweep:")
    for blk in (64, 128, 256, 512, 1024):
        grid = (triton.cdiv(n, blk), a.batch)

        def run(blk=blk, grid=grid):
            sim.fast.cnt.zero_()
            membrane_compact[grid](
                sim.u, sim.g, sim.r, sim.tonic, sim.fast.spikes, sim.fast.cnt,
                sim.fast.over, n, sim.cap, float(sim.decay), float(sim.alpha),
                float(U_RESET), float(U_TH), float(REFRAC), float(DT), BLOCK=blk)

        us = timeit(run, a.steps)
        gbs = state_bytes / us * 1e6 / 1e9
        res["membrane"][blk] = {"us": round(us, 1), "GBs": round(gbs, 1)}
        print(f"  BLOCK={blk:5d}   {us:8.1f} us   {gbs:6.1f} GB/s")

    print("\nscatter_spikes, EBLOCK sweep:")
    sim.fast.cnt.zero_()
    membrane_compact[sim.fast.grid_m](
        sim.u, sim.g, sim.r, sim.tonic, sim.fast.spikes, sim.fast.cnt,
        sim.fast.over, n, sim.cap, float(sim.decay), float(sim.alpha),
        float(U_RESET), float(U_TH), float(REFRAC), float(DT),
        BLOCK=sim.fast.block)
    torch.cuda.synchronize()
    k = int(sim.fast.cnt.item())
    events = k * (len(col) / n)

    for eblk in (32, 64, 128, 256, 512):
        def run(eblk=eblk):
            scatter_spikes[(sim.cap,)](
                sim.fast.spikes, sim.fast.cnt, sim.fast.crow, sim.fast.col,
                sim.fast.val, sim.g, n, EBLOCK=eblk)

        us = timeit(run, a.steps)
        rate_g = events / us * 1e6 / 1e9
        res["scatter"][eblk] = {"us": round(us, 1), "Gevents_s": round(rate_g, 2)}
        print(f"  EBLOCK={eblk:5d}  {us:8.1f} us   {rate_g:5.2f} G synaptic events/s")

    print("\nout-degree distribution of the cells that actually spiked:")
    idx = sim.fast.spikes[:k].long()
    src = (idx % n)
    deg = (sim.crow[src + 1] - sim.crow[src]).float()
    qs = torch.tensor([0.5, 0.9, 0.99, 1.0], device=deg.device)
    q = torch.quantile(deg, qs).tolist()
    print(f"  median {q[0]:.0f}   p90 {q[1]:.0f}   p99 {q[2]:.0f}   max {q[3]:.0f}")
    print(f"  mean {deg.mean():.1f}  -> longest program does "
          f"{q[3]/max(deg.mean().item(),1):.0f}x the average work")
    res["spiking_out_degree"] = {"median": q[0], "p90": q[1], "p99": q[2],
                                 "max": q[3], "mean": float(deg.mean())}

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
