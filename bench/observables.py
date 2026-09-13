"""Measure the simulation the way the experiments measured the animal.

Every observable here corresponds to a target in src/fit_targets.py, and is
computed with the criterion that target's source used where we know it. Where
we do not -- the spike-to-fluorescence conversion for sparsely active central
neurons has never been calibrated in Drosophila -- the criterion used is stated
in the docstring rather than hidden in a threshold constant.
"""

import numpy as np
import torch

KC_THRESHOLD_HZ = 1.0   # ours, not a paper's; see docs/targets/mushroom-body.md T-MB-17


def _masks(sim, glom):
    ct = sim.cell_type
    return dict(
        orn=np.char.startswith(ct, f"ORN_{glom}"),
        kc=np.char.startswith(ct, "KC"),
        apl=np.char.startswith(ct, "APL"),
        ln=np.char.startswith(ct, "lLN") | np.char.startswith(ct, "vLN"),
        pn=np.array([c.endswith("_lPN") or c.endswith("_vPN") for c in ct]),
    )


def observe(sim, glom="DA1", poisson_hz=150.0, seconds=0.6, membrane_samples=40):
    """Run the standard battery and return every observable the targets need."""
    m = _masks(sim, glom)
    out = {}

    # --- resting state, nothing driven ---------------------------------
    sim.reset()
    sim.set_poisson(None, 0.0)
    r_rest = sim.run(seconds * 1000)[0]
    out["spontaneous_hz"] = float(r_rest.mean())
    out["silent_fraction_pct"] = 100.0 * float((r_rest == 0).mean())
    out["kc_baseline_hz"] = float(r_rest[m["kc"]].mean())

    # Distance to threshold, in each cell's own fluctuation width. No
    # published number exists for this in the fly, so the target built on it
    # is deliberately loose and held out.
    snap = []
    for i in range(membrane_samples * 20):
        sim.step(sim.drive["off"])
        if i % 20 == 0:
            snap.append(sim.u.detach().clone()[0])
    torch.cuda.synchronize()
    u = torch.stack(snap)
    sd = u.std(0)
    ok = (sd > 1e-6).cpu().numpy() & m["pn"]
    if ok.any():
        gap = (sim.u_th - u.mean(0)).cpu().numpy()[ok] / sd.cpu().numpy()[ok]
        out["pn_gap_in_sd"] = float(np.median(gap))
    else:
        out["pn_gap_in_sd"] = float("nan")

    # --- odour presented to one glomerulus ------------------------------
    sim.reset()
    sim.set_poisson(m["orn"], poisson_hz)
    r = sim.run(seconds * 1000)[0]
    out["kc_recruited_pct"] = 100.0 * float((r[m["kc"]] > KC_THRESHOLD_HZ).mean())
    out["apl_rate_hz"] = float(r[m["apl"]].mean()) if m["apl"].any() else 0.0
    out["ln_rate_hz"] = float(r[m["ln"]].mean()) if m["ln"].any() else 0.0
    out["network_hz"] = float(r[~m["orn"]].mean())

    # Peak projection neuron response: the strongest uniglomerular type, which
    # is what the Rmax fits in the source describe.
    pn_rates = []
    for t_ in sorted({c for c in sim.cell_type if c.endswith(("_lPN", "_vPN"))}):
        sel = sim.cell_type == t_
        if sel.sum() >= 2:
            pn_rates.append(float(r[sel].mean()))
    out["pn_peak_hz"] = max(pn_rates) if pn_rates else 0.0
    own = [float(r[sim.cell_type == t_].mean())
           for t_ in sorted({c for c in sim.cell_type if c.startswith(glom + "_")})
           if (sim.cell_type == t_).sum() >= 2]
    others = [v for v in pn_rates if v not in own]
    med = float(np.median(others)) if others else 0.0
    out["selectivity"] = (max(own) / med) if (own and med > 0.01) else float("nan")

    # --- the causal test: block APL's output ----------------------------
    if m["apl"].any():
        crow = sim.crow.cpu().numpy().astype(np.int64)
        mask = torch.zeros_like(sim.val, dtype=torch.bool)
        for i in np.flatnonzero(m["apl"]):
            mask[crow[i]:crow[i + 1]] = True
        saved = sim.val[mask].clone()
        sim.val[mask] = 0.0
        sim.reset()
        sim.set_poisson(m["orn"], poisson_hz)
        r2 = sim.run(seconds * 1000)[0]
        sim.val[mask] = saved
        blocked = 100.0 * float((r2[m["kc"]] > KC_THRESHOLD_HZ).mean())
        out["apl_block_delta_pp"] = blocked - out["kc_recruited_pct"]
        out["kc_recruited_apl_blocked_pct"] = blocked
    else:
        out["apl_block_delta_pp"] = float("nan")

    return out
