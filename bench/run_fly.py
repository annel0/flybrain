"""Let the whole central nervous system run, and see what it does.

No stimulus, no body, no task: the released MaleCNS wiring with generic LIF
dynamics and a frozen per-cell background drive. This measures two things --
what it costs to advance the full graph with and without the optimised
kernels, and what the network settles into when nothing drives it.

What this is not: a fly. Cell-type-specific physiology, synaptic delays,
receptor identity beyond an excitatory/inhibitory sign, sensory input and a
body are all absent. Synaptic strength and background drive are knobs tuned
to land near a plausible mean rate, not measurements. Nothing about behaviour
follows from anything below.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph
from precision_error import Sim, calibrate, DT
from final import FinalSim


def run_recorded(sim, seconds, bin_ms=100.0):
    """Advance, keeping a population trace and a per-neuron tally."""
    steps = int(round(seconds * 1000 / DT))
    per_bin = int(round(bin_ms / DT))
    sim.counts.zero_()
    trace, last = [], 0.0
    t0 = time.perf_counter()
    for i in range(steps):
        sim.step(record=True)
        if (i + 1) % per_bin == 0:
            tot = float(sim.counts.sum())
            trace.append((tot - last) / (bin_ms / 1000.0) / sim.n)
            last = tot
    torch.cuda.synchronize()
    wall = time.perf_counter() - t0
    return sim.counts.cpu().numpy() / seconds, np.array(trace), wall


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--baseline-seconds", type=float, default=2.0)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--out", default="out/run_fly.json")
    ap.add_argument("--plot", default="out/run_fly.png")
    a = ap.parse_args()

    z = np.load(a.graph, allow_pickle=False)
    superclass = z["superclass"].astype(str)
    nt = z["nt"].astype(str)
    crow, col, val, _ = load_graph(a.graph)
    n = len(crow) - 1
    print(f"MaleCNS v1.0: {n:,} neurons, {len(col):,} directed edges")

    tonic, rate, mu = calibrate(crow, col, val, "cuda", a.scale, 5.0, 4.0, verbose=False)
    print(f"background drive tuned to mu={mu:.2f} (a knob, not a measurement)\n")

    # ---- cost, with and without the optimised kernels --------------------
    print(f"cost of {a.baseline_seconds:.0f} s of simulated time, one replica:")
    ref = Sim(crow, col, val, torch.float32, "cuda", tonic, a.scale, batch=1)
    t0 = time.perf_counter()
    ref.run(a.baseline_seconds * 1000)
    torch.cuda.synchronize()
    t_ref = time.perf_counter() - t0
    print(f"  unoptimised (torch.compile + torch scatter) {t_ref:8.2f} s wall"
          f"   {a.baseline_seconds/t_ref:6.3f}x realtime")

    fast = FinalSim(crow, col, val, torch.float32, "cuda", tonic, a.scale,
                    batch=1).setup(1 << 16, rate)
    _, _, t_fast = run_recorded(fast, a.baseline_seconds)
    print(f"  optimised kernels                           {t_fast:8.2f} s wall"
          f"   {a.baseline_seconds/t_fast:6.3f}x realtime")
    print(f"  speedup {t_ref/t_fast:.2f}x\n")

    # ---- the long run ----------------------------------------------------
    print(f"running {a.seconds:.0f} s of simulated CNS time:")
    fly = FinalSim(crow, col, val, torch.float32, "cuda", tonic, a.scale,
                   batch=1).setup(1 << 16, rate)
    rates, trace, wall = run_recorded(fly, a.seconds)
    print(f"  {wall:.1f} s wall  ({a.seconds/wall:.2f}x realtime), "
          f"overflow flag {int(fly.over.item())}")

    silent = int((rates == 0).sum())
    act = rates[rates > 0]
    print(f"\n  mean rate over all cells   {rates.mean():7.3f} Hz")
    print(f"  cells that never fired     {silent:7,} ({100*silent/n:.1f}%)")
    print(f"  of the {len(act):,} that did: median {np.median(act):.2f} Hz, "
          f"p90 {np.percentile(act,90):.1f}, p99 {np.percentile(act,99):.1f}, "
          f"max {act.max():.1f} Hz")
    drift = 100 * (trace[-10:].mean() - trace[:10].mean()) / max(trace[:10].mean(), 1e-9)
    print(f"  population rate drift, first vs last second: {drift:+.1f}% "
          f"(stability check)")

    print("\n  mean rate by superclass:")
    rows = []
    for sc in sorted(set(superclass)):
        m = superclass == sc
        if m.sum() < 50:
            continue
        rows.append((sc, int(m.sum()), float(rates[m].mean()),
                     float((rates[m] == 0).mean())))
    for sc, cnt, r, sil in sorted(rows, key=lambda x: -x[2])[:12]:
        print(f"    {sc:22s} {cnt:7,} cells  {r:6.2f} Hz  "
              f"{100*sil:5.1f}% silent")

    print("\n  mean rate by predicted transmitter:")
    for t_ in sorted(set(nt)):
        m = nt == t_
        if m.sum() < 200:
            continue
        print(f"    {t_:22s} {int(m.sum()):7,} cells  {rates[m].mean():6.2f} Hz")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(15, 4))
        ax[0].plot(np.arange(len(trace)) * 0.1, trace, lw=0.8)
        ax[0].set_xlabel("simulated seconds"); ax[0].set_ylabel("population rate, Hz")
        ax[0].set_title("Is it stable?")
        ax[1].hist(act, bins=np.logspace(-1, np.log10(max(act.max(), 1)), 60))
        ax[1].set_xscale("log"); ax[1].set_yscale("log")
        ax[1].set_xlabel("firing rate, Hz"); ax[1].set_ylabel("cells")
        ax[1].set_title(f"Rate distribution ({len(act):,} active of {n:,})")
        top = sorted(rows, key=lambda x: -x[2])[:10]
        ax[2].barh([r[0] for r in top][::-1], [r[2] for r in top][::-1])
        ax[2].set_xlabel("mean rate, Hz"); ax[2].set_title("By superclass")
        fig.tight_layout()
        Path(a.plot).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(a.plot, dpi=110)
        print(f"\nwrote {a.plot}")
    except ImportError:
        print("\n(matplotlib not installed, skipping plot)")

    Path(a.out).write_text(json.dumps(
        {"neurons": n, "edges": len(col), "sim_seconds": a.seconds,
         "wall_s": wall, "speed_x_realtime": a.seconds / wall,
         "unoptimised_x_realtime": a.baseline_seconds / t_ref,
         "optimised_x_realtime": a.baseline_seconds / t_fast,
         "speedup": t_ref / t_fast, "mean_rate_hz": float(rates.mean()),
         "silent_cells": silent, "drift_percent": float(drift),
         "by_superclass": [{"superclass": r[0], "cells": r[1],
                            "mean_hz": r[2], "silent_frac": r[3]} for r in rows]},
        indent=2) + "\n")


if __name__ == "__main__":
    main()
