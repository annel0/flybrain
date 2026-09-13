# Central complex targets

Scope: the head-direction / heading-bump system built from the ellipsoid
body (EB) and protocerebral bridge (PB) — EPG ("compass") neurons, PEN1/PEN2
neurons, PEG neurons, and Delta7 interneurons — plus quantitative fan-shaped
body (FB) sleep-homeostat measurements where they exist. Perturbations first,
per the priority rule in `README.md` and the brief for this file.

This circuit is the richest quantitative target set in the fly brain: its
output is a literal, localized bump of activity whose width, amplitude,
position and velocity are all measured numbers, not population averages. A
model that cannot sustain a single localized bump at all is falsified by
section 1 before any number is even compared.

Naming note: papers use different names for the same cells. E-PG = EPG =
"compass neurons". P-EN1 = PEN1 = PEN_a. P-EN2 = PEN2 = PEN_b. P-EG = PEG.
Delta7 = Δ7, an interneuron tiling the protocerebral bridge with inhibitory
output. "PVA" = population vector average, the standard readout of bump
position from a ring of imaged ROIs (usually a 16-wedge EB grid).

Access notes: Seelig & Jayaraman 2015 (PMC4704792), Turner-Evans et al. 2017
(PMC5440168), Franconville et al. 2018 (PMC6150698), Turner-Evans &
Jayaraman 2020 (PMC8356802), Green et al. 2017 (PMC6320684), Hulse et al.
2021 (PMC9477501), Pimentel et al. 2016 (PMC4998959) and Donlea et al. 2014
(PMC3969244) were read in open-access full text via PMC (fetched as rendered
text; a single-pass extraction of long papers, so absence of a number below
is not proof it isn't in the paper somewhere we didn't reach). Kim, Rouault,
Druckmann & Jayaraman 2017 (Science) has **no PMC copy** (confirmed via
NCBI elink) and is paywalled — only the abstract was available, stated
explicitly wherever this matters rather than guessed. Fisher & Wilson 2019
(Nature) and Shiozaki & Kazama 2017 (Nat Neurosci) likewise have no PMC copy
— abstract only. Donlea et al. 2018 (Neuron, the dFB-R2-helicon loop paper)
was identified but not fetched in full text within the tool-call budget for
this file — abstract only.

---

## 1. Perturbations (causal — highest priority)

### T-CX-01  EPG silencing abolishes the localized bump

- **Quantity** — spatial structure of EB compass-neuron calcium activity
  when EPG synaptic output is acutely blocked
- **Value** — at the restrictive temperature, activity across the *entire*
  EB rose together when the fly turned, instead of a single localized peak
  moving; population-vector-average (PVA) strength (the bump "sharpness"
  metric) "dropped drastically across flies." No numeric percentage or
  before/after PVA-strength value is stated as text — it is shown only in
  a figure (Fig. 3F,G of the source).
- **Type** — perturbation
- **Method** — two-photon calcium imaging (GCaMP6f/jRGECO1a) of the EB in
  head-fixed, tethered-walking flies
- **Observation model** — UAS-shibire-ts1 in EPG neurons; permissive vs.
  restrictive (32 °C) block of synaptic output; PVA computed over the
  16-wedge EB ROI grid used throughout the source paper
- **Conditions** — head-fixed fly walking on an air-supported ball, visual
  virtual reality and darkness
- **Source** — Turner-Evans & Jayaraman et al. (2020) "The Neuroanatomical
  Ultrastructure and Function of a Biological Ring Attractor," *Neuron*
  108(1):145–163.e10. doi:10.1016/j.neuron.2020.08.006. PMID 32916090.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8356802/
- **Confidence** — medium-high for direction (bump destroyed, replaced by
  diffuse whole-EB activity); low for magnitude — no plain-text number was
  recoverable, and our fetch of this long paper may not have captured every
  section, so the absence of a number here is not conclusive.

### T-CX-02  Delta7 silencing lowers bump amplitude and makes it move erratically, but does not change its width

- **Quantity** — EB bump amplitude, width, and tracking consistency when
  Delta7 synaptic output is acutely blocked
