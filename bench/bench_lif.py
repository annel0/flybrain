"""Batched leaky integrate-and-fire throughput benchmark on one GPU.

Question this answers: how many replicas of a MaleCNS-sized network can one
RTX 3060 advance per wall second, and what limits it -- kernel launches or
memory bandwidth?

The simulation is deliberately minimal: exponential synaptic conductance,
LIF membrane, absolute refractory period, event-driven spike propagation
through the released CSR graph. It is a performance probe, not a validated
model of fly physiology, and no claim about behaviour follows from it.

Spiking can be driven two ways:
  --mode harness   force an exact target rate, so timings measure the machine
  --mode dynamics  let the recurrent network fire, and report the rate it found
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

DT_MS = 0.1
TAU_M_MS = 20.0
TAU_S_MS = 5.0
V_REST, V_RESET, V_TH = -52.0, -55.0, -45.0
REFRAC_MS = 2.2


def subgraph(crow, col, val, n_keep):
    """Induced subgraph on the first n_keep nodes: a size probe, not a circuit."""
    import numpy as np
    keep_e = []
    new_crow = np.zeros(n_keep + 1, dtype=np.int64)
    for i in range(n_keep):
        s, e = crow[i], crow[i + 1]
        m = col[s:e] < n_keep
        keep_e.append((s + np.flatnonzero(m)))
        new_crow[i + 1] = new_crow[i] + int(m.sum())
    idx = np.concatenate(keep_e) if keep_e else np.array([], dtype=np.int64)
    return new_crow, col[idx].copy(), val[idx].copy()


def load_graph(path, n_fallback=166_700, e_fallback=25_582_938, seed=0):
    """Real CSR graph if present, otherwise a size-matched synthetic stand-in."""
    if path and Path(path).exists():
        z = np.load(path, allow_pickle=False)
        return z["crow"], z["col"], z["val"], "real"
    rng = np.random.default_rng(seed)
    deg = rng.lognormal(mean=4.2, sigma=1.1, size=n_fallback)
    deg = np.maximum(1, (deg * (e_fallback / deg.sum())).astype(np.int64))
    crow = np.zeros(n_fallback + 1, dtype=np.int64)
    np.cumsum(deg, out=crow[1:])
    e = int(crow[-1])
    col = rng.integers(0, n_fallback, size=e, dtype=np.int64).astype(np.int32)
    val = (rng.lognormal(0.0, 0.8, size=e).astype(np.float32))
    val[rng.random(e) < 0.3] *= -1.0
    return crow, col, val, "synthetic"


class Net:
    def __init__(self, crow, col, val, batch, device, tonic=0.0):
        self.dev = torch.device(device)
        self.n = len(crow) - 1
        self.b = batch
        self.crow = torch.from_numpy(crow).to(self.dev)
        self.col = torch.from_numpy(col).to(self.dev).long()
        self.val = torch.from_numpy(val).to(self.dev)
        self.v = torch.full((batch, self.n), V_REST, device=self.dev)
        self.g = torch.zeros((batch, self.n), device=self.dev)
        self.refr = torch.zeros((batch, self.n), device=self.dev)
        self.tonic = tonic
        self.decay_s = float(np.exp(-DT_MS / TAU_S_MS))
        self.alpha_m = DT_MS / TAU_M_MS
        self.spike_count = 0
        self.event_count = 0

    def propagate(self, sb, sn):
        """Scatter the out-edges of the spiking cells into postsynaptic g."""
        start = self.crow[sn]
        cnt = self.crow[sn + 1] - start
        total = int(cnt.sum())          # host sync: measured, not hidden
        if total == 0:
            return
        base = torch.repeat_interleave(start, cnt, output_size=total)
        off = torch.cumsum(cnt, 0) - cnt
        rank = (torch.arange(total, device=self.dev)
                - torch.repeat_interleave(off, cnt, output_size=total))
        e = base + rank
        tgt = self.col[e]
        bb = torch.repeat_interleave(sb, cnt, output_size=total)
        self.g.view(-1).index_add_(0, bb * self.n + tgt, self.val[e])
        self.event_count += total

    def step_dynamics(self):
        self.g.mul_(self.decay_s)
        live = self.refr <= 0
        self.v.add_(self.alpha_m * (V_REST - self.v + self.g + self.tonic) * live)
        s = (self.v >= V_TH) & live
        self.v = torch.where(s, torch.full_like(self.v, V_RESET), self.v)
        self.refr = torch.where(s, torch.full_like(self.refr, REFRAC_MS),
                                self.refr - DT_MS)
        sb, sn = s.nonzero(as_tuple=True)
        self.spike_count += sn.numel()
        self.propagate(sb, sn)

    def step_harness(self, k):
        """Fire exactly k cells per replica per step; same memory traffic."""
        self.g.mul_(self.decay_s)
        self.v.add_(self.alpha_m * (V_REST - self.v + self.g + self.tonic))
        sn = torch.randint(0, self.n, (self.b * k,), device=self.dev)
        sb = torch.arange(self.b, device=self.dev).repeat_interleave(k)
        self.v.view(-1)[sb * self.n + sn] = V_RESET
        self.spike_count += sn.numel()
        self.propagate(sb, sn)


def run(net, steps, mode, k):
    fn = (lambda: net.step_harness(k)) if mode == "harness" else net.step_dynamics
    for _ in range(steps):
        fn()


def bench(crow, col, val, batches, device, steps, warmup, mode, rate):
    n = len(crow) - 1
    k = max(1, round(rate * DT_MS / 1000.0 * n))
    rows = []
    for b in batches:
        try:
            torch.cuda.empty_cache() if device == "cuda" else None
            net = Net(crow, col, val, b, device, tonic=13.0)
            run(net, warmup, mode, k)
            if device == "cuda":
                torch.cuda.synchronize()
            net.spike_count = net.event_count = 0
            t0 = time.perf_counter()
            run(net, steps, mode, k)
            if device == "cuda":
                torch.cuda.synchronize()
            dt = time.perf_counter() - t0

            sim_ms = steps * DT_MS
            per_replica = (sim_ms / 1000.0) / dt
            state_bytes = 3 * 2 * b * n * 4 * steps      # v,g,refr read+write
            rows.append({
                "batch": b,
                "wall_s": round(dt, 3),
                "sim_speed_per_replica": round(per_replica, 3),
                "throughput_x_realtime": round(per_replica * b, 2),
                "mean_rate_hz": round(net.spike_count / b / n / (sim_ms / 1000.0), 2),
                "syn_events_per_sim_s": int(net.event_count / b / (sim_ms / 1000.0)),
                "state_bandwidth_GBs": round(state_bytes / dt / 1e9, 1),
                "gpu_mem_GiB": round(torch.cuda.max_memory_allocated() / 2**30, 2)
                if device == "cuda" else None,
            })
            print(json.dumps(rows[-1]))
            del net
            if device == "cuda":
                torch.cuda.reset_peak_memory_stats()
        except torch.cuda.OutOfMemoryError:
            print(json.dumps({"batch": b, "error": "OOM"}))
            break
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--batches", default="1,2,4,8,16,32,64")
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--mode", choices=["harness", "dynamics"], default="harness")
    ap.add_argument("--rate", type=float, default=5.0, help="target Hz in harness mode")
    ap.add_argument("--subsample", type=int, default=0,
                    help="keep only the first N neurons (induced subgraph)")
    ap.add_argument("--out", default="out/bench.json")
    a = ap.parse_args()

    crow, col, val, kind = load_graph(a.graph)
    if a.subsample:
        crow, col, val = subgraph(crow, col, val, a.subsample)
        kind += f" (subgraph {a.subsample:,})"
    n, e = len(crow) - 1, len(col)
    print(f"graph: {kind}  {n:,} neurons  {e:,} edges  "
          f"mean out-degree {e/n:.1f}  ({(val<0).mean()*100:.0f}% inhibitory)")
    if a.device == "cuda":
        p = torch.cuda.get_device_properties(0)
        print(f"device: {p.name}  {p.total_memory/2**30:.1f} GiB  SMs={p.multi_processor_count}")

    batches = [int(x) for x in a.batches.split(",")]
    rows = bench(crow, col, val, batches, a.device, a.steps, a.warmup, a.mode, a.rate)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"graph": kind, "neurons": n, "edges": e,
                               "device": a.device, "mode": a.mode,
                               "steps": a.steps, "dt_ms": DT_MS,
                               "rows": rows}, indent=2) + "\n")
    print(f"\nwrote {out}")
    if rows:
        best = max(rows, key=lambda r: r.get("throughput_x_realtime", 0))
        print(f"best aggregate throughput: {best['throughput_x_realtime']}x realtime "
              f"at batch {best['batch']}  ({best['state_bandwidth_GBs']} GB/s state traffic)")


if __name__ == "__main__":
    main()
