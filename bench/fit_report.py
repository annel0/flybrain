"""Read a fit's history and report what the data allows, not just its winner.

A search returns a best point. That hides the two things worth knowing when
the best point is not good enough: which targets were missed, and whether the
misses are separable. If every target is satisfiable alone but some pair never
is together, the model is not merely badly tuned -- it is the wrong model, and
the pair names the mechanism it is missing.

So this reports, over every evaluation in the history: how often each target
was met, how often each pair was met together, and the largest set of targets
any single parameter set satisfied. Those are three different questions and
only the last is answered by a best-of run.
"""

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import fit_targets as T


def band(t):
    """The target as a human reads it."""
    if "value" in t:
        return f"{t['value']:g} +- {t['tol']:g}"
    if "at_least" in t:
        return f">= {t['at_least']:g} (tol {t['tol']:g})"
    return f"<= {t['at_most']:g} (tol {t['tol']:g})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fit", nargs="?", default="out/fit2.json")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    doc = json.loads(Path(a.fit).read_text())
    hist = [h for h in doc["history"] if h.get("observables")]
    fits, holds = T.fit_targets(), T.holdout_targets()
    n = len(hist)
    print(f"{a.fit}: {len(doc['history'])} evaluations, {n} ran without error\n")

    # Per target: how many parameter sets satisfied it at all.
    ok = {t["id"]: [T.score(t, h["observables"].get(t["obs"])) <= 1.0 for h in hist]
          for t in fits}
    print("each target on its own")
    print(f"  {'target':14s} {'observable':22s} {'band':22s}  satisfied")
    for t in fits:
        c = sum(ok[t["id"]])
        print(f"  {t['id']:14s} {t['obs']:22s} {band(t):22s}  "
              f"{c:4d}/{n}  {100*c/n:5.1f}%")

    # Pairs. A pair that is never satisfied together, while each member is
    # satisfiable alone, is a conflict the parameters cannot resolve.
    print("\npairs never satisfied together (each satisfiable alone)")
    conflicts = []
    for x, y in combinations(fits, 2):
        both = sum(p and q for p, q in zip(ok[x["id"]], ok[y["id"]]))
        if both == 0 and sum(ok[x["id"]]) and sum(ok[y["id"]]):
            conflicts.append((x["id"], y["id"], sum(ok[x["id"]]), sum(ok[y["id"]])))
            print(f"  {x['id']:14s} ({sum(ok[x['id']]):3d})  x  "
                  f"{y['id']:14s} ({sum(ok[y['id']]):3d})   ->    0")
    if not conflicts:
        print("  none -- every pair is jointly satisfiable somewhere")

    # The most any one parameter set managed.
    counts = [sum(ok[t["id"]][i] for t in fits) for i in range(n)]
    best_k = max(counts)
    print(f"\nbest any single parameter set achieved: {best_k} of {len(fits)} targets")
    missed = {}
    for i, c in enumerate(counts):
        if c == best_k:
            for t in fits:
                if not ok[t["id"]][i]:
                    missed[t["id"]] = missed.get(t["id"], 0) + 1
    n_best = sum(1 for c in counts if c == best_k)
    print(f"  {n_best} parameter sets reach it; what they miss:")
    for k, v in sorted(missed.items(), key=lambda z: -z[1]):
        print(f"    {k:14s} missed by {v} of {n_best}")

    # The best point by score, with every target spelled out.
    b = min(hist, key=lambda h: h["fit_score"])
    print(f"\nbest by score: eval {b['eval']} ({b['phase']}), "
          f"fit {b['fit_score']:.3f}, holdout {b['holdout_score']:.3f}")
    print("  parameters: " + "  ".join(f"{k}={v:.4g}" for k, v in b["params"].items()))
    print(f"\n  {'target':14s} {'observable':22s} {'band':22s} {'got':>10s}  miss")
    for t in fits + holds:
        v = b["observables"].get(t["obs"])
        s = T.score(t, v)
        mark = "ok" if s <= 1.0 else f"{s:.2f}x"
        tag = "" if t["split"] == "fit" else "  (held out)"
        got = "n/a" if v is None else f"{v:.3g}"
        print(f"  {t['id']:14s} {t['obs']:22s} {band(t):22s} {got:>10s}  {mark}{tag}")

    if a.out:
        Path(a.out).write_text(json.dumps({
            "n": n,
            "per_target": {t["id"]: sum(ok[t["id"]]) for t in fits},
            "conflicts": [{"a": c[0], "b": c[1]} for c in conflicts],
            "best_simultaneous": best_k,
            "best_point": b,
        }, indent=2))
        print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
