# Prior validation: what other connectome-based fly models were tested against

Scope: every connectome-based *Drosophila* brain/body model I could find with a
public validation claim, what each one actually measured (as opposed to what
press coverage says it measured), and where each one failed, hedged, or simply
didn't check. Rationale per the project brief: another group's validation set
is cheaper to reuse than reconstructing one from primary literature, and a
target several independent groups failed to hit is more diagnostic than one
everybody hits.

**Method note.** Findings below come from a mix of primary sources read in full
(the Shiu et al. Nature paper via PMC, the FlyVis Nature paper via PMC, the
Digital Sphinx preprint, the FlyGM arXiv preprint, the NeuroMechFly v2 Nature
Methods paper, and the Loihi 2 arXiv preprint — all read directly, not
summarized by an intermediary) and secondary sources (news coverage, blog
posts, a critique blog) read via automated fetch, which occasionally
paraphrases loosely. Where a number rests only on secondary paraphrase, that is
flagged in the Confidence field. Two access attempts (the "State of Brain
Emulation Report 2025", arXiv:2510.15745, and a live biorxiv full-text fetch of
Shiu et al.'s preprint) failed for tooling reasons (file too large / rate
limited) and are not used as sources below — I did not fabricate content from
them.

**Overall pattern, stated up front:** none of the seven systems in scope
validate what a reader would assume from press coverage. Two (Loihi 2, FlyGM)
validate literally nothing biological — one checks hardware against its own
software twin, the other checks an RL controller against RL baselines. One
(Eon Systems) reports a headline accuracy number that traces back to a
*different, older, disembodied* model, not to the system being announced. Two
(Shiu et al., FlyVis) did real, quantitative comparisons against experimental
recordings, but over a minority of the system's components, with explicit,
named failure modes. One (NeuroMechFly v2) is honest that most of its
"validation" is internal self-consistency or qualitative cross-species
gesture, with the real experimental comparison confined to leg kinematics
during straight walking. One (the Digital Sphinx) isn't a model to validate at
all — it's a demonstration that the entire genre's favorite success criterion
(does it look like realistic behavior?) is measuring nothing.

---

## Summary table

| Model | What it actually validated against | Headline claim | Sharpest caveat |
|---|---|---|---|
| Shiu et al. 2024 (LIF whole-brain) | Optogenetic activation/silencing behavior for a subset of feeding/grooming circuits | 91% of 164 tested predictions confirmed (84% excluding an inflated screen) | Explicitly fails on inhibitory/neuromodulatory-driven circuits |
| FlyVis 2024 (Lappalainen/Turaga) | Prior electrophysiology/imaging studies, ~32 of ~64 optic-lobe cell types | Ensemble matches contrast- and direction-selectivity for all characterized types | ~33 of ~64 cell types have no experimental data to check against at all; Tm4 polarity is wrong; correct T4 mechanism was one of three degenerate solutions |
| FlyGM (arXiv:2602.17997) | Other RL controllers (random graph, rewired graph, MLP, SNN) on task performance only | Connectome-structured controller has lower angle error, faster convergence | No biological validation attempted or claimed; only a qualitative nod to two imaging papers |
| Eon Systems (Mar 2026) | Nothing new for the embodied phase; the "~95%" figure is recycled from Shiu et al. 2024 | "~95% accuracy predicting motor behavior" | Own write-up admits hand-picked brain-body interfaces and admits internal dynamics were never checked against biology |
| NeuroMechFly v2 (2024) | Own video-derived leg kinematics (real fly); everything past that is internal self-consistency or cross-species gesture | Framework reproduces real walking kinematics; several closed-loop behaviors demonstrated | Adhesion, path integration, and head stabilization are validated against the simulator itself, not against matched real-fly data |
| Loihi 2 (arXiv:2508.16792) | Its own software reference simulation (Brian2/STACS) of an already-simplified model | 3x-350x speedup, spike rates track software parity line | Zero contact with biological data anywhere in the paper |
| The Digital Sphinx (2026) | N/A — a negative-control demonstration, not a model to validate | A worm connectome can be trained to walk a fly body indistinguishably from a real fly | Proves behavioral realism is uninformative about biological correctness of the network driving it |

---

## 1. Shiu et al. 2024, Nature — LIF whole-brain model

