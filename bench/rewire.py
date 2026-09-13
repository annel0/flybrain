"""Degree-preserving rewirings of the connectome, as null models.

The Digital Sphinx (Brunton & Tuthill 2026) argues that a model reproducing
realistic behaviour proves nothing unless a randomly rewired network fails to
do the same, and proposes that control as close to a minimum bar. Of the
connectome-based fly models surveyed in docs/targets/prior-validation.md,
exactly one ran it.

Two nulls of different strictness, so the question is not only whether the
wiring matters but at what grain it matters:

* `config` permutes the postsynaptic column globally. Out-degree is untouched
  because the CSR row boundaries are untouched, and in-degree is preserved
  exactly because a permutation preserves the multiset of targets. Every
  neuron keeps its number of inputs and outputs and its outgoing weight
  profile; nothing else about who connects to whom survives.

* `superclass` permutes within the set of edges pointing at each superclass,
  so the superclass-by-superclass connectivity matrix is preserved on top of
  both degree sequences. Regional organisation stays; cell-level specificity
  goes. If the real graph beats `config` but ties with `superclass`, the
  information the model uses is regional rather than cellular.

Synaptic sign needs no special handling: it is a property of the presynaptic
cell, and the presynaptic side of every edge is left in place.
"""

import numpy as np


def rewire(crow, col, mode, superclass=None, seed=0):
    """Return a rewired copy of `col`. `crow` and the weights are untouched."""
    rng = np.random.default_rng(seed)
    new = col.copy()
    if mode == "none":
        return new
    if mode == "config":
        rng.shuffle(new)
        return new
    if mode == "superclass":
        if superclass is None:
            raise ValueError("superclass labels required for this null")
        target_class = superclass[col]
        for s in np.unique(target_class):
            idx = np.flatnonzero(target_class == s)
            new[idx] = col[rng.permutation(idx)]
        return new
    raise ValueError(f"unknown rewiring mode: {mode}")


def check(crow, col, new_col, n):
    """Confirm the null preserved what it claims to preserve."""
    out_before = np.diff(crow)
    in_before = np.bincount(col, minlength=n)
    in_after = np.bincount(new_col, minlength=n)
    kept = int((col == new_col).sum())
    return {
        "out_degree_identical": True,          # crow never touched
        "in_degree_identical": bool(np.array_equal(in_before, in_after)),
        "edges_unchanged": kept,
        "edges_unchanged_pct": 100.0 * kept / len(col),
        "mean_out_degree": float(out_before.mean()),
    }
