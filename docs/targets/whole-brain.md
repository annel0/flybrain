# Whole-brain and behavioural-state targets

Scope: brain-wide activity level, functional networks, behavioural-state
modulation, excitation/inhibition balance, and seizure as a perturbation.
These are meant to constrain the model's global operating point — see
`../lab-notebook.md` (2026-09-13 entries) for why that is currently our
biggest unresolved problem, and `../theory-review.md` for the balanced-network
framing this file assumes throughout.

**Headline honest answer, stated up front:** nobody has measured the
brain-wide distribution of spontaneous firing rates in *Drosophila*. There is
no dense electrophysiological survey and no calcium-imaging dataset that
reports spike-level statistics across the whole central brain. What exists is
(a) scattered single-cell-type patch-clamp measurements, each from a different
lab, prep, and often a different decade; (b) whole-brain calcium imaging that
reports neuropil-averaged fluorescence correlated with behaviour, not spike
counts; and (c) the fact that the most comparable existing model — a
connectome-scale spiking simulation of the whole fly brain — does not validate
against any such distribution either, because it can't. Sections 1 and 4 below
collect what does exist and are explicit about the gap. Sections 2, 3 and 5
are in better shape.

---

## 1. Firing-rate distributions across the brain

### T-WB-1  Brain-wide spontaneous firing-rate distribution — not measured

- **Quantity** — distribution (median, spread, fraction silent) of spontaneous
  firing rates across identified central neurons, brain-wide
- **Value** — **not measured.** No study reports a brain-wide census of
  spontaneous spike rates in *Drosophila*. The closest things that exist are
  (i) single-cell-type in vivo patch-clamp studies (a few dozen cell types at
  most, see T-WB-2/T-WB-3), each too small and too methodologically distinct
  to pool into a distribution, and (ii) calcium imaging, which reports
  fluorescence, not spikes, at rates far below typical firing rates (see
  T-WB-6/T-WB-9/T-WB-10) and cannot recover a rate distribution without an
  indicator deconvolution step that nobody has validated brain-wide in this
  animal
- **Type** — steady-state
- **Method** — n/a (no method exists at this scope)
- **Observation model** — n/a. This is the gap our extractor cannot be built
  to close by better engineering; it has to be closed by picking a proxy
  (see T-WB-2 through T-WB-5) and being honest that it is a proxy
