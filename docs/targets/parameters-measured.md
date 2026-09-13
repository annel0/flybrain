# Measured parameters

This file is the mirror image of `README.md` in this folder. That file collects
**targets** — invariants a simulation should reproduce, to be matched by
adjusting free parameters. This file collects **direct measurements of the
parameters themselves**, so that fewer numbers ever have to be *found* by
fitting in the first place. Every entry below that says "measured" is a
dimension that can be pinned before the optimizer ever runs; every entry that
says "not measured" is a dimension the optimizer is stuck carrying, and is
worth knowing about for that reason alone.

The model this is feeding currently gives all 166,700 neurons one shared set
of membrane constants (Kakaria & de Bivort 2017: resting potential −52 mV,
threshold −45 mV, membrane time constant 20 ms, synaptic time constant 5 ms,
refractory period 2.2 ms) and reduces every synapse to a sign. The question
behind every section below is the same: how much of that crudeness is
actually optional, given what has been measured?

**Note on sourcing.** Numbers below come from a mix of (a) content retrieved
directly from the primary paper or a secondary description of it in this
research pass — these are cited with the specific finding stated the way the
source stated it, and (b) well-established facts this agent is highly
confident of from general training knowledge but could not re-confirm against
the primary text this session (several publisher sites — `jneurosci.org`,
`cell.com`, `pnas.org`, `jbc.org` — returned HTTP 403 to automated fetches).
Anything in the second category is explicitly flagged "(not independently
re-verified this session)" and should be checked against the primary source
before being hard-coded as a model constant. A dedicated background search for
receptor kinetics (item 1 below) was launched but had not returned by the time
this file was written; if it surfaces materially different numbers they
supersede the ones here.

---

## 1. Receptor identity and kinetics

The single most useful fact in this whole section: **identity, mechanism
class (ionotropic/fast vs. metabotropic/slow), and sign are well established
for all five systems below.** That alone is a strict improvement over a
uniform ± sign and does not require new measurements — it requires only
implementing what is already known. What is *not* well established, for any
of these receptors, is a full quantitative kinetic description (rise τ, decay
τ, reversal potential) measured natively in identified Drosophila central
neurons, as opposed to inferred by homology or measured in a heterologous
system.

### 1.1 Nicotinic acetylcholine receptor (nAChR)

- **Subunit composition — partially known.** Drosophila has 7 α subunits
  (Dα1–Dα7) and 3 β subunits (Dβ1–Dβ3). Croset, Treiber & Waddell 2018 (eLife
  7:e34550), single-cell RNA-seq of 10,286 midbrain cells (28–30 clusters from
  8 replicates × 80–100 pooled brains), detected all 7 α subunits and 2 of the
  3 β subunits (β1, β2), with clearly cell-type-specific patterns: α1, α5,
  α6, α7 broadly expressed; α2, α3, α4 more restricted; α3 broadly expressed
  but specifically absent from Kenyon cells; β1 expressed in roughly twice as
  many cells as β2. This tells us subunit expression is genuinely
  heterogeneous across cell types, which is exactly what a uniform model
  misses — but it does not tell us actual subunit *stoichiometry* per neuron
  (which subunits co-assemble into one functional pentamer in vivo), which
  determines the real biophysics and is not resolved for almost any
  identified Drosophila central neuron.
- **Mechanism — measured.** Ionotropic, cation-non-selective Cys-loop
  channel; the dominant fast excitatory receptor in the fly CNS (cholinergic
  neurons are the majority "excitatory" class in connectome-wide
  neurotransmitter predictions).
- **Reversal potential — not directly measured for native fly CNS synapses.**
  Mechanistically expected near 0 mV, as for any cation-non-selective Cys-loop
  channel (by homology with the same result in every other characterized
  nAChR, vertebrate or invertebrate). No paper found in this pass reports a
  measured reversal potential from a full I-V curve in an identified
  Drosophila central neuron; whole-cell recordings (e.g. Su & O'Dowd 2003 J
  Neurosci; Gu & O'Dowd 2006 J Neurosci) hold cells at a fixed negative
  potential to isolate inward current rather than mapping reversal.
- **Kinetics — partially known.** Su & O'Dowd 2003 (J Neurosci 23:9246,
  cultured pupal-derived Drosophila CNS neurons, including Kenyon cells) and
  Gu & O'Dowd 2006 (J Neurosci 26:265, in situ, adult) both establish that
  fast miniature EPSCs in Kenyon cells are mediated by
  α-bungarotoxin-sensitive nAChRs with "rapid rise and decay kinetics."
  Exact decay time constants in milliseconds could not be retrieved from
  either paper this session (both hosts blocked automated fetch). Verdict:
  the fast/ionotropic *class* is confirmed in situ; the specific τ_decay is
  not confirmed here.

### 1.2 GABA-A / Rdl (ionotropic)

