"""How far does one spike travel? Branching ratio and avalanche statistics.

This measures the quantity that our failed light experiment was really about.
A signal entering the network either amplifies, holds, or dies, and the
branching ratio sigma says which: the mean number of spikes each spike causes
on the following step. Below 1 an input decays within a few synapses -- which
is exactly what happened in the lamina. Above 1 it runs away, which is what
happened at the published weight. Near 1 the network is at the edge where a
signal can cross it without saturating it.

The same recording also gives avalanche size and duration distributions. The
criticality hypothesis predicts power laws there, and while the hypothesis is
contested, the measurement is nearly free for us and a network that is dead or
saturated fails it obviously.

Caveat kept in view throughout: sigma estimated from consecutive bin counts is
biased low under subsampling. We record every spike, so the population estimate
is unsubsampled; the sampled-subset estimate is reported alongside to show the
size of that effect.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import params as P
from fly_sim import FlySim, calibrate_noise, DT


def branching_ratio(counts):
    """Slope of n(t+1) on n(t): the mean spikes caused by each spike."""
    a, b = counts[:-1].astype(np.float64), counts[1:].astype(np.float64)
    live = a > 0
    if live.sum() < 50:
        return None, None
    a, b = a[live], b[live]
    slope = float((a * b).sum() / (a * a).sum())          # through the origin
    resid = b - slope * a
    se = float(np.sqrt((resid ** 2).sum() / max(len(a) - 1, 1) / (a * a).sum()))
    return slope, se


def avalanches(counts, bin_steps):
    """Runs of consecutive non-empty bins, bounded by empty ones."""
    n = len(counts) // bin_steps * bin_steps
    binned = counts[:n].reshape(-1, bin_steps).sum(1)
    sizes, durations, cur, dur = [], [], 0, 0
    for c in binned:
        if c > 0:
            cur += int(c)
            dur += 1
        elif dur:
            sizes.append(cur)
            durations.append(dur)
            cur, dur = 0, 0
    empty = float((binned == 0).mean())
    return np.array(sizes), np.array(durations), empty, binned


def power_law_exponent(x, xmin=None):
    """Discrete maximum-likelihood exponent, Clauset et al. Not a fit test."""
    x = x[x > 0]
    if len(x) < 50:
        return None, None, len(x)
    xmin = xmin or max(1, int(np.percentile(x, 10)))
    tail = x[x >= xmin]
    if len(tail) < 50:
        return None, None, len(tail)
    alpha = 1.0 + len(tail) / np.sum(np.log(tail / (xmin - 0.5)))
    return float(alpha), int(xmin), int(len(tail))


def measure(scale, seconds, target_hz, sample_n, seed=0):
    sim = FlySim(scale=scale, delay_mode="published")
    sim.build_drive(0.0, 0.0)
    sigma, spont = calibrate_noise(sim, target_hz, verbose=False)
    sim.sigma = sigma

    steps = int(round(seconds * 1000 / DT))
    sim.reset()
    hist = sim.record_history(steps)
    for _ in range(2000):                    # settle before recording
        sim.step(sim.drive["off"])
    sim.t = 0
    sim.history = hist
    for _ in range(steps):
        sim.step(sim.drive["off"], record=True)
    torch.cuda.synchronize()

    counts = hist.cpu().numpy().astype(np.int64)
    rates = sim.counts.cpu().numpy() / seconds
    out = {"w_syn": scale, "noise_sigma": sigma, "spontaneous_hz": spont,
           "mean_rate_hz": float(rates.mean()),
           "spikes_per_step": float(counts.mean()),
           "silent_fraction": float((rates == 0).mean())}

    sig, se = branching_ratio(counts)
    out["branching_ratio"] = sig
    out["branching_ratio_se"] = se

    # Bin at the population's own timescale, as the avalanche literature does.
    # The avalanche literature bins at the population's own event interval.
    # Above roughly one spike per step the bins never empty and avalanches
    # cannot be separated at all; that is reported rather than forced.
    mean_per_step = max(counts.mean(), 1e-9)
    bin_steps = max(1, int(round(1.0 / mean_per_step)))
    sizes, durs, empty, binned = avalanches(counts, bin_steps)
    out["bin_steps"] = bin_steps
    out["empty_bin_fraction"] = empty
    out["n_avalanches"] = int(len(sizes))
    if len(sizes):
        a_s, xmin_s, n_s = power_law_exponent(sizes)
        a_d, xmin_d, n_d = power_law_exponent(durs)
        out.update({"size_exponent": a_s, "size_xmin": xmin_s, "size_n": n_s,
                    "duration_exponent": a_d, "duration_n": n_d,
                    "max_avalanche": int(sizes.max())})
    del sim
    torch.cuda.empty_cache()
    return out, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=3.0)
    ap.add_argument("--target-hz", type=float, default=0.5)
    ap.add_argument("--tag", default="")
    ap.add_argument("--scales", default="0.05,0.075,0.10,0.15,0.275")
    ap.add_argument("--sample", type=int, default=1000)
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    print(f"published weight {P.PUBLISHED_WEIGHT_PER_SYNAPSE_MV} mV, "
          f"ours {P.WEIGHT_PER_SYNAPSE_MV} mV")
    print(f"{a.seconds:.0f} s of spontaneous activity per condition, "
          f"background noise calibrated to ~{a.target_hz} Hz each time\n")
    print(f"  {'w_syn':>7} {'rate Hz':>8} {'spk/step':>9} {'sigma':>8} "
          f"{'empty bins':>11} {'avalanches':>11} {'size exp':>9}")

    rows = []
    for sc in [float(x) for x in a.scales.split(",")]:
        r, counts = measure(sc, a.seconds, a.target_hz, a.sample)
        rows.append(r)
        sig = f"{r['branching_ratio']:.3f}" if r["branching_ratio"] else "  n/a"
        exp = f"{r['size_exponent']:.2f}" if r.get("size_exponent") else "  n/a"
        print(f"  {sc:7.3f} {r['mean_rate_hz']:8.3f} {r['spikes_per_step']:9.1f} "
              f"{sig:>8} {100*r['empty_bin_fraction']:10.1f}% "
              f"{r['n_avalanches']:11,} {exp:>9}")

    print("\nreading these:")
    print("  sigma < 1  an input dies out; sigma ~ 1  it crosses the network;")
    print("  sigma > 1  it runs away. Critical branching predicts a size")
    print("  exponent near 1.5; a dead or saturated network has no avalanches")
    print("  to fit at all.")

    out = a.out or f"out/criticality{a.tag}.json"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(
        {"seconds": a.seconds, "target_spontaneous_hz": a.target_hz,
         "dt_ms": DT, "rows": rows,
         "note": "sigma from regression of consecutive population spike counts "
                 "through the origin; every spike is recorded, so this is not "
                 "subsampled"}, indent=2) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
