"""Does the real connectome do anything a degree-matched random graph doesn't?

Runs the measurements we have been reporting on the real wiring and on two
degree-preserving rewirings. If the rewired networks reproduce them, we have
been measuring the degree distribution rather than the connectome, and every
result in the lab notebook needs rereading.

The measurements are the ones we have leaned on:
  - Kenyon cell recruitment under stimulation of one glomerulus' receptor cells
  - the collapse of that sparseness when APL's output is blocked, which is the
    one causal validation this model has passed
  - selectivity of the matching projection neuron for its own glomerulus
  - the level of self-sustained activity
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
from rewire import rewire, check


def measure(sim, glom, seconds, poisson_hz):
    ct = sim.cell_type
    orn = np.char.startswith(ct, f"ORN_{glom}")
    kc = np.char.startswith(ct, "KC")
    apl = np.char.startswith(ct, "APL")
    sim.build_drive(0.0, 0.0)
    sim.sigma = 0.0

    sim.reset()
    sim.set_poisson(orn, poisson_hz)
    r = sim.run(seconds * 1000)[0]

    # Same APL block as the regression test: zero its outgoing weights.
    crow = sim.crow.cpu().numpy().astype(np.int64)
    mask = torch.zeros_like(sim.val, dtype=torch.bool)
    for i in np.flatnonzero(apl):
        mask[crow[i]:crow[i + 1]] = True
    saved = sim.val[mask].clone()
    sim.val[mask] = 0.0
    sim.reset()
    sim.set_poisson(orn, poisson_hz)
    r_noapl = sim.run(seconds * 1000)[0]
    sim.val[mask] = saved

    # Glomerular selectivity: does the matching projection neuron lead?
    pn_types = sorted({c for c in ct if c.endswith("_lPN") or c.endswith("_vPN")})
    own, others = [], []
    for t_ in pn_types:
        m = ct == t_
        if m.sum() >= 2:
            (own if t_.startswith(glom + "_") else others).append(float(r[m].mean()))
    sel = (max(own) / max(np.median(others), 1e-9)) if own and others else float("nan")

    # Self-sustained activity with nothing driving it.
    sim.reset()
    rng = np.random.default_rng(0)
    kick = np.zeros(sim.n, dtype=bool)
    kick[rng.choice(sim.n, int(sim.n * 0.02), replace=False)] = True
    sim.set_poisson(kick, 100.0)
    sim.run(50.0)
    sim.force.zero_()
    r_self = sim.run(400.0)[0]

    kc_intact = 100 * float((r[kc] > 1.0).mean())
    kc_blocked = 100 * float((r_noapl[kc] > 1.0).mean())
    return {"kc_recruited_pct": kc_intact,
            "kc_recruited_apl_blocked_pct": kc_blocked,
            "apl_effect_pp": kc_blocked - kc_intact,
            "own_glomerulus_selectivity": sel,
            "apl_rate_hz": float(r[apl].mean()),
            "network_mean_hz": float(r[~orn].mean()),
            "self_sustained_hz": float(r_self.mean()),
            "self_sustained_active_pct": 100 * float((r_self > 0.1).mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--inh-gain", type=float, default=1.0)
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--seconds", type=float, default=1.0)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--out", default="out/rewire_control.json")
    a = ap.parse_args()

    z = np.load(a.graph, allow_pickle=False)
    crow, col = z["crow"], z["col"].astype(np.int64)
    superclass = z["superclass"].astype(str)
    n = len(crow) - 1
    classes = {s: i for i, s in enumerate(np.unique(superclass))}
    sc_idx = np.array([classes[s] for s in superclass])

    print(f"{n:,} neurons, {len(col):,} connections, w_syn {a.scale} mV, "
          f"inhibitory gain x{a.inh_gain:g}")
    print(f"driving ORN_{a.glomerulus} at {P.POISSON_RATE_HZ:.0f} Hz\n")

    conditions = [("real", "none", 0)]
    for s in range(a.seeds):
        conditions.append((f"rewired, superclass-preserved #{s+1}", "superclass", s))
    for s in range(a.seeds):
        conditions.append((f"rewired, degree-preserved #{s+1}", "config", s))

    rows = []
    for label, mode, seed in conditions:
        new_col = rewire(crow, col, mode, sc_idx, seed)
        if mode != "none":
            chk = check(crow, col, new_col, n)
            if not chk["in_degree_identical"]:
                raise RuntimeError(f"{label}: in-degree not preserved")
        else:
            chk = {"edges_unchanged_pct": 100.0}

        tmp = Path("out/_rewired.npz")
        np.savez(tmp, crow=crow, col=new_col.astype(np.int32), val=z["val"],
                 ids=z["ids"], sign=z["sign"], nt=z["nt"], superclass=z["superclass"],
                 cell_type=z["cell_type"], xyz=z["xyz"], cell_class=z["cell_class"],
                 subclass=z["subclass"], neuromere=z["neuromere"], side=z["side"],
                 receptor=z["receptor"], hex1=z["hex1"], hex2=z["hex2"])
        sim = FlySim(graph=str(tmp), scale=a.scale, delay_mode="published",
                     inh_gain=a.inh_gain)
        r = measure(sim, a.glomerulus, a.seconds, P.POISSON_RATE_HZ)
        r["condition"] = label
        r["edges_unchanged_pct"] = chk["edges_unchanged_pct"]
        rows.append(r)
        print(f"  {label:36s} KC {r['kc_recruited_pct']:5.1f}%  "
              f"APL-block {r['apl_effect_pp']:+6.1f}pp  "
              f"selectivity {r['own_glomerulus_selectivity']:5.2f}x  "
              f"self {r['self_sustained_hz']:5.2f} Hz")
        del sim
        torch.cuda.empty_cache()

    real = rows[0]
    print("\nthe real wiring against each null (mean over seeds):")
    for mode, name in (("superclass-preserved", "superclass"),
                       ("degree-preserved", "degree")):
        sel = [r for r in rows if mode in r["condition"]]
        if not sel:
            continue
        for key, label in (("kc_recruited_pct", "KC recruited"),
                           ("apl_effect_pp", "APL block effect"),
                           ("own_glomerulus_selectivity", "own-glomerulus selectivity"),
                           ("self_sustained_hz", "self-sustained rate")):
            v = np.array([r[key] for r in sel], dtype=float)
            print(f"  {label:26s} real {real[key]:8.2f}   {name} null "
                  f"{np.nanmean(v):8.2f} +- {np.nanstd(v):5.2f}")
        print()

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"neurons": n, "edges": len(col),
                                       "w_syn": a.scale, "inh_gain": a.inh_gain,
                                       "glomerulus": a.glomerulus, "rows": rows},
                                      indent=2) + "\n")
    Path("out/_rewired.npz").unlink(missing_ok=True)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