- **Mechanism and identity — measured.** RDL ("Resistant to Dieldrin") is an
  ionotropic Cys-loop Cl⁻ channel; it can form functional homomers in
  heterologous expression, and is presumed to assemble with less-understood
  partner subunits (e.g. LCCH3, GRD) in at least some native neurons.
  GABA receptors containing Rdl subunits mediate fast inhibitory synaptic
  transmission in cultured Drosophila CNS neurons (title confirmed: J
  Neurosci 2003;23(11):4625, O'Dowd-lab culture preparation; full text was
  not retrievable this session, so the exact decay τ reported there is not
  confirmed here).
- **The one genuinely distinctive, well-established kinetic fact — measured
  qualitatively, not pinned quantitatively for native Drosophila synapses.**
  RDL is well known across the insect-pharmacology literature (ffrench-Constant
  / Sattelle / Hosie tradition) for unusually **slow desensitization**
  compared with vertebrate GABA-A receptors — this is precisely why RDL
  became the standard heterologous target for insecticide (dieldrin,
  fipronil) research. The degree of slow desensitization is itself tunable in
  vivo by alternative splicing and A-to-I RNA editing of the Rdl transcript,
  which is a real, Drosophila-specific extra layer with no vertebrate
  analogue (not independently re-verified numerically this session — treat
  the *direction and existence* of this fact as solid, and any specific τ
  value you find elsewhere as needing its own citation check).
- **Reversal potential — not measured per cell type, and this is a real
  gap, not just an oversight.** Being Cl⁻-mediated, RDL's reversal potential
  equals E_Cl of the specific neuron, and intracellular Cl⁻ regulation
  (cation-chloride cotransporter expression, etc.) has essentially no
  systematic mapping across Drosophila central neurons. This matters because
  it means GABA is not guaranteed to be hyperpolarizing everywhere — the
  model's blanket "GABAergic = negative sign" could be locally wrong in any
  neuron with atypical Cl⁻ homeostasis, and there is no current way to know
  which ones without new measurements.

### 1.3 GABA-B (metabotropic)

- **Identity — measured.** Three subunits, GABA-B-R1, R2, R3 (commonly
  cited to Mezler et al. 2001 for cloning; exact journal not independently
  re-verified this session), presumed R1+R2 heteromer with R3 as an auxiliary/
  modulatory subunit, by analogy with other insect and vertebrate GABA-B
  receptors.
- **Mechanism — partially known.** Gi/o-coupled metabotropic receptor,
  presumed (by vertebrate analogy) to act through GIRK-type K⁺ channels
  and/or presynaptic Ca²⁺-channel inhibition. The actual downstream effector
  channel has not been directly confirmed for any identified Drosophila
  central neuron in the sources found here.
