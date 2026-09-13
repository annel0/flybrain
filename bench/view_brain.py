"""Draw the activity where it actually sits, instead of reading it off tables.

Soma coordinates come with the release for 84% of retained neurons, so a run
can be shown on the real anatomy. This is the diagnostic instrument for the
physiology work: a wrong activity regime is obvious in a picture and easy to
miss in a table of means.

Produces a still frame of per-neuron rates over the run, and an animation of
the same in short time bins.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation

sys.path.insert(0, str(Path(__file__).parent))
from bench_lif import load_graph
from precision_error import calibrate, DT
from final import FinalSim

DARK = "#0d0f14"


def record(sim, seconds, bin_ms):
    """Per-neuron rate per time bin."""
    steps = int(round(seconds * 1000 / DT))
    per_bin = int(round(bin_ms / DT))
    frames, prev = [], torch.zeros_like(sim.counts)
    sim.counts.zero_()
    for i in range(steps):
        sim.step(record=True)
        if (i + 1) % per_bin == 0:
            cur = sim.counts.clone()
            frames.append(((cur - prev) / (bin_ms / 1000.0)).cpu().numpy())
            prev = cur
    return np.stack(frames)


def panel(ax, xy, c, vmax, title, size=0.6):
    ax.set_facecolor(DARK)
    sc = ax.scatter(xy[:, 0], xy[:, 1], c=c, s=size, cmap="inferno",
                    vmin=0, vmax=vmax, linewidths=0, rasterized=True)
    ax.set_title(title, color="#c9d1d9", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    for sp in ax.spines.values():
        sp.set_color("#30363d")
    return sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--seconds", type=float, default=2.0)
    ap.add_argument("--bin-ms", type=float, default=20.0)
    ap.add_argument("--scale", type=float, default=0.05)
    ap.add_argument("--max-points", type=int, default=60000)
    ap.add_argument("--still", default="out/brain_still.png")
    ap.add_argument("--movie", default="out/brain_activity.gif")
    a = ap.parse_args()

    z = np.load(a.graph, allow_pickle=False)
    xyz = z["xyz"]
    superclass = z["superclass"].astype(str)
    cell_type = z["cell_type"].astype(str)
    crow, col, val, _ = load_graph(a.graph)
    n = len(crow) - 1

    ok = np.isfinite(xyz[:, 0])
    print(f"{n:,} neurons, {ok.sum():,} with soma coordinates")
    lo, hi = np.nanmin(xyz, 0), np.nanmax(xyz, 0)
    print(f"extent  x {lo[0]:.0f}..{hi[0]:.0f}   y {lo[1]:.0f}..{hi[1]:.0f}"
          f"   z {lo[2]:.0f}..{hi[2]:.0f}")

    tonic, rate, mu = calibrate(crow, col, val, "cuda", a.scale, 5.0, 4.0, verbose=False)
    sim = FinalSim(crow, col, val, torch.float32, "cuda", tonic, a.scale,
                   batch=1).setup(1 << 16, rate)
    for _ in range(2000):
        sim.step()
    print(f"recording {a.seconds:.1f} s in {a.bin_ms:.0f} ms bins...")
    frames = record(sim, a.seconds, a.bin_ms)
    mean_rate = frames.mean(0)
    print(f"  {frames.shape[0]} frames, mean {mean_rate.mean():.2f} Hz")

    idx = np.flatnonzero(ok)
    if len(idx) > a.max_points:
        idx = np.random.default_rng(0).choice(idx, a.max_points, replace=False)
    P = xyz[idx]
    vmax = float(np.percentile(mean_rate[idx][mean_rate[idx] > 0], 95)) if (
        mean_rate[idx] > 0).any() else 1.0

    views = [((0, 1), "frontal  (x, y)"), ((0, 2), "horizontal  (x, z)"),
             ((2, 1), "sagittal  (z, y)")]

    fig, axes = plt.subplots(1, 4, figsize=(19, 5.2), facecolor=DARK)
    for ax, ((i, j), name) in zip(axes[:3], views):
        sc = panel(ax, P[:, [i, j]], mean_rate[idx], vmax, name)
    cb = fig.colorbar(sc, ax=axes[2], fraction=0.04)
    cb.set_label("Hz", color="#c9d1d9"); cb.ax.tick_params(colors="#c9d1d9")

    ax = axes[3]; ax.set_facecolor(DARK)
    kc = np.array([t.startswith("KC") for t in cell_type]) & ok
    mb = np.array([t.startswith(("KC", "MBON", "PPL1", "PAM", "APL"))
                   for t in cell_type]) & ok
    ax.scatter(xyz[ok][:, 0], xyz[ok][:, 1], c="#20262e", s=0.4, linewidths=0)
    ax.scatter(xyz[mb][:, 0], xyz[mb][:, 1], c="#3fb950", s=1.2, linewidths=0,
               label=f"mushroom body circuit ({mb.sum():,})")
    ax.scatter(xyz[kc][:, 0], xyz[kc][:, 1], c="#f85149", s=1.2, linewidths=0,
               label=f"Kenyon cells ({kc.sum():,})")
    ax.set_title("Where the first experiment lives", color="#c9d1d9", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
    lg = ax.legend(loc="lower right", fontsize=7, facecolor=DARK, edgecolor="#30363d")
    for t in lg.get_texts():
        t.set_color("#c9d1d9")
    for sp in ax.spines.values():
        sp.set_color("#30363d")

    fig.suptitle(f"MaleCNS v1.0 — {n:,} neurons, mean {mean_rate.mean():.1f} Hz, "
                 f"{100*(mean_rate==0).mean():.0f}% silent  "
                 f"(generic physiology, no stimulus — regime not yet realistic)",
                 color="#8b949e", fontsize=11)
    fig.tight_layout()
    Path(a.still).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.still, dpi=115, facecolor=DARK)
    print(f"wrote {a.still}")

    # ---- animation -------------------------------------------------------
    sub = idx if len(idx) <= 30000 else np.random.default_rng(1).choice(idx, 30000, False)
    Pa = xyz[sub]
    fmax = float(np.percentile(frames[:, sub][frames[:, sub] > 0], 97)) if (
        frames[:, sub] > 0).any() else 1.0
    figa, axa = plt.subplots(1, 3, figsize=(14, 4.6), facecolor=DARK)
    scs = []
    for ax, ((i, j), name) in zip(axa, views):
        scs.append(panel(ax, Pa[:, [i, j]], frames[0][sub], fmax, name, size=1.0))
    ttl = figa.suptitle("", color="#c9d1d9", fontsize=11)
    figa.tight_layout()

    def update(f):
        for s in scs:
            s.set_array(frames[f][sub])
        ttl.set_text(f"t = {f * a.bin_ms / 1000:.2f} s     "
                     f"population {frames[f].mean():.1f} Hz")
        return scs

    anim = animation.FuncAnimation(figa, update, frames=len(frames),
                                   interval=80, blit=False)
    anim.save(a.movie, writer=animation.PillowWriter(fps=12), dpi=80,
              savefig_kwargs={"facecolor": DARK})
    print(f"wrote {a.movie}  ({len(frames)} frames)")


if __name__ == "__main__":
    main()
