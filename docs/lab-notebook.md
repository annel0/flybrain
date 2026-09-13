# Lab notebook

One entry per experiment, newest last. Each entry records what was asked, what
was run, what came out, and what it changed. Raw logs are in `logs/`, machine
-readable results in `out/*.json`.

Entries are not edited after the fact. When a later run contradicts an earlier
one, the later entry says so and both stay.

---

## 2026-09-13 — Operating point: five experiments, two of my conclusions overturned

**Asked:** measure statistics, keep logs, use git.

**Ran:** `criticality.py`, `one_spike.py`, `operating_point.py`, `balance.py`,
`fit_weight.py --inh-gain 8`. Logs in `logs/20260913T10*`.

### 1. The first branching-ratio estimate was worthless

Regression of consecutive population spike counts gave sigma = 0.943 to 0.995
across weights spanning a near-silent network and a saturated one. That range
is the tell: under constant background noise, consecutive counts correlate
because the mean is stationary, so the slope tends to 1 regardless of what the
network does. It measured stationarity, not propagation. Discarded.

### 2. Measured directly instead: one spike causes nothing

Two runs identical in every respect including the noise seed, differing only in
one neuron forced to spike once. **Drift between two unperturbed runs: 0 spikes**
— bit-identical, so the measurement floor is exact and any difference is causal.

| w_syn | self | gen 1 | gen 2 | total descendants | caused anything |
|---|---|---|---|---|---|
| 0.050 | 0.92 | 0.00 | 0.00 | -0.5 | 4% |
| **0.075** | 1.00 | **0.00** | 0.08 | -1.3 | 8% |
| 0.100 | 1.00 | 0.00 | 0.00 | -0.5 | 8% |
| 0.150 | 1.00 | 0.00 | 0.00 | -0.0 | 4% |
| 0.275 | 1.00 | 0.00 | 0.08 | 138.4 | 8% |

"self" reads ~1 as predicted, which validates the indexing. Generation 1 is
0.00 everywhere: **one spike produces no descendants at any weight tried**, and
only 4-8% of source cells caused anything at all. This is the direct cause of
the light response dying within one synapse.

### 3. Why: the membrane sits four fluctuation widths from threshold

| w_syn | mean u | sd u | gap | gap/sd | within 1 sd |
|---|---|---|---|---|---|
| 0.075 | 0.05 mV | 1.75 mV | 6.95 mV | **4.0** | 0.0% |

Mean membrane potential sits at rest. Firing happens only on 4-sigma
excursions of the injected noise. A single presynaptic spike contributes
0.15-0.75 mV, a fifth of a fluctuation width — far too little to convert a cell.

### 4. But the network is not disconnected, which is where I was wrong

I concluded from the above that the recurrent network contributes nothing.
Removing the noise entirely and kicking 2% of cells for 50 ms shows otherwise:
activity persists at 1.00 Hz for the rest of the run at w = 0.075, and 11.4 Hz
at w = 0.275. **The network sustains itself.** What is true is narrower: at
these weights the self-sustaining activity involves a small fraction of cells
(1-11%) in a reverberating minority, not a distributed state.

### 5. The balanced regime exists, and needs inhibition scaled separately

The connectome says who inhibits whom, not how hard. Adding a separate
inhibitory gain and sweeping, with no injected noise at all:

| w_syn | inh gain | mean Hz | participating | Hz if active | gap/sd |
|---|---|---|---|---|---|
| 0.275 | 1 | 11.41 | 11.3% | 100.9 | 19.1 |
| 1.0 | 8 | 1.46 | 7.0% | 18.9 | **1.9** |
| 1.0 | 16 | 0.53 | 5.8% | 11.0 | **1.2** |
| 2.0 | 8 | 2.39 | 11.2% | 20.2 | **1.5** |

At excitation around 1-2 mV per synapse with inhibition 8-16x stronger, the
network reaches exactly what balanced-network theory describes: self-sustained,
mean potential one to two fluctuation widths below threshold, a few percent of
cells active at ~20 Hz. Inhibitory-to-excitatory ratios of 4-8 are standard in
balanced network models, so this is not an exotic setting.

### 6. But the two criteria do not agree — negative result

Refitting Kenyon cell sparseness inside the balanced regime (inhibitory gain 8):

| w_syn | 0.50 | 0.75 | 1.0 | 1.5 | 2.0 | 3.0 |
|---|---|---|---|---|---|---|
| KC active | 1.9% | 31.1% | 20.6% | 23.1% | 11.6% | 39.1% |

Non-monotonic and erratic. The clean 5.6% we obtained at w = 0.075 with no
inhibitory scaling does not survive into the balanced regime, and no weight
here reproduces it cleanly. So the two independent criteria — a balanced
operating point and measured sparse coding — **do not select the same
parameters**. That is the degeneracy problem arriving on schedule: fitting one
observable constrains the model without identifying it.

**Open, not resolved.** Next: whether the erratic sparseness is a real property
of the balanced regime or an artefact of 0.5 s windows against ongoing
activity, and whether APL-dependence survives there. The APL block regression
test must be rerun at any candidate operating point before it is adopted.
