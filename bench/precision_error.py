"""What does lower-precision state storage cost in accuracy?

Storage is fp16/bf16, arithmetic is always fp32 inside a fused kernel --
the LLM weight-quantisation idea applied to neuron state instead of weights.
Membrane voltage is kept as a deviation from rest so that the accumulator
sits near zero, where the float grid is fine.

Spiking networks are chaotic, so individual spike trains diverge no matter
what. The run therefore always includes two controls: the same fp32 config
run twice (atomic scatter is not bit-reproducible), and fp32 with a 1e-4 mV
nudge. Any precision effect only means something measured against those.
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph, subgraph
from kernels import membrane_triton

DT = 0.1
TAU_M, TAU_S = 20.0, 5.0
V_REST, V_RESET, V_TH = -52.0, -55.0, -45.0     # mV, absolute
REFRAC = 2.2
# state is stored as deviation from rest, so these become:
U_RESET, U_TH = V_RESET - V_REST, V_TH - V_REST


@torch.compile(dynamic=False)
def membrane(u_s, g_s, r_s, decay, alpha, tonic):
    """Read low precision, compute fp32, write low precision."""
    u, g, r = u_s.float(), g_s.float(), r_s.float()
    g = g * decay
    live = r <= 0
    u = u + alpha * (-u + g + tonic) * live
    s = (u >= U_TH) & live
    u = torch.where(s, torch.full_like(u, U_RESET), u)
    r = torch.where(s, torch.full_like(r, REFRAC), r - DT)
    return u.to(u_s.dtype), g.to(g_s.dtype), r.to(r_s.dtype), s


def drive(n, mu, sigma, dev, seed=1234):
    """Per-cell background drive. Identical cells all fire or none do, so the
    spread is what produces graded population activity. Frozen across variants."""
    g = torch.Generator(device="cpu").manual_seed(seed)
    z = torch.randn(n, generator=g)
    return (mu + sigma * z).to(dev)


class Sim:
    def __init__(self, crow, col, val, dtype, dev, tonic, scale, batch=1, seed=0):
        du, dg, dr = dtype if isinstance(dtype, tuple) else (dtype, dtype, dtype)
        self.dev = torch.device(dev)
        self.n = len(crow) - 1
        self.b = batch
        self.dtype = (du, dg, dr)
        self.crow = torch.from_numpy(crow).to(self.dev)
        self.col = torch.from_numpy(col).to(self.dev).long()
        self.val = (torch.from_numpy(val).to(self.dev) * scale).to(dg)
        self.u = torch.zeros((batch, self.n), device=self.dev, dtype=du)
        self.g = torch.zeros((batch, self.n), device=self.dev, dtype=dg)
        self.r = torch.zeros((batch, self.n), device=self.dev, dtype=dr)
        self.tonic = tonic if torch.is_tensor(tonic) else torch.tensor(tonic)
        self.tonic = self.tonic.to(self.dev).float()
        self.decay = float(np.exp(-DT / TAU_S))
        self.alpha = DT / TAU_M
        self.kernel = "torch"
        self.s_buf = torch.zeros((batch, self.n), device=self.dev, dtype=torch.int8)
        g = torch.Generator(device=self.dev).manual_seed(seed)
        # a little scatter in initial voltage, otherwise every cell is identical
        self.u += (torch.rand(self.u.shape, generator=g, device=self.dev) * 3.0
                   ).to(du)

    def perturb(self, eps):
        self.u += torch.full_like(self.u, eps)

    def step(self):
        if self.kernel == "triton":
            s = membrane_triton(self.u, self.g, self.r, self.tonic, self.s_buf,
                                self.decay, self.alpha, U_RESET, U_TH, REFRAC, DT)
        else:
            self.u, self.g, self.r, s = membrane(
                self.u, self.g, self.r, self.decay, self.alpha, self.tonic)
        sb, sn = s.nonzero(as_tuple=True)
        if sn.numel():
            start = self.crow[sn]
            cnt = self.crow[sn + 1] - start
            total = int(cnt.sum())
            if total:
                base = torch.repeat_interleave(start, cnt, output_size=total)
                off = torch.cumsum(cnt, 0) - cnt
                rank = (torch.arange(total, device=self.dev)
                        - torch.repeat_interleave(off, cnt, output_size=total))
                e = base + rank
                bb = torch.repeat_interleave(sb, cnt, output_size=total)
                self.g.view(-1).index_add_(0, bb * self.n + self.col[e], self.val[e])
        return s

    def run(self, ms, bin_ms=50.0):
        steps = int(round(ms / DT))
        per_bin = int(round(bin_ms / DT))
        counts = torch.zeros(self.n, device=self.dev, dtype=torch.float32)
        pop = []
        acc = torch.zeros(self.n, device=self.dev, dtype=torch.float32)
        binned = []
        for i in range(steps):
            s = self.step()
            c = s[0].to(torch.float32)
            counts += c
            acc += c
            if (i + 1) % per_bin == 0:
                binned.append(acc.clone())
                pop.append(float(acc.sum()))
                acc.zero_()
        return (counts.cpu().numpy() / (ms / 1000.0),
                np.array(pop) / (bin_ms / 1000.0),
                torch.stack(binned).cpu().numpy() if binned else None)


def calibrate(crow, col, val, dev, scale, target, sigma, ms=200.0, verbose=True):
    """Find the mean background drive that puts the network near target rate.

    Coarse sweep first, because the rate-vs-drive curve can be steep and a
    blind bisection lands on the silent side of it.
    """
    n = len(crow) - 1
    curve = []
    for mu in (0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 14.0):
        t = drive(n, mu, sigma, dev)
        r = float(Sim(crow, col, val, torch.float32, dev, t, scale).run(ms)[0].mean())
        curve.append((mu, r))
        if verbose:
            print(f"  mu={mu:5.1f} -> {r:8.2f} Hz")
        if r > target * 4:
            break
    below = [c for c in curve if c[1] <= target]
    above = [c for c in curve if c[1] > target]
    if not above:
        return drive(n, curve[-1][0], sigma, dev), curve[-1][1], curve[-1][0]
    lo = below[-1][0] if below else 0.0
    hi = above[0][0]
    best = (hi, above[0][1])
    for _ in range(10):
        mid = (lo + hi) / 2
        t = drive(n, mid, sigma, dev)
        r = float(Sim(crow, col, val, torch.float32, dev, t, scale).run(ms)[0].mean())
        if abs(r - target) < abs(best[1] - target):
            best = (mid, r)
        if r < target:
            lo = mid
        else:
            hi = mid
        if abs(r - target) < target * 0.05:
            break
    return drive(n, best[0], sigma, dev), best[1], best[0]


def compare(ref_rates, rates, ref_bins, bins, label):
    d = rates - ref_rates
    active = ref_rates > 0.5
    out = {
        "variant": label,
        "mean_rate_hz": round(float(rates.mean()), 3),
        "mean_rate_delta_hz": round(float(d.mean()), 4),
        "population_rate_rel_error_%": round(
            100 * abs(float(rates.mean() - ref_rates.mean())) / max(float(ref_rates.mean()), 1e-9), 2),
        "per_neuron_rate_corr": round(float(np.corrcoef(ref_rates, rates)[0, 1]), 4),
        "per_neuron_mean_abs_err_hz": round(float(np.abs(d).mean()), 4),
        "median_rel_err_active_%": round(
            100 * float(np.median(np.abs(d[active]) / ref_rates[active])), 2) if active.any() else None,
        "silent_cells_ref": int((ref_rates == 0).sum()),
        "silent_cells_var": int((rates == 0).sum()),
    }
    if ref_bins is not None and bins is not None:
        rb, bb = ref_bins.ravel(), bins.ravel()
        out["binned_50ms_corr"] = round(float(np.corrcoef(rb, bb)[0, 1]), 4)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--subsample", type=int, default=0)
    ap.add_argument("--ms", type=float, default=1000.0)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--target-rate", type=float, default=5.0)
    ap.add_argument("--batch", type=int, default=64,
                    help="batch used for the speed part only")
    ap.add_argument("--sigma", type=float, default=4.0,
                    help="spread of per-cell background drive, mV")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--out", default="out/precision.json")
    a = ap.parse_args()

    crow, col, val, kind = load_graph(a.graph)
    if a.subsample:
        crow, col, val = subgraph(crow, col, val, a.subsample)
    n = len(crow) - 1
    print(f"graph {kind}: {n:,} neurons, {len(col):,} edges, weight scale {a.scale}")

    print("calibrating background drive:")
    tonic, rate, mu = calibrate(crow, col, val, a.device, a.scale,
                                a.target_rate, a.sigma)
    print(f"chosen mu={mu:.3f} (sigma {a.sigma}) -> {rate:.2f} Hz mean\n")

    def speed(dtype, batch, steps=400, kernel="torch"):
        sim = Sim(crow, col, val, dtype, a.device, tonic, a.scale, batch=batch)
        sim.kernel = kernel
        for _ in range(60):
            sim.step()
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        for _ in range(steps):
            sim.step()
        torch.cuda.synchronize()
        return (time.perf_counter() - t0) / steps * 1e6

    def go(dtype, seed=0, eps=0.0):
        sim = Sim(crow, col, val, dtype, a.device, tonic, a.scale, seed=seed)
        if eps:
            sim.perturb(eps)
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        r = sim.run(a.ms)
        torch.cuda.synchronize()
        return r, time.perf_counter() - t0

    (ref_rates, ref_pop, ref_bins), t_ref = go(torch.float32)
    print(f"reference fp32: {ref_rates.mean():.3f} Hz, {t_ref:.1f} s wall")

    f32, f16, bf16 = torch.float32, torch.float16, torch.bfloat16
    variants = [
        ("fp32 rerun (identical config)", f32, 0, 0.0),
        ("fp32 + 1e-4 mV nudge", f32, 0, 1e-4),
        ("all fp16 storage", (f16, f16, f16), 0, 0.0),
        ("all bf16 storage", (bf16, bf16, bf16), 0, 0.0),
        ("mixed: v fp32, g+refr fp16", (f32, f16, f16), 0, 0.0),
        ("mixed: g fp32, v+refr fp16", (f16, f32, f16), 0, 0.0),
        ("mixed: v+g fp32, refr fp16", (f32, f32, f16), 0, 0.0),
    ]
    rows = []
    for label, dt, seed, eps in variants:
        (rates, pop, bins), t = go(dt, seed, eps)
        row = compare(ref_rates, rates, ref_bins, bins, label)
        row["wall_s"] = round(t, 2)
        row["speedup_vs_fp32"] = round(t_ref / t, 2)
        rows.append(row)
        print(json.dumps(row))

    print(f"\nspeed at batch {a.batch} (us/step, where bandwidth actually bites):")
    speeds = {}
    configs = [("torch.compile  fp32", f32, "torch"),
               ("torch.compile  all fp16", (f16, f16, f16), "torch"),
               ("torch.compile  v fp32 mixed", (f32, f16, f16), "torch"),
               ("triton         fp32", f32, "triton"),
               ("triton         all fp16", (f16, f16, f16), "triton"),
               ("triton         v fp32 mixed", (f32, f16, f16), "triton")]
    for label, dt, kern in configs:
        us = speed(dt, a.batch, kernel=kern)
        speeds[label] = round(us, 1)
        print(f"  {label:14s} {us:8.1f} us/step")
    base = speeds["torch.compile  fp32"]
    for k, v in speeds.items():
        print(f"  {k:14s} speedup vs fp32: {base/v:.2f}x")

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(
        {"neurons": n, "edges": len(col), "sim_ms": a.ms, "tonic_mu": float(mu),
         "weight_scale": a.scale, "drive_mu": float(mu), "drive_sigma": a.sigma,
         "speed_us_per_step": speeds, "speed_batch": a.batch, "ref_mean_rate_hz": float(ref_rates.mean()),
         "ref_wall_s": float(t_ref), "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
