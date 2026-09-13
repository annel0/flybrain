# What is live here, and what is a record

Kernels were rewritten several times as measurements came in. The superseded
versions are kept rather than deleted, because the reasons they were replaced
are part of the result — see `docs/benchmarks.md` and `docs/lab-notebook.md`.

## Live

| file | role |
|---|---|
| `fly_sim.py` | the simulator: graph, state, per-cell physiology, the step |
| `fly_kernels.py` | membrane with spike compaction, delayed delivery, tally |
| `fast_kernels3.py` | `scatter_stride`, the synaptic scatter in current use |
| `graded.py` | non-spiking cells: continuous release instead of threshold |
| `observables.py` | measures a run the way the source experiments measured |
| `fit.py` | gradient-free search over the unknown parameters |

## Experiments

`replicate_shiu.py` reproduces published firing rates on the connectome they
were published on — the one external check in this repository.
`rewire_control.py` and `rewire_matched.py` are the real-versus-rewired
control. `one_spike.py`, `operating_point.py`, `balance.py` and
`criticality.py` characterise the operating point. `odor.py`, `fit_weight.py`,
`sparseness_variance.py` and `graded_ln.py` are the mushroom body and antennal
lobe work. `timestep.py` bounds the discretisation artefact. `view_brain.py`
and `view_response.py` draw activity on the anatomy.

## Superseded, kept on purpose

| file | why it was replaced |
|---|---|
| `bench_lif.py` | first simulator; torch scatter and a dense spike mask |
| `kernels.py` | first Triton kernel; beaten by Inductor on uniform fp32 and kept only for the mixed-precision case it fixed |
| `fast_kernels.py` | one program per spike-buffer slot, so 54 of every 55 launched only to exit |
| `fast_kernels2.py` | lane-split scatter, measured 2.9x **slower** — the diagnosis behind it was wrong |
| `final.py`, `opt_bench.py`, `tune*.py` | the optimisation passes that produced those numbers |
| `precision_error.py`, `test_fusion.py` | the fp16/bf16 and fusion measurements |

`fast_kernels2.py` in particular is worth keeping: it is a correct
implementation of a fix for a problem that turned out not to exist.
