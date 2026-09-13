"""Where does a simulation step actually go? Membrane update, spike
detection, or synaptic scatter -- and how much is host-sync stall.

Run at one batch size and split the step into parts. Each part is timed in
isolation with the same state, so the numbers are indicative of cost share,
not a strict decomposition of the fused loop.
"""

import argparse
import json
import time

import numpy as np
import torch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import Net, load_graph, DT_MS, V_RESET


def timeit(fn, steps, dev):
    for _ in range(20):
        fn()
    torch.cuda.synchronize() if dev == "cuda" else None
    t0 = time.perf_counter()
    for _ in range(steps):
        fn()
    torch.cuda.synchronize() if dev == "cuda" else None
    return (time.perf_counter() - t0) / steps * 1e6      # microseconds per step


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--rate", type=float, default=5.0)
    a = ap.parse_args()

    crow, col, val, kind = load_graph(a.graph)
    n = len(crow) - 1
    k = max(1, round(a.rate * DT_MS / 1000.0 * n))
    net = Net(crow, col, val, a.batch, a.device, tonic=13.0)
    dev = a.device
    print(f"graph {kind}: {n:,} neurons, {len(col):,} edges; batch {a.batch}, "
          f"{k} spikes/replica/step")

    def elementwise():
        net.g.mul_(net.decay_s)
        net.v.add_(net.alpha_m * (V_RESET - net.v + net.g + net.tonic))

    sn_fixed = torch.randint(0, n, (a.batch * k,), device=net.dev)
    sb_fixed = torch.arange(a.batch, device=net.dev).repeat_interleave(k)

    def scatter_only():
        net.propagate(sb_fixed, sn_fixed)

    def sync_only():
        start = net.crow[sn_fixed]
        cnt = net.crow[sn_fixed + 1] - start
        int(cnt.sum())

    def spike_select():
        s = net.v >= -45.0
        s.nonzero(as_tuple=True)

    def full():
        net.step_harness(k)

    parts = {"elementwise (g decay + v update)": elementwise,
             "spike select (compare + nonzero)": spike_select,
             "host sync only (cnt.sum -> int)": sync_only,
             "synaptic scatter (full propagate)": scatter_only,
             "FULL STEP": full}

    res = {}
    for name, fn in parts.items():
        res[name] = round(timeit(fn, a.steps, dev), 1)
        print(f"  {name:38s} {res[name]:9.1f} us/step")

    full_us = res["FULL STEP"]
    sim_speed = DT_MS / 1000.0 / (full_us / 1e6)
    print(f"\nfull step {full_us:.0f} us -> {sim_speed:.3f}x realtime per replica, "
          f"{sim_speed*a.batch:.2f}x aggregate")
    print(json.dumps(res))


if __name__ == "__main__":
    main()