- **Value** — at the restrictive temperature: bump amplitude decreased and
  the bump "moved erratically in response to the fly's movements"; tracking
  became "significantly less consistent" (Fig. 4Q–S). By contrast, **bump
  width was reported unchanged** ("bump amplitude was lower ... the bump
  width remained the same," Fig. S6E,F). No splitting into two discrete
  peaks is reported. Exact numbers (amplitude ratio, width in degrees
  before/after) are given only as figure panels, not as text.
- **Type** — perturbation
- **Method** — two-photon calcium imaging, as in T-CX-01
- **Observation model** — UAS-shibire-ts1 in Delta7 neurons, permissive vs.
  restrictive (32 °C) block
- **Conditions** — head-fixed tethered-walking fly, visual VR and darkness
- **Source** — Turner-Evans & Jayaraman et al. (2020), as above,
  Figs. 4Q–S, S6E–F
- **Confidence** — medium. The amplitude-down / width-unchanged dissociation
  is explicit in the text; we could not recover the actual numbers. This
  dissociation is itself a useful qualitative constraint: **amplitude and
  width are separately controlled**, so a model reproducing the bump should
  show two separable knobs, not one coupled "gain" parameter.

### T-CX-03  PEN (P-EN1) silencing degrades heading tracking in darkness

- **Quantity** — correlation between EPG bump phase and the fly's angular
  (ball) velocity, with P-EN1 synaptic output blocked
- **Value** — "the E-PG signal failed to consistently track the dynamics of
  the fly's heading in the dark" when P-EN synaptic output was blocked; the
  permissive-to-restrictive change in phase-vs.-velocity correlation was
  significantly different between P-EN>shibire-ts flies and controls
  (P < 0.01). The correlation values themselves are shown only in Fig. 4h,
  not stated as text numbers.
- **Type** — perturbation
- **Method** — two-photon calcium imaging of EPG bump position, tethered
  walking fly, closed-loop visual VR and darkness
- **Observation model** — UAS-shibire-ts1 in P-EN1 neurons; permissive vs.
  32 °C restrictive block; bump-vs.-ball-velocity correlation as readout
- **Conditions** — darkness specifically (the affected pathway is the
  self-motion update; with a visual landmark, EPG can still be cue-driven)
- **Source** — Green, Adachi et al. (2017) "A neural circuit architecture
  for angular integration in Drosophila," *Nature* 546(7656):101–106.
  doi:10.1038/nature22343. PMID 28538731.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6320684/
- **Confidence** — high for direction and significance (P < 0.01); low for
  magnitude, which was not text-quoted.

### T-CX-04  Optogenetically overwriting the bump's location — the network re-adopts and maintains the new position

- **Quantity** — EB/PB bump position and dynamics after optogenetic
  stimulation forces a new, artificial bump location
- **Value** — combining two-photon calcium imaging with optogenetics in
  tethered flying flies, the authors "overwrite the existing population
  representation with an artificial one, which was then maintained by the
  circuit with naturalistic dynamics." Interpretation: a network with local
  excitation and global inhibition enforces a *unique, persistent* heading
  representation regardless of whether it was reached by normal sensory
  drive or forced optogenetically. **No numeric values (success rate, decay
  time back to a "normal" bump, amplitude of the induced bump) could be
  retrieved** — we had abstract-level access only.
- **Type** — perturbation
- **Method** — two-photon calcium imaging + optogenetics, tethered flying
  flies
- **Observation model** — not retrievable beyond the abstract
- **Conditions** — tethered flight
- **Source** — Kim, Rouault, Druckmann & Jayaraman (2017) "Ring attractor
  dynamics in the Drosophila central brain," *Science* 356(6340):849–853.
  doi:10.1126/science.aal4835. PMID 28473639. **No PMC copy exists**
  (confirmed via NCBI elink, dbfrom=pubmed&db=pmc returns no pubmed_pmc
  link for this PMID); the publisher page is paywalled.
- **Confidence** — high for the qualitative claim (this is among the most-
  cited direct causal evidence for ring-attractor dynamics in this circuit)
  but we explicitly could not obtain any quantitative number from it. This
  is the single biggest gap in this file relative to the brief, which names
  this paper first under "perturbations." Whoever needs the numbers should
  get institutional access to *Science* 356:849–853 directly.

### T-CX-05  Delta7 is the obligatory relay from EPG to the rest of the columnar network

- **Quantity** — functional (optogenetically evoked calcium) connectivity
  from EPG onto other central-complex columnar cell types, direct vs. via
  Delta7
- **Value** — "E-PG neurons are the only columnar type that are presynaptic
  in the PB, but their activation did not trigger a significant response in
  any of the five other columnar neurons we tested" directly. By contrast,
  "the Δ7 interneurons are strongly activated by E-PG neurons, and their
  activation leads to significant responses in several columnar neuron
  types (E-PG, P-EN1, P-EN2, P-F1N3 and P-F3N2v)." The sign differs by
  target: P-ENs show mild activation, E-PG and P-F3N2v show inhibition,
  P-F1N3 shows strong rebound excitation. Ring neurons onto EPG are
  inhibitory (picrotoxin-sensitive, i.e., GABAergic). Exact ΔF/F effect
  sizes are not given as text numbers, only qualitative/significance calls
  plus a connectivity-matrix figure (Fig. 4).
- **Type** — perturbation (causal optogenetic stimulation + calcium
  imaging, not just anatomy)
- **Method** — simultaneous optogenetic stimulation (CsChrimson), two-photon
  calcium imaging, and pharmacology (picrotoxin, mecamylamine) across 70
  presynaptic-to-postsynaptic cell-type pairs, at least 6 flies per pair
- **Observation model** — response classified via Mahalanobis distance of
  the postsynaptic calcium response to a null (no-stimulation) sample
- **Conditions** — optogenetic circuit mapping preparation, not freely
  behaving flies
- **Source** — Franconville, Beron & Jayaraman (2018) "Building a functional
  connectome of the Drosophila central complex," *eLife* 7:e37017.
  doi:10.7554/eLife.37017. PMID 30124430.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6150698/
- **Confidence** — high for the qualitative wiring logic (Delta7 as
  obligatory hub, feeding inhibition back onto EPG); low for any effect-size
  number, none of which we could extract as plain text.

### T-CX-06  Landmark jump: the bump follows an abrupt cue shift with a measurable lag

- **Quantity** — EB bump position (PVA) relative to a visual landmark,
  before vs. after the landmark is abruptly displaced
- **Value** — r = 0.85, slope = 0.78 ± 0.07, R² = 0.72 (N = 50 shifts across
  n = 6 flies) relating the post-shift change in landmark position to the
  change in PVA (bump) position. A slope of 1 would mean the bump jumps
  perfectly to the new landmark position; 0.78 indicates a systematic
  undershoot.
- **Type** — perturbation (abrupt visual-scene rotation, exactly the
  experiment class named in the brief) / dynamic response
- **Method** — two-photon calcium imaging of EPG dendrites tiling the EB,
  virtual-reality single-stripe arena with the stripe suddenly repositioned
- **Observation model** — PVA computed from imaged EB tile ROIs; offset =
  angular difference between PVA and stripe position, compared immediately
  before vs. after the jump
- **Conditions** — head-fixed fly walking on an air-supported ball,
  closed-loop single-stripe virtual reality
- **Source** — Seelig & Jayaraman (2015) "Neural dynamics for landmark
  orientation and angular path integration," *Nature* 521(7551):186–191.
  doi:10.1038/nature14446. PMID 25971509.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/ (Fig. 3b)
- **Confidence** — high. This is a directly text-stated regression with N
  and R², not a figure-only estimate.

### T-CX-07  Visually evoked inhibitory map onto EPG can remap over minutes after sensorimotor conflict

- **Quantity** — spatial map of ring-neuron-mediated visual inhibition onto
  each EPG neuron, and the EB "compass coordinate frame," before vs. after
  minutes of exposure to an altered (rotated/gain-mismatched) virtual
  environment
- **Value** — qualitative only at the access level we had (abstract): a
  visual cue evokes synaptic inhibition in EPG neurons via ring neurons;
  each EPG neuron is inhibited only by specific cue positions (most
  anatomically possible R-neuron-to-EPG connections are "weak or silent");
  this pattern "can reorganize over minutes" of altered virtual reality,
  producing "persistent changes in the compass coordinate frame." **No
  quantitative remapping rate, magnitude, or trial count was recoverable.**
- **Type** — perturbation (sensorimotor conflict) / plasticity
- **Method** — in vivo whole-cell patch-clamp of EPG neurons in head-fixed
  flies, plus ensemble two-photon calcium imaging
- **Observation model** — not retrievable beyond the abstract
- **Conditions** — head-fixed, tethered walking in altered virtual reality
- **Source** — Fisher et al. (2019) "Sensorimotor experience remaps visual
  input to a heading-direction network," *Nature* 576(7785):121–125.
  doi:10.1038/s41586-019-1772-4. PMID 31748749. No PMC copy found via
  elink; abstract-only access.
- **Confidence** — medium for the qualitative claim (it is the paper's
  headline result); not usable yet as a numeric target.

### T-CX-08  Silencing the bulb (BU) impairs landmark-memory-guided steering

- **Quantity** — flight-simulator directional-choice behavior based on a
  recently seen landmark, with bulb (BU) neurons silenced
- **Value** — qualitative only (abstract-level access): silencing BU
  neurons impaired landmark-experience-guided directional choice; dorsal BU
  calcium activity encoded recent landmark location, ventral BU tracked
  self-motion/turning. **No behavioral effect size (e.g., % correct choice,
  control vs. silenced) was recoverable.**
- **Type** — perturbation
- **Method** — flight simulator (rigid tether), two-photon calcium imaging
  during flight, photolabeling-based circuit tracing
- **Observation model** — not retrievable beyond the abstract
- **Conditions** — tethered flight
- **Source** — Shiozaki & Kazama (2017) "Parallel encoding of recent visual
  experience and self-motion during navigation in Drosophila," *Nat
  Neurosci* 20(10):1395–1403. doi:10.1038/nn.4628. PMID 28869583. No PMC
  copy found; abstract only.
- **Confidence** — low-medium; included because the brief specifically asks
  about landmark-memory and visual-rotation experiments, but this circuit
  (BU → ring neurons → EPG) sits upstream of the EB bump rather than being
  a bump measurement itself.

---

## 2. Heading bump: width, tracking gain, and persistence

### T-CX-09  Bump width (FWHM) in the EB — varies with visual condition, and two papers' central values do not match exactly (recorded as a conflict, not resolved)

- **Quantity** — full width at half maximum (FWHM) of the EPG population
  calcium bump in the ellipsoid body
- **Value** — from Seelig & Jayaraman (2015), all mean ± s.d.:
  - single vertical stripe: **82.3° ± 11.5°** (n = 15 flies) [Fig. 1k]
  - multiple visual features: **84.9° ± 12.6°** (n = 9 flies); not
    significantly different from single stripe, p = 0.14
  - two identical stripes: **78.7° ± 15.6°** (n = 7 flies); significantly
    narrower than single stripe, p = 4.5 × 10⁻⁶
  - darkness (6 mm ball): **90.9° ± 11.2°**; significantly wider than
    single stripe, p = 8 × 10⁻⁹

  From Turner-Evans et al. (2017, eLife): both the EPG and P-EN bumps in
  the EB are stated as **~100° wide (FWHM)**, reported flat/constant across
  different angular-velocity bins (the bump does not visibly broaden when
  the fly turns faster). In the protocerebral bridge, bump half-width spans
  **~2 glomeruli** (of 9 per side).
- **Type** — steady-state (per visual condition) / dynamic response
  (constancy across velocity)
- **Method** — two-photon calcium imaging (GCaMP); EB divided into a
  16-wedge (~22.5°/wedge) ROI grid for readout in both papers
- **Observation model** — bump = spatial calcium profile around the EB ring
  per imaging frame; FWHM computed on the fitted or raw profile. Our
  extractor should bin any simulated bump profile onto the same 16-wedge
  grid before computing FWHM, to compare fairly.
- **Conditions** — head-fixed tethered-walking fly, various visual VR
  conditions and darkness, room temperature
- **Source** — Seelig & Jayaraman (2015), *Nature* 521:186–191, PMID
  25971509, Fig. 1k / Fig. 2c / Extended Data Figs. 4c, 7a
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC4704792/); and Turner-Evans et
  al. (2017) "Angular velocity integration in a fly heading circuit,"
  *eLife* 6:e23496. doi:10.7554/eLife.23496. PMID 28530551, Fig. 9 /
  Fig. 8E,F (https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/)
