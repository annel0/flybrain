"""Where does the membrane actually sit relative to threshold?

One forced spike produces zero descendants at every weight we have tried, and
a small rate change at the photoreceptors produced almost nothing downstream.
Both follow from the same thing if the cells sit far below threshold: a
membrane that is many fluctuation-widths away from firing is insensitive to
any input short of massive synchrony.

Balanced-network theory says a working network sits the other way round --
excitation and inhibition nearly cancelling, the mean potential just below
threshold, and firing driven by the fluctuations rather than the mean. That
predicts a distance to threshold of order one standard deviation, not twenty.

This measures the distance in units of the membrane's own fluctuation, which
is the number that decides whether anything can propagate.
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
from fly_sim import FlySim, calibrate_noise, DT, U_TH


def sample_membrane(sim, settle, samples, every=25):
    sim.reset()
    for _ in range(settle):
        sim.step(sim.drive["off"])
    snap = []
    for i in range(samples * every):
        sim.step(sim.drive["off"])
        if i % every == 0:
            snap.append(sim.u.detach().clone()[0])
    torch.cuda.synchronize()
    return torch.stack(snap)          # [samples, n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="0.05,0.075,0.10,0.15,0.275")
    ap.add_argument("--target-hz", type=float, default=0.5)
    ap.add_argument("--settle", type=int, default=4000)
    ap.add_argument("--samples", type=int, default=120)
    ap.add_argument("--out", default="out/operating_point.json")
    a = ap.parse_args()

    print(f"threshold sits {U_TH:.1f} mV above rest")
    print("distance to threshold measured in each cell's own fluctuation width;")
    print("balanced-network theory expects order 1, not order 10\n")
    print(f"  {'w_syn':>7} {'spont Hz':>9} {'mean u':>8} {'sd u':>7} "
          f"{'gap mV':>8} {'gap/sd':>8} {'within 1sd':>11}")

    rows = []
    for sc in [float(x) for x in a.scales.split(",")]:
        sim = FlySim(scale=sc, delay_mode="published")
        sim.build_drive(0.0, 0.0)
        sigma, spont = calibrate_noise(sim, a.target_hz, ms=400.0, verbose=False)
        sim.sigma = sigma

        u = sample_membrane(sim, a.settle, a.samples)
        mean_u = u.mean(0)                       # per cell, over time
        sd_u = u.std(0)
        ok = sd_u > 1e-6
        gap = (U_TH - mean_u)[ok]
        z = (gap / sd_u[ok])
        within = float((z < 1).float().mean())

        row = {"w_syn": sc, "spontaneous_hz": spont, "noise_sigma": sigma,
               "mean_u_mV": float(mean_u.mean()), "sd_u_mV": float(sd_u[ok].mean()),
               "gap_mV": float(gap.mean()),
               "gap_in_sd_median": float(z.median()),
               "fraction_within_1sd": within,
               "cells_measured": int(ok.sum())}
        rows.append(row)
        print(f"  {sc:7.3f} {spont:9.3f} {row['mean_u_mV']:8.3f} "
              f"{row['sd_u_mV']:7.3f} {row['gap_mV']:8.2f} "
              f"{row['gap_in_sd_median']:8.1f} {100*within:10.1f}%")
        del sim, u
        torch.cuda.empty_cache()

    print("\n'gap/sd' is the median cell's distance to threshold in its own")
    print("fluctuation widths. At 1 or 2 a cell is responsive to its inputs;")
    print("at 10 or more it is effectively deaf, and nothing short of massive")
    print("synchrony will move it.")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"threshold_above_rest_mV": U_TH, "dt_ms": DT, "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
