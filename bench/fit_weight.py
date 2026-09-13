"""Refit the one parameter that was never measured.

Six of the seven constants in the published model carry citations to
measurements and transfer unchanged. The seventh, weight per synapse, is
labelled "Free parameter" in that model's own source: it was fitted, and it
was fitted against FlyWire.

This dataset is not FlyWire. MaleCNS retains every released connection at
confidence 0.5, including the single-synapse ones -- 25.6M connections, mean
out-degree 153.5 against roughly 72 -- so one spike distributes about 120 mV
across its targets at the published weight, against a 7 mV threshold. It
cannot help but run away, and it did: 100% of Kenyon cells at 195 Hz.

So the weight is refitted here against a measured invariant rather than
guessed: an odour recruits only a small percentage of Kenyon cells. Sparse
coding in the mushroom body is exactly the kind of target a free parameter
should be fitted to, and it is independent of the quantity being fitted.
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
from fly_sim import FlySim


def probe(crow_scale, glom, seconds, rate, threshold_syn):
    sim = FlySim(scale=crow_scale, delay_mode="published",
                 min_synapses=threshold_syn)
    ct = sim.cell_type
    orn = np.char.startswith(ct, f"ORN_{glom}")
    kc = np.char.startswith(ct, "KC")
    sim.build_drive(0.0, 0.0)
    sim.sigma = 0.0
    sim.reset()
    sim.set_poisson(orn, rate)
    rates, _, _, _ = sim.run(seconds * 1000)
    active = float((rates[kc] > 1.0).mean())
    return {"kc_active_frac": active, "kc_mean_hz": float(rates[kc].mean()),
            "net_mean_hz": float(rates[~orn].mean()),
            "max_hz": float(rates[~orn].max())}, sim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--seconds", type=float, default=0.5)
    ap.add_argument("--rate", type=float, default=P.POISSON_RATE_HZ)
    ap.add_argument("--min-synapses", type=int, default=1,
                    help="drop connections weaker than this (FlyWire convention is 5)")
    ap.add_argument("--scales", default="0.275,0.1,0.05,0.02,0.01,0.005,0.002,0.001")
    ap.add_argument("--out", default="out/fit_weight.json")
    a = ap.parse_args()

    print(f"target: an odour should recruit a few percent of Kenyon cells")
    print(f"driving ORN_{a.glomerulus} at {a.rate:.0f} Hz, "
          f"connection threshold >={a.min_synapses} synapses\n")
    print(f"  {'w_syn mV':>9}  {'KC active':>10}  {'KC mean':>9}  "
          f"{'net mean':>9}  {'max':>8}")
    rows = []
    for sc in [float(x) for x in a.scales.split(",")]:
        r, sim = probe(sc, a.glomerulus, a.seconds, a.rate, a.min_synapses)
        rows.append({"w_syn": sc, **r})
        print(f"  {sc:9.4f}  {100*r['kc_active_frac']:9.1f}%  "
              f"{r['kc_mean_hz']:8.2f}  {r['net_mean_hz']:8.3f}  "
              f"{r['max_hz']:7.1f}")
        del sim
        torch.cuda.empty_cache()

    ok = [r for r in rows if 0.02 <= r["kc_active_frac"] <= 0.15]
    if ok:
        best = min(ok, key=lambda r: abs(r["kc_active_frac"] - 0.06))
        print(f"\nclosest to sparse coding: w_syn = {best['w_syn']} mV "
              f"({100*best['kc_active_frac']:.1f}% of Kenyon cells)")
    else:
        print("\nno scale in this sweep lands in the sparse range")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"glomerulus": a.glomerulus, "poisson_hz": a.rate,
         "min_synapses": a.min_synapses, "rows": rows,
         "published_w_syn": P.WEIGHT_PER_SYNAPSE_MV,
         "note": "published weight was fitted against FlyWire, not this dataset"},
        indent=2) + "\n")


if __name__ == "__main__":
    main()
