"""Can the network sustain itself, and at what inhibitory gain?

The operating point measurement found the real problem. It is not only that
cells sit below threshold -- it is that their mean membrane potential sits at
rest, meaning the network's input to itself is close to nothing. At 0.5 Hz
each cell receives roughly 0.14 mV of synaptic drive against a 7 mV threshold.
The recurrent network is effectively disconnected, and everything that moves a
membrane is the noise we inject.

Balanced-network theory describes the other regime: excitation and inhibition
are each large and nearly cancel, leaving a mean just below threshold and
large fluctuations. Reaching it needs excitation and inhibition scaled
separately, and our model has one weight where the theory needs two. The
connectome says who inhibits whom; it does not say how hard.

The test here removes the crutch: no injected noise, no stimulus. A brief kick,
then the network is left alone. If activity persists, it is sustaining itself.
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
from fly_sim import FlySim, DT, U_TH


def self_sustained(sim, kick_ms, run_ms, kick_frac, rng):
    """Kick a random fraction of cells, then leave the network alone."""
    sim.reset()
    sim.sigma = 0.0
    n_kick = int(sim.n * kick_frac)
    idx = rng.choice(sim.n, n_kick, replace=False)
    mask = np.zeros(sim.n, dtype=bool)
    mask[idx] = True

    steps_kick = int(round(kick_ms / DT))
    steps_run = int(round(run_ms / DT))
    hist = sim.record_history(steps_kick + steps_run)
    sim.set_poisson(mask, 100.0)
    for _ in range(steps_kick):
        sim.step(sim.drive["off"])
    sim.force.zero_()
    snap = []
    sim.counts.zero_()
    for i in range(steps_run):
        sim.step(sim.drive["off"], record=True)
        if i % 200 == 0:
            snap.append(sim.u.detach().clone()[0])
    torch.cuda.synchronize()

    rates = sim.counts.cpu().numpy() / (run_ms / 1000.0)
    counts = hist.cpu().numpy().astype(np.float64)
    tail = counts[-steps_run // 3:]
    early = counts[steps_kick:steps_kick + steps_run // 3]
    u = torch.stack(snap) if snap else None
    gap_sd = None
    if u is not None:
        sd = u.std(0)
        ok = sd > 1e-6
        if ok.any():
            gap_sd = float(((U_TH - u.mean(0))[ok] / sd[ok]).median())
    return {"rate_early_hz": float(early.mean() / sim.n / (DT / 1000)),
            "rate_late_hz": float(tail.mean() / sim.n / (DT / 1000)),
            "gap_in_sd": gap_sd,
            "participating": float((rates > 0.1).mean()),
            "rate_of_active_hz": float(rates[rates > 0.1].mean())
                                 if (rates > 0.1).any() else 0.0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="0.075,0.15,0.275")
    ap.add_argument("--inh-gains", default="1,2,4,8")
    ap.add_argument("--kick-ms", type=float, default=50.0)
    ap.add_argument("--run-ms", type=float, default=600.0)
    ap.add_argument("--kick-frac", type=float, default=0.02)
    ap.add_argument("--out", default="out/balance.json")
    a = ap.parse_args()

    print(f"kick {100*a.kick_frac:.0f}% of cells for {a.kick_ms:.0f} ms, then")
    print(f"no noise and no input for {a.run_ms:.0f} ms. Persisting activity")
    print("means the network is driving itself.\n")
    print(f"  {'w_syn':>7} {'inh':>5} {'late Hz':>8} {'active%':>8} "
          f"{'Hz if active':>13} {'gap/sd':>7}  verdict")

    rng = np.random.default_rng(0)
    rows = []
    for sc in [float(x) for x in a.scales.split(",")]:
        for gi in [float(x) for x in a.inh_gains.split(",")]:
            sim = FlySim(scale=sc, delay_mode="published", inh_gain=gi)
            sim.build_drive(0.0, 0.0)
            r = self_sustained(sim, a.kick_ms, a.run_ms, a.kick_frac, rng)
            ratio = r["rate_late_hz"] / max(r["rate_early_hz"], 1e-9)
            if r["rate_late_hz"] < 0.05:
                verdict = "died"
            elif r["rate_late_hz"] > 50:
                verdict = "saturated"
            elif 0.3 < ratio < 3:
                verdict = "SUSTAINED"
            else:
                verdict = "drifting"
            gs = f"{r['gap_in_sd']:.1f}" if r["gap_in_sd"] is not None else " n/a"
            print(f"  {sc:7.3f} {gi:5.1f} {r['rate_late_hz']:8.2f} "
                  f"{100*r['participating']:7.1f}% {r['rate_of_active_hz']:13.1f} "
                  f"{gs:>7}  {verdict}")
            rows.append({"w_syn": sc, "inh_gain": gi, **r,
                         "ratio": ratio, "verdict": verdict})
            del sim
            torch.cuda.empty_cache()

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"kick_ms": a.kick_ms, "run_ms": a.run_ms, "kick_fraction": a.kick_frac,
         "threshold_above_rest_mV": U_TH, "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
