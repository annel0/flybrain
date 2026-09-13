"""Make the antennal lobe local interneurons graded and see what changes.

Prediction being tested: our local interneurons run at ~350 Hz and smear
activity across glomeruli, leaving only a 2-6x preference for the driven one.
If that smearing is an artefact of forcing non-spiking cells to spike, making
them graded should sharpen the labelled line.

The honest uncertainty is which cells to convert. The paper identifying
non-spiking local interneurons characterises one population and does not
quantify what fraction of all local interneurons is non-spiking, so the
fraction is swept here rather than assumed. Converting all of them is an upper
bound on the effect, not a claim about the animal.
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


def measure(sim, glom, seconds):
    ct = sim.cell_type
    orn = np.char.startswith(ct, f"ORN_{glom}")
    kc = np.char.startswith(ct, "KC")
    ln = np.char.startswith(ct, "lLN") | np.char.startswith(ct, "vLN")
    sim.reset()
    sim.sigma = 0.0
    sim.set_poisson(orn, P.POISSON_RATE_HZ)
    r = sim.run(seconds * 1000)[0]

    pn = sorted({c for c in ct if c.endswith("_lPN") or c.endswith("_vPN")})
    own, others = [], []
    for t_ in pn:
        m = ct == t_
        if m.sum() >= 2:
            (own if t_.startswith(glom + "_") else others).append(float(r[m].mean()))
    med = float(np.median(others)) if others else 0.0
    sel = (max(own) / med) if (own and med > 0.01) else float("nan")
    return {"ln_rate_hz": float(r[ln].mean()) if ln.any() else 0.0,
            "own_pn_hz": max(own) if own else 0.0,
            "median_other_pn_hz": med,
            "selectivity": sel,
            "kc_recruited_pct": 100 * float((r[kc] > 1.0).mean()),
            "network_mean_hz": float(r[~orn].mean()),
            "max_rate_hz": float(r[~orn].max())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--seconds", type=float, default=1.0)
    ap.add_argument("--fractions", default="0,1.0")
    ap.add_argument("--reference-hz", type=float, default=50.0)
    ap.add_argument("--gain-sweep", default="",
                    help="reference-Hz values to sweep at 100%% graded, to "
                         "match the inhibition the spiking version delivered")
    ap.add_argument("--out", default="out/graded_ln.json")
    a = ap.parse_args()

    sim = FlySim(scale=a.scale, delay_mode="published")
    ct = sim.cell_type
    ln = np.char.startswith(ct, "lLN") | np.char.startswith(ct, "vLN")
    ln_idx = np.flatnonzero(ln)
    sim.build_drive(0.0, 0.0)
    print(f"antennal lobe local interneurons found: {len(ln_idx):,}")
    print(f"driving ORN_{a.glomerulus}, graded cells release at "
          f"{a.reference_hz:.0f} Hz when at spike threshold\n")
    print(f"  {'graded':>8} {'n':>5} {'LN rate':>9} {'own PN':>8} "
          f"{'other PN':>9} {'selectivity':>12} {'KC %':>6} {'max Hz':>8}")

    rng = np.random.default_rng(0)
    rows = []
    for frac in [float(x) for x in a.fractions.split(",")]:
        k = int(round(frac * len(ln_idx)))
        mask = np.zeros(sim.n, dtype=bool)
        if k:
            mask[rng.choice(ln_idx, k, replace=False)] = True
        n_graded = sim.set_graded(mask if k else None, a.reference_hz)
        r = measure(sim, a.glomerulus, a.seconds)
        rows.append({"graded_fraction": frac, "n_graded": n_graded, **r})
        sel = f"{r['selectivity']:.2f}x" if np.isfinite(r["selectivity"]) else "undefined"
        print(f"  {100*frac:7.0f}% {n_graded:5d} {r['ln_rate_hz']:9.1f} "
              f"{r['own_pn_hz']:8.1f} {r['median_other_pn_hz']:9.1f} "
              f"{sel:>12} {r['kc_recruited_pct']:5.1f}% {r['max_rate_hz']:8.1f}")

    if a.gain_sweep:
        base = rows[0]
        print(f"\nthe first run conflated two changes: making the cells graded,")
        print(f"and weakening them. The spiking version ran at "
              f"{base['ln_rate_hz']:.0f} Hz while a graded cell at threshold was")
        print(f"set to release at only {a.reference_hz:.0f} Hz, so their")
        print(f"inhibition was cut several-fold. Sweeping the gain to restore it:\n")
        print(f"  {'ref Hz':>8} {'own PN':>8} {'other PN':>9} {'selectivity':>12} "
              f"{'KC %':>6} {'net Hz':>8}")
        mask = np.zeros(sim.n, dtype=bool)
        mask[ln_idx] = True
        for ref in [float(x) for x in a.gain_sweep.split(",")]:
            sim.set_graded(mask, ref)
            r = measure(sim, a.glomerulus, a.seconds)
            rows.append({"graded_fraction": 1.0, "reference_hz": ref,
                         "n_graded": len(ln_idx), **r})
            sel = f"{r['selectivity']:.2f}x" if np.isfinite(r["selectivity"]) else "undefined"
            print(f"  {ref:8.0f} {r['own_pn_hz']:8.1f} {r['median_other_pn_hz']:9.1f} "
                  f"{sel:>12} {r['kc_recruited_pct']:5.1f}% {r['network_mean_hz']:8.3f}")
        print(f"\n  spiking baseline for comparison: own PN {base['own_pn_hz']:.1f}, "
              f"other {base['median_other_pn_hz']:.1f}, "
              f"selectivity {base['selectivity']:.2f}x, "
              f"KC {base['kc_recruited_pct']:.1f}%, net {base['network_mean_hz']:.3f} Hz")
        print("\nread the row whose KC recruitment and network rate sit closest")
        print("to the spiking baseline: that is the matched comparison, and its")
        print("selectivity is the answer to whether graded release sharpens the")
        print("labelled line.")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"glomerulus": a.glomerulus, "w_syn": a.scale,
         "reference_hz": a.reference_hz, "local_interneurons": len(ln_idx),
         "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