- **Confidence** — high for the Seelig et al. numbers (explicit text values
  with n and p). Medium for the Turner-Evans "~100°" figure (stated in text
  but as an approximate, not mean ± s.d.). **Conflict**: 79–91° vs. ~100°
  are in the same rough range but do not match exactly — record both rather
  than picking one; a model should be judged against an ~80–100° band, not
  a single point value.

### T-CX-10  Tracking gain (slope) between visual landmark position and bump position

- **Quantity** — slope of bump (PVA) position vs. visual landmark position,
  mapped from a 270° visual arena onto the 360° EB
- **Value** — single stripe: slope = 0.92 ± 0.32 (n = 172 walking epochs);
  multiple features: 0.97 ± 0.43 (n = 74 epochs); two stripes: 1.08 ± 0.41
  (n = 96 epochs). All close to the ideal gain of 1.
- **Type** — steady-state / dynamic response
- **Method** — two-photon calcium imaging, PVA vs. stripe azimuth during
  closed-loop walking
- **Observation model** — linear regression of PVA angle against cue angle
  across walking epochs; our extractor should apply the same epoch-based
  regression, not an instantaneous per-frame comparison
- **Conditions** — head-fixed tethered walking, closed-loop visual VR
- **Source** — Seelig & Jayaraman (2015), as above, Extended Data
  Figs. 2d, 3d, 4g
