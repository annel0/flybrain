# Antennal lobe and early olfaction targets

Scope: olfactory receptor neurons (ORN/OSN), antennal-lobe projection neurons
(PN), and antennal-lobe local interneurons (LN) — the first two synapses of
the fly olfactory system, and the stage where our model currently drives its
input. See `../theory-review.md` (§1 "The antennal lobe interneurons should
not be spiking at all", §2 "Gap junctions are missing") and
`../lab-notebook.md` (2026-09-13, "One correction to the framing") for why
this domain is a priority: our LNs fire at 350 Hz against a biological
population that is partly non-spiking by construction, gap junctions are
absent from the model, and the "20-30 Hz" oscillation figure the notebook
uses needs a species qualifier — see T-AL-19/T-AL-20 below, which is a
direct correction to that note.

**Headline conflict, stated up front:** the two quantitative relationships
that matter most for this domain — the ORN→PN divisive-normalization fit
(T-AL-9) and the local-interneuron spiking/non-spiking split (T-AL-16 to
T-AL-18) — come from different eras of the same research programme and were
never reconciled with each other. The 2010 normalization model was fit
assuming all antennal-lobe neurons downstream of ORNs are point-process
spiking units; the 2022/2023 discovery that a subset of LNs is non-spiking
came after, and nobody has re-fit the normalization model accounting for a
graded-potential LN population. Both are correct as measured; neither
constrains the other.

## Priority order

Perturbations first, per `README.md`. Sections below: (1) perturbations —
gap-junction disruption and oscillation-desynchronising manipulations; (2)
divisive normalization — a fitted relationship, not a single number,
called out by name in our brief as a strong target; (3) ORN and PN firing
rates; (4) local interneurons — count, spiking fraction, firing rates; (5)
odour-evoked oscillations; (6) temporal dynamics of PN responses.

---

## 1. Perturbations

### T-AL-1  Inx7 knockdown abolishes PN-PN calcium synchrony in culture

- **Quantity** — cross-correlation of spontaneous calcium transients between
  pairs of physically-connected, cultured antennal-lobe projection neurons
  (PNs), with vs. without RNAi knockdown of innexin 7 (`inx7`)
- **Value** — control (GH146-Gal4 > GFP, physically-connected PN pairs):
  cross-correlation function (CCF) peak ≈ 1.0 at zero lag, N = 28 pairs.
  RNAi-`inx7` pairs: significantly reduced correlated activity, N = 15 pairs,
  p < 0.01 (Kruskal-Wallis ANOVA). Spontaneous transient frequency and
  amplitude in RNAi-`inx7` PNs were *not* different from control when cells
  were recorded singly — the knockdown removes synchrony between cells, not
  activity in each cell
- **Type** — perturbation
- **Method** — primary culture of dissociated antennal-lobe PNs (GH146-Gal4,
  UAS-GFP, labels ~2/3 of AL PNs), loaded with Fura-2 AM ratiometric calcium
  dye; 340/380 ratio sampled every 4 s; cross-correlation computed over
  ≥10 min per pair (Clampfit9). TTX (1 µM) + curare (20 µM) + picrotoxin
  (10 µM) present throughout to block fast chemical synaptic transmission,
  isolating electrical/gap-junction coupling; Co²⁺ (2 mM) and Plectreurys
  toxin (PLTX-II, 50 nM) used in some experiments to block Ca²⁺ channels
- **Observation model** — this is a dissociated-culture assay, not an intact
  circuit measurement. A model comparison would need to reproduce the
  *reduction in pairwise correlation* under gap-junction knockdown, not an
  absolute rate. Calcium-transient definition used by the authors: rise
  >60 nM (>5x baseline noise), peaking within 20 s
- **Conditions** — dissociated primary culture from pupal/adult AL tissue;
  RNAi_`inx7` line VDRC #22949, verified 85 ± 7% mRNA knockdown (N = 3),
  driven by GH146-Gal4; a weaker RNAi line (VDRC #22948, 50 ± 7% knockdown)
  was not used for the main experiments
- **Source** — Fuenzalida-Uribe, Hidalgo, Silva, Gandhi, Vo, Zamani, Holmes,
  Sayin, Grunwald Kadow, Hadjieconomou, O'Dowd, Campusano (2025) "The innexin
  7 gap junction protein contributes to synchronized activity in the
  Drosophila antennal lobe and regulates olfactory function." *Front Neural
  Circuits* 19:1563401. https://pmc.ncbi.nlm.nih.gov/articles/PMC12062127/
  (task-supplied link; PMID 40352759)
- **Confidence** — high for the reported statistics; medium for generalising
  to the intact circuit, since this is a dissociated-culture assay
  engineered specifically to isolate electrical coupling from chemical
  synaptic transmission

### T-AL-2  Inx7 knockdown paradoxically *increases* in vivo odour-evoked calcium response

- **Quantity** — GCaMP3 calcium response in AL PNs (GH146-Gal4) to vinegar,
  with vs. without in vivo RNAi knockdown of `inx7`
- **Value** — RNAi-`inx7` flies showed an *augmented* (not reduced) calcium
  response to both 1% and 20% vinegar dilutions relative to GH146-Gal4 >
  GCaMP3 controls (p < 0.01 and p < 0.001 respectively, two-way ANOVA with
  Sidak's multiple-comparisons test). N = 38-74 events per genotype, from
  ≥5 flies per condition
- **Type** — perturbation
- **Method** — in vivo GCaMP3 calcium imaging of AL PNs during vinegar
  odour presentation
- **Observation model** — direction matters here more than magnitude: a
  model of gap-junction removal that predicts *reduced* PN odour response
  (the naive expectation from "coupling helps signal") would be wrong in
  sign. The authors' interpretation is that Inx7-mediated coupling normally
  *dampens* PN responses (consistent with a role in gain control /
  cross-glomerular normalization, not just synchrony)
- **Conditions** — intact adult flies, in vivo, odour = vinegar (1% and 20%
  dilutions)
- **Source** — same as T-AL-1
- **Confidence** — high for the direction and significance; the mechanistic
  interpretation (coupling as a dampener) is the authors' inference, not a
  separately measured quantity

### T-AL-3  Inx7 knockdown halves behavioural preference for vinegar

- **Quantity** — T-maze olfactory preference (response index, RI) for 20%
  vinegar, with vs. without in vivo RNAi knockdown of `inx7`
- **Value** — RNAi-`inx7` flies: RI reduced by 50% relative to control flies
  (p < 0.05, one-way ANOVA). N = 30-50 flies per group
- **Type** — perturbation
- **Method** — two-choice T-maze assay, appetitive response to vinegar odour
- **Observation model** — a behavioural readout, two steps removed from
  spiking activity; useful as a sanity-check target (does silencing this
  gap junction move behaviour in the right direction) rather than a direct
  circuit-activity constraint
- **Conditions** — intact adult flies; genotype controls included
  RNAi_`inx7`/+ and GH146/+ parental lines alone
- **Source** — same as T-AL-1
- **Confidence** — high (clear significance, standard assay), but behaviour
  is a weak constraint on circuit dynamics by itself

### T-AL-4  Inx7 knockdown abolishes trial-by-trial behavioural escalation

- **Quantity** — locomotor speed response to repeated vinegar exposure on a
  spherical treadmill, trial 1 vs. trial 10, with vs. without `inx7`
  knockdown
- **Value** — trial 1: no difference between control and RNAi-`inx7` flies
  (both show an increased-speed response to vinegar). Trial 10: control
  flies show escalating speed across trials; RNAi-`inx7` flies show no
  increase in motivation/speed across repeated trials (p < 0.01,
  Mann-Whitney U-test)
- **Type** — perturbation
- **Method** — spherical treadmill, repeated vinegar presentation across 10
  trials, locomotor speed as readout
- **Observation model** — this is specifically a target for *trial history /
  sensitisation* dynamics, not steady-state odour response — the naive
  response (trial 1) is untouched by the perturbation, only the
  across-trial change is
- **Conditions** — intact adult flies, repeated-trial paradigm
- **Source** — same as T-AL-1
- **Confidence** — medium-high; single study, but internally consistent
  (trial-1 null result argues against a general motor or sensory deficit)

### T-AL-5  GABA-mediated inhibition is necessary for PN/LN oscillatory synchrony but not for each neuron's own temporal firing pattern (locust)

- **Quantity** — effect of blocking ionotropic GABA receptors in the
  antennal lobe on (a) oscillatory synchronization across the PN/LN
  ensemble and (b) each neuron's own stimulus-locked temporal firing
  pattern
- **Value** — local application of a GABA_A antagonist to the antennal-lobe
  neuropil abolished oscillatory synchronization of the odour-coding neural
  ensemble, but did **not** affect each neuron's own temporal response
  pattern to odours — even when that pattern contained periods of
  inhibition. No spike counts or Hz values given in the abstract; effect
  reported as qualitative abolition of synchrony
- **Type** — perturbation
- **Method** — local pharmacological antagonism of ionotropic GABA
  receptors at the first olfactory relay (antennal lobe), paired
  intracellular recordings from PNs/LNs, odour puffs
- **Observation model** — this is the clean dissociation a model should be
  able to reproduce: silencing fast GABAergic LN→PN inhibition should
  desynchronize the population-oscillation phase relationship while leaving
  each unit's own odour-triggered rate/timing pattern intact. A model that
  can only do one or the other (e.g., inhibition strength coupled to both
  synchrony and tuning) does not match this dissociation
- **Conditions** — locust, *Schistocerca americana* (species per the
  Laurent lab's standard preparation for this series; not independently
  re-confirmed for this specific paper in this pass), in vivo, intact
  antennal lobe
- **Source** — MacLeod K, Laurent G (1996) "Distinct mechanisms for
  synchronization and temporal patterning of odor-encoding neural
  assemblies." *Science* 274(5289):976-979.
  https://pubmed.ncbi.nlm.nih.gov/8875938/
- **Confidence** — high for the qualitative dissociation (clean, oft-cited
  result); low for any quantitative extrapolation since we could not access
  full-text numbers, only the abstract

### T-AL-6  Desynchronizing odour-coding assemblies impairs fine but not coarse odour discrimination (honeybee)

- **Quantity** — behavioural odour-discrimination accuracy after
  picrotoxin-induced desynchronization of PN oscillatory assemblies, for
  molecularly similar vs. dissimilar odorant pairs
- **Value** — picrotoxin (GABA_A antagonist) desynchronizes PN assemblies
  (confirmed electrophysiologically) and **impairs discrimination of
  molecularly similar odorants but not of dissimilar odorants**, in a
  behavioural learning paradigm. No percentages given in the abstract
- **Type** — perturbation
- **Method** — electrophysiological confirmation of PN assembly
  desynchronization + a classical behavioural conditioning
  (discrimination-learning) paradigm, before/after picrotoxin
- **Observation model** — a strong target for what oscillatory
  synchronization is *for*, functionally: it should matter for
  fine-grained pattern separation, not gross detection. Relevant to
  whatever role we assign synchrony/oscillation in the model — the
  prediction is behaviourally testable at the "similar vs. dissimilar odour
  pair" resolution, not just at the level of raw response magnitude
- **Conditions** — honeybee (*Apis mellifera*), **not locust and not
  Drosophila** — flagged explicitly because this is the paper's species and
  it is easy to misattribute to locust given the same lab and the same
  mechanism (GABA_A-dependent oscillatory synchrony) being demonstrated
  first in locust
- **Source** — Stopfer M, Bhagavan S, Smith BH, Laurent G (1997) "Impaired
  odour discrimination on desynchronization of odour-encoding neural
  assemblies." *Nature* 390(6655):70-74.
  https://pubmed.ncbi.nlm.nih.gov/9363891/
- **Confidence** — high for the qualitative finding (widely cited); we could
  not access full-text quantitative discrimination scores in this pass

### T-AL-7  Silencing one specific LN population (not the other) abolishes odour-evoked LFP oscillation (Drosophila)

- **Quantity** — odour-evoked mushroom-body LFP oscillatory power, with
  each of two morphologically distinct GABAergic local-neuron populations
  (LN1: restricted/patchy innervation; LN2: widely-branching innervation)
  conditionally and reversibly silenced
- **Value** — silencing LN2 (widely-branching population) via temperature-
  shift activation of temperature-sensitive `shibire` (dynamin, blocks
  synaptic vesicle recycling) produced a significantly greater drop in
  odour-evoked LFP oscillatory power than silencing LN1 (restricted
  population) or controls. Quantified as mean odor-evoked LFP spectral
  power (max between 5-45 Hz) across 20 repeated odour presentations,
  averaged over 15-24 animals per genotype; only LN2 silencing abolishes
  oscillation. LN1 silencing alone did not significantly reduce oscillatory
  power
- **Type** — perturbation
- **Method** — GAL4-driven expression of temperature-sensitive `shibire`
  in genetically distinguished LN populations (LN1 vs. LN2 GAL4 lines),
  paired with LFP recording from the mushroom-body calyx and intracellular
  recording from antennal-lobe neurons; oscillation power compared at
  permissive (23°C) vs. restrictive (29°C) temperature
- **Observation model** — a clean genetic dissociation: our model, if it
  ever represents LN population substructure, should be checkable against
  "removing the widely-branching class abolishes the oscillation; removing
  the patchy class does not." This argues the oscillation-generating
  circuit motif is specifically wide lateral inhibition, not
  glomerulus-restricted inhibition
- **Conditions** — Drosophila, in vivo, intact brain, adult; natural food
  odours (banana, yeast headspace) and pure chemicals (cyclohexanone, ethyl
  acetate, hexanol) at a range of concentrations, including low
  concentrations of pure chemicals
- **Source** — Tanaka NK, Ito K, Stopfer M (2009) "Odor-evoked neural
  oscillations in Drosophila are mediated by widely branching interneurons."
  *J Neurosci* 29(26):8595-8603.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2753235/ (task-supplied topic;
  PMID 19571150)
- **Confidence** — high; directly verified from primary full text

### T-AL-8  Picrotoxin reversibly abolishes the odour-evoked LFP oscillation (Drosophila)

- **Quantity** — odour-evoked mushroom-body LFP oscillation, before/during/
  after bath application of the GABA_A blocker picrotoxin
- **Value** — oscillation reversibly abolished during picrotoxin
  application; oscillations sometimes transiently *increased* just after
  drug onset before disappearing (qualitative report; no dose-response
  numbers extracted)
- **Type** — perturbation
- **Method** — LFP recording from mushroom-body calyx, bath application of
  picrotoxin (GABA_A antagonist), before/during/after design
- **Observation model** — same oscillation-generation circuit as T-AL-7,
  confirmed pharmacologically rather than genetically: fast GABA_A
  transmission is necessary for the oscillation to exist at all, not just
  for its amplitude
- **Conditions** — Drosophila, in vivo, intact brain, adult
- **Source** — same as T-AL-7
- **Confidence** — high for the qualitative abolition; we did not extract a
  quantitative dose-response curve

### T-AL-9  Direct current injection shows PN spike-frequency non-adaptation is intrinsic (a negative-result perturbation, useful for localising where adaptation *does* come from)

- **Quantity** — PN firing-rate stability during 500 ms of constant somatic
  current injection (bypassing the ORN-PN synapse entirely), at firing
  rates >100 spikes/s
- **Value** — final firing rate was 104.2% of the initial rate over the
  500 ms current step (N = 8 cells) — i.e., essentially **no** intrinsic
  spike-frequency adaptation in the PN membrane itself at these rates
- **Type** — perturbation (direct current injection, bypassing the synapse,
  used as a causal control)
- **Method** — in vivo whole-cell current-clamp recording from PNs,
  square-pulse somatic current injection sufficient to drive >100 spikes/s
- **Observation model** — this is the key mechanistic result for anyone
  building PN adaptation into a model: **do not implement PN response
  transience/adaptation as an intrinsic PN membrane property** (e.g., an
  adaptation conductance). The data say the fast transience seen in odour
  responses (T-AL-25, T-AL-9-normalization-transience) must come from
  somewhere presynaptic — see T-AL-15 (short-term synaptic depression at
  the ORN-PN synapse) and T-AL-27 (slow presynaptic vesicle-release
  depression) for where it actually comes from
- **Conditions** — Drosophila, in vivo, adult, whole-cell patch clamp
- **Source** — Kazama H, Wilson RI (2008) "Homeostatic matching and
  nonlinear amplification at identified central synapses." *Neuron*
  58(3):401-413. https://pmc.ncbi.nlm.nih.gov/articles/PMC2429849/
  (PMID 18466750)
- **Confidence** — high; directly extracted from primary full text, N
  explicitly stated

---

## 2. Divisive normalization — the ORN→PN transformation

This is the strong target named in our brief: a fitted relationship, not a
single number. Directly verified against the primary full text (not just an
abstract or a secondary summary).

### T-AL-10  ORN→PN input-output function: saturating (Naka-Rushton-type) nonlinearity, per glomerulus

- **Quantity** — steady-state relationship between the odour-evoked firing
  rate of a single ORN type and the firing rate of its cognate second-order
  PN, for a "private" odour that activates only one ORN type
- **Value** — fits the hyperbolic-ratio (Naka-Rushton) form:

  ```
  PN = Rmax · ( ORN^1.5 / (ORN^1.5 + σ^1.5) )        (Eq. 1)
  ```

  with **Rmax = 170, 167, 163, 144** and **σ = 16.3, 11.8, 12.4, 44.8**
  (both in spikes/s, from 500-ms-averaged firing rates) for glomeruli
  **DM4, DL5, VM7, DM1** respectively (fixed order as reported). Exponent
  fixed at **1.5** for all glomeruli and all three equations in this paper
  (empirically the best fit; not derived from a mechanistic model). Rmax
  and σ are described as "essentially the same for all glomeruli" except
  that DM1's σ is elevated when GABA-receptor antagonists are *not*
  present (i.e., DM1 receives more tonic inhibition than the other three
  by default; adding GABA antagonists brings its curve in line with the
  others)
- **Type** — steady-state (explicitly: the authors state "we have not
  modeled the dynamics of neural activity... our model is not able to
  consider finer timescales" — this is a 500-ms-window steady-state fit,
  see T-AL-12 for the separate dynamical finding)
- **Method** — in vivo extracellular recording from single ORNs and
  whole-cell patch clamp from synaptically-connected PNs in the same
  glomerulus; "private" odours chosen to selectively activate one ORN type;
  responses quantified as mean firing rate over the 500 ms odour-stimulus
  period, baseline-subtracted
- **Observation model** — our extractor must average simulated firing
  rates over a 500 ms window to compare against Rmax/σ, not read out an
  instantaneous or peak rate. The saturating nonlinearity is mechanistically
  attributed (by the same group, citing Kazama & Wilson 2008) to the
  combined effect of **short-term synaptic depression at the ORN-PN
  synapse** and **the PN's relative refractory period** — i.e., this curve
  should emerge from realistic synaptic depression + refractoriness, not be
  hand-fit as a static transfer function, if the goal is a mechanistic
  rather than phenomenological match
- **Conditions** — Drosophila, in vivo, adult; glomeruli DM4, DL5, VM7, DM1
  (the four for which a genetically-identified, singly-activated "private"
  odour existed)
- **Source** — Olsen SR, Bhandawat V, Wilson RI (2010) "Divisive
  normalization in olfactory population codes." *Neuron* 66(2):287-299.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2866644/ (PMID 20435004).
  Supersedes the logarithmic fit used in Bhandawat et al. 2007 and Olsen &
  Wilson 2008 — the authors state Eq. 1 fits the data better than that
  earlier log form
- **Confidence** — high; equation and all four glomeruli's fitted constants
  extracted verbatim from primary full text (not an AI-generated summary)

### T-AL-11  Divisive normalization by lateral inhibition: functional form and fitted sensitivity

- **Quantity** — how a second, "public" odour (activating many ORN types
  and thus driving population-wide lateral inhibition) modifies the private
  ORN→PN curve of T-AL-10
- **Value** — best-fitting model ("input gain control"):

  ```
  PN = Rmax · ( ORN^1.5 / (ORN^1.5 + s^1.5 + σ^1.5) )     (Eq. 2)
  s = m · LFP                                              (Eq. 4)
  ```

  where `s` is the lateral-inhibition suppression term, and `LFP` is the
  antennal local field potential, used as a proxy for total ORN population
  activity because it scales linearly with summed ORN firing (their Eq. 5:
  `LFP = (Σ_{i=1}^{24} r_i) / 190`, summed over 24 characterized ORN
  types — units as extracted are "mV·sec²/spikes", which may be a
  text-extraction artefact of a more complex printed unit; treat the
  scale factor 190 as approximate). Fitted **m = 10.63 for glomerulus VM7,
  4.19 for glomerulus DL5** — i.e., glomeruli differ substantially (~2.5x)
  in how sensitive they are to lateral inhibition. An alternative
  "response gain control" model (Eq. 3, lateral inhibition scales Rmax
  multiplicatively rather than entering the denominator) fit *worse* for
  both VM7 and DL5 (m = 0.164 for VM7 under that alternative model,
  included for completeness but not the preferred model)
- **Type** — steady-state (same 500-ms-averaging caveat as T-AL-10)
- **Method** — same preparation as T-AL-10, plus a second "public" odour
  (pentyl acetate at varying concentrations) mixed with the private odour
  to titrate total ORN population activity; antennal LFP recorded
  simultaneously as the population-activity proxy
- **Observation model** — this is the actual "divisive normalization"
  result: lateral inhibition raises the effective semi-saturation constant
  of the private-odour curve, rather than scaling its ceiling — confirmed
  by Eq. 2 outperforming Eq. 3 as a fit. A model should reproduce (a) the
  denominator-additive form, not a multiplicative-gain form, and (b) the
  per-glomerulus difference in m — a single global normalization strength
  is not what was measured
- **Conditions** — same as T-AL-10; only glomeruli VM7 and DL5 had a usable
  private odour combined with the public-odour titration design
- **Source** — same as T-AL-10
- **Confidence** — high for the equations and the VM7/DL5 m values
  (verbatim from primary text); medium for generalising m to other
  glomeruli, since only two were measured this way

### T-AL-12  Increasing total ORN population activity makes PN responses more transient (not just smaller)

- **Quantity** — PN response transience (ratio of peak firing rate to mean
  firing rate over the response) as a function of total ORN population
  activity (public-odour concentration), separately at different levels of
  direct ("private") input strength
- **Value** — mixing in a public odour makes PN responses to a *weak*
  private odour more transient; the same public odour has little effect on
  PN response dynamics when the private odour is *strong*. Reported as a
  qualitative trend across concentration series (2-butanone at 10⁻⁶, 10⁻⁵,
  10⁻⁴ as the public odour; pentyl acetate at 0, 10⁻⁶, 10⁻⁵, 10⁻⁴, 10⁻³ as
  the private odour) — no single scalar summary value given, this is a
  relationship across a concentration series, not a point estimate
- **Type** — dynamic response
- **Method** — same preparation as T-AL-10/T-AL-11; PSTHs compared across
  public/private odour concentration combinations; transience quantified as
  peak/mean firing-rate ratio
- **Observation model** — mechanistically attributed to faster recruitment
  of lateral inhibition when the ORN population responds faster/harder
  (higher public-odour concentrations produce a faster-rising antennal
  LFP). A model should show the same *conditional* effect — increased
  total activity speeds up PN dynamics specifically when direct drive is
  weak, not uniformly
- **Conditions** — same as T-AL-10
- **Source** — same as T-AL-10
- **Confidence** — high for the qualitative/conditional relationship
  (verbatim from primary text); this is explicitly not reduced to a single
  fitted time constant by the authors, so do not treat it as one

---

## 3. ORN and PN firing rates

### T-AL-13  ORN spontaneous firing rate

- **Value** — **~8 spikes/s**, population average across ORN types
  (Wilson 2013 review, citing de Bruyne et al. 1999 and de Bruyne et al.
  2001). Individual glomerulus/type-specific numbers from other Wilson-lab
  papers, all lower-confidence "unpublished observations" cited within
  peer-reviewed papers rather than a dedicated dataset: **DM4 ORNs ≈ 4
  spikes/s**, "a typical ORN" ≈ **7 spikes/s** (Kazama & Wilson 2008,
  attributed to "R.I.W., unpublished observations"); **VM7 ORNs ≈ 10
  spikes/s** (Olsen & Wilson 2008, stated directly as "each VM7 ORN fires
  spontaneously at ~10 spikes/s"). Spread across ORN types is real, not
  just noise — de Bruyne et al. found 16 distinct ORN classes with distinct
  response spectra and presumably distinct baseline rates, but we did not
  find a single table of all 16 baseline rates in this pass
- **Type** — steady-state
- **Method** — in vivo extracellular single-sensillum recording (de Bruyne
  papers, the primary source for the ORN population survey); in vivo
  extracellular recording of individual identified ORN types (Wilson-lab
  papers, for the glomerulus-specific numbers)
- **Observation model** — no odour present, i.e., baseline/inter-trial
  firing in the extractor should be measured in the absence of any odour
  input to compare against these numbers, over a window long enough to
  average out inter-spike-interval variability (not specified precisely in
  source text)
- **Conditions** — Drosophila, in vivo, adult; antenna/maxillary palp basi­
  conic and other sensilla depending on ORN type
- **Source** — de Bruyne M, Clyne PJ, Carlson JR (1999) "Odor coding in a
  model olfactory organ: the Drosophila maxillary palp." *J Neurosci*
  19(11):4520-4532. https://pubmed.ncbi.nlm.nih.gov/10341252/ — de Bruyne
  M, Foster K, Carlson JR (2001) "Odor coding in the Drosophila antenna."
  *Neuron* 30(2):537-552. https://pubmed.ncbi.nlm.nih.gov/11395013/ —
  Wilson RI (2013) "Early olfactory processing in Drosophila: mechanisms
  and principles." *Annu Rev Neurosci* 36:217-241.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3933953/ — Kazama & Wilson 2008
  (see T-AL-9) — Olsen SR, Wilson RI (2008) "Lateral presynaptic inhibition
  mediates gain control in an olfactory circuit." *Nature* 452:956-960.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2824883/
- **Confidence** — medium-high for the ~8 spikes/s population figure
  (secondary citation of a primary dataset, but the review is authoritative
  and the primary papers are the standard reference for this number);
  medium for the individual 4/7/10 spikes/s numbers, since two of the three
  are explicitly labelled "unpublished observations" rather than data from
  the paper's own formal dataset. We could not find the original Wilson,
  Turner & Laurent (2003/2004) Science paper's own quantitative baseline
  table (paywalled; only abstract text accessible in this pass — see the
  note at the end of this file)

### T-AL-14  ORN odour-evoked firing rate range

- **Value** — most odour-evoked ORN responses are **<50 spikes/s**; maximum
  ORN firing rate across the receptor repertoire (Hallem & Carlson's
  panel) is **~300 spikes/s**. A separate statement (Kazama & Wilson 2008)
  puts sustained odour-evoked ORN rates as easily going "well above 200
  spikes/s." Odours that evoke small ORN responses (<20 spikes/s) can drive
  the postsynaptic PN to >100 spikes/s — see T-AL-15
- **Type** — steady-state
- **Method** — Hallem & Carlson's dataset: in vivo single-sensillum
  extracellular recording, "Empty Neuron" heterologous expression system
  for some receptors, responses measured as spike count over a 500 ms
  window
- **Observation model** — the extractor should compare against a
  500-ms-window average, consistent with T-AL-10's use of the same dataset
  as its ORN input
- **Conditions** — Drosophila, in vivo (or heterologous "empty neuron"
  system for some receptor/sensillum combinations), adult
- **Source** — Hallem EA, Carlson JR (2006) "Coding of odors by a receptor
  repertoire." *Cell* 125(1):143-160.
  https://pubmed.ncbi.nlm.nih.gov/16615896/ — Wilson 2013 review (as
  T-AL-13) — Kazama & Wilson 2008 (as T-AL-9)
- **Confidence** — high for the ~300 spikes/s maximum (directly cited,
  consistent across two independent secondary citations); medium for the
  "well above 200 spikes/s" phrasing, which is qualitative

### T-AL-15  ORN→PN amplification example, and the ORN-PN synapse's short-term depression

- **Value** — a single ORN spike depolarizes its postsynaptic PN by ~6 mV
  at minimal stimulation frequency (0.033 Hz): unitary EPSP amplitude
  **6.19 ± 0.45 mV (N = 23)**; unitary EPSC amplitude **29.0 ± 2.6 pA
  (N = 45)**. At a stimulus frequency mimicking basal ORN firing (7 Hz),
  synaptic responses depress by **~40%** but remain relatively strong.
  Strong depression occurs at all frequencies above **~50 spikes/s**. A
  directly-quoted illustration of the resulting amplification: "odors that
  evoke small responses in ORNs (<20 spikes/s) can evoke much stronger
  responses in postsynaptic PNs (>100 spikes/s)" (citing Bhandawat et al.
  2007)
- **Type** — steady-state / dynamic response (synaptic depression is
  frequency-dependent, i.e., a dynamic property, but reported here as
  discrete operating points)
- **Method** — in vivo whole-cell patch-clamp recording from PNs; unitary
  EPSCs/EPSPs evoked by minimal-intensity electrical stimulation of the
  antennal nerve at controlled frequencies, in some experiments with
  antennae removed to isolate the ORN-PN synapse from ongoing sensory
  drive
  and lateral inputs
- **Observation model** — depression is measured as a fraction of the
  initial EPSC amplitude across a train at fixed frequency — an extractor
  comparing synaptic weights should apply the same frequency-dependent
  discount rather than treating ORN-PN synaptic strength as a fixed weight
- **Conditions** — Drosophila, in vivo, adult; glomeruli DM4 and VM2 used
  for the specific numbers above
- **Source** — Kazama H, Wilson RI (2008), as T-AL-9. Amplification claim
  originally from Bhandawat V, Olsen SR, Gouwens NW, Schlief ML, Wilson RI
  (2007) "Sensory processing in the Drosophila antennal lobe increases
  reliability and separability of ensemble odor representations." *Nat
  Neurosci* 10:1474-1482. https://pmc.ncbi.nlm.nih.gov/articles/PMC2838615/
- **Confidence** — high; EPSP/EPSC numbers and depression percentages
  extracted verbatim from Kazama & Wilson 2008 primary full text

### T-AL-16  PN maximum evoked firing rate (from the normalization fits)

- **Value** — **Rmax = 170, 167, 163, 144 spikes/s** for glomeruli DM4,
  DL5, VM7, DM1 respectively — see T-AL-10 for the full equation this comes
  from. Consistent with the "<20 spikes/s ORN → >100 spikes/s PN"
  illustration in T-AL-15
- **Type** — steady-state
- **Method/Observation model/Conditions/Source** — identical to T-AL-10;
  listed separately here only because firing-rate magnitude, not the
  normalization relationship itself, is the quantity of interest for this
  entry
- **Confidence** — high (same primary-text extraction as T-AL-10)

### T-AL-17  Original Science 2003/2004 paper: qualitative transformation, quantitative table not recovered

- **Quantity** — the founding observation that antennal-lobe PNs display
  broader odour tuning and more complex responses than their presynaptic
  ORN afferents in the same glomerulus
- **Value** — **not recovered as Hz numbers in this pass.** The abstract
  states the qualitative finding ("second-order neurons display broader
  tuning and more complex responses than their primary afferents...
  implicating lateral interactions") but we could not obtain the paper's
  full text (paywalled at Science; no PMC deposit found; CSHL repository
  record has metadata only, no full text or PDF). All quantitative ORN/PN
  Hz numbers used elsewhere in this file (T-AL-13 through T-AL-16) come
  from later papers by the same and overlapping authors (Bhandawat 2007,
  Olsen & Wilson 2008, Kazama & Wilson 2008, Olsen/Bhandawat/Wilson 2010),
  which is almost certainly what our brief's "and later work" was pointing
  at, but it means we cannot cite this specific paper's own tables
- **Type** — steady-state
- **Method** — whole-cell recording in vivo, comparing afferent (ORN) and
  postsynaptic (PN) activity within the same identified glomerulus
- **Observation model** — n/a — no extractable numeric protocol from this
  pass
- **Conditions** — Drosophila, in vivo, adult
- **Source** — Wilson RI, Turner GC, Laurent G (2003/2004) "Transformation
  of olfactory representations in the Drosophila antennal lobe." *Science*
  303(5656):366-370. https://www.science.org/doi/10.1126/science.1090782
  (task-supplied link; PMID 14684826)
- **Confidence** — low/not applicable for a quantitative value; this entry
  exists to document the gap rather than to supply a number. If full-text
  access becomes available, re-visit this entry first

### T-AL-18  PN response reliability exceeds ORN reliability (companion finding, not one of the six requested items but directly adjacent)

- **Quantity** — trial-to-trial reliability of odour-evoked responses,
  compared between ORNs and their postsynaptic PNs
- **Value** — PN responses are significantly more reliable (lower
  trial-to-trial variability) than ORN responses to the same odour,
  p < 10⁻¹⁵ (Mann-Whitney U-test), N = 779 ORN responses and 843 PN
  responses, whether measured over the whole stimulus period or a 100 ms
  epoch at the response peak
- **Type** — steady-state
- **Method** — in vivo extracellular (ORN) and whole-cell (PN) recording,
  repeated presentations of the same odour to the same synaptically-
  connected ORN-PN pair
- **Observation model** — a model in which PN spiking is a simple
  feedforward readout of noisy ORN input, with no independent
  noise-reduction mechanism, would not reproduce this reliability gain. Not
  requested by name in our brief but flagged because it is a companion
  finding in the same paper we were told to check for T-AL-9/T-AL-15
- **Conditions** — Drosophila, in vivo, adult, 500 ms odour pulses
- **Source** — Bhandawat et al. 2007, as T-AL-15
- **Confidence** — high; verbatim statistics from primary full text

---

## 4. Local interneurons (LN): count, spiking fraction, firing rates

This is the section most directly relevant to the 350 Hz problem named in
`theory-review.md` §1.

### T-AL-19  Non-spiking LNs exist and their mechanism is known; the fraction of all LNs that are non-spiking is **not quantified**

- **Quantity** — existence, mechanism, and population fraction of
  non-spiking antennal-lobe local interneurons
- **Value** — one genetically-defined LN population (R32F10-Gal4, "patchy"
  innervation pattern) is non-spiking: no action potentials under current
  injection (N = 9 cells tested with voltage steps) and no detectable
  TTX-sensitive sodium current in voltage clamp. Mechanism: the `para`
  (voltage-gated sodium channel) transcript **is** detected by HCR in situ
  hybridization in both non-spiking and spiking LN populations (N = 14
  R32F10-Gal4, N = 12 R70A09-Gal4 [spiking control line]; p = 0.18, not
  significant — i.e., transcription is not reduced) but Para **protein**
  (FlpTag reporter) is significantly reduced in the non-spiking population
  (N = 12 R32F10-Gal4 vs. N = 14 R70A09-Gal4; p = 0.000035) — i.e.,
  **post-transcriptional/translational regulation**, not a transcriptional
  or genomic knockout, silences the sodium current. **The paper explicitly
  characterises only this one driver line and does not attempt, and does
  not report, a fraction of all AL LNs that are non-spiking.** This
  directly confirms what `theory-review.md` §1 already suspected ("The
  paper characterises one population and does not quantify what fraction
  of all LNs is non-spiking") — we searched specifically for a follow-up
  quantifying the fraction and found none
- **Type** — steady-state (a population/mechanistic property, not a rate)
- **Method** — whole-cell patch clamp in vivo (current clamp for spiking
  test, voltage clamp for Na⁺ current), digitized at 10 kHz; HCR (hybrid­
  ization chain reaction) in situ for `para` transcript; FlpTag protein
  reporter for Para protein; GCaMP7b wide-field calcium imaging at 20
  frames/s for odour-response mapping
- **Observation model** — a model wanting to reproduce this should
  implement at least two LN populations with different intrinsic dynamics
  (graded/non-spiking vs. spiking), gated by a mechanism equivalent to
  translational suppression of sodium conductance — not by simply setting
  a subset of LN sodium conductances to zero at the parameter level only
  (the biology is a specific regulatory mechanism, potentially odour- or
  state-dependent, though this was not tested)
- **Conditions** — Drosophila, in vivo, adult (electrophysiology: 1-2 days
  post-eclosion; imaging: 7-9 days post-eclosion); odour panel = pentyl
  acetate at 10⁻¹⁰, 10⁻⁸, 10⁻⁶, 10⁻⁴ dilutions, plus pure cVA
- **Source** — Schenk JE, Gaudry Q (2023) "Nonspiking Interneurons in the
  Drosophila Antennal Lobe Exhibit Spatially Restricted Activity." *eNeuro*
  10(1):ENEURO.0109-22.2022. https://www.eneuro.org/content/10/1/ENEURO.0109-22.2022
  (task-supplied link; PMID 36650069)
- **Confidence** — high for the existence/mechanism claims (verified against
  primary full text); high-confidence **absence claim** for the
  unquantified fraction (this is the central "if nobody has quantified it,
  say so" item our brief asked for)

### T-AL-20  Total LN count and cell-type census: two incompatible-looking numbers, likely counting different things

- **Value** — **~100** ipsilaterally-projecting LNs estimated per antennal
  lobe, from a genetic/anatomical survey of >1,500 individual LNs across
  many brains (MARCM single-cell clones) (Chou et al. 2010). Separately,
  the 2021 hemibrain connectome reports **196 antennal-lobe local neurons
  (ALLNs) in one (right) hemisphere**, sorted into **5 lineages, 4
  morphological classes, 25 anatomical groups, and 74 cell types** (quote
  verified verbatim: "We find 196 ALLNs in the right hemisphere which we
  assign to 5 lineages, 4 morphological classes, 25 anatomical groups and
  74 cell types") (Schlegel, Bates et al. 2021). **We record both rather
  than picking one.** The ~2x discrepancy (100 vs. 196) is plausibly
  because Chou et al.'s estimate covers only the ipsilaterally-projecting,
  GABAergic-lineage-derived LNs they were genetically sampling, while the
  hemibrain count is a complete EM census including any bilateral/
  cholinergic/other LNs the genetic approach may have under-sampled — but
  neither paper reconciles the two numbers with each other, so this is our
  inference, not a stated resolution
- **Type** — steady-state (anatomical/connectomic census)
- **Method** — Chou et al.: MARCM clonal genetic labelling + confocal
  reconstruction + hierarchical clustering of glomerular innervation
  patterns, N > 1,500 individual LNs, 1,489 used for the ipsilateral
  projection analysis. Schlegel/Bates et al.: EM reconstruction (hemibrain
  connectome) + connectivity-based clustering
- **Observation model** — "how many LN types should our model have" does
  not have a single citable answer; 74 (EM cell types) is the more
  authoritative modern number if the model is meant to be
  connectome-matched, but note it is a *morphological/connectivity*
  typology, not a physiological (spiking/non-spiking, or fast/slow) one —
  it says nothing about which of the 74 types map onto the non-spiking
  population in T-AL-19
- **Conditions** — Chou et al.: Drosophila, various Gal4 driver lines,
  female flies 0-14 days old (some lines used males only, noted per-line);
  Schlegel/Bates et al.: hemibrain EM volume, one adult female fly, right
  hemisphere only
- **Source** — Chou YH, Spletter ML, Yaksi E, Leong JCS, Wilson RI, Luo L
  (2010) "Diversity and wiring variability of olfactory local interneurons
  in the Drosophila antennal lobe." *Nat Neurosci* 13(4):439-449.
  https://www.nature.com/articles/nn.2489 (PDF:
  https://luolab.stanford.edu/sites/g/files/sbiybj20556/files/media/file/chou_spletter_yaksi_et_al_natneurosci_2010_0.pdf) —
  Schlegel P, Bates AS, et al. (2021) "Information flow, cell types and
  stereotypy in a full olfactory connectome." *eLife* 10:e66018.
  https://elifesciences.org/articles/66018
- **Confidence** — high for each number individually (both verified against
  primary text/quotes); the reconciliation between them is our inference
  and should be treated as low confidence

### T-AL-21  LN morphology is individually variable, not cleanly typed, within at least one major class

- **Value** — of 161 individually-reconstructed "patchy"-class LNs, **all
  161 showed distinct glomerular innervation patterns** — no two identical.
  Each patchy LN occupies an estimated 13.1 ± 1.6% of antennal-lobe volume
  (mean ± SD, N = 8), implying ~8 such cells could tile an entire antennal
  lobe, but which glomeruli any individual patchy LN covers is
  fly-to-fly variable, not stereotyped
- **Type** — steady-state
- **Method** — MARCM single-cell clonal labelling and confocal
  reconstruction, cross-fly comparison of innervation patterns
- **Observation model** — this argues against building a single
  "canonical" LN wiring diagram for the patchy class the way one would for
  ORN→PN glomerular wiring (which *is* highly stereotyped); a model
  targeting this class should treat glomerulus-level LN connectivity as
  drawn from a distribution, not fixed
- **Conditions** — Drosophila, as T-AL-20 (Chou et al.)
- **Source** — same as T-AL-20 (Chou et al. 2010)
- **Confidence** — high; verbatim from primary full text ("no two cells had
  identical innervation patterns")

### T-AL-22  Spiking LN firing rates by genetically-defined line (the closest thing we found to "firing rates of the ones that do spike")

- **Value** — from whole-cell patch-clamp recordings of five Gal4-defined
  LN lines (the paper's internal numbering, lines 5-9; specific molecular
  identities beyond the driver line are not given in the text we
  extracted), all values in spikes/s (mean ± SEM) except the last column
  (% of total odour-evoked spikes occurring in the first 100 ms):

  | Line | Spontaneous | Max odour response | Mean odour response | % spikes in first 100 ms |
  |------|-------------|---------------------|----------------------|---------------------------|
  | 5    | 4.0 ± 0.4   | 15.7 ± 1.7          | 8.7 ± 1.4            | 14 ± 1                    |
  | 6    | 4.5 ± 0.7   | 7.0 ± 1.0           | 2.5 ± 0.6            | 21 ± 2                    |
  | 7    | 16.8 ± 1.7  | 1.5 ± 1.2           | −3.1 ± 1.2 (net suppression) | 23 ± 2            |
  | 8    | 5.2 ± 0.6   | 2.7 ± 1.1           | −0.3 ± 0.7           | 43 ± 4                    |
  | 9    | 7.8 ± 2.1   | 18.1 ± 5.5          | 7.7 ± 3.5            | 17 ± 3                    |

  Note line 7's high spontaneous rate (16.8 Hz) paired with net
  odour-evoked *suppression* — this line is very likely (or overlaps
  strongly with) the panglomerular class described separately, see
  T-AL-23
- **Type** — steady-state
- **Method** — in vivo whole-cell patch clamp, odour panel presented to
  each recorded cell, responses averaged across cells within each Gal4 line
- **Observation model** — these are the only concrete, tabulated Hz values
  for genetically-identified *spiking* LN populations we could find in the
  literature. If our model's LN firing rates are to be checked against
  real spiking-LN data, this table — not an assumed "LNs fire fast"
  prior — is the closest available ground truth, and it is far below
  350 Hz: max recorded mean was ~18 spikes/s, max single-line odour peak
  ~15.7-18.1 spikes/s
- **Conditions** — Drosophila, in vivo, adult, as T-AL-20
- **Source** — same as T-AL-20 (Chou et al. 2010)
- **Confidence** — high for the table values (extracted verbatim from
  primary full text); medium for our inference linking line 7 to the
  panglomerular class (not stated explicitly as identical in the extracted
  text)

### T-AL-23  Panglomerular LNs: higher spontaneous rate, weaker/suppressive odour response, than other LN classes

- **Value** — panglomerular LNs (innervating most/all glomeruli), N = 26,
  comprising **28%** of all LNs recorded in this physiology dataset, have
  **significantly higher spontaneous firing rates** than other LNs
  (p < 0.01) and **significantly weaker mean and maximum odour responses**
  (p < 0.05, t-tests). In the presence of odour, spontaneous spiking in
  many panglomerular cells shuts down completely (sometimes after a brief
  burst at odour onset); others modestly increase firing. A second,
  separate morphological class — LNs that selectively avoid glomerulus
  VA1d (and frequently DL3, both innervated by pheromone-selective trichoid
  ORNs) — accounts for **~15%** of all LNs in the dataset
- **Type** — steady-state
- **Method** — same as T-AL-22
- **Observation model** — the finding that LNs innervating *more*
  glomeruli have *lower* odour-evoked firing (Pearson's r = −0.2, p < 0.05
  between glomerulus count innervated and odour-response strength) is a
  specific, checkable relationship, not just a rate — a model with a
  single homogeneous "LN" population cannot reproduce this anti-correlation
  by construction
- **Conditions** — same as T-AL-20
- **Source** — same as T-AL-20 (Chou et al. 2010)
- **Confidence** — high; verbatim from primary full text

### T-AL-24  Four electrophysiologically distinct LN classes by intrinsic properties (independent classification, predates the non-spiking discovery)

- **Value** — whole-cell patch-clamp characterisation identifies **four
  classes of LNs** with distinct intrinsic electrophysiological properties:
  differences in firing pattern, degree of spike adaptation, and spike
  afterhyperpolarization amplitude. **One class shows burst firing; the
  other three are tonically active.** Morphologically, three classes
  innervate almost all glomeruli, one innervates a specific glomerular
  subpopulation. No Hz values recovered from the abstract/summary we could
  access; this paper's classification is entirely about spiking LNs — by
  construction, since burst/tonic firing pattern and afterhyperpolarization
  amplitude are properties that presuppose spiking, this 2010 study would
  not have detected a non-spiking population even if it were present in
  its sample, which is consistent with the non-spiking phenomenon only
  being reported over a decade later (T-AL-19)
- **Type** — steady-state
- **Method** — whole-cell patch-clamp recording, morphological
  reconstruction, hierarchical clustering by electrophysiological and
  anatomical properties
- **Observation model** — flagged mainly as a caution: this is a second,
  independent (Max Planck, not Wilson/Luo lab) LN classification scheme
  (four electrophysiological classes) that does not obviously map onto
  either Chou et al.'s morphological classes (T-AL-20 to T-AL-23) or the
  74-cell-type hemibrain typology (T-AL-20) — nobody has cross-walked these
  three classification schemes against each other as far as we found
- **Conditions** — Drosophila, in vivo, adult
- **Source** — Seki Y, Rybak J, Wicher D, Sachse S, Hansson BS (2010)
  "Physiological and morphological characterization of local interneurons
  in the Drosophila antennal lobe." *J Neurophysiol* 104(2):1007-1019.
  https://pubmed.ncbi.nlm.nih.gov/20505124/
- **Confidence** — medium; we could only access the abstract in this pass,
  not primary full-text numbers

### T-AL-25  Locust antennal-lobe LNs are largely non-spiking by a different mechanism (cross-species context, not Drosophila)

- **Value** — in locust, antennal-lobe local neurons generate **no
  conventional action potentials**, instead producing TTX-resistant
  "spikelets" of variable amplitude, thought to be driven by
  voltage-dependent calcium currents rather than sodium-based action
  potentials
- **Type** — steady-state
- **Method** — intracellular recording from locust antennal-lobe LNs, TTX
  application
- **Observation model** — important cross-species context for T-AL-19:
  non-spiking (or non-canonically-spiking) local interneurons in the
  antennal lobe are not a Drosophila-specific oddity — a related phenomenon
  (different biophysical mechanism: absent/suppressed Ca²⁺ spikelets in
  locust vs. suppressed Na⁺ current translation in Drosophila) has been
  known in locust for decades. This raises prior confidence that
  non-spiking signalling is a general feature of insect antennal-lobe LN
  circuits, not a one-off Drosophila finding restricted to a single driver
  line
- **Conditions** — locust, in vivo, intact antennal lobe
- **Source** — this specific claim was recovered from a secondary-source
  search summary describing Laurent G, Davidowitz H (1994) "Encoding of
  olfactory information with oscillating neural assemblies." *Science*
  265(5180):1872-1875. https://pubmed.ncbi.nlm.nih.gov/17797226/ — we were
  **not able to independently verify this specific sentence against
  primary full text** in this pass (older Science paper, no PMC deposit
  found)
- **Confidence** — low/medium — flagged explicitly because it is a
  secondary-source claim we could not verify against the primary text
  ourselves; treat as a lead to re-check, not a settled fact, before
  relying on it

### T-AL-26  ShakB (not Inx7) is a second, distinct gap-junction protein at AL PN-PN synapses

- **Value** — the innexin ShakB, genetically and molecularly distinct from
  Inx7 (see T-AL-1 to T-AL-4), also "contributes to electrical synapses
  between AL projection neurons (PNs) in Drosophila," per the introduction
  of the Inx7 paper; ShakB additionally forms the well-characterised
  rectifying electrical synapses of the giant-fibre escape circuit
  (unrelated to olfaction). No knockdown/perturbation of ShakB was
  performed in the Inx7 study — its role in the AL is stated as prior
  background, not re-measured
- **Type** — steady-state (background/anatomical fact, not a new
  measurement)
- **Method** — n/a (cited prior literature within the Inx7 paper's
  introduction)
- **Observation model** — relevant only insofar as a model including gap
  junctions between AL PNs should not assume Inx7 is the *only* gap
  junction protein there — at least two (Inx7, ShakB) are implicated, of
  four innexins expressed in Drosophila neurons generally (`inx5`, `inx6`,
  `inx7`, `shakB`, per `theory-review.md` §2)
- **Conditions** — n/a
- **Source** — Fuenzalida-Uribe et al. 2025, as T-AL-1 (introduction section)
- **Confidence** — medium; this is the paper's own background citation, not
  independently re-verified against the ShakB primary literature by us in
  this pass

---

## 5. Odour-evoked oscillations

**This section directly corrects `lab-notebook.md` (2026-09-13, "One
correction to the framing"), which states "Odour-evoked oscillations at
20-30 Hz structure spike timing in the insect antennal lobe" without a
species qualifier.** Our findings: the well-replicated 20 Hz figure is
**locust**; the one Drosophila study we found that directly measured
odour-evoked LFP oscillation frequency reports **~10 Hz**, not 20-30 Hz. A
separate, frequently-cited "20-30 Hz" figure for Drosophila brain LFP
activity exists but describes a different phenomenon (visual
salience/attention, not odour-evoked antennal-lobe oscillation) — see
T-AL-30. **Species matters here exactly as our brief warned.**

### T-AL-27  Locust: ~20 Hz odour-evoked oscillation, Kenyon cells phase-locked

- **Value** — odour presentation (not clean air) evokes spatially coherent
  local field potential oscillations in the ipsilateral mushroom body, with
  a frequency of **approximately 20 Hz**, independent of odorant identity.
  Autocorrelograms of spontaneous (non-odour-evoked) LFP activity show
  small peaks at ±50 ms, consistent with an intrinsic ~20 Hz resonance of
  the mushroom-body network even without stimulation. During odour-evoked
  oscillation, Kenyon cell membrane potential oscillates around resting
  level under phase-locked excitatory input; each depolarizing phase can be
  amplified by dendritic excitable properties and sometimes produces one
  action potential, phase-locked to the population oscillation. Notably,
  this 1994 paper reports the oscillation was **not** seen in antennal-lobe
  LFP recordings themselves, only in the mushroom body — suggesting (at
  least in this dataset) generation in the mushroom body or via feedback,
  which is a different circuit locus than later work (T-AL-7, T-AL-8,
  Drosophila) attributes the oscillation to (antennal-lobe LN-driven
  feedback inhibition, per Laurent's own later papers e.g. MacLeod &
  Laurent 1996, T-AL-5) — flagged as a within-literature evolution of the
  model, not necessarily a contradiction, but worth noting
- **Type** — dynamic response (steady-state frequency, but a response
  property, not a rate)
- **Method** — intracellular and local-field-potential electrode recording
  in vivo, olfactory stimulation of one antenna
- **Observation model** — our extractor would need an LFP-like aggregate
  signal (e.g., summed/filtered population membrane potential) rather than
  a single-unit spike train to compare against a reported oscillation
  frequency; a spike-based readout should look for ~20 Hz periodicity in
  population spike-time histograms as a proxy
- **Conditions** — locust, species stated in secondary sources as
  *Schistocerca americana* (not independently re-confirmed against this
  specific paper's own methods text in this pass — see T-AL-25's caveat,
  same source-access limitation), in vivo, intact brain
- **Source** — Laurent G, Naraghi M (1994) "Odorant-induced oscillations in
  the mushroom bodies of the locust." *J Neurosci* 14(5):2993-3004.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6577505/ (PMID 8182454, full
  abstract verified against primary source; body text beyond the abstract
  was not accessible to us)
- **Confidence** — high for the ~20 Hz figure itself (abstract text
  verified directly, and independently corroborated by Laurent & Davidowitz
  1994 Science and multiple later Laurent-lab papers using the same ~20 Hz
  figure); medium for the "not seen in antennal lobe LFP" detail and the
  exact species name (both from abstract/secondary sources only)

### T-AL-28  Drosophila: ~10 Hz odour-evoked oscillation in the mushroom body calyx (not 20-30 Hz)

- **Value** — common food odours at natural concentrations elicit LFP
  oscillations in the mushroom-body calyx with **an average frequency of
  ~10 Hz** (quote verified verbatim against primary full text: "we found
  that oscillatory responses with an average frequency of ∼10 Hz could be
  elicited"). Recordings/analysis used a 5-30 Hz (sometimes 5-15 Hz for
  phase analysis) bandpass filter and searched for maximal spectral power
  between 5-45 Hz — i.e., the ~10 Hz figure is the actual measured peak
  within a broader analysis window, not an artefact of a narrow filter
  choice. This is the perturbation target described in T-AL-7/T-AL-8
  (LN2 silencing, picrotoxin)
- **Type** — dynamic response
- **Method** — paired intracellular (antennal-lobe PNs/LNs) and LFP
  (mushroom-body calyx) recording in vivo, natural and synthetic odours
- **Observation model** — same as T-AL-27 (LFP-like aggregate signal, or
  population PSTH periodicity, at ~10 Hz rather than ~20-30 Hz for a
  Drosophila-specific model)
- **Conditions** — Drosophila, in vivo, intact brain, adult
- **Source** — Tanaka, Ito, Stopfer 2009, as T-AL-7
- **Confidence** — high; frequency figure and filter bandwidths extracted
  verbatim from primary full text via direct HTML retrieval (not an AI
  summary)

### T-AL-29  Drosophila oscillation: PN/LN phase relationship differs from locust

- **Value** — the timing relationship between PN spikes and the phase of
  LFP oscillations (5-15 Hz bandpass) is consistent: 799 spikes from 4
  cells, LFP cycle maximum defined as 0°, minimum as 180°. LN1 and LN2
  spikes are also phase-consistent with the LFP (362 spikes from 4 LN1
  cells, 234 spikes from 6 LN2 cells). Reported comparison to locust:
  Drosophila PNs lead LNs by **~20° per cycle**, versus **~180°** in
  locust — attributed to differences in spike-generation mechanisms between
  the two species' local neurons (recall locust LNs largely produce
  TTX-resistant spikelets, not conventional spikes — T-AL-25 — which is a
  plausible mechanistic reason for the very different phase relationship)
- **Type** — dynamic response
- **Method** — same as T-AL-28, phase-histogram analysis of intracellular
  spikes relative to simultaneously-recorded LFP
- **Observation model** — a model with distinguishable PN and LN
  populations and an emergent oscillation should reproduce a PN-leads-LN
  phase relationship on the order of tens of degrees for Drosophila
  specifically, not the ~180° antiphase relationship reported for locust
- **Conditions** — Drosophila, as T-AL-28
- **Source** — same as T-AL-28
- **Confidence** — high for the Drosophila phase numbers (verbatim from
  primary text); medium for the locust "~180°" comparison figure, which we
  extracted as a comparative statement rather than independently verifying
  against a locust primary source in this pass

### T-AL-30  A separate "20-30 Hz" Drosophila brain-oscillation figure exists, but is not an odour-evoked antennal-lobe phenomenon — flagged to prevent conflation

- **Value** — "Salience modulates 20-30 Hz brain activity in Drosophila" is
  a real, separate, frequently-cited result, but it concerns **visual
  attention/salience-linked central-brain LFP activity**, not odour-evoked
  antennal-lobe/mushroom-body oscillation. We surfaced this paper because
  it is the only primary source we found anywhere in the Drosophila
  literature actually stating a "20-30 Hz" figure for fly brain LFP — which
  makes us suspect it, rather than an olfaction-specific paper, may be the
  ultimate source of the "20-30 Hz" figure currently used in
  `lab-notebook.md`, possibly via conflation with the (correctly) frequently
  co-cited locust olfactory-oscillation literature. We did not access this
  paper's full text and cannot confirm or rule out an olfactory component
  to its findings; we flag it as a **likely but unconfirmed** source of
  possible terminology conflation, not as evidence about the antennal lobe
  itself
- **Type** — steady-state (of the cited phenomenon; not olfactory)
- **Method** — not reviewed in this pass beyond the title/existence check
- **Observation model** — n/a — this entry exists as a caution, not a
  fitting target
- **Conditions** — Drosophila, presumably visual stimulation paradigm
  (based on title alone)
- **Source** — van Swinderen B, Greenspan RJ (2003) "Salience modulates
  20-30 Hz brain activity in Drosophila." *Nat Neurosci* 6:579-586.
  https://pubmed.ncbi.nlm.nih.gov/12717438/
- **Confidence** — low, deliberately — this entry is a documented suspicion
  about *why* a number might be wrong elsewhere, not a verified fact about
  this paper's content

### T-AL-31  Kenyon-cell phase-sensitivity mechanism (coincidence detection), locust

- **Value** — the transformation from dense/redundant antennal-lobe odour
  representations to sparse mushroom-body (Kenyon cell) representations
  depends on a combination of oscillatory dynamics and intrinsic/circuit
  properties acting as a temporal filter — i.e., Kenyon cells are
  positioned as coincidence detectors reading out the phase-structured PN
  population output described in T-AL-27. This is the mechanistic paper
  underlying the general claim "Kenyon cells are sensitive to oscillation
  phase" in our brief. We could not access full text and so cannot report
  the specific coincidence-detection time window (commonly discussed in
  secondary literature as several milliseconds, but we do not have a
  verified primary-text number for this pass)
- **Type** — dynamic response
- **Method** — not recovered beyond the abstract in this pass
- **Observation model** — n/a — see confidence note
- **Conditions** — locust, in vivo
- **Source** — Perez-Orive J, Mazor O, Turner GC, Cassenaer S, Wilson RI,
  Laurent G (2002) "Oscillations and sparsening of odor representations in
  the mushroom body." *Science* 297(5580):359-365.
  https://www.science.org/doi/10.1126/science.1070502 (PMID 12130775)
- **Confidence** — medium for the qualitative mechanism (well-known,
  highly-cited result, abstract verified against primary source); low for
  any specific quantitative time window, which we could not verify in this
  pass — do not cite a specific millisecond value from memory for this
  paper without re-verifying against full text

---

## 6. Temporal dynamics of PN responses

### T-AL-32  PN responses rise and decay faster than their presynaptic ORNs (statistically verified, no single "peak time" number)

- **Value** — comparing peri-stimulus time histograms averaged across all
  odours and glomeruli: **PN responses peak significantly faster than ORN
  responses** (p < 10⁻⁷, paired t-test, N = 69 odour/glomerulus
  combinations); PNs have a **shorter latency to reach 90% of response
  peak**; PN responses show **faster decay from peak to half-peak** than
  ORNs (p < 10⁻⁵, paired t-test); a **larger fraction of total PN spike
  count falls within the first 200 ms after odour onset**, compared to
  ORNs, in the same 500-ms-odour-pulse paradigm. For reference, ORN
  responses in this same paradigm "typically do not peak until 100-300 ms
  after odor onset." **We did not find a single stated "PN responses peak
  at N ms" scalar** — the paper reports these as paired statistical
  comparisons (PN faster than ORN) and as a spike-count-fraction measure,
  not as an absolute peak-latency number for PNs alone. Treat our brief's
  "PN responses peak around 200 ms" as an approximate paraphrase of the
  "more spikes within the first 200 ms" finding, not a verbatim quote from
  this source
- **Type** — dynamic response
- **Method** — in vivo extracellular (ORN) and whole-cell (PN) recording,
  500 ms odour pulses, PSTHs peak-normalized and averaged across all
  odour/glomerulus pairs
- **Observation model** — an extractor comparing "PN peak timing" to a
  simulated model should use the *ORN-relative* comparison (is the
  simulated PN's peak-to-half-decay time shorter than its ORN input's, by
  a comparable margin) rather than trying to match a single absolute
  millisecond figure, since the source data does not supply one
- **Conditions** — Drosophila, in vivo, adult, 500 ms odour stimulus period
- **Source** — Bhandawat et al. 2007, as T-AL-15
- **Confidence** — high for the statistical comparisons (verbatim,
  including exact p-values and N); the "~200 ms" framing itself is
  medium-confidence as an approximation of what the paper actually reports

### T-AL-33  ORN response kinetics: peak latency depends strongly on stimulus sharpness

- **Value** — with a fast/sharp stimulus onset, Drosophila ORN responses
  can **peak in as little as 30 ms and terminate within 200 ms**. With the
  slower odour-delivery kinetics typical of standard olfactometer pulses
  (as used in Bhandawat et al. 2007, T-AL-32), ORN responses instead
  typically peak 100-300 ms after nominal odour onset. For comparison,
  vertebrate (moth) ORN responses to a brief (25 ms) odour pulse take
  ~400 ms to peak and ~1,000 ms to terminate — i.e., Drosophila ORN
  transduction is intrinsically much faster than the moth's, but the
  *observed* peak latency in any given experiment is dominated by the
  odour-delivery device's own rise time, not just the receptor's intrinsic
  speed
- **Type** — dynamic response
- **Method** — fast odour-delivery methods with photoionization-detector-
  verified onset kinetics (Nagel & Wilson 2011; Schuckel et al. 2009), vs.
  standard olfactometer-pulse methods (Bhandawat et al. 2007)
- **Observation model** — **this is a methods-dependent number, not a
  fixed biological constant** — our own extractor's simulated "odour onset"
  must be defined the same way (instantaneous receptor-level stimulus vs.
  olfactometer-output-referenced) as whichever source number we are
  comparing against, or the comparison is meaningless
- **Conditions** — Drosophila (main figure), moth used only for
  cross-species speed comparison
- **Source** — cited within Wilson RI (2013) review, as T-AL-13, drawing on
  Nagel KI, Wilson RI (2011) and Bhandawat V et al. (2005, moth data) and
  Bhandawat et al. (2007, Drosophila standard-pulse data)
- **Confidence** — medium; we have not independently verified the Nagel &
  Wilson 2011 primary source's own numbers in this pass, only the review's
  citation of them

### T-AL-34  PN slow adaptation (calcium): multi-second time constants, presynaptic in origin

- **Value** — ORN calcium responses to a sustained, fluctuating odour
  stimulus stay sustained over the full stimulus duration, but **PN
  calcium responses adapt within tens of seconds**: it reproducibly took
  **~20 s** for PN calcium dynamics to reach steady state after stimulus
  onset. Fitting an exponential decay to the peak response of each pulse in
  a pseudorandom stimulus sequence gave decay time constants that **ranged
  from ~1 to ~40 s across glomeruli**, glomerulus- and concentration-
  dependent — e.g., glomeruli D and DC1 adapted slowly (**τ ≈ 30 s**),
  DL1 and DL5 adapted fast (**τ ≈ 4 s**); glomerulus DM1 specifically:
  responses decreased to ~50% of initial amplitude, with fitted decay
  timescales of **3-10 s**. Recovery from this slow adaptation took
  ~1 minute. Mechanistically attributed to **slow presynaptic depression of
  vesicle release** at the ORN-PN synapse (distinct from — and slower
  than — the fast, spike-driven short-term synaptic depression in T-AL-15).
  The authors explicitly state this slow PN adaptation is "of a different
  nature" than adaptation previously reported in locust (Stopfer & Laurent
  1999) or fly (Das et al. 2011) — **an acknowledged discrepancy with
  earlier literature that was not resolved**, only noted, by this 2019
  paper
- **Type** — dynamic response
- **Method** — in vivo two-photon calcium imaging, GCaMP3 and GCaMP6f,
  ORNs (orco-GAL4), PNs (GH146-GAL4) and LNs (NP2426) imaged in the same
  glomerulus (mainly DM1, DM4); pseudorandom odour-pulse sequences (pulse
  and gap durations 300 ms-2.7 s) and fixed-background/fixed-pulse
  paradigms; exponential fits to peak-response-vs-time series. Indicator
  kinetics were separately characterized and deconvolved (τ = 0.7 s for
  GCaMP6f in one calibration, 0.2 s in another — flagged by the paper's own
  published peer review as an internal inconsistency between figures,
  alongside a separately-noted inconsistency in a fitted linear-filter
  time constant τ₂, which the reviewers found to vary between ~1 s and
  ~10 s across different figures in the same paper)
- **Observation model** — **this is calcium-imaging data, not spike rate**
  — our extractor must convolve simulated spike trains with a GCaMP-like
  indicator kernel (the paper's own τ ≈ 0.2-0.7 s range for GCaMP6f) before
  comparing to these multi-second adaptation time constants, exactly the
  kind of observation-model mismatch this targets file's format is meant to
  prevent. Do not compare a raw simulated firing-rate adaptation curve
  directly to these τ values
- **Conditions** — Drosophila, in vivo, adult; odour = methyl acetate at
  various dilutions (10⁻⁹ to 10⁻⁵ range across experiments)
- **Source** — Martelli C, et al. (2019) "Slow presynaptic mechanisms that
  mediate adaptation in the olfactory pathway of Drosophila." *eLife*
  8:e43735. https://pmc.ncbi.nlm.nih.gov/articles/PMC6581506/
- **Confidence** — high for the τ ranges and the ~20 s steady-state latency
  (verbatim from primary full text, including the published peer-review
  discussion of internal inconsistencies); the paper itself flags some
  internal figure-to-figure inconsistency in the exact τ₂ value, which we
  are passing through rather than resolving — this is a case of "where the
  paper disagrees with itself," reported as instructed

### T-AL-35  Fast PN adaptation is not intrinsic to the PN membrane (cross-reference)

- See T-AL-9 (Kazama & Wilson 2008 current-injection control) — listed here
  again only as a pointer, since it is the fast-timescale complement to
  T-AL-34's slow-timescale finding, and both should be read together when
  deciding how to implement PN adaptation: **fast component is not
  intrinsic (T-AL-9); slow component (tens of seconds) is presynaptic
  vesicle-release depression (T-AL-34); the intermediate short-term
  synaptic depression at fixed stimulation frequencies (T-AL-15) is a
  third, distinct timescale/mechanism again.** Nobody has published a
  single unified model spanning all three timescales in the sources we
  reviewed.

---

## Summary of explicit gaps (per README instruction to say so when a number does not exist)

1. **Fraction of antennal-lobe LNs that are non-spiking vs. spiking is not
   quantified anywhere we could find** (T-AL-19). This is the single most
   important unresolved number for fixing the 350 Hz LN problem, and as far
   as we can tell nobody has measured it as of the 2023 eNeuro paper.
2. The original Wilson, Turner & Laurent (2003/2004) Science paper's own
   quantitative ORN/PN firing-rate tables were not recovered (paywalled,
   no PMC deposit found) — all Hz numbers in this file come from later
   Wilson-lab papers instead (T-AL-17).
3. No single scalar "PN peak latency in ms" number exists in the literature
   we found; only ORN-relative statistical comparisons (T-AL-32).
4. No fitted time constant exists for the fast component of PN response
   transience/adaptation — only a demonstration that it is not intrinsic to
   the PN membrane (T-AL-9) and must therefore be synaptic, plus a
   frequency-dependent depression curve without a single tau (T-AL-15).
5. The Kenyon-cell coincidence-detection time window (T-AL-31) is
   qualitatively well established but we could not verify a specific
   millisecond value against primary text in this pass.
6. Cross-walking the three independent LN classification schemes (Chou et
   al. morphological, Seki et al. electrophysiological, hemibrain
   connectomic cell types) against each other, and against the
   spiking/non-spiking split, has apparently not been done by anyone
   (T-AL-20, T-AL-24).
