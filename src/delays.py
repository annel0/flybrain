"""Per-neuron axonal delay, derived from the reconstruction's own geometry.

The simulation had no delays at all: a spike reached every target in the same
timestep. That is not a small omission -- conduction and synaptic transmission
are what set whether a recurrent network oscillates, and their absence is a
plausible reason the activity showed no spatial structure.

Delay here is a property of the *source* neuron, not of each synapse: one
axonal delay per cell, equal to a fixed synaptic component plus the time to
travel the mean soma-to-target distance measured in the volume. Real delays
vary per synapse; this is the cheap approximation, and it is stated rather
than hidden. Cells without a soma in the volume take the population median.

Conduction velocity for small unmyelinated invertebrate neurites is of order
0.1-1 m/s; 0.5 m/s is used. The synaptic component is 0.8 ms. Both are
literature-scale choices, not measurements from this dataset.
"""

import argparse
import json
from pathlib import Path

import numpy as np

VOXEL_UM = 0.008          # 8 nm voxels
VELOCITY_UM_PER_MS = 500.0
SYNAPTIC_MS = 0.8
MIN_MS, MAX_MS = 0.5, 3.1


def compute(graph_path: str, dt_ms: float = 0.1):
    z = np.load(graph_path, allow_pickle=False)
    crow, col, xyz = z["crow"], z["col"].astype(np.int64), z["xyz"]
    n = len(crow) - 1

    src = np.repeat(np.arange(n, dtype=np.int64), np.diff(crow))
    a, b = xyz[src], xyz[col]
    d = np.linalg.norm(a - b, axis=1) * VOXEL_UM          # micrometres
    ok = np.isfinite(d)

    total = np.bincount(src[ok], weights=d[ok], minlength=n)
    count = np.bincount(src[ok], minlength=n)
    mean_um = np.divide(total, np.maximum(count, 1), where=count > 0)
    mean_um[count == 0] = np.nan

    ms = SYNAPTIC_MS + mean_um / VELOCITY_UM_PER_MS
    ms[~np.isfinite(ms)] = np.nanmedian(ms)
    ms = np.clip(ms, MIN_MS, MAX_MS)
    steps = np.maximum(1, np.round(ms / dt_ms)).astype(np.int8)
    return ms, steps, mean_um, int((count == 0).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--out", default="data/malecns_v1/delays.npz")
    ap.add_argument("--dt", type=float, default=0.1)
    a = ap.parse_args()

    ms, steps, mean_um, no_geom = compute(a.graph, a.dt)
    q = np.percentile(ms, [5, 25, 50, 75, 95])
    print(f"axonal delay, ms:  p5 {q[0]:.2f}  p25 {q[1]:.2f}  median {q[2]:.2f}"
          f"  p75 {q[3]:.2f}  p95 {q[4]:.2f}")
    print(f"mean soma-to-target distance: median "
          f"{np.nanmedian(mean_um):.0f} um  max {np.nanmax(mean_um):.0f} um")
    print(f"cells without usable geometry (median substituted): {no_geom:,}")
    print(f"ring buffer needs {int(steps.max())} slots at dt={a.dt} ms")

    np.savez(a.out, delay_ms=ms.astype(np.float32), delay_steps=steps)
    Path(a.out).with_suffix(".json").write_text(json.dumps(
        {"velocity_um_per_ms": VELOCITY_UM_PER_MS, "synaptic_ms": SYNAPTIC_MS,
         "clamp_ms": [MIN_MS, MAX_MS], "dt_ms": a.dt,
         "median_delay_ms": float(q[2]), "max_slots": int(steps.max()),
         "note": "per-source-neuron axonal delay, not per-synapse"},
        indent=2) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
