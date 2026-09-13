# Escape circuit, descending neurons, and the VNC motor system

Scope: our connectome is the male CNS and includes the full nerve cord — 708
motor neurons, 13,161 VNC intrinsic neurons, 1,314 descending neurons, and
1,846 ascending neurons — and up to now nothing in our modelling has touched
any of them. This file collects fitting targets for three overlapping areas:
the Giant Fiber (GF) escape circuit, descending neurons that drive specific
identified behaviours, and the leg motor system (recruitment, rates, gait
timescales).

**Why the Giant Fiber pathway matters most for us specifically:** our model
(`src/params.py`, per `shiu-predictions.md`) applies one fixed axonal delay,
`t_dly = 1.8 ms`, to every connection in the brain regardless of synapse
count, transmitter, or path length. The GF escape pathway is the one place
in the fly where the anatomy of a multi-synapse path is completely solved
(GF → TTMn is monosynaptic and mixed electrical/chemical; GF → DLMn is
disynaptic via the PSI, the "peripherally synapsing interneuron") and the
end-to-end latency has been measured directly by electrical stimulation.
That makes it close to a ground-truth test of the fixed-delay assumption.
The short version of what we found (detailed in §1 below): **measured
end-to-end latencies for both the 1-synapse and 2-synapse paths are
themselves smaller than the model's single fixed per-connection delay** —
which is a direct, quantitative problem for `t_dly = 1.8 ms` if taken
literally as "conduction + synaptic delay per hop," not just a rough
average.

Abbreviations used throughout: GF = Giant Fiber (also called GFN, DNp01 in
connectome nomenclature); TTMn = tergotrochanteral ("jump") motor neuron;
TTM = tergotrochanteral muscle; DLMn = dorsal longitudinal (flight) muscle
motor neuron; DLM = dorsal longitudinal muscle; PSI = peripherally
synapsing interneuron (relays GF → DLMn); MDN = moonwalker descending
neuron; VPN = visual projection neuron.

**Perturbations and latencies are listed first in every section**, per this
repository's stated priority that causal manipulations outrank steady-state
numbers.

---

## 1. The Giant Fiber escape pathway — conduction, synaptic delay, latency

### T-MOT-1  GF → TTM (jump muscle) stimulation-to-response latency

- **Quantity** — latency from electrical stimulation of the GF (at the
  brain/cervical connective) to the evoked response in the tergotrochanteral
  ("jump") muscle, via the monosynaptic, mixed electrical/chemical
  GF–TTMn synapse
- **Value** — **1.46 ± 0.02 ms**
- **Type** — dynamic response (direct-stimulation latency)
- **Method** — extracellular/intracellular stimulation of the GF and
  recording of the muscle (or motor neuron) response; classic
  stimulate-and-record giant-fiber physiology preparation
- **Observation model** — define t=0 as the simulated GF spike time at the
  stimulation site; measure time to first depolarization/spike in the
  simulated TTMn or TTM; compare directly against this value. No
  filtering/thresholding subtlety beyond spike-time detection since this is
  a single-trial-averaged electrophysiological latency, not an imaging
  signal.
- **Conditions** — adult *Drosophila melanogaster*, in vivo stimulation
  preparation; temperature **not stated in the abstract retrieved this
  session** (see gap note in §6); sex not confirmed this session
- **Source** — Trimarchi JR, Schneiderman AM (1993). Giant fiber activation
  of an intrinsic muscle in the mesothoracic leg of *Drosophila
  melanogaster*. J Exp Biol. PMID 8486998.
  <https://pubmed.ncbi.nlm.nih.gov/8486998/>
- **Confidence** — medium. The number itself is a precise, tight-SEM
  electrophysiological measurement (high confidence as reported), but see
  **conflict with T-MOT-2** below — a different, more recent measurement of
  what should be a comparable GF→TTM latency gives a substantially smaller
  value (0.93 ms) in young flies. We could not resolve this from abstracts
  alone.

### T-MOT-2  GF → TTM and GF → DLM latency, young vs. aged flies (and the model's own delay decomposition)

- **Quantity** — latency from GF stimulation to (a) TTM response via the
  monosynaptic path, and (b) DLM response via the disynaptic
  GF→PSI→DLMn path, measured in young vs. aged flies, feeding a
  compartmental computational model of the pathway
- **Value** — **TTM: 0.93 ms (young) vs 1.22 ms (old)**; **DLM: 1.44 ms
  (young) vs 1.85 ms (old)**. Model components used to reproduce these:
  neuromuscular-junction delay 0.35 ms; chemical synapse delay at
  PSI→DLMn 0.15 ms (rise time constant 0.1 ms, decay time constant 1 ms);
  gap-junction conductance at the electrical synapse drops from 135 µS
  (young) to 34.5 µS (old, ≈75% reduction) — this decline, not a change in
  axonal conduction per se, is presented as the main driver of the
  age-related latency increase. The paper explicitly does **not** decompose
  out a separate pure axonal-conduction delay or separate the GF–TTMn vs
  GF–PSI synaptic delays from each other — the 0.93–1.85 ms figures are
  end-to-end (stimulation-to-muscle-response) latencies.
- **Type** — dynamic response (latency), with an embedded perturbation
  (biological aging, i.e. comparing young vs old flies as the manipulated
  variable)
- **Method** — direct electrophysiological stimulation/recording (same
  paradigm as T-MOT-1) used to fit and validate a Hodgkin-Huxley-style
  compartmental circuit model of the GF/PSI/TTMn/DLMn pathway
- **Observation model** — as T-MOT-1; additionally, if modelling the aging
  comparison, the observable is the ~0.3–0.4 ms latency increase with age,
  attributable in this source specifically to gap-junction conductance
  loss rather than conduction velocity change
- **Conditions** — adult *D. melanogaster*; "young" vs "old" defined by the
  source paper (exact ages in days not extracted this session — see gap
  note); **no recording temperature is stated in the paper** (confirmed
  absent from the full text, not just an extraction miss); GF activation
  modelled with a 120 nA / 0.03 ms current pulse at the proximal GF (a
  model input choice, not necessarily the literal experimental threshold)
- **Source** — Augustin H, Zylbertal A, Partridge L (2019). A Computational
  Model of the Escape Response Latency in the Giant Fiber System of
  *Drosophila melanogaster*. eNeuro. PMID 31001574, PMC6469880.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6469880/>