**What they claim and what they actually measured.** The model (~127,000
neurons, ~50 million synapses, from the FlyWire connectome, signed by
predicted neurotransmitter identity) was tested by simulating optogenetic
activation/silencing of specific neuron types and comparing the model's
predicted downstream effect (spiking, or a specific behavior like proboscis/
rostrum extension) against real optogenetic and behavioral experiments run by
the same team. Per the paper's own reporting: **across 164 predictions tested
empirically, 91% were consistent with the empirical result; excluding the
optogenetic split-GAL4 screen (in which most tested cell types are true
negatives that don't respond, inflating the raw percentage), the stated
accuracy is 84%.** Two sub-results feeding into that aggregate: at 50 Hz
stimulation, 10 of 11 cell types predicted to activate motor neuron MN9
actually elicited rostrum extension, and of 95 cell types predicted *not* to
activate it, only 4 showed any rostrum extension (the paper describes this as
"over 90% accuracy" at that frequency). A separate water-sensing test targeted
11 neurons (6 predicted to have a silencing phenotype, 5 predicted not to);
5/6 and 4/5 respectively were confirmed.

**Acknowledged limitations (quoted from the paper, via PMC full text).** The
model "does not account for gap junctions, non-spiking neurons, internal
state or long-range neuropeptides, and assumes that the basal firing of each
neuron is zero." It "ignore[s] neural morphology and receptor dynamics" and
"treat[s] each neuron identically as a spiking neuron." Critically, the
authors report an explicit **failure mode**: the model "failed to predict
behavioural results in the SEZ split-GAL4 screen when the neurons tested were
predicted to be inhibitory (that is, Tentacular or Phantom) or
neuromodulatory (Usnea)," concluding that "circuits in which there is
extensive basal inhibition, not captured by the model because of the zero
basal firing rate, may be poorly simulated." They also note the model's
accuracy is bounded above by "the underlying synapse and neurotransmitter
prediction accuracy" it inherits from FlyWire's automated connectomics
pipeline — i.e. even a perfect simulator inherits the connectome's own error
bars.

**Critique or failed replication.** I found no independent paper that
attempted to replicate Shiu et al.'s specific predictions and failed. The
closest things are (a) the general "black box" critique aimed at how *Eon
Systems* later reused this model embodied (see §4 — that critique targets the
embodiment, not the original 91%/84% figures), and (b) the fact that Turaga
(FlyVis's own senior author) is on record expressing skepticism about whether
a downstream reuse of this model outperforms a random network — again aimed
at Eon's reuse, not at Shiu et al.'s own reported numbers. Treat the 91%/84%
figures as not independently contested, but also not independently confirmed.

### T-PRIOR-001 Shiu et al. aggregate prediction accuracy
- **Quantity** — fraction of model-generated circuit predictions (evoked
  spiking / evoked behavior from simulated neuron activation or silencing)
  confirmed by real optogenetic activation/silencing experiments
- **Value** — 91% of 164 predictions (all predictions tested); 84% when the
  SEZ split-GAL4 optogenetic screen is excluded (that screen alone: 10/11
  positive predictions and 91/95 negative predictions confirmed at 50 Hz
  stimulation); water-sensing sub-test: 5/6 and 4/5
- **Type** — perturbation (this is an aggregate over many individual
  activation/silencing perturbations — the individual predictions themselves
  are being extracted separately elsewhere in this project; this entry is the
  aggregate statistic only, not a substitute for that extraction)
- **Method** — computational: simulate activation or silencing of a
  named neuron type in the LIF model, read out downstream spiking / a scored
  behavior (e.g. rostrum extension). Compared against real optogenetic
  activation/silencing of the same genetically targeted (split-GAL4) neuron
  type, scored the same way (behavior presence/absence, or electrophysiology)
- **Observation model** — a fair comparison needs the same "hit" threshold
  the authors used (e.g. any non-zero rostrum extension counts as a positive)
  and the same denominator convention (all tested cell types, vs. excluding
  the screen's structurally-inflated negatives)
- **Conditions** — adult *Drosophila*, split-GAL4 driver lines targeting
  specific SEZ (subesophageal zone) neuron types; sex/age not confirmed here
- **Source** — Shiu, P. K. et al. "A Drosophila computational brain model
  reveals sensorimotor processing." *Nature* 634, 210–219 (2024).
  https://www.nature.com/articles/s41586-024-07763-9 ; PMC11446845
- **Confidence** — high for the 91%/84%/164 numbers (read directly from
  primary-source full text); medium for the sub-counts (10/11, 91/95, 5/6,
  4/5), which came through an automated full-text fetch rather than direct
  visual reading of the PDF

### T-PRIOR-002 Shiu et al. — model fails on inhibitory/neuromodulatory circuits
- **Quantity** — whether the model correctly predicts the behavioral effect
  of activating/silencing neurons whose function is inhibitory or
  neuromodulatory, within the SEZ split-GAL4 screen
- **Value** — model predictions failed for neurons predicted to be inhibitory
  (named: Tentacular, Phantom) or neuromodulatory (named: Usnea); exact N and
  effect size not given in the extraction available to me — treat as a
  qualitative, named failure rather than a quantified one
- **Type** — perturbation (negative result)
- **Method** — same optogenetic screen as T-PRIOR-001; failure specifically
  localized to neuron classes whose function depends on non-zero basal firing
  or neuromodulation, which the LIF model structurally cannot represent
  (model assumes zero basal firing rate for every neuron)
- **Observation model** — any extractor reproducing this target must itself
  assume zero basal firing rate to be a fair comparison — i.e. this target is
  specifically diagnostic of *that* modeling choice, not of the connectome
  data itself
- **Conditions** — same SEZ split-GAL4 screen as above
- **Source** — same as T-PRIOR-001, Discussion/Limitations section
- **Confidence** — medium — the named failure is stated explicitly in the
  paper, but I could not confirm the exact number of neurons involved or
  effect sizes from the extraction tools available

---

## 2. FlyVis, Lappalainen & Turaga 2024, Nature

**How they judged success.** FlyVis is a connectome-constrained deep
mechanistic network (an ensemble of ANNs, each neuron/synapse corresponding to
a real optic-lobe neuron/synapse, task-optimized for motion detection) covering
64 cell types across ~721 columns of the fly's motion-vision pathways.
Predictions were checked against previously published electrophysiology and
calcium-imaging studies — cited secondary extractions disagree on the exact
count (24 in one pass over the abstract, 26 in a pass over the full text);
treat it as "roughly two dozen" prior studies, not a precise number.

**What matched.** For the ~32 optic-lobe cell types with previously
established contrast selectivity (ON vs. OFF preference), the trained model
*ensemble*'s median prediction matched all 32; a single task-optimal network
matched 30/32 (93.75%). For direction selectivity, the model correctly
identified 9 cell types as *not* motion-tuned (Mi1, Tm3, Mi4, Mi9, Tm1, Tm2,
Tm4, Tm9, CT1) and 12 cell types as direction-selective (T4a–d, T5a–d, TmY3,
TmY4, TmY5a, TmY18) consistent with known biology — including reproducing the
textbook finding that T4 is ON-motion-selective and T5 is OFF-motion-selective.
Across the model ensemble, networks that achieved better task performance
(motion-estimation loss) also showed better agreement with real
direction-selectivity indices (r = 0.60, P = 2.6×10⁻⁶) — a genuine, non-circular
finding, since nothing forced task-optimization to also produce biological
accuracy.

**What did not match, in the model's own words.** "Tm4 is incorrectly
predicted to depolarize" to OFF-flashes — a named, direct contradiction of
recorded data. The model's own ON/OFF metric "cannot capture" a subset of
real cells (R1–R8, L1, L2) that are "unrectified" — i.e. the validation
framework itself has no way to score a whole class of real neurons, not just
a modeling failure. The architecture explicitly omits gap junctions/electrical
synapses, nonlinear chemical synapses, neuromodulation, and superposition
optics, and approximates neurotransmitter release as threshold-linear rather
than the real nonlinear voltage-gated release. Perhaps the single most
important limitation for a target-selection project: **roughly 33 of the ~64
modeled cell types have no prior experimental characterization at all**, so
the "high accuracy" claims necessarily apply only to the roughly half of the
model that could be checked — the paper is silent, not confirmed-successful,
on the rest.

**A methodological finding worth flagging separately (see Lessons):** for T4
direction selectivity, three mechanistically distinct solutions emerged across
the trained ensemble, and only one matched real biology — meaning connectivity
plus task-optimization alone did not uniquely determine the correct circuit
mechanism; picking the biologically correct one required the experimental data
as a tie-breaker, not the model alone.

### T-PRIOR-003 FlyVis contrast-selectivity (ON/OFF) match rate
- **Quantity** — fraction of optic-lobe cell types for which predicted
  contrast preference (ON vs. OFF) matches previously recorded contrast
  preference
- **Value** — 32/32 (100%) by ensemble median prediction; 30/32 (93.75%) for
  a single task-optimal network
- **Type** — steady-state
- **Method** — simulated response to circular flash stimuli (ON/OFF flash
  response index, FRI), classified by sign; compared to prior
  electrophysiology/calcium-imaging recordings of the same cell types under
  flash stimuli
- **Observation model** — must use the same Flash Response Index definition
  and the same "characterized" cell-type subset (32 of ~64) — do not compare
  against the full cell-type roster, most of which lacks a recorded ground
  truth
- **Conditions** — *Drosophila* optic lobe, in-vivo electrophysiology/imaging
  in the source studies (specific prep conditions not extracted here)
- **Source** — Lappalainen, J. K. et al. "Connectome-constrained networks
  predict neural activity across the fly visual system." *Nature* 634,
  1132–1140 (2024). https://www.nature.com/articles/s41586-024-07939-3 ;
  PMC11525180
- **Confidence** — high for the 32/32 and 30/32 figures (consistent across
  extraction passes); medium for exactly which 32 cell types, not individually
  re-verified here

### T-PRIOR-004 FlyVis direction-selectivity classification
- **Quantity** — which optic-lobe cell types are correctly classified as
  motion-direction-tuned vs. untuned
- **Value** — 9 types correctly classified as untuned (Mi1, Tm3, Mi4, Mi9,
  Tm1, Tm2, Tm4, Tm9, CT1); 12 types correctly classified as direction-selective
  (T4a–d, T5a–d, TmY3, TmY4, TmY5a, TmY18); correlation between task
  performance and biological match r = 0.60 (P = 2.6×10⁻⁶)
- **Type** — steady-state (categorical classification), with the r/P value as
  a secondary dynamic-response-adjacent statistic
- **Method** — Direction Selectivity Index (DSI) from simulated responses to
  moving-edge stimuli, thresholded at the 99th percentile of DSI values from
  known non-tuned cell types; compared against the same real recordings as
  T-PRIOR-003
- **Observation model** — extractor must reproduce the DSI computation and
  the percentile-based threshold, not an arbitrary cutoff
- **Conditions** — as T-PRIOR-003
- **Source** — same as T-PRIOR-003, main text and Extended Data Fig. 2e
- **Confidence** — high for the classification list; medium for the r/P value
  (single extraction pass, not independently re-derived)

### T-PRIOR-005 FlyVis named failure: Tm4 polarity
- **Quantity** — predicted vs. real response polarity (depolarize/
  hyperpolarize) of cell type Tm4 to an OFF-contrast flash
- **Value** — model (task-optimal ensemble) incorrectly predicts Tm4
  depolarizes to OFF-flashes; real recordings show this is wrong (i.e. real
  Tm4 does not follow the predicted sign)
- **Type** — steady-state (negative result)
- **Method** — same Flash Response Index approach as T-PRIOR-003, for the
  single cell type Tm4
- **Observation model** — same as T-PRIOR-003
- **Conditions** — as T-PRIOR-003
- **Source** — same as T-PRIOR-003, main text
- **Confidence** — medium — the direction of the error is stated in the
  paper; I was not able to independently confirm the exact real polarity value
  (only that the model's prediction is called out as incorrect)

---

## 3. FlyGM, arXiv:2602.17997 — "Whole-Brain Connectomic Graph Model Enables Whole-Body Locomotion Control in Fruit Fly"

Read in full from the arXiv PDF (Jin, Zhu, Zhang, Sui; Tsinghua University).
This section separates the two claim types the brief asked me to keep apart.

**(A) What was actually validated — RL task performance only.** FlyGM
instantiates the FlyWire connectome directly as a recurrent graph neural
network (nodes = neurons, partitioned into afferent/intrinsic/efferent by
FlyWire's own flow-type classification; edges = signed synapse counts by
neurotransmitter), trained in two stages (imitation learning from an expert
MLP policy, then PPO fine-tuning) to drive a MuJoCo biomechanical fly body
("flybody", Vaxenburg et al. 2025 Nature) through gait initiation, straight
walking, turning, and flight. Its comparisons are **all against other
artificial controllers**, not against biological data:

| Model | Angle error, deg (v=2,ψ=0) | (v=3,ψ=0) | (v=3,ψ=4) | (v=3,ψ=7, sharp turn) |
|---|---|---|---|---|
| FlyGM (real connectome) | 4.96±0.09 | 5.57±0.06 | 6.36±0.33 | **8.29±0.21** |
| Degree-preserving rewired connectome | 7.84±0.08 | 7.77±0.08 | 9.72±0.12 | 13.55±0.69 |
| Erdős–Rényi random graph (same node/edge count) | 12.11±0.23 | 11.33±0.27 | 17.45±0.26 | 125.36±8.96 (degenerates) |
| MLP (larger parameter count) | 6.76±0.13 | 7.18±0.05 | 8.85±0.24 | 13.90±0.45 |

A biologically-plausible spiking-neuron (SNN) baseline that is *not*
connectome-structured "fails to learn a usable gait" at all (Appendix F) — the
authors' own reading is that single-neuron biological plausibility without the
real wiring diagram is not sufficient, and (from an ablation in Appendix G)
that an *unweighted* version of FlyGM (topology only, discarding synapse-count
weights and neurotransmitter sign) still beats every non-connectome baseline —
i.e. the advantage they measure comes from *which neuron connects to which*,
not from the finer biological detail layered on top.

**(B) Biological validation — essentially absent.** The only nod toward
biology is qualitative: the authors observe that functional segregation
(distinct activation signatures for afferent/intrinsic/efferent populations
across behavioral phases) emerges from training, and state this is
"consistent with" two real imaging papers (Brezovec et al. 2024 *Current
Biology*; Schaffer et al. 2023 *Nature Communications*) — with a random-graph
control run through the same analysis showing no such structure, which is a
fair internal control for "is this an artifact of our analysis pipeline,"
but **no quantitative comparison to either cited paper's actual data is
given**. There is no comparison of simulated joint kinematics, muscle
activation, or spiking statistics to real fly recordings anywhere in the
paper. The stated limitations section itself only mentions wanting more
complete connectome data and more compute — it does not list "we have not
validated this against real neural or behavioral data" as a limitation, which
a skeptical reader should notice as an omission, not an oversight to excuse.

**Conclusion for target-building purposes: FlyGM contributes no reusable
T-PRIOR entry.** Its numbers are RL-controller benchmarks against other RL
controllers, which is a different claim from a match to biological data, per
the brief's own instruction to keep these separate. The one thing worth
carrying into the Lessons section is the ablation finding itself (topology
alone drives the RL benefit) as a methodological data point, not a target.

---

## 4. Eon Systems embodied fly emulation (March 2026)

**What the "~95% accuracy" figure actually is.** Multiple independent
secondary sources, read directly, attribute this figure explicitly to the
**2024 Shiu et al. connectome model, before embodiment** — not to the
March 2026 embodied demonstration. From a German-language startup-news
write-up: "showed motor behavior with 95% accuracy, **but without a body**."
From another summary: "achieving 95% accuracy in motor predictions according
to prior work led by Philip Shiu" (Eon's senior scientist — the same person
as the first author of the original 2024 Nature paper). This number does not
exactly match Shiu et al.'s own reported headline figures (91% overall, 84%
excluding the inflated optogenetic screen — see T-PRIOR-001); it most likely
derives from a specific favorable sub-statistic in that paper (e.g. the ~96%
true-negative rate on the 95 non-activator predictions, or the paper's own
"over 90% accuracy" phrase, rounded upward in press retelling) rather than
being a distinct new measurement. **Practical implication: the number
currently circulating in press coverage of Eon's embodied fly is not a
measurement of the embodied fly at all** — it is a recycled, likely
imprecisely-transcribed statistic from a different (disembodied) paper, two
years earlier, describing a different claim (single-circuit optogenetic
prediction, not general "motor behavior").

**What Eon's own technical write-up admits (read directly, eon.systems/
updates/embodied-brain-emulation).** No quantitative accuracy figure is
given anywhere for the embodied model itself — "no comparison metrics,
benchmarks, or datasets are cited for validating motor output fidelity." The
write-up explicitly hedges on exactly the two points the brief anticipated:

- Hand-chosen interfaces: "Many of the mappings between brain and body were
  chosen by hand rather [than] derived from the connectome"; on
  descending-neuron-to-behavior translation specifically, "these mappings can
  be somewhat arbitrarily chosen by hand (as is our case)."
- Unvalidated internal signatures: "We have not yet validated the model's
  internal dynamics against known biological signatures, such as the
  head-direction ring attractor or central pattern generators." The brain
  model also lacks "dendritic nonlinearities, biophysical channel diversity"
  and omits "internal state, plasticity, learning, hormonal changes."
- Narrow coverage: the descending-neuron interface covers "a small subset of
  sensory inputs and model[s] only a handful of behaviors."

The body is NeuroMechFly v2 (87 independent joints) in MuJoCo (see §5).
Behaviors demonstrated — grooming, feeding, foraging, looming-stimulus
responses — are described only qualitatively; no quantitative kinematic or
behavioral comparison to real flies is reported.

**Published critique.** The Carboncopies Foundation's response ("No, a Fruit
Fly Has Not Been Uploaded") makes a structural argument, not just a numbers
complaint: "Putting the Shiu et al. brain model into a closed-loop behavior
setup that treats the brain model as a black box is not enough to evaluate the
degree of emulation," because a pre-built body model's "internal stabilizers
and pre-set gait cycles" can turn even noisy or wrong brain output into a
plausible-looking step (their term: the "puppet effect") — real validation
requires inspecting whether internal microcircuits (e.g. central pattern
generators) actually match known biology, not just watching the external
behavior. It separately criticizes announcing the result outside peer review.
Independently, coverage of the Digital Sphinx paper's reception (§7) quotes
Turaga expressing doubt that Eon's embodied model outperforms a random
network absent published specifics, and quotes Eon's own Philip Shiu partially
conceding the point: "I think it's fair to say that this is not a full blown
copy of a fly."

**Conclusion for target-building purposes: no new reusable target from Eon.**
The one number in circulation traces back to Shiu et al. 2024 (T-PRIOR-001);
treat any target sourced to "Eon Systems, 2026" with the presumption that it
is not a new measurement until proven otherwise.

---

## 5. NeuroMechFly v2 / FlyGym, Nature Methods 2024

Read in full from the EPFL-hosted postprint PDF (Wang-Chen, Stimpfling, Lam,
Özdil, Genoud, Hurtak, Ramdya).

**What the body model and kinematics were validated against.** The one place
this paper compares directly to real, matched-condition data with a stated
method is **leg kinematics during straight walking**: the team recorded real
wildtype female *Drosophila melanogaster* (25 °C, 50% relative humidity,
12h:12h light:dark, 4–5 days post-eclosion) walking through a 12×4×2 mm
corridor at 360 Hz from three camera views, manually annotated five leg
keypoints per leg (thorax-coxa, coxa-trochanter, femur-tibia, tibia-tarsus,
claw) plus antennae/neck/thorax/abdomen, and applied inverse kinematics.
From 16 candidate step cycles (8 swing-to-swing, 8 stance-to-stance across
front/middle/hind legs) 7 were discarded for insufficient "closure"
(start/end joint-angle mismatch above 0.17/0.12/0.17 rad for
front/middle/hind legs respectively); the remaining 9 steps were stretched to
a common 0.135 s duration and mirrored to produce 30 combined stepping
patterns used to drive the model.

**Everything else in the paper is weaker than it first appears:**

- **Leg adhesion / climbing:** critical climbing slope was measured as a
  function of adhesion force *within the simulation itself* (Fig. 2c) — there
  is no matched real-fly inverted-walking dataset to compare against yet; the
  paper says so directly: "we expect experimental recordings of real inverted
  walking kinematics to enable locomotion at even higher inclinations" (i.e.
  that comparison doesn't exist yet).
- **Path integration:** heading and forward-displacement predictions from
  simulated leg-proprioception achieve R²=0.96 and R²=0.98 — but this is the
  model's internal linear-readout prediction checked against the *simulator's
  own ground-truth trajectory*, not against a real fly path-integration
  experiment. The paper itself calls the biological source of these cues
  "unknown."
- **Head stabilization:** described only as "reminiscent of data from
  blowflies" — a qualitative, cross-species, uncited-in-the-visible-text
  gesture, not a same-species quantitative match.
- **Odor plume navigation:** the simulated fly reached within 15 mm of an
  odor source in 9 of 100 trials (9%), which the authors describe as "similar
  [to the] success rate compared to what was seen in real flies in a larger
  arena over a longer time period" — note the authors' own hedge: different
  arena size, different trial duration. This is a loose comparison, not a
  matched one.
- **Vision/olfaction:** the compound-eye model is anatomically grounded
  (~700–750 ommatidia, hexagonal lattice, 270° combined FOV, ~17° binocular
  overlap, 7:3 yellow:pale ommatidia ratio) but not functionally validated
  against electrophysiology; olfaction is an abstract multi-dimensional
  sensor with no specific ORN data behind it.
- **Terrain-controller benchmarking** (CPG vs. rule-based vs. hybrid
  controller speed over rugged terrain, N=20 trials, Mann-Whitney U,
  p<0.01/p<0.001) is a real statistical comparison, but controllers are only
  compared **against each other**, not against real fly locomotion speed data
  over matched terrain.
- The fly-following task plugs in the actual FlyVis connectome-constrained
  visual network (obtained pre-publication from the Turaga lab) and evaluates
  success qualitatively over 11 trials with/without head stabilization — not
  against real fly-following kinematics.

### T-PRIOR-006 Real fly straight-walking leg-joint kinematics
- **Quantity** — 3D joint-angle trajectories (thorax-coxa, coxa-trochanter,
  femur-tibia, tibia-tarsus) for each leg during one straight-walking step
  cycle
- **Value** — 9 retained step trajectories (of 16 candidates), each
  normalized to 0.135 s duration; not a single scalar — this is a
  trajectory-shaped target (see source for full traces/supplementary data)
- **Type** — dynamic response
- **Method** — 360 Hz, 3-camera videography of untethered straight walking in
  a 12×4×2 mm corridor; 5 keypoints/leg manually annotated; inverse
  kinematics onto a scaled skeleton template; steps segmented and screened
  for closure (discarded if mean start/end joint-angle mismatch exceeds
  0.17 rad front/hind or 0.12 rad middle legs)
- **Observation model** — an extractor must replicate the same closure
  screening and normalization-to-median-step-length (0.135 s) before
  comparing, or it is comparing against a differently-filtered dataset
- **Conditions** — wildtype (PR) female adult *Drosophila melanogaster*,
  25 °C, 50% relative humidity, 12h:12h light:dark, 4–5 days post-eclosion,
  untethered, straight walking only
- **Source** — Wang-Chen, S. et al. "NeuroMechFly v2: simulating embodied
  sensorimotor control in adult Drosophila." *Nature Methods* 21, 2353–2362
  (2024). https://www.nature.com/articles/s41592-024-02497-y
- **Confidence** — high — read directly from the primary source's Methods
  section ("Stepping pattern")

### T-PRIOR-007 Real-fly odor-plume-seeking success rate (weak, flagged)
- **Quantity** — fraction of trials in which a fly (real or simulated)
  reaches within a fixed distance of an odor source in a plume-seeking task
- **Value** — simulated fly: 9/100 trials (9%) reaching within 15 mm;
  compared, per the authors' own hedge, to "similar" real-fly success rates
  reported in the plume-navigation study they implemented the algorithm from
  (specific real-fly percentage not given in the text available to me)
- **Type** — perturbation/behavioral
- **Method** — Poisson-process-governed stop/walk/turn plume-navigation
  algorithm (from a previously published *Drosophila* plume study), run in
  simulation over a modeled complex odor plume
- **Observation model** — arena size and trial duration are NOT matched
  between the simulated and real comparisons per the authors' own text — any
  reuse of this as a target must either find the original real-fly study's
  exact arena/duration or treat this comparison as only order-of-magnitude
  informative
- **Conditions** — simulated arena; real-fly comparison condition described
  by the source paper only as "a larger arena over a longer time period"
- **Source** — same as T-PRIOR-006, Results ("Using more bio-realistic
  algorithms for sensorimotor control"); the underlying real-fly plume study
  is cited in that paper as ref. 51, which I did not independently retrieve
- **Confidence** — low — arena/duration mismatch is explicitly flagged by the
  source authors themselves, and I have not verified the original real-fly
  percentage independently

### T-PRIOR-008 Real fly treadmill kinematics used to train connectome-body interfaces
- **Quantity** — 3D joint kinematic trajectories of real walking flies,
  extracted via markerless pose estimation, used as an imitation-learning
  target for at least one other model in this survey (the Digital Sphinx's
  motor decoder, §7)
- **Value** — trajectory-shaped target; not a single scalar (see source)
- **Type** — dynamic response
- **Method** — miniature linear and split-belt treadmill recordings of
  walking *Drosophila*, 3D pose extracted with Anipose (a markerless
  pose-estimation toolkit)
- **Observation model** — whatever imitation-learning or trajectory-matching
  procedure is used to consume this data should be reported alongside it, since
  at least one model (Digital Sphinx) demonstrated that a sufficiently
  expressive decoder can imitate this kind of trajectory data regardless of
  whether the upstream network is biologically meaningful — the target is only
  informative about the trajectories themselves, not about whatever network
  was fit to reproduce them
- **Conditions** — walking *Drosophila* on miniature linear/split-belt
  treadmills; further prep details not extracted here
- **Source** — Pratt, B. G., Lee, S.-Y. J., Chou, G. M. & Tuthill, J. C.
  "Miniature linear and split-belt treadmills reveal mechanisms of adaptive
  motor control in walking Drosophila." *Current Biology* 34, 4368–4381.e5
  (2024); pose extraction via Karashchuk, P. et al. "Anipose: a toolkit for
  robust markerless 3D pose estimation." *Cell Reports* (2021). Both cited
  from Brunton, Abe, Hu & Tuthill, "The digital sphinx" (2026), which is
  where I identified this as a convergently-reused dataset (see §7)
  — I did not independently fetch the Pratt et al. or Karashchuk et al.
  papers themselves
- **Confidence** — medium — the dataset's existence and use are confirmed
  from a primary source I read in full (Digital Sphinx), but I have not
  directly read Pratt et al. 2024 itself, so exact recording parameters are
  not verified here

---

## 6. Loihi 2 neuromorphic implementation, arXiv:2508.16792

Read in full from the arXiv PDF (Wang, Theilman, Rothganger, Severa, Vineyard,
Aimone; Sandia National Laboratories).

**Direct answer to "did they validate dynamics or only performance": both, but
the dynamics validation has zero contact with biology.** The paper reimplements
a *simplified* version of the Shiu et al. model (point-neuron LIF, synapses
condensed from ~50 million to ~15 million by merging same-source/target
connections) and maps it onto 12 Intel Loihi 2 chips. Its dynamics check is:
replicate a small "sugar neuron" sub-experiment from the original paper
(~20 Poisson-driven sensory input neurons at 150 Hz, activity confined to a
few hundred downstream neurons) on Loihi 2 hardware, and compare **average
per-neuron spike rates against the same simplified model run in software**
(Brian2, and an intermediate simulator called STACS) — a hardware-vs-software
self-consistency check of their own reimplementation, not a check against any
biological recording, and not even a check against the original full
(50-million-synapse) model. The parity plot (10 trials) is described as
"largely" matching, with named, explained sources of small systematic
deviation: conductance-only spike integration introduces a timing/aliasing
lag for a subset of neurons, and capping synaptic weights to a 9-bit range
(±255/256) — affecting only 0.007% of all weights (454 negative + 637
positive) — measurably skews rates for the highest-weight neurons. These
deviations were tracked down and explained, not eliminated.

The paper's actual claimed result is a **performance** metric: 3x–350x speedup
over the Brian2 CPU reference depending on background spike rate, with the
speed advantage increasing as network activity gets sparser; Loihi 2 beats
real-time simulation at background rates the CPU/GPU references never do in
this comparison. The authors themselves frame this as a systems/engineering
feasibility demonstration ("Although not directly related to network
validation and performance, we also wanted to discuss..." — their own words
about a side-topic in §4.3 underline that validation and performance are the
paper's two explicit axes, and neither axis touches biological data).

**Conclusion for target-building purposes: no reusable biological target.**
This paper is useful only as a methodological data point (see Lessons) about
what "validated" can mean in this literature — here, it means "our hardware
port reproduces our own software model's numbers," nothing more.

---

## 7. The Digital Sphinx, Brunton & Tuthill 2026

Read in full (bioRxiv preprint PDF, 6 pages; also posted as an eLife reviewed
preprint rated "valuable" / "solid evidence"). This is not a model to be
validated — it is a purpose-built negative control aimed at the entire genre
in scope here, and its criteria are directly usable by this project.

**The experiment.** The authors built a deliberately-absurd chimera: the
complete *C. elegans* hermaphrodite connectome (302 neurons: 82 sensory, 80
inter-, 140 motor), modeled as a graded (non-spiking) activation network with
synaptic weights signed by neurotransmitter identity — wired to a MuJoCo
biomechanical *Drosophila* body (42 leg actuators, 148 proprioceptive
sensors). The interface was maximally naive: body-proprioception was mapped to
the worm's 82 sensory neurons by a fixed **random projection** with no
sensory-type discrimination and no trained parameters; a DRL-trained
variational encoder-decoder then mapped the worm's motor-neuron activity to
leg torque commands, trained by imitation learning (PPO via MIMIC-MJX) against
**real fly walking kinematics** (Karashchuk et al. 2021; Pratt et al. 2024 —
see T-PRIOR-008). Neither the worm connectome's weights nor any neuron's
cellular parameters were trained — only the encoder/decoder was.

**Result:** the chimera produced "highly realistic fly walking," closely
matching real fly joint-angle trajectories and leg-coordination patterns.

**Their argument for why this proves nothing.** In the authors' own words:
"The digital sphinx model, with a worm brain and a fly body, produced highly
realistic walking... Yet the model is implausible and scientifically
meaningless... The fact that a worm connectome can be trained to control fly
walking reveals nothing about either worms or flies." It also "fails to
qualify as brain 'emulation,' which would require that the model preserves
the biological meaning of its components." Mechanistically: "the worm
connectome functions simply as a recurrent neural network (RNN) with rich
enough dynamics to support learning of realistic locomotor trajectories. Its
role in the movement policy could be fulfilled equally well by a randomly
connected RNN, akin to reservoir computing... since all the learning happens
in the black-box ANN motor decoder, a functioning interface is not necessarily
a meaningful one." Two lessons the authors draw explicitly: (1) DRL is a
powerful enough function approximator to fit realistic motion from
"incomplete or outright wrong" imposed constraints, so behavioral realism
cannot be used as evidence the constraints were right; (2) even when a brain
model and a body model are each individually defensible, a biologically
arbitrary *interface* between them can make the combined system meaningless —
and this failure mode is invisible from the outside, because the output still
looks correct.

**Their proposed criteria for real validation** (quoted, and directly usable
by this project as acceptance criteria rather than as targets themselves):

1. "neuromechanical models must be well grounded in biological knowledge.
   Most critically, **the inputs and outputs of the connectome model must be
   accurately connected to the muscles and sensors in the body model**." They
   note this mapping is only "partially achieved" today even by the best
   efforts, and that body models "also lack biological realism in their
   musculature, sensory neurons, and skeletal mechanics."
2. "neuromechanical models should be developed **in close collaboration with
   biological experiments**. Models can be powerful even without perfectly
   realistic components, provided they **generate testable predictions about
   feasible experiments**." (I.e. a model earns credibility by being falsifiable
   and by being checked, not by looking right.)
3. Implicit in their own mechanistic argument, and worth stating as an
   explicit criterion for this project: **a real-vs-randomly-rewired-connectome
   control is close to a minimum bar.** If a random or degree-matched-rewired
   network could be trained to do equally well, the specific wiring diagram is
   not what's being validated. (FlyGM, §3, is the one model in this survey
   that actually ran this control — worth noting as the field's only example
   so far of taking this specific piece of advice, albeit only at the level of
   RL task performance, not biological dynamics.)

**Their own stated limitation:** the exercise "teaches us nothing about either
animal," by design — it is a methodological cautionary tale, not a source of
biological data, and the authors say so themselves.

---

## 8. Other models found

### Network Structure Governs Drosophila Brain Functionality (Zhang et al., arXiv:2404.17128 / PMC13247498)
Also circulated under the title "Simple Network Mechanism Leads to Quasi-Real
Brain Activation Patterns with Drosophila Connectome." This model propagates
activation through the FlyWire connectome using deliberately simple,
generic neuron-activation rules and claims the resulting patterns are
"quasi-real." Worth including here specifically because of what it admits:
**it is compared against no experimental recording of any kind.** "Success" is
scored only against the authors' own anatomical/theoretical expectations (a
"consistency indicator": the fraction of activated neurons falling in the
functional region theory says they should). The authors state this
outright: their approach "fall[s] short of verifying whether a network model
accurately reflects the brain's actual activation patterns," and that
"existing experimental methods are not well-suited for directly measuring the
weights between neurons in a whole brain." They also note one of their own
hypotheses (activation likelihood by anatomical distance) underperformed in a
way that conflicts with unspecified earlier work, and that this conflict is
unresolved. **No T-PRIOR target follows from this paper** — it contributes
nothing checkable against biology — but it is a second, independent
confirmation of the pattern in Lessons below: a published connectome model
whose only validation is against its own theoretical expectations, honestly
labeled as such by its own authors.