- **Confidence** — high; explicit text values with n.

### T-CX-11  Bump persistence and drift in darkness

- **Quantity** — how long the EB bump maintains a stable position without
  visual input or locomotion (standing in the dark), and how far it drifts
- **Value** — mean standing-bout duration before the PVA drifted from its
  initial position: **6.7 ± 5.1 s** (n = 499 standing bouts across n = 11
  flies); qualitatively, activity "sometimes persisted for more than
  30 seconds." Drift magnitude during standing: mean ΔPVA = 0.017 ± 0.76 rad
  (≈ 1° ± 44°, i.e. near-zero mean but large trial-to-trial spread).
- **Type** — steady-state (persistence) / dynamic response (drift)
- **Method** — two-photon calcium imaging during quiescent (non-walking)
  bouts on the ball, in darkness
- **Observation model** — "standing" defined by a ball-velocity threshold;
  drift = change in PVA angle from start to end of a standing bout
- **Conditions** — head-fixed, darkness, no locomotion
- **Source** — Seelig & Jayaraman (2015), as above, Fig. 4i, Extended Data
  Fig. 10b,d,f
- **Confidence** — high for the 6.7 ± 5.1 s value and drift statistics
  (explicit text numbers with n); the ">30 s" claim is qualitative only.

### T-CX-12  Self-motion-to-bump gain in darkness is low and highly variable before visual experience

