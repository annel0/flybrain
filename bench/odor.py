"""Present an odour and follow it through a pathway that actually spikes.

Vision was the wrong entry point for this model, and not by our mistake: the
fly's early visual system is largely non-spiking. Photoreceptors and the
lamina monopolar cells L1-L3 signal with graded potentials, so a leaky
integrate-and-fire network cannot represent them. That is why the published
spiking model of this brain was validated on taste and grooming, and why the
visual system has its own model built from graded units instead.

The olfactory pathway does spike, all the way through: receptor neurons ->
projection neurons -> Kenyon cells. This drives one glomerulus' receptor
neurons as a Poisson source, exactly as optogenetic activation is modelled in
the source paper, and reports what responds -- with the sparseness of the
Kenyon cell response as the check, since a given odour is expected to recruit
only a small percentage of them.
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
from fly_sim import FlySim, DT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--rate", type=float, default=P.POISSON_RATE_HZ)
    ap.add_argument("--seconds", type=float, default=1.0)
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--out", default="out/odor.json")
    a = ap.parse_args()

    sim = FlySim(scale=a.scale, delay_mode="published")
    ct = sim.cell_type
    orn = np.char.startswith(ct, f"ORN_{a.glomerulus}")
    kc = np.char.startswith(ct, "KC")
    print(f"{P.CITATION}")
    print(f"w_syn {a.scale} mV, delay {P.DELAY_MS} ms, no background noise\n")
    print(f"driving ORN_{a.glomerulus}: {int(orn.sum())} receptor neurons "
          f"at {a.rate:.0f} Hz Poisson")
    if not orn.sum():
        avail = sorted({c for c in ct if c.startswith("ORN_")})[:20]
        print(f"  no such glomerulus. available: {avail}")
        return

    sim.build_drive(0.0, 0.0)
    sim.sigma = 0.0

    sim.reset()
    sim.set_poisson(None if True else orn, 0.0)
    base, _, _, _ = sim.run(a.seconds * 1000)

    sim.reset()
    sim.set_poisson(orn, a.rate)
    resp, _, _, _ = sim.run(a.seconds * 1000)

    d = resp - base
    print(f"\nmean rate: baseline {base.mean():.3f} Hz -> {resp.mean():.3f} Hz")

    print("\ncell types that responded most (driven cells excluded):")
    mask = ~orn
    types = np.unique(ct[mask])
    rows = []
    for t_ in types:
        m = (ct == t_) & mask
        if m.sum() < 4:
            continue
        rows.append((t_, int(m.sum()), float(d[m].mean()), float(resp[m].mean())))
    rows.sort(key=lambda r: -r[2])
    for t_, k, dd, rr in rows[:16]:
        print(f"   {t_:22s} {k:5d} cells  {dd:+8.2f} Hz   (now {rr:6.2f} Hz)")

    n_kc = int(kc.sum())
    kc_active = int((resp[kc] > 1.0).sum())
    print(f"\nKenyon cells: {kc_active:,} of {n_kc:,} above 1 Hz "
          f"({100*kc_active/max(n_kc,1):.1f}%)  mean {resp[kc].mean():.3f} Hz")
    print("  (a given odour is expected to recruit a small percentage of them)")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"glomerulus": a.glomerulus, "orn_cells": int(orn.sum()),
         "poisson_hz": a.rate, "weight_per_synapse_mV": a.scale,
         "baseline_mean_hz": float(base.mean()), "response_mean_hz": float(resp.mean()),
         "kenyon_cells": n_kc, "kenyon_active": kc_active,
         "kenyon_active_percent": 100 * kc_active / max(n_kc, 1),
         "top_responders": [{"type": t, "cells": k, "delta_hz": dd}
                            for t, k, dd, _ in rows[:25]],
         "source": P.CITATION}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
