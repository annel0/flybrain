"""Is the erratic Kenyon cell recruitment real, or an artefact of short windows?

Refitting sparseness inside the balanced regime gave 1.9%, 31.1%, 20.6%,
23.1%, 11.6%, 39.1% across a smooth weight sweep. Either the balanced regime
genuinely produces unstable recruitment, or half a second of simulated time
against ongoing self-sustained activity is simply too short to measure it.

Those two possibilities make opposite predictions and this separates them. If
the windows are too short, repeats of the *same* condition will scatter widely
and lengthening the window will shrink that scatter. If the regime is really
unstable, repeats will agree with each other while the weight dependence stays
ragged.

Repeats differ only in the random seed, which drives the Poisson forcing of
the receptor neurons; everything else including the graph is identical.
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


def recruitment(sim, orn, kc, seconds, seed):
    sim.seed = seed
    sim.reset()
    sim.set_poisson(orn, P.POISSON_RATE_HZ)
    rates = sim.run(seconds * 1000)[0]
    return (100 * float((rates[kc] > 1.0).mean()),
            float(rates[kc].mean()),
            float(rates[~orn].mean()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="0.75,1.0,1.5,2.0")
    ap.add_argument("--inh-gain", type=float, default=8.0)
    ap.add_argument("--windows", default="0.5,2.0")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--out", default="out/sparseness_variance.json")
    a = ap.parse_args()

    windows = [float(x) for x in a.windows.split(",")]
    scales = [float(x) for x in a.scales.split(",")]
    print(f"inhibitory gain x{a.inh_gain:g}, ORN_{a.glomerulus}, "
          f"{a.repeats} seeds per condition")
    print("wide scatter between seeds -> the window is too short;")
    print("tight scatter with a ragged weight curve -> the regime is unstable\n")
    print(f"  {'window':>7} {'w_syn':>7} {'KC recruited %':>26} {'net Hz':>8}")

    rows = []
    for win in windows:
        for sc in scales:
            sim = FlySim(scale=sc, delay_mode="published", inh_gain=a.inh_gain)
            ct = sim.cell_type
            orn = np.char.startswith(ct, f"ORN_{a.glomerulus}")
            kc = np.char.startswith(ct, "KC")
            sim.build_drive(0.0, 0.0)
            sim.sigma = 0.0

            vals, kcmean, net = [], [], []
            for k in range(a.repeats):
                pct, km, nm = recruitment(sim, orn, kc, win, 1000 + 97 * k)
                vals.append(pct); kcmean.append(km); net.append(nm)
            v = np.array(vals)
            spread = f"{v.mean():6.1f} +- {v.std():5.1f}  [{v.min():5.1f}-{v.max():5.1f}]"
            print(f"  {win:6.1f}s {sc:7.3f} {spread:>26} {np.mean(net):8.3f}")
            rows.append({"window_s": win, "w_syn": sc, "inh_gain": a.inh_gain,
                         "recruited_pct": vals, "mean": float(v.mean()),
                         "sd": float(v.std()), "cv": float(v.std() / max(v.mean(), 1e-9)),
                         "kc_mean_hz": float(np.mean(kcmean)),
                         "net_hz": float(np.mean(net))})
            del sim
            torch.cuda.empty_cache()

    print("\nscatter between seeds, by window:")
    for win in windows:
        sel = [r for r in rows if r["window_s"] == win]
        cv = np.mean([r["cv"] for r in sel])
        print(f"  {win:.1f}s: mean coefficient of variation across seeds {100*cv:.0f}%")
    print("\nweight dependence, by window (mean recruitment per weight):")
    for win in windows:
        sel = sorted([r for r in rows if r["window_s"] == win], key=lambda r: r["w_syn"])
        print(f"  {win:.1f}s: " + "  ".join(f"{r['w_syn']:.2f}->{r['mean']:.1f}%"
                                            for r in sel))

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"glomerulus": a.glomerulus,
                                       "repeats": a.repeats, "rows": rows},
                                      indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
