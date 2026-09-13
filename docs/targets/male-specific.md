# Male-specific circuits and sexual dimorphism

Scope: MaleCNS is the male central nervous system, and its accompanying paper
is specifically about sexual dimorphism. Every other domain file in this
collection draws on physiology that may have used female or sex-unspecified
flies; this file collects (1) targets that only exist in, or are known to
differ in, the male, and (2) an explicit warning list of where physiology
already cited in this repository — including our own fitted parameters — came
from a female preparation. Point (2) is flagged inline at each affected target
below and again, consolidated, in **Sex-mismatch warnings** near the end.

Two general findings shape everything below and are worth stating up front:

1. **The two connectomes almost everyone else benchmarks against are both
   female.** FlyWire/FAFB (Full Adult Fly Brain) is a single female specimen;
   the hemibrain (Scheffer et al. 2020) is also a single female specimen ("a
   5-day-old female... Canton-S G1 x w1118"). Our own `src/params.py` already
   depends on FlyWire for its free-parameter comparison (see warnings).
2. **The mismatch is not evenly distributed.** The MaleCNS paper's own
   cross-matching found 97.5% of male neurons/types match a counterpart in
   FlyWire/hemibrain/MANC. The ~2.5-4.8% that do not match are concentrated
   exactly in the circuits most likely to be fitting targets — courtship,
   aggression, pheromone processing, and specific descending/song pathways —
   not spread uniformly across the brain. Sensory and motor periphery
   (including the ORN/PN layer we drive as `ORN_DA1`) is reported as "largely
   isomorphic."

---

## 1. The MaleCNS paper itself

**Sexual dimorphism in the complete Drosophila male central nervous system
connectome.** Cell (2026), DOI 10.1016/j.cell.2026.08.015; preprint bioRxiv
10.1101/2025.10.09.680999 (posted 2025-10-09); PMC12636603. Collaboration:
FlyEM/HHMI Janelia, University of Cambridge Dept. of Zoology, MRC LMB, Google
Research. This is the paper behind the MaleCNS v1.0 release we import in
`src/import_graph.py`.

**No new physiology.** Read carefully: this paper is connectomic/anatomical
only. It presents no calcium imaging, electrophysiology, or new behavioural
experiments of its own. Every physiological claim about *why* a dimorphic
circuit matters is a citation to the prior literature collected in sections
2-4 below. Anyone looking to this paper for a validated activity target will
not find one there — the anatomy is the target; the physiology has to come
from elsewhere.

### T-MALE-1  Central-brain dimorphic/sex-specific cell-type census

- **Quantity** — count of cell types in the central brain that are isomorphic
  (present, matched, indistinguishable between sexes), dimorphic (matched
  pair, consistent morphological/connectivity differences), male-specific, or
  female-specific, and the fraction of *neurons* (not types) this represents
- **Value** — of 7,319 cross-matched central-brain cell types: **114
  dimorphic**, **262 male-specific**, **69 female-specific** (remainder
  isomorphic), "totalling 4.8% of neurons in males and 2.4% in females" —
  quoted directly from the abstract. A second extraction pass of the same
  abstract returned 138 dimorphic / 289 male-specific / 71 female-specific /
  8,069 isomorphic types instead. The two disagree at the level of exact
  digits; both agree on order of magnitude and on the 4.8%/2.4% asymmetry. I
  could not resolve which is the precise, final Cell-version wording without
  the primary PDF (see Confidence).
- **Type** — steady-state
- **Method** — EM reconstruction (FIB-SEM, 8x8x8 nm isotropic), NBLAST
  morphology scoring + connectivity co-clustering for cross-sex cell-type
  matching, registration to FAFB/FlyWire
- **Observation model** — not applicable to our simulator directly; this is a
  structural census our `import_graph.py` node/edge counts should already be
  consistent with (166,691 vs our reported 166,700; MaleCNS uses `minconf
  0.5`, matching our import policy)
- **Conditions** — male: single MaleCNS specimen; female comparator:
  FlyWire/FAFB, a separate single female specimen (cross-animal, cross-sex
  comparison, not a within-animal control)
- **Source** — Cell 2026, DOI 10.1016/j.cell.2026.08.015; bioRxiv
  10.1101/2025.10.09.680999; PMC12636603
- **Confidence** — medium-high on the pattern (dimorphism concentrated in a
  small, higher-order fraction of cell types); low-medium on the exact digits
  above — two independent extraction passes of the same abstract disagree
  (114 vs 138 dimorphic types, 262 vs 289 male-specific, 69 vs 71
  female-specific, 4.8%/2.4% agrees both times). Recorded as a conflict per
  the README rule rather than silently picking one. A third, independent
  source (Janelia press release) corroborates the 262/114 figures, which is
  why they are listed first.

### T-MALE-2  Whole-CNS dimorphic/sex-specific neuron counts (not cell types)

- **Quantity** — individual-neuron-level (not cell-type-level) counts of
  sex-specific and dimorphic neurons across the *entire* CNS (brain + VNC),
  a different and larger scope than T-MALE-1's central-brain cell types
- **Value** — 1,427 male-specific neurons; 363 female-specific neurons; 924
  dimorphic neurons in the male matched to 811 dimorphic neurons in the female
- **Type** — steady-state
- **Method** — as T-MALE-1, extended to the full CNS including VNC
- **Observation model** — n/a (structural)
- **Conditions** — same cross-animal, cross-sex comparison as T-MALE-1
- **Source** — same as T-MALE-1
- **Confidence** — medium. Single extraction pass, not independently
  cross-checked against a second source the way T-MALE-1 was. Internally
  consistent (neuron counts are larger than type counts, as expected since
  each type contains multiple neurons).

### T-MALE-3  Fruitless/doublesex annotation census (the `fruDsx` field)

- **Quantity** — count of neurons annotated as fruitless-expressing (fru+),
  doublesex-expressing (dsx+), or both, at two confidence tiers
- **Value** — approximately 4,500-4,900 fru+ neurons (approximately
  2,700-2,800 "high confidence"), approximately 407-412 dsx+ neurons
  (approximately 330-332 "high confidence"), approximately 250 co-expressing
  both. Two extraction passes gave slightly different digits (4,505 vs 4,858
  fru+; 2,695 vs 2,804 high-confidence; 407 vs 412 dsx+; 332 vs 331
  high-confidence) — treat as a range, not exact counts, until checked against
  the primary annotation file. 73% of all fru/dsx annotations fall in the
  central brain; 9.5% of male central-brain neurons are fru+ (4.7% at high
  confidence).
- **Additional finding** — gene expression correlates strongly with the
  dimorphism call: 89% of male-specific central-brain neurons are fru+/dsx+,
  61% of dimorphic neurons are, but only 6.4% of isomorphic neurons are. This
  is a strong internal-consistency check on the `fruDsx` field itself, useful
  for validating our own import of it.
- **Type** — steady-state
- **Method** — light-microscopy driver line co-registration (fru-GAL4,
  dsx-GAL4/LexA lines) matched onto EM-reconstructed morphology; confidence
  tiers reflect matching quality
- **Observation model** — this is exactly the field the task names: our
  connectome annotations carry a `fruDsx` field so cells can be filtered by
  it. We do not currently import it in `src/import_graph.py` (which imports
  `superclass, type, class, side, subclass, neuromere, receptor` but not a
  fru/dsx column) — **this is an actionable gap** if fru/dsx-conditioned
  targets are to be used. I could not inspect the raw `annotations.feather`
  locally (no `data/` directory is present in this checkout) to confirm the
  exact column name and value set MaleCNS uses internally.
- **Conditions** — MaleCNS male specimen; FlyWire's own equivalent column is
  named `fru_dsx` (confirmed from `flyconnectome/flywire_annotations` on
  GitHub, introduced in annotation version 3.0.0, built by cross-validating
  FlyWire materialization 783 against MaleCNS v0.9) — so the two datasets'
  fru/dsx calls are not independent, they were partly cross-derived
- **Source** — Cell 2026 (as above); `flyconnectome/flywire_annotations`
  GitHub repository (changelog for v3.0.0/v3.1.0)
- **Confidence** — medium on exact counts (see range above); high on the
  qualitative structure (confidence-tiered fru/dsx calls exist and correlate
  with dimorphism); low on the exact local schema since it is unverified
  against our own data files.

### T-MALE-4  Optic lobe: dimorphism is rare but present, plus an anatomical sex difference

- **Quantity** — count of sex-specific/dimorphic optic-lobe intrinsic cell
  types, and eye size (ommatidia count) difference
- **Value** — out of 249 optic-lobe intrinsic types: **3 sex-specific**
  (Cm26, Tm26, Mi20), **1 dimorphic** (TmY21), plus **1 male-specific visual
  projection neuron** (LoVP92) that is not one of the 249 intrinsic types.
  Separately: the male eye has approximately 100 more ommatidia than the
  female eye.
- **Type** — steady-state
- **Method** — as T-MALE-1
- **Observation model** — n/a (structural); relevant to any separate
  visual-system model this project builds (per `bench/odor.py`'s note that
  the visual system needed its own graded-unit model), since a female-derived
  visual physiology target would need re-checking against these specific
  named cell types and the ommatidia-count difference before being assumed to
  transfer
- **Conditions** — cross-sex comparison, MaleCNS vs FlyWire/hemibrain optic
  lobe reconstructions
- **Source** — Cell 2026 (as above)
- **Confidence** — medium (single extraction pass; specific named types are
  plausible and internally consistent with the paper's "periphery is largely
  isomorphic" headline, since 4/249 is a small fraction)

### T-MALE-5  Dimorphism concentrates in a few hemilineages

- **Quantity** — fraction of hemilineages producing sex-specific/dimorphic
  neurons, and a worked example
- **Value** — approximately a quarter of hemilineages produce any
  sex-specific or dimorphic neurons, but just 8 of those (4% of all
  hemilineages) produce more than half of all such neurons. Named example:
  hemilineage DM4 produces 349 neurons in the male versus 205 in the female.
- **Type** — steady-state
- **Method** — as T-MALE-1, cross-referenced to hemilineage identity
  (developmental origin) annotations
- **Observation model** — n/a (structural/developmental)
- **Conditions** — cross-sex comparison
- **Source** — Cell 2026 (as above)
- **Confidence** — medium (single extraction pass)

### T-MALE-6  Cross-sex cell-type matching rate

- **Quantity** — fraction of MaleCNS neurons successfully matched to a
  counterpart cell type in an existing (female-derived, except MANC)
  connectome
- **Value** — 97.5% of MaleCNS neurons matched to FAFB/FlyWire, hemibrain, or
  MANC
- **Type** — steady-state
- **Method** — NBLAST + connectivity co-clustering, spatial transform between
  datasets
- **Observation model** — n/a (structural); this is the number that supports
  the "safe to transfer" default posture for anything **not** flagged
  dimorphic/sex-specific elsewhere in this file
- **Conditions** — cross-dataset, cross-sex (except the MANC comparison, which
  is male-male)
- **Source** — Cell 2026 (as above)
- **Confidence** — medium-high (specific, clean figure, internally consistent
  with the 95-97% isomorphic-type figures elsewhere in the paper)

### T-MALE-7  VNC sex differences (our connectome includes the nerve cord)

Our MaleCNS import is brain **and** ventral nerve cord ("first fly brain and
nerve cord connected through an intact neck" — project README). A companion,
same-consortium paper compares the male VNC (MANC) against a newly-aligned
female VNC (BANC), superseding an earlier, physically damaged female VNC
dataset (FANC).

- **Quantity** — count of sex-specific/dimorphic intrinsic-neuron (IN) types
  and cells in the VNC
- **Value** — 205 male-specific IN types (659 cells); 190 female-specific IN
  types (417 cells); 144 dimorphic IN types (587 cells in male MANC, 582 in
  female BANC); 2,344 isomorphic types in MANC vs 2,362 in BANC. Named
  examples: male-specific song-production core (pMP2, dPR1, vMS12, plus a
  newly identified feedback-inhibition neuron IN03B024 and 35 new candidate
  song-related types); DNp13, a *dimorphic* descending neuron controlling
  ovipositor extrusion (a female rejection behaviour) that targets **motor
  neurons in females but neurosecretory cells in males** — same neuron
  identity, different postsynaptic targets by sex; oviDNs (6 subtypes,
  mostly female-specific, egg-laying).
- **Type** — steady-state (the DNp13 differential-target finding is a
  circuit-switch fact, not a measured perturbation)
- **Method** — graph-matching connectome alignment ("ACDC" — Alternating
  Continuous and Discrete Combinatorial optimization — plus a weighted-Jaccard
  connectivity-similarity metric, "ConSim"), validated against MANC-vs-MaleCNS
  VNC alignment (male-male) as a same-sex individual-variability control
  before the cross-sex comparison
- **Observation model** — n/a (structural); purely connectomic — the authors
  explicitly state no electrophysiology, imaging, or behaviour was collected:
  "molecular and functional characterization of individual cell types will be
  required for confirmation"
- **Conditions** — MANC (male) vs BANC (female), both EM reconstructions
- **Source** — "Uncovering Sex Differences in the Drosophila Ventral Nerve
  Cord Through Connectome Alignment," bioRxiv 10.64898/2026.06.14.732053,
  PMC13307954, PubMed 42367857 (2026); shares authors with the MaleCNS Cell
  paper (e.g., Wei-Chung Allen Lee) and is presented as part of the same
  consortium effort
- **Confidence** — medium-high for the headline counts (single source, but
  internally detailed and consistent); the paper is explicitly anatomy-only

---

## 2. P1/pC1 neurons and courtship — persistent activity

This is the strongest dynamical target in this file: **P1 stimulation drives
a behavioural and neural state that outlasts the stimulus by minutes**, and
critically, the persistence is *not* a property of P1 itself — it is a
network property of a specific downstream population. A model that only
reproduces "P1 on -> behaviour on, P1 off -> behaviour off" has not
reproduced the phenomenon.

### T-MALE-8  P1 activation drives aggression that outlasts the stimulus by >=10 minutes

- **Quantity** — persistence of male-male aggression (lunging) after P1
  photostimulation (PS) ends
- **Value** — enhanced aggression was still observed when the barrier
  separating two males was not removed until 10 minutes after PS offset (i.e.
  persistence >= 10 min). n = 11 pairs for the barrier-delay experiment.
- **Type** — perturbation
- **Method** — optogenetic activation, CsChrimson (685 nm, 0.02 mW/mm^2) or
  ReaChR (530 nm, 10 Hz, 20 ms pulses, 0.2 mW/mm^2); also thermogenetic
  dTrpA1 (29-32 degC); stimulation 1-50 Hz, single 1-minute or repeated
  30-second blocks; P1a split-GAL4 driver labels 8-10 FruM+ P1 neurons per
  hemisphere (so roughly 16-20 per brain, consistent with the commonly cited
  "~20 P1 neurons/brain" figure)
- **Observation model** — behavioural scoring (lunging frequency) after a
  variable post-stimulus delay before the second fly is introduced/barrier
  removed; our extractor would need an equivalent "kick then measure a
  downstream behavioural proxy at delay D" protocol rather than reading
  instantaneous network state
- **Conditions** — adult **male** flies, paired male-male, courtship-chamber
  assay, 25 degC nominal fly husbandry
- **Source** — Hoopfer, Jung, Inagaki, Rubin, Anderson, "P1 interneurons
  promote a persistent internal state that enhances inter-male aggression in
  Drosophila," eLife 4:e11346 (2015). PMID 26714106.
  https://elifesciences.org/articles/11346
- **Confidence** — high (eLife, specific N and protocol reported; Anderson
  lab, as the task specifically asked to check)

### T-MALE-9  Wing-extension display decays with a characteristic half-life after P1 offset

- **Quantity** — half-life of wing-extension (courtship song display) decline
  after P1 photostimulation ends
- **Value** — t1/2 = 9 +/- 3 s in one condition versus t1/2 = 56 +/- 7 s in
  another (the fetch tool's summary did not let me confirm with certainty
  which value belongs to paired vs. solitary males — **this needs a check
  against the primary figure** before being used as a tight fitting target)
- **Type** — dynamic response
- **Method** — as T-MALE-8, behavioural scoring of wing-extension bouts
  post-stimulus
- **Observation model** — decay-curve fit to a behavioural time series, not
  directly a neural rate; would need a mapping from simulated motor-pathway
  activity to an assumed behavioural readout before comparison
- **Conditions** — adult male flies, as T-MALE-8
- **Source** — Hoopfer et al. 2015, eLife 4:e11346 (as above)
- **Confidence** — medium — the two-timescale finding is solid, the exact
  condition-to-value assignment is not confirmed by me and should be checked
  against the paper directly

### T-MALE-10  P1 itself does not show persistent activity — the persistence is downstream

- **Quantity** — whether the P1 population's own calcium activity outlasts
  optogenetic stimulation
- **Value** — P1a>GCaMP6s responses scaled linearly with stimulation
  frequency (10-50 Hz) but "activation of P1 neurons themselves did not
  appear to trigger long-lasting persistent activity within this population"
  — i.e., **no persistence at the P1 level itself**
- **Type** — dynamic response (a negative result, and an important
  modelling constraint)
- **Method** — two-photon calcium imaging, GCaMP6s, P1a driver
- **Observation model** — direct population calcium trace, no persistence to
  reproduce at this node
- **Conditions** — adult male flies
- **Source** — Hoopfer et al. 2015, eLife 4:e11346 (as above)
- **Confidence** — high (directly stated finding, not an inference)

### T-MALE-11  Silencing a P1-downstream population selectively suppresses persistent aggression

- **Quantity** — effect of silencing FruM+ neurons downstream of P1
  (TkFruM/Kir2.1) on post-stimulus aggression and courtship
- **Value** — silencing "strongly suppressed the enhancement of lunging"
  after PS offset, but paradoxically *increased* wing-extension in the same
  post-stimulation window — i.e. aggression-persistence and courtship-song
  pathways downstream of P1 dissociate under this manipulation
- **Type** — perturbation
- **Method** — genetic silencing with Kir2.1 (constitutive hyperpolarization)
  crossed onto a FruM+ intersectional driver, same behavioural assay as
  T-MALE-8
- **Observation model** — behavioural scoring, before/after silencing,
  same-animal or matched-cohort comparison
- **Conditions** — adult male flies
- **Source** — Hoopfer et al. 2015, eLife 4:e11346 (as above)
- **Confidence** — medium-high (clear qualitative direction; exact p-values
  for this specific comparison were not resolved by my extraction)

### T-MALE-12  pCd neurons carry the persistence; decay time constant far exceeds P1's own

- **Quantity** — decay time constant of calcium activity in P1 versus its
  "follower" population pCd, after optogenetic P1 stimulation ends
- **Value** — **P1 decay tau ~= 15 s; pCd decay tau ~= 83 s**, matching the
  minutes-long timescale of the persistent behavioural state. This is the
  single most citable dynamical number in this file: a ~5.5x longer decay
  constant in a specific, named downstream population, discovered precisely
  by looking for cells whose activity outlasts the driving stimulus.
- **Type** — dynamic response
- **Method** — volumetric calcium imaging (GCaMP6s) of ~2,000 neurons
  simultaneously during and after optogenetic P1 photostimulation, screening
  for "follower" cells with above-baseline activity long after stimulus
  offset
- **Observation model** — exponential decay fit to population calcium trace
  following stimulus offset; our extractor needs the same "stimulate briefly,
  then fit the decay of downstream activity" protocol — an instantaneous
  rate readout at t=0 will not capture this at all
- **Conditions** — adult male flies, optogenetic (opsin/protocol as in
  Hoopfer et al., same lab)
- **Source** — Jung, Kennedy, Chiu, Mohammad, Claridge-Chang, Anderson,
  "Neurons that Function within an Integrator to Promote a Persistent
  Behavioral State in Drosophila," Neuron 105(2):322-333 (2020). Preprint:
  bioRxiv 10.1101/735985. https://www.sciencedirect.com/science/article/pii/S0896627319309237
- **Confidence** — high for the qualitative/order-of-magnitude claim (P1 decays
  an order of magnitude faster than pCd); medium for the exact tau values,
  which came from a search-summary rather than a primary-figure read and
  should be checked directly against the paper before being used as a tight
  numeric target

### T-MALE-13  pCd is required for P1-evoked persistent aggression and courtship

- **Quantity** — effect of silencing pCd neurons on P1-evoked persistent
  behaviour
- **Value** — pCd neurons are "required for P1-evoked persistent courtship
  and aggression" (qualitative; I could not retrieve the exact silencing
  method or effect size for this specific manipulation from what I was able
  to fetch — flagged as not found, see below)
- **Type** — perturbation
- **Method** — not confirmed (likely Kir2.1 or shibire-ts genetic silencing
  of the pCd driver, paired with the same optogenetic-P1 + delayed-assay
  protocol as T-MALE-8; not verified)
- **Observation model** — not confirmed
- **Conditions** — adult male flies
- **Source** — Jung et al. 2020, Neuron 105(2):322-333 (as above)
- **Confidence** — low-medium on specifics; the qualitative "required for"
  claim is stated confidently in secondary summaries but I was not able to
  pull the primary numbers. **Action: fetch the primary PDF/HTML directly
  before fitting anything to this number.**

### T-MALE-14  Female pC1 (pC1d/e, "pC1-Alpha") shows an analogous persistent state — FEMALE, use with caution

The female counterpart circuit, included here because it is the closest
functional/developmental homolog of male P1 (both are dsx+/fru+ pC1-lineage
neurons) and because the task specifically asks for cross-sex context.
**This entire target is measured in females; do not apply it to a male model
without treating the sex difference as a free hypothesis, not a given.**

- **Quantity** — duration/decay of persistent neural activity and behaviour
  after optogenetic activation of pC1-Alpha (a single pC1d + single pC1e
  neuron per hemisphere, 4 cells/fly)
- **Value** — pan-neuronal imaging (47,882 ROIs across 28 brains; 4,254
  significant) found a persistent-activity response type occupying 4.3% of
  imaged volume, present in >30% of pC1-Alpha-activated flies and 24.7x more
  voxels than controls; activity persisted >=5 min post-offset, still present
  at 10 min, decaying further by t=3 min and t=6 min. Behaviourally,
  female shoving/chasing persisted up to 30 min at a 3-minute stimulus delay;
  receptivity/copulation was highest with no delay (75% copulated within 5
  min at 0- and 3-minute delays). Stimulation protocols: 5-minute continuous
  ReaChR (primary), also tested at 2 min and 30 s.
- **Type** — dynamic response (persistence) and perturbation (activation ->
  behaviour change)
- **Method** — whole-brain/pan-neuronal volumetric calcium imaging (light-field
  or similar), plus targeted imaging of Dsx+ cells (273 ROIs/16 flies vs 192
  ROIs/11 controls) and Fru+ cells (9 flies vs 5 controls); ReaChR
  optogenetics with all-trans-retinal feeding
- **Observation model** — same decay-fit requirement as T-MALE-12
- **Conditions** — **adult FEMALE flies**, virgin, paired with a male target
  or isolated depending on assay arm
- **Source** — Deutsch, Pacheco et al. (Murthy and Seung labs, Princeton),
  "The neural basis for a persistent internal state in Drosophila females,"
  eLife 9:e59502 (2020). https://elifesciences.org/articles/59502
- **Confidence** — medium-high on the qualitative persistence finding
  (multiple independent lines of evidence within the same paper: pan-neuronal,
  Dsx+-targeted, and Fru+-targeted imaging all show it); medium on exact
  numbers (single extraction pass). **Sex flag: FEMALE — see warnings.**

### T-MALE-15  pC1-Int silencing reduces female receptivity — FEMALE

- **Quantity** — effect of silencing pC1-Int neurons on female receptivity and
  song-response
- **Value** — silencing (tetanus toxin, TNT) "diminished responses to male
  song" and reduced receptivity; Cox proportional-hazards regression p =
  6.3e-6
- **Type** — perturbation
- **Method** — genetic silencing (TNT) crossed onto pC1-Int driver; behavioural
  receptivity assay with survival/hazard-style statistics on latency to
  copulation
- **Observation model** — time-to-event (copulation latency) rather than a
  rate; would need a matching behavioural-proxy layer, not a raw spike-rate
  comparison
- **Conditions** — **adult FEMALE flies**
- **Source** — Deutsch, Pacheco et al. 2020, eLife 9:e59502 (as above)
- **Confidence** — medium-high (specific statistic reported). **Sex flag:
  FEMALE.**

### Fruitless/doublesex circuits beyond the census (task item 3)

Most of what is *measured* (as opposed to anatomically catalogued) about
fru+/dsx+ neuron activity is already covered above and in section 4 below —
P1, pCd, pC1, mAL, and the aSP-f/aSP-g pair are all fru+ and/or dsx+ cell
types with activity data. Two additional qualitative circuit facts from the
connectomic literature, included here because they describe *how* fru+
circuits are wired rather than just that they exist:

- A male-specific GABAergic neuron, **mAL**, sits in a disinhibitory loop
  described from hemibrain connectomic analysis: an auditory neuron **vPN1**
  inhibits **mAL**, which inhibits **pC1** — i.e., mAL is normally holding pC1
  down, and disinhibiting it (via vPN1) is proposed as a switch between
  courtship and aggression states. I could not obtain a clean primary
  citation with authors/year for this specific circuit diagram from what I
  fetched (it appeared in a secondary discussion of hemibrain connectomic
  work on the courtship-song pathway) — **treat as a lead to verify, not a
  sourced target.**
- **vAB3** (excitatory, fru+) and **mAL** (inhibitory, fru+) both receive
  gustatory input and feed forward into the third-order pheromone-processing
  layer (aSP-g in females) described in section 4, per a review of
  multimodal chemosensory courtship circuits (Clowney/Kim-type review
  literature; exact citation not pinned down with full confidence).
- **Confidence for both of the above: low** — included for completeness
  because the task specifically asked about fruitless/doublesex circuit
  function, but flagged clearly as needing a primary-source check before
  being treated as a citable target.

---

## 3. cVA pheromone pathway (DA1) — directly usable, since we already drive `ORN_DA1`

The throughline of this section: **the periphery (ORN, and the second-order
DA1 projection neuron) is sex-invariant; the dimorphism appears at the third
synapse**, in the lateral horn. For a model that drives `ORN_DA1` as a Poisson
source (as `bench/odor.py` does), this means the ORN and immediate PN response
should be modelled identically regardless of which sex's data informed it —
but anything claiming a *behavioural* or *decision-layer* consequence of that
drive is sex-specific from the third-order neuron onward.

### T-MALE-16  DA1 projection neuron response to cVA is identical in both sexes

- **Quantity** — whether second-order DA1 projection neuron (PN) responses to
  cVA differ between males and females
- **Value** — "first-order ORNs and second-order PNs both express... fruitless
  ...but appear functionally isomorphic" / DA1 PNs are "activated by cVA
  equally in male and female brain." This is a **sex-invariant baseline** —
  useful precisely because it tells us where the ORN_DA1 pathway's measured
  properties transfer safely across sex, before the signal reaches the
  lateral horn.
- **Type** — steady-state
- **Method** — GFP photoactivation to label single fru+ DA1 PNs, followed by
  electrophysiological recording
- **Observation model** — direct PN spike/voltage response to cVA puff, no
  special sex-conditioning needed in an extractor for this specific node
- **Conditions** — adult male and female flies compared directly, in vivo
- **Source** — Datta, Vasconcelos, Ruta, Luo, Wong, Demir, Flores, Balonze,
  Dickson, Axel, "The Drosophila pheromone cVA activates a sexually dimorphic
  neural circuit," Nature 452:473-477 (2008). PMID 18305480.
  https://www.nature.com/articles/nature06808 ; extended by Ruta, Datta,
  Vasconcelos, Freeland, Looger, Axel, "A dimorphic pheromone circuit in
  Drosophila from sensory input to descending output," Nature 468:686-690
  (2010). PMID 21124455.
- **Confidence** — high (consistent across two independent papers from
  overlapping authors, and consistent with the double-dissociation logic of
  T-MALE-17/18 below, i.e. dimorphism has to start somewhere downstream of an
  isomorphic input for the third-order double dissociation to make sense)

### T-MALE-17  Third-order lateral-horn neurons: a clean double dissociation by sex

This is the actual locus of cVA's sexual dimorphism, and a strong,
quotable perturbation-grade target because it is a *natural* double
dissociation (sex, not a lesion, is the manipulation) with electrophysiology
on both sides.

- **Quantity** — probability and magnitude of a cVA-evoked response in two
  reciprocal third-order lateral-horn neuron (LHN) clusters, aSP-f and aSP-g
- **Value** — **aSP-f** (identified in males): cVA-responsive in 20/37 males
  vs. 1/34 females; peak firing rates 4-36 Hz; narrow odour tuning (high
  lifetime sparseness). **aSP-g** (identified in females): cVA-responsive in
  11/15 females vs. 1/17 males; weaker, broader-tuned responses; DA1-evoked
  depolarization 12.3 +/- 2.8 mV (n=9); synaptic latency to DA1 input 1.8 +/-
  0.3 ms. Both clusters exist anatomically in both sexes — the dimorphism is
  in which one is functionally wired to respond, not in cell presence/absence.
- **Type** — steady-state (tuning/response-probability comparison; the
  causal manipulation is sex itself, which cannot be perturbed within an
  animal, so this is reported as steady-state per the README's categories
  even though it functions like a lesion study)
- **Method** — in vivo whole-cell patch-clamp electrophysiology with biocytin
  fills and morphological reconstruction; local acetylcholine iontophoresis
  onto DA1 for controlled glomerular stimulation; genetic mosaic analysis
  (MARCM) to confirm cell identity
- **Observation model** — spike-rate and subthreshold-depolarization readout
  per identified cell, cross-referenced to confirmed morphological identity;
  our extractor would need to identify the equivalent MaleCNS cell type(s)
  (aSP-f should exist as a named/typed cluster we can select on) and compare
  only within-sex, i.e. we can only ever test the male (aSP-f) side of this
  dissociation against our model
- **Conditions** — adult male and female flies, in vivo, directly compared
- **Source** — Kohl, Ostrovsky, Frechter, Jefferis, "A bidirectional circuit
  switch reroutes pheromone signals in male and female brains," Cell
  155(7):1610-1623 (2013). PMID 24360281. PMC3898676.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3898676/
- **Confidence** — high (large N for a patch-clamp study — 130 wild-type
  recordings, 288 total across genotypes; FDR-adjusted p<0.01; consistent with
  the anatomical dimorphism reported in Datta 2008/Ruta 2010)

### T-MALE-18  FruM is necessary for the male-specific lateral-horn arbor

- **Quantity** — effect of disrupting fruitless function on the male-specific
  axonal branch of DA1 PNs in the lateral horn
- **Value** — the male-specific branch "depends on normal fru gene function"
  — loss of FruM in DA1 PNs (and other fru+ cells) eliminates the
  male-specific arbor. The full traced circuit (Ruta et al. 2010) is
  minimally 4 neurons across 3 synapses (ORN -> PN -> third-order LHN ->
  descending neuron to VNC), of which 3 of the 4 are "overtly dimorphic," and
  it defines a male-specific neuropil integrating multiple sensory modalities
  before sending output to the VNC.
- **Type** — perturbation (genetic loss-of-function)
- **Method** — MARCM genetic mosaics removing fru function in single labelled
  neurons; photoactivatable-GFP tracing; laser microlesioning to test circuit
  necessity; combined electrophysiology and optical imaging
- **Observation model** — anatomical (arbor present/absent) rather than a
  firing-rate readout; relevant to our model only if it ever represents
  fru-genotype as a structural variable rather than treating the wiring
  diagram as fixed
- **Conditions** — adult male flies (mosaic clones), compared to wild-type
  male and to female
- **Source** — Datta et al. 2008, Nature 452:473-477; Ruta et al. 2010,
  Nature 468:686-690 (both as above)
- **Confidence** — high (foundational, repeatedly cited result, consistent
  across both papers)

### T-MALE-19  Peripheral cVA receptors differ in sensitivity, not just downstream wiring

- **Quantity** — relative sensitivity of the two cVA-responsive odorant
  receptors, Or67d and Or65a, to cVA concentration
- **Value** — "a relatively large amount of cVA was required to activate
  Or65a, while a small amount of cVA was enough to stimulate Or67d" — i.e.
  Or67d (feeding into DA1) is high-sensitivity/low-threshold, Or65a (feeding
  into VA1lm) is low-sensitivity/high-threshold. **I could not find specific
  Hz firing-rate values for either receptor's dose-response curve** despite a
  dedicated search — flagged as not found (see below).
- **Type** — steady-state
- **Method** — single-sensillum recording (SSR) from T1 sensilla (Or67d) and
  the corresponding Or65a sensillum
- **Observation model** — dose-response curve, peak firing rate vs.
  concentration; without the actual Hz numbers this cannot yet be turned into
  a tight target, only a qualitative ordering (Or67d more sensitive than
  Or65a)
- **Conditions** — sex not specified in what I could retrieve — cVA is
  "detected by both sexes via apparently identical neural circuits in their
  antennae" per multiple sources, so this is expected to be sex-invariant,
  consistent with T-MALE-16
- **Source** — van der Goes van Naters and Carlson, Current Biology 17(7),
  2007 (title/venue from a secondary summary, not independently verified by
  direct fetch — treat citation details as medium-confidence)
- **Confidence** — medium on the qualitative ordering; low on any numeric
  value, because no numeric value was actually recovered

### T-MALE-20  Mating state gates cVA attraction in females via Or65a-mediated inhibition of DA1 — FEMALE, state-dependent

A useful example of a perturbation target that is both sex-specific and
state-dependent (mating status), layered on top of the otherwise
sex-invariant DA1/ORN_DA1 pathway (T-MALE-16).

- **Quantity** — effect of mating on female behavioural attraction to cVA, and
  the circuit mechanism
- **Value** — virgin females are attracted to cVA; shortly after mating,
  females are no longer attracted. Mechanism: activating Or65a-expressing
  OSNs (a separate receptor/glomerulus from Or67d/DA1, engaged post-mating,
  e.g. by a male-transferred cue) inhibits the DA1 glomerulus response to
  cVA; silencing Or65a in mated females restores cVA attraction.
- **Type** — perturbation (mating-state manipulation; also a silencing
  perturbation on Or65a)
- **Method** — behavioural attraction assay pre/post mating; functional
  calcium imaging of the DA1 glomerulus while co-activating Or65a; genetic
  silencing of Or65a
- **Observation model** — glomerular-level calcium imaging (population, not
  single-cell) with and without a simulated "mated state" input; our model
  has no mating-state variable at present, so this target cannot be applied
  without first adding one
- **Conditions** — **adult FEMALE flies**, virgin vs. mated
- **Source** — Lebreton, Trona, Borrero-Echeverry, Bilz, Grabe, Becher,
  Carlsson, Hansson, Witzgall, Bengtsson, Sachse, "Love makes smell blind:
  mating suppresses pheromone attraction in Drosophila females via Or65a
  olfactory neurons," Scientific Reports 4:7119 (2014).
  https://www.nature.com/articles/srep07119
- **Confidence** — medium-high on the qualitative circuit logic (clear,
  specific mechanism reported); not independently cross-checked against a
  second source. **Sex flag: FEMALE, and state-dependent (mating status) —
  double caution before use.**

### Background: cVA's behavioural valence itself flips by sex

Not a numeric target, but essential context found repeatedly across the
above sources and worth recording explicitly: cVA is transferred from male to
female during mating and is aversive/aggression-modulating to rival
courting males, while it promotes receptivity in virgin females exposed to a
courting male (classic result, e.g. Kurtovic, Widmer, Dickson-era work
referenced in review articles surfaced during this search, not independently
re-verified here). The **hardware is shared (Or67d -> DA1 -> PN, sex-invariant
per T-MALE-16), the decision made from it is not** — this is the single
clearest illustration in this whole file of why a male connectome cannot
just inherit a female-measured decision-layer target, even when the
sensory-layer target is safe to inherit.

---

## 4. Sex-mismatch warnings (targets and parameters already in this project)

This is the section the task calls one of the main outputs. Each item below
names a specific number or citation **already present in this repository**,
what sex (or life stage) it actually came from, and what that implies.

1. **`src/params.py`: `PUBLISHED_WEIGHT_PER_SYNAPSE_MV = 0.275` and the
   mean-out-degree-~72 comparison figure (also repeated in `theory-review.md`
   item 6, the 1/sqrt(K) scaling discussion) — sourced from Shiu et al. 2024
   (Nature, "A Drosophila computational brain model reveals sensorimotor
   processing"), whose structural substrate is the FlyWire connectome ("the
   model was implemented... using all Flywire neurons"), built from FAFB, a
   single **female** specimen.** This is the cleanest, highest-priority
   mismatch in our own pipeline: our single free parameter's original fitting
   context, and the connectivity-density baseline we compare our own
   mean-out-degree (153.5) against, both come from a female brain, while
   MaleCNS is male. `params.py` already flags that this weight "does not
   transfer to this dataset" for connection-completeness reasons (minconf 0.5
   vs FlyWire's >=5-synapse convention) — it does not currently flag the sex
   difference as a *separate*, additional reason not to expect transfer.
2. **The hemibrain connectome** (Scheffer et al. 2020), the other major EM
   dataset that most published Drosophila connectivity claims in the wider
   literature are benchmarked against, **is also female** (a single 5-day-old
   female Canton-S x w1118 fly). Any future target file in this collection
   that cites "hemibrain connectivity says X" inherits the same female-vs-our-
   male mismatch as FlyWire, even when the citing paper does not mention
   FlyWire at all.
3. **`src/params.py`: `V_REST_MV`, `V_RESET_MV`, `V_THRESH_MV`,
   `TAU_MEMBRANE_MS`** — cited to Kakaria and de Bivort 2017. On inspection
   this is not itself a primary electrophysiology paper: its actual title is
   "Ring Attractor Dynamics Emerge from a Spiking Model of the Entire
   Protocerebral Bridge" (Frontiers in Behavioral Neuroscience), and it is a
   **computational modelling paper** that assigns "-52 mV in all neurons" /
   "-45 mV" etc. as generic values "consistent with various Drosophila
   measurements," without identifying whose measurements, in which cell
   type, or in which sex. **These four foundational parameters of our own
   simulation have no traceable sex (or even cell-type) provenance** —
   a different and in some ways more basic problem than a female/male
   mismatch: we do not actually know what the numbers describe.
4. **`src/params.py`: `TAU_SYNAPSE_MS = 5.0`** — cited to Jürgensen et al.
   (IOP Neuromorphic Computing and Engineering, DOI 2634-4386/ac3ba6). This
   paper models the Drosophila **larval** olfactory system ("A neuromorphic
   model of olfactory processing and sparse coding in the Drosophila larva
   brain"), not the adult CNS, and is itself a modelling paper reusing
   assumed time constants rather than reporting a new adult measurement. Sex
   is not a meaningful category for a larval connectome in the way it is for
   an adult (pre-differentiation). This is a **life-stage mismatch**, the
   same family of risk as a sex mismatch: a parameter borrowed from a
   preparation that does not match ours, just on a different axis.
5. **`src/params.py`: `REFRACTORY_MS = 2.2`** — cited to "Lazar et al.,
   eLife," DOI 10.7554/eLife.62362. That DOI resolves to "Accelerating with
   FlyBrainLab the discovery of the functional logic of the Drosophila brain
   in the connectomic and synaptomic era" — a **software/platform paper**,
   not a refractory-period measurement. It loads existing connectome
   datasets (including one explicitly built from "22,828 female Drosophila
   neurons" from FlyCircuit) but does not itself report new fly
   electrophysiology. The true empirical origin of the 2.2 ms figure is not
   traceable through this citation and should be tracked down before this
   parameter is treated as a validated, sexed measurement.
6. **`src/params.py`: `DELAY_MS = 1.8`** — cited to Paul et al. 2015
   (Frontiers in Cellular Neuroscience). This paper ("Bruchpilot and
   Synaptotagmin collaborate to drive rapid glutamate release and active
   zone differentiation") measures synaptic delay at the **larval
   neuromuscular junction** (motor-neuron-to-muscle synapse) in **male
   third-instar larvae** — so, unusually in this list, the sex label is
   actually male, matching our model. What does *not* match is developmental
   stage (larva, not adult) and synapse location/type (peripheral
   glutamatergic NMJ, not a central synapse). Flagged for the same reason as
   item 4: a mismatch on a non-sex axis, but on one of our four foundational
   single-synapse parameters, so worth tracking in the same list.
7. **The mushroom body sparse-coding / APL regression test** — the "first
   causal validation this model has passed" per `theory-review.md` (APL
   block: 5.6% -> 89.2% Kenyon-cell recruitment), built on Lin et al. 2014
   (Nature Neuroscience, "Sparse, decorrelated odor coding...") and Amin et
   al. 2020 (eLife, "Localized inhibition in the Drosophila mushroom body").
   **I could not confirm the sex of flies used in either paper.** The Amin
   2020 methods, specifically checked, describe husbandry and imaging
   preparation but never state fly sex or age — "a notable omission" in the
   paper itself, not just a gap in my search. Lin 2014's methods were behind
   a login wall I could not get past. Common lab convention for mushroom-body
   dissection/imaging in this literature leans female (easier dissection,
   standard virgin-female stocks), but that is an inference from convention,
   not a confirmed fact for these two specific papers — **do not treat this
   as settled**. Given this project explicitly holds up the APL regression
   test as its best-validated result, resolving this is worth the primary-text
   check.
8. **The eNeuro 2022 nonspiking-local-interneuron paper** (Schenk and Gaudry,
   informing `theory-review.md` item 1, our plan to make antennal-lobe LNs
   graded rather than spiking) — the methods state flies were bred from
   "male and female flies... raised and crossed" (a husbandry statement about
   the breeding stock), but I could not confirm the sex of the flies actually
   used for the electrophysiology/imaging recordings themselves. Flagged as
   unconfirmed, not assumed.
9. **Structural risk is concentrated, not uniform** (restating the top-of-file
   point in warning form): MaleCNS-to-female cross-matching succeeds for
   97.5% of neurons (T-MALE-6), and the periphery is "largely isomorphic," but
   the ~2.5-4.8% that fails to match sits disproportionately in higher-order
   centers — courtship (P1/pC1), the lateral-horn pheromone layer
   (aSP-f/aSP-g), and specific VNC song/reproductive circuits (T-MALE-7).
   Any future target drawn from "central complex," "mushroom body output
   neuron," or general sensory-periphery physiology is a priori lower risk
   than anything touching the lateral horn, SMP/SIP, or VNC interneurons
   named in sections 1-3 above.
10. **Optic lobe**: a female-derived visual-physiology target should be
    checked against T-MALE-4 (3 sex-specific + 1 dimorphic intrinsic cell
    type, 1 male-specific VPN, ~100-ommatidia eye-size difference) before
    being assumed to transfer to this project's separate visual-system model.

---

## 5. Direct cross-references: female-measured targets already in this collection

Three sibling domain files (`whole-brain.md`, `prior-validation.md`,
`measurement-protocols.md`) did not exist when this task started and appeared
in `docs/targets/` while this file was being researched. Reading them after
the fact turns up concrete, explicitly-female-tagged targets that can be
named directly rather than warned about only in the abstract — exactly the
cross-reference the task asked for:

- **`whole-brain.md` T-WB-2 / T-WB-14** — antennal-lobe projection-neuron
  resting potential (-47.8 mV whole-cell / -57.8 mV cell-attached, N=12),
  explicitly "adult, female" (Gouwens & Wilson 2009). `whole-brain.md` itself
  leans on this number for the "how close to threshold do central neurons
  sit" question that is central to this project's own operating-point work
  (`lab-notebook.md`), but does not itself flag the sex. The antennal lobe is
  squarely "sensory periphery" — the part of the brain the MaleCNS paper
  reports as "largely isomorphic" (T-MALE-6) — so the a priori risk here is
  plausibly low, but it is unconfirmed low, not verified low.
- **`whole-brain.md` T-WB-6, T-WB-7, T-WB-8** — Aimon et al. 2023 whole-brain
  imaging during walking (brain-wide R²=0.194 walk correlation; divergent
  dopaminergic/octopaminergic vs. serotonergic response; the brain-VNC
  transection perturbation), explicitly "tethered adult female flies...84
  adult female flies overall across the study." T-WB-8 is flagged in that
  file as its strongest single result, and it is a perturbation (surgical),
  which the README ranks above steady-state numbers — meaning it is exactly
  the kind of target likely to get reused first. None of these three are
  courtship/aggression circuits, so lower dimorphism risk than sections 2-3
  above, but they are brain-wide averages, and T-MALE-1/T-MALE-5 show
  dimorphic neurons concentrate in higher-order centers that any brain-wide
  average necessarily includes rather than excludes.
- **`whole-brain.md` T-WB-12 / T-WB-13** — behavioural-state modulation of the
  ON-motion pathway (T4 and its inputs Mi1, Tm3, Mi4, Mi9); that file already
  marks sex as "not confirmed." Cross-checked against this file's own
  optic-lobe census (T-MALE-4): none of T4, Mi1, Tm3, Mi4, or Mi9 are among
  the specific types the MaleCNS paper names as sex-specific or dimorphic
  (Cm26, Tm26, Mi20, TmY21, LoVP92). Reassuring, not conclusive — T-MALE-4's
  census covers 249 "intrinsic" optic-lobe types and may not be exhaustive
  for this exact pathway, and an anatomically isomorphic cell type can still
  carry an unmeasured sex difference in physiology, exactly the pattern
  T-MALE-17 demonstrates for the DA1 pathway (identical PN anatomy, dimorphic
  third-order response). Lower risk, not risk-free.
- **`prior-validation.md` T-PRIOR-006** — real-fly straight-walking leg-joint
  kinematics used to validate NeuroMechFly v2, explicitly "wildtype (PR)
  **female** adult Drosophila melanogaster." Body/motor kinematics rather
  than a central neural-circuit target, and walking gait is not an
  established sexually-dimorphic behaviour, but named here for completeness
  since it is an explicit female tag already sitting in the collection.

**Process note.** Sections 1-4 of this file were compiled from literature
search alone, before any sibling domain file existed to check against. This
section exists only because the sibling files happened to land during this
session. If more domain files are added later, they should be checked
against this one the same way, and this file should be checked against them
again — the cross-reference is not a one-time pass, and I cannot rule out
that further female-tagged targets already sit in `whole-brain.md` or
`prior-validation.md` beyond the ones named above (in particular, several
entries in both files explicitly say sex was "not confirmed" — those are not
listed here as female, but they are not confirmed male-safe either).

---

## What I could not find

Listed explicitly, per the task's instruction:

- The exact, final published-Cell-version wording of the headline dimorphism
  census (T-MALE-1): two extraction passes of what should be the same
  abstract gave different digits (114/262/69 vs 138/289/71 for
  dimorphic/male-specific/female-specific types). I was not able to obtain
  and read the primary PDF text directly (tool fetches of biorxiv.org and
  cell.com either redirected through a summarizing layer or returned
  HTTP 403/429).
- Any quantitative firing-rate (Hz) dose-response values for Or67d or Or65a
  responding to cVA (T-MALE-19) — only a qualitative sensitivity ordering was
  recovered despite a dedicated search.
- The exact silencing method and effect size for the pCd-required-for-
  persistence claim (T-MALE-13) — the qualitative claim is well supported,
  the specific numbers are not, in what I was able to retrieve.
- Confirmed fly sex for the two papers underlying this project's best-
  validated existing result, the APL sparse-coding regression test (Lin et
  al. 2014; Amin et al. 2020) — see warning 7. This feels like the highest-
  value single follow-up: it bears on a result the project already treats as
  load-bearing.
- Confirmed fly sex for the eNeuro 2022 nonspiking-LN electrophysiology/
  imaging experiments specifically (as opposed to the breeding stock) — see
  warning 8.
- The exact local schema of the `fruDsx` annotation field in our own MaleCNS
  data files: no `data/` directory exists in this checkout, so I could not
  open `annotations.feather` and confirm column name, value set, or how it
  relates to `superclass`/`class`/`subclass`, which are the fields
  `src/import_graph.py` currently imports. I relied on the equivalent,
  confirmed `fru_dsx` column documented for FlyWire (built via cross-
  validation against MaleCNS v0.9) as the closest verifiable analogue.
- A primary, authored citation for the vPN1-\|mAL-\|pC1 disinhibitory
  courtship/aggression switch, and for the vAB3/mAL gustatory-integration
  claim, mentioned qualitatively at the end of section 2 — both came from
  secondary discussion in search results without a clean authors/year/DOI I
  could verify directly.
- Any MaleCNS-reported count of P1 or pC1 neurons *within the MaleCNS
  connectome itself* (as opposed to the older hemibrain/light-microscopy
  figure of ~20 P1 neurons/brain used throughout section 2). This would be a
  useful direct sanity check against our own imported `cell_type` array once
  fru/dsx and cell-type-name annotations are both available locally.
- Whether the MaleCNS v1.0 release notes page documents annotation-schema
  changes in detail — the live release-notes page I fetched only gave
  one-line summaries ("minor proofreading changes," "refinement of neuron
  annotations") for v1.0 and v0.9, with no field-level changelog visible to
  the fetch.
