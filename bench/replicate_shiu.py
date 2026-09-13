"""Replicate Shiu et al.'s published firing rates on their own connectome.

Their cell-type names are absent from the MaleCNS annotations, so their 164
predictions cannot be applied to our dataset. Running them on theirs answers a
different and more basic question: is our engine correct? Their Supplementary
Table 1D gives fifteen named neurons with exact predicted rates under a fully
specified protocol, which makes this a numerical comparison rather than a
qualitative one.

Protocol as published: the 21 sugar-sensing gustatory receptor neurons driven
as a Poisson source at 100 Hz, weight per synapse 0.275 mV, one fixed 1.8 ms
delay, membrane 20 ms, synapse 5 ms, threshold 7 mV above a -52 mV rest which
is also the reset, conductance cleared on each spike, no background noise, and
30 runs of 1000 ms. One detail from their source that is easy to miss: neurons
receiving the Poisson drive have their refractory period set to zero.
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

SUGAR_GRNS = [
    720575940624963786, 720575940630233916, 720575940637568838, 720575940638202345,
    720575940617000768, 720575940630797113, 720575940632889389, 720575940621754367,
    720575940621502051, 720575940640649691, 720575940639332736, 720575940616885538,
    720575940639198653, 720575940620900446, 720575940617937543, 720575940632425919,
    720575940633143833, 720575940612670570, 720575940628853239, 720575940629176663,
    720575940611875570,
]

# Supplementary Table 1D, via docs/targets/shiu-predictions.md T-SHIU-3.
PUBLISHED = [
    ("Zorro_l",   720575940629888530, 102.2),
    ("G2N-1_l",   720575940620874757,  69.4),
    ("Rattle_l",  720575940638103349,  75.4),
    ("Usnea_l",   720575940632648612,  72.6),
    ("Clavicle_l", 720575940655014049, 54.0),
    ("FMIn_l",    720575940614763666,  61.3),
    ("MN9_r",     720575940660219265,  68.0),
    ("Phantom_l", 720575940616103218,  57.6),
    ("Roundup_l", 720575940623211725,  46.3),
    ("MN9_l",     720575940645521262,  49.0),
    ("Fdg_l",     720575940631997032,  38.3),
    ("MN6_r",     720575940628826128,  31.7),
    ("Fudog_l",   720575940612648106,   0.5),
    ("Bract_l",   720575940610001220,   5.1),
    ("TH-VUM",    720575940616857174,  32.8),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/flywire_783_shiu/graph.npz")
    ap.add_argument("--rate", type=float, default=100.0)
    ap.add_argument("--seconds", type=float, default=1.0)
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--scale", type=float, default=P.PUBLISHED_WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--out", default="out/replicate_shiu.json")
    a = ap.parse_args()

    sim = FlySim(graph=a.graph, scale=a.scale, delay_mode="published")
    sim.build_drive(0.0, 0.0)
    sim.sigma = 0.0
    ids = np.load(a.graph, allow_pickle=False)["ids"].astype(np.uint64)
    index = {int(v): i for i, v in enumerate(ids)}

    grn = np.zeros(sim.n, dtype=bool)
    missing = [g for g in SUGAR_GRNS if g not in index]
    for g in SUGAR_GRNS:
        if g in index:
            grn[index[g]] = True
    print(f"graph: {sim.n:,} neurons, {len(sim.col):,} connections")
    print(f"sugar receptor neurons found: {int(grn.sum())} of {len(SUGAR_GRNS)}"
          + (f"  missing {missing}" if missing else ""))
    print(f"protocol: {a.rate:.0f} Hz Poisson, {a.runs} runs of "
          f"{a.seconds*1000:.0f} ms, w_syn {a.scale} mV\n")

    probes = [(nm, index[i], pub) for nm, i, pub in PUBLISHED if i in index]
    absent = [nm for nm, i, _ in PUBLISHED if i not in index]
    if absent:
        print(f"not present in this graph: {absent}\n")

    runs = []
    for k in range(a.runs):
        sim.seed = 1000 + 97 * k
        sim.reset()
        sim.set_poisson(grn, a.rate)
        runs.append(sim.run(a.seconds * 1000)[0])
    rates = np.stack(runs)

    print(f"  {'neuron':12s} {'published':>10} {'ours':>10} {'sd':>7} "
          f"{'diff':>9} {'ratio':>7}")
    rows, diffs = [], []
    for nm, idx, pub in probes:
        v = rates[:, idx]
        got, sd = float(v.mean()), float(v.std())
        ratio = got / pub if pub > 0.5 else float("nan")
        rows.append({"neuron": nm, "published_hz": pub, "ours_hz": got,
                     "sd_hz": sd, "ratio": ratio})
        if pub > 0.5:
            diffs.append(ratio)
        print(f"  {nm:12s} {pub:10.1f} {got:10.1f} {sd:7.1f} "
              f"{got-pub:+9.1f} {ratio:7.2f}")

    d = np.array(diffs)
    print(f"\n  median ratio ours/published: {np.median(d):.2f}   "
          f"range {d.min():.2f} to {d.max():.2f}")
    corr = np.corrcoef([r["published_hz"] for r in rows],
                       [r["ours_hz"] for r in rows])[0, 1]
    print(f"  correlation across the fifteen neurons: {corr:.3f}")
    print("\n  a correct engine should land close to 1.00 on the ratio and high")
    print("  on the correlation. A systematic ratio away from 1 with a high")
    print("  correlation points at one shared constant, not at the wiring.")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"graph": a.graph, "rate_hz": a.rate, "runs": a.runs,
         "w_syn": a.scale, "correlation": float(corr),
         "median_ratio": float(np.median(d)), "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