- **Confidence** — medium-high for the internal young/old comparison
  (this is the paper's central, carefully controlled result); **medium and
  flagged as conflicting** against T-MOT-1 for the absolute GF→TTM value —
  0.93 ms (young, this source) vs 1.46 ms (Trimarchi & Schneiderman 1993).
  A ~0.5 ms discrepancy in a pathway this fast is not trivial; possible
  causes include different fly ages/genotypes, different definitions of
  "response onset," or genuine temperature differences between labs, none
  of which we could confirm this session. **Record both values; do not
  average them into a single tight target.**

**Synthesis relevant to `t_dly = 1.8 ms`:** taking either source at face
value, the total measured latency for a *monosynaptic* GF path (0.93–1.46
ms) is already smaller than the model's single fixed per-connection delay,
and the *disynaptic* path (1.44–1.85 ms, one extra chemical synapse) adds
only on the order of 0.4–0.5 ms for the additional hop — not another 1.8 ms.
If this generalizes, it suggests `t_dly` is not simply too small or too
large on average, but structurally wrong in shape: real synaptic delay
increments are much smaller than real axonal-conduction-dominated
first-hop latency, whereas the model currently charges the same flat cost
for both.

### T-MOT-3  GF axon conduction velocity increases ~80% during the first day of adult life

- **Quantity** — axonal action-potential conduction velocity of the GF
  interneuron, measured across early adult maturation
- **Value** — increases by **~80%** during the first 24 hours of adult life
  (exact m/s values not extracted this session — see gap note); GF axon
  diameter ≈ **7 µm**
- **Type** — dynamic response / developmental perturbation (age is the
  manipulated variable)
- **Method** — intracellular recording of GF axonal action potentials at
  two points to derive conduction velocity, in newly eclosed vs 1-day-old
  adults; pharmacological/genetic dissection of contributing channels
- **Observation model** — velocity, not latency, so comparison requires
  knowing our model's effective axon length for the GF to convert to a
  delay; we do not have that length calibrated in `src/params.py` currently
- **Conditions** — adult *D. melanogaster*, 0 vs ~24 h post-eclosion;
  requires functional Para (voltage-gated Na⁺), Shaker (Kv1), L-type-like
  Ca²⁺, and Slowpoke (BK) channels; temperature not extracted this session
- **Source** — Kadas D, Duch C, Consoulas C (2019). Postnatal Increases in
  Axonal Conduction Velocity of an Identified *Drosophila* Interneuron
  Require Fast Sodium, L-Type Calcium and Shaker Potassium Channels.
  eNeuro. PMID 31253715. <https://pubmed.ncbi.nlm.nih.gov/31253715/>
- **Confidence** — medium; a relative (%) change, not an absolute velocity,
  and we did not fetch the full text this session to get the raw m/s
  numbers that presumably exist in it.

### T-MOT-4  GF conduction velocity is comparatively very slow (relative benchmark, not absolute)

- **Quantity** — comparison of mature GF axon conduction velocity to
  vertebrate myelinated sensory (Aβ) axons
- **Value** — GF conduction is **20–60× slower** than vertebrate Aβ
  sensory axons (qualitative/comparative statement only; no absolute m/s
  value extracted this session)
- **Type** — steady-state (species/axon-class comparison)
- **Method** — as T-MOT-3
- **Observation model** — not directly usable as a fitting target without
  an absolute number; included so the range is not lost, and as a sanity
  check that GF, despite being the fly's largest-diameter CNS axon, is not
  "fast" by vertebrate myelinated standards — consistent with a fly-wide
  connectome having no myelin
- **Conditions** — as T-MOT-3
- **Source** — same as T-MOT-3 (Kadas, Duch, Consoulas 2019)
- **Confidence** — low as a quantitative target (comparative statement
  only); flagged as a gap to fill from the full text if this pathway
  becomes a hard modelling target.

### T-MOT-5  ShakB null mutation eliminates the electrical (not chemical) component of the GF–TTMn synapse

- **Quantity** — effect of a *shakB* null mutation on the mixed
  electrical/chemical GF output synapse; gap-junction ultrastructural
  spacing
- **Value** — *shakB* null **eliminates electrical transmission but spares
  chemical transmission** at the GF–TTMn synapse (a clean double
  dissociation of the two components). Two membrane-separation values are
  reported in the source, **3.25 ± 0.12 nm** and **1.41 ± 0.08 nm**,
  alongside "41 nm vesicles" (consistent with the chemical-synapse
  component); this session's extraction could not confirm with certainty
  which of the two spacing values corresponds to wild-type gap junction vs.
  which structure in the mutant — **flagged for full-text verification
  before use**
- **Type** — perturbation (genetic null mutant)
- **Method** — dye-coupling/electrophysiology to demonstrate loss of
  electrical coupling; electron microscopy for membrane-spacing and
  vesicle measurements
- **Observation model** — binary/structural target: does the simulated
  GF→TTMn connection, if split into separate electrical and chemical
  sub-components, reproduce a mutant condition where only the chemical
  component survives silencing of gap-junction conductance
- **Conditions** — adult *D. melanogaster*, *shakB* null allele vs.
  wild-type comparison
- **Source** — Phelan P, et al. (1999). Null mutation in shaking-B
  eliminates electrical, but not chemical, synapses in the *Drosophila*
  giant fiber system. J Comp Neurol. PMID 9987990.
  <https://pubmed.ncbi.nlm.nih.gov/9987990/>
- **Confidence** — high for the qualitative double-dissociation (electrical
  vs chemical), low/unverified for which numeric spacing value maps to
  which genotype.

### T-MOT-6  ShakB(N+16) mediates a mixed chemical+electrical synapse from auditory (Johnston's Organ) sensory neurons onto the GF

- **Quantity** — identity of the innexin isoform and synapse type at the
  JO (Johnston's Organ) → GF input synapse (upstream of the GF, i.e. an
  auditory input to the escape circuit, distinct from the visual LC4/LPLC2
  inputs in §2)
- **Value** — JO neurons form **mixed chemical and electrical synapses**
  onto the GF; the specific innexin isoform **ShakB(N+16)** mediates
  coupling; *shakB* mutation disrupts it, and ShakB overexpression causes
  ectopic dye coupling. No latency/conductance numbers extracted.
- **Type** — perturbation (genetic mutant / overexpression)
- **Method** — dye coupling, immunohistochemistry (ShakB antibody
  localization to contact zone), genetic manipulation of *shakB*
- **Observation model** — structural/connectivity target (presence/absence
  of electrical coupling), not directly a timing number
- **Conditions** — adult *D. melanogaster*
- **Source** — Pézier AP, Jezzini SH, Bacon JP, Blagburn JM (2016). Shaking
  B Mediates Synaptic Coupling between Auditory Sensory Neurons and the
  Giant Fiber of *Drosophila melanogaster*. PLoS One. PMID 27043822.
  <https://pubmed.ncbi.nlm.nih.gov/27043822/>
- **Confidence** — high for the qualitative finding; not a numeric target.

### T-MOT-7  Rectification mechanism at GF electrical synapses (mechanism identified, ratio not extracted)

- **Quantity** — molecular mechanism producing rectification (asymmetric
  current flow) at identified GF electrical synapses
- **Value** — mechanism paper; **no numeric rectification ratio was
  extracted from the abstract this session**
- **Type** — perturbation (molecular/genetic dissection, per title)
- **Method** — not extracted this session (full text not fetched)
- **Observation model** — if pursued, our extractor would need to know the
  ratio of forward:reverse conductance at ShakB-containing GF electrical
  synapses to model them as truly rectifying rather than symmetric gap
  junctions
- **Conditions** — not extracted this session
- **Source** — Phelan lab (2008). Molecular mechanism of rectification at
  identified electrical synapses in the *Drosophila* giant fiber system.
  Curr Biol. PMID 19084406. <https://pubmed.ncbi.nlm.nih.gov/19084406/>
- **Confidence** — low as a numeric target — **this is a named gap**: we
  know rectification exists and roughly why, but not by how much.

### T-MOT-8  Aging reduces GF electrical transmission via ShakB trafficking; rescued by insulin-signalling / proteasome manipulation

- **Quantity** — effect of reduced insulin/IGF signalling and increased
  proteasomal activity on age-related decline of GF system electrical
  transmission
- **Value** — qualitative perturbation result: reduced insulin signalling
  **maintains** electrical transmission in aging flies (prevents the
  age-related decline) by preserving trafficking of the gap-junction
  protein ShakB (via Rab4/Rab11-dependent endosomal recycling); separately,
  increasing proteasomal activity also prevents the age-related functional
  decline of the GF system. No latency/conductance numbers extracted this
  session.
- **Type** — perturbation (genetic manipulation of insulin signalling /
  proteasome; aging as a co-variate)
- **Method** — electrophysiological recording of GF system output (jump/
  flight muscle response) across age, combined with genetic manipulation
  and imaging of ShakB trafficking
- **Observation model** — not directly a timing number; relevant if we
  ever model activity-dependent or age-dependent synaptic weight decay for
  electrical synapses specifically (as opposed to chemical ones)
- **Conditions** — adult *D. melanogaster*, aged cohorts vs young, genetic
  manipulation of insulin signalling/proteasome/Rab4/Rab11
- **Source** — Augustin H, McGourty K, Allen MJ, et al., Partridge L
  (2017). Reduced insulin signaling maintains electrical transmission in a
  neural circuit in aging flies. PLoS Biol. PMID 28902870. Companion:
  Augustin H, et al. (2018). Impact of insulin signaling and proteasomal
  activity on physiological output of a neuronal circuit in aging
  *Drosophila melanogaster*. Neurobiol Aging. PMID 29579685.
  <https://pubmed.ncbi.nlm.nih.gov/28902870/>
- **Confidence** — high for the qualitative causal claim (this is exactly
  the "silencing/manipulating X changes Y" perturbation form this
  repository prioritizes); no numeric magnitude captured this session.

### T-MOT-9  Rearing temperature (29 °C) alters GF circuit robustness and habituation across the lifespan

- **Quantity** — effect of chronic high-temperature rearing (29 °C) on
  GF/downstream jump-and-flight circuit habituation and use-dependence,
  tracked across aging
- **Value** — qualitative: high-temperature-reared (29 °C) flies show
  altered, age-dependent trajectories of habituation and use-dependence in
  the GF-driven jump-and-flight reflex relative to standard-temperature
  controls; specific magnitudes not extracted this session
- **Type** — perturbation (chronic rearing temperature)
- **Method** — behavioural/electrophysiological assay of GF-driven jump/
  flight reflex habituation, compared across rearing temperature and age
- **Observation model** — this is the clearest *rearing*-temperature
  (developmental/chronic) perturbation we found for this circuit — distinct
  from *recording*-temperature, which is the more direct confound for
  comparing latency numbers across labs (see gap note in §6, since none of
  the latency papers above state recording temperature)
- **Conditions** — adult *D. melanogaster*, reared at 29 °C ("HT") vs
  standard rearing temperature (typically 25 °C, not explicitly confirmed
  this session), assayed across adult age
- **Source** — Iyengar A, Ruan H, Wu CF (2022). Distinct Aging-Vulnerable
  and -Resilient Trajectories of Specific Motor Circuit Functions in
  Oxidation- and Temperature-Stressed *Drosophila*. eNeuro. PMID 34876473.
  <https://pubmed.ncbi.nlm.nih.gov/34876473/>
- **Confidence** — medium; qualitative effect confirmed, magnitudes not
  extracted.

### T-MOT-10  Oxidative stress (Sod1 loss-of-function) increases GF pathway latency and degrades high-frequency following

- **Quantity** — effect of *Sod1* loss-of-function mutation (and
  paraquat-induced oxidative stress) on GF pathway response latency and
  fidelity under repetitive stimulation
- **Value** — qualitative: adult GF escape pathway shows **"increased
  latency and poor response to repetitive high-frequency stimulation"** in
  *Sod1* mutants; no ms values extracted this session
- **Type** — perturbation (genetic loss-of-function / chemical oxidative
  stressor)
- **Method** — electrophysiological stimulation/recording of the GF
  pathway (same general paradigm as T-MOT-1/2) in mutant vs control
- **Observation model** — a "latency increases under stress" perturbation
  is directly testable if our model has any stress/energy-state variable
  affecting conduction or synaptic reliability — currently it does not
- **Conditions** — adult *D. melanogaster*, *Sod1* loss-of-function vs
  paraquat-exposed vs control
- **Source** — Ueda A, Iyengar A, Wu CF (2021). Differential effects on
  neuromuscular physiology between Sod1 loss-of-function mutation and
  paraquat-induced oxidative stress in *Drosophila*. MicroPubl Biol. PMID
  34027314. <https://pubmed.ncbi.nlm.nih.gov/34027314/>
- **Confidence** — medium; qualitative only.

### T-MOT-11  GF silencing shortens escape duration and affects survival under real predation

- **Quantity** — effect of genetically silencing the GF pathway on escape
  behaviour and survival when flies are exposed to live predators
  (ecological validation of lab-defined "short-mode" escape)
- **Value** — qualitative: GF-driven (short-duration) escapes causally
  contribute to survival during actual predation; silencing GF changes
  action selection and escape duration. No survival-rate percentages
  extracted this session.
- **Type** — perturbation (genetic silencing) with a naturalistic/ecological
  readout
- **Method** — optogenetic/genetic silencing of GF, staged predation
  assays (e.g. against predatory flies or mantises), high-speed videography
- **Observation model** — behavioural readout (escape occurs / does not;
  duration short vs long), not a neural timing number — useful as a
  higher-level validation target once/if the model produces spiking output
  through a GF-homologue node
- **Conditions** — adult *D. melanogaster*, real predation context (not a
  reduced/restrained preparation)
- **Source** — Chai CM, Morrow CM, Parikh DD, von Reyn CR, Leonardo A, Card
  GM (2025). Shorter-duration escapes driven by *Drosophila* giant
  interneurons promote survival during predation. Proc Biol Sci. PMID
  40425165. <https://pubmed.ncbi.nlm.nih.gov/40425165/>
- **Confidence** — medium; recent paper, abstract-level detail only.

### T-MOT-12  Relative spike timing between GF and a parallel pathway determines behaviour selection

- **Quantity** — how the *relative timing* of spikes in the GF versus a
  parallel, non-GF descending pathway determines which motor program
  (stable flight maintained vs. escape take-off) is selected
- **Value** — qualitative spike-timing-code result; **no numeric timing
  values were retrieved this session** — full text was not successfully
  accessed (see §6)
- **Type** — perturbation / dynamic response (this is a "spike-timing
  determines action selection" causal claim, exactly the perturbation form
  this repository prioritizes, but we could not pull the actual numbers)
- **Method** — intracellular recording from GF and the parallel pathway
  during visually evoked escape, correlated with behavioural outcome
- **Observation model** — would require our model to track relative spike
  timing between two specific pathways, not just individual firing rates —
  a structurally different kind of target than most of what's in this
  repository so far
- **Conditions** — adult *D. melanogaster*, tethered, visual looming
  stimulus
- **Source** — von Reyn CR, Breads P, Peek MY, et al., Card GM (2014). A
  spike-timing mechanism for action selection. Nat Neurosci. PMID
  24908103. <https://pubmed.ncbi.nlm.nih.gov/24908103/>
- **Confidence** — low as a numeric target this session (concept only) —
  **flagged gap**; this paper likely contains exactly the kind of latency
  numbers the project wants most, and is worth a dedicated full-text pass.

### T-MOT-13  Single GF spike timing determines short- vs long-mode takeoff

- **Quantity** — how the timing of a single GF spike (relative to
  stimulus/visual feature trajectory) determines whether the fly executes
  a fast "short-mode" jump-take-off or a slower "long-mode" take-off with
  preparatory leg movements
- **Value** — qualitative: **"the timing of a single spike in the GF...
  determines whether a fly uses a short or long takeoff."** LPLC2 and LC4
  visual projection neurons both synapse directly onto the GF; a model
  summing a linear function of angular velocity and a Gaussian function of
  angular size reproduces GF recruitment. **No numeric latency/threshold
  values were extracted from the abstract**, and our attempt to fetch the
  full text this session retrieved the wrong PMC article (a different,
  unrelated paper) — genuine full-text numbers remain a gap.
- **Type** — perturbation / dynamic response
- **Method** — intracellular GF recording plus high-speed videography of
  takeoff mode, during controlled looming visual stimuli; LPLC2/LC4
  identification via connectomics + genetic silencing
- **Observation model** — binary classification (short vs long mode) keyed
  to single-spike timing — again a structurally different target from a
  firing-rate comparison
- **Conditions** — adult *D. melanogaster*, tethered/walking, looming
  visual stimuli of varying size and approach velocity
- **Source** — Ache JM, Polsky J, Alghailani S, et al., von Reyn CR, Card
  GM (2019). Neural Basis for Looming Size and Velocity Encoding in the
  *Drosophila* Giant Fiber Escape Pathway. Curr Biol. PMID 30827912.
  <https://pubmed.ncbi.nlm.nih.gov/30827912/>
- **Confidence** — low as a numeric target this session (concept only) —
  **flagged gap**, same caveat as T-MOT-12.

### T-MOT-14  Linear integration of angular size and angular velocity within the GF sets motor-program selection and its timing

- **Quantity** — how two classes of looming-responsive visual projection
  neurons (one encoding angular expansion velocity, one encoding angular
  size) are linearly integrated postsynaptically in the GF to jointly
  determine both *which* escape motor program runs and *when* it starts
- **Value** — qualitative integration/probabilistic-behaviour result; no
  numeric values extracted from the abstract this session
- **Type** — perturbation (this paper's title is literally "Feature
  Integration Drives Probabilistic Behavior")
- **Method** — intracellular GF recording during visual stimulation
  isolating size vs. velocity cues; genetic silencing of specific VPN types
- **Observation model** — if pursued, needs our model to represent at
  least two separable visual feature channels converging on one
  integrator neuron, not a single lumped "looming" input
- **Conditions** — adult *D. melanogaster*, tethered, visual stimulation
- **Source** — von Reyn CR, Nern A, Williamson WR, Breads P, Wu M, Namiki
  S, Card GM (2017). Feature Integration Drives Probabilistic Behavior in
  the *Drosophila* Escape Response. Neuron. PMID 28641115.
  <https://pubmed.ncbi.nlm.nih.gov/28641115/>
- **Confidence** — medium for the qualitative claim; no numeric target
  extracted.

### T-MOT-15  GF response is azimuth-invariant to looming, via bilateral/contralateral integration

- **Quantity** — whether/how the GF's response to a looming stimulus
  depends on the stimulus's azimuthal (left-right) position
- **Value** — GF responds with **azimuthal invariance** to looming stimuli;
  a contralateral visual pathway contributing to this invariance was
  identified. No numeric values extracted this session.
- **Type** — steady-state / dynamic response (an invariance property, not a
  perturbation)
- **Method** — intracellular GF recording during looming stimuli presented
  at varying azimuthal positions, bilaterally
- **Observation model** — a model-checkable invariance: simulated GF
  response amplitude/latency should not vary strongly with stimulus
  azimuth, if this pathway is ever built out
- **Conditions** — adult *D. melanogaster*, tethered, looming stimuli at
  multiple azimuths
- **Source** — Jang H, Goodman DP, Ausborn J, von Reyn CR (2023). Azimuthal
  invariance to looming stimuli in the *Drosophila* giant fiber escape
  circuit. J Exp Biol. PMID 37066993.
  <https://pubmed.ncbi.nlm.nih.gov/37066993/>
- **Confidence** — medium for the qualitative claim; no numeric target.

---

## 2. Looming responses: LC4, LPLC2, and short- vs long-mode escape

### T-MOT-16  LC4 looming-selectivity via radial motion opponency, output onto GF

- **Quantity** — mechanism by which LC4 visual projection neurons achieve
  "ultra-selective" looming detection, and their downstream target
- **Value** — LC4 responds strongly to outward (expanding) motion; local
  inhibitory inputs are directionally selective for *inward* motion,
  producing radial motion opponency; LC4 (part of the same VPN population
  discussed alongside LPLC2 for looming) **terminates onto the giant fibre
  descending neurons, which drive the jump-muscle motor neuron.** No
  numeric latency, threshold, or angular-size/velocity tuning values were
  extracted from the abstract this session.
- **Type** — perturbation (the paper uses genetic silencing/activation to
  establish the circuit, per its methods) — not confirmed in detail this
  session
- **Method** — not extracted this session (full text not fetched); known
  from the field to combine EM connectomics, calcium imaging, and
  behaviour
- **Observation model** — would need our extractor to reproduce a
  directionally-opponent receptive field (outward-excite / inward-inhibit),
  not just a generic "looming detector"
- **Conditions** — not extracted this session
- **Source** — Klapoetke NC, Nern A, Peek MY, Rogers EM, Breads P, Rubin
  GM, Reiser MB, Card GM (2017). Ultra-selective looming detection from
  radial motion opponency. Nature. PMID 29120418.
  <https://pubmed.ncbi.nlm.nih.gov/29120418/>
- **Confidence** — medium for the qualitative mechanism (well-known,
  frequently cited result); no numeric target extracted this session —
  **flagged gap**, full text not fetched due to session tool budget.

### T-MOT-17  LPLC2 and LC4 provide convergent looming input directly onto the GF

- **Quantity** — connectivity and functional role of LPLC2 alongside LC4
  as direct presynaptic partners of the GF, encoding complementary looming
  features
- **Value** — see T-MOT-13: both LPLC2 and LC4 **synapse directly onto the
  GF**; a linear-angular-velocity-plus-Gaussian-angular-size summation
  model reproduces GF recruitment from these two input classes
- **Type** — perturbation / connectivity
- **Method** — as T-MOT-13
- **Observation model** — as T-MOT-13
- **Conditions** — as T-MOT-13
- **Source** — same as T-MOT-13 (Ache et al. 2019, Curr Biol, PMID
  30827912)
- **Confidence** — medium for connectivity/qualitative model structure; no
  numeric target extracted this session.

### T-MOT-18  ~200 ms preparatory postural adjustment precedes take-off

- **Quantity** — timing of preparatory postural/leg adjustments before a
  visually evoked take-off
- **Value** — **approximately 200 ms** before takeoff, flies begin a series
  of postural adjustments (leg repositioning, wing raising) — this is
  reported in the context of the (slower) long-mode/planned take-off, not
  the fast GF-mediated short-mode escape
- **Type** — dynamic response
- **Method** — high-speed videography (typically thousands of fps) of
  tethered/loosely-restrained flies responding to a looming visual stimulus
  (expanding disc), with kinematic tracking of leg and wing movements
- **Observation model** — our extractor would need to define "postural
  adjustment onset" the same way (first detectable leg-angle change) rather
  than reading out a first-spike time; note this is a whole-body kinematic
  latency, not a neural one
- **Conditions** — adult *D. melanogaster*, tethered or loosely restrained,
  visual looming stimulus; temperature not extracted this session
- **Source** — Card G, Dickinson MH (2008). Visually mediated motor
  planning in the escape response of *Drosophila*. Curr Biol. PMID
  18760606. <https://pubmed.ncbi.nlm.nih.gov/18760606/>
- **Confidence** — medium; single number extracted from abstract, full
  text (likely containing the short-mode latency for direct comparison)
  not fetched this session.

### T-MOT-19  Short-mode vs long-mode total escape latency — NOT FOUND this session

- **Quantity** — the actual numbers we most wanted for this section: total
  latency from looming-stimulus feature (e.g. time-to-contact threshold
  crossing) to take-off initiation, separately for GF-mediated short-mode
  vs. non-GF long-mode escapes
- **Value** — **not found this session.** We queried Card & Dickinson 2008
  (Curr Biol, PMID 18760606 — only yielded the 200 ms postural-adjustment
  figure above), Card & Dickinson's companion paper "Performance trade-offs
  in the flight initiation of *Drosophila*" (J Exp Biol, PMID 18203989 — no
  numeric values surfaced in the abstract), and Zabala, Card, Fontaine,
  Dickinson, Murray (2009), "Flight dynamics and control of evasive
  maneuvers: the fruit fly's takeoff" (IEEE Trans Biomed Eng, PMID
  19643699 — no numeric values surfaced in the abstract). None of these
  abstracts contained the short-vs-long latency comparison; full text was
  not fetched for any of the three due to session tool-call budget.
