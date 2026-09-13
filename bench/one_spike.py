"""How many spikes does one extra spike cause? Measured, not inferred.

The regression estimate of the branching ratio turned out to be worthless here.
Under constant background noise consecutive population counts are correlated
simply because the mean is stationary, so the slope of n(t+1) on n(t) tends to
1 whatever the network does -- and indeed it read 0.94 to 0.99 across a weight
range that spans a silent network and a saturated one. It measured
stationarity, not propagation.

This measures propagation directly. Two runs, identical in every respect
including the noise seed, differing only in that one neuron is forced to spike
once. The difference between their population activity is the cascade that one
spike caused. Summed, it is the number of descendants; its decay from step to
step is the branching ratio per generation.

Both runs are bit-identical until the perturbation, so the difference is
causal until chaos separates them -- which is why the window is kept short and
the divergence of an unperturbed pair is measured as the noise floor.
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
from fly_sim import FlySim, calibrate_noise, DT


def run(sim, settle, record, perturb_idx=None):
    sim.reset()
    hist = sim.record_history(record)
    for _ in range(settle):
        sim.step(sim.drive["off"])
    sim.t = 0
    sim.history = hist
    for i in range(record):
        if perturb_idx is not None and i == 0:
            sim.force.zero_()
            sim.force[perturb_idx] = 1.0        # certain spike, this step only
            sim.step(sim.drive["off"])
            sim.force.zero_()
        else:
            sim.step(sim.drive["off"])
    torch.cuda.synchronize()
    return hist.cpu().numpy().astype(np.int64)


def cascade(sim, settle, record, targets, rng):
    base = run(sim, settle, record)
    control = run(sim, settle, record)           # same seed, no perturbation
    drift = int(np.abs(control - base).sum())

    excess = []
    for idx in targets:
        pert = run(sim, settle, record, perturb_idx=int(idx))
        excess.append(pert - base)
    return base, np.array(excess), drift


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="0.05,0.075,0.10,0.15,0.275")
    ap.add_argument("--target-hz", type=float, default=0.5)
    ap.add_argument("--settle", type=int, default=3000)
    ap.add_argument("--window-ms", type=float, default=60.0)
    ap.add_argument("--repeats", type=int, default=24)
    ap.add_argument("--out", default="out/one_spike.json")
    a = ap.parse_args()

    record = int(round(a.window_ms / DT))
    print(f"one forced spike, {a.window_ms:.0f} ms window, "
          f"{a.repeats} source cells per condition")
    print(f"published weight {P.PUBLISHED_WEIGHT_PER_SYNAPSE_MV} mV, "
          f"ours {P.WEIGHT_PER_SYNAPSE_MV} mV\n")
    print(f"  {'w_syn':>7} {'spont':>8} {'self':>7} {'gen 1':>7} {'gen 2':>7} "
          f"{'gen 3':>7} {'total desc':>10} {'any?':>9} {'drift':>6}")

    rows = []
    rng = np.random.default_rng(0)
    for sc in [float(x) for x in a.scales.split(",")]:
        sim = FlySim(scale=sc, delay_mode="published")
        sim.build_drive(0.0, 0.0)
        sigma, spont = calibrate_noise(sim, a.target_hz, ms=400.0, verbose=False)
        sim.sigma = sigma
        deg = (sim.crow[1:] - sim.crow[:-1]).cpu().numpy()
        targets = rng.choice(np.flatnonzero(deg > 50), a.repeats, replace=False)

        base, excess, drift = cascade(sim, a.settle, record, targets, rng)
        d = int(round(P.DELAY_MS / DT))
        # History records *delivered* spikes, which lag emission by one axonal
        # delay. The forced spike is emitted at step 0 and therefore appears in
        # window [d, 2d); its direct descendants appear in [2d, 3d). Generation
        # 0 below is the forced spike itself and should read ~1.
        gens = [float(excess[:, d * (k + 1):d * (k + 2)].sum(1).mean())
                for k in range(4)]
        total = excess[:, 2 * d:].sum(1)          # descendants only
        fired = float((total > 0).mean())

        rows.append({"w_syn": sc, "descendants_mean": float(total.mean()),
                     "descendants_sd": float(total.std()),
                     "fraction_with_any_cascade": fired,
                     "unperturbed_drift": drift,
                     "generation_0_self": gens[0], "generation_1": gens[1],
                     "generation_2": gens[2], "generation_3": gens[3],
                     "spontaneous_hz": spont, "noise_sigma": sigma})
        print(f"  {sc:7.3f} {spont:8.3f} {gens[0]:7.2f} {gens[1]:7.2f} "
              f"{gens[2]:7.2f} {gens[3]:7.2f} {total.mean():10.1f} "
              f"{100*fired:8.0f}% {drift:6d}")
        del sim
        torch.cuda.empty_cache()

    print("\n'self' is the forced spike itself and should read about 1.")
    print("'gen 1' is what it caused one synapse later: that ratio is the")
    print("branching ratio. 'any?' is the fraction of source cells that caused")
    print("anything at all. 'drift' is how far two identical unperturbed runs")
    print("diverge over the same window -- the floor for all of this.")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"window_ms": a.window_ms, "repeats": a.repeats, "dt_ms": DT,
         "delay_ms": P.DELAY_MS, "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
