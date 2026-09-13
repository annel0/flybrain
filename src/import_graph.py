"""MaleCNS v1.0 flat connectome -> compact CSR graph for GPU simulation.

Reads the released feather files and writes one npz holding the CSR
adjacency plus per-neuron annotations. This module only reshapes the
released reconstruction; it infers no dynamics, receptors or behaviour.

Node policy follows the published release notes: keep entries carrying an
assigned superclass, drop entries explicitly annotated as glia. Edge policy
keeps every released edge between retained nodes, with no extra threshold.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pyarrow.feather as feather

# Released neurotransmitter labels split into a sign for the simulation.
# The connectome does not state signs; this mapping is a modelling choice.
#
# Glutamate and histamine are both inhibitory in Drosophila, which is the
# opposite of the mammalian default: glutamate acts on GluCl chloride
# channels, and histamine -- the photoreceptor transmitter -- on HisCl1/ort
# chloride channels. Treating histamine as excitatory mis-signs every
# photoreceptor in the optic lobes.
INHIBITORY = {"gaba", "glutamate", "histamine"}
EXCITATORY = {"acetylcholine"}
MODULATORY = {"dopamine", "octopamine", "serotonin"}


def pick(schema_names, *candidates):
    for c in candidates:
        if c in schema_names:
            return c
    raise KeyError(f"none of {candidates} in {sorted(schema_names)[:40]}")


def load_nodes(data_dir: Path):
    """Retained neurons, their sign, and whatever annotation we can carry."""
    t = feather.read_table(data_dir / "annotations.feather", memory_map=True)
    names = set(t.schema.names)
    c_id = pick(names, "bodyId", "body", "bodyid")
    c_super = pick(names, "superclass", "super_class")
    cols = {"id": t[c_id].to_numpy().astype(np.uint64),
            "superclass": np.asarray(t[c_super].to_pylist(), dtype=object)}
    for key, cands in (("status", ("status",)), ("type", ("type",)),
                       ("hex1", ("assignedOlHex1",)), ("hex2", ("assignedOlHex2",)),
                       ("class", ("class",)), ("side", ("somaSide", "side")),
                       ("subclass", ("subclass",)),
                       ("neuromere", ("somaNeuromere",)),
                       ("receptor", ("receptorType",))):
        try:
            cols[key] = np.asarray(t[pick(names, *cands)].to_pylist(), dtype=object)
        except KeyError:
            cols[key] = np.full(len(cols["id"]), None, dtype=object)

    has_super = np.array([s is not None and str(s) != "" for s in cols["superclass"]])
    is_glia = np.array([s is not None and str(s) == "Glia" for s in cols["status"]])
    keep = has_super & ~is_glia

    nt_t = feather.read_table(data_dir / "neurotransmitters.feather", memory_map=True)
    nt_names = set(nt_t.schema.names)
    nt_id = nt_t[pick(nt_names, "body", "bodyId")].to_numpy().astype(np.uint64)
    nt_val = np.asarray(nt_t[pick(nt_names, "consensus_nt", "nt", "predicted_nt")].to_pylist(),
                        dtype=object)
    nt_map = dict(zip(nt_id.tolist(), (str(v).lower() if v is not None else "unknown"
                                       for v in nt_val)))

    ids = cols["id"][keep]
    order = np.argsort(ids, kind="stable")
    ids = ids[order]
    if len(np.unique(ids)) != len(ids):
        raise ValueError("duplicate body IDs among retained nodes")

    nt = np.array([nt_map.get(int(i), "unknown") for i in ids], dtype=object)
    sign = np.ones(len(ids), dtype=np.float32)
    sign[np.isin(nt, list(INHIBITORY))] = -1.0

    meta = {k: cols[k][keep][order] for k in
            ("superclass", "type", "class", "side", "subclass", "neuromere",
             "receptor")}
    # Ommatidial lattice coordinates, so a real image can be presented to the eye.
    for k in ("hex1", "hex2"):
        v = cols[k][keep][order]
        meta[k] = np.array([float(x) if x is not None else np.nan for x in v],
                           dtype=np.float32)
    meta["nt"] = nt

    # Soma coordinates, so activity can be drawn where it actually sits.
    # Many entries have no soma in the volume; those stay NaN and are dropped
    # by anything that plots, rather than being placed at the origin.
    xyz = np.full((len(ids), 3), np.nan, dtype=np.float32)
    try:
        raw = t_soma = feather.read_table(
            data_dir / "annotations.feather", columns=["bodyId", "somaLocation"],
            memory_map=True)
        loc_id = raw["bodyId"].to_numpy().astype(np.uint64)
        loc = raw["somaLocation"].to_pylist()
        pos = {int(i): v for i, v in zip(loc_id, loc)
               if v is not None and len(v) == 3}
        for k, i in enumerate(ids):
            v = pos.get(int(i))
            if v is not None:
                xyz[k] = v
    except (KeyError, OSError):
        pass
    meta["xyz"] = xyz
    return ids, sign, meta, int(keep.sum()), int(len(keep))


def build_csr(data_dir: Path, ids: np.ndarray, sign: np.ndarray):
    t = feather.read_table(data_dir / "edges.feather", memory_map=True)
    names = set(t.schema.names)
    c_pre = pick(names, "bodyId_pre", "pre", "bodyid_pre", "body_pre")
    c_post = pick(names, "bodyId_post", "post", "bodyid_post", "body_post")
    c_w = pick(names, "weight", "count", "syn_count", "n")

    pre = t[c_pre].to_numpy().astype(np.uint64)
    post = t[c_post].to_numpy().astype(np.uint64)
    w = t[c_w].to_numpy().astype(np.float32)
    del t

    i = np.searchsorted(ids, pre)
    np.clip(i, 0, len(ids) - 1, out=i)
    ok = ids[i] == pre
    j = np.searchsorted(ids, post)
    np.clip(j, 0, len(ids) - 1, out=j)
    ok &= ids[j] == post
    dropped = int((~ok).sum())

    i = i[ok].astype(np.int64)
    j = j[ok].astype(np.int64)
    w = w[ok] * sign[i]          # sign is a property of the presynaptic cell
    del pre, post, ok

    order = np.argsort(i, kind="stable")
    i, j, w = i[order], j[order], w[order]
    crow = np.zeros(len(ids) + 1, dtype=np.int64)
    np.cumsum(np.bincount(i, minlength=len(ids)), out=crow[1:])
    return crow, j.astype(np.int32), w.astype(np.float32), dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/malecns_v1")
    ap.add_argument("--out", default="data/malecns_v1/graph.npz")
    a = ap.parse_args()

    data_dir = Path(a.data)
    ids, sign, meta, kept, total = load_nodes(data_dir)
    print(f"nodes: kept {kept:,} of {total:,} annotated entries")

    crow, col, val, dropped = build_csr(data_dir, ids, sign)
    n, e = len(ids), len(col)
    print(f"edges: {e:,} retained, {dropped:,} dropped (endpoint not a retained node)")
    have_xyz = int(np.isfinite(meta["xyz"][:, 0]).sum())
    print(f"mean out-degree {e/n:.1f}   inhibitory fraction {(sign < 0).mean():.3f}")
    print(f"soma coordinates available for {have_xyz:,} of {n:,} neurons "
          f"({100*have_xyz/n:.1f}%)")

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez(out, crow=crow, col=col, val=val, ids=ids, sign=sign,
             nt=meta["nt"].astype(str), superclass=meta["superclass"].astype(str),
             cell_type=meta["type"].astype(str), xyz=meta["xyz"],
             cell_class=meta["class"].astype(str),
             subclass=meta["subclass"].astype(str),
             neuromere=meta["neuromere"].astype(str),
             side=meta["side"].astype(str),
             receptor=meta["receptor"].astype(str),
             hex1=meta["hex1"], hex2=meta["hex2"])
    print(f"wrote {out}  ({out.stat().st_size/2**20:.0f} MiB)")

    summary = {"nodes": n, "edges": e, "nodes_dropped": total - kept,
               "edges_dropped": dropped, "mean_out_degree": e / n,
               "inhibitory_fraction": float((sign < 0).mean()),
               "source": "MaleCNS v1.0 flat connectome, minconf 0.5, CC-BY"}
    Path(out.parent / "graph_summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
