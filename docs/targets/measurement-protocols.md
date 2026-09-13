# Measurement protocols

This file documents **how** the numbers in the other target files were produced,
so our extractor can reproduce the instrument, not just the biology. Per the
project's own [`README.md`](README.md): a target without its measurement
method is not usable, and every target's **Observation model** field should
point back to a specific transformation defined here rather than re-derive one
ad hoc.

The reasoning throughout is the same in every section: our simulator has
privileged access no experiment has — every spike, of every neuron, with
infinite precision, from a population whose exact composition and connectivity
we also know exactly. A published number never has that access. It is the
output of an imperfect instrument (a calcium indicator, an electrode, a
trained observer scoring behaviour) applied to a nervous system under specific,
often unstated, physiological conditions. **Comparing our raw output to their
processed output is comparing different quantities.** The fix is always the
same shape: degrade our ground truth through the same instrument and the same
conditions before comparing, and where that degradation cannot be built (a
missing forward model, an unmeasured constant, a body and motor system we do
not simulate), say so plainly rather than compare anyway.

Confidence tags below follow the README's convention (high / medium / low).
Where a search of the literature in this pass could not pin a number down
precisely, it is marked low confidence with a pointer to the primary source to
check before hard-coding it.

## Contents

1. [Calcium imaging](#1-calcium-imaging)
2. [Patch-clamp and sharp-electrode electrophysiology](#2-patch-clamp-and-sharp-electrode-electrophysiology)
3. [Electrode arrays, LFP, and subsampling bias](#3-electrode-arrays-lfp-and-subsampling-bias)
4. [Behavioural assays](#4-behavioural-assays)
5. [Conditions that make targets mutually inconsistent](#5-conditions-that-make-targets-mutually-inconsistent)
6. [Summary: what each transformation needs](#6-summary-what-each-transformation-needs)

---

## 1. Calcium imaging

### 1.1 Indicators and kinetics

Fly work spans four indicator generations. Rise/decay figures below are for a
**single action potential** unless noted; they lengthen and change shape for
bursts (§1.2). "Rise"/"decay" are reported inconsistently across papers as
either an exponential time constant, a 10–90% rise time, or a half-time —
treat the numbers here as representative, not exact, unless flagged high
confidence.

| Indicator | τ rise (1 AP) | Decay (1 AP) | Notes | Confidence |
|---|---|---|---|---|
| GCaMP3 | not pinned down here | on the order of several hundred ms | Used in the founding Kenyon-cell sparse-coding imaging papers (2011–2013 era, e.g. Honegger, Campbell & Turner below). Low single-spike sensitivity; responses in that literature are effectively multi-spike-burst signals. | Low — re-derive exact figures from [Tian et al. 2009](https://www.nature.com/articles/nmeth.1398) Table 1 before hard-coding |
| GCaMP5 | not pinned down here | not pinned down here | Brighter than GCaMP3; rarely the indicator of choice in current fly work. | Low — [Akerboom et al. 2012](https://www.jneurosci.org/content/32/40/13819) |
| GCaMP6f | ≈ 30–45 ms | ≈ 140–150 ms | "Fast" variant; current default for population imaging of transient events. | Medium–high — [Chen et al. 2013](https://www.nature.com/articles/nature12354), values vary by prep (culture vs. mouse V1 in vivo) |
| GCaMP6s | ≈ 150–180 ms | ≈ 550–600 ms | "Slow"/sensitive variant: bigger ΔF/F per spike, worse temporal resolution. | Medium–high — Chen et al. 2013 |
| jGCaMP7f | reported ≈ 60 ms half-rise in one secondary summary | reported ≈ 150 ms | Meant to match 6f's speed with more sensitivity; the 60 ms half-rise figure above is *slower* than 6f's, which is inconsistent with that design goal and was not independently confirmed against the primary source in this pass. | **Low — verify against** [Dana et al. 2019](https://www.nature.com/articles/s41592-019-0435-6) **Table 1 before use** |
| jGCaMP7s / 7b / 7c | not pinned down here | not pinned down here | 7s: highest sensitivity, slowest. 7b: brighter in neurites/neuropil. 7c: large ΔF/F, aimed at wide-field/population imaging — this is the variant used in the one direct fly spike/calcium calibration found (§1.6). | Low |
| jGCaMP8f | ≈ 2 ms half-rise | 192 ± 26 ms half-decay | Fastest GECI published to date; tracks individual spikes up to ≈ 50 Hz. | High — [Zhang et al. 2023, Nature](https://www.nature.com/articles/s41586-023-05828-9) |
| jGCaMP8m | ≈ 2 ms half-rise | 137 ± 21 ms half-decay | | High — Zhang et al. 2023 |
| jGCaMP8s | ≈ 2 ms half-rise | 198 ± 21 ms half-decay | Most sensitive of the 8-series. | High — Zhang et al. 2023 |

None of the rise/decay constants above were measured in *Drosophila* neurons —
all come from mouse cortex (or culture) characterization papers. This is the
default in the field: treat cross-species transfer of kinetics as a modelling
assumption, not a measured fact, when it matters (it usually does not, since
decay time constants are set by calcium buffering/extrusion and indicator
chemistry more than by cell type, but flag it once in code as an assumption).

### 1.2 Nonlinearity: fluorescence vs. spike count

GCaMP fluorescence is not proportional to instantaneous calcium, and calcium
is not proportional to spike count. Two documented regimes:

- **Cooperative/supralinear at low spike counts.** GCaMP has four
  calmodulin-derived Ca²⁺-binding sites with cooperative (Hill-type, reported
  Hill coefficients up to ≈ 3) binding. For GCaMP6f, a 10-spike burst produces
  a response **≈ 20-fold** larger than one spike — far more than 10× —
  consistent with positive cooperativity ([Zhang et al. 2023](https://www.nature.com/articles/s41586-023-05828-9); modelled explicitly in
  [precise calcium-to-spike biophysical models](https://pmc.ncbi.nlm.nih.gov/articles/PMC12045362/)).
- **Saturation at high spike counts.** jGCaMP8f's equivalent ratio is only
  **≈ 3-fold** for 10 spikes vs. 1 — not because it is "more linear" but
  because it saturates earlier; a flatter burst/single ratio can mean either
  thing and the two require opposite corrections (a compressive Hill
  nonlinearity for supralinearity vs. a ceiling for saturation), so do not
  collapse this into a single "linearity" verdict per indicator without
  checking which regime applies to the spike-count range in question.

**The one direct *Drosophila* calibration found** (§1.6) reports an
approximately **linear** relationship between continuous firing rate and peak
ΔF/F for GCaMP6m, jGCaMP7c and jGCaMP8s, across 0–400 Hz, with R² ≈ 0.7–0.8
and indicator-dependent slopes (jGCaMP8s significantly shallower than jGCaMP7c,
p = 0.0042). This is a different regime from the single/few-spike
cooperativity numbers above — it is a peripheral olfactory receptor neuron
firing continuously at tens–hundreds of Hz, not a sparse central neuron
producing a handful of spikes. **There is no published calibration of the
spike-count-to-ΔF/F relationship for sparsely-firing central neurons in
Drosophila** (e.g. Kenyon cells, which is exactly the regime this project's
mushroom-body sparseness target lives in). Treat any gain constant applied to
KC-like cells as an extrapolation across both cell type and firing regime, and
flag it as such in code and in any target that depends on it.

### 1.3 Detection floor

There is no fixed "minimum number of spikes" independent of imaging
conditions — detectability is an SNR problem, and the honest way to get a
floor is to run the full noise model (§1.7) and see where it crosses the
paper's own stated threshold, not to hard-code a spike count. For context,
best-published values (all mouse cortex, none fly-specific):

- Under **best-case, single-cell, high-SNR** imaging, GCaMP6s detects a single
  action potential with probability **0.99**, GCaMP6f with probability
  **0.84**, both at a 1% false-positive rate ([Chen et al. 2013](https://www.nature.com/articles/nature12354)).
- Under **typical population-imaging** conditions (hundreds of neurons in one
  field of view, lower per-cell SNR), single-spike detection at a 5%
  false-positive rate falls to roughly **10–40%** depending on the cell and
  field-of-view size ([Huang et al. 2019, eLife](https://elifesciences.org/articles/51675)).

This is a real evidentiary gap for this project specifically: our clearest
existing target (mushroom-body sparseness, a few percent of Kenyon cells
active) sits exactly in the low-spike-count regime where the floor matters
most, and no one has measured it there. Implement the full forward model
(§1.7) so the floor emerges from the noise level actually reported or implied
by the target paper, and flag any KC-level "responding" call as sensitive to
an unmeasured assumption.

### 1.4 Typical imaging frame rates in fly experiments

| Modality | Rate | Example / source |
|---|---|---|
| Single-plane, few ROIs | 5–10 Hz typical, up to ~30 Hz with resonant scanning | Mushroom body single-plane KC imaging at 5 Hz |
| Early population imaging, false-colour | ~4 frames/s | Early antennal lobe population imaging |
| Volumetric, piezo multi-plane (classic population imaging) | ~1–5 volumes/s | e.g. 5 axial planes at 2 volumes/s over a mushroom-body-sized volume |
| Volumetric, modern piezo (≈50 planes) | ~2.2 volumes/s | Representative of current "standard" whole-region volumetric two-photon |
| Volumetric, state-of-the-art (2020s "light beads microscopy") | 28–60 volumes/s | [High-speed whole-brain imaging in Drosophila](https://www.nature.com/articles/s41467-026-72437-1), 2026 — not representative of most existing published targets, which predate this |
| Fly-specific spike/calcium calibration recording (§1.6) | 10 Hz | [Simultaneous recording of spikes and calcium signals...](https://pmc.ncbi.nlm.nih.gov/articles/PMC12262726/) |

**Implication:** most of the mushroom-body/antennal-lobe imaging literature
this project will draw targets from was collected at **1–10 Hz effective
sampling**, an order of magnitude below our simulation's native 0.1 ms (10 kHz)
resolution and below even the fast-GCaMP decay time constants in §1.1. The
downsampling step in the transformation below is not a formality — at 5–10 Hz
a paper's frame is integrating over 100–200 ms, comparable to or longer than
GCaMP6f's whole decay, and several of our simulated bins collapse into one of
theirs.

### 1.5 What "a responding cell" operationally means

The recurring pattern across the papers surveyed: a cell counts as responding
if its ΔF/F during (or shortly after) stimulus presentation exceeds a multiple
of the baseline noise's standard deviation, evaluated over a stated window,
against a stated baseline. Representative example, from a fly antennal-neuron
imaging paper: response amplitude during stimulus must exceed the pre-stimulus
baseline mean by **3 SD for excitatory** responses and **2 SD for inhibitory**
responses (asymmetric threshold — inhibitory dips are held to a looser
standard because inhibition is smaller in absolute ΔF/F terms).

Two distinct measurement families exist for "Kenyon cell sparseness"
specifically, and they are **not the same quantity**:

- **Calcium-imaging-based**: fraction of cells crossing a ΔF/F-vs-SD
  threshold (as above) during an odour window, e.g. [Honegger, Campbell &
  Turner 2011](https://www.jneurosci.org/content/31/33/11772) (GCaMP3,
  two-photon, >100 MB neurons imaged simultaneously, ≈5% of the population
  responsive to a given odour) and [Campbell et al.
  2013](https://www.jneurosci.org/content/33/25/10568) (same lab, GCaMP,
  population code framing).
- **Electrophysiology-based**: fraction of cells with a statistically
  significant spike-rate increase over baseline across repeated trials, e.g.
  [Turner, Bazhenov & Laurent 2008](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf)
  (whole-cell, in vivo) and the sparse-coding/APL-feedback electrophysiology
  in [Lin et al. 2014, Nature Neuroscience](https://www.nature.com/articles/nn.3660)
  (already load-bearing for this project's APL-block validation, per
  `docs/theory-review.md`).

Before comparing our simulated recruitment fraction to any single "~5%"
number, check which family it came from — an imaging threshold and a spike-rate
significance test are different statistical procedures applied to different
physical quantities, and will not have identical false-positive/negative
behaviour even on the same underlying activity.

### 1.6 The actual spike-rate ↔ ΔF/F calibration in Drosophila

The only direct simultaneous electrophysiology + calcium imaging calibration
found in Drosophila: [Simultaneous recording of spikes and calcium signals in
odor-evoked responses of Drosophila antennal neurons](https://pmc.ncbi.nlm.nih.gov/articles/PMC12262726/)
(2025). Odorant receptor neuron ab2A, single-sensillum recording plus GCaMP6m
/ jGCaMP7c / jGCaMP8s imaging simultaneously.

- Linear correlation between spike firing frequency and peak ΔF/F across the
  full range tested (over 400 Hz), R² ≈ 0.7–0.8 for GCaMP6m against methyl
  acetate.
- Slopes differ significantly between indicators (jGCaMP8s shallower than
  jGCaMP7c, p = 0.0042); GCaMP6m and jGCaMP7c had statistically
  indistinguishable slopes (p = 0.32).
- Imaging at 10 Hz, 470 nm excitation, 50 ms pulses at 50% duty cycle.
- n = 7 flies (dual recordings), n = 69 sensilla / 7 flies (imaging survey),
  n = 36 neurons / 6 flies (electrophysiology-only survey).

This is peripheral, high-firing-rate, single-neuron-type data. It is the best
grounding available for a spike-rate-to-ΔF/F gain constant, but using it for
central neurons (projection neurons, Kenyon cells, antennal lobe
interneurons — the actual cell types in this project's connectome) is an
extrapolation, not a validated transfer. Flag it as such wherever it is used.

### 1.7 Transformation: spikes → comparable calcium signal

Given our exact spike train(s) for a modelled neuron or population:

1. **Pick the indicator** the target paper used, and its τ_rise / τ_decay
   (§1.1). If the paper predates 2013, assume GCaMP3 or 5 and flag low
   confidence on kinetics.
2. **Build a single-spike kernel** `k(t) = A · (1 − exp(−t/τ_rise)) ·
   exp(−t/τ_decay)` for t ≥ 0 — the standard double-exponential calcium
   transient shape used throughout the deconvolution literature. `A` (the
   single-spike ΔF/F amplitude) depends on indicator and expression level and
   is generally not known a priori; treat it as a free scale unless the paper
   or §1.6 supplies one, and say so when reporting a result that depends on it.
3. **Convolve** the spike train with `k(t)` to get a continuous
   fluorescence-proxy trace.
4. **Apply the appropriate nonlinearity** (§1.2): a compressive/cooperative
   correction if working near the single-to-few-spike regime with a GCaMP6-era
   indicator, negligible correction for jGCaMP8 (near-linear until it
   saturates), and the fly-specific linear gain from §1.6 only when the target
   cell type and firing regime resemble the ORN calibration (continuous,
   tens–hundreds of Hz) rather than sparse bursts.
5. **Add baseline noise.** Best practice: don't invent a noise level —
   back it out from the paper's own reported detection performance (if they
   can detect a response of amplitude X at N SD, and X implies a certain
   number of underlying spikes via steps 2–4, solve for the σ that makes that
   true) rather than assuming a number from a different lab's rig.
6. **Downsample**: box-car average over one exposure/volume period, then
   sample at the paper's frame rate (§1.4). Do not skip this even after doing
   the kinetic convolution carefully — at 1–10 Hz it is often the dominant
   source of information loss, not the indicator kinetics.
7. **Compute ΔF/F** against a baseline F0 defined exactly as the paper states
   (commonly the mean of a pre-stimulus window of a few hundred ms to a few
   seconds; a running low percentile for spontaneous-activity papers).
8. **Apply the paper's response criterion** — same statistic (peak / mean /
   integral), same window, same SD multiple, same consecutive-frame
   requirement if any (§1.5) — to classify "responding," and report the
   resulting fraction, not the fraction of cells with any nonzero true spike
   increase.
9. **Repeat across simulated seeds/trials** the same number of times the
   paper repeated across flies, and report a mean ± spread the same way,
   rather than a single run (see §4.5 — this project's own
   `bench/sparseness_variance.py` result, 36–54% coefficient of variation
   across seeds, shows this is not a formality here).

### 1.8 Confidence and gaps

- High confidence: jGCaMP8 kinetics, Chen et al. 2013 single-AP detection
  probabilities, the qualitative cooperativity/saturation contrast between
  GCaMP6f and jGCaMP8f, the Drosophila ORN linear calibration (§1.6).
- Low confidence / unresolved: exact GCaMP3/GCaMP5/jGCaMP7-family kinetic
  constants (flagged inline above — re-derive from primary tables before
  hard-coding); any spike-to-ΔF/F calibration for central, sparsely-firing fly
  neurons (does not exist yet); the single-spike amplitude constant `A` for
  any indicator in situ in the fly brain (expression-level dependent, not a
  universal constant).

---

## 2. Patch-clamp and sharp-electrode electrophysiology

### 2.1 Preparations

Two preparation families are in current use, and papers do not always state
which clearly:

- **Ex vivo whole-brain explant**: brain dissected whole out of the head
  capsule into a recording chamber, immobilised with tissue glue. Gives full
  access to central-brain neurons, easy solution exchange/temperature control,
  but is a fully isolated brain with no body, no sensory periphery beyond
  whatever is left attached, and no behaviour. Origin: [Gu & O'Dowd 2006];
  current protocol: [Roemmich, Schutte & O'Dowd 2018, Bio-protocol](https://cshprotocols.cshlp.org/content/2022/8/pdb.prot107935)
  — cells preserved and "functional" for **up to about 1 hour** after
  dissection.
- **In vivo, head-fixed**: fly alive and tethered, a small cuticle window cut
  and the brain desheathed locally over the target region, saline
  superfused; sensory periphery and (if the setup allows leg movement /
  behaviour on a ball) some behavioural context are intact. Origin for
  central-brain whole-cell in this prep: Wilson & Laurent-style antennal-lobe
  recordings.

**Two different saline families are used for two different purposes, and
conflating them silently is a real risk:**

| Purpose | Composition found | Notes |
|---|---|---|
| Preserve network activity (sensory-driven / spontaneous spike rate targets) | Bicarbonate-buffered, carbogen-gassed: 103 NaCl, 3 KCl, 5 TES, 8 trehalose, 10 glucose, 26 NaHCO₃, 1 NaH₂PO₄, 1.5 CaCl₂, 4 MgCl₂ (mM), 270–275 mOsm, bubbled 95% O₂/5% CO₂, pH 7.3 — an "adult hemolymph-like saline" (AHLS) type recipe (see [CSH Protocols: Drosophila AHLS](https://cshprotocols.cshlp.org/content/2013/11/pdb.rec079459.full)) | No receptor blockers. Fair comparison target: our intact-network spike rate/Vm. |
| Isolate intrinsic/passive membrane properties | HEPES-buffered, room-air: 122 NaCl, 3.0 KCl, 1.8 CaCl₂, 0.8 MgCl₂, 5.0 glucose, 10 HEPES (mM), pH 7.2, 250–255 mOsm, **plus 20 µM (+)-tubocurarine and 10 µM picrotoxin** (nicotinic and GABA-A block); voltage-clamp variant substitutes 1.8 mM CoCl₂ for CaCl₂ and adds 2.5 mM TEA + 1.0 mM 4-AP | [Roemmich, Schutte & O'Dowd 2018](https://cshprotocols.cshlp.org/content/2022/8/pdb.prot107935). **A neuron recorded here is pharmacologically disconnected from its network.** Fair comparison target: a version of our model with that cell's synaptic conductances zeroed, never the intact network. |

Neither recipe is universal; the field is not standardized (see also the
larval-NMJ-specific HL3.1 solution, which is a different preparation entirely
and not relevant to adult central-brain targets).

### 2.2 Temperature, duration, throughput

- **Temperature**: both prep types are most commonly run at **room
  temperature** (≈20–22°C reported explicitly in one protocol), sometimes
  actively heated toward 25°C or higher when temperature is a deliberate
  variable. Fly rearing is standardly 25°C. **This mismatch (room-temperature
  recording of an animal reared and behaviourally tested at 25°C) is common
  and rarely discussed as a confound** — see §5 for the size of temperature
  effects on firing.
- **Duration**: ex vivo explant neurons remain viable/patchable for **up to
  ≈1 hour** post-dissection. Sharp-electrode recordings, which damage the
  membrane less, can hold "minutes to hours."
- **Throughput**: both techniques are low-throughput and effectively
  terminal — typically **one recording per fly**, one cell at a time. Typical
  published sample sizes for a given cell type run to a few dozen cells across
  many flies (e.g. Kenyon cell intrinsic properties below), not the hundreds
  our simulator could trivially "record" from at once. If a comparison is
  meant to reproduce a paper's actual statistical power, subsample our
  population to a comparably small N rather than pooling the full modelled
  population.

### 2.3 What is measured, with concrete Kenyon-cell numbers

From [Turner, Bazhenov & Laurent 2008, J Neurophysiol](https://www.bazhlab.ucsd.edu/wp-content/uploads/2014/04/JNeurophys2008.pdf)
(in vivo whole-cell, Kenyon cells):

- Input resistance: **2.5 ± 1 GΩ**
- Whole-cell capacitance: **2.7 ± 0.8 pF** (Kenyon cells are near the
  practical lower size limit for patch-clamp — see accessibility bias below)
- Resting potential immediately after break-in: **−53 ± 9 mV**
- Resting potential 5 minutes after break-in: **−55 ± 10 mV**

That last pair of numbers is direct, quantified, in-fly evidence of §2.4's
first bias.

### 2.4 Known biases

1. **Whole-cell dialysis / rundown.** The pipette solution replaces cytoplasm,
   washing out soluble second messengers, native calcium buffers, and ATP. The
   Kenyon-cell numbers above show a measurable **≈2 mV hyperpolarizing drift
   within 5 minutes** of break-in. Our simulated Vm is stationary and has no
   equivalent process; when a target ties a number to a specific post-break-in
   time, prefer the earliest reported value as more "native," and treat later
   values as carrying a small, technique-specific, uncorrectable offset — do
   not tune a model parameter to match a late-recording number exactly.
2. **Dissection/exposure injury.** Both preparations require cutting cuticle
   and exposing (or fully removing) the brain to saline; whole-cell access
   additionally requires enzymatic/mechanical desheathing, removing a glial
   layer that provides mechanical, ionic, and trophic support. There is no
   clean "undisturbed" baseline to compare against — the existence of a
   [saline-free surgical prep developed specifically to avoid this](https://pubmed.ncbi.nlm.nih.gov/42101939/)
   is itself evidence the field treats standard saline exposure as a
   non-negligible confound. Treat any single ex vivo/in vivo baseline activity
   level as possibly displaced from the intact animal's, in an unknown
   direction, rather than as ground truth.
3. **Electrode leak conductance.** A patch seal or sharp-electrode
   penetration adds a leak conductance in parallel with the membrane, so
   measured input resistance is a systematic **underestimate** of the true
   value, by an amount that depends on seal quality and is essentially never
   reported quantitatively. **No general correction exists.** Treat published
   Rin as a lower bound, not a target to fit exactly.
4. **Accessibility/size sampling bias.** Patch-clamp selects for larger, more
   superficial, mechanically robust somata. Kenyon cells (2.7 ± 0.8 pF) are
   near the practical floor of what is patchable at all; many small or deep
   central neurons in this project's connectome were likely never sampled in
   any electrophysiology study. If comparing a full simulated population to a
   paper's N cells, restrict to a plausibly-sampled subset when a size/depth
   proxy exists, and flag the mismatch when it doesn't.

### 2.5 Transformation: our Vm/spike trace → comparable electrophysiology quantity

1. Identify the saline/pharmacology condition (§2.1 table). If synaptic
   blockers were present, compare against a version of our model neuron with
   its synaptic inputs zeroed for that condition — never against the intact
   network.
2. Match recording duration/window: truncate to the reported length, not the
   full simulated run.
3. Match or flag temperature (§5); if unstated, assume room temperature
   (≈20–22°C) rather than the 25°C rearing/behavioural default, and note the
   two are not the same.
4. Extract the same statistic (mean firing rate, resting Vm at a stated time,
   Rin from a stated test-pulse protocol) over the matched window.
5. For Rin/Cm comparisons, treat the published value as a lower/biased bound
   per §2.4.3, not an exact target.
6. If the target ties a Vm number to a specific post-break-in time beyond a
   minute or two, apply no correction but note the likely small hyperpolarizing
   offset (§2.4.1) when judging goodness of fit.
7. Match N: report our result across as many independent simulation
   replicates as the paper had cells, not pooled over the full population,
   when the comparison is meant to be statistically like-for-like.

### 2.6 Confidence and gaps

High confidence on the Kenyon-cell numbers (directly sourced, Turner, Bazhenov
& Laurent 2008) and on the qualitative existence and direction of all four
biases in §2.4. Low confidence / not found: a quantitative dissection-injury
magnitude (no paper quantifies "how much does desheathing itself change spike
rate"); a general formula for the electrode-leak correction (none exists in
the literature — it is universally treated as an unquantified lower bound).

---

## 3. Electrode arrays, LFP, and subsampling bias

### 3.1 What is actually recorded

A multi-electrode array or LFP probe records from a tiny fraction of the
population it sits in: classically **on the order of 60 channels out of
10⁴–10⁵ neurons** in cortical-culture and cortex work (the setting that
motivated the estimator below), and, in the one fly-specific instance found,
a **16-channel silicon probe inserted through the eye** into the central
brain of a tethered fly ([Whole-brain electrophysiology in Drosophila during
sleep and wake](https://cshprotocols.cshlp.org/content/2024/9/pdb.prot108418);
[Fly seizure EEG](https://pmc.ncbi.nlm.nih.gov/articles/PMC13186001/) and
related [van Swinderen lab](https://www.biorxiv.org/content/10.1101/049460v1.full)
isoflurane/LFP work) — against a central brain of order 10⁵ neurons, at least
as extreme a subsampling ratio as the cortical case.

Each channel records either **multi-unit spiking activity** near its tip, or a
**local field potential**, generally understood to mainly reflect summed
local synaptic/dendritic current rather than spikes directly. Our model is
point neurons with no dendritic compartments and no extracellular volume
conductor: **we cannot synthesize a genuine LFP.** The only defensible proxy
is pooled spike counts from model neurons in a chosen anatomical grouping,
standing in for "activity near an electrode" (a multi-unit-activity proxy).
Any target reported as an LFP amplitude or frequency-band power (rather than a
spike-derived statistic like a branching ratio or an avalanche exponent from
threshold-crossing events) should be flagged as **currently out of reach**
without an added biophysical forward model for extracellular potentials — do
not substitute a spike-count proxy and call it equivalent.

### 3.2 The naive estimator, and why it is biased

The conventional branching-ratio estimator regresses population activity at
one time step against the next:

```
m_naive = Σ a(t)·a(t+1) / Σ a(t)²      (linear regression through the origin)
```

**This project's own `bench/criticality.py` already implements exactly this**
(`branching_ratio()`), and the lab notebook already recorded the textbook
symptom of subsampling/stationarity confound: regressing consecutive
population spike counts gave σ = 0.943–0.995 across networks ranging from
near-silent to saturated, correctly diagnosed there as "measuring stationarity,
not propagation," and discarded. That diagnosis is exactly the phenomenon the
literature below explains and fixes — the multistep correction is the direct,
citable follow-up to re-run before trusting or discarding a branching-ratio
measurement again.

Why it's biased under subsampling: let `A(t)` be the true full-population
activity and `a(t) = α·A(t) + noise` be what a sparse or subsampled recording
sees. [Wilting & Priesemann 2018, Nature Communications](https://www.nature.com/articles/s41467-018-04725-4)
show that the *k*-step regression slope

```
r_k = slope of linear regression of a(t+k) on a(t),  for k = 1 .. k_max
```

follows, under full sampling, the clean exponential `r_k = m^k`. **Under
subsampling it becomes `r_k = b · m^k`**, where `b = α²·Var[A_t]/Var[a_t]` is a
constant that does not depend on `k`. The naive one-step estimator is just
`m_naive = r_1 = b·m` — contaminated by the unknown, subsampling-dependent
factor `b`, and the contamination is **not a simple multiplicative rescaling
by the sampling fraction** — it is nonlinear and severe.

### 3.3 The correction: multistep regression (MR) estimator

Because `b` is the same at every lag `k`, it can be fit out: compute `r_k` for
`k = 1 .. k_max` (choose `k_max` a few multiples of the expected
autocorrelation time) and fit

```
r_k ≈ b̂ · m̂^k          (nonlinear least squares over b̂, m̂;
                          equivalently, linear regression of log r_k on k
                          where r_k > 0)
```

`m̂` recovered this way is **consistent regardless of the subsampling
fraction** — this is the entire point of the estimator, proved analytically in
the source paper. The fitted `m̂` also converts to a physical relaxation time
via `τ = −Δt / ln(m̂)` (equivalently `m̂ = exp(−Δt/τ)`), useful as a sanity
check against known circuit timescales.

**Documented size of the naive bias** (Wilting & Priesemann 2018, simulated
branching networks with known true `m`):

| True m | Sampling | Naive m̂ (one-step) | MR estimate |
|---|---|---|---|
| 0.9 | 10% of units | **0.312** | ≈ 0.9 (recovered) |
| 0.9 | 1% of units | **0.047** | ≈ 0.9 (recovered) |
| 0.954 | single unit out of the population | **0.057** | ≈ 0.954 (recovered) |

The bias is always **downward** for this class of models — subsampling can
make a near-critical or reverberating network look like an almost-random one,
never the reverse. A subsampled naive estimate close to 1 is therefore strong
evidence the true value is at least that close (or closer); a subsampled
estimate well below 1 is close to uninformative about the true value without
the correction.

### 3.4 Avalanche size/duration exponents: no equivalent correction exists

Subsampling also distorts avalanche statistics (`avalanches()` /
`power_law_exponent()` in `bench/criticality.py`), but **there is no analytic
fix analogous to the MR estimator.**
[Priesemann, Munk & Wibral 2009, BMC Neuroscience](https://bmcneurosci.biomedcentral.com/articles/10.1186/1471-2202-10-40)
showed that with too few sampled sites, the observed avalanche-size
distribution develops an artefactual feature near the number of active
channels, and the recovered exponent depends on how many sites were sampled —
not only on the true underlying process. More sampling sites reduce, but do
not eliminate, the effect.

**Practical consequence: there is no way to "correct" a subsampled
experimental exponent back to a full-population value after the fact.** The
only valid comparison is to degrade our fully-observed simulation to the same
channel count, placement, and time-binning as the experiment, and compare the
two *subsampled* exponents to each other. Never compare our full-population
exponent — an option no real experiment has — directly to a published
subsampled one; the disagreement would be a measurement artefact, not a
finding about the model.

### 3.5 Transformation: full population → subsampled, matched statistics

1. Start from the full-population spike train (always available to us).
2. Choose the subsample to match the target: number of channels/units `K`,
   and anatomical spread if stated. If unstated, draw **many** independent
   random `K`-neuron subsamples rather than one — the bias depends on the
   specific subsample draw, not only on `K`.
3. Bin the subsampled spikes into time bins of width Δt matching the paper;
   if unstated, the field's classical convention is Δt equal to the average
   inter-event interval of the recorded population ([Beggs & Plenz
   2003](https://www.jneurosci.org/content/23/35/11167), the paper that
   established the avalanche framework).
4. Compute, on this subsampled/binned series:
   - the naive one-step estimator (comparable to a paper that itself only
     reports the naive number — most do);
   - the MR-corrected estimate (comparable to a paper using the MR estimator,
     or as our internal best estimate of the "true" value);
   - avalanche size/duration distributions and exponents, on the *same*
     subsampled series — never on the full population when comparing to a
     published exponent.
5. Report the full-population and subsampled values side by side, clearly
   labelled, so it is never ambiguous which is being compared to which kind of
   source.

### 3.6 Confidence and gaps

High confidence: the MR estimator's equations and the numeric bias table
(directly from the primary source, analytically proved, not just an empirical
regularity). High confidence that our own `criticality.py` currently computes
only the naive, biased version. Low/no correction available: avalanche
exponent de-biasing (match by degrading both sides, do not attempt to invert);
true LFP synthesis from a point-neuron model (not attempted; flag and skip
LFP-amplitude targets rather than fake them).

---

## 4. Behavioural assays

A cross-cutting caveat before the individual assays: **none of PER, T-maze
learning, or grooming can currently be produced by this model end-to-end.**
This project's connectome-based simulator has spiking sensory/central
circuits but, per `docs/theory-review.md` and `docs/lab-notebook.md`, no body,
no motor output stage, and no synaptic plasticity rule. Each subsection below
gives the assay's real operational definition and variability so a target file
can record it correctly, and then states explicitly what would be needed
before our model could produce the matching quantity — which, for three of the
four assays, is "a component we do not have," not a transformation we can
apply today.

### 4.1 Proboscis extension response (PER)

- **What is counted**: binary per-trial score. A positive response requires
  full proboscis extension with sustained contact/feeding for **≥1 second**
  (visible oesophageal movement); flies that do not respond to a positive
  control (e.g. 4% sucrose) are typically excluded from the dataset rather
  than scored as non-responders.
- **Reported as**: fraction of flies (or fraction of trials for one fly)
  responding, per group.
- **Typical N**: **≥8–12 flies** per group is standard, with some protocols
  recommending ≥12 when comparing mutants against controls in case effect
  sizes are small.
- **Trial-to-trial variability**: PER habituates across repeated stimulation;
  an individual fly's early-trial response pattern (number of extensions in
  the first 5 trials, which trial it first stops responding) predicts its
  short-term and 1-hour habituation trajectory — i.e., trial-to-trial
  variability is not noise around a fixed probability but a systematic,
  fly-specific decay ([course of habituation study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3384023/)).
- **What would be needed to produce this**: gustatory receptor neuron input
  (not currently driven in this model, which is built around the olfactory
  pathway) and a defined motor/premotor threshold on a proboscis-extension
  descending or motor neuron. *If* such a pathway is identified in the
  connectome, the closest honest transformation is: drive the taste input
  population at a Poisson rate representing the tastant, take spike count of
  the identified premotor output in a response window, threshold it, and
  report fraction of "trials" crossing threshold across seeds — **but the
  threshold itself would have to be calibrated against a reported baseline
  response rate**, making any resulting number a fit, not a prediction. State
  this plainly wherever it is used.

### 4.2 Olfactory T-maze learning

- **Performance Index (PI)**, [Tully & Quinn
  1985](https://ncbi.nlm.nih.gov/pmc/articles/PMC3020398) paradigm:
  flies are trained with one odour (CS+) paired with electric shock and a
  second odour (CS−) unpaired, then given a binary choice in a T-maze.
  ```
  PI = [ (n choosing correctly) − (n choosing incorrectly) ] / (n total)
  ```
  computed from the counts of flies on each arm. **Critically, PI is always
  reported as the mean of two reciprocal groups** — one trained with odour A
  as CS+ and one with odour B as CS+ — specifically to cancel each odour's
  innate (unlearned) attractiveness/aversiveness. A PI computed from only one
  training direction conflates learning with naive odour preference.
- **Scored per group**, not per individual: a T-maze run splits a cohort
  (commonly on the order of 50–100 flies) between two arms and computes one PI
  per cohort; "N" in these papers is the number of independent cohorts, not
  flies.
- **Range**: −1 (perfect avoidance of CS+... i.e. anti-learning) to +1
  (perfect learned avoidance), 0 = no learning. Cohort-to-cohort spread is
  substantial in this literature generally, though this pass did not find a
  precise, citable SD/CV figure — treat any specific spread number as needing
  per-paper verification rather than a field-wide constant.
- **What would be needed to produce this**: an associative plasticity rule at
  the Kenyon-cell → mushroom body output neuron synapse, gated by dopaminergic
  reinforcement — not present in this model (static synaptic weights
  throughout, per `src/params.py` and the lab notebook). **A learning-index
  target cannot currently be produced by this simulator and should not be
  approximated by post-hoc reweighting of a static network** — that would be
  fitting the answer, not measuring it. A weaker, different quantity — CS+/CS−
  discriminability in the unlearned MBON response pattern — could in
  principle be measured today, but it is not the same quantity as PI and must
  not be reported as if it were.

### 4.3 Grooming quantification

- **Method**: automated frame-by-frame classification (k-nearest-neighbours
  or similar) into behaviour classes (grooming / locomotion / feeding /
  rest / sleep) from video, e.g. [Automated analysis of long-term grooming
  behavior in Drosophila](https://elifesciences.org/articles/34497).
- **Headline number**: flies spend **≈13% of waking time grooming**, with
  strong circadian structure (grooming is gated by the clock, via CYCLE/CLOCK).
- **Metrics available**: total time fraction, bout count, bout duration
  distribution; grooming additionally has a documented anterior-to-posterior
  sequencing/suppression hierarchy across body-part-specific programs in the
  broader literature (noted here at lower confidence — not independently
  re-verified in this pass).
- **What would be needed to produce this**: a body and a motor-program /
  descending-neuron competition layer, which this model does not have. The
  more tractable substitute, consistent with the README's stated priority
  that perturbations outrank steady-state numbers: if specific
  grooming-command descending neuron types are identifiable in the connectome,
  measure their *relative* activation and, as a perturbation, whether
  silencing one shifts dominance to the next in the documented hierarchy —
  a causal comparison rather than an absolute "% time grooming" target this
  model cannot produce.

### 4.4 Bang-sensitivity (seizure) assay

- **Stimulus**: mechanical — typically a **10-second vortex** at maximum
  speed.
- **Behavioural sequence scored**: initial paralysis/seizure, leg
  shaking/wing buzzing, a tonic-clonic-like phase, then recovery of posture
  and mobility.
- **Primary metric**: **recovery time** — time to regain normal posture and
  mobility — used as an inverse proxy for seizure severity (longer recovery =
  more severe). Secondary metrics: fraction of flies seizing at all
  (penetrance varies by allele/background), paralysis duration.
- **Genetic instances**: `para^bss1` ("bang-senseless," gain-of-function in
  the voltage-gated sodium channel) has the lowest seizure threshold of the
  bang-sensitive series; `easily shocked (eas)` hits ethanolamine
  kinase/membrane lipid synthesis. Both already referenced in
  `docs/theory-review.md` as the literature match for this project's own
  saturated/195 Hz runaway-excitation finding.
- **What this model already has, uniquely among the four assays**: a
  mechanistic match. The project's own lab notebook already produced the
  textbook seizure signature (100% of Kenyon cells at 195 Hz, "predominance of
  excitatory over inhibitory processes") as an *unintended* operating point,
  not a deliberately built one. The honest transformation here is an analogy,
  not a literal reproduction (there is no motor system to shake legs): apply
  a brief, strong, population-wide depolarizing perturbation (standing in for
  the mechanosensory volley a vortex produces via campaniform sensilla and
  chordotonal organs), define "seizure" operationally the same way the assay
  does behaviourally — population firing rate exceeding some multiple of
  baseline for longer than some duration — and measure **network relaxation
  time back to baseline** as the model-side stand-in for behavioural
  **recovery time**. Flag this explicitly as an untested analogy: whether
  network relaxation time actually correlates with behavioural recovery time
  has not, to this pass's knowledge, been directly co-measured in any
  published study, so treat agreement or disagreement with a real recovery
  time as weak evidence either way, not confirmation.

### 4.5 General note: group variability is the real unit of comparison

Behavioural assays other than single-fly PER are almost always reported as
**group means with cohort-to-cohort spread**, not single-individual
measurements. This project's own `bench/sparseness_variance.py` result — 5
seeds × 4 weights × 2 window lengths, coefficient of variation **36–54%**
across seeds in Kenyon cell recruitment, attributed to genuine state
dependence rather than measurement noise — is the same phenomenon behavioural
cohort variability reflects: a self-sustaining or state-dependent network's
response depends on what it was already doing, and that differs every trial.
**When a target reports a mean and SD/SEM across N flies or cohorts, the
directly comparable simulated quantity is a mean and SD across an equal
number of independent seeds, not a single run** — a point already established
for this project's own numbers and equally applicable to every behavioural
target in this section.

---

## 5. Conditions that make targets mutually inconsistent

If two target papers used different values for any of the following, and the
difference is not accounted for, "target A says 5%, target B says 15%" may be
a real, uncontrolled biological difference rather than a conflict about the
same quantity.

| Condition | Typical range across labs | Known effect on neural activity | Confidence |
|---|---|---|---|
| **Temperature** | Rearing standard 25°C; testing often uncontrolled room temperature (≈20–23°C); thermogenetic tools (dTrpA1 opens ≈29°C, shibire-ts blocks transmission ≈29–32°C) actively hold "control" and "experimental" flies at *different* temperatures from each other and from rearing | Large and systematic. Insect neural/behavioural rates commonly show Q10 ≈ 2 (roughly doubling per 10°C) over the physiological range; some central thermosensory neurons scale firing rate directly with absolute temperature above/below the fly's ≈25°C preferred point. **A perturbation paper using a thermogenetic silencer is running its "silenced" condition at a temperature that itself changes baseline excitability** — a confound layered on top of the intended manipulation. | Medium-high for the general Q10 magnitude (general insect physiology); the specific thermogenetic confound is a logical consequence of the tool's mechanism, not independently quantified here |
| **Fly age** | Most physiology/behaviour studies use 1–10 days post-eclosion, commonly 3–7 days | Mild within this "young adult plateau"; larger effects appear only at senescent ages (weeks), rarely used for these assays | Medium |
| **Sex** | Varies by study; **this project's connectome is MaleCNS** | Most cell types/circuits are shared between sexes, but specific circuits are sexually dimorphic by design (fru/dsx-positive neurons — courtship command neuron P1, and other identified dimorphic types in the connectome). **A target measured in female flies for a dimorphic circuit is not comparable to this model regardless of any other correction**; for non-dimorphic sensory/central circuits (e.g. general olfactory processing, KC sparseness), sex is a secondary concern | Medium — dimorphism is well documented qualitatively; which specific circuits/cell types differ quantitatively is not exhaustively catalogued here |
| **Starvation state** | Many olfactory/appetitive assays deliberately starve flies 18–24 h (wet filter paper, water only) to increase motivation | Large and directly on-pathway for this project: starvation measurably increases olfactory receptor neuron sensitivity via reduced insulin signalling → increased sNPF-mediated presynaptic facilitation, plus octopaminergic modulation of feeding/search state. This changes the gain of the exact circuit (ORN → PN → KC) this project's core targets sit in. | Medium-high — mechanism and direction well documented; exact magnitude in dF/F or Hz terms not extracted here |
| **Time of day / circadian state** | Rarely tightly controlled or reported beyond "entrained 12:12 LD, tested during hours X–Y" | Documented substantial effect specifically on the olfactory pathway: antenna-intrinsic circadian clocks (independent of central clock neurons) drive rhythms in olfactory receptor neuron spike amplitude and odour-evoked behaviour, peaking near mid-night even in constant darkness | Medium |
| **Anaesthesia** | CO₂ (common, fast, cheap) vs. cold/ice (common for brief immobilisation before mounting) vs. volatile general anaesthetics (isoflurane, used transiently in some LFP/imaging preps) | **CO₂ has a long, frequently underestimated tail**: as little as 5 minutes of exposure produces climbing/flight deficits detectable **up to 24 hours later**, with longer exposure producing multi-day deficits; reduces longevity, fecundity and mating success. Cold anaesthesia is generally considered shorter-lived but not neutral. Isoflurane measurably suppresses LFP complexity/informational structure during and after exposure (this project's own §3 LFP sources). **Any assay run "shortly after" anaesthesia, especially CO₂, carries a real, long-lived confound that is routinely not reported as a variable.** | High for the CO₂ duration/magnitude (directly measured); medium for how routinely it goes unreported |
| **Genetic background** | Canton-S, w1118, Oregon-R and others in common use, plus GAL4/UAS driver-line-specific backgrounds; degree of outcrossing/isogenisation varies by lab | Baseline behaviour (locomotor activity, seizure threshold) differs measurably between common wild-type strains; w1118 in particular carries a visible phenotype (white gene affecting biogenic amine transport) with known knock-on effects. Separately — and this bounds *all* targets, not just background-sensitive ones — per `docs/theory-review.md`, connection weights in real connectomes are "surprisingly variable" within and across individual flies, and even Kenyon cell counts vary roughly two-fold between individuals (hemibrain vs. FlyWire). **This is a floor on achievable agreement, not a bias to correct**: no measurement-protocol fix closes the gap between one MaleCNS connectome and the natural range of real nervous systems. | Medium for background-strain effects; the connectome-variability floor is high confidence and already established in this project's own review |

### 5.2 Project-specific flags

- **This model's constants were not all measured under the same
  conditions.** `src/params.py` combines resting/threshold/membrane time
  constant from [Kakaria & de Bivort 2017](https://doi.org/10.3389/fnbeh.2017.00008),
  synaptic time constant from [Jürgensen et
  al.](https://doi.org/10.1088/2634-4386/ac3ba6), and refractory period from
  [Lazar et al., eLife](https://doi.org/10.7554/eLife.62362) — three
  different labs, three different preparations, and (per §2.2) probably three
  different uncontrolled temperatures. This is exactly the "targets mutually
  inconsistent if ignored" risk the README warns about, already latent inside
  the model's own parameter set, not only in the target list. Worth a
  one-time check of each source's stated recording temperature before relying
  on precise timing comparisons.
- **Sex-match the connectome before trusting a dimorphic-circuit target.**
  Since the simulator is built on MaleCNS, any target from a study that used
  female or mixed-sex flies for a circuit with known or suspected sexual
  dimorphism should be flagged in that target's Conditions field, independent
  of any other correction in this document.
- **Starvation state most directly threatens the olfactory targets this
  project already relies on** (Kenyon cell sparseness, projection neuron
  gain) — check whether the source paper starved its flies before comparing
  absolute response magnitudes, not only relative sparseness fractions.

### 5.3 Conditions checklist (paste into a target's Conditions field)

```
- Prep: [ex vivo explant | in vivo head-fixed | intact behaving]
- Saline (if electrophysiology): [network-preserving / bicarbonate / no blockers
  | intrinsic-isolating / HEPES / blockers: list them]
- Temperature: [rearing __°C, testing __°C, or "not stated"]
- Fly age: [days post-eclosion, or "not stated"]
- Sex: [male | female | mixed] — dimorphic circuit? [y/n]
- Starvation: [ad lib | starved __h on water/agar]
- Time of day tested: [ZT/CT range, or "not stated"]
- Anaesthesia: [none | CO2, recovery time allowed __h | cold | isoflurane]
- Genetic background: [strain / driver line / outcrossed?]
```

---

## 6. Summary: what each transformation needs

| Domain | Best-supported piece | Weakest / missing piece |
|---|---|---|
| Calcium imaging (§1) | Kinetics convolution → nonlinearity → noise → downsample → threshold pipeline; jGCaMP8 constants; one direct fly ORN calibration | No fly calibration for sparse central-neuron regimes (exactly where the KC sparseness target lives); GCaMP3/5/7-family kinetic constants need primary-source verification |
| Patch-clamp / sharp electrode (§2) | Preparation and pharmacology matching; quantified Kenyon-cell rundown, Rin, Cm, resting Vm | No general correction for electrode leak on Rin; dissection-injury magnitude not quantified anywhere found |
| Electrode array / LFP / subsampling (§3) | MR estimator equations and numeric bias table (analytically proved, directly sourced); direct match to this project's own discarded naive measurement | Cannot synthesize true LFP from point neurons; avalanche exponent bias has no analytic correction, only degrade-and-match |
| Behavioural assays (§4) | Exact operational scoring for PER, T-maze PI (with reciprocal-averaging requirement), bang-sensitivity recovery time | PER needs unmodelled gustatory/motor circuitry; T-maze PI needs unmodelled plasticity (cannot be approximated by reweighting); grooming needs a body; bang-sensitivity transformation is an explicit, unvalidated analogy |
| Conditions (§5) | Direction and rough size of the largest effects (temperature, starvation, anaesthesia duration, sex-dimorphism, connectome individual variability) | Precise quantitative correction factors for most; connectome variability is a floor to report, not an error to remove |

The common thread: wherever a numeric constant is missing, the honest move
demonstrated throughout this file is to build the forward model with the
constant left explicit and flagged, rather than pick a plausible-looking
number silently. A target compared through a flagged, approximate
transformation is still more informative than one compared with no
transformation at all — but only if the flag survives into whatever consumes
the comparison.
