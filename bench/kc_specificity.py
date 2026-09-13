"""Why the modelled mushroom body fails to tell two odours apart.

The fit's held-out target says two odours should recruit largely separate
Kenyon cells. The model recruits the same ones: at the sparseness the fit
prefers, 96% of the smaller population responds to both, where chance is 7%.

Sparseness alone does not explain that -- a model that recruited few cells at
random would score near chance. So the question is what picks the survivors.
Two candidates, and they make opposite predictions:

  a fixed ranking   the cells that fire are whichever have the most total
                    input, a property of the wiring that does not depend on
                    which odour is present. Then the two response sets are the
                    same set, and each cell's rate is predicted by its total
                    input weight alone.

  the actual wiring each Kenyon cell samples a handful of glomeruli, so the
                    cells wired to the stimulated one respond. Then the
                    difference between the two responses is predicted by the
                    difference in glomerular input, and total input says little.

Both are measured here against the same run.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fly_sim import FlySim
from observables import KC_THRESHOLD_HZ


def in_weight(sim, src_mask=None):
    """Total incoming weight per neuron, optionally only from `src_mask`."""
    col = sim.col.cpu().numpy()
    val = sim.val.cpu().numpy().astype(np.float64)
    if src_mask is not None:
        crow = sim.crow.cpu().numpy()
        keep = np.zeros(len(col), dtype=bool)
        for i in np.flatnonzero(src_mask):
            keep[crow[i]:crow[i + 1]] = True
        col, val = col[keep], val[keep]
    return np.bincount(col, weights=val, minlength=sim.n)


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--params", default="out/fit2.json")
    ap.add_argument("--glom", default="DA1")
    ap.add_argument("--second", default="VA1v")
    ap.add_argument("--seconds", type=float, default=1.0)
    ap.add_argument("--out", default="out/kc_specificity.json")
    ap.add_argument("--override", default="",
                    help="k=v,k=v applied to the fitted parameters, to ask "
                         "what a control changes")
    ap.add_argument("--label", default="best point of the fit")
    a = ap.parse_args()

    doc = json.loads(Path(a.params).read_text())
    hist = [h for h in doc["history"] if h.get("observables")]
    p = dict(min(hist, key=lambda h: h["fit_score"])["params"])
    for kv in filter(None, a.override.split(",")):
        k, v = kv.split("=")
        p[k] = float(v)
    print(f"parameters: {a.label}")
    print("  " + "  ".join(f"{k}={v:.4g}" for k, v in p.items()) + "\n")

    sim = FlySim(graph=a.graph, scale=p["w_syn"], delay_mode="published",
                 inh_gain=p["inh_gain"], tau_syn=p["tau_syn"], v_th=p["v_th"],
                 tau_mem=p["tau_mem"], tau_mem_by_type={"KC": p["tau_mem_kc"]},
                 delay_ms=p["delay_ms"])
    sim.build_drive(0.0, 0.0)
    sim.sigma = p["sigma"]
    sim.seed = 1000

    ct = sim.cell_type
    kc = np.char.startswith(ct, "KC")
    pn = np.array([c.endswith("_lPN") or c.endswith("_vPN") for c in ct])
    rates, carried = {}, {}
    for tag, glom in (("A", a.glom), ("B", a.second)):
        sim.reset()
        sim.set_poisson(np.char.startswith(ct, f"ORN_{glom}"), 150.0)
        full = np.asarray(sim.run(a.seconds * 1000)[0])
        rates[tag] = full[kc]
        carried[tag] = (float(full[pn].mean()), float(full[pn].max()),
                        float(full[kc].mean()), float(full[kc].max()))
    print("does the odour reach the mushroom body at all?")
    for tag in ("A", "B"):
        pm, px, km, kx = carried[tag]
        print(f"  odour {tag}: projection neurons mean {pm:6.2f} Hz peak {px:7.2f} Hz   "
              f"Kenyon cells mean {km:6.3f} Hz peak {kx:7.2f} Hz")
    print()
    rA, rB = rates["A"], rates["B"]
    onA, onB = rA > KC_THRESHOLD_HZ, rB > KC_THRESHOLD_HZ
    n = int(kc.sum())
    shared = int((onA & onB).sum())
    chance = onA.sum() * onB.sum() / n
    print(f"{n} Kenyon cells: {onA.sum()} respond to {a.glom}, {onB.sum()} to "
          f"{a.second}, {shared} to both ({chance:.1f} expected by chance)")
    if min(onA.sum(), onB.sum()):
        print(f"  that is {100*shared/min(onA.sum(), onB.sum()):.0f}% of the "
              f"smaller population, against {100*chance/min(onA.sum(), onB.sum()):.0f}% "
              f"by chance\n")

    # Candidate one: a fixed ranking by total input, which cannot know the odour.
    tot = in_weight(sim)[kc]
    print("does total input -- which does not depend on the odour -- predict who fires?")
    print(f"  rank correlation, total input vs response to {a.glom}:  {spearman(tot, rA):+.3f}")
    print(f"  rank correlation, total input vs response to {a.second}: {spearman(tot, rB):+.3f}")
    print(f"  rank correlation, the two responses with each other:  {spearman(rA, rB):+.3f}\n")

    # Candidate two: the glomerular wiring, which does know the odour.
    pnA = np.array([c.startswith(a.glom + "_") for c in ct])
    pnB = np.array([c.startswith(a.second + "_") for c in ct])
    wA, wB = in_weight(sim, pnA)[kc], in_weight(sim, pnB)[kc]
    print(f"does the wiring to the stimulated glomerulus predict the difference?")
    print(f"  Kenyon cells with any input from {a.glom}: {int((wA>0).sum())}, "
          f"from {a.second}: {int((wB>0).sum())}")
    print(f"  rank correlation, ({a.glom} input - {a.second} input) vs "
          f"(response A - response B): {spearman(wA - wB, rA - rB):+.3f}")
    for tag, w, r, other in (("A", wA, rA, rB), ("B", wB, rB, rA)):
        wired = w > 0
        if wired.any():
            print(f"  cells wired to {tag}: {100*float((r[wired]>KC_THRESHOLD_HZ).mean()):5.1f}% respond, "
                  f"unwired: {100*float((r[~wired]>KC_THRESHOLD_HZ).mean()):5.1f}%")

    res = dict(label=a.label, n_kc=n, on_a=int(onA.sum()), on_b=int(onB.sum()), shared=shared,
               chance=float(chance),
               rho_total_a=spearman(tot, rA), rho_total_b=spearman(tot, rB),
               rho_a_b=spearman(rA, rB), rho_wiring_diff=spearman(wA - wB, rA - rB),
               params=p)
    Path(a.out).write_text(json.dumps(res, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
