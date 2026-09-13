"""Is the step limited by the GPU, or by unfused PyTorch operations?

The membrane update as written allocates a temporary for every arithmetic
operation, so the same arrays cross the memory bus several times. This
compares it against a torch.compile-fused version and against the card's
measured copy bandwidth, to separate implementation cost from the hardware
ceiling.
"""

import argparse
import time

import torch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import Net, load_graph, V_RESET


def timeit(fn, steps=300):
    for _ in range(30):
        fn()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(steps):
        fn()
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / steps * 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--batch", type=int, default=64)
    a = ap.parse_args()

    crow, col, val, _ = load_graph(a.graph)
    n = len(crow) - 1
    net = Net(crow, col, val, a.batch, "cuda", tonic=13.0)
    nbytes = net.v.numel() * 4

    print(f"batch {a.batch}: each state array is {nbytes/2**20:.1f} MiB")

    # Reference: how fast can this card move memory at all?
    src = torch.empty_like(net.v)
    dst = torch.empty_like(net.v)
    t = timeit(lambda: dst.copy_(src))
    print(f"  raw copy (read+write 1 array)      {t:8.1f} us  "
          f"-> {2*nbytes/t*1e6/1e9:6.1f} GB/s measured peak")

    def unfused():
        net.g.mul_(net.decay_s)
        net.v.add_(net.alpha_m * (V_RESET - net.v + net.g + net.tonic))

    t_unfused = timeit(unfused)
    print(f"  membrane update, unfused           {t_unfused:8.1f} us")

    @torch.compile(dynamic=False)
    def fused(v, g, decay, alpha, rest, tonic):
        g2 = g * decay
        v2 = v + alpha * (rest - v + g2 + tonic)
        return v2, g2

    def run_fused():
        net.v, net.g = fused(net.v, net.g, net.decay_s, net.alpha_m, V_RESET, net.tonic)

    try:
        t_fused = timeit(run_fused, steps=200)
        print(f"  membrane update, torch.compile     {t_fused:8.1f} us  "
              f"({t_unfused/t_fused:.1f}x faster)")
        eff = 3 * nbytes / t_fused * 1e6 / 1e9
        print(f"      -> {eff:.0f} GB/s effective on 3 array passes")
    except Exception as exc:
        print(f"  torch.compile failed: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