- **Type** — n/a (gap)
- **Method** — n/a
- **Observation model** — n/a
- **Conditions** — n/a
- **Source** — see above three PMIDs as the most likely places to find this
  next
- **Confidence** — n/a — **explicitly flagged as not found**, per the
  instruction to state plainly what could not be located, rather than
  filled in from memory/estimation.

### T-MOT-20  Molecular wiring gradient sets LPLC2 output synapse distribution (context, not physiology)

- **Quantity** — how graded expression of cell-recognition molecules
  (Dpr13, DIP-ε, Beat-VI) along LPLC2 axons sets the spatial gradient of
  its output synapses to downstream partners including the GF
- **Value** — qualitative developmental-wiring result; not a timing or
  rate measurement
- **Type** — perturbation (genetic disruption of the recognition molecules
  changes synaptic distribution)
- **Method** — connectomics + genetic manipulation of cell-recognition
  molecule expression + synaptic distribution mapping
- **Observation model** — not applicable to dynamical fitting; relevant
  only if we ever model synapse-count gradients along a single axon rather
  than a lumped per-cell-type weight
- **Conditions** — adult *D. melanogaster*
- **Source** — Dombrovski M, Zang Y, Frighetto G, et al., Card GM, Zipursky
  SL (2024/2025). Molecular gradients shape synaptic specificity of a
  visuomotor transformation. Nature (also circulated as a 2025 bioRxiv
  preprint, PMID 39974884). PMID 40468081.
  <https://pubmed.ncbi.nlm.nih.gov/40468081/>