- **Kinetics — measured qualitatively (order-of-magnitude), not as a clean
  τ.** This is the best-supported fast/slow contrast in the whole section.
  Olsen & Wilson 2008 (Nature 452:956, "Lateral presynaptic inhibition
  mediates gain control in an olfactory circuit") and Root et al. 2008
  (Neuron, GABAergic presynaptic inhibition of ORN terminals), both in vivo
  whole-cell patch clamp in the Drosophila antennal lobe, directly show that
  GABA-B-receptor-mediated presynaptic inhibition has a much slower time
  course than the fast ionotropic (RDL) component — Olsen & Wilson describe
  inhibitory epochs spanning "tens to thousands of milliseconds" for the
  combined GABA-A + GABA-B presynaptic inhibition. That is a genuine,
  citable, order-of-magnitude separation between the fast and slow inhibitory
  channels (tens of ms vs. hundreds to thousands of ms) — useful even without
  a single clean biexponential fit.
- **Reversal potential — not measured** for any Drosophila central neuron in
  the sources found here.

### 1.4 GluCl (glutamate-gated chloride channel)

- **Identity, mechanism, and sign — measured, and this is one of the more
  important qualitative facts for the whole model.** GluClα is an ionotropic
  Cl⁻ channel, a member of the same Cys-loop gene family as RDL and nAChR
  (NOT related to vertebrate ionotropic glutamate receptors). Glutamate is
  therefore **inhibitory** across much of the Drosophila CNS — a
  glutamatergic connectome edge is not safely assumed excitatory the way a
  vertebrate-trained intuition would assume.
- **Native, in vivo circuit evidence — measured.** Liu & Wilson 2013 (PNAS
  110:10294, "Glutamate is an inhibitory neurotransmitter in the Drosophila
  olfactory system"), in vivo whole-cell patch clamp in the antennal lobe:
  about one-third of antennal-lobe local interneurons are glutamatergic;
  iontophoresed glutamate hyperpolarizes essentially every major
  antennal-lobe cell type; the effect is blocked both by picrotoxin and by
  GluClα RNAi knockdown, directly confirming the receptor.
- **Reversal potential and rise/decay τ — not confirmed this session.** By
  mechanism (a Cl⁻ channel) the reversal potential should track the same
  E_Cl as RDL in a given neuron, but the paper's own reported numbers could
  not be retrieved here (403 on both direct-publisher attempts). This is a
  concrete, well-defined follow-up: the numbers almost certainly exist in
  Liu & Wilson 2013's main figures and just need direct journal/PDF access.

### 1.5 Histamine receptors: HisCl1 (hclB) and ort (hclA)

- **Identity and mechanism — measured.** Both are Cys-loop histamine-gated
  Cl⁻ channels; together they carry essentially the entire fast output
  synapse of photoreceptors (which are histaminergic) onto lamina monopolar
  cells and other targets. ort/hclA was identified as the Drosophila gene by
  mutant analysis (Gengs et al. 2002, J Biol Chem 277:42113, "The target of
  Drosophila photoreceptor synaptic transmission is a histamine-gated
  chloride channel encoded by ort (hclA)"); HisCl1/a second subunit were
  identified the same year (Gisselmann et al. 2002, J Biol Chem, "Two novel
  Drosophila melanogaster histamine-gated chloride channel subunits expressed
  in the eye").
- **Species caveat — important, and exactly the kind of thing this file
  exists to flag.** The founding electrophysiological description of the
  histamine-gated chloride current (Hardie 1989, Nature 339:704) was recorded
  in blowfly (*Calliphora*) large monopolar cells, not *Drosophila
  melanogaster*. A comparative study across dipterans exists (Skingsley et
  al., J Comp Physiol A, "Properties of histamine-activated chloride channels
  in the large monopolar cells of the dipteran compound eye") reporting
  single-channel sub-conductance states around 25, 40 and 60 pS — but because
  it is explicitly cross-species, it is not safe to assume those exact
  numbers are the Drosophila value without checking.
- **Drosophila-specific functional data exists but its numbers were not
  retrieved here.** Pantazis et al. 2008 (J Neurosci 28:7250, "Distinct Roles
  for Two Histamine Receptors (hclA and hclB) at the Drosophila Photoreceptor
  Synapse") directly recorded in Drosophila and reports the two receptors
  play distinct functional roles at the synapse; the paper's specific
  quantitative content (reversal potential, τ) could not be pulled from the
  publisher site this session (403) and is a clean, specific follow-up target.

### Section 1 summary

| Receptor | Identity/mechanism | Sign | Reversal potential | Rise/decay τ |
|---|---|---|---|---|
| nAChR | measured | measured (+) | not measured (native); ~0 mV expected | partial (fast, ms-scale; exact τ not confirmed) |
| GABA-A / Rdl | measured | measured (−, but see E_Cl caveat) | not measured per cell type | partial (qualitatively slow-desensitizing; no confirmed native τ) |
| GABA-B | measured | measured (−) | not measured | partial (order-of-magnitude only: ~10-100x slower than Rdl) |
| GluCl | measured | measured (−) | not confirmed this session (paper likely has it) | not confirmed this session |
| HisCl1 / ort | measured | measured (−) | not confirmed for *D. melanogaster* specifically | not confirmed for *D. melanogaster* specifically |

---

## 2. Single-neuron physiology by cell type

### 2.1 What has actually been measured

- **Antennal lobe projection neuron, glomerulus DM1 — measured, and the
  strongest single number in this whole file.** Gouwens & Wilson 2009 (J
  Neurosci 29:6239, "Signal Propagation in Drosophila Central Neurons"),
  whole-cell patch clamp, antennae removed: **input resistance = 598.0 ± 69.3
  MΩ (n = 14)**. The same paper fit single-cell compartmental models to 3
  cells and recovered specific membrane resistance (8.3–20.8 kΩ·cm²) and
  specific membrane capacitance (0.8–2.6 μF/cm²) — multiplying these per cell
  gives an implied membrane time constant of roughly **17–31 ms**, which
  brackets the model's current uniform 20 ms assumption. That is a genuine,
  if narrow, validation: for this one identified PN type, 20 ms is not an
  unreasonable number, but it is also only one cell type out of thousands.
- **Kenyon cells (mushroom body) — partially known.** Turner, Bazhenov &
  Laurent 2008 (J Neurophysiol) is the standard reference for Kenyon cell
  intracellular physiology and is widely cited (including in this agent's
  training data) for reporting unusually **high input resistance** relative
  to PNs, consistent with KCs' small size and their role as coincidence
  detectors requiring several simultaneous PN inputs to spike (see also
  Gruntman & Turner 2013, Nat Neurosci 16:1821, on claw-level integration
  requiring multiple simultaneous PN inputs). The exact input resistance and
  capacitance figures are **not independently re-verified this session** —
  flagged rather than stated as a specific number, to avoid seeding false
  precision.
- **Antennal lobe local interneurons (LNs) — partially known, and known to
  be heterogeneous.** Wilson & Laurent 2005 (J Neurosci) and the broader
  Wilson-lab body of work characterize LN physiology alongside PNs; a 2023
  eNeuro paper (PMC9884108, "Nonspiking Interneurons in the Drosophila
  Antennal Lobe Exhibit Spatially Restricted Activity") directly compares
  three genetically defined LN populations by whole-cell patch clamp:
  R32F10-GAL4 (patchy innervation, graded potentials only, no detectable
  voltage-gated Na⁺ current), versus R70A09-GAL4 and NP3056-GAL4
  (pan-glomerular, clear voltage-gated Na⁺ currents, TTX-sensitive action
  potentials). Approximate neuron counts of ~11.5 (R70A09) and ~12.8
  (R32F10) per the source unit (most likely per hemisphere/brain, exact unit
  not confirmed) are reported. This paper does **not** report input
  resistance, capacitance, resting potential, or threshold numbers for any
  of the three lines — it establishes spiking phenotype and morphology only.
- **APL (anterior paired lateral) — measured (qualitative), not
  quantitative.** Amin, Apostolopoulou, Suárez-Grimalt, Vrontou & Lin 2020
  (eLife 9:e56954, "Localized inhibition in the Drosophila mushroom body")
  directly states electrophysiological recording shows APL "elicits
  nonspikes," and that voltage-gated Na⁺ and Ca²⁺ channels are expressed at
  lower levels in APL than in other mushroom body neurons — consistent with,
  but not itself a full quantitative passive-property characterization of,
  graded transmission. No Rin/Cm/Vrest numbers found.
- **Lobula plate tangential cells (HS/VS, motion vision) — measured
  (qualitative class), Drosophila-specific.** Joesch, Schnell, Raghu, Reiff &
  Borst 2008 (Curr Biol) recorded HS cells in Drosophila directly (whole-cell
  patch, adult) and found graded, directionally-selective membrane-potential
  changes plus small, TTX-sensitive "spikelets" superimposed on the graded
  signal — a genuinely intermediate case, not cleanly "spiking" or
  "non-spiking" (see Section 3).
- **Circadian clock neurons — measured, and a useful warning about
  "constants."** Flourakis et al. 2015 (Cell 162:836, "A Conserved Bicycle
  Model for Circadian Clock Control of Membrane Excitability") shows that in
  l-LNv and DN1p clock neurons, a Na⁺-leak conductance (na/NALCN, trafficked
  by NLF-1) is itself under circadian transcriptional control, so resting
  potential and excitability cycle across the day in these specific,
  identified neurons. This is direct evidence that "resting potential" is
  not a fixed per-cell-type constant even in principle for at least one
  well-studied population — a structural fact a static-parameter model
  cannot represent regardless of how good the per-cell-type numbers get.
- **Other circuits with at least some recordings, not deeply searched this
  session:** giant fiber system and DLM flight motor neurons (von Reyn et
  al., Koto et al.), leg motor neurons/VNC (Azevedo, Tuthill lab), R1–R8
  photoreceptors (graded; Juusola-lab-style recordings, mostly not
  Drosophila-specific historically — see Section 3), ellipsoid-body ring
  neurons (mostly calcium imaging, Seelig & Jayaraman).

### 2.2 The headcount: how small is "small"?

This is as important as any individual number. Assembling every distinct,
**named/identified** central neuron type or type-group this pass actually
found any quantitative or semi-quantitative intracellular electrophysiology
for — DM1 (and a handful of other) antennal-lobe PN types, 2–3 genetically
defined AL-LN populations, Kenyon cells (studied more as a class than by its
αβ/α′β′/γ sub-types), APL (one identified neuron per hemisphere), a handful
of HS/VS lobula-plate tangential cell types, 2–3 clock-neuron populations
(l-LNv, DN1p, and to a lesser extent s-LNv/LNd), the giant-fiber/DLM motor
system, and a few leg motor neuron types — comes to **very roughly 20–40
distinct cell types or narrowly defined populations**, generously counted, with
**any** published quantitative membrane-property data at all, and a much
smaller number (arguably fewer than 10) with a *complete* set (Rin, Cm,
Vrest, threshold, and τ_m all reported together for the same cells).

Set that against the connectome: the hemibrain alone catalogs on the order of
**5,000 morphological cell types** across its ~130,000 traced neurons, and
FlyWire's whole-brain, finer-grained typing pushes this higher still. So the
fraction of cell types with *any* patch-clamp characterization is on the
order of **well under 1%** — this is a hard ceiling, not a temporary gap: even
optimistic near-term experimental effort is very unlikely to characterize
more than a few percent of cell types individually in the foreseeable future,
because whole-cell patch clamp on genetically-targeted single Drosophila
central neurons is slow, low-throughput work. **This number — a few dozen
out of several thousand — is the real answer to "how much can per-cell-type
physiology ever be constrained by direct measurement," and it means the
model will need either (a) a principled way to generalize from the ~30
measured types to the rest (by cell size, transcriptomic similarity, or
lineage), or (b) to accept a shared/statistical prior over membrane constants
rather than treating them as a fitting target per cell type.**

(Caveat: this headcount is this agent's own synthesis from the papers
surfaced in one research pass, not a number quoted from any single review —
a dedicated systematic search of Drosophila electrophysiology literature,
which this session's tooling limits prevented from being run as a parallel
sub-agent, could sharpen it, most plausibly upward by some tens of percent,
not by an order of magnitude.)

### 2.3 A caution restated

Even where a cell type *has* been measured, Section 2.1's clock-neuron
example shows the measured value is not always a constant — some identified
neurons' excitability is deliberately time-varying. Any per-cell-type
membrane-constant table this project builds should flag which entries are
known to be state-dependent rather than presenting all of them with equal
confidence as fixed numbers.

---

## 3. Which neurons spike and which are graded

### 3.1 Cases with direct evidence

- **Photoreceptors (R1–R8) — graded, well established.** Long-standing,
  essentially uncontested in the literature (not re-derived from a specific
  new fetch this session, but about as solid a fact as exists in insect
  neurophysiology).
- **Lamina monopolar cells — graded for L1–L3 specifically, per the
  literature's usual framing (matching how this task itself describes them);
  L4 and L5 were not confirmed one way or the other in this pass** and
  should be treated as an open item rather than assumed graded by
  association.
- **APL — graded/non-spiking, measured directly.** Amin et al. 2020 (eLife
  56954) explicitly: "Kenyon cells receive feedback inhibition from a
  non-spiking interneuron called the anterior paired lateral (APL) neuron,"
  with electrophysiology showing "nonspikes" and reduced voltage-gated
  Na⁺/Ca²⁺ channel expression relative to spiking MB neurons. This appears to
  be the settled, current view (superseding any earlier ambiguity); no
  conflicting recent report was found.
- **Antennal-lobe local interneurons — a genuine mixed population, not a
  single answer, and this is directly measured, not inferred.** The 2023
  eNeuro study (PMC9884108) used electrophysiology (presence/absence of
  action potentials and voltage-gated Na⁺ current, TTX sensitivity) plus
  morphology to show that different genetically-defined LN populations
  within the same antennal lobe are on opposite sides of the spiking/graded
  divide: R32F10-GAL4 LNs are non-spiking with patchy, spatially-restricted
  glomerular innervation and odor tuning; R70A09-GAL4 and NP3056-GAL4 LNs are
  spiking with pan-glomerular innervation and broader tuning. No overall
  brain-wide or even antennal-lobe-wide *fraction* (e.g. "X% of LNs are
  non-spiking") was reported by this paper or found elsewhere this session —
  only that both categories coexist and are each substantial (order of ~10
  neurons per genotype per the counts given).
- **Lobula plate tangential cells (HS/VS) — a genuine intermediate case,
  measured directly, and worth flagging as neither of the model's two
  categories.** Joesch et al. 2008 recorded graded, directionally-tuned
  membrane potential changes with small TTX-sensitive "spikelets" riding on
  top, in adult Drosophila. This is neither "spikes and nothing else" nor
  "purely graded" — a binary spiking/non-spiking model has no natural slot
  for it.

### 3.2 Is there a systematic, brain-wide survey?

**No.** Nothing found in this pass amounts to a systematic, comprehensive
classification of spiking vs. non-spiking status across Drosophila central
neuron types. What exists is a set of independent, circuit-by-circuit
findings (listed above), each using its own criteria (presence of
voltage-gated Na⁺ current, TTX sensitivity, or observed all-or-none spikes
under current injection) in its own small population of genetically-targeted
cells. There is no brain-wide electrophysiological census, and — as
important — no validated *indirect* (e.g. purely morphological or
transcriptomic) classifier that has been checked against ground truth broadly
enough to trust brain-wide.

The most relevant place such a decision would have had to be made explicitly
is a whole-brain connectome-based spiking model: Shiu et al. (bioRxiv 2023 /
Nature 2024, leaky-integrate-and-fire model of the entire adult central brain
connectome, >125,000 neurons). This session could confirm the model's broad
strokes (LIF with α-synapse dynamics; neurons classified only as excitatory
cholinergic vs. inhibitory GABAergic/glutamatergic, with dopaminergic/
octopaminergic/serotonergic neurons folded into "excitatory"; zero
basal-rate assumption; gap junctions excluded) but **could not confirm from
accessible text whether known non-spiking types (photoreceptors, lamina
neurons, APL, non-spiking LNs) were specially excluded, flagged, or simply
modeled as spiking units like everything else** — the PDF's methods section
did not extract cleanly in this session. This is worth checking directly
against the paper's methods/supplement, because if the field's most
comprehensive current whole-brain spiking model does *not* special-case these
neurons, that is itself a strong data point about how unresolved this
question is considered to be.

### 3.3 What fraction of the fly brain is non-spiking?

**No quantitative estimate exists.** No paper found in this session gives a
number, even a rough one, for what fraction of the ~166,700 Drosophila brain
neurons (or of its ~5,000 cell types) are non-spiking. The honest state of
knowledge is: a specific, growing list of individual cases (photoreceptors,
L1–L3, APL, a subset of AL LNs, and the intermediate HS/VS case), each nailed
down in its own circuit, and no brain-wide accounting at all. Given that
non-spiking transmission is disproportionately a property of *local*
interneurons (short-range, compact arbors where passive spread is
sufficient) — a pattern that shows up in every case above except the LPTCs —
a plausible but **unverified** structural prior is that non-spiking status
correlates with "local interneuron without a long projecting axon," echoing
the older, morphology-based heuristic from classical (non-Drosophila) insect
neurobiology (Burrows' work on nonspiking interneurons in orthopterans). This
project should treat that correlation as a hypothesis to test against
whatever ground truth exists, not as a validated rule — it has not, to this
session's knowledge, been checked systematically against Drosophila
electrophysiology.

---

## 4. Fly Cell Atlas and single-cell transcriptomics

### 4.1 What actually exists

- **Fly Cell Atlas** (Li et al. 2022, Science 375:eabk2432): whole-animal,
  not brain-specific — 580,000 nuclei from 15 individually dissected sexed
  tissues plus whole head and whole body, snRNA-seq (10x Chromium +
  Smart-seq2), >250 annotated cell types, annotated across >100 experts from
  ~40 labs in >20 online "jamborees." Data via SCope/ASAP.
- **Precursor/companion brain atlases:** Davie et al. 2018 (Cell,
  "A Single-Cell Transcriptome Atlas of the Aging Drosophila Brain") and, in
  more receptor-relevant detail, **Croset, Treiber & Waddell 2018** (eLife
  7:e34550): 10,286 midbrain cells, 28–30 clusters, with detailed
  neurotransmitter-receptor-subunit expression reported per cluster (see
  Section 1.1 for the nAChR detail) and clusters matched to several
  *specific, named* cell types — Kenyon cells (with αβ/γ/α′β′ sub-structure),
  olfactory projection neurons (4 sub-clusters), ellipsoid-body ring
  neurons, the four monoaminergic classes, glia/astrocytes, and
  insulin-producing cells. One large cluster (reported as ~7,000 of the
  10,286 cells) could not be given a definitive identity — a concrete
  illustration of how much of even a "successful" central-brain mapping
  effort remains unresolved.
- **Optic lobe transcriptomics** (Kurmangaliyev, Yoo, LoCascio & Zipursky,
  and related Desplan-lab work: Konstantinides et al. 2018, 2022, Cell): this
  session's searches surfaced this group's work mainly through its
  circuit-*assembly*/cell-adhesion-molecule angle (matching pre- and
  postsynaptic partners during development) rather than a directly confirmed
  receptor-expression-per-connectome-type resource. Background knowledge
  (not independently re-verified this session) is that this line of work did
  successfully match transcriptomic clusters to known, named optic-lobe cell
  types — the optic lobe is the best case for this kind of matching because
  its ~200 columnar types are highly stereotyped, repeated, and already have
  strong genetic markers from decades of anatomical work (Fischbach &
  Dittrich). Whether *receptor* genes specifically (as opposed to
  transcription factors and cell-adhesion molecules, which is what these
  papers are centrally about) were systematically reported per matched type
  was not confirmed here.

### 4.2 Is there a connectome-integrated receptor map? — Partial, and the gap is specific

The **chemoconnectome (CCT)** project (Deng, Li, Liu, Cao, Li, Qian, Xu, Mao,
Zhou, Zhang, Huang & Rao 2019, Neuron, "Chemoconnectomics: Mapping Chemical
Transmission in Drosophila," with a 2024 eLife follow-up on conditional
tools, "cCCTomics") is the closest thing found to what the task is asking
about, and it is worth being precise about what it is and is not:

- It **does** cover fast ionotropic receptor genes, not just neuropeptides
  and GPCRs — confirmed from the 2024 follow-up: the CCT gene set (209 genes
  total) explicitly includes nAChRα1, nAChRα2, nAChRβ2, GABA-B-R2, and
  references to Rdl, alongside its more emphasized neuropeptide/biogenic-amine
  GPCR content.
- It **is** a systematic, genome-scale genetic toolkit: knockout lines for
  every CCT gene, plus GAL4/knock-in driver lines for expression mapping and
  intersectional manipulation, validated behaviorally (e.g. a pilot screen
  implicating 41 genes in sleep).
- It **does not** integrate with the EM connectome. No mention of mapping CCT
  gene expression onto hemibrain or FlyWire cell-type identifiers was found
  in either the original 2019 paper's summary or the 2024 follow-up's full
  text. It answers "which genes, and roughly which broad neuron populations
  by driver-line expression pattern" — not "which receptor sits on
  postsynaptic cell type X in the wiring diagram."

So: the raw genetic material to eventually build a Drosophila receptor
connectome exists and is more complete than this agent expected going in
(fast ionotropic receptors included, not just neuropeptide GPCRs) — but the
actual mapping onto connectome cell types, the step that would make it usable
for this project, **has not been done and published**, as of the sources
found here.

### 4.3 The C. elegans comparison, and why it does not transfer directly

**Ripoll-Sánchez et al. 2023** (Neuron 111:3765, "The neuropeptidergic
connectome of C. elegans") is the precedent the task points at, and it is a
good one to understand precisely because the reason it worked does not carry
over cleanly to Drosophila. It combined the CeNGEN single-neuron RNA-seq
atlas (built on the fact that every one of *C. elegans*'s 302 neurons is
individually and reproducibly identifiable, by name, in every animal) with
the known wiring diagram to computationally infer neuropeptide-GPCR
connectivity, producing three range-scaled models (long/mid/short-range) and
finding a dense, decentralized network with some little-studied "hub"
neurons for peptidergic signaling.

The load-bearing fact is: **CeNGEN gives literal single-neuron
transcriptomes, one profile per uniquely-named cell, directly attachable to
the wiring diagram's own nodes.** Fly Cell Atlas, Davie et al., and Croset et
al. give **clusters** — statistical groupings pooled across many
dissociated brains, each cluster typically representing many individual
neurons of a "type," not one identified cell — and connectome cell types
(hemibrain/FlyWire identifiers) do not automatically line up with
transcriptomic cluster boundaries. Matching the two requires an extra,
non-trivial validation step per cell type: marker-gene confirmation via in
situ hybridization or split-GAL4 lines, spatial transcriptomics, or
morphology-informed computational matching. This has been done well only
where the biology was already unusually favorable — Kenyon cells, clock
neurons, some monoaminergic populations, and optic-lobe columnar types with
decades of prior genetic markers — not brain-wide, and not as a general
method.

### 4.4 Verdict

Receptor identity per connectome cell type is **not** something that can be
read straight out of current Drosophila transcriptomic data the way it can
for *C. elegans*. It is **partially usable today** for a limited, specific
set of well-marked cell types (Kenyon cells, clock neurons, some AL PNs, and
optic-lobe columnar types), where cross-referencing Croset et al. /
Kurmangaliyev-et-al.-style clusters against known markers is tractable. For
the large majority of the brain's ~5,000 connectome cell types, this mapping
**does not yet exist as a published, validated resource**. Building it
brain-wide — combining Fly Cell Atlas/Croset-style receptor-expression data
with FlyWire cell-type identifiers via marker validation — is a well-defined,
Drosophila-appropriate analogue of what Ripoll-Sánchez et al. did for C.
elegans, and appears to be a genuinely open project rather than one this
agent found already completed somewhere it missed.

---

## 5. Short-term plasticity at central synapses (NMJ excluded)

The neuromuscular junction is deliberately out of scope here (it is well
characterized for facilitation/depression/augmentation, but it is a
peripheral motor synapse, not a central circuit one).

### 5.1 What exists

- **ORN→PN synapse, antennal lobe — depression demonstrated to exist,
  magnitude/τ not confirmed.** Kazama & Wilson 2008 (Neuron 58:401,
  "Homeostatic matching and nonlinear amplification at identified central
  synapses"), in vivo whole-cell patch clamp: this synapse has many release
  sites and high release probability (explaining amplification of weak ORN
  responses in PNs), unitary EPSC amplitude is matched to a PN's dendritic
  arbor size, and — the directly relevant sentence — **"strong stimuli
  produce short-term depression at this synapse."** This confirms STD exists
  at a specific, named central synapse from a direct in vivo recording. The
  paper almost certainly reports a magnitude and/or recovery time constant in
  its figures; this session could not retrieve them (403 on both the
  publisher and PMC mirror attempted).
- **GABA-B presynaptic inhibition of ORN terminals — a related but distinct
  phenomenon, not classical STP.** Root et al. 2008 / Olsen & Wilson 2008
  describe activity-dependent presynaptic inhibition building up over
  ongoing firing (Section 1.3) — this is a genuine use-dependent reduction
  in transmission, but it is a heterosynaptic, circuit-level (GABAergic LN
  feedback) effect, not the same phenomenon as vesicle-depletion/residual-
  calcium short-term depression intrinsic to one synapse's own recent
  activity. Worth keeping conceptually separate when parameterizing a model.
- **Kenyon cell → mushroom body output neuron (MBON) synapse — a specific
  paired-pulse protocol was found in this session's search, but the exact
  citation could not be fully confirmed.** A snippet describing whole-cell
  voltage-clamp recording of optogenetically-evoked EPSCs at the
  γKC-to-MBON-γ1pedc synapse, with a paired-pulse protocol (1 ms pulse width,
  400 ms inter-stimulus interval) used to probe short-term plasticity while
  manipulating divalent cation concentration or partially blocking
  postsynaptic ionotropic receptors, surfaced in a general search on
  Drosophila paired-pulse ratio. This is very likely from the
  Turner-lab/Aso-Rubin-lab/Waddell-lab body of work on KC-MBON physiology
  (candidates include Hige & Turner 2013 J Neurophysiol and/or later
  MBON-γ1pedc-specific plasticity papers), but this session could not pin
  down the exact author/year with confidence — **flagged for direct
  follow-up rather than guessed at.**
- **PN→Kenyon cell dendritic claw synapse — searched specifically, not
  found.** Gruntman & Turner 2013 (Nat Neurosci 16:1821) is the standard
  reference for claw-level integration of PN input, but this session found
  no evidence it reports facilitation/depression numbers — its focus is
  cross-claw response heterogeneity (each claw wired to one PN type), not
  short-term dynamics of a single claw's synapse under repeated
  stimulation.
- **Visual system (Mi1, Tm3, T4/T5, etc.) — not found, and the field's own
  best model implicitly says why.** Lappalainen et al. 2024 (Nature,
  "Connectome-constrained networks predict neural activity across the fly
  visual system," the `flyvis` model) uses real connectome-derived
  connectivity for 64 optic-lobe cell types but treats single-neuron and
  single-synapse **dynamical parameters as unknown**, fitting them by deep
  learning against ~26 studies' worth of functional data rather than
  plugging in measured values — including, presumably, any short-term
  plasticity. That the most sophisticated current connectome-constrained
  functional model of this system still has to *fit* rather than *measure*
  its synaptic dynamics is itself informative: it suggests the field does
  not currently regard direct STP measurements as available and reusable
  even for this unusually well-studied part of the brain.
- **Central complex / descending neurons — not searched successfully this
  session;** no paired-pulse or train-stimulation data was found, and the
  giant-fiber pathway's key outputs are partly electrical/mixed synapses,
  where the concept of chemical STP may not even apply in the usual sense.

### 5.2 Verdict

Central (non-NMJ) short-term plasticity in Drosophila is **demonstrated to
exist qualitatively** at at least one named synapse (ORN→PN depression,
directly stated in Kazama & Wilson 2008) and probably at KC→MBON synapses
(paired-pulse protocol found but not fully attributed), but **reusable
quantitative parameters — τ_facilitation, τ_depression, fractional
depletion per spike, recovery time constant — were not retrievable from any
source in this session for any central Drosophila synapse.** This is the
most clear-cut "does not exist in the accessible literature" verdict in this
document. Given that even a state-of-the-art connectome-constrained model of
the best-studied circuit in the brain (the visual system, via Lappalainen et
al. 2024) fits rather than measures these dynamics, the pragmatic
recommendation is the same one that paper effectively adopted: treat STP
time constants as free parameters to be fit (possibly shared across broad
synapse classes, e.g. "fast cholinergic," "GABAergic," etc.) rather than
values to look up, unless and until direct measurements surface.

---

## Overall summary

| # | Parameter group | Status |
|---|---|---|
| 1 | Receptor identity, mechanism class, sign (all 5 systems) | **Measured** |
| 1 | Receptor reversal potentials (native, per cell type) | **Not measured** (mechanistic inference only) |
| 1 | Receptor rise/decay time constants (native central synapses) | **Partial** — qualitative fast/slow class known; exact native τ mostly not confirmed |
| 1 | nAChR/Rdl subunit stoichiometry per identified neuron | **Not measured** for almost all cell types |
| 2 | Passive/active membrane properties, per identified cell type | **Partial**, and structurally bounded: on the order of a few dozen cell types out of several thousand will likely ever be directly measured |
| 2 | DM1 projection neuron input resistance | **Measured**: 598 ± 69 MΩ (Gouwens & Wilson 2009) |
| 3 | Spiking vs. graded status, specific well-studied cases | **Measured** (photoreceptors, L1–L3, APL, some AL-LN genotypes, HS/VS intermediate case) |
| 3 | Spiking vs. graded status, brain-wide | **Not measured** — no systematic survey exists |
| 3 | Fraction of brain that is non-spiking | **Does not exist** as a number anywhere found |
| 4 | Receptor gene expression per transcriptomic cluster (some cell types) | **Partial** (Croset et al. 2018 and similar; strongest for nAChR subunits) |
| 4 | Receptor identity mapped onto connectome (hemibrain/FlyWire) cell-type IDs | **Does not exist** as a published resource, brain-wide |
| 4 | Genetic toolkit covering receptor/transmitter genes (chemoconnectome) | **Measured/exists**, but genetic, not structural — not connectome-mapped |
| 5 | Existence of short-term depression at a named central synapse | **Measured** (ORN→PN, Kazama & Wilson 2008) |
| 5 | Short-term plasticity time constants/magnitudes, central synapses | **Does not exist** in retrievable form — treat as a fitted, not measured, parameter |

## What this means for the fitting problem

The genuinely free-lunch items are in Section 1: swapping the uniform ± sign
for five receptor-specific sign-and-speed classes (fast cholinergic
excitation, fast Rdl inhibition, slow GABA-B inhibition, fast GluCl
inhibition, fast histaminergic inhibition) costs no new fitting, only
implementation, and is justified by measurement rather than assumption. The
Section 3 spiking/graded findings are similarly free: a short, explicit list
of confirmed-graded cell types (photoreceptors, L1–L3, APL, specific AL-LN
driver lines) can be hard-coded rather than fit, even though the brain-wide
picture is unknown. Everything else — per-cell-type membrane constants
beyond the ~30-or-so measured types, all receptor reversal potentials and
exact time constants, any connectome-wide receptor map, and every short-term
plasticity parameter — remains either partially constrained at best or a
genuinely open dimension the optimizer must carry, and this file's main
contribution is drawing that line as precisely as the current literature
allows.
