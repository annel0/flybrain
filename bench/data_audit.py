"""What is in the files we downloaded, and what are we actually using?

The importer reads the columns it was written to read. Nothing tells it about
the others, and a column that is never opened is indistinguishable from one
that does not exist. This lists every field in every source file with its fill
rate, its cardinality and a sample of its values, and marks which ones reach
the graph.
"""

import argparse
import sys
from pathlib import Path

import numpy as np


def describe(name, values, used, n_rows):
    vals = [v for v in values if v is not None and str(v) != "" and str(v) != "nan"]
    fill = 100.0 * len(vals) / max(n_rows, 1)
    mark = "ИСПОЛЬЗУЕМ" if used else "          "
    if not vals:
        print(f"  {mark}  {name:26s} {'пусто':>8s}")
        return
    if isinstance(vals[0], (int, float, np.integer, np.floating)) and not isinstance(vals[0], bool):
        a = np.asarray(vals, dtype=float)
        print(f"  {mark}  {name:26s} {fill:6.1f}%  числа: "
              f"{a.min():.4g} .. {a.max():.4g}  медиана {np.median(a):.4g}")
    else:
        u = sorted({str(v) for v in vals})
        head = ", ".join(u[:6])
        if len(head) > 74:
            head = head[:71] + "..."
        print(f"  {mark}  {name:26s} {fill:6.1f}%  {len(u):>7d} знач.  {head}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--sample", type=int, default=250000)
    a = ap.parse_args()
    root = Path(a.data)

    # Fields the importers read. Anything not here never reaches the model.
    USED = {
        "annotations.feather": {"bodyId", "superclass", "status", "type",
                                "assignedOlHex1", "assignedOlHex2", "class",
                                "somaSide", "subclass", "somaNeuromere",
                                "receptorType", "somaLocation"},
        "neurotransmitters.feather": {"body", "consensus_nt"},
        "edges.feather": {"body_pre", "body_post", "weight"},
        "flywire_annotations.tsv": {"root_id", "super_class", "cell_type",
                                    "top_nt", "side", "soma_x", "soma_y", "soma_z"},
        "connectivity.parquet": {"Presynaptic_Index", "Postsynaptic_Index",
                                 "Excitatory x Connectivity"},
    }

    import pyarrow.feather as feather
    import pyarrow.parquet as pq

    for path in sorted(root.rglob("*")):
        if path.suffix not in (".feather", ".parquet", ".tsv", ".csv"):
            continue
        used = USED.get(path.name, set())
        try:
            if path.suffix == ".feather":
                t = feather.read_table(path, memory_map=True)
                cols, n = t.schema.names, t.num_rows
                get = lambda c: t[c].slice(0, a.sample).to_pylist()
            elif path.suffix == ".parquet":
                f = pq.ParquetFile(path)
                cols, n = f.schema.names, f.metadata.num_rows
                t = next(f.iter_batches(batch_size=a.sample))
                get = lambda c: t.column(c).to_pylist()
            else:
                import csv
                sep = "\t" if path.suffix == ".tsv" else ","
                with path.open(newline="") as fh:
                    r = csv.reader(fh, delimiter=sep)
                    cols = next(r)
                    rows = [row for _, row in zip(range(a.sample), r)]
                n = sum(1 for _ in path.open()) - 1
                by = {c: [row[i] if i < len(row) else None for row in rows]
                      for i, c in enumerate(cols)}
                get = lambda c: by[c]
        except Exception as exc:
            print(f"\n### {path}  — не прочитать: {exc}")
            continue

        shown = min(n, a.sample)
        print(f"\n### {path}")
        print(f"    строк {n:,}  колонок {len(cols)}  "
              f"(смотрим первые {shown:,})")
        n_unused = 0
        for c in cols:
            is_used = c in used
            n_unused += not is_used
            try:
                describe(c, get(c), is_used, shown)
            except Exception as exc:
                print(f"              {c:26s} (ошибка: {exc})")
        print(f"    -> не используем {n_unused} из {len(cols)}")


if __name__ == "__main__":
    main()