- **Quantity** — gain relating the fly's walking (ball) rotation to bump
  (PVA) rotation, in darkness, in flies with no prior visual-landmark
  exposure in the session
- **Value** — mean gain = **0.47 ± 1.2** (n = 397 walking bouts) — on
  average the bump moves less than half as much as ideal path integration
  would require, with variance exceeding the mean.
- **Type** — steady-state / dynamic response
- **Method** — two-photon calcium imaging, darkness, naive flies
- **Observation model** — regression slope of PVA rotation vs. ball
  rotation across walking bouts
- **Conditions** — head-fixed, darkness, naive (pre-visual-experience) flies
- **Source** — Seelig & Jayaraman (2015), as above, Extended Data Fig. 9a
- **Confidence** — medium — explicit text number, but the spread (± 1.2 on
  a mean of 0.47) means this alone is not a tight constraint; treat it as
  "path integration gain is poor and unreliable without visual calibration"
  with a rough scale, not a precise target.

---

## 3. Angular velocity → bump velocity (path integration gain)

### T-CX-13  PEN calcium asymmetry correlates with angular velocity

- **Quantity** — correlation between the left-right difference in P-EN
  calcium signal (in the noduli) and the fly's angular velocity
- **Value** — Pearson **R = 0.65 ± 0.14** (mean ± s.d., N = 10 flies)
- **Type** — dynamic response
- **Method** — two-photon calcium imaging of P-EN termini in the noduli,
  tethered walking fly
- **Observation model** — per-frame or per-bin correlation of (L−R) ΔF/F
  against angular velocity from the ball tracker
- **Conditions** — head-fixed tethered walking, visual VR
- **Source** — Turner-Evans et al. (2017), *eLife* 6:e23496, PMID 28530551,
  Fig. 2D. https://pmc.ncbi.nlm.nih.gov/articles/PMC5440168/
- **Confidence** — high; explicit text value with N.

### T-CX-14  PEN-EPG bump offset grows with angular velocity — the mechanistic basis of bump movement

- **Quantity** — angular offset between the P-EN bump and the EPG bump in
  the EB, as a function of the fly's angular (turning) velocity
- **Value** — offset grows from near zero at low angular velocity to
  **20.7° ± 11.7°** at 150–180°/s; the increase with velocity is
  significant (p = 1.3 × 10⁻⁷, one-way ANOVA). Bump width itself (both P-EN
  and EPG, ~100° FWHM, see T-CX-09) stays flat across these same velocity
  bins — only the offset (position), not the width, scales with speed.
- **Type** — dynamic response. This is arguably the single most useful
  number in this file for constraining an angular-path-integration model:
  it directly ties a kinematic variable (turning speed) to a specific
  internal-variable prediction (leading bump offset).
- **Method** — two-color two-photon calcium imaging (GCaMP6f in one
  population, jRGECO1a in the other) to image P-EN and EPG bumps
  simultaneously in the same fly (N = 10 flies)
- **Observation model** — offset = circular difference between the two
  fitted bump-center positions, binned by simultaneous angular velocity
  from the ball tracker
- **Conditions** — head-fixed tethered walking, visual VR
- **Source** — Turner-Evans et al. (2017), as above, Fig. 9G
- **Confidence** — high; explicit text value with a stated p-value, from a
  two-color experiment specifically designed to measure this.

### T-CX-15  PEN firing-rate modulation with turn direction (electrophysiology)

- **Quantity** — P-EN spike rate during fast turns in the cell's preferred
  vs. non-preferred rotational direction, and the angular-velocity range
  ("bandwidth") over which firing is modulated
- **Value** — spike rate increased by **5.6 ± 3.7 Hz** during fast turns in
  the preferred vs. non-preferred direction (N = 12 cells); the rotational
  velocity range over which activity was modulated was **145 ± 82 °/s**
  (N = 12)
- **Type** — dynamic response
- **Method** — in vivo electrophysiology (patch-clamp) from P-EN neurons,
  tethered walking fly
- **Observation model** — spike rate binned by simultaneous ball angular
  velocity, split by rotation direction relative to each cell's preferred
  direction
- **Conditions** — head-fixed tethered walking, visual VR
- **Source** — Turner-Evans et al. (2017), as above, Fig. 4B
- **Confidence** — high; explicit text values with N. This is the only
  direct spike-rate (Hz) number for any central-complex heading cell type
  that we could recover anywhere in this search — see the gap noted in
  T-CX-17.

