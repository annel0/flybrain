"""Import the exact connectivity Shiu et al. ran their model on.

Their published predictions are stated on the FlyWire 783 graph with their own
completeness filter, and their cell-type names do not appear anywhere in the
MaleCNS annotations we normally use -- not as `type`, `flywireType` or
`hemibrainType` -- so those predictions cannot be applied to our dataset. They
can be replicated on theirs.

That separates two questions we had been running together: whether our engine
is correct, which their graph and their numbers can answer exactly, and
whether our model of MaleCNS is right, which is a different matter entirely.

Node order here is the row order of their completeness table, because their
Presynaptic_Index / Postsynaptic_Index columns are positional into it.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/flywire_783_shiu")
    ap.add_argument("--out", default="data/flywire_783_shiu/graph.npz")
    a = ap.parse_args()
    d = Path(a.data)

    comp = pd.read_csv(d / "completeness.csv", index_col=0)
    ids = comp.index.to_numpy().astype(np.uint64)
    n = len(ids)
    print(f"nodes: {n:,} (all marked complete: {bool(comp['Completed'].all())})")

    con = pd.read_parquet(d / "connectivity.parquet",
                          columns=["Presynaptic_Index", "Postsynaptic_Index",
                                   "Excitatory x Connectivity"])
    i = con["Presynaptic_Index"].to_numpy().astype(np.int64)
    j = con["Postsynaptic_Index"].to_numpy().astype(np.int64)
    w = con["Excitatory x Connectivity"].to_numpy().astype(np.float32)
    del con
    if i.max() >= n or j.max() >= n:
        raise ValueError("connection index outside the completeness table")

    order = np.argsort(i, kind="stable")
    i, j, w = i[order], j[order], w[order]
    crow = np.zeros(n + 1, dtype=np.int64)
    np.cumsum(np.bincount(i, minlength=n), out=crow[1:])

    print(f"edges: {len(j):,}   synapses: {np.abs(w).sum():,.0f}   "
          f"inhibitory {100*(w<0).mean():.1f}%")
    print(f"mean out-degree {len(j)/n:.1f}   "
          f"mean synapses per connection {np.abs(w).mean():.2f}")

    # The fields our simulator expects. FlyWire cell types come from the
    # community annotation file when present; sign is already carried in the
    # weights, so the transmitter column is filled only for reference.
    ann_path = d / "flywire_annotations.tsv"
    cell_type = np.full(n, "None", dtype=object)
    superclass = np.full(n, "None", dtype=object)
    nt = np.full(n, "unknown", dtype=object)
    side = np.full(n, "None", dtype=object)
    xyz = np.full((n, 3), np.nan, dtype=np.float32)
    if ann_path.exists():
        ann = pd.read_csv(ann_path, sep="\t", low_memory=False,
                          usecols=["root_id", "cell_type", "super_class",
                                   "top_nt", "side", "soma_x", "soma_y", "soma_z"])
        ann = ann.set_index("root_id")
        pos = pd.Index(ids).get_indexer(ann.index.to_numpy())
        keep = pos >= 0
        p = pos[keep]
        sub = ann[keep]
        cell_type[p] = sub["cell_type"].astype(str).to_numpy()
        superclass[p] = sub["super_class"].astype(str).to_numpy()
        nt[p] = sub["top_nt"].astype(str).to_numpy()
        side[p] = sub["side"].astype(str).to_numpy()
        xyz[p] = sub[["soma_x", "soma_y", "soma_z"]].to_numpy(dtype=np.float32)
        print(f"annotations matched for {int(keep.sum()):,} of {len(ann):,} rows")

    blank = np.full(n, "None", dtype=object)
    out = Path(a.out)
    np.savez(out, crow=crow, col=j.astype(np.int32), val=w, ids=ids,
             sign=np.sign(w[np.searchsorted(crow, np.arange(n), side="left")
                            .clip(0, len(w) - 1)]).astype(np.float32),
             nt=nt.astype(str), superclass=superclass.astype(str),
             cell_type=cell_type.astype(str), xyz=xyz,
             cell_class=blank.astype(str), subclass=blank.astype(str),
             neuromere=blank.astype(str), side=side.astype(str),
             receptor=blank.astype(str),
             hex1=np.full(n, np.nan, dtype=np.float32),
             hex2=np.full(n, np.nan, dtype=np.float32))
    print(f"wrote {out} ({out.stat().st_size/2**20:.0f} MiB)")
    Path(str(out).replace(".npz", "_summary.json")).write_text(json.dumps(
        {"source": "FlyWire 783 as shipped with philshiu/Drosophila_brain_model",
         "nodes": n, "edges": int(len(j)),
         "synapses": float(np.abs(w).sum()),
         "mean_out_degree": len(j) / n,
         "inhibitory_fraction": float((w < 0).mean())}, indent=2) + "\n")


if __name__ == "__main__":
    main()
