"""Can one pair of time constants serve both the escape circuit and the
mushroom body?

The escape pathway needs a single spike to cross a synapse: in the animal one
giant-fibre spike reliably fires the jump motor neuron. Our model cannot do
that, because a membrane following with tau 20 ms a conductance that decays
with tau 5 ms sees only 16% of the event -- 3 mV where 7 are needed.

The obvious fix is to speed the membrane up or slow the synapse down. But the
mushroom body wants the opposite: sparse, weak responses in which most Kenyon
cells stay silent. So before adding a propagation target to the fit, this
sweeps both time constants and measures both circuits at once.

Three outcomes, all informative. A region satisfying both means one parameter
set can serve them and the fit should be given the propagation target. No such
region means the two circuits demand different physiology, which turns "the
model needs cell-type-specific parameters" from an assertion into a
measurement. And if the escape circuit never works at any setting, the missing
gap junctions are the whole story rather than a contributing one.
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


def escape_margin(sim, gf_mask, ttm_idx, window_ms=60.0):
    """Peak membrane depolarisation at the jump motor neuron, in units of
    threshold, after one giant-fibre spike. 1.0 means it just fires."""
    sim.reset()
    sim.sigma = 0.0
    sim.force.zero_()
    sim.force[torch.from_numpy(gf_mask).to(sim.dev)] = 1.0
    peak = 0.0
    fired = False
    for i in range(int(round(window_ms / sim.dt))):
        if i == 1:
            sim.force.zero_()
        sim.step(sim.drive["off"], record=True)
        peak = max(peak, float(sim.u[0, ttm_idx].max()))
        if float(sim.counts[ttm_idx].sum()) > 0.5:
            fired = True
            break
    return peak / sim.u_th, fired


def kc_response(sim, orn_mask, kc_mask, seconds=0.5):
    sim.reset()
    sim.sigma = 0.0
    sim.set_poisson(orn_mask, P.POISSON_RATE_HZ)
    r = sim.run(seconds * 1000)[0]
    return 100.0 * float((r[kc_mask] > 1.0).mean()), float(r.mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--scale", type=float, default=P.PUBLISHED_WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--tau-mem", default="2,5,10,20,40")
    ap.add_argument("--tau-syn", default="1,5,10,20,40")
    ap.add_argument("--out", default="out/two_circuits.json")
    a = ap.parse_args()

    print(f"w_syn {a.scale} mV (published), one giant-fibre spike, "
          f"ORN_DA1 at {P.POISSON_RATE_HZ:.0f} Hz")
    print("escape: peak depolarisation at the jump motor neuron, "
          "as a fraction of threshold (>=1 fires)")
    print("mushroom body: percentage of Kenyon cells recruited "
          "(measured 6 +- 5%)\n")

    rows = []
    taum = [float(x) for x in a.tau_mem.split(",")]
    taus = [float(x) for x in a.tau_syn.split(",")]
    print("            " + "".join(f"  tau_s={t:<8.0f}" for t in taus))
    for tm in taum:
        cells = []
        for ts in taus:
            sim = FlySim(graph=a.graph, scale=a.scale, delay_mode="published",
                         tau_mem=tm, tau_syn=ts)
            sim.build_drive(0.0, 0.0)
            ct = sim.cell_type
            gf = np.flatnonzero(np.char.startswith(ct, "DNp01"))
            ttm = torch.from_numpy(np.flatnonzero(ct == "TTMn")).to(sim.dev)
            orn = np.char.startswith(ct, "ORN_DA1")
            kc = np.char.startswith(ct, "KC")
            margin, fired = escape_margin(sim, gf, ttm)
            kcp, net = kc_response(sim, orn, kc)
            rows.append({"tau_mem": tm, "tau_syn": ts, "escape_margin": margin,
                         "escape_fires": bool(fired), "kc_recruited_pct": kcp,
                         "network_hz": net})
            ok_e = "+" if fired else " "
            ok_k = "*" if 1.0 <= kcp <= 11.0 else " "
            cells.append(f" {margin:5.2f}{ok_e}{kcp:5.1f}%{ok_k}")
            del sim
            torch.cuda.empty_cache()
        print(f"  tau_m={tm:<5.0f}" + "".join(cells))

    print("\n  each cell: escape margin, '+' if it fires; KC percentage, "
          "'*' if inside the measured 6 +- 5%")
    both = [r for r in rows if r["escape_fires"] and 1.0 <= r["kc_recruited_pct"] <= 11.0]
    print(f"\n  settings satisfying BOTH circuits: {len(both)} of {len(rows)}")
    if both:
        for r in both:
            print(f"    tau_m {r['tau_mem']:.0f}, tau_s {r['tau_syn']:.0f}: "
                  f"escape {r['escape_margin']:.2f}, KC {r['kc_recruited_pct']:.1f}%")
    else:
        e = [r for r in rows if r["escape_fires"]]
        k = [r for r in rows if 1.0 <= r["kc_recruited_pct"] <= 11.0]
        print(f"    none. escape works at {len(e)} settings, the mushroom body "
              f"at {len(k)}, and they do not overlap.")
        print("    That is a measurement of the claim that this model needs "
              "cell-type-specific physiology.")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"w_syn": a.scale, "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
