"""Is the measurement reading a state, or a transient?

Every observable in observables.py is counted from sim.reset(), which zeroes
every membrane potential. That is not rest -- it is a brain that has never been
switched on. If the network needs time to reach its own steady state, then what
we counted is the settling transient, and the parameters were fitted to it.

This measures the thing directly: the same observables in successive windows,
from reset outward, at rest and during an odour. If the numbers are flat, the
protocol was fine. If they drift, every target in the fit was scored against
the wrong state.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fly_sim import FlySim
from observables import KC_THRESHOLD_HZ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--params", default="out/fit2.json")
    ap.add_argument("--glom", default="DA1")
    ap.add_argument("--bin", type=float, default=250.0)
    ap.add_argument("--total", type=float, default=4000.0)
    ap.add_argument("--override", default="")
    ap.add_argument("--out", default="out/state_check.json")
    a = ap.parse_args()

    doc = json.loads(Path(a.params).read_text())
    hist = [h for h in doc["history"] if h.get("observables")]
    p = dict(min(hist, key=lambda h: h["fit_score"])["params"])
    for kv in filter(None, a.override.split(",")):
        k, v = kv.split("="); p[k] = float(v)
    print("  " + "  ".join(f"{k}={v:.4g}" for k, v in p.items()))
    print(f"  windows of {a.bin:g} ms out to {a.total:g} ms, counted from reset\n")

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
    orn = np.char.startswith(ct, f"ORN_{a.glom}")

    res = {}
    for cond in ("rest", "odour"):
        sim.reset()
        sim.set_poisson(orn if cond == "odour" else None,
                        150.0 if cond == "odour" else 0.0)
        _, frames, _, _ = sim.run(a.total, record_bin_ms=a.bin)
        rows = []
        print(f"{cond}:")
        print(f"  {'window ms':>14s} {'whole brain Hz':>15s} {'silent %':>9s} "
              f"{'PN peak Hz':>11s} {'KC %':>7s} {'KC Hz':>8s}")
        for i, f in enumerate(frames):
            row = dict(t0=i * a.bin, t1=(i + 1) * a.bin,
                       net_hz=float(f[~orn].mean()),
                       silent_pct=100.0 * float((f == 0).mean()),
                       pn_peak_hz=float(f[pn].max()) if pn.any() else 0.0,
                       kc_pct=100.0 * float((f[kc] > KC_THRESHOLD_HZ).mean()),
                       kc_hz=float(f[kc].mean()))
            rows.append(row)
            if i < 4 or (i + 1) % 4 == 0:
                print(f"  {row['t0']:6.0f}-{row['t1']:<7.0f} {row['net_hz']:15.3f} "
                      f"{row['silent_pct']:9.1f} {row['pn_peak_hz']:11.1f} "
                      f"{row['kc_pct']:7.2f} {row['kc_hz']:8.3f}")
        res[cond] = rows
        # How much would the answer change if we had settled first?
        n_half = max(1, int(500.0 / a.bin))
        first = rows[:n_half]
        last = rows[-n_half:]
        def med(rs, k): return float(np.median([r[k] for r in rs]))
        print(f"  first {500:.0f} ms vs last {n_half*a.bin:.0f} ms:")
        for k, lbl in (("net_hz", "whole brain Hz"), ("silent_pct", "silent %"),
                       ("pn_peak_hz", "PN peak Hz"), ("kc_pct", "KC %")):
            x, y = med(first, k), med(last, k)
            ratio = (y / x) if x > 1e-9 else float("inf")
            print(f"    {lbl:16s} {x:9.3f} -> {y:9.3f}   x{ratio:.2f}")
        print()

    Path(a.out).write_text(json.dumps({"params": p, **res}, indent=2) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