### T-CX-16  Per-cell-type "ball-tracking gain" values in Green et al. 2017 — flagged as a likely calibration artifact, not a neural gain

- **Quantity** — a gain parameter of 0.75 (EPG), 1.0 (P-EN1), and 0.89
  (P-EN2) appears in the paper's extended data
- **Value** — 0.75 / 1.0 / 0.89 for EPG / P-EN1 / P-EN2 respectively
  (Extended Data Fig. 2)
- **Type** — steady-state (methodological parameter, not a measured
  biological dynamic)
- **Method** — described as a per-fly, per-cell-type "ball position gain"
  used in the imaging/tracking analysis pipeline, not a stimulation or
  recording protocol
- **Observation model** — the authors explicitly caution: "We do not
  interpret these different gains ... to mean that the three cell types
  have phase signals that drift relative to each other" — i.e., they warn
  against reading this as a real biological gain difference between cell
  types
- **Conditions** — n/a
- **Source** — Green et al. (2017), *Nature* 546:101–106, PMID 28538731,
  Extended Data Fig. 2 and its legend
- **Confidence** — low, by the authors' own statement. Included only so
  that if this number resurfaces elsewhere (e.g., in a review) it is not
  mistaken for a genuine EPG-vs-PEN gain difference.

---

## 4. Firing rates of EPG, PEN, PEG and Delta7

### T-CX-17  What we could and could not find

