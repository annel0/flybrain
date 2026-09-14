"""How much of the model's synaptic sign rests on a confident prediction?

Every excitatory or inhibitory sign in this model comes from one column,
`consensus_nt`, treated as fact. The same file ships the classifier's own
confidence and, for a subset of cells, ground truth -- and the importer uses
neither. This measures what that costs.

The question matters most for the modulatory cells. A classifier trained on
synaptic ultrastructure responds to dense-core vesicles, which peptidergic and
aminergic cells share; published cases exist of one cell being called dopamine,
octopamine and serotonin by three different connectomes at about 50% each. Our
importer gives every one of them sign +1 at full weight.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pyarrow.feather as feather

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from import_graph import INHIBITORY, EXCITATORY, MODULATORY


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/malecns_v1")
    ap.add_argument("--graph", default="data/malecns_v1/graph.npz")
    ap.add_argument("--out", default="out/nt_confidence.json")
    a = ap.parse_args()

    g = np.load(a.graph, allow_pickle=True)
    ids, nt_used, crow = g["ids"], g["nt"].astype(str), g["crow"].astype(np.int64)
    outdeg = np.diff(crow)

    t = feather.read_table(Path(a.data) / "neurotransmitters.feather", memory_map=True)
    body = t["body"].to_numpy().astype(np.uint64)
    conf = np.asarray(t["predicted_nt_confidence"].to_pylist(), dtype=object)
    cons = np.asarray([str(v).lower() if v is not None else "unknown"
                       for v in t["consensus_nt"].to_pylist()], dtype=object)
    gt = np.asarray([str(v).lower() if v is not None else None
                     for v in t["ground_truth"].to_pylist()], dtype=object)
    npred = np.asarray(t["total_nt_predictions"].to_pylist(), dtype=object)

    # One row per body: the file carries more rows than neurons.
    first = {}
    for k, b in enumerate(body.tolist()):
        if b not in first:
            first[k] = b
    keep = np.array(sorted(first.keys()))
    body, conf, cons, gt, npred = (x[keep] for x in (body, conf, cons, gt, npred))
    print(f"{len(body)} unique bodies in the transmitter file; "
          f"{len(ids)} neurons in our graph")

    cmap = {int(b): (float(c) if c is not None else np.nan) for b, c in zip(body, conf)}
    gmap = {int(b): v for b, v in zip(body, gt) if v}
    nmap = {int(b): (float(n) if n is not None else 0.0) for b, n in zip(body, npred)}

    c = np.array([cmap.get(int(i), np.nan) for i in ids])
    n_syn = np.array([nmap.get(int(i), 0.0) for i in ids])
    have = np.isfinite(c)
    print(f"confidence present for {have.sum()} of {len(ids)} "
          f"({100*have.mean():.1f}%)\n")

    print("how the sign we use is distributed over the classifier's confidence")
    print(f"  {'confidence':>14s} {'neurons':>9s} {'% of cells':>11s} "
          f"{'connections':>13s} {'% of edges':>11s}")
    tot_e = outdeg.sum()
    bands = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)]
    res_bands = []
    for lo, hi in bands:
        m = have & (c >= lo) & (c < hi)
        e = int(outdeg[m].sum())
        print(f"  {lo:.2f}-{hi:<8.2f} {int(m.sum()):9d} {100*m.mean():10.1f}% "
              f"{e:13d} {100*e/tot_e:10.1f}%")
        res_bands.append(dict(lo=lo, hi=hi, cells=int(m.sum()), edges=e))

    print("\nconfidence by the sign we assign it")
    for label, group in (("excitatory (+1)", EXCITATORY),
                         ("inhibitory (-1)", INHIBITORY),
                         ("modulatory (given +1)", MODULATORY),
                         ("unclear/unknown (given +1)", {"unclear", "unknown"})):
        m = have & np.isin(nt_used, list(group))
        if m.any():
            print(f"  {label:28s} n={int(m.sum()):6d}  median {np.median(c[m]):.3f}  "
                  f"below 0.5: {int((c[m] < 0.5).sum()):5d}  "
                  f"edges {int(outdeg[m].sum()):9d}")

    # Ground truth: the file's own answer key, which the importer never opens.
    # `consensus_nt` is NOT independent of it -- where ground truth exists the
    # consensus is set to it, so comparing the two measures nothing. The honest
    # test is the classifier's own column, `predicted_nt`, against the truth.
    pmap = {int(b): (str(v).lower() if v is not None else "unknown")
            for b, v in zip(body, np.asarray(t["predicted_nt"].to_pylist(),
                                             dtype=object)[keep])}
    gt_ids = np.array([int(i) for i in ids if int(i) in gmap])
    if len(gt_ids):
        cons_here = np.array([str(nt_used[np.searchsorted(ids, i)]) for i in gt_ids])
        truth = np.array([gmap[int(i)] for i in gt_ids])
        same = float((cons_here == truth).mean())
        print(f"\nconsensus_nt agrees with ground truth for {100*same:.1f}% of "
              f"{len(gt_ids)} cells -- if that reads 100%, the consensus is "
              f"derived from the truth and is not an independent test")
        pred = np.array([pmap.get(int(i), "unknown") for i in gt_ids])
        agree = pred == truth
        print(f"\nground truth is available for {len(gt_ids)} of our neurons")
        print(f"  consensus_nt matches it for {int(agree.sum())} "
              f"({100*agree.mean():.1f}%)")

        def sgn(x):
            return np.where(np.isin(x, list(INHIBITORY)), -1.0, 1.0)
        s_agree = sgn(pred) == sgn(truth)
        print(f"  the SIGN we derive matches for {int(s_agree.sum())} "
              f"({100*s_agree.mean():.1f}%) -- the number that matters, since "
              f"the model only uses the sign")
        bad = ~s_agree
        if bad.any():
            print(f"\n  where the sign is wrong ({int(bad.sum())} cells):")
            pairs = {}
            for p, q in zip(pred[bad], truth[bad]):
                pairs[(p, q)] = pairs.get((p, q), 0) + 1
            for (p, q), k in sorted(pairs.items(), key=lambda z: -z[1])[:10]:
                print(f"    called {p:14s} actually {q:14s} {k:5d} cells")
        res_gt = dict(n=len(gt_ids), label_accuracy=float(agree.mean()),
                      sign_accuracy=float(s_agree.mean()))
    else:
        print("\nno ground truth overlaps our retained neurons")
        res_gt = None

    Path(a.out).write_text(json.dumps(
        dict(bands=res_bands, ground_truth=res_gt,
             n_with_confidence=int(have.sum()), n_neurons=len(ids)), indent=2) + "\n")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
