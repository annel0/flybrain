"""The fly with delays and a stimulus that enters through the eyes.

Light enters the way it does in the animal, which is backwards from the
intuition. Every one of the 6,098 photoreceptors is histaminergic, and
histamine opens chloride channels, so a photoreceptor *inhibits* its targets:
in darkness it is depolarised and holds L1/L2/L3 down, and light hyperpolarises
it, releasing them. Driving photoreceptors is therefore darkness, not light --
and an earlier version of this file made exactly that mistake, then measured
no downstream response because there was nothing to suppress at a 1 Hz
baseline.

So photoreceptors are held tonically active here, and "light" is a *reduction*
of that drive on one eye, alternating left and right. The response to look for
downstream is disinhibition.

Everything engineered rather than measured is named in `protocol()`.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import triton

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph
from fly_kernels import membrane_delay, deliver, tally_slot, RING_SLOTS

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import params as P

DT = 0.1
TAU_M, TAU_S = P.TAU_MEMBRANE_MS, P.TAU_SYNAPSE_MS
V_REST, V_RESET, V_TH = P.V_REST_MV, P.V_RESET_MV, P.V_THRESH_MV
U_RESET, U_TH = V_RESET - V_REST, V_TH - V_REST
REFRAC_MS = P.REFRACTORY_MS
BLOCK, EBLOCK, GRID, LANES = 256, 128, 1024, 4
SENSORY = ("ol_sensory", "cb_sensory", "sensory_ascending")


class FlySim:
    def __init__(self, graph="data/malecns_v1/graph.npz",
                 delays="data/malecns_v1/delays.npz", device="cuda",
                 scale=P.WEIGHT_PER_SYNAPSE_MV, cap=1 << 14, batch=1,
                 delay_mode="published", min_synapses=1):
        z = np.load(graph, allow_pickle=False)
        crow, col, val, _ = load_graph(graph)
        self.n = n = len(crow) - 1
        self.b = batch
        self.cap = cap
        self.dev = torch.device(device)
        self.superclass = z["superclass"].astype(str)
        self.side = z["side"].astype(str)
        self.xyz = z["xyz"]
        self.cell_type = z["cell_type"].astype(str)

        if min_synapses > 1:
            keep = np.abs(val) >= min_synapses
            src = np.repeat(np.arange(n), np.diff(crow))
            crow = np.zeros(n + 1, dtype=np.int64)
            np.cumsum(np.bincount(src[keep], minlength=n), out=crow[1:])
            col, val = col[keep], val[keep]
        self.min_synapses = min_synapses
        self.crow = torch.from_numpy(crow).to(self.dev).int()
        self.col = torch.from_numpy(col).to(self.dev).int()
        self.val = (torch.from_numpy(val).to(self.dev) * scale)
        if delay_mode == "published":
            # One fixed delay for every connection, as in the source model.
            d = np.full(n, int(round(P.DELAY_MS / DT)), dtype=np.int8)
        else:
            d = np.load(delays, allow_pickle=False)["delay_steps"].astype(np.int8)
        self.delay_mode = delay_mode
        self.delay = torch.from_numpy(np.clip(d, 1, RING_SLOTS - 1)).to(self.dev)

        self.u = torch.zeros((batch, n), device=self.dev)
        self.g = torch.zeros((batch, n), device=self.dev)
        self.r = torch.zeros((batch, n), device=self.dev, dtype=torch.int8)
        self.ring = torch.zeros(RING_SLOTS * cap, dtype=torch.int32, device=self.dev)
        self.ring_cnt = torch.zeros(RING_SLOTS, dtype=torch.int32, device=self.dev)
        self.counts = torch.zeros(n, device=self.dev)
        self.force = torch.zeros(n, device=self.dev)
        self.refrac_steps = int(round(REFRAC_MS / DT))
        self.decay = float(np.exp(-DT / TAU_S))
        self.alpha = DT / TAU_M
        self.grid_m = (triton.cdiv(n, BLOCK), batch)
        self.t = 0

        self.is_sensory = np.isin(self.superclass, SENSORY)
        self.is_photo = self.superclass == "ol_sensory"
        self.left, self.right, self.midline = self._sides(crow, col)
        self.sigma = 0.0
        self.seed = 12345

    def _sides(self, crow, col):
        """Hemisphere per cell, falling back to where its targets sit.

        Photoreceptor somata are in the retina, outside the imaged volume, so
        6,062 of 6,098 carry neither coordinates nor a side label. A cell's
        output side is recoverable from the geometry of what it projects to.
        """
        x = self.xyz[:, 0].astype(np.float64)
        lab = self.side
        lx = np.nanmedian(x[(lab == "L") & np.isfinite(x)])
        rx = np.nanmedian(x[(lab == "R") & np.isfinite(x)])
        mid = (lx + rx) / 2.0

        src = np.repeat(np.arange(self.n), np.diff(crow))
        tx = x[col]
        ok = np.isfinite(tx)
        tot = np.bincount(src[ok], weights=tx[ok], minlength=self.n)
        cnt = np.bincount(src[ok], minlength=self.n)
        target_x = np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan)

        best = np.where(np.isfinite(x), x, target_x)
        left = np.where(lab == "L", True, np.where(lab == "R", False, best > mid))
        left = left & np.isfinite(best)
        right = (~left) & np.isfinite(best)
        # explicit labels always win over the geometric guess
        left = np.where(lab == "L", True, left)
        right = np.where(lab == "R", True, right)
        return left.astype(bool), right.astype(bool), float(mid)

    # ---- drive -----------------------------------------------------------
    def build_drive(self, dark_drive, light_drop):
        """Photoreceptors held depolarised (darkness); light lowers one eye."""
        def vec(lit_mask):
            v = torch.zeros(self.n, device=self.dev)
            ph = torch.from_numpy(np.flatnonzero(self.is_photo)).to(self.dev)
            v[ph] = dark_drive
            if lit_mask is not None and lit_mask.any():
                v[torch.from_numpy(np.flatnonzero(lit_mask)).to(self.dev)] = max(
                    0.0, dark_drive - light_drop)
            return v

        self.drive = {"left": vec(self.is_photo & self.left),
                      "right": vec(self.is_photo & self.right),
                      "dark": vec(None),
                      "off": torch.zeros(self.n, device=self.dev)}
        self.n_left = int((self.is_photo & self.left).sum())
        self.n_right = int((self.is_photo & self.right).sum())
        return self.drive

    # ---- one step --------------------------------------------------------
    def step(self, tonic, record=False):
        slot = self.t % RING_SLOTS
        membrane_delay[self.grid_m](
            self.u, self.g, self.r, tonic, self.force, self.delay,
            self.ring, self.ring_cnt,
            self.n, self.cap, self.t, float(self.decay), float(self.alpha),
            float(U_RESET), float(U_TH), self.refrac_steps,
            float(self.sigma), int(self.seed), BLOCK=BLOCK, D=RING_SLOTS)
        deliver[(GRID, LANES)](
            self.ring, self.ring_cnt, self.crow, self.col, self.val, self.g,
            self.n, self.cap, slot, EBLOCK=EBLOCK, GRID=GRID, LANES=LANES)
        if record:
            tally_slot[(triton.cdiv(self.cap, 1024),)](
                self.ring, self.ring_cnt, self.counts, self.n, self.cap, slot,
                BLOCK=1024)
        self.ring_cnt[slot] = 0
        self.t += 1

    def set_poisson(self, mask, rate_hz):
        """Drive these cells as a Poisson spike source at the given rate."""
        self.force.zero_()
        if mask is not None and mask.any():
            idx = torch.from_numpy(np.flatnonzero(mask)).to(self.dev)
            self.force[idx] = rate_hz * DT / 1000.0
        return int(mask.sum()) if mask is not None else 0

    def reset(self):
        self.u.zero_(); self.g.zero_(); self.r.zero_()
        self.ring_cnt.zero_(); self.ring.zero_(); self.counts.zero_()
        self.t = 0

    def run(self, ms, phase_ms=None, record_bin_ms=None, warm=False):
        steps = int(round(ms / DT))
        frames, labels = [], []
        prev = torch.zeros_like(self.counts)
        self.counts.zero_()
        per_bin = int(round(record_bin_ms / DT)) if record_bin_ms else 0
        t0 = time.perf_counter()
        for i in range(steps):
            if phase_ms is None:
                tonic = self.drive["off"]
                lab = "off"
            else:
                k = int((i * DT) // phase_ms) % 2
                lab = "left" if k == 0 else "right"
                tonic = self.drive[lab]
            self.step(tonic, record=True)   # tally is cheap; always count
            if per_bin and (i + 1) % per_bin == 0:
                cur = self.counts.clone()
                frames.append(((cur - prev) / (record_bin_ms / 1000.0)).cpu().numpy())
                prev = cur
                labels.append(lab)
        torch.cuda.synchronize()
        wall = time.perf_counter() - t0
        rates = self.counts.cpu().numpy() / (ms / 1000.0)
        return rates, (np.stack(frames) if frames else None), labels, wall

    def protocol(self, sigma, stim_amp):
        return {
            "engineered_not_measured": [
                "uniform LIF parameters for every cell type",
                "synaptic sign from predicted transmitter only, no receptor kinetics",
                "axonal delay per source cell, not per synapse",
                "synaptic weight = synapse count x a single global scale factor",
                "light is a step change in photoreceptor drive, not a phototransduction model",
                "photoreceptors spike here; real ones are graded, non-spiking cells",
                "spontaneous activity comes from injected Gaussian noise; the published model has none",
                "photoreceptor hemisphere inferred from target geometry, not annotated",
            ],
            "noise_sigma": sigma, "stimulus_amplitude": stim_amp,
            "photoreceptors_left": self.n_left, "photoreceptors_right": self.n_right,
            "weight_scale_applied": True, "dt_ms": DT, "ring_slots": RING_SLOTS,
        }


def calibrate_noise(sim, target_hz, lo=0.0, hi=1.0, ms=150.0, verbose=True):
    """Pick the noise amplitude that leaves the unstimulated net near target.

    Noise, not a constant current: a constant either crosses threshold or does
    not, so it cannot produce a graded spontaneous rate.
    """
    sim.build_drive(0.0, 0.0)
    best = None
    for _ in range(12):
        mid = (lo + hi) / 2
        sim.sigma = mid
        sim.reset()
        rates, _, _, _ = sim.run(ms)
        r = float(rates.mean())
        if verbose:
            print(f"    sigma {mid:.4f} -> {r:7.2f} Hz")
        if best is None or abs(r - target_hz) < abs(best[1] - target_hz):
            best = (mid, r)
        if r < target_hz:
            lo = mid
        else:
            hi = mid
        if abs(r - target_hz) < target_hz * 0.08:
            break
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=2.0)
    ap.add_argument("--phase-ms", type=float, default=250.0)
    ap.add_argument("--bin-ms", type=float, default=20.0)
    ap.add_argument("--baseline-hz", type=float, default=1.0,
                    help="0 reproduces the published model, which is silent at rest")
    ap.add_argument("--delay-mode", choices=["published", "geometric"],
                    default="published")
    ap.add_argument("--scale", type=float, default=P.WEIGHT_PER_SYNAPSE_MV)
    ap.add_argument("--dark-drive", type=float, default=14.0,
                    help="tonic drive holding photoreceptors depolarised")
    ap.add_argument("--light-drop", type=float, default=14.0,
                    help="how much light lowers that drive on the lit eye")
    ap.add_argument("--out", default="out/fly_sim.json")
    ap.add_argument("--npz", default="out/fly_frames.npz")
    a = ap.parse_args()

    sim = FlySim(scale=a.scale, delay_mode=a.delay_mode)
    print(f"parameters: {P.CITATION}")
    print(f"  w_syn {a.scale} mV/synapse, reset {V_RESET} mV, "
          f"delay {'1.8 ms fixed' if a.delay_mode=='published' else 'from geometry'}")
    print(f"{sim.n:,} neurons | sensory {int(sim.is_sensory.sum()):,} "
          f"| photoreceptors {int(sim.is_photo.sum()):,}")
    print(f"delay steps: median {int(sim.delay.float().median())}, "
          f"max {int(sim.delay.max())} (ring {RING_SLOTS})")

    print(f"hemispheres: {int(sim.left.sum()):,} left, {int(sim.right.sum()):,} "
          f"right (midline x={sim.midline:.0f}, photoreceptor side from targets)")
    if a.baseline_hz > 0:
        print("calibrating spontaneous activity with background noise:")
        sigma, got = calibrate_noise(sim, a.baseline_hz, verbose=False)
        sim.sigma = sigma
        print(f"  sigma {sigma:.4f} -> {got:.2f} Hz spontaneous\n")
    else:
        sigma, got = 0.0, 0.0
        sim.sigma = 0.0
        print("no background noise: silent at rest, as in the published model\n")

    sim.build_drive(a.dark_drive, a.light_drop)
    print(f"photoreceptors: {sim.n_left:,} left, {sim.n_right:,} right")
    print(f"darkness drive {a.dark_drive}, light lowers it by {a.light_drop}; "
          f"eyes alternate every {a.phase_ms:.0f} ms")
    print("(photoreceptors are inhibitory, so the lit eye DISINHIBITS its lobe)\n")
    sim.reset()
    rates, frames, labels, wall = sim.run(a.seconds * 1000, a.phase_ms, a.bin_ms)
    print(f"ran {a.seconds:.1f} s in {wall:.1f} s wall "
          f"({a.seconds/wall:.2f}x realtime), mean {rates.mean():.2f} Hz\n")

    # Does the stimulated side actually differ from the other?
    lab = np.array(labels)
    L = np.flatnonzero(sim.left), np.flatnonzero(sim.right)
    def starts(arr, *prefixes):
        m = np.zeros(len(arr), dtype=bool)
        for pre in prefixes:
            m |= np.char.startswith(arr, pre)
        return m

    ol_no_photo = starts(sim.superclass, "ol") & ~sim.is_photo
    lam = np.isin(sim.cell_type, ["L1", "L2", "L3", "L4", "L5"])
    regions = [("photoreceptors [driven]", sim.is_photo),
               ("lamina L1-L5", lam),
               ("medulla Mi/Tm/Dm", starts(sim.cell_type, "Mi", "Tm", "Dm")),
               ("T4/T5 motion", starts(sim.cell_type, "T4", "T5")),
               ("optic lobe, no photoreceptors", ol_no_photo),
               ("central brain", starts(sim.superclass, "cb")),
               ("descending neurons", sim.superclass == "descending_neuron")]
    print("  response to LIGHT on a cell's own side "
          "(driven cells marked; everything else is downstream):")
    for region, mask in regions:
        li = np.flatnonzero(mask & sim.left)
        ri = np.flatnonzero(mask & sim.right)
        if not len(li) or not len(ri):
            continue
        dl = frames[lab == "left"][:, li].mean() - frames[lab == "right"][:, li].mean()
        dr = frames[lab == "right"][:, ri].mean() - frames[lab == "left"][:, ri].mean()
        print(f"    {region:30s} left {dl:+7.3f} Hz   right {dr:+7.3f} Hz"
              f"   ({len(li):,}/{len(ri):,})")

    np.savez_compressed(a.npz, frames=frames.astype(np.float32),
                        labels=np.array(labels), rates=rates)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"neurons": sim.n, "spontaneous_hz": got, "noise_sigma": sigma,
         "mean_rate_hz": float(rates.mean()), "wall_s": wall,
         "speed_x_realtime": a.seconds / wall,
         "protocol": sim.protocol(sigma, a.light_drop)}, indent=2) + "\n")
    print(f"\nwrote {a.out} and {a.npz}")


if __name__ == "__main__":
    main()
