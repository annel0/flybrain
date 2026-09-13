"""Did stimulating one eye actually reach the rest of the brain?

The difference map is the test: mean activity during left-eye stimulation
minus mean activity during right-eye stimulation, drawn on the anatomy. If the
network conducts a lateralised signal, the two optic lobes take opposite
colours. If it does not, the map is noise.

Photoreceptor somata are outside the imaged volume, so the cells being driven
do not appear in these plots at all -- everything visible is downstream.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation

DARK = "#0d0f14"
TEXT = "#c9d1d9"


def style(ax, title=""):
    ax.set_facecolor(DARK)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
    ax.set_title(title, color=TEXT, fontsize=10)
    for sp in ax.spines.values():
        sp.set_color("#30363d")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="out/fly_frames.npz")
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--still", default="out/response_map.png")
    ap.add_argument("--movie", default="out/response.gif")
    ap.add_argument("--max-points", type=int, default=45000)
    a = ap.parse_args()

    d = np.load(a.frames, allow_pickle=False)
    frames, labels = d["frames"], d["labels"].astype(str)
    z = np.load(a.graph, allow_pickle=False)
    xyz, superclass = z["xyz"], z["superclass"].astype(str)
    cell_type = z["cell_type"].astype(str)
    lamina = np.isin(cell_type, ["L1", "L2", "L3", "L4", "L5"])
    photo = superclass == "ol_sensory"

    ok = np.isfinite(xyz[:, 0])
    L = frames[labels == "left"].mean(0)
    R = frames[labels == "right"].mean(0)
    diff = L - R
    diff_plot = np.where(photo, np.nan, diff)   # driven cells are not a response

    idx = np.flatnonzero(ok)
    rng = np.random.default_rng(0)
    if len(idx) > a.max_points:
        idx = rng.choice(idx, a.max_points, replace=False)
    P = xyz[idx]
    v = float(np.percentile(np.abs(diff[idx]), 99)) or 1.0

    print(f"left-lit phases {int((labels=='left').sum())}, "
          f"right {int((labels=='right').sum())}")
    mid = 48302
    for name, m in (("lamina, left half", lamina & (xyz[:, 0] > mid)),
                    ("lamina, right half", lamina & (xyz[:, 0] <= mid))):
        mm = m & ok
        if mm.sum():
            print(f"  {name:22s} mean(L-R) = {diff[mm].mean():+.4f} Hz "
                  f"over {mm.sum():,} cells")

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.4), facecolor=DARK)

    sc = axes[0].scatter(P[:, 0], P[:, 1], c=diff_plot[idx], s=1.0, cmap="coolwarm",
                         vmin=-v, vmax=v, linewidths=0, rasterized=True)
    style(axes[0], "left-eye minus right-eye activity  (frontal)")
    cb = fig.colorbar(sc, ax=axes[0], fraction=0.04)
    cb.set_label("Hz", color=TEXT); cb.ax.tick_params(colors=TEXT)

    mean_all = frames.mean(0)
    sc2 = axes[1].scatter(P[:, 0], P[:, 1], c=mean_all[idx], s=1.0, cmap="inferno",
                          vmin=0, vmax=float(np.percentile(mean_all[idx], 99)) or 1,
                          linewidths=0, rasterized=True)
    style(axes[1], "mean firing rate over the run")
    cb2 = fig.colorbar(sc2, ax=axes[1], fraction=0.04)
    cb2.set_label("Hz", color=TEXT); cb2.ax.tick_params(colors=TEXT)

    ax = axes[2]; ax.set_facecolor(DARK)
    t = np.arange(len(frames)) * 0.02
    left_half = lamina & ok & (xyz[:, 0] > mid)
    right_half = lamina & ok & (xyz[:, 0] <= mid)
    ax.plot(t, frames[:, left_half].mean(1), color="#f85149", lw=1.3,
            label=f"left lamina ({left_half.sum():,})")
    ax.plot(t, frames[:, right_half].mean(1), color="#58a6ff", lw=1.3,
            label=f"right lamina ({right_half.sum():,})")
    for i, lab in enumerate(labels):
        if i and labels[i] != labels[i - 1]:
            ax.axvline(t[i], color="#30363d", lw=0.7)
    ax.set_xlabel("seconds", color=TEXT); ax.set_ylabel("Hz", color=TEXT)
    ax.tick_params(colors=TEXT)
    ax.set_title("Lamina against which eye is lit\n(vertical lines = switch)",
                 color=TEXT, fontsize=10)
    lg = ax.legend(fontsize=8, facecolor=DARK, edgecolor="#30363d")
    for txt in lg.get_texts():
        txt.set_color(TEXT)
    for sp in ax.spines.values():
        sp.set_color("#30363d")

    fig.suptitle("Alternating light, 1 ms axonal delays, 0.97 Hz spontaneous — "
                 "photoreceptors are inhibitory, so the lit eye disinhibits its "
                 "lamina", color="#8b949e", fontsize=10)
    fig.tight_layout()
    Path(a.still).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.still, dpi=115, facecolor=DARK)
    print(f"wrote {a.still}")

    sub = idx if len(idx) <= 28000 else rng.choice(idx, 28000, replace=False)
    Pa = xyz[sub]
    fmax = float(np.percentile(frames[:, sub], 99.5)) or 1.0
    figa, axa = plt.subplots(figsize=(7.5, 6), facecolor=DARK)
    s0 = axa.scatter(Pa[:, 0], Pa[:, 1], c=frames[0][sub], s=2.0, cmap="inferno",
                     vmin=0, vmax=fmax, linewidths=0)
    style(axa)
    ttl = figa.suptitle("", color=TEXT, fontsize=12)
    figa.tight_layout()

    def update(f):
        s0.set_array(frames[f][sub])
        ttl.set_text(f"t = {f*0.02:5.2f} s     stimulating {labels[f].upper()} eye")
        return [s0]

    anim = animation.FuncAnimation(figa, update, frames=len(frames),
                                   interval=80, blit=False)
    anim.save(a.movie, writer=animation.PillowWriter(fps=12), dpi=85,
              savefig_kwargs={"facecolor": DARK})
    print(f"wrote {a.movie}")


if __name__ == "__main__":
    main()