- We found one directly stated electrophysiological firing-rate number for
  this circuit: the P-EN modulation depth of **5.6 ± 3.7 Hz** and bandwidth
  of **145 ± 82 °/s** in T-CX-15 (Turner-Evans et al. 2017). We did **not**
  find a stated baseline or peak absolute firing rate (e.g., "X Hz inside
  the bump vs. Y Hz outside it") for P-EN, and we found **no**
  electrophysiological firing-rate numbers at all — inside-bump,
  outside-bump, or otherwise — for EPG, PEG, or Delta7 neurons in any
  source we accessed.
- The reason is largely methodological: essentially every EPG/PEG/Delta7
  study in our source list (Seelig & Jayaraman 2015, Kim et al. 2017,
  Turner-Evans & Jayaraman 2020, Franconville et al. 2018) uses two-photon
  **calcium imaging** (GCaMP6f/jRGECO1a/GCaMP3), reporting ΔF/F, not spike
  rates. Turner-Evans et al. (2017) is the exception, and it patch-clamped
  P-EN neurons specifically, not EPG/PEG/Delta7.
- **Type** — n/a (this is a documented gap, not a data point)
- **Confidence** — n/a. Anyone needing EPG/PEG/Delta7 spike rates should
  check whether Turner-Evans & Jayaraman (2020, Neuron) has a supplementary
  electrophysiology section beyond what our single-pass fetch captured (we
  could not rule this out with certainty), or look at preprint/unpublished
  sources not searched here.

---

## 5. Fan-shaped body sleep measurements

Quantitative numbers exist here, but almost all of the ones we could recover
are **relative changes or inferential statistics (p-values, F-values)**
rather than absolute physiological values (mV, MΩ, ms) or absolute sleep
amounts (minutes/day) — the absolute numbers appear to live only in figures
we could not read pixel values from. This is stated plainly per entry below
rather than estimated.

### T-CX-18  Dorsal FB (dFB) neuron excitability state switch: input resistance and membrane time constant drop from the "ON" (high sleep pressure) to the "OFF" (low sleep pressure) state

- **Quantity** — input resistance and membrane time constant of dFB
  sleep-promoting neurons, comparing the electrically active ("ON") state
  to the electrically silent ("OFF") state
- **Value** — both dropped when switching ON→OFF: input resistance fell to
  **53.3 ± 1.8%** of its ON-state value, and membrane time constant fell to
  **24.0 ± 1.3%** of its ON-state value (mean ± s.e.m., n = 15 cells).
  These are *relative* (fractional) changes — the absolute ON-state or
  OFF-state values in MΩ or ms were not recoverable as plain text (Fig. 3b,c
  in the source).
- **Type** — perturbation / dynamic response (dopamine-triggered state
  switch, see T-CX-19)
- **Method** — in vivo whole-cell patch-clamp of dFB neurons
- **Observation model** — input resistance and membrane time constant from
  standard current-step protocols; ON/OFF state assigned per-cell from the
  same recording
- **Conditions** — dFB neurons in flies under varying sleep pressure
  (sleep-deprived vs. rested)
- **Source** — Pimentel et al. (2016) "Operation of a homeostatic sleep
  switch," *Nature* 536(7616):333–337. doi:10.1038/nature19055.
  PMID 27487216. https://pmc.ncbi.nlm.nih.gov/articles/PMC4998959/
- **Confidence** — high for the relative-change numbers (explicit text,
  n = 15 cells); incomplete without absolute MΩ/ms values, which we state
  plainly we could not extract as text.

### T-CX-19  Dopamine hyperpolarizes dFB neurons within tens of milliseconds by ~7.5 mV

- **Quantity** — magnitude and time course of dopamine-induced membrane
  hyperpolarization in dFB neurons
- **Value** — hyperpolarization occurred **within tens of milliseconds** of
  dopamine application; magnitude ranged **2–13 mV**, mean **7.50 ± 0.56 mV**
  (mean ± s.e.m.)
- **Type** — perturbation / dynamic response
- **Method** — in vivo whole-cell patch-clamp, local dopamine
  application/puff, dFB neurons
- **Observation model** — membrane potential trace aligned to dopamine
  onset; hyperpolarization measured as peak deflection from baseline
- **Conditions** — dFB neurons, in vivo
- **Source** — Pimentel et al. (2016), as above, Fig. 1a,c
- **Confidence** — high; explicit text values.

### T-CX-20  cv-c-dependent excitability of dFB neurons tracks sleep pressure — effect sizes given only as inferential statistics, not absolute values

- **Quantity** — input resistance (Rm) and membrane time constant (τm) of
  dFB neurons in cv-c mutants vs. wild-type, and their dependence on prior
  sleep history
- **Value** — Rm and τm were both reduced in cv-c mutants vs. WT controls
  (n = 37–82 cells per group; two-tailed t-test, **p = 0.0026** for Rm,
  **p < 0.0001** for τm). Sleep history (rested vs. deprived) interacted
  significantly with genotype for both Rm (F(2,243) = 3.109, **p = 0.0464**)
  and τm (F(2,231) = 3.701, **p = 0.0262**), i.e. sleep deprivation raises
  Rm/τm in WT but this modulation is blunted in cv-c mutants. **No absolute
  Rm (MΩ) or τm (ms) values, nor an effect size in natural units, were
  recoverable as text** — only the statistical test results; the actual
  values appear to be confined to Figs. 6A and 7A–B.
- **Type** — perturbation (genetic) / dynamic response (sleep-history
  dependence)
- **Method** — in vivo whole-cell patch-clamp of dFB neurons
- **Observation model** — Rm, τm from current-step protocols; compared
  across genotype and sleep-history groups
- **Conditions** — cv-c mutant vs. heterozygous control flies, rested vs.
  sleep-deprived
- **Source** — Donlea et al. (2014) "Neuronal machinery of sleep
  homeostasis in Drosophila," *Neuron* 81(4):860–872.
  doi:10.1016/j.neuron.2013.12.013. PMID 24559676.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3969244/
- **Confidence** — medium. Direction and significance are explicit and
  well-powered (dozens of cells per group); the actual electrophysiological
  values are not, and we say so rather than infer them.

### T-CX-21  cv-c is required in dFB neurons for normal total sleep time — direction and significance only, no absolute sleep-time numbers recovered

- **Quantity** — total daily sleep time and sleep rebound after deprivation,
  cv-c mutant/knockdown vs. control
- **Value** — cv-c mutants: significant genotype effect on total sleep time
  per day, F(2,141) = 70.03, **p < 0.0001**, and reduced sleep rebound after
  12 h overnight deprivation vs. heterozygous controls (exact percentages
  not text-quoted). dFB-restricted RNAi knockdown of cv-c (three independent
  driver lines: C5-GAL4, 104y-GAL4, 23E10-GAL4) each significantly reduced
  sleep vs. parental controls (F(2,71) = 24.87, F(2,73) = 21.09,
  F(2,94) = 38.17 respectively, all **p < 0.0001**). **The actual sleep-time
  values (minutes/day or % time asleep) were not recoverable as plain
  text** — the paper reports ANOVA statistics in text and puts the bar
  heights only in Figs. 1B–D and 3D,H,L.
- **Type** — perturbation
- **Method** — locomotor/sleep monitoring (Drosophila Activity Monitor-style
  assay); the specific inactivity threshold defining "sleep" was not
  confirmed from the text we extracted, though ≥5 min is standard for this
  experimental tradition
- **Observation model** — total sleep time and rebound computed from
  activity-monitor beam breaks; our extractor would need the same
  inactivity threshold and bout-merging rule, not independently confirmed
  here
- **Conditions** — adult flies, 12:12 LD, cv-c mutant/RNAi vs. controls
- **Source** — Donlea et al. (2014), as above, Figs. 1B–D, 2C, 3D,H,L, 4A
- **Confidence** — medium for direction/significance; low for magnitude,
  explicitly not recovered.

### T-CX-22  dFB–R2(ellipsoid body)–helicon cell autoregulatory sleep-pressure loop — qualitative only, not fetched in full text

- **Quantity** — a proposed circuit loop: dFB neurons inhibit "helicon
  cells" (AstA-R1-expressing interneurons linking the superior arch to the
  EB) via allatostatin-A; helicon cells excite EB R2 (ring) neurons, whose
  activity-dependent plasticity is proposed to signal rising sleep pressure
  back to dFB
