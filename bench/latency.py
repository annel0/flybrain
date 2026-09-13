"""Time, not rate: how long a spike takes to cross a known pathway.

Every target the fitter currently uses is a firing rate, which is why the
axonal delay parameter is invisible to it -- nothing in the objective depends
on timing. The escape circuit fixes that, because it is the one pathway in the
fly whose conduction times are measured directly and whose every link is
named and present in this connectome.

Two paths from the giant fibre (DNp01), differing by exactly one synapse:

  GF -> TTMn                       one synapse    0.93-1.46 ms measured
  GF -> PSI -> DLMn                two synapses   1.44-1.85 ms measured

The pair is the point. Our model charges one fixed delay for every connection,
so it predicts the two-synapse path costs twice the one-synapse path. The
measurements say it costs about 1.3x. That is a structural claim about how
delay accumulates, and this measures whether ours is wrong in the way the
arithmetic says it should be.

Sources: Trimarchi & Schneiderman 1993 (1.46 +- 0.02 ms); Augustin, Zylbertal
& Partridge 2019, PMC6469880 (0.93 ms young / 1.22 ms aged to TTM; 1.44 / 1.85
to DLM; the two disagree and both are recorded). No recording temperature is
given in either, which matters because conduction speed depends on it.
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

PUBLISHED = {
    "GF->TTMn": [("Trimarchi & Schneiderman 1993", 1.46),
                 ("Augustin et al. 2019, young", 0.93),
                 ("Augustin et al. 2019, aged", 1.22)],
    "GF->DLMn": [("Augustin et al. 2019, young", 1.44),
                 ("Augustin et al. 2019, aged", 1.85)],
}


def first_spike_ms(sim, drive_mask, probes, window_ms):
    """Fire the driven group once, then watch when each probe first fires.

    Two things this has to get right, both of which it got wrong at first.
    The drive is a certainty, not a rate: `set_poisson` converts Hz into a
    per-step probability, so asking for 2000 Hz fires the cell on only one
    step in five. And the tally counts spikes as they are *delivered*, one
    axonal delay after they are emitted, so every reading is late by exactly
    that -- which cancels when latencies are taken as differences from the
    driven cell's own recorded spike, and that is how they are reported.
    """
    sim.reset()
    sim.sigma = 0.0
    steps = int(round(window_ms / sim.dt))
    prev = {k: 0.0 for k in probes}
    first = {k: None for k in probes}

    sim.force.zero_()
    sim.force[torch.from_numpy(np.flatnonzero(drive_mask)).to(sim.dev)] = 1.0
    for i in range(steps):
        if i == 1:
            sim.force.zero_()                     # one step of drive only
        sim.step(sim.drive["off"], record=True)
        counts = sim.counts
        for name, mask in probes.items():
            if first[name] is not None:
                continue
            tot = float(counts[mask].sum())
            if tot > prev[name] + 0.5:
                first[name] = (i + 1) * sim.dt
            prev[name] = tot
    return first


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--delays", default="0.8,1.0,1.4,1.8")
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--window-ms", type=float, default=12.0)
    ap.add_argument("--out", default="out/latency.json")
    a = ap.parse_args()

    print("measured, for comparison:")
    for path, vals in PUBLISHED.items():
        for src, v in vals:
            print(f"   {path:12s} {v:5.2f} ms   {src}")
    lo_t = min(v for _, v in PUBLISHED["GF->TTMn"])
    hi_t = max(v for _, v in PUBLISHED["GF->TTMn"])
    ratio_pub = (np.mean([v for _, v in PUBLISHED["GF->DLMn"]])
                 / np.mean([v for _, v in PUBLISHED["GF->TTMn"]]))
    print(f"\n   the two-synapse path costs {ratio_pub:.2f}x the one-synapse path "
          f"in the animal")
    print(f"   a model with one fixed delay per connection must say 2.00x\n")

    rows = []
    for d in [float(x) for x in a.delays.split(",")]:
        sim = FlySim(graph=a.graph, scale=a.scale, delay_mode="published",
                     delay_ms=d)
        sim.build_drive(0.0, 0.0)
        ct = sim.cell_type
        gf = np.char.startswith(ct, "DNp01")
        probes = {"GF": gf,                       # reference for the subtraction
                  "TTMn": ct == "TTMn",
                  "DLMn": np.char.startswith(ct, "DLMn"),
                  "PSI": ct == "PSI"}
        if not gf.any():
            print("giant fibre not found in this graph")
            return
        got = first_spike_ms(sim, gf, probes, a.window_ms)
        ref = got["GF"]
        sub = lambda v: (v - ref) if (v is not None and ref is not None) else None
        t, l, p = sub(got["TTMn"]), sub(got["DLMn"]), sub(got["PSI"])
        ratio = (l / t) if (t and l) else float("nan")
        rows.append({"delay_ms": d, "gf_to_ttmn_ms": t, "gf_to_dlmn_ms": l,
                     "gf_to_psi_ms": p, "ratio": ratio,
                     "n_gf": int(gf.sum())})
        fmt = lambda v: f"{v:5.2f}" if v else "  --"
        print(f"  delay {d:4.2f} ms ->  GF->PSI {fmt(p)}   GF->TTMn {fmt(t)}   "
              f"GF->DLMn {fmt(l)}   ratio {ratio:5.2f}"
              if ratio == ratio else
              f"  delay {d:4.2f} ms ->  GF->PSI {fmt(p)}   GF->TTMn {fmt(t)}   "
              f"GF->DLMn {fmt(l)}   ratio    --")
        del sim
        torch.cuda.empty_cache()

    ok = [r for r in rows if r["gf_to_ttmn_ms"]]
    if ok:
        best = min(ok, key=lambda r: min(abs(r["gf_to_ttmn_ms"] - v)
                                         for _, v in PUBLISHED["GF->TTMn"]))
        print(f"\n  closest to the measured one-synapse latency: delay "
              f"{best['delay_ms']} ms giving {best['gf_to_ttmn_ms']:.2f} ms "
              f"(measured {lo_t:.2f}-{hi_t:.2f})")
        rs = [r["ratio"] for r in ok if r["ratio"] == r["ratio"]]
        if rs:
            print(f"  our two-to-one-synapse ratio: {np.mean(rs):.2f}   "
                  f"animal: {ratio_pub:.2f}")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"published": PUBLISHED, "rows": rows},
                                      indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
