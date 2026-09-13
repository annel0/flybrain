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

---

## 2026-09-13 — Does the imposed clock change the answers?

**Asked:** raised from outside the session — the simulation advances all
166,700 neurons in lockstep every 0.1 ms, nothing in the animal does that, and
that clock is both an artefact and the source of the 8.9x performance ceiling.

Both halves are right, but they are separate problems with separate answers, so
the artefact was measured rather than argued about. Each timestep is a distinct
simulation: refractory counter, delay in steps, ring length, membrane and
synaptic decay factors and the Poisson forcing probability are all recomputed.

| dt (ms) | ring | delay steps | self-sustained Hz | odour Hz | KC recruited | cost |
|---|---|---|---|---|---|---|
| 0.200 | 16 | 9 | 0.967 | 0.952 | 5.1% | 0.4x |
| **0.100** | 32 | 18 | 1.005 | 0.983 | **5.6%** | 0.7x |
| 0.050 | 64 | 36 | 1.036 | 0.998 | 6.0% | 1.4x |
| 0.025 | 128 | 72 | 1.045 | 1.005 | 6.1% | 2.8x |

Relative to the 0.1 ms we have been using: -3.7% / +3.1% / +4.0% on the
self-sustained rate, and -8.8% / +7.9% / +8.4% on Kenyon cell recruitment.

**The sequence converges.** Halving again from 0.05 to 0.025 moves the
self-sustained rate 0.9%, the odour rate 0.7% and recruitment 1.7% relative.
The residual error at 0.1 ms against the converged limit is roughly 4% on rates
and 8% on recruitment, always in the same direction — a coarser step misses
threshold crossings and reports slightly less activity.

### What that settles

**As an accuracy problem it is small and now bounded.** Four to eight percent,
systematic, one-directional. Against the things that actually move results —
the free-parameter weight moved recruitment from 0.2% to 100%, the
excitation/inhibition balance moved the distance to threshold from 19 to 1.2
fluctuation widths, non-spiking neurons we cannot represent at all — the clock
is a rounding error. Every number reported so far survives it.

**As a cost problem it is the whole story, and that was under-sold earlier.**
The dense per-neuron update is 59% of each step, and there are 10,000 steps per
simulated second: 1.67 billion membrane updates per second of fly time. Exact
event-driven integration touches a neuron only when an event reaches it —
about 25 million events per simulated second at 1 Hz. That is a **65-fold**
reduction in work, not a marginal gain, and the earlier dismissal of
event-driven integration named the obstacles (poor GPU parallelism, breaks
under plasticity and graded neurons) without naming that prize.

### One correction to the framing

"A brain has no reference frequency" is right in general and wrong for the
circuit we are working in. Odour-evoked oscillations at 20-30 Hz structure
spike timing in the insect antennal lobe, and Kenyon cells are sensitive to
their phase; separately, `inx7` gap junctions synchronise antennal lobe
activity, which we already noted as missing from the model. The olfactory
system has a rhythm. What it does not have is *our* rhythm — 10 kHz, global,
and identical for every cell.

---

## 2026-09-13 — The ragged sparseness is real, and it names the blocker

**Asked:** is the erratic Kenyon cell recruitment in the balanced regime real,
or an artefact of half-second windows?

**Ran:** `sparseness_variance.py` (5 seeds x 4 weights x 2 window lengths) and
the APL regression test at four operating points.

### It is real, and the source is state dependence

| window | w_syn | recruitment across 5 seeds |
|---|---|---|
| 0.5 s | 1.00 | 68.1 ± 26.3 % [19.9 – 92.1] |
| 2.0 s | 1.00 | 67.2 ± 27.9 % [14.2 – 89.6] |
| 2.0 s | 0.75 | 36.7 ± 4.1 % [32.1 – 41.8] |
| 2.0 s | 2.00 | 48.1 ± 10.6 % [34.3 – 61.7] |

Coefficient of variation across seeds: **54% at 0.5 s, 36% at 2 s**. Quadrupling
the window helps but does not converge, and repeats of one condition span
14% to 90%. The scatter is not measurement noise from a short window — it is
the network's ongoing state at the moment the odour arrives. In a
self-sustaining regime the response rides on whatever the network is already
doing, and that is different every time.

State dependence is biologically real. It also means "recruitment is 5%" is
not a property this regime has; it has a distribution.

### The APL regression test passes everywhere — including where we did not expect

| w_syn | inh gain | APL rate | KC intact | KC, APL blocked | change |
|---|---|---|---|---|---|
| 0.075 | 1 | **249.5 Hz** | 5.6% | 89.1% | +83.5 pp |
| 0.75 | 8 | 30.5 Hz | 30.6% | 100.0% | +69.4 pp |
| **1.0** | **8** | **70.5 Hz** | 16.6% | 99.9% | +83.3 pp |
| 2.0 | 8 | 73.0 Hz | 23.3% | 99.9% | +76.7 pp |

This reframes the earlier result. Our "correct" 5.6% recruitment was obtained
with APL firing at 250 Hz and the whole network in an unbalanced state with
membranes four fluctuation widths from threshold. The balanced regime is better
on every measure we can take — APL at a physiological 30-70 Hz, membranes one to
two fluctuation widths from threshold, self-sustaining without injected noise,
and the APL dependence intact — and worse on exactly one: recruitment sits at
16-31% instead of a few percent.

### Which names the blocker precisely

A point-neuron APL can only implement one global inhibition applied to every
Kenyon cell at once. The measured biology is not that: APL's inhibition is
spatially localised, and an individual Kenyon cell inhibits *itself* through
APL more strongly than it inhibits its neighbours. That per-cell self-inhibition
is the mechanism that holds recruitment low and stable — and it is exactly what
collapsing APL into a single voltage destroys.

So the two criteria not converging is no longer a mystery to be resolved by
more parameter search. It is a missing mechanism with a name. **Compartmentalise
APL, then re-fit.** Until then the sparseness criterion cannot select an
operating point, because the model lacks the thing that sets sparseness.

**Revised standing:** the balanced regime at w = 1.0, inhibitory gain 8, is the
better operating point on present evidence, despite the recruitment figure.
The 0.075 / gain 1 point should not be defended on its 5.6% alone.