- **Value** — qualitative only at the access level we used (abstract):
  enhancing or diminishing allatostatinergic transmission from dFB, and
  inhibiting or optogenetically stimulating helicon cells, both changed
  sleep in the direction the model predicts. **No quantitative sleep
  amounts, calcium-signal changes, or synaptic weights were retrieved** —
  we did not spend budget fetching this paper's full text, so this entry is
  a bigger gap than T-CX-18 through T-CX-21 (those had full-text access,
  just not every number in text form; this one is abstract-only by choice
  of where we spent the tool-call budget).
- **Type** — perturbation
- **Method** — not retrieved
- **Observation model** — not retrieved
- **Conditions** — not retrieved
- **Source** — Donlea et al. (2018) "Recurrent Circuitry for Balancing
  Sleep Need and Sleep," *Neuron* 97(2):378–389.e4.
  doi:10.1016/j.neuron.2017.12.016. PMID 29307711.
- **Confidence** — low, and explicitly incomplete. If FB sleep dynamics
  become a modeling priority, this is the next paper to pull full text
  from.

---

## Anatomical reference numbers (not dynamic targets, but needed to build the observation model)

From Hulse et al. (2021) "A connectome of the Drosophila central complex
reveals network motifs suitable for flexible navigation and context-
dependent action selection," *eLife* 10:e66039. doi:10.7554/eLife.66039.
PMID 34696823. https://pmc.ncbi.nlm.nih.gov/articles/PMC9477501/ — the full
EM connectome (hemibrain) paper that Turner-Evans and Hulse produced:

- Neuron counts per hemisphere (hemibrain reconstruction): **EPG = 46,
  PEN_a (P-EN1) = 20, PEN_b (P-EN2) = 22, Delta7 = 42, PEG = 18**.
- Protocerebral bridge: **9 glomeruli per side** (18 total), consistent
  with the "~2 glomeruli" PB half-width figure in T-CX-09.
- We did **not** find, in what our fetch of this very long paper captured,
  an explicit synapse-count number for the EPG→Delta7→PEN/EPG loop, nor a
  stated "N columns of inhibition width" bump-width prediction derived
  directly from the connectome. These are very likely in the paper (it is
  built specifically to make such predictions) but were not in the excerpt
  we retrieved — flagged as not found rather than assumed absent.

These are not fitting targets in themselves (they are static anatomy, not a
measured dynamic), but any model claiming to reproduce EPG/PEN/PEG/Delta7
dynamics should use population sizes in this range, not arbitrary ones.

---

## What we looked for and did not find

- **A quantified "bump splits into two" perturbation result.** The brief
  specifically asks whether silencing/activating specific cell classes
  causes the bump to split. In the sources we could access, Delta7
  silencing causes amplitude loss and erratic movement (T-CX-02) and EPG
  silencing causes loss of localization entirely (T-CX-01) — neither source
  reports a clean split into two discrete bumps. Bump splitting is a
  standard failure mode/prediction in ring-attractor *theory* and spiking
  models of the protocerebral bridge (e.g., Kakaria & de Bivort (2017)
  "Ring Attractor Dynamics Emerge from a Spiking Model of the Entire
  Protocerebral Bridge," *Front Behav Neurosci*, PMID 28261066 — a modeling
  paper, not data, so not included as a target), but we found no
  experimental paper in this search reporting bump-splitting
  quantitatively. Treat as an open question, not a documented absence of
  the phenomenon.
- **Any quantitative number at all from Kim, Rouault, Druckmann &
  Jayaraman (2017), Science** — the paper the brief names first under
  "perturbations." It has no PMC copy; we only had the abstract (T-CX-04).
  This is the most important follow-up for anyone with *Science* access.
- **Baseline or peak firing rates (Hz) for EPG, PEG, or Delta7 neurons**,
  inside or outside the bump (T-CX-17). Only P-EN has a directly reported
  electrophysiological number in this search.
- **Explicit synapse counts or a bump-width prediction directly from the EM
  connectome** (Hulse et al. 2021) — we obtained per-cell-type counts and
  PB glomerulus count, but not the finer connectivity numbers (see the
  anatomical reference section above).
- **Pisokas & Webb (2020), eLife**, "The head direction circuit of two
  insect species" (PMID 32628112) — identified as likely relevant
  (comparative, connectome-based modeling of the HD circuit across species)
  but not fetched at all within the budget for this file.
- **Absolute physiological values behind the FB sleep p-values** (T-CX-20,
  T-CX-21) — resting potentials, MΩ, ms, and minutes/day are all reported
  only in figures in the two sleep papers we read in full text.
