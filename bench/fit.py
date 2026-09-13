"""Fit the parameters we do not know against the quantities that are measured.

Search is gradient-free because the simulator is not differentiable end to end,
and noisy because the response depends on the network's ongoing state -- which
we measured at a coefficient of variation of 36-54%. Each candidate is
therefore evaluated over several seeds and scored on the median.

What comes out is not one parameter set but the whole population of evaluated
points, so the *set* that satisfies every target can be reported rather than a
single winner. That matters here: many different parameter sets produce the
same circuit output, and a search returning one point would hide that.

Held-out targets are never scored during the search and are reported at the
end. A fit that improves on its own targets while getting worse on held-out
ones is overfitting, and that is visible only if the split is kept.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import fit_targets as T
from fly_sim import FlySim
from observables import observe


def decode(x):
    """Unit cube to named parameters, respecting log-scaled dimensions."""
    p = {}
    for xi, spec in zip(x, T.PARAMS):
        if spec["log"]:
            lo, hi = np.log(spec["lo"]), np.log(spec["hi"])
            p[spec["name"]] = float(np.exp(lo + xi * (hi - lo)))
        else:
            p[spec["name"]] = float(spec["lo"] + xi * (spec["hi"] - spec["lo"]))
    return p


def build(params, graph, seed):
    sim = FlySim(graph=graph, scale=params["w_syn"], delay_mode="published",
                 inh_gain=params["inh_gain"], tau_syn=params["tau_syn"],
                 v_th=params["v_th"], tau_mem=params["tau_mem"],
                 tau_mem_by_type={"KC": params["tau_mem_kc"]},
                 delay_ms=params["delay_ms"])
    sim.build_drive(0.0, 0.0)
    sim.sigma = params["sigma"]
    sim.seed = 1000 + 97 * seed
    return sim


def evaluate(params, graph, seeds, seconds):
    """Median observables over seeds, plus the fit and holdout scores."""
    runs = []
    for s in range(seeds):
        try:
            sim = build(params, graph, s)
            runs.append(observe(sim, seconds=seconds))
            del sim
            torch.cuda.empty_cache()
        except Exception as exc:                   # a bad corner of the space
            return None, float("inf"), float("inf"), str(exc)
    obs = {k: float(np.median([r[k] for r in runs])) for k in runs[0]}
    fit = float(np.mean([T.score(t, obs.get(t["obs"])) for t in T.fit_targets()]))
    hold = float(np.mean([T.score(t, obs.get(t["obs"])) for t in T.holdout_targets()]))
    return obs, fit, hold, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--budget", type=int, default=120)
    ap.add_argument("--population", type=int, default=12)
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--seconds", type=float, default=0.6)
    ap.add_argument("--sigma0", type=float, default=0.30)
    ap.add_argument("--out", default="out/fit.json")
    a = ap.parse_args()

    d = len(T.PARAMS)
    print(f"{d} parameters, {len(T.fit_targets())} targets to fit, "
          f"{len(T.holdout_targets())} held out")
    for spec in T.PARAMS:
        print(f"   {spec['name']:12s} [{spec['lo']:g}, {spec['hi']:g}]"
              f"{' log' if spec['log'] else ''}   {spec['note']}")
    print(f"\nbudget {a.budget} evaluations, {a.seeds} seeds each, "
          f"{a.seconds:g} s per run\n")

    rng = np.random.default_rng(0)
    mean = np.full(d, 0.5)
    sigma = a.sigma0
    history, best = [], None
    used, t0 = 0, time.perf_counter()

    while used < a.budget:
        pop = np.clip(mean + sigma * rng.standard_normal((a.population, d)), 0, 1)
        scored = []
        for x in pop:
            if used >= a.budget:
                break
            params = decode(x)
            obs, fit, hold, err = evaluate(params, a.graph, a.seeds, a.seconds)
            used += 1
            rec = {"eval": used, "x": x.tolist(), "params": params,
                   "fit_score": fit, "holdout_score": hold,
                   "observables": obs, "error": err}
            history.append(rec)
            scored.append((fit, x))
            if best is None or fit < best["fit_score"]:
                best = rec
                print(f"  [{used:4d}] fit {fit:7.3f}  holdout {hold:7.3f}   "
                      + "  ".join(f"{k}={v:.3g}" for k, v in params.items()))
        if not scored:
            break
        scored.sort(key=lambda z: z[0])
        elite = np.array([x for _, x in scored[:max(2, len(scored) // 3)]])
        mean = elite.mean(0)
        sigma = max(0.05, sigma * 0.85)

    wall = time.perf_counter() - t0
    print(f"\n{used} evaluations in {wall/60:.1f} min "
          f"({wall/max(used,1):.1f} s each)")

    ok = [h for h in history if h["observables"]]
    feasible = [h for h in ok
                if all(T.score(t, h["observables"].get(t["obs"])) <= 1.0
                       for t in T.fit_targets())]
    print(f"parameter sets satisfying every fitted target: {len(feasible)} "
          f"of {len(ok)}")
    if feasible:
        print("  the feasible range of each parameter (this is the degeneracy):")
        for spec in T.PARAMS:
            v = np.array([h["params"][spec["name"]] for h in feasible])
            span = v.max() / max(v.min(), 1e-12)
            print(f"    {spec['name']:12s} {v.min():9.3g} .. {v.max():9.3g}"
                  f"   ({span:5.1f}x)   prior span "
                  f"{spec['hi']/max(spec['lo'],1e-12):.0f}x")

    if best:
        print(f"\nbest fitted score {best['fit_score']:.3f}, "
              f"held-out score at that point {best['holdout_score']:.3f}")
        print("  target by target:")
        for t in T.fit_targets() + T.holdout_targets():
            v = best["observables"].get(t["obs"])
            s = T.score(t, v)
            want = (f"= {t['value']}" if "value" in t else
                    f">= {t['at_least']}" if "at_least" in t else
                    f"<= {t['at_most']}")
            flag = "fit " if t["split"] == "fit" else "HELD"
            print(f"    [{flag}] {t['id']:12s} {t['obs']:24s} "
                  f"got {v:9.3g}  want {want:>10}  miss {s:5.2f}")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"params": T.PARAMS, "targets": T.TARGETS, "evaluations": used,
         "wall_s": wall, "best": best, "feasible_count": len(feasible),
         "history": history}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
