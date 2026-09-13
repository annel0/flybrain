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

---

## 2026-09-13 — The rewired-connectome control, and it passes

**Why:** the Digital Sphinx critique proposes a real-versus-rewired control as
close to a minimum bar, and of the connectome-based fly models surveyed in
docs/targets/prior-validation.md exactly one had run it. The rewired graph is
a control, not a model: built, measured, discarded.

**Two nulls**, both pure permutations of the postsynaptic column, so out-degree
is untouched and in-degree is preserved exactly. `config` permutes globally;
`superclass` permutes within the edges pointing at each superclass, preserving
the superclass-by-superclass connectivity matrix on top of both degrees.

### First run looked too clean, and it was

Every measurement collapsed to exactly zero on both nulls. A dead network fails
every test trivially, so that reading was worthless until the cause was known.
Checking input statistics ruled out starvation — rewiring *raises* the median
neuron's net drive from +29 to +107, because the real graph is skewed and a
permutation evens it out. The nulls are not starved; the weight was simply
fitted on the real graph.

A coarse sweep then suggested the nulls had no intermediate regime at all,
jumping from 0.09 Hz to 41.6 Hz between two sweep points. **That was also
wrong** — bisection found the intermediate state the sweep had stepped over.

### The fair comparison, at matched spontaneous activity

| | w_syn | self-sustained | cells active | KC recruited | APL block | APL rate |
|---|---|---|---|---|---|---|
| **real** | 0.075 | 1.005 Hz | **1.7%** | **5.6%** | **+83.5 pp** | 249.5 Hz |
| degree-preserved null | 0.307 | 0.905 Hz | 14.5% | 1.3% | **+0.0 pp** | **0.0 Hz** |

At the same mean rate the null spreads activity over eight times as many cells,
recruits a quarter as many Kenyon cells, produces no measurable projection
neuron response to stimulating one glomerulus, and **the APL neuron does not
fire at all**, so the mushroom body's feedback loop is simply absent.

The one causal result this model has passed does not survive rewiring. The
connectome is doing work beyond its degree sequence.

### What this does not establish

The superclass-preserving null could not be activity-matched. Its transition is
razor-thin — 0.1797 gives 0.386 Hz and 0.1798 gives 9.694 Hz — and repeated
evaluations at the same weight returned 9.694, 8.340 and 7.956 Hz, so at the
edge it is chaotically sensitive to the non-determinism of atomic accumulation.
That null therefore was not fairly tested, and the question of whether regional
structure alone suffices is open.

Worth noting for later: the *more* constrained null is the *less* stable one.
Preserving regional structure without cell-level structure concentrates
connectivity into strong local loops with none of the specific inhibition that
regulates them in the real graph.

### One number in the first output was garbage

A selectivity of 230,769,231x came from dividing by a 1e-9 floor when every
non-target projection neuron was silent. Fixed to report undefined instead.
Undefined here means the null produced no projection neuron response at all,
which is a failure rather than perfect selectivity.

---

## 2026-09-13 — Graded local interneurons: prediction falsified, and it costs us

**Prediction under test:** our antennal lobe local interneurons run at ~227-350 Hz
and smear activity across glomeruli, leaving only a 2-6x preference for the
driven one. Some such cells do not spike in the animal at all — they transcribe
the sodium channel gene `para` without translating it (eNeuro 2022). If forcing
non-spiking cells to spike was what smeared the labelled line, making them
graded should sharpen it.

**Implementation:** graded cells never spike, never reset, and release
continuously in proportion to how far they sit above rest, delivered through
the same axonal delay via a small per-cell ring. 177 local interneurons found.

### First run repeated the mistake I had just corrected elsewhere

Selectivity fell from 2.32x to 1.03x and Kenyon cell recruitment exploded from
5.6% to 78.5%. But the gain was set so a graded cell at threshold releases at
50 Hz, while the spiking version was running at 227 Hz — so the change was not
"graded instead of spiking", it was "graded **and five times weaker**", and
these cells are inhibitory. Same error as the first rewiring control: compared
without matching the confound.

