"""The fair version: give the rewired network the same tuning opportunity.

The first control found every measurement collapsing to zero on a rewired
graph, which is suspicious on its own -- a network that is simply dead fails
every test trivially, and that would say nothing about wiring.

Checking the input statistics ruled that reading out: rewiring *raises* the
median neuron's net drive, from +29 to +107, because the real graph is skewed
and a permutation evens it out. The nulls are not starved. But the weight was
fitted on the real graph, and a parameter that does not transfer between two
graphs is a weak result.

So this matches the two on activity before comparing them. The null's weight
is raised until it sustains the same spontaneous rate as the real network, and
only then are the specific measurements taken. If selectivity and Kenyon cell
recruitment come back at matched activity, the connectome was contributing
excitability. If they stay absent while the network is just as alive, the
connectome is contributing the specific paths, which is a much stronger claim.
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
from rewire import rewire


def write_graph(z, crow, new_col, path):
    np.savez(path, crow=crow, col=new_col.astype(np.int32), val=z["val"],
             ids=z["ids"], sign=z["sign"], nt=z["nt"], superclass=z["superclass"],
             cell_type=z["cell_type"], xyz=z["xyz"], cell_class=z["cell_class"],
             subclass=z["subclass"], neuromere=z["neuromere"], side=z["side"],
             receptor=z["receptor"], hex1=z["hex1"], hex2=z["hex2"])


def self_rate(sim, ms=400.0):
    sim.reset()
    sim.sigma = 0.0
    rng = np.random.default_rng(0)
    kick = np.zeros(sim.n, dtype=bool)
    kick[rng.choice(sim.n, int(sim.n * 0.02), replace=False)] = True
    sim.set_poisson(kick, 100.0)
    sim.run(50.0)
    sim.force.zero_()
    r = sim.run(ms)[0]
    return float(r.mean()), float((r > 0.1).mean())


def specifics(sim, glom, seconds):
    ct = sim.cell_type
    orn = np.char.startswith(ct, f"ORN_{glom}")
    kc = np.char.startswith(ct, "KC")
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
    # Undefined rather than enormous when every other projection neuron is
    # silent: dividing by a floor produced a meaningless 2e8 in an earlier run.
    med = float(np.median(others)) if others else 0.0
    sel = (max(own) / med) if (own and med > 0.01) else float("nan")
    return {"kc_recruited_pct": 100 * float((r[kc] > 1.0).mean()),
            "own_glomerulus_selectivity": sel,
            "network_mean_hz": float(r[~orn].mean()),
            "downstream_of_driven_hz": float(r[~orn].mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--seconds", type=float, default=1.0)
    ap.add_argument("--sweep", default="0.075,0.1,0.15,0.25,0.4,0.6,1.0,1.5")
    ap.add_argument("--out", default="out/rewire_matched.json")
    a = ap.parse_args()

    z = np.load(a.graph, allow_pickle=False)
    crow, col = z["crow"], z["col"].astype(np.int64)
    sc = z["superclass"].astype(str)
    classes = {s: i for i, s in enumerate(np.unique(sc))}
    sc_idx = np.array([classes[s] for s in sc])

    sim = FlySim(graph=a.graph, scale=a.scale, delay_mode="published")
    sim.build_drive(0.0, 0.0)
    real_rate, real_active = self_rate(sim)
    real_spec = specifics(sim, a.glomerulus, a.seconds)
    print(f"real graph at w_syn {a.scale}: self-sustained {real_rate:.3f} Hz "
          f"({100*real_active:.1f}% active), KC {real_spec['kc_recruited_pct']:.1f}%, "
          f"selectivity {real_spec['own_glomerulus_selectivity']:.2f}x")
    del sim
    torch.cuda.empty_cache()

    tmp = Path("out/_rewired_matched.npz")
    rows = [{"condition": "real", "w_syn": a.scale, "self_hz": real_rate,
             "active_pct": 100 * real_active, **real_spec}]

    for mode, name in (("config", "degree-preserved"), ("superclass", "superclass-preserved")):
        new_col = rewire(crow, col, mode, sc_idx, 0)
        write_graph(z, crow, new_col, tmp)
        print(f"\n{name} null: does a weight exist that gives {real_rate:.3f} Hz?")
        # Bisection rather than a coarse sweep. The earlier run jumped from
        # 0.09 Hz to 41.6 Hz between two sweep points, so the question is
        # whether an intermediate state exists at all, not where it is.
        lo, hi, best, trace = 0.05, 2.0, None, []
        for _ in range(16):
            w = (lo + hi) / 2
            s = FlySim(graph=str(tmp), scale=w, delay_mode="published")
            s.build_drive(0.0, 0.0)
            rate, active = self_rate(s)
            trace.append({"w_syn": w, "self_hz": rate, "active_pct": 100 * active})
            print(f"    w_syn {w:7.4f} -> {rate:9.3f} Hz ({100*active:5.1f}% active)")
            if best is None or abs(rate - real_rate) < abs(best[1] - real_rate):
                best = (w, rate, active)
            del s
            torch.cuda.empty_cache()
            if rate < real_rate:
                lo = w
            else:
                hi = w
            if abs(rate - real_rate) < real_rate * 0.25:
                break

        w, rate, active = best
        s = FlySim(graph=str(tmp), scale=w, delay_mode="published")
        s.build_drive(0.0, 0.0)
        spec = specifics(s, a.glomerulus, a.seconds)
        print(f"  matched at w_syn {w} ({rate:.3f} Hz vs real {real_rate:.3f}): "
              f"KC {spec['kc_recruited_pct']:.1f}%, "
              f"selectivity {spec['own_glomerulus_selectivity']:.2f}x")
        rows.append({"condition": f"{name}, activity-matched", "w_syn": w,
                     "self_hz": rate, "active_pct": 100 * active,
                     "bisection_trace": trace, "matched": bool(
                         abs(rate - real_rate) < real_rate * 0.5), **spec})
        del s
        torch.cuda.empty_cache()

    print("\nat matched spontaneous activity:")
    for r in rows:
        print(f"  {r['condition']:34s} w {r['w_syn']:5.3f}  self {r['self_hz']:6.3f} Hz"
              f"   KC {r['kc_recruited_pct']:5.1f}%   "
              f"selectivity {r['own_glomerulus_selectivity']:5.2f}x"
              + ("" if r.get("matched", True) else "   [NO MATCHING WEIGHT FOUND]"))

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"glomerulus": a.glomerulus, "rows": rows},
                                      indent=2) + "\n")
    tmp.unlink(missing_ok=True)
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