- **Conditions** — n/a
- **Source** — absence claim based on a targeted literature search
  (September 2026) across PubMed/eLife/bioRxiv for "Drosophila brain-wide
  firing rate distribution", "central neuron spontaneous rate survey", and
  related terms; corroborated by the State of Brain Emulation Report 2025
  (https://arxiv.org/abs/2510.15745), which states that no organism has
  whole-brain recording at single-neuron spike resolution, and that calcium
  imaging — the only brain-wide method available in *Drosophila* — runs at
  1-30 Hz against real firing rates that are faster and less regular than that
- **Confidence** — high, for the negative claim (absence is easier to be
  confident about after a systematic search than a positive number would be).
  A single unpublished or overlooked dataset could exist; we did not find one

**Aside, not a target:** a neuromorphic simulation of the FlyWire connectome on
Loihi 2 hardware (arXiv:2508.16792) reports about 0.3% of ~138,000 neurons
active at any time — but this is another group's *model output* under their
own parameter choices, structurally the same kind of number our own
`operating_point.py` produces, not a measurement of the real animal. It is
listed here only to flag that other people fitting the same connectome without
brain-wide ground truth have also converged on extreme sparsity as a
modelling choice rather than a validated target.

### T-WB-2  Antennal-lobe projection neurons rest close to spike threshold

- **Quantity** — resting membrane potential of antennal-lobe projection
  neurons (PNs) in vivo, and qualitative distance from spike threshold
- **Value** — whole-cell mode: **-47.8 ± 1.6 mV** (N = 12); cell-attached mode
  (closer to true resting potential, since whole-cell breaks in disturb it):
  **-57.8 ± 1.5 mV** (N = 12). The ~10 mV difference is attributed to seal
  conductance depolarizing the cell in whole-cell mode — a systematic artefact
  the authors name explicitly, not noise. Separately, PN physiology is
  repeatedly described (Kazama & Wilson's papers on this circuit) as resting
  close to spiking threshold, consistent with fluctuation-driven rather than
  mean-driven firing, but we could not independently pull a quantified
  threshold-distance number from those papers in this pass
- **Type** — steady-state
- **Method** — in vivo whole-cell and cell-attached patch clamp, adult female
  flies 2-10 days post-eclosion, identified PN types via GH146-Gal4,
  NP3062-Gal4, NP5221-Gal4 driver lines (DM1 and other glomerular classes)
- **Observation model** — if comparing to a model's resting V_m, use the
  cell-attached number (-57.8 mV) as the less-biased estimate, and treat any
  whole-cell-derived resting potential in the wider literature as
  possibly ~10 mV too depolarized for the same reason
- **Conditions** — adult, female, in vivo, brain intact, unclear if
  anaesthetised during dissection but recording itself is in an awake
  preparation typical of the Wilson-lab antennal lobe rig
- **Source** — Gouwens NW, Wilson RI (2009) "Signal propagation in Drosophila
  central neurons." *J Neurosci* 29(19):6239-6249.
  https://www.jneurosci.org/content/29/19/6239 (PMID 19439602)
- **Confidence** — high for the two V_m numbers and the artefact explanation
  (directly extracted from the paper); low/medium for the general "rests near
  threshold" characterization, which is a paraphrase from secondary sources
  describing the Kazama & Wilson body of work rather than a number we
  independently verified against primary text in this pass

### T-WB-3  Kenyon cells are close to silent at baseline, by circuit design

- **Quantity** — Kenyon cell (KC) spontaneous firing and what keeps it low
- **Value** — no brain-wide-style aggregate rate reported, but the mechanism
  is well characterised: KC responses are sparse relative to their PN inputs
  because (i) excitatory PSPs from PN input decay rapidly, (ii) PN-to-KC
  convergence is low (~10 PNs/KC on average), and (iii) KC spike threshold is
  high. This is a structural explanation for near-silence, not a rate number
  we can cite directly. This is directly relevant to our own APL/sparseness
  work (`lab-notebook.md`, 2026-09-13, sections 5-6): the mechanism described
  here is the animal-side reason KCs sit near threshold at baseline, which is
  the same "far below threshold, fluctuation-driven" regime our own balanced
  fit reproduces at the population level
- **Type** — steady-state
- **Method** — in vivo whole-cell patch clamp recording from KCs, odour
  stimulation, comparison to simultaneously-characterised PN input statistics
- **Observation model** — a model claiming to reproduce KC sparseness should
  reproduce it through the same three structural routes (fast EPSP decay, low
  convergence, high threshold), not just by turning up global inhibition —
  which is exactly the point our theory-review.md already makes about
  point-neuron APL being the wrong instrument
- **Conditions** — in vivo, adult, odour-evoked and spontaneous conditions
  compared
- **Source** — Turner GC, Bazhenov M, Laurent G (2008) "Olfactory
  representations by Drosophila mushroom body neurons." *J Neurophysiol*
  99:734-746. PMID 18094099
- **Confidence** — medium. The mechanism is well-established and widely
  cited, but we worked from search-engine-extracted summaries of the paper
  rather than the primary numeric tables (direct PDF fetch was not
  machine-readable in this pass), so no baseline Hz figure is quoted here —
  deliberately, rather than guess one

### T-WB-4  Olfactory receptor neurons show wide, receptor-type-specific spontaneous-rate heterogeneity (peripheral, not central — included for contrast)

- **Quantity** — spontaneous firing rate across ~24 identified olfactory
  receptor neuron (ORN) types
- **Value** — heterogeneous across receptor type; the one number we could
  directly confirm is **Or47a < 4 spikes/s**. We did not verify the full
  reported range across all 24 receptor types in this pass and are
  deliberately not repeating a fuller range from memory
- **Type** — steady-state
- **Method** — single-sensillum extracellular recording, "empty neuron"
  heterologous expression system for receptor-by-receptor comparison
- **Observation model** — n/a directly to our model (these are peripheral
  sensory neurons upstream of the circuit we simulate), but this is the
  best-quantified example of a genuine across-cell-type spontaneous-rate
  *distribution* that exists anywhere in the fly nervous system, and it is
  heterogeneous by an order of magnitude or more between receptor types. That
  argues against assuming a single spontaneous rate for all cells of a given
  broad class in the model
- **Conditions** — adult, in vivo, sensillum recording
- **Source** — Hallem EA, Carlson JR (2006) "Coding of odors by a receptor
  repertoire." *Cell* 125:143-160
- **Confidence** — medium. The <4 spikes/s figure for Or47a is confirmed; the
  general claim of order-of-magnitude heterogeneity across the receptor
  repertoire is well known in the olfaction literature but we are citing it
  cautiously since we verified only one data point directly

### T-WB-5  The field's own whole-CNS spiking model has no brain-wide firing-rate ground truth to validate against either

- **Quantity** — whether the most directly comparable prior work (a
  leaky-integrate-and-fire model built on the full adult brain connectome)
  validated its simulated firing rates against measured brain-wide rates
- **Value** — no. The model (~125,000 neurons, ~50 million synapses) was
  validated against specific, previously-published circuit-level predictions
  (which neurons respond to sugar/water/bitter gustatory input, which neurons
  drive proboscis extension and antennal grooming) — i.e., against sparse,
  circuit-specific behavioural/physiological predictions, not against a
  brain-wide rate distribution
- **Type** — steady-state (absence of validation target)
- **Method** — LIF connectome simulation; validation by comparison to
  previously published sparse circuit-level findings, not electrophysiology
  collected for this purpose
- **Observation model** — reinforces T-WB-1: this is independent evidence
  that brain-wide rate ground truth doesn't exist, from a group that had
  every incentive to use it if it existed
- **Conditions** — n/a
- **Source** — Shiu PK, Sterne GR, Spiller N, et al. (2024) "A Drosophila
  computational brain model reveals sensorimotor processing." *Nature*
  634:210-219. PMID 39358519. Preprint: Shiu et al., bioRxiv
  10.1101/2023.05.02.539144
- **Confidence** — medium. Based on search-level summaries of their
  validation approach, not a full read of their methods section; worth a
  direct check of their supplementary material before leaning on this claim
  further, since a supplement is where such a comparison would likely live if
  it existed at all

---

## 2. Whole-brain calcium imaging

### T-WB-6  Brain-wide activity rises with walking; ~20% of variance explained

- **Quantity** — correlation between brain-wide neural activity and walking
  behaviour, pan-neuronally and by neurotransmitter class
- **Value** — all anatomically defined brain regions were significantly
  positively correlated with walk (95% CI above zero, adjusted p < 0.001
  everywhere). Pan-neuronal regression of activity against walking: **median
  R² = 0.194**. Cholinergic (excitatory), glutamatergic, and GABAergic
  (inhibitory) neuron classes showed statistically indistinguishable spatial
  activity maps (cosine similarity Cha-vs-Vglut 0.98, Cha-vs-Gad 0.99,
  Vglut-vs-Gad 0.98) — i.e. excitation and inhibition both scale up together
  with walking, brain-wide, at this resolution
- **Type** — steady-state / dynamic response (activity tracks behaviour bout
  by bout)
- **Method** — light-field microscopy (Thorlabs Cerna, microlens array,
  Leica 25x/0.95 or 20x/1.0 objective), **frame rate 5-98 Hz depending on
  expression/SNR, most experiments at 5/10/20/50 Hz**, restricted to ≥30 Hz
  for temporal-dynamics analysis. Indicators: **GCaMP6s/6m/6f/7s/7f**
  (UAS-GCaMP, various), plus UAS-syt-GCaMP6s for presynaptically-tethered
  signal. Driver lines: pan-neuronal nsyb-Gal4 and GMR57C10-Gal4;
  neurotransmitter-specific Cha-Gal4 (cholinergic), Vglut-Gal4 (glutamatergic),
  Gad1-Gal4 (GABAergic); neuromodulatory TH/DDC-Gal4 (dopaminergic),
  Tdc2-Gal4 (octopaminergic), Trh-Gal4 (serotonergic). Voxel-level neuropil
  signal reduced to functional components via PCA→ICA and correlated with a
  walk regressor
- **Observation model** — our extractor must convolve simulated spikes with
  the specific GCaMP variant's kinetics used in a given comparison, then
  downsample to the actual frame rate used for that panel (these varied
  5-98 Hz within the same paper) before computing any R² against a behaviour
  regressor — a raw simulated rate is not comparable to this number
- **Conditions** — tethered adult female flies, walking on an air-supported
  ball; both spontaneous and mechanically forced walking tested; brain imaged
  through the head capsule, not dissected
- **Source** — Aimon S, Cheng KY, Gjorgjieva J, Grunwald Kadow IC (2023)
  "Global change in brain state during spontaneous and forced walk in
  Drosophila is composed of combined activity patterns of different neuron
  classes." *eLife* 12:e85202. https://elifesciences.org/articles/85202
- **Confidence** — high (extracted directly from the paper). N = 16 flies
  for the pan-neuronal walk regression (12 nsyb + 4 GMR57C10); 58 flies
  total across genotypes for the main spontaneous walk/turn analysis; 26
  flies for forced-walk experiments; 84 adult female flies overall across the
  study

### T-WB-7  Neuromodulatory classes diverge: dopamine/octopamine rise with walk, serotonin selectively falls in one region

- **Quantity** — differential brain-wide response of dopaminergic,
  octopaminergic and serotonergic neuron populations to walking
- **Value** — dopaminergic (TH/DDC-Gal4) and octopaminergic (Tdc2-Gal4)
  populations were both broadly and strongly activated during walk, and not
  significantly different from each other (TH vs TDC: not significant).
  Serotonergic neurons (Trh-Gal4) were **significantly less** activated than
  either (Mann-Whitney, Bonferroni-adjusted p = 0.032 TH-vs-Trh, p = 0.040
  TDC-vs-Trh), and one specific component — **AVLPshell**, tentatively a
  serotonergic neuron of unknown identity in the anterior ventrolateral
  protocerebrum — showed a **clear decrease** in activity specifically at
  walk onset, the only region in the study with this sign
- **Type** — dynamic response
- **Method** — same light-field/GCaMP pipeline as T-WB-6, per-driver-line
  comparison; N = 11 flies (TH/DDC spontaneous, 5 forced), N = 7 (Tdc2
  spontaneous, 6 forced), N = 9 (Trh spontaneous, 6 forced)
- **Observation model** — a model with only one global "arousal" gain applied
  uniformly cannot reproduce this: it needs at least one population whose
  gain moves in the opposite direction from the rest during locomotion
- **Conditions** — same as T-WB-6
- **Source** — Aimon et al. 2023, eLife 85202 (as above)
- **Confidence** — high for the direction and significance values (extracted
  directly); the specific identity of AVLPshell as serotonergic is explicitly
  flagged by the authors themselves as speculative

### T-WB-8  Severing the brain-VNC connection abolishes walk-related brain activity (perturbation)

- **Quantity** — causal dependence of brain-wide walk-correlated activity on
  ascending input from the ventral nerve cord (VNC)
- **Value** — flies with the brain-VNC connection severed continued to walk
  on the treadmill but showed **"hardly any activity in the brain"** — in
  contrast to intact forced-walk controls, which showed the same robust
  brain-wide activation as spontaneous walk (cosine similarity between
  spontaneous and forced walk maps: 0.993 for R², 0.985 for regression
  coefficients, overall; 0.87/0.85 componentwise)
- **Type** — **perturbation**
- **Method** — surgical transection between brain and VNC, same light-field
  imaging pipeline as T-WB-6, comparing walk-locked brain activity with and
  without the connection intact
- **Observation model** — this is the strongest single result in this section
  for our purposes, per the README's own priority rule (perturbations outrank
  steady-state numbers): it says the brain-wide walk signal is not
  self-generated centrally, it is driven by signals ascending from the VNC
  (efference copy or proprioceptive reafference). A model that generates
  "walking-like" brain-wide activation from central drive alone, without an
  ascending input pathway, is reproducing the correlation without the cause
- **Conditions** — tethered, forced walk (ball rotated externally), adult
  female
- **Source** — Aimon et al. 2023, eLife 85202 (as above)
- **Confidence** — medium-high. The qualitative result ("hardly any
  activity") is a direct quote from the paper; we do not have the N for this
  specific transection experiment or an effect-size number beyond the
  qualitative description

### T-WB-9  High-speed (28-60 volumes/s) whole-brain imaging resolves sub-second, >1 Hz dynamics that slower imaging misses

- **Quantity** — brain-wide imaging speed sufficient to resolve fast sensory
  dynamics (single courtship-song pulses), and what is lost at conventional
  (slower) whole-brain rates
- **Value** — light beads microscopy (LBM) achieved **28 volumes/s** for the
  whole brain and **60 volumes/s** restricted to the central brain, extracting
  ~48,000 ROIs per brain (2,000 per plane over 24 planes). Mean activity
  tracked auditory pulse trains up to 5 Hz, and Fourier analysis showed
  **power at frequencies above 1 Hz only in the LBM data**, i.e. conventional
  (slower) whole-brain calcium imaging misses real, fast, brain-wide sensory
  dynamics that exist above ~1 Hz
- **Type** — dynamic response (methodological — establishes what temporal
  resolution is needed, using an auditory-evoked response as the test signal)
- **Method** — light beads microscopy, GCaMP6f pan-neuronal (nsyb-Gal4) for
  the main experiments, GCaMP8m for the higher-speed (60 Hz) experiments;
  courtship-song pulse playback as the stimulus
- **Observation model** — this sets a lower bound on the imaging rate our
  extractor needs to emulate if a comparison target ever uses this dataset or
  a similar one: subsampling below ~28-60 Hz for volumetric whole-brain
  imaging will itself remove real signal, independent of anything our model
  gets right or wrong
- **Conditions** — adult flies, tethered, auditory (courtship song) stimulus;
  small N — **3 animals at 28 Hz, 2 animals at 60 Hz** pulse-tracking
- **Source** — Gauthey W, Lin A, Ahmed OM, Leifer AM, Murthy M, Thiberge SY.
  "High-speed whole-brain imaging in Drosophila." bioRxiv 2025
  (10.1101/2025.06.18.660371); published as *Nature Communications* (2026),
  https://www.nature.com/articles/s41467-026-72437-1. PMID 40611904
- **Confidence** — medium-high for the rate/indicator numbers (extracted
  directly); low statistical power given N = 2-3 animals, noted by us, not
  necessarily by the authors as a limitation in the excerpt we obtained

### T-WB-10  An intrinsic (resting-state) functional network exists in the immobilized, non-behaving central brain

- **Quantity** — spontaneous, behaviour-independent functional connectivity
  between central-brain regions
- **Value** — **~27% of possible region-pair connections** showed
  significant correlation. Olfactory regions (antennal lobe, lateral horn,
  mushroom body) were the most interconnected; fan-shaped body and ellipsoid
  body showed connections across hemispheres. Reliability: mean **between-fly**
  correlation-matrix similarity R = 0.64 ± 0.01; **within-fly** (session-to-
  session) reliability R = 0.88 ± 0.03
- **Type** — steady-state
- **Method** — two-photon resonant scanning (Bruker Ultima, Leica 20x/1.0NA
  water immersion), **volume rate ≈ 1.91 Hz**, **GCaMP6m** ("kinetics best
  matched imaging rate" per the authors), correlating activity across
  atlas-registered regions
- **Observation model** — critical methodological point: **this is not a
  behaving fly.** Flies were cold-anaesthetized, then mechanically
  immobilized (nail polish on head/legs/wings), and the brain was dissected
  to expose the central neuropil (eyes and cuticle otherwise intact). This is
  a resting-state, reduced-preparation measurement, closer in spirit to
  resting-state fMRI than to T-WB-6's behaving-fly imaging. Do not treat this
  and T-WB-6 as the same kind of "brain state" — one is intrinsic/anaesthesia-
  adjacent connectivity, the other is behaviourally-driven, and they should
  not be pooled or expected to match
- **Conditions** — cold-anaesthetized then mechanically immobilized, brain
  dissected/exposed, not walking or otherwise behaving; N = 18 flies, 17 min
  per session, two sessions per fly
- **Source** — Mann K, Gallen CL, Clandinin TR (2017) "Whole-Brain Calcium
  Imaging Reveals an Intrinsic Functional Network in Drosophila." *Current
  Biology* 27:2389-2396. PMID 28756955.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5967399/
- **Confidence** — high (extracted directly from the paper, including the
  preparation details, which matter more than usual here)

---

## 3. Behavioural state as a perturbation (highest-value targets in this file)

### T-WB-11  Octopamine boosts visual-motion gain at flight onset — necessary and sufficient (perturbation)

- **Quantity** — change in visual-motion response of vertical-system (VS)
  wide-field motion-sensitive neurons between quiescence and flight, and the
  causal role of octopamine
- **Value** — VS cells show a **boost in response to visual motion during
  flight compared to quiescence**; at flight onset, VS cell baseline membrane
  potential (measured at the soma) **shifts upward rapidly**, and the
  amplitude of responses to large-field visual motion **increases**.
  Octopaminergic neurons that project to the optic lobes **increase their own
  activity during flight**. Bath-applied octopamine in *quiescent* flies
  reproduces the flight-like response boost. Genetic silencing/activation of
  octopamine neurons shows they are **both necessary and sufficient** for the
  flight-induced boost. We could not extract an exact fold-change or
  percentage for the gain increase itself from the sources accessible in this
  pass (paywalled full text); the qualitative result and the causal
  (necessity + sufficiency) structure are solid, the magnitude is a gap to
  fill by reading the primary figures before building an extractor target
  around a specific number
- **Type** — **perturbation** (genetic silencing/activation of octopamine
  neurons; also pharmacological)
- **Method** — intracellular recording of membrane potential at the VS cell
  body, in tethered flying vs quiescent flies; genetic manipulation of
  octopaminergic neurons (driver line and effector not confirmed in this
  pass — likely a Tdc2-Gal4-type driver with a temperature-sensitive
  silencer, standard for this lab at the time, but state this as inferred,
  not confirmed); pharmacological octopamine application as a positive
  control in quiescent flies
- **Observation model** — this is exactly the kind of target the README
  ranks highest: "silencing octopamine neurons removes the flight-induced
  visual gain boost" is a causal claim a global rescaling of our model cannot
  fake. Our model currently has exactly one behavioural state and no
  octopaminergic gain mechanism at all (theory-review.md, point 8) — this is
  the literature target that specific gap should eventually be checked
  against
- **Conditions** — adult, tethered flight vs quiescence, intact/awake prep,
  intracellular recording
- **Source** — Suver MP, Mamiya A, Dickinson MH (2012) "Octopamine neurons
  mediate flight-induced modulation of visual processing in Drosophila."
  *Current Biology* 22:2294-2302. https://pubmed.ncbi.nlm.nih.gov/23142045/
  (PMID 23142045)
- **Confidence** — high for the qualitative/causal claims (drawn from the
  paper's own abstract, quoted above); explicitly low/not-established for any
  specific magnitude, which we are flagging rather than guessing

### T-WB-12  Walking changes baseline activity and temporal tuning of T4 and its inputs Mi1, Tm3, Mi4, Mi9

- **Quantity** — behavioural-state-dependent change in baseline activity
  level and temporal-frequency tuning of the ON-pathway direction-selective
  neuron T4 and its presynaptic inputs Mi1, Tm3, Mi4, Mi9
- **Value** — behavioural state (walking vs. quiescent) alters **both the
  baseline activity level and the temporal tuning** of all five cell types;
  the effect is **"especially prominent" in Mi4**, the inhibitory
  (GABAergic) input to T4. We could not extract the specific percentage
  change in baseline or the specific shift in corner/preferred temporal
  frequency (Hz) from the sources accessible in this pass (PNAS full text
  and PMC copy both blocked in this session — paywall/bot-check); treat the
  existence and direction (Mi4 most affected) as established and the
  magnitude as a gap
- **Type** — steady-state / dynamic response (baseline shift = steady-state;
  temporal-tuning shift = dynamic response)
- **Method** — almost certainly two-photon calcium imaging of medulla
  interneurons in a head-fixed fly walking on an air-supported ball, given
  the lab and the standard method for this exact cell population at the time
  (T4/Mi1/Tm3/Mi4/Mi9 are not accessible to patch clamp in the medulla at the
  throughput this experiment needs) — **but we did not independently confirm
  the indicator, frame rate, or exact behavioural monitoring method from the
  primary text in this session.** This must be verified before an extractor
  is built against this target; do not assume GCaMP6f/two-photon without
  checking
- **Observation model** — n/a until the method is confirmed
- **Conditions** — adult, head-fixed, walking vs. quiescent on a ball;
  species/sex/age not confirmed in this pass
- **Source** — Strother JA, Wu ST, Rogers EM, Eliason JLM, Wong AM, Nern A,
  Reiser MB (2018) "Behavioral state modulates the ON visual motion pathway
  of Drosophila." *PNAS* 115(1):E102-E111.
  https://www.pnas.org/doi/full/10.1073/pnas.1703090115 (PMID 29255026)
- **Confidence** — medium for the qualitative claim (consistent across the
  PubMed abstract and multiple independent secondary summaries); low for
  every methodological detail beyond "behavioural state was manipulated and
  measured" — flagged explicitly rather than filled in from convention

### T-WB-13  Octopamine input to Mi4 is required specifically for fast-motion responses in walking flies (perturbation)

- **Quantity** — causal role of octopaminergic input to Mi4 in the
  behavioural-state effect above
- **Value** — central octopaminergic neurons synapse onto Mi4 and **increase
  its excitability**; octopamine neurons are **required for sustained
  behavioural responses to fast-moving, but not slow-moving, visual stimuli**
  in walking flies — i.e. the necessity is temporal-frequency-specific, not a
  blanket effect on all motion responses
- **Type** — **perturbation**
- **Method** — genetic silencing of octopaminergic neurons combined with
  behavioural (optomotor) readout in walking flies, stimuli varied in
  temporal frequency; exact effector/driver not confirmed in this pass (same
  caveat as T-WB-12)
- **Observation model** — like T-WB-11, this is a perturbation with a
  frequency-specific signature, which is a much sharper test than "does gain
  go up" — a model that gets a flat gain increase for all temporal
  frequencies would fail this even if its average gain change were right
- **Conditions** — same as T-WB-12
- **Source** — Strother et al. 2018, PNAS 115(1):E102-E111 (as above)
- **Confidence** — medium. The claim is a direct paraphrase of the paper's
  own abstract/summary language, so the existence and direction of the effect
  is solid; magnitude and full method are not confirmed (see T-WB-12)

---

## 4. Excitation/inhibition balance and network stability

### T-WB-14  In vivo resting Vm of central neurons, and a systematic recording artefact to correct for

- **Quantity / Value / Method / Source** — identical dataset to T-WB-2
  (Gouwens & Wilson 2009): PN resting potential -47.8 ± 1.6 mV whole-cell vs.
  -57.8 ± 1.5 mV cell-attached, N = 12, ~10 mV attributed to seal-conductance
  artefact in whole-cell mode
- **Type** — steady-state
- **Observation model** — flagged separately here because it generalizes
  beyond PNs: **any in vivo whole-cell Vm measurement in a small Drosophila
  central neuron should be assumed ~10 mV more depolarized than the true
  resting potential**, per this paper's own explanation of the mechanism
  (seal conductance in a high-input-resistance cell). This matters directly
  for our own operating-point work: if we ever calibrate a target "resting
  potential" from a whole-cell paper without this correction, we will set our
  model's baseline too depolarized, which pushes directly against the exact
  problem (`lab-notebook.md`) of getting cells to sit the right distance from
  threshold
- **Conditions** — see T-WB-2
- **Confidence** — high for the two numbers and the mechanism; this is a
  methodological point rather than a new empirical claim

### T-WB-15  Projection neurons are described as resting close to spike threshold — no brain-wide fluctuation-width number found

- **Quantity** — how far, in fluctuation units, central neurons sit from
  spike threshold at rest (directly comparable to our own "gap/sd" measure
  in `lab-notebook.md`, where we found 4.0 in the unbalanced regime and
  1.2-1.9 in the balanced regime)
- **Value** — the qualitative characterization in the literature on
  antennal-lobe PNs (Kazama & Wilson's body of work on this circuit) is that
  PNs rest close to spiking threshold, consistent with a fluctuation-driven
  rather than mean-driven regime — the same picture our own balanced fit
  converges on. **We did not find a quantified "distance to threshold in
  units of membrane-potential SD" figure for any Drosophila central neuron
  type.** That specific number — the one most directly comparable to our own
  measurement — appears not to exist in a form we could locate
- **Type** — steady-state
- **Method** — in vivo patch clamp (see T-WB-2); the "near threshold"
  characterization is qualitative in the sources we found
- **Observation model** — our own gap/sd = 1.2-1.9 (balanced regime) vs. 4.0
  (unbalanced regime) number has no published fly value to be checked
  against directly. This is worth stating plainly rather than implying a
  comparison exists: van Vreeswijk & Sompolinsky-style balanced-network
  theory (already cited in theory-review.md) predicts this regime on
  theoretical grounds, and single-cell physiology is qualitatively
  consistent with it, but nobody has published the number that would let us
  fit to it quantitatively
- **Conditions** — see T-WB-2
- **Source** — qualitative characterization attributed to Kazama H, Wilson RI
  (2008) "Homeostatic matching and nonlinear amplification at identified
  central synapses." *Neuron* 60:766-777, and/or Kazama H, Wilson RI (2009)
  "Origins of correlated activity in an olfactory circuit." *Nat Neurosci*
  — we were not able to pin the exact claim to one paper with a page/figure
  reference in this pass
- **Confidence** — low. This entry exists mainly to record that we looked
  for the one number that would map most directly onto our own balance
  measurement, and did not find it — that absence is itself the useful
  result

### T-WB-16  Avalanche/criticality dynamics — not measured in any insect

- **Quantity** — whether spontaneous or evoked activity in an insect nervous
  system shows the power-law avalanche statistics associated with the
  "critical brain" hypothesis
- **Value** — **not measured.** A dedicated search for avalanche/criticality
  studies in Drosophila, other insects (locust, honeybee), or any
  invertebrate nervous system found none. The entire avalanche/criticality
  literature we could locate is vertebrate or in vitro: cultured cortical
  and hippocampal neurons, anaesthetized rat cortex, awake monkey cortex,
  zebrafish, and human EEG (classic exponents: avalanche size ~-1.5,
  duration ~-2, Beggs & Plenz-style). We found general theoretical
  literature on criticality and self-organized criticality, and one
  methodological debate about whether power-law avalanches actually imply
  criticality at all — but nothing applying either the measurement or the
  debate to an insect nervous system
- **Type** — steady-state (diagnostic on spontaneous dynamics)
- **Method** — n/a — this is the gap
- **Observation model** — this exactly matches our own theory-review.md
  point 7: avalanche statistics are "nearly free" for us to compute (we
  already record every spike) and would be a model-internal sanity check on
  whether the operating point is dead, saturated, or plausible — but there is
  no insect measurement to fit *to*. This is a diagnostic we can only ever
  check for internal consistency (does our own network's avalanche
  statistics change sensibly across the parameter sweep we've already run in
  `criticality.py`?), not a target we can validate against real data, until
  someone measures it in an insect. Worth being explicit that our earlier
  branching-ratio estimate (`lab-notebook.md`, "worthless" result) was a
  different, confounded measurement of the same general idea, not evidence
  against trying a proper avalanche-size/duration analysis
- **Conditions** — n/a
- **Source** — absence claim from a targeted search (September 2026);
  general (non-insect) criticality literature surveyed for context only,
  not cited as fly data
- **Confidence** — high for the absence claim in insects specifically; the
  general vertebrate criticality literature is large and we did not attempt
  to be exhaustive about it since it is out of scope for a fitting target

---

## 5. Seizure and hyperexcitability as a perturbation target

### T-WB-17  para-bss1: a gain-of-function point mutation in the voltage-gated sodium channel

- **Quantity** — molecular mechanism of the para-bss1 ("bang senseless")
  allele
- **Value** — a **point mutation causing L1699F**, in the paddle motif of
  the S3b segment of homology domain IV of the *para* voltage-gated sodium
  channel. This is a **gain-of-function** change that alters the
  voltage-dependence of channel **inactivation** (shown by heterologous
  expression and voltage-clamp of the mutant channel), making neurons more
  excitable. Described as the most severe and lowest-threshold of the
  bang-sensitive mutant series, and its seizures are reported to resist
  pharmacological (anti-epileptic drug) suppression more than other
  bang-sensitive genotypes — offered by the authors as a model of
  pharmacologically-resistant human epilepsy
- **Type** — steady-state (describes a constitutive channel property, not a
  single perturbation event)
- **Method** — molecular genetics (mutation mapping) plus heterologous
  expression and voltage-clamp electrophysiology of the mutant channel
- **Observation model** — n/a directly (this is a channel-property target,
  useful if we ever model channel kinetics explicitly rather than
  point-neuron thresholds)
- **Conditions** — heterologous expression system for the channel
  biophysics; whole-animal phenotype separately characterized in vivo (see
  T-WB-18/19)
- **Source** — Parker L, Padilla M, Du Y, Dong K, Tanouye MA (2011)
  "Drosophila as a Model for Epilepsy: bss Is a Gain-of-Function Mutation in
  the Para Sodium Channel Gene That Leads to Seizures." *Genetics*
  187(2):523-534. https://academic.oup.com/genetics/article/187/2/523/6063291
- **Confidence** — high for the molecular description; medium for the
  "resists pharmacological suppression more than other bang-sensitive
  mutants" comparative claim (paraphrased from the paper, not seen as a
  primary data table in this pass)

### T-WB-18  para-bss1 electroconvulsive seizure threshold: ~90% lower than wild-type

- **Quantity** — brain-stimulation voltage threshold to trigger the
  stereotyped seizure discharge, measured via DLM (dorsal longitudinal
  muscle, an indirect flight muscle in the giant-fiber pathway) recording
- **Value** — wild-type (Canton-S) seizure threshold **≈ 30 V** high-frequency
  stimulation (HFS); para-bss1 **≈ 3 V** HFS — roughly a **90% reduction**.
  Each genotype has its own characteristic/signature threshold voltage. This
  is corroborated by an independent-looking number from FlyBase's allele
  report (3.2-3.7 V induction threshold for para-bss1), which is consistent
  with, though not necessarily independent of, the ~3 V figure
- **Type** — dynamic response (threshold measurement) / directly usable as a
  **perturbation** target if we implement a para-bss1-like channel change and
  ask whether our model's own seizure threshold drops comparably
- **Method** — high-frequency electrical stimulation (HFS) delivered
  directly to the brain via electrode, response read out via intracellular
  recording from the DLM (dorsal longitudinal indirect flight muscle),
  innervated by the well-characterized giant-fiber pathway; threshold defined
  as the stimulus intensity that reliably triggers the stereotyped seizure
  discharge
- **Observation model** — our model has no muscle or motor output layer, so
  this cannot be replicated literally; the usable part of this target is the
  **relative** threshold reduction (an ~order-of-magnitude drop in the
  stimulus needed to trigger runaway activity), which maps onto "how much do
  we have to perturb excitability before our network's own operating point
  tips into saturation" — a question our `fit_weight.py`/`balance.py` sweeps
  already probe from the other direction
- **Conditions** — adult, tethered, in vivo brain stimulation
- **Source** — Kuebler D, Tanouye MA (2000) "Modifications of seizure
  susceptibility in Drosophila." *J Neurophysiol* 83(2):998-1009
- **Confidence** — medium-high. The ~30 V / ~3 V / ~90% figures come from a
  secondary summary of the paper (direct full-text fetch was blocked by the
  publisher in this session), cross-checked against a FlyBase-reported number
  in the same range; we were not able to read the primary table ourselves

### T-WB-19  para-bss1 mechanical (vortex) bang-sensitivity: recovery time and refractory period

- **Quantity** — recovery time from vortex-induced seizure paralysis, and
  the subsequent refractory period, for para-bss1 homozygotes and
  heterozygotes
- **Value** — homozygote recovery **≈ 240 s**; heterozygote recovery
  **≈ 50 s** (semidominant: >95% of heterozygotes show some bang-sensitive
  phenotype, ~2/3 are bang-sensitive at room temperature); refractory period
  (time before the fly can be induced into a second seizure) **≈ 600 ± 70 s**
- **Type** — dynamic response
- **Method** — mechanical bang assay: vortexing flies for ~10 s, timing
  recovery of normal posture/mobility by eye or video
- **Observation model** — this is a **different measurement protocol** from
  T-WB-18 (mechanical vortex vs. electrical brain stimulation) even though
  both are called "seizure threshold/severity" informally — do not conflate
  them when deciding what our extractor needs to reproduce. The vortex assay
  measures whole-animal behavioural recovery time, several steps downstream
  of any central firing-rate quantity our model produces
- **Conditions** — adult, room temperature (semidominance is
  temperature-sensitive per the source), whole-animal behavioural assay
- **Source** — FlyBase allele report for Dmel\para[bss1] (FBal0001325),
  https://flybase.org/reports/FBal0001325, drawing on Parker et al. 2011
  (as above) and related literature curated by FlyBase
- **Confidence** — medium. FlyBase curation is generally reliable but we are
  citing the aggregated allele report rather than having independently
  traced each number to its original primary source table

### T-WB-20  Relative seizure severity across bang-sensitive mutants (vortex assay)

- **Quantity** — ranked seizure duration across bang-sensitive genotypes,
  same assay, same source
- **Value** — vortex-assay seizure duration: **para-bss1 (bss) 168.4 ± 11.0 s
  > easily shocked (eas) 107.7 ± 8.9 s > jus 73.6 ± 3.9 s > pk-sple ≈ 15.2 s
  > wild-type ≈ 0.2 ± 0.1 s**. All differences are large relative to their
  reported spreads
- **Type** — steady-state (comparative phenotype severity)
- **Method** — vortex/bang mechanical assay, recovery time defined as time
  to regain posture and mobility
- **Observation model** — useful as a ranked severity scale if we ever
  implement more than one hyperexcitability mutation in the model and want
  to check that their relative severity, not just their existence, comes out
  right
- **Conditions** — adults, room temperature, whole-animal assay
- **Source** — table compiled in "Characterization of Seizure Induction
  Methods in Drosophila," *eNeuro* 8(4):ENEURO.0079-21.2021.
  https://www.eneuro.org/content/8/4/ENEURO.0079-21.2021 (itself citing the
  primary genetic literature for each mutant)
- **Confidence** — medium. This is a secondary compilation; we did not trace
  each individual number back to its original primary paper in this pass

### T-WB-21  easily shocked (eas): a membrane-lipid pathway mutation causing giant-fiber pathway failure

- **Quantity** — mechanism and physiological phenotype of the easily shocked
  mutant
- **Value** — *eas* disrupts **ethanolamine kinase**, required for
  phosphatidylethanolamine synthesis — a membrane phospholipid pathway, not
  a channel gene directly. Electrophysiological recording from the giant
  fiber pathway (flight muscle output) shows that electrical induction
  produces a brief seizure discharge followed by **failure of the muscle to
  respond to giant-fiber stimulation** — i.e. the phenotype is a
  seizure-then-conduction-failure, not sustained hyperexcitability alone.
  Bang sensitivity here is attributed to an excitability defect from altered
  membrane lipid composition rather than a direct channel gating change
- **Type** — steady-state (constitutive mutant phenotype) with a dynamic
  seizure-then-failure response under stimulation
- **Method** — electrophysiological recording from DLM/giant-fiber pathway
  under electrical brain stimulation, same general paradigm as T-WB-18
- **Observation model** — the seizure-then-failure signature (not just
  "fires more") is a second reminder, alongside T-WB-23 below, that a real
  fly seizure phenotype is a specific temporal pattern (discharge, then
  failure, then recovery, then refractory period), not simply elevated
  steady-state firing
- **Conditions** — adult, in vivo, giant-fiber pathway stimulation/recording
- **Source** — Pavlidis P, Ramaswami M, Tanouye MA (1994) "The Drosophila
  easily shocked gene: a mutation in a phospholipid synthetic pathway causes
  seizure, neuronal failure, and paralysis." *Cell* (PMID 7923374)
- **Confidence** — medium-high for the mechanism (ethanolamine kinase, lipid
  pathway) and the seizure-then-failure description; drawn from secondary
  summaries rather than the primary Cell paper directly in this pass

### T-WB-22  DLM/giant-fiber discharge classification: Type I and Type II seizure spike rates vs. normal flight/grooming motor pattern

- **Quantity** — spike-frequency signature of electroconvulsive seizure
  discharge in the DLM/giant-fiber system, classified into named types, and
  compared to normal motor patterns
- **Value** — normal flight bouts coincide with regular DLM spike activity
  around **8-10 Hz**, with tonic ~5 Hz firing described elsewhere as
  sufficient to sustain oscillatory flight-muscle Ca²⁺ influx. Seizure
  discharge is classified into two types: **Type I** — trains at
  **~10-30 Hz**, lacking clear pattern, terminating abruptly; **Type II** —
  bursts that **increase in frequency while decreasing in amplitude** within
  each burst, with burst-internal rates reported up to **~100 Hz** and
  activity near the end of a seizure episode reaching **~150 Hz**
- **Type** — dynamic response
- **Method** — intracellular/extracellular recording from DLM (indirect
  flight muscle, giant-fiber pathway) during (a) natural flight/grooming
  behaviour and (b) electroconvulsive-stimulus-triggered seizure; spike
  pattern analysis (firing frequency, inter-spike-interval statistics,
  cross-fiber timing) used to distinguish discharge types
- **Observation model** — **this is the most directly useful number in this
  file for the specific question we were asked to help answer** ("does our
  saturated state resemble a real seizure phenotype"): it gives a
  quantitative Hz comparison between normal motor-linked firing (~5-10 Hz)
  and seizure discharge (~10-30 Hz sustained, up to ~100-150 Hz in bursts).
  Two caveats before using it directly: (1) this is a muscle/motor-neuron
  readout in the giant-fiber pathway, not a central-brain interneuron rate —
  it is downstream of whatever central seizure activity caused it, so the
  mapping to "what should our central LIF neurons be doing" is indirect; (2)
  the defining feature of Type II discharge is a *changing* rate within a
  burst (accelerating, then failing), which a model that simply saturates to
  a constant ceiling rate would not reproduce even if the ceiling rate itself
  were in the right range — see T-WB-23, the same point applies more
  strongly there
- **Conditions** — adult, tethered, in vivo; both natural behaviour and
  electroconvulsive-stimulus conditions on the same prep
- **Source** — Lee J, Iyengar A, Wu CF (2019) "Distinctions among
  electroconvulsion- and proconvulsant-induced seizure discharges and native
  motor patterns during flight and grooming: quantitative spike pattern
  analysis in Drosophila flight muscles." *J Neurogenetics* 33(2):125-142
  (preprint bioRxiv 10.1101/481234); classification scheme originates with
  Lee S, Wu CF (2002) "Electroconvulsive Seizure Behavior in Drosophila:
  Analysis of the Physiological Repertoire Underlying a Stereotyped Action
  Pattern in Bang-Sensitive Mutants." *J Neurosci* 22(24):11065-11079; flight
  motor pattern numbers from Iyengar A, Wu CF (2014) "Flight and seizure
  motor patterns in Drosophila mutants: simultaneous acoustic and
  electrophysiological recordings of wing beats and flight muscle activity."
  *J Neurogenetics* 28(3-4):316-328
- **Confidence** — medium. The Hz figures were retrieved via aggregated
  search-engine extraction across these three related papers rather than a
  single directly-fetched primary source (direct PDF/HTML fetches of all
  three were blocked by rate-limiting or 403s in this session); the
  Type I/Type II qualitative classification and its attribution to Lee & Wu
  2002 is our best-confidence read of a consistent naming scheme across
  sources, but the exact numbers should be re-checked against the primary
  papers before being used as a hard fitting target

### T-WB-23  Brain-wide local field potential (LFP) signature of seizure is patterned and genotype/drug-specific, not just "everything fires more"

- **Quantity** — brain-wide local field potential recorded during
  electroconvulsive seizure in behaving tethered flies, compared across rest,
  flight, a sodium-channel gain-of-function mutant (para-bss1), and a
  pharmacological convulsant (picrotoxin, a GABA-A blocker)
- **Value** — electroconvulsive-stimulus (ECS) seizures produce
  **large-amplitude LFP oscillations with a stereotyped temporal correlation
  to DLM (flight muscle) spiking**, clearly distinct in pattern from both
  rest-associated and flight-associated LFP. In the **para-bss1** mutant, the
  LFP pattern is **prolonged**, and the temporal correlation between LFP
  oscillations and DLM discharge is **altered** relative to wild-type — i.e.
  the genotype changes the *pattern* of the seizure signature, not only its
  duration. Under **picrotoxin** (GABA-A blockade, a different route to
  hyperexcitability than the sodium-channel route), the LFP shows a
  **qualitatively different** signature: a **slow, ~1 Hz, repetitive
  waveform**, tightly coupled to DLM bursting and behavioural spasms
- **Type** — **perturbation** (genetic: para-bss1; pharmacological:
  picrotoxin) with brain-wide ensemble readout
- **Method** — local field potential (LFP) electrode(s) in the brain of
  behaving tethered flies, recorded simultaneously with DLM
  (flight-muscle/giant-fiber) spiking, across rest, flight, and
  electroconvulsive-stimulus-triggered seizure conditions; compared across
  genotype (wild-type vs. para-bss1) and pharmacology (picrotoxin)
- **Observation model** — **this is the key finding for the question we were
  asked to help answer.** A real fly seizure, measured at brain scale, is not
  "uniform maximal firing everywhere" — it is a specific, patterned,
  oscillatory ensemble state whose *shape* depends on which mechanism caused
  it (sodium-channel gain-of-function gives a different LFP-DLM coupling
  pattern than GABA-A blockade does). If our model saturates under some
  parameter settings, the honest comparison is not "is the rate high" but
  "does the saturated state show a comparable oscillatory, tightly-coupled,
  mechanism-specific structure" — and a point-neuron LIF network with no
  oscillatory mechanism built in has no obvious way to produce the ~1 Hz
  picrotoxin-like waveform or the prolonged-but-still-patterned para-bss1-like
  waveform. A flat, unpatterned ceiling-rate saturation is arguably **more
  different** from either measured seizure signature than it is similar to
  either — that is a usable, falsifiable statement, not just a caveat
- **Conditions** — adult, tethered, behaving (rest/flight) and
  stimulus-triggered seizure conditions, in vivo brain LFP
- **Source** — Iyengar A, Wu CF (2021) "Fly seizure EEG: field potential
  activity in the Drosophila brain." *J Neurogenetics* 35(3), published
  online 2021 Jul 18 (PMID 34278939)
- **Confidence** — high for the qualitative structure of the finding
  (extracted directly from the paper's own abstract, quoted/paraphrased
  above); no N or effect-size numbers were available from the abstract alone,
  so this target currently supports a qualitative ("patterned vs.
  unpatterned") comparison, not a quantitative fit

---

## Summary: what's usable now, and what is honestly missing

**Solid enough to fit to directly:**
- Whole-brain calcium-imaging methodology and its headline numbers (T-WB-6
  through T-WB-10) — imaging rates, indicators, and the ~20% variance-
  explained figure are all extracted from primary text.
- The brain-VNC transection result (T-WB-8) and the LFP seizure-signature
  result (T-WB-23) — both are perturbations with clear qualitative structure,
  which the README correctly ranks above steady-state numbers.
- para-bss1's ~90% electroconvulsive threshold reduction (T-WB-18) and the
  Type I/II discharge frequency ranges (T-WB-22), with the stated caveats
  about what they don't measure (central rates, as opposed to motor output).

**Real, but only qualitative — magnitude is a follow-up task, not a gap in
our search:**
- Both behavioural-state perturbation targets named in the brief (T-WB-11,
  T-WB-12/13) are solidly established as directional, causal findings but we
  could not extract effect sizes from the accessible text (paywalls/bot-checks
  on Cell Press, PNAS, and PMC all blocked full-text access in this session).
  Reading the actual figures in these two papers is probably the single
  highest-value follow-up action from this whole file, given the brief calls
  them the highest-priority targets.

**Genuinely thin or absent — not a search failure, a fact about the field:**
- **A brain-wide firing-rate distribution does not exist** (T-WB-1). Nobody
  has it, including the one directly comparable whole-CNS connectome model
  (T-WB-5). Any operating-point target for "what fraction of neurons should
  be active" will have to be justified from balanced-network theory and
  scattered per-cell-type physiology (T-WB-2 through T-WB-4), not from a
  measured distribution — and that should be said explicitly wherever this
  gets used, not quietly assumed.
- **No fluctuation-width/distance-to-threshold number exists** for any fly
  central neuron (T-WB-15), which is frustrating given it's exactly the
  quantity our own balanced-fit work (`lab-notebook.md`) already measures
  internally — we have a model number with no animal number to check it
  against.
- **No avalanche/criticality measurement exists in any insect** (T-WB-16).
  The diagnostic is cheap for us to run on our own model (as theory-review.md
  already proposes) but it can only ever be an internal consistency check
  until someone measures it in a real insect brain.