### Matched, the answer does not change

| reference Hz | own PN | other PN | selectivity | KC recruited | network |
|---|---|---|---|---|---|
| spiking baseline | 193.5 | 83.5 | **2.32x** | **5.6%** | 1.021 Hz |
| 50 | 203.2 | 196.8 | 1.03x | 78.5% | 3.623 Hz |
| 300 | 60.2 | 57.5 | 1.05x | 76.9% | **1.055 Hz** |
| 2000 | 20.5 | 20.0 | 1.03x | 60.9% | 0.354 Hz |

Selectivity sits at 1.03-1.05x across a **forty-fold** range of gain, including
the setting where network rate matches the spiking baseline almost exactly.
The prediction is falsified: with this transfer function, graded release does
not sharpen the labelled line, it abolishes it.

### The uncomfortable implication

We have been reporting 2-6x glomerular selectivity as evidence the model finds
the right anatomy. That selectivity apparently **depends on the local
interneurons spiking** — and they are the cells we have the clearest evidence
should not spike, at rates we already knew were far too high. So one of our
better-looking results may rest on an artefact we had already identified as an
artefact.

### What this does not settle

The transfer function is rectified-linear with no saturation. Real graded
synapses saturate, and an unsaturating proportional release is uniform
inhibition with no contrast enhancement, which is close to the worst case for a
labelled line. A saturating transfer is the obvious next thing to try, and
until it is tried the finding is about *this* graded model rather than about
graded transmission.

Also unknown, and not knowable from the source paper: what fraction of local
interneurons is actually non-spiking. It characterises one population and does
not quantify the rest. Converting all 177 is an upper bound, not a claim.

---

## 2026-09-13 — Over half the network is cells that do not spike

The visual-system target collection reports that the whole optic lobe pathway
signals with graded potentials — not only photoreceptors and the lamina
monopolar cells we already knew about, but **T4 and T5 themselves**, confirmed
by voltage imaging against calcium imaging (Mishra et al. 2023). The only cell
in that pathway confidently identified as spiking is the giant fibre
descending neuron, which is downstream of it.

Counted in our own graph:

| region | neurons | share |
|---|---|---|
| **optic lobes** | **95,501** | **57.3%** |
| central brain | 37,229 | 22.3% |
| ventral nerve cord | 20,429 | 12.3% |
| other | 13,541 | 8.1% |

So a majority of the network we simulate consists of cells that do not fire
action potentials, and we model every one of them as a leaky integrate-and-fire
neuron.

### This closes the light experiment retroactively

We spent a session driving photoreceptors and measuring the lamina, got a
response in the right direction that died within one synapse, and concluded the
operating point was wrong. The operating point may well be wrong, but it was
never the main problem: we were running a spiking model on a population that
does not spike, and the failure was structural rather than parametric.

### It also bounds where our existing work stands

Everything we have actually validated — the mushroom body, the antennal lobe,
the APL result — sits in the 22% that is spiking. That work is not undermined
by this. Anything visual is.

### An observation-model trap that would have caught us

Calcium-imaging direction selectivity is reported as substantially higher than
the underlying voltage selectivity for the same cells. Nearly all the published
tuning numbers are calcium-based. So comparing a model's raw output against
them systematically reads as "too weak" unless a threshold, filter and
nonlinearity cascade is applied first — the model would look wrong while being
right, and the natural response would be to raise gains until it broke.

### Useful numbers that did arrive

Behnia et al. 2014 gives millisecond-scale delays and rectification ratios for
Mi1, Tm3, Tm1 and Tm2. Chiappe et al. 2010 gives walking-state gain changes of
2.96-6.5x, up to 16x in one animal, with the tuning peak shifting to 6 Hz —
which is a perturbation target with real numbers attached.

---

## 2026-09-13 — Target collection complete: 222 targets, eleven domains

