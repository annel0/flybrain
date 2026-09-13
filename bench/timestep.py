"""Does the imposed clock change the answers?

The simulation advances every one of 166,700 neurons in lockstep every 0.1 ms.
Nothing in the animal does that: a brain has no global clock, and the
discretisation is ours. The fair question is not whether the artefact exists --
it does -- but whether it changes any result we have reported.

That is testable. If 0.1 ms is fine enough, halving and quartering it leaves
the answers where they are. If the answers move, the clock is doing work it
should not be doing, and every number measured at 0.1 ms is suspect.

Each timestep is a separate simulation: the refractory counter, the delay in
steps, the ring length, the membrane and synaptic decay factors and the Poisson
forcing probability are all recomputed from it. Noise amplitude is held in the
per-step units the kernel uses, so its per-step variance is deliberately *not*
rescaled -- the comparison below therefore also shows how much of any change is
the noise process rather than the integration.
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
import params as P
from fly_sim import FlySim, calibrate_noise


def measure(dt, scale, inh_gain, seconds, target_hz, glom, poisson_hz):
    sim = FlySim(scale=scale, delay_mode="published", inh_gain=inh_gain, dt=dt)
    ct = sim.cell_type
    orn = np.char.startswith(ct, f"ORN_{glom}")
    kc = np.char.startswith(ct, "KC")
    sim.build_drive(0.0, 0.0)

    # Spontaneous: noise amplitude fitted separately at each timestep, since a
    # per-step amplitude means something different when the steps differ.
    sigma, spont = calibrate_noise(sim, target_hz, ms=400.0, verbose=False)
    sim.sigma = sigma

    # Self-sustained activity, noise off: this one needs no calibration and is
    # the cleanest comparison across timesteps.
    sim.sigma = 0.0
    sim.reset()
    rng = np.random.default_rng(0)
    mask = np.zeros(sim.n, dtype=bool)
    mask[rng.choice(sim.n, int(sim.n * 0.02), replace=False)] = True
    sim.set_poisson(mask, 100.0)
    sim.run(50.0)
    sim.force.zero_()
    sim.counts.zero_()
    r_self = sim.run(400.0)[0]

    # Odour response, no noise.
    sim.reset()
    sim.set_poisson(orn, poisson_hz)
    t0 = time.perf_counter()
    rates = sim.run(seconds * 1000)[0]
    torch.cuda.synchronize()
    wall = time.perf_counter() - t0

    out = {"dt_ms": dt, "ring_slots": sim.ring_slots,
           "delay_steps": int(sim.delay.max()),
           "refractory_steps": sim.refrac_steps,
           "noise_sigma_fitted": sigma, "spontaneous_hz": spont,
           "self_sustained_hz": float(r_self.mean()),
           "self_sustained_active_pct": 100 * float((r_self > 0.1).mean()),
           "odour_net_hz": float(rates[~orn].mean()),
           "odour_kc_active_pct": 100 * float((rates[kc] > 1.0).mean()),
           "odour_kc_mean_hz": float(rates[kc].mean()),
           "wall_s_per_sim_s": wall / seconds}
    del sim
    torch.cuda.empty_cache()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dts", default="0.2,0.1,0.05,0.025")
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--inh-gain", type=float, default=1.0)
    ap.add_argument("--seconds", type=float, default=0.5)
    ap.add_argument("--target-hz", type=float, default=0.5)
    ap.add_argument("--glomerulus", default="DA1")
    ap.add_argument("--poisson-hz", type=float, default=P.POISSON_RATE_HZ)
    ap.add_argument("--out", default="out/timestep.json")
    a = ap.parse_args()

    print(f"w_syn {a.scale} mV, inhibitory gain x{a.inh_gain:g}")
    print("if 0.1 ms is fine enough, these columns are flat\n")
    print(f"  {'dt ms':>6} {'ring':>5} {'delay':>6} {'rfrc':>5} "
          f"{'self Hz':>8} {'active%':>8} {'odour Hz':>9} {'KC act%':>8} "
          f"{'KC Hz':>7} {'cost':>7}")

    rows = []
    for dt in [float(x) for x in a.dts.split(",")]:
        r = measure(dt, a.scale, a.inh_gain, a.seconds, a.target_hz,
                    a.glomerulus, a.poisson_hz)
        rows.append(r)
        print(f"  {dt:6.3f} {r['ring_slots']:5d} {r['delay_steps']:6d} "
              f"{r['refractory_steps']:5d} {r['self_sustained_hz']:8.3f} "
              f"{r['self_sustained_active_pct']:7.1f}% {r['odour_net_hz']:9.3f} "
              f"{r['odour_kc_active_pct']:7.1f}% {r['odour_kc_mean_hz']:7.2f} "
              f"{r['wall_s_per_sim_s']:6.1f}x")

    ref = [r for r in rows if abs(r["dt_ms"] - 0.1) < 1e-9]
    if ref and len(rows) > 1:
        ref = ref[0]
        print("\nchange relative to the 0.1 ms we have been using:")
        for r in rows:
            if r is ref:
                continue
            def rel(k):
                b = ref[k]
                return 100 * (r[k] - b) / abs(b) if abs(b) > 1e-9 else float("nan")
            print(f"  dt {r['dt_ms']:.3f}: self-sustained {rel('self_sustained_hz'):+7.1f}%"
                  f"   odour rate {rel('odour_net_hz'):+7.1f}%"
                  f"   KC recruited {rel('odour_kc_active_pct'):+7.1f}%")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps({"w_syn": a.scale, "inh_gain": a.inh_gain,
                                       "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