I also came across but did not deep-dive (out of the seven requested; flagged
for awareness only): **flybody** (Vaxenburg et al. 2025, *Nature*, "Whole-body
physics simulation of fruit fly locomotion") — the shared MuJoCo body
substrate underneath both FlyGM (§3) and the Digital Sphinx (§7). It is a
biomechanics/physics paper, not a connectome-based brain model, so it's out of
this survey's scope, but any target-building work on body kinematics should be
aware it recurs as shared infrastructure across at least two of the models
above.

---

## Methodological lessons (not targets)

These are not fitting targets — they're recurring failure patterns across
this literature that should shape how this project's own validation is
designed and reported.

**1. Behavioral realism is not evidence of biological correctness.** The
Digital Sphinx is the cleanest demonstration: a worm connectome, wired to a
fly body through an untrained random projection and a black-box trained
decoder, reproduces real fly walking kinematics essentially perfectly, while
being "biologically meaningless" by construction. Any claim in this project of
the form "our model produces realistic behavior X" should be treated as
necessary but nowhere near sufficient, and should be paired with a check on
whether the *specific biological structure* used (not just "a" sufficiently
rich network) is what's doing the work.

**2. The random/rewired-connectome control is the field's closest thing to a
minimum bar, and almost nobody runs it.** Of everything surveyed, only FlyGM
(§3) compared its connectome-structured model against degree-preserving
rewired and Erdős–Rényi random graphs — and even that was only at the level of
RL task performance (angle error, convergence speed), not biological dynamics.
This project should run the equivalent control (real connectome vs.
degree-matched rewired vs. random) for any claim that "the connectome
structure explains X," and should do it at the level of whatever X is actually
claimed about (behavior, dynamics, or both) rather than only one.

**3. Interfaces are where the biology quietly disappears.** Three separate
systems in this survey (Eon's brain-body interface, FlyGM's encoder/decoder,
the Digital Sphinx's sensory random-projection and motor decoder) hide their
least-biological component at the boundary between a connectome model and
whatever consumes its output. Eon says so explicitly ("chosen by hand rather
[than] derived from the connectome"). FlyGM's encoder (raw observations →
afferent neuron states) and decoder (efferent neuron states → motor torques)
are both generic trained networks with no claimed correspondence to real
sensory or motor neuron identities, despite the recurrent core being the real
connectome. The Digital Sphinx makes this the whole point of the paper. A
model can have a biologically faithful *core* and still be biologically
meaningless *overall* if its interfaces aren't checked — this project should
budget specific validation effort for interfaces, not just for the core
network.

**4. Headline accuracy numbers travel badly and should be traced to their
original denominator before reuse.** Eon's "~95% accuracy predicting motor
behavior" is, as best I can trace it, a rounded, re-contextualized version of
a sub-statistic from Shiu et al. 2024's optogenetic screen (a study of
specific feeding/grooming circuits under experimenter-chosen stimulation),
reattached in press coverage to a claim about a different, later, embodied
system it was never measured on. Before reusing any "X% accuracy" figure
found in secondary coverage of this literature as a target, trace it to the
primary paper's own denominator and conditions — do not take a press number at
face value even when (especially when) it is round and impressive.

**5. Optimization plus connectivity does not guarantee a unique or correct
mechanism.** FlyVis's own ensemble produced three mechanistically distinct
solutions for T4 direction selectivity, and only one matched real biology —
task-optimization under connectome constraints was compatible with wrong
answers, and picking the right one required the experimental data as a
tie-breaker. This means a future version of this project's own model, if
fit primarily to connectivity plus a task objective, should expect a similar
risk of degenerate, equally-fitting-but-biologically-wrong solutions, and
should look for held-out biological data specifically capable of
distinguishing between otherwise-equivalent solutions, not just an aggregate
loss.

**6. "Validated" ranges from "matched to real neural recordings" to "our
hardware reproduces our own software" — always ask which one.** Loihi 2's
validation is hardware-vs-its-own-software-twin of an already-simplified
model; the "Network Structure Governs..." paper's validation is against its
own theoretical expectations; FlyGM's validation is against other RL
controllers. All three are legitimately called "validation" by their authors.
None of them touch a real fly. When this project cites another group's
"validated" model as license for a modeling choice, check which of these
meanings is operative.

**7. Black-box behavioral testing cannot distinguish real emulation from a
"puppet effect."** The Carboncopies critique of Eon's demo generalizes beyond
Eon: a sufficiently good body model (pre-built stabilizers, tuned gait
cycles) can convert noisy or even wrong brain output into behavior that looks
correct from the outside. Wherever this project's own body/controller
substrate is capable of self-stabilizing, a "the behavior looks right" check
is measuring the body model as much as the brain model, and internal
dynamics (not just external kinematics) need their own check.