| domain | targets |
|---|---|
| antennal lobe | 35 |
| escape and motor | 41 |
| mushroom body | 32 |
| visual system | 29 |
| whole brain | 23 |
| central complex | 22 |
| male-specific | 20 |
| Shiu predictions | 12 |
| prior validation | 8 |

The Shiu row is the shortfall: 12 of the paper's 164 predictions, and the agent
said so plainly. Those 152 remain the largest single block of causal
constraints available anywhere and are the obvious next collection job.

### The central complex gives us a real falsification test

This circuit carries a single localised bump of activity that tracks the fly's
heading. Our model has no mechanism that could produce one, so this is a test
it can fail cleanly rather than a number it can be tuned toward.

- bump width: FWHM **82-91 degrees** (Seelig & Jayaraman 2015) against **~100
  degrees** (Turner-Evans et al. 2017) — recorded as a conflict, not averaged
- persistence in darkness before drift: **6.7 +- 5.1 s** across 499 bouts in 11
  flies, sometimes beyond 30 s
- PEN-to-EPG bump offset grows with turning speed to **20.7 +- 11.7 degrees**
  at 150-180 deg/s — probably the single most useful number for constraining
  path integration
- landmark jump tracking: slope **0.78 +- 0.07**, r = 0.85, N = 50 shifts
- silencing Delta7 drops the bump's amplitude while leaving its width
  **explicitly unchanged**, so amplitude and width are separately controlled —
  a structural constraint no single rate can express

### And a fact that reframes the whole collection

The most quantitatively characterised circuit in the fly brain contains
**exactly one published spike-rate number**: PEN cells modulate by 5.6 +- 3.7 Hz
between preferred and non-preferred turn directions, N = 12. Everything else in
it is calcium imaging.

That is the observation-model problem in its sharpest form. We built a spiking
simulator, and the best-studied circuit available to test it against was almost
entirely measured in a currency our simulator does not produce. Comparing
against it requires the indicator model, not a threshold we chose.

---

## 2026-09-13 — Replication on Shiu's own connectome: the engine is validated

**Why this and not their 164 predictions directly:** their cell-type names do
not appear in the MaleCNS annotations at all — zero matches against `type`,
`flywireType` or `hemibrainType` — so the predictions cannot be transferred to
our dataset. Running them on theirs answers a different and more basic
question, and separates two things we had been running together: is our engine
correct, and is our model of MaleCNS right.

**Setup:** imported FlyWire 783 exactly as shipped with their repository —
138,639 neurons, 15,091,983 connections, 54.5M synapses, mean out-degree 108.9.
Their protocol: 21 sugar receptor neurons driven at 100 Hz Poisson, w_syn
0.275 mV, 1.8 ms delay, no noise. Target: Supplementary Table 1D, fifteen named
neurons with exact published rates.

### First pass was systematically 17% low, with a precise cause

Median ratio 0.83, correlation 0.957. A uniform shortfall with a high
correlation points at one shared constant rather than at the wiring, and the
arithmetic identified it: their source sets the refractory period of
Poisson-driven neurons to **zero**, and ours kept the 2.2 ms. After a forced
spike, 22 steps are blocked before a geometric wait of ~100, so a cell asked
for 100 Hz delivers 10000/122 = 82 Hz — and everything downstream is low by
that factor. 0.82 against an observed 0.83.

### With that fixed

| neuron | published | ours | ratio |
|---|---|---|---|
| **MN9_r** | **68.0** | **67.8** | **1.00** |
| Zorro_l | 102.2 | 107.2 | 1.05 |
| Rattle_l | 75.4 | 77.2 | 1.02 |
| Phantom_l | 57.6 | 58.4 | 1.01 |
| Usnea_l | 72.6 | 81.9 | 1.13 |
| FMIn_l | 61.3 | 67.6 | 1.10 |
| Fdg_l | 38.3 | 42.2 | 1.10 |
| MN6_r | 31.7 | 27.9 | 0.88 |
| G2N-1_l | 69.4 | 59.2 | 0.85 |
| Roundup_l | 46.3 | 38.1 | 0.82 |
| Clavicle_l | 54.0 | 34.7 | 0.64 |
| Bract_l | 5.1 | 2.5 | 0.49 |