- **Confidence** — high for the qualitative claim; low relevance to our
  current (non-spatial) connectome-weight representation, included for
  completeness only.

---

## 3. Descending neurons driving specific behaviours

### T-MOT-21  DNa02: stride-locked firing modulation and neural-to-behaviour latency during steering

- **Quantity** — during turning in walking flies, how DNa02 firing rate is
  modulated relative to the stride cycle, and how far in advance firing
  changes precede the resulting behavioural (stride length/direction)
  change
- **Value** — DNa02 shows **stride-locked firing modulation of
  approximately 15 spikes/s (~10% of the cell's overall dynamic range)**;
  firing-rate changes **precede the behavioural change by approximately
  150 ms**; turning is accompanied by stride-length changes of
  approximately **5% of body length**, modulated at a stride-locked
  frequency of about **10 Hz**. Rotational (turning) velocities examined
  spanned bins of 20–50, 50–100, 100–150, and 150–200 °/s.
- **Type** — dynamic response, with perturbation components elsewhere in
  the same paper (optogenetic activation/silencing of DNa02, per its
  broader design — not itself detailed in what we extracted)
- **Method** — simultaneous intracellular/extracellular recording from
  identified descending neurons and high-resolution leg-tracking during
  spontaneous and visually/mechanically driven turning, in a
  head-fixed walking preparation
- **Observation model** — the ~150 ms neural-to-behaviour lead time is
  exactly the kind of "signal precedes response by X ms" number our
  extractor should be able to reproduce directly from simulated spike
  trains vs. a simulated/assumed motor-output readout — no imaging
  indicator kinetics to convolve through, since this is electrophysiology
- **Conditions** — adult *D. melanogaster*, head-fixed, walking on a
  spherical treadmill; temperature not extracted this session
- **Source** — Yang HH, Brezovec BE, Serratosa Capdevila L, Vanderbeck QX,
  Adachi A, Mann RS, Wilson RI (2024). Fine-grained descending control of
  steering in walking *Drosophila*. Cell. PMID 39293446, PMC12778575.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC12778575/>
- **Confidence** — high; recent, detailed, quantitative electrophysiology
  paper, and PMC full text was successfully accessed this session.

### T-MOT-22  DNg13 plays a complementary steering role alongside DNa02

- **Quantity** — division of labour between DNa02 and a second descending
  neuron type, DNg13, in fine steering control
- **Value** — qualitative: DNa02 and DNg13 have **"opposite effects during
  different locomotor rhythm phases"** — one type lengthens strides on the
  turn's exterior side, the other attenuates strides on the interior side;
  together they produce coordinated, phase-specific steering adjustments
- **Type** — dynamic response / perturbation (the paper manipulates each
  neuron type individually per its design)
- **Method** — as T-MOT-21
- **Observation model** — requires modelling at least two distinct
  descending steering channels with opposite, phase-dependent effects on
  the step cycle, not one lumped "turn" signal
- **Conditions** — as T-MOT-21
- **Source** — same as T-MOT-21 (Yang et al. 2024, Cell, PMID 39293446)
- **Confidence** — high for the qualitative division of labour; the
  precise phase-dependence numbers were not fully extracted this session.

### T-MOT-23  MDN activation triggers backward walking; touch is relayed to MDN by TwoLumps ascending neurons

- **Quantity** — causal role of moonwalker descending neurons (MDN) in
  backward walking, and of TwoLumps Ascending (TLA) neurons as an upstream
  touch-triggered relay onto MDN
- **Value** — **silencing TLA impairs backward locomotion; optogenetically
  activating TLA triggers backward walking.** TLA responds to anterior
  body touch and provides feedforward excitatory drive onto MDN. No
  latency (ms) values extracted this session.
- **Type** — perturbation (optogenetic silencing and activation — a clean
  bidirectional causal test, exactly this repository's preferred target
  type)
- **Method** — optogenetic silencing (e.g. GtACR1) and activation (e.g.
  CsChrimson) of genetically targeted TLA neurons, combined with
  mechanical touch stimulation and behavioural tracking
- **Observation model** — binary/rate behavioural readout (backward
  walking occurs / rate of occurrence), keyed to optogenetic stimulation
  windows — directly comparable to how this repository already handles
  other activation/silencing experiments (see `shiu-predictions.md`
  protocol) if a VNC/descending-neuron module is added
- **Conditions** — adult *D. melanogaster*, walking, anterior-body
  mechanical touch stimulus, optogenetic manipulation
- **Source** — Sen R, Wang K, Dickson BJ (2019). TwoLumps Ascending Neurons
  Mediate Touch-Evoked Reversal of Walking Direction in *Drosophila*. Curr
  Biol. PMID 31813606. <https://pubmed.ncbi.nlm.nih.gov/31813606/>
- **Confidence** — high for the qualitative causal claim; no numeric
  latency/rate extracted this session.

### T-MOT-24  MDN mediates visually evoked retreat (backward walking)

- **Quantity** — causal role of MDN in visually evoked backward walking
  (retreat), as distinct from touch-evoked reversal (T-MOT-23)
- **Value** — qualitative: MDN activity mediates visually evoked retreat;
  no numeric values were captured from the abstract this session
- **Type** — perturbation (optogenetic, per title/known paradigm)
- **Method** — not captured in detail this session
- **Observation model** — same general form as T-MOT-23
- **Conditions** — adult *D. melanogaster*
- **Source** — Sen R, Wu M, Branson K, et al. (2017). Moonwalker Descending
  Neurons Mediate Visually Evoked Retreat in *Drosophila*. Curr Biol. PMID
  28238656. <https://pubmed.ncbi.nlm.nih.gov/28238656/>
- **Confidence** — medium; qualitative only, no numbers extracted this
  session.

### T-MOT-25  Olfactory stimuli drive backward locomotion via moonwalker SEZ neurons upstream of MDN

- **Quantity** — a second, olfactory (rather than touch or vision) input
  pathway onto MDN, via subesophageal-zone "moonwalker" neurons (MooSEZ)
- **Value** — qualitative: MooSEZ neurons trigger straight and rotational
  backward locomotion via postsynaptic MDNs, in response to olfactory
  stimuli; no numeric values extracted this session
- **Type** — perturbation (optogenetic/genetic, per known paradigm)
- **Method** — not captured in detail this session
- **Observation model** — adds a third distinct sensory channel (after
  touch/TLA and vision) converging on the same MDN output node — relevant
  if MDN is modelled as a single integration point
- **Conditions** — adult *D. melanogaster*
- **Source** — (2022). Olfactory stimuli and moonwalker SEZ neurons can
  drive backward locomotion in *Drosophila*. Curr Biol. PMID 35139358.
  <https://pubmed.ncbi.nlm.nih.gov/35139358/>
- **Confidence** — medium; author names not confirmed this session (not
  captured in the abstract extraction) — flagged for verification before
  citing formally.

### T-MOT-26  Downstream of MDN: identified leg motor circuit elements for backward walking

- **Quantity** — identity and role of specific neurons immediately
  downstream of MDN that implement backward walking at the leg
  motor-circuit level
- **Value** — qualitative: **LBL40** provides hindleg power stroke during
  stance phase; **LUL130** lifts the legs at the end of stance to initiate
  swing (during backward walking). No firing rates extracted this session.
- **Type** — perturbation (per title, "distributed control" implies
  silencing/activation of each identified element)
- **Method** — connectomics-guided genetic targeting, optogenetic
  manipulation, leg kinematic tracking during backward walking
- **Observation model** — gives named, connectome-identifiable
  intermediate nodes between MDN and the leg motor neurons — directly
  useful if we extend our graph beyond "MDN → generic leg MN"
- **Conditions** — adult *D. melanogaster*, backward walking
- **Source** — Feng K, et al. (2020). Distributed control of motor circuits
  for backward walking in *Drosophila*. Nat Commun. PMID 33268800.
  <https://pubmed.ncbi.nlm.nih.gov/33268800/>
- **Confidence** — medium; full author list and numeric rates not captured
  this session.

### T-MOT-27  MDN cell bodies cluster via Innexin-8 gap junctions, enabling synchronous firing required for backward-walking initiation

- **Quantity** — role of Innexin-8-mediated electrical coupling between
  MDN cell bodies (via soma clustering) in producing the synchronous
  firing needed to initiate backward walking
- **Value** — qualitative perturbation: disrupting Inx8-mediated clustering
  disrupts synchronous MDN firing and, with it, reliable backward-walking
  initiation; clustering is also associated with a more depolarized
  resting membrane potential. No conductance/latency numbers extracted
  this session.
- **Type** — perturbation (genetic disruption of Inx8/clustering)
- **Method** — anatomical clustering analysis, dye-coupling/electrical
  recording for synchrony, genetic disruption of Inx8, behavioural assay
  of backward walking
- **Observation model** — this is a second, independent instance (besides
  ShakB in the GF pathway, §1) of an **electrical synapse being causally
  required for a fast, stereotyped escape/locomotor behaviour** — directly
  relevant to this project's specific interest in gap-junction-mediated
  transmission as a modelling feature, not just chemical synapses
- **Conditions** — adult *D. melanogaster*
- **Source** — (2026). Cell body position of *Drosophila* Moonwalker
  Descending Neurons regulates locomotor circuit function. Proc Natl Acad
  Sci U S A. PMID 42685078. Companion preprint: (2026). Cell body
  clustering drives gap junction-mediated synchronous activity in command
  neurons. bioRxiv. PMID 41867757.
  <https://pubmed.ncbi.nlm.nih.gov/42685078/>
- **Confidence** — medium; very recent (2026) publication, author names not
  fully captured this session, no quantitative conductance/timing values
  extracted — qualitative mechanism only, worth a follow-up full-text pass
  given its direct relevance to the electrical-synapse modelling question.

### T-MOT-28  MDN integrates antennal touch to drive forward-to-backward transitions; DopaMeander neuron activity correlates with turning

- **Quantity** — a further upstream input (antennal mechanosensation) onto
  MDN driving gait-direction switching, plus a dopaminergic descending
  pathway ("DopaMeander") correlated with turning direction
- **Value** — qualitative: MDN integrates antennal touch signals to drive
  forward-to-backward direction changes; **DopaMeander neuron activity
  correlates with ipsiversive turning.** No numeric values extracted this
  session.
- **Type** — dynamic response / perturbation (correlational finding
  reported here; the source paper likely also contains an activation
  experiment we did not capture in detail)
- **Method** — not captured in detail this session
- **Observation model** — adds antennal touch as a fourth sensory channel
  onto MDN (after leg/body touch, vision, olfaction) and introduces a
  parallel dopaminergic steering channel
- **Conditions** — adult *D. melanogaster*
- **Source** — (2026). Control of walking direction by descending and
  dopaminergic neurons in *Drosophila*. Curr Biol. PMID 42442357.
  <https://pubmed.ncbi.nlm.nih.gov/42442357/>
- **Confidence** — medium; very recent (2026), author names and numeric
  values not captured this session.

### T-MOT-29  Pair1 descending neuron activation arrests forward locomotion; the MDN-Pair1 circuit persists from larva to adult

- **Quantity** — causal effect of activating the Pair1 descending neuron,
  and the developmental persistence of the MDN-Pair1 circuit motif across
  metamorphosis
- **Value** — **optogenetic activation of Pair1 arrests forward
  locomotion.** The MDN-Pair1 circuit is present and functions similarly
  in both larval and adult stages. No latency numbers extracted this
  session.
- **Type** — perturbation (optogenetic activation)
- **Method** — optogenetic activation (e.g. CsChrimson) of genetically
  targeted Pair1 neurons in both larvae and adults, with behavioural
  tracking
- **Observation model** — binary/rate behavioural readout (locomotion
  arrest), comparable in form to other activation experiments already in
  this repository's protocol style
- **Conditions** — *D. melanogaster*, both larval and adult stages
- **Source** — (2021). A locomotor neural circuit persists and functions
  similarly in larvae and adult *Drosophila*. eLife. PMID 34259633.
  <https://pubmed.ncbi.nlm.nih.gov/34259633/>
- **Confidence** — medium; author names not captured this session.

### T-MOT-30  DNp09 activation drives running or freezing in a state-dependent manner

- **Quantity** — behavioural effect of optogenetically activating the
  DNp09 descending neuron pair, and its dependence on the fly's ongoing
  behavioural/speed state
- **Value** — qualitative: **DNp09 activation induces either running or
  freezing, contingent on the fly's behavioural state** at the time of
  activation (i.e. not a fixed stereotyped output — an unusual and
  important caveat for treating DNp09 as a simple "forward walking driver"
  in a model). No latency or firing-rate numbers extracted this session.
- **Type** — perturbation (optogenetic activation)
- **Method** — optogenetic activation of genetically targeted DNp09,
  behavioural state classification, locomotor tracking
- **Observation model** — a state-dependent, non-deterministic
  stimulation→behaviour mapping — if modelled naively as "activating DNp09
  always produces walking," this result says that would be wrong; the
  model would need a state variable gating the outcome
- **Conditions** — adult *D. melanogaster*, freely walking
- **Source** — (2018). Speed dependent descending control of freezing
  behavior in *Drosophila melanogaster*. Nat Commun. PMID 30209268.
  <https://pubmed.ncbi.nlm.nih.gov/30209268/>
- **Confidence** — medium; **author names could not be confirmed this
  session** (not captured in the abstract extraction) — flagged for
  verification before formal citation.

### T-MOT-31  Foundational descending-neuron papers not retrieved this session

- **Quantity** — three papers we specifically went looking for, by name,
  because they are the best-known primary sources for exactly the neurons
  this project asked about
- **Value** — **not retrieved this session**:
  (1) Bidaye SS, Machacek C, Wu Y, Dickson BJ (2014), "Neuronal control of
  *Drosophila* walking direction," Science — the original MDN/moonwalker
  discovery paper;
  (2) Bidaye et al. (2020), "Two Brain Pathways Initiate Distinct Forward
  Walking Programs in *Drosophila*," Neuron — the primary DNp09
  forward-walking paper;
  (3) Cande J, Namiki S, Qiu J, Korff W, Card GM, Shaevitz JW, Stern DL,
  Berman GJ (2018), "Optogenetic dissection of descending behavioral
  control in *Drosophila*," eLife — a systematic activation screen across
  many identified descending neurons including DNp09.
  Multiple NCBI esearch query phrasings for all three ("Bidaye moonwalker
  Drosophila walking direction," combinations with "DNp09," "descending
  neuron") returned **zero PubMed results** this session, which is
  surprising given how well-cited these papers are — most likely a
  query-construction/term-matching issue on our end (esearch's default
  term-mapping appears to fail silently on some multi-word combinations,
  as we also saw for other queries in this session — see §6) rather than
  these papers being genuinely absent from PubMed.
- **Type** — n/a (gap)
- **Method/Observation model/Conditions** — n/a
- **Source** — cited from general background knowledge only; **not
  independently re-verified via NCBI this session**
- **Confidence** — **flagged explicitly as unverified** — the existence and
  rough content of these three papers is well-established prior knowledge,
  but no specific number attributed to them in this file should be trusted
  without re-fetching them directly (e.g. by DOI or PMID looked up
  directly on pubmed.ncbi.nlm.nih.gov rather than via esearch keyword
  queries).

---

## 4. Leg motor neuron recruitment (Azevedo, Tuthill et al.)

### T-MOT-32  Recruitment order follows a size principle: slow → intermediate → fast

- **Quantity** — order in which the three broad classes of leg motor
  neuron (slow, intermediate, fast) are recruited as motor drive increases
- **Value** — **slow motor neurons are recruited first, then intermediate,
  then fast** — a direct *Drosophila* analogue of Henneman's size
  principle in vertebrate motor units
- **Type** — steady-state (an ordering/organizational principle observed
  across many trials/behaviours) — arguably also a "dynamic response"
  since it concerns temporal recruitment sequence within a single motor
  act; recorded here as the paper's central claim
- **Method** — intracellular/patch recording from identified leg motor
  neurons (by size/anatomical class) during spontaneous and evoked leg
  movements (walking, grooming, kicking), in an intact or semi-intact adult
  preparation
- **Observation model** — our extractor would need to rank simulated motor
  neuron activation thresholds by class and confirm the same ordering,
  ideally across multiple behaviours (the paper explicitly checks this
  across walking/grooming/kicking, not just one behaviour)
- **Conditions** — adult *D. melanogaster*, multiple leg behaviours
  (walking, grooming, kicking); temperature not extracted this session
- **Source** — Azevedo AW, Dickinson ES, Gurung P, Venkatasubramanian L,
  Mann RS, Tuthill JC (2020). A size principle for recruitment of
  *Drosophila* leg motor neurons. eLife. PMID 32490810, PMC7347388.
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7347388/>
- **Confidence** — high; PMC full text was successfully accessed this
  session and confirms the core claim in detail.

### T-MOT-33  Force output per spike differs roughly 100-fold across motor neuron classes

- **Quantity** — force produced per single motor neuron spike, by class
- **Value** — **fast motor neurons: ~10 µN per spike** (stated as
  "approximately equal to the fly's body weight"); **intermediate: ~1 µN
  per spike**; **slow: <0.1 µN per spike**
- **Type** — steady-state
- **Method** — combined motor neuron recording and force/kinematic
  measurement (e.g. via calibrated leg movement or attached force
  transducer) time-locked to identified single spikes
- **Observation model** — a per-spike force-transfer-function target,
  separable by class — directly usable if our model ever outputs
  spike-to-force conversion rather than just firing rate
- **Conditions** — adult *D. melanogaster*
- **Source** — same as T-MOT-32
- **Confidence** — high (specific, directly quoted numbers from PMC full
  text).

### T-MOT-34  Input resistance differs ~5-fold across motor neuron classes (150–700 MΩ)

- **Quantity** — somatic/whole-cell input resistance, by motor neuron class
- **Value** — **fast: 150 MΩ; intermediate: 300 MΩ; slow: 700 MΩ**
  (monotonically decreasing input resistance with increasing recruitment
  order — the biophysical basis of the size principle, mirroring the
  same size-resistance relationship as vertebrate motor units)
- **Type** — steady-state (passive membrane property)
- **Method** — whole-cell patch clamp, current-step protocol, standard
  input-resistance calculation
- **Observation model** — directly comparable to any of our existing
  per-cell-type Rin targets elsewhere in this repository (see
  `parameters-measured.md` for the general membrane-property target
  format); note this is one of the few *complete* passive-property sets
  (Rin + Vrest, see T-MOT-35) for an identified *Drosophila* motor neuron
  class
- **Conditions** — adult *D. melanogaster*, ex vivo/semi-intact patch clamp
- **Source** — same as T-MOT-32
- **Confidence** — high.

### T-MOT-35  Resting potential differs across motor neuron classes (−68 to −48 mV)

- **Quantity** — resting membrane potential, by motor neuron class
- **Value** — **fast: −68 mV; intermediate: −60 mV; slow: −48 mV**
  (fast neurons rest furthest from threshold, slow neurons closest —
  again consistent with, and part of the mechanistic basis for, the
  recruitment order in T-MOT-32)
- **Type** — steady-state
- **Method** — same as T-MOT-34
- **Observation model** — same as T-MOT-34
- **Conditions** — same as T-MOT-34
- **Source** — same as T-MOT-32
- **Confidence** — high.

### T-MOT-36  Slow motor neurons have a resting spontaneous spike rate of ~30 Hz

- **Quantity** — baseline (unstimulated) spontaneous firing rate of slow
  leg motor neurons
- **Value** — **≈30 Hz** at rest
- **Type** — steady-state
- **Method** — intracellular/extracellular recording at rest (no imposed
  movement or stimulus)
- **Observation model** — directly comparable to a simulated baseline
  firing rate for the corresponding connectome cell type, with no
  filtering/threshold subtlety since this is direct spike counting
- **Conditions** — adult *D. melanogaster*, at rest
- **Source** — same as T-MOT-32
- **Confidence** — high.

### T-MOT-37  Leg motor neuron census: 53 motor neurons drive 14 muscles per leg

- **Quantity** — total count of motor neurons and muscles per leg, and the
  breakdown for one specific joint (tibia flexion)
- **Value** — **53 motor neurons innervate 14 muscles** in a single leg;
  tibia flexion specifically is controlled by **~15 motor neurons**,
  comprising **8–9 slow** neurons (innervating distal muscle fibers) and
  **2–5 intermediate** neurons (innervating proximal muscle fibers), plus
  fast neurons
- **Type** — steady-state (anatomical census)
- **Method** — connectomics / genetic-driver-based counting (MANC-era leg
  motor neuron atlas work, consistent with the broader VNC connectome this
  file's scope is built on)
- **Observation model** — a direct cross-check against our own connectome
  import: the 708 total VNC motor neurons cited in this file's framing
  should decompose, per leg, into census numbers consistent with this
  53-per-leg (times 6 legs = 318, plus wing/haltere/neck/abdominal motor
  neurons for the remainder) — worth a direct comparison against
  `src/import_graph.py`'s own motor neuron counts as a sanity check, not
  just a physiology target
- **Conditions** — adult *D. melanogaster*
- **Source** — same as T-MOT-32
- **Confidence** — high for the per-leg breakdown as reported; the
  "6× per-leg ≈ whole-VNC-total" arithmetic above is our own extrapolation,
  not a claim from the source, and should be checked against actual MANC
  counts rather than assumed.

### T-MOT-38  Proprioceptive gain: slow motor neurons are sensitive to 1° changes in tibia angle

- **Quantity** — sensitivity of slow tibia motor neuron firing rate to
  small changes in joint angle (a proprioceptive feedback gain measurement)
- **Value** — a **1° change in tibia angle produced a significant change
  in firing rate** in slow motor neurons (exact Hz/degree gain not
  extracted this session)
- **Type** — dynamic response
- **Method** — intracellular recording from identified slow tibia motor
  neurons during controlled, small-amplitude imposed joint rotations
  (proprioceptive feedback assay)
- **Observation model** — a fine-grained gain target (Hz per degree) if
  the exact value is retrieved in a follow-up pass; currently only the
  qualitative sensitivity threshold (1° is enough to matter) is recorded
- **Conditions** — adult *D. melanogaster*, semi-intact preparation with
  controlled joint manipulation
- **Source** — same as T-MOT-32
- **Confidence** — medium; qualitative threshold only, exact gain value
  not extracted this session.

---

## 5. Walking and flight timescales

### T-MOT-39  Walking speed is controlled almost exclusively via step frequency, with a tripod-to-tetrapod gait transition

- **Quantity** — how *Drosophila* modulates walking speed (step frequency
  vs. step length), and how inter-leg coordination pattern changes with
  speed
- **Value** — qualitative: **"Drosophila controls its walking speed almost
  exclusively via step frequency"** (not step length); coordination
  follows a **tripod** pattern at high speeds and a **tetrapod** pattern at
  low speeds. Exact step-frequency values (Hz) and walking-speed values
  (mm/s or body-lengths/s) were **not extracted from the abstract this
  session**; full text was not fetched.
- **Type** — steady-state (behavioural relationship across a speed range)
- **Method** — high-speed videography of freely walking flies across a
  range of induced speeds, automated leg-tip tracking, gait-pattern
  classification, across four wild-type strains
- **Observation model** — our extractor would need a simulated
  walking-speed-vs-step-frequency relationship (ideally near-linear, per
  this qualitative claim) and a discrete gait-pattern classifier keyed to
  speed, rather than one fixed "step frequency" constant
- **Conditions** — adult *D. melanogaster*, four strains, freely walking;
  temperature not extracted this session
- **Source** — Wosnitza A, Bockemühl T, Dübbert M, Scholz H[?], Büschges A
  (2013). Inter-leg coordination in the control of walking speed in
  *Drosophila*. J Exp Biol. PMID 23038731.
  <https://pubmed.ncbi.nlm.nih.gov/23038731/>
- **Confidence** — medium; qualitative relationship well-established
  (this is a frequently cited paper), but the specific Hz/speed numbers
  this project would need for a tight target were not retrieved this
  session — **flagged gap**, full-text follow-up recommended. (Author
  initials for "Scholz" not fully confirmed.)

### T-MOT-40  Wingbeat frequency — NOT independently verified this session

- **Quantity** — cruising wingbeat frequency of tethered or free-flying
  *Drosophila melanogaster*
- **Value** — **not established with a verified citation this session.**
  Multiple NCBI esearch queries ("Drosophila wingbeat frequency,"
  "Drosophila melanogaster wingbeat frequency tethered flight Hz," and
  variants) either returned zero results or returned papers whose
  abstracts did not state the number (e.g. muscle-mechanics papers that
  discuss wingbeat frequency *changes* under genetic manipulation, such as
  PMID 19450484 and 18805920, without giving the baseline Hz value in the
  abstract). The commonly cited figure in the field is on the order of
  **~200 Hz**, but we are **not citing that here as a sourced value**
  because we could not re-verify it against a specific paper this session
  — including it without a source would violate this file's own standard
  ("a target without its measurement method is not usable").
- **Type** — n/a (gap)
- **Method/Observation model/Conditions** — n/a
- **Source** — none confirmed this session; candidate papers not fully
  checked include Vogel S (1967) and Lehmann FO & Dickinson MH (1997), by
  reputation rather than this session's direct verification
- **Confidence** — **explicitly flagged as not found** — this is a basic,
  presumably easy-to-find number that we nonetheless failed to pin down
  with a citation in the time available; a dedicated follow-up search
  (or a direct full-text check of a Dickinson-lab flight aerodynamics
  paper) should resolve it quickly.

### T-MOT-41  Flight steering modulation onset ~85 ms after olfactory stimulus onset

- **Quantity** — latency from the onset of an olfactory stimulus to the
  onset of a measurable change in flight steering/speed
- **Value** — flight modulation can begin **within about 85 ms** of
  olfactory transduction onset, driven by as few as "a handful of spikes"
  in a single olfactory receptor neuron type
- **Type** — dynamic response
- **Method** — rigid tethered-flight preparation (flight simulator),
  intracellular/extracellular ORN recording, wingbeat-based steering
  readout, precisely timed odor delivery
- **Observation model** — this is a flight-circuit sensorimotor latency,
  not a wingbeat-frequency number — useful as a general "how fast can the
  fly's flight motor system react to a new sensory input" benchmark,
  complementary to the escape-circuit latencies in §1, and much slower
  than the GF pathway (85 ms vs ~1–2 ms) since it does not involve the GF
  at all
- **Conditions** — adult *D. melanogaster*, tethered rigidly for flight,
  odor pulse stimulation; temperature not extracted this session
- **Source** — Bhandawat V, Maimon G, Dickinson MH, Wilson RI (2010).
  Olfactory modulation of flight in *Drosophila* is sensitive, selective
  and rapid. J Exp Biol. PMID 20952610.
  <https://pubmed.ncbi.nlm.nih.gov/20952610/>
- **Confidence** — high (specific number directly stated in abstract).

---

## 6. What we could not find (explicit gaps)

Per this repository's standard, listed plainly rather than silently
omitted:

1. **Recording temperature for every single Giant Fiber latency number in
   this file.** Not one of the sources we accessed (Trimarchi &
   Schneiderman 1993; Augustin et al. 2019, confirmed by direct full-text
   check) states the temperature at which GF latencies were recorded. This
   matters more here than almost anywhere else in this repository, because
   conduction velocity in an ectotherm is directly temperature-dependent,
   and the task's central question — whether real multi-synapse latencies
   support or contradict a fixed 1.8 ms delay — cannot be fully answered
   without knowing whether these numbers were taken at room temperature
   (~21–23 °C) or fly-incubator temperature (25 °C), which could plausibly
   account for some of the T-MOT-1 vs T-MOT-2 discrepancy.
2. **Absolute GF axon conduction velocity in m/s.** We only found relative
   statements (80% increase in the first day of adult life; 20–60× slower
   than vertebrate Aβ fibers) — see T-MOT-3/T-MOT-4.
3. **Full-text numeric latency/threshold values from three central
   papers**: von Reyn et al. 2014 (Nat Neurosci, spike-timing action
   selection), von Reyn et al. 2017 (Neuron, feature integration), and
   Ache et al. 2019 (Curr Biol, looming size/velocity encoding). All three
   abstracts confirm the qualitative finding we most wanted (GF spike
   timing determines behaviour choice) but none gave numbers in the
   abstract, and our attempts to fetch full text either failed to resolve
   the correct PMC ID (elink's id-to-PMC mapping was unreliable when
   multiple PubMed IDs were queried together, and in one case — Ache et
   al. — the PMC ID we were given turned out, on inspection, to be a
   completely different, unrelated paper) or were not attempted due to
   session tool-call budget. **This is the single biggest remaining gap
   relative to the task's top priority.**
4. **Exact short-mode vs long-mode total escape latency (stimulus to
   takeoff, in ms).** See T-MOT-19 — checked three likely papers, none of
   their abstracts contained it.
5. **Three foundational descending-neuron papers**: Bidaye et al. 2014
   Science (MDN discovery), Bidaye et al. 2020 Neuron (DNp09), and Cande
   et al. 2018 eLife (descending-neuron activation screen). See T-MOT-31 —
   NCBI esearch returned zero results for several query phrasings, most
   likely a query-construction issue rather than genuine absence from
   PubMed.
6. **A sourced Drosophila wingbeat frequency value (Hz).** See T-MOT-40 —
   we deliberately did not include the commonly-quoted ~200 Hz figure
   without a citation we could verify this session.
7. **ShakB electrical-synapse rectification ratio** (how many-fold larger
   conductance is in one direction than the other). Mechanism paper found
   (T-MOT-7) but the numeric ratio was not in the abstract and full text
   was not fetched.
8. **A general note on tool reliability this session**: several NCBI
   esearch queries that combined more than ~4-5 keywords returned zero
   results even for topics known to have abundant literature (e.g. plain
   "Drosophila giant fiber escape latency threshold conduction" returned
   nothing, while "giant fiber Drosophila escape" returned 20+ results).
   Where a search came back empty, we generally retried with a shorter
   query rather than concluding no literature exists — but it is possible
   some topics above are under-represented simply because we did not find
   the right short query for them, not because the literature is thin.
   Anyone extending this file should keep queries to 3-4 keywords at most.