**Median ratio 1.01, correlation 0.970** across thirteen neurons. The motor
neuron the whole paper is built around matches to 0.3%.

**Our engine reproduces published results on the connectome they were
published on.** That is the first thing in this project that has been checked
against someone else's numbers rather than against our own reasoning.

### What it does not cover

Two of the fifteen are absent from this graph: MN9_l and TH-VUM, whose IDs are
not in the completeness table shipped with the repository — a proofreading
version difference, not something we can resolve here. Two outliers remain,
Clavicle at 0.64 and Bract at 0.49; Bract fires at 5.1 Hz with a run-to-run
spread of 1.4, so it is within noise, while Clavicle at 54 Hz is not and stays
unexplained. We ran 10 repeats against their 30.

And it validates the **engine**, not our MaleCNS model. Those remain separate,
which was the point.

### A correction to an earlier claim

Shiu et al. ran a connectivity-shuffling control themselves: across 100
shuffled matrices MN9 fired in 1 of 100, mean 0.0043 Hz against 68 Hz with real
wiring. So the earlier statement — from the prior-validation survey — that
FlyGM was the only model in the field to run that control is wrong. Two did.

---

## 2026-09-13 — First fit: it satisfied its targets, and the run cannot be trusted

400 evaluations, 38 minutes, 8 parameters against 6 fitted targets with 3 held
out. 53 parameter sets satisfy every fitted target simultaneously — which is
itself progress, since earlier we could not find one satisfying both a balanced
operating point and sparse Kenyon cell coding.

Best point: KC recruitment 4.04% (want 6 ± 5), APL block +90.6 pp (want ≥ 20),
APL rate 5.0 Hz (want ≤ 5), KC baseline 0.277 Hz, PN peak 149 Hz, spontaneous
1.01 Hz. Fitted score 0.097.

### Three reasons the result does not support a claim

**Three parameters sat on their bounds.** `w_syn` came out 0.835-1.0 against a
ceiling of 1.0, `inh_gain` 7.76-16 against a ceiling of 16, `tau_mem` 10-24
against a floor of 10. A parameter at its bound means the bound is setting the
answer, not the data.

**The search converged rather than explored.** 52 of the 53 feasible points
come from the second half of the run, median evaluation 339 of 400. The
strategy shrinks its spread 15% per generation, so it *must* converge whether
or not the targets constrain anything. The narrow parameter ranges it produced
are therefore a picture of where the search went, not a measurement of what the
data allows — which means the degeneracy prediction made before this run was
**not tested**, rather than confirmed or refuted.

**It overfitted, visibly.** Fitted score 0.097 against a held-out score of
1.856. Two of three held-out targets fail badly: membrane potentials sit 11
fluctuation widths from threshold against a target of ≤ 3, and 89.9% of the
network is silent against ≤ 60%. The fit met its targets by building a nearly
dead network in which a handful of cells behave correctly.

The correlation between fitted and held-out score across all 400 evaluations is
+0.025 — essentially zero. So this is not the usual overfitting where improving
one degrades the other. It is worse in a quieter way: the six fitted targets
carry **no information at all** about what the held-out ones measure.

### Fixes, all specific

1. Widen the three bounds that were hit, and re-run.
2. Separate the two questions the run conflated: use the converging search to
   *find* a good point, and a uniform or Latin-hypercube sample to *measure*
   the feasible region. One run cannot do both.
3. Either move the two failing held-out targets into the fitted set, or state
   plainly that the model cannot satisfy them — the second being a result.

### Kept as a standing caution

The held-out split is the only reason any of this was visible. Reported on its
fitted targets alone this run looks like a success: six of six satisfied, score
0.097.
