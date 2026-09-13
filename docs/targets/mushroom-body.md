# Mushroom body targets

Scope: Kenyon cells (KC), the APL neuron, mushroom body output neurons (MBON),
and the dopaminergic neurons that innervate the mushroom body (PPL1, PAM).
Perturbations first, per the priority rule in `README.md`.

Everything below was pulled directly from primary sources (full text where
accessible — eLife and PMC copies are open access and were fetched directly;
Nature/Cell/J Neurophysiol paywalled pages were worked around via PMC, author
PDFs, or institutional repositories). Where I only had abstract-level access,
that is stated. Nothing here is estimated or back-calculated from unrelated
numbers without saying so.

---

## APL perturbations (causal — highest priority)

### T-MB-01  APL synaptic block increases KC odor-evoked Ca2+ response

- **Quantity** — change in KC population odor-evoked calcium transient
  amplitude when APL output is acutely blocked
- **Value** — "large temperature-dependent increase" in odor-evoked Ca2+
  transients at the restrictive temperature, P < 0.001 (Friedman test with
  Dunn's multiple comparisons), n = 16 hemispheres (15 flies). Exact fold
  change is given only graphically (Fig. 1b/2b of the source), not as text —
  I could not recover a single number for "how much bigger."
- **Type** — perturbation
- **Method** — in vivo two-photon Ca2+ imaging, GCaMP3, mb247-LexA driver,
  910 nm excitation, frame time interpolated to 0.09 s (~11 Hz effective)
- **Observation model** — UAS-shibire-ts1 in APL neurons; permissive 22 °C
  vs. restrictive 32 °C (32 °C held for 15 min before and throughout imaging).
  Response = ΔF/F over the odor pulse against a pre-stimulus baseline average.
- **Conditions** — male and female flies, 1–7 days post-eclosion, reared at
  18 °C, imaged restrained (cuticle/trachea removed, superfused), 10⁻² odor
  dilution, 5-s odor pulses
- **Source** — Lin, Bygrave, de Calignon, Lee, Miesenböck (2014) "Sparse,
  decorrelated odor coding in the mushroom body enhances learned odor
  discrimination," *Nat Neurosci* 17:559–568. https://doi.org/10.1038/nn.3660
  (open PMC copy: https://pmc.ncbi.nlm.nih.gov/articles/PMC4000970/)
- **Confidence** — high for direction and significance; the magnitude is not
  recoverable as a plain number from the text, only from figures.

### T-MB-02  APL block decreases KC population sparseness, raises inter-odor correlation

- **Quantity** — population sparseness and pairwise correlation between
  odor representations across the KC population, with vs. without APL
  (or KC recurrent) output
- **Value** — stated qualitatively in the text: "population sparseness
  decreased and inter-odor correlations increased" when APL (or the KC→APL→KC
  loop) is blocked. The paper's own figure (their Fig. 5) carries the actual
  before/after percentages; I could not extract those as text from the
  sources available to me — only the direction and that it is treated as a
  clear, reportable effect.
- **Type** — perturbation
- **Method** — same as T-MB-01 (GCaMP3, two-photon, mb247-LexA)
- **Observation model** — same shibire-ts block; sparseness computed across
  the odor panel from thresholded ΔF/F responses (2 SD criterion, see T-MB-16)
- **Conditions** — as T-MB-01
- **Source** — Lin et al. (2014), as above, Figure 5
- **Confidence** — medium. Direction and statistical significance are stated
  explicitly in the source; I do not have the exact percentages and say so
  rather than infer them. Whoever writes the extractor should pull Fig. 5
  directly from the paper (or its PMC supplementary data) for the numbers.

### T-MB-03  APL hyperactivation almost abolishes KC odor response

- **Quantity** — KC odor-evoked Ca2+ response with APL thermogenetically
  hyperactivated
- **Value** — odor-evoked Ca2+ influx in KCs "almost completely abolished"
  at the restrictive temperature; n = 9 hemispheres (5 flies), P < 0.01
  (unpaired Welch t-test)
- **Type** — perturbation
- **Method** — GCaMP3 two-photon imaging as above
- **Observation model** — UAS-dTrpA1 in APL, driven to fire at 32 °C
  (dTrpA1 is a heat-activated cation channel; this is tonic hyperactivation,
  not a controlled spike rate)
- **Conditions** — as T-MB-01
- **Source** — Lin et al. (2014), as above
- **Confidence** — high. This is the clearest causal bound on the "APL knob"
  in the whole target set: near-total suppression at one extreme, large
  disinhibition at the other (T-MB-01).

### T-MB-04  APL block selectively impairs discrimination of similar (not dissimilar) odors

- **Quantity** — learned odor discrimination performance (T-maze choice
  behavior) with APL output blocked vs. control, for a similar odor pair
  and two dissimilar odor pairs
- **Value** —
  - Similar odors (isoamyl acetate:ethyl butyrate mixed 1:4 vs. 4:1):
    control learning score comparable at 21 °C and 32 °C; APL-blocked flies
    normal at 21 °C but severely impaired at 32 °C. Interaction P = 0.0012
    (2-way ANOVA, temperature × genotype). n = 55 flies / 8 experiments
    (control), 51 flies / 9 experiments (APL-blocked). Exact learning-score
    percentages are only in Fig. 7 as bar heights; I read them as roughly
    20–25% (control/permissive) falling to roughly 5–10% (blocked,
    restrictive) but flag these two numbers as figure-estimates, not
    text-quoted values.
  - Dissimilar odors (isoamyl acetate:ethyl butyrate 4:1 vs.
    δ-decalactone): no significant effect of APL block at either
    temperature (interaction P = 0.53). n = 44/7 (control), 32/9 (blocked).
  - Dissimilar odors (3-octanol vs. 4-methylcyclohexanol): "blocking APL
    synaptic output did not significantly affect learned discrimination."
    n = 41/6 (control), 16/6 (blocked).
- **Type** — perturbation
- **Value carries N** — see above per condition
- **Method** — single-fly T-maze-style choice chambers (polycarbonate,
  50 × 5 × 1.3 mm), odor conditioning with electric shock
- **Observation model** — behavioral learning score = change in % time
  spent avoiding the shock-paired odor; UAS-shibire-ts1 in APL, 32 °C
  restrictive vs. 21 °C permissive, applied during training/testing
- **Conditions** — 1-min odor exposure during training, shock 1.25 s
  duration at 0.2 Hz repetition rate during the odor; flies 1–7 days old,
  male and female, reared 18 °C
- **Source** — Lin et al. (2014), as above, Figure 7
- **Confidence** — high for the qualitative result (similar odors need APL,
  dissimilar odors don't) — this is the paper's central behavioral claim and
  well powered. Low confidence on the two percentages I read off the figure.

### T-MB-05  APL silencing removes calyx-level normalization of KC input

- **Quantity** — KC dendritic (calyx, postsynaptic) Ca2+ response to two
  odors of different intrinsic PN-drive strength, with vs. without
  APL output
- **Value** — control (APL active): responses to the two test odors (methyl
  cyclohexanol "Mch" vs. octanol "Oct") statistically indistinguishable in
  peak amplitude across responding microglomeruli (n = 10, P = 0.949,
  two-way ANOVA; distributions "highly overlapping," P = 0.0533).
  APL silenced (tetanus toxin light chain, TNT): Oct produces a
  significantly stronger average response than in controls (n = 10,
  P = 0.0003, two-way ANOVA), response distribution skews toward higher
  values resembling the raw presynaptic PN bouton signal (Kolmogorov–Smirnov
  P < 0.0001), and a modest increase in the number of responding
  microglomeruli (P = 0.047).
- **Type** — perturbation
- **Method** — in vivo two-photon Ca2+ imaging in the calyx: APL imaged with
  GCaMP6m, KC postsynaptic sites with MB247-homer::GCaMP3, PN presynaptic
  boutons with UAS-Syp::GCaMP3. Scanning ~9 Hz (single plane), ~16 Hz
  (volumetric 3D stacks). F0 = average of the first 30 frames; reported as
  ΔF/F0% and ΔF/F0%MAX.
- **Observation model** — chronic APL silencing via APL-Gal4 > UAS-TNT
  (not an acute/temperature-gated block, unlike T-MB-01–04)
- **Conditions** — not otherwise specified beyond standard rearing in the
  accessible text
- **Source** — Prisco, Deimel, Yeliseyeva, Fiala, Tavosanis (2022) "The
  anterior paired lateral neuron normalizes odour-evoked activity in the
  Drosophila mushroom body calyx," *eLife* 11:e74172.
  https://doi.org/10.7554/eLife.74172
- **Confidence** — high. This is a direct, statistically clean
  demonstration that APL's job at the calyx is to equalize KC input across
  odors of different raw strength, not merely to subtract a constant.

### T-MB-06  APL inhibition in the lobes is spatially localized, not global

- **Quantity** — spread of APL-mediated inhibition along the mushroom body
  lobes from a local activation site
- **Value** — local APL activation (via ATP uncaging onto P2X2 receptors)
  at the vertical-lobe tip: APL's own calcium signal "decayed to an
  undetectable level by the branching point between the two lobes"
  (~100 µm away). A distance-weighted connectome model
  (w(d) = e^(−d/λ)) fit to this spread gave a best-fit space constant
  **λ = 50 µm** (25, 50, and 75 µm were tested; 50 µm fit best). Shock
  strongly activates APL in the vertical-lobe (V) region specifically, with
  significantly smaller responses elsewhere; odor activates the S region
  somewhat more than γ; activating only α′β′ KCs drives a response in only
  the α′ lobe of APL.
- **Type** — perturbation / steady-state (mixed: local activation is a
  perturbation, the spatial-response mapping is observational)
- **Method** — GCaMP6f volumetric two-photon imaging, ~5 Hz effective rate;
  local APL activation via ATP-gated P2X2 channel; local GABA application
  reproduces the same inhibitory effect
- **Observation model** — baseline = average pre-stimulus fluorescence,
  ΔF/F = (F−F0)/F0; "normalized inhibitory effect" =
  (ΔF/F_odor+stim − ΔF/F_odor-alone) / peak ΔF/F_odor-alone
- **Conditions** — odors at 10⁻² dilution, 5-s pulses; hemibrain connectome
  (v1.1) used for the anatomical/distance model
- **Source** — Amin, Apostolopoulou, Suárez-Grimalt, Vrontou, Lin (2020)
  "Localized inhibition in the Drosophila mushroom body," *eLife* 9:e56954.
  https://doi.org/10.7554/eLife.56954
- **Confidence** — high. This is the paper the project's own theory review
  already cites for "APL differentially inhibits different compartments";
  this entry gives the actual space constant and the anatomical method
  behind it.

### T-MB-07  APL inhibition in the calyx tracks a spatial gradient of active input

- **Quantity** — spatial profile of APL-mediated inhibition across calyx
  sections, relative to which PN boutons are active
- **Value** — the ratio of posterior-to-anterior calyx fluorescence was
  higher in posterior calyx sections and reduced in anterior ones,
  "reflecting the bouton distribution of the PNs activated by these two
  odours" (n = 7, P = 0.0004 for the slope, linear regression). Described
  as "a gradient that peaks at the [microglomeruli] active during a given
  stimulus and attenuates with distance" — the same qualitative spread
  limitation as T-MB-06, independently found in the calyx.
- **Type** — steady-state (spatial mapping under normal odor stimulation)
- **Method** — GCaMP6m (APL) / two-photon, ~9–16 Hz as in T-MB-05
- **Observation model** — ΔF/F0% relative to first-30-frame baseline;
  spatial ratio computed between defined calyx sub-regions
- **Conditions** — as T-MB-05
- **Source** — Prisco et al. (2022), as above
- **Confidence** — high; corroborates T-MB-06 in an independent prep
  (calyx/dendritic side vs. lobes/axonal side of APL).

### T-MB-08  An individual KC inhibits itself via APL more than it inhibits other KCs

- **Quantity** — relative strength of APL-mediated feedback inhibition a
  KC receives back onto itself (via its own KC→APL→KC loop) vs. the
  inhibition it delivers to other individual KCs
- **Value** — "each Kenyon cell inhibits itself more strongly than it
  inhibits other individual Kenyon cells." Quantified as a **median
  imbalance of ~40%** between self- and average-other-inhibition (at the
  best-fit space constant λ = 50 µm; Fig. 8K–M of the source), significantly
  different from a ratio of 1.0 (Wilcoxon test, P < 0.0001), n = 1,923 KCs
  (1,927 traced KCs in the hemibrain, minus 4 annotated as the unusual
  KCγ-s1–s4 embryonic-born types). Underlying anatomical counts: all traced
  KCs form reciprocal synapses with APL at **49.6 ± 17.9 APL→KC synapses**
  and **52.6 ± 13.4 KC→APL synapses per KC** (mean ± SD).
- **Type** — steady-state (anatomical/connectomic), supporting the
  perturbation results above
- **Method** — **not direct physiology** — this is a computational analysis
  of the hemibrain EM connectome (Janelia FlyEM/Google, v1.1). All
  APL↔KC synapses (95,678 and 101,430 of them respectively) were mapped
  onto APL's own neurite skeleton (182,631 skeleton nodes, 80.2 mm total
  length), and a distance-weighted model of feedback strength
  s(k1,k2) = Σ w(d) was built and fit against the physiological spread data
  from T-MB-06.
- **Observation model** — self-inhibition and other-inhibition are both
  *modeled* quantities (weighted sums over synapse-pair skeleton distances),
  not measured currents — the "40% imbalance" is a property of the
  connectome-plus-fitted-space-constant model, calibrated against the
  independent physiological decay measurement in T-MB-06
- **Conditions** — n/a (EM reconstruction, one hemibrain volume)
- **Source** — Amin et al. (2020), as above (T-MB-06), Figure 8 and
  Discussion/Abstract
- **Confidence** — high for the qualitative/directional claim (it is the
  paper's headline result and is what the project's own `theory-review.md`
  already quotes); medium for the exact "~40%" figure, because it is a
  model output conditioned on a fitted space constant, not a directly
  measured current ratio. This is precisely the number that motivates
  compartmentalizing APL rather than using a point-neuron implementation.

### T-MB-09  APL is non-spiking / graded, not a conventional spiking neuron

- **Quantity** — mode of electrical signaling in APL
- **Value** — APL "does not fire action potentials." Supporting evidence in
  Drosophila: voltage-gated Na⁺ and Ca²⁺ channel transcripts are expressed
  at lower levels in APL than in every other mushroom body cell type
  examined, yet APL shows "significant voltage-gated Ca²⁺ conductance"
  (via Ort channel experiments) and its calcium/depolarization response
  scales continuously with PN input strength (graded release) rather than
  behaving all-or-none.
- **Type** — steady-state (intrinsic property)
- **Method** — gene expression profiling + voltage-clamp characterization
  (Amin et al. 2020); independently, graded scaling with PN input strength
  observed by Ca2+ imaging (Prisco et al. 2022, T-MB-05/07)
- **Observation model** — n/a (this is a qualitative circuit-design fact
  the model needs to represent, not a number to threshold against — the
  practical implication is APL should not be modeled as a LIF/spiking unit)
- **Conditions** — n/a
- **Source** — Amin et al. (2020), as above; and, **by analogy from a
  different species**, Papadopoulou, Cassenaer, Nowotny, Laurent (2011)
  "Normalization for sparse encoding of odors by a wide-field interneuron,"
  *Science* 332:721–725, https://doi.org/10.1126/science.1201835 — this
  paper describes the **locust** giant GABAergic neuron (GGN), a
  functionally analogous but anatomically and genetically distinct cell in
  a different insect. Amin et al. cite it as precedent for a wide-field,
  non-spiking, graded-release normalizing interneuron design, **not** as
  direct Drosophila APL data. Keep the species distinction explicit if this
  citation is reused elsewhere in the project.
- **Confidence** — high for Drosophila APL being non-spiking/graded (this is
  now stated by multiple independent Drosophila papers); the locust citation
  is included only as design precedent, not as a Drosophila measurement.

### T-MB-10  KC→MBON synaptic depression from odor + dopamine pairing

- **Quantity** — magnitude of depression at the KC→MBON-γ1pedc synapse
  after odor is paired with activation of its dopaminergic input
  (PPL1-γ1pedc)
- **Value** — spike-rate reduction in MBON-γ1pedc to the paired odor:
  **80 ± 5.7%** (pre-pairing: 118 ± 8.3 spikes; post-pairing: 24 ± 7.4
  spikes; mean ± SEM, n = 7). Synaptic current (EPSC charge transfer)
  reduction: **90 ± 3.7%**. The unpaired control odor showed a smaller,
  non-specific decrease (pre 110 ± 11, post 83 ± 14 spikes) — i.e., the
  large effect is odor-specific, not general rundown. *Caveat: the paper
  reports these as spike/charge counts tied to a specific trial structure;
  I could not fully resolve from the accessible text whether "118 ± 8.3
  spikes" is a single-trial count or summed over a fixed pre-pairing block
  of several 1-s odor pulses — check Figure 1 of the source directly before
  treating this as a per-trial firing rate.*
  In the α2 compartment (MBON-α2sc / PPL1-α3 pathway), the same 1-s pairing
  protocol produced **no significant depression**; only a much longer 1-min
  odor + 120-pulse DAN activation protocol produced significant,
  odor-specific depression (P < 10⁻⁵) — i.e., **the timing/duration
  requirement for inducing plasticity differs by compartment.**
- **Type** — perturbation
- **Method** — in vivo whole-cell current-clamp and voltage-clamp
  electrophysiology of the MBON; separately, GCaMP6f population calcium
  imaging of KCs (showing no CS+-specific change in the KCs' own odor
  response, P = 0.58 — the plasticity is expressed post-synaptically /
  at the synapse, not as a change in KC odor coding itself, which is the
  basis for calling this "heterosynaptic")
- **Observation model** — pairing protocol (γ1pedc): 1-s odor + four 1-ms
  optogenetic light pulses at 2 Hz starting 0.2 s after odor onset (single
  pairing). Backward-pairing control (odor delivered 0.5 s *after* the
  light pulses) produced no change, showing the effect requires the correct
  temporal order. Depression persisted through the full recording session
  (≥40 min) with only slight recovery.
- **Conditions** — flies raised at room temperature, all-trans-retinal fed
  36–72 h before testing (for optogenetics), F1 females collected on day of
  eclosion; pre-pairing odor responses measured with 1-s pulses at 25-s ISI
- **Source** — Hige, Aso, Modi, Rubin, Turner (2015) "Heterosynaptic
  Plasticity Underlies Aversive Olfactory Learning in Drosophila," *Neuron*
  88:985–998. Open PMC copy:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4674068/
- **Confidence** — high for the ~80–90% depression magnitude and the
  compartment-specific timing requirement (both are the paper's central,
  well-powered results). Medium on how to convert the "spikes" numbers into
  a firing rate without checking the original figure.

### T-MB-11  Sub-second timing precision for reward/punishment valence

- **Quantity** — how precisely the relative timing of odor (CS) and
  dopaminergic reinforcement (US) must align to determine the sign
  (attractive vs. aversive) of the resulting memory
- **Value** — "shifting the relative timing of an odor and reinforcement
  by less than 1 second can switch the valence of an olfactory memory."
  Two dopamine receptors (DopR1, DopR2) couple to distinct second
  messengers and drive synaptic depression vs. potentiation depending on
  this timing.
- **Type** — perturbation (parametric manipulation of CS–US timing)
- **Method** — behavioral conditioning with precisely timed optogenetic
  DAN activation relative to odor delivery; receptor-specific genetic
  manipulation (DopR1, DopR2 mutants/rescue)
- **Observation model** — not fully resolved from what I could access —
  I found the qualitative/quantified headline claim (sub-second switch) but
  could not retrieve the exact set of tested intervals or the full
  timing-vs-valence curve; the primary text is paywalled and I only reached
  search-indexed summaries, not the full methods.
- **Conditions** — not resolved (see above)
- **Source** — Handler, Graham, Cohn, Morantte, Siliciano, Zeng, Li, Ruta
  (2019) "Distinct Dopamine Receptor Pathways Underlie the Temporal
  Sensitivity of Associative Learning," *Cell* 178:60–75.
  https://www.cell.com/cell/fulltext/S0092-8674(19)30611-7 (fetch blocked
  by the publisher for automated access; PMID 31230716 for a PMC/library
  lookup)
- **Confidence** — medium. The headline number ("<1 s") is stated
  consistently across multiple independent summaries of this paper, but I
  could not verify it against the primary text myself, and I do not have
  the supporting interval-by-interval data.

### T-MB-12  Independent corroboration: ~80% depression in the γ1 MBON compartment

- **Quantity** — same synapse/compartment as T-MB-10, measured in a
  second, independent study
- **Value** — pairing odor with optogenetic activation of γ1 dopaminergic
  neurons drove "a near 80% reduction in the odor-evoked response of the
  γ1 mushroom body output neuron, but not in the neighboring γ2 mushroom
  body output neuron" — i.e., odor-specific and compartment-specific,
  matching Hige et al.'s 80 ± 5.7% almost exactly.
- **Type** — perturbation
- **Method** — electrophysiology and presynaptically localized GCaMP,
  in a dissected-brain preparation (KC stimulation paired with DAN
  activation) and in an intact fly (odor paired with DAN activation)
- **Observation model** — not further resolved beyond the above; I worked
  from indexed summaries of the paper rather than the full text (Cell is
  paywalled and I could not fetch it directly)
- **Conditions** — not resolved
- **Source** — Cohn, Morantte, Ruta (2015) "Coordinated and Compartmentalized
  Neuromodulation Shapes Sensory Processing in Drosophila," *Cell*
  163:1742–1755.
- **Confidence** — medium-high for the ~80% figure itself (independently
  converging with T-MB-10 on the same number is a strong signal), low on
  method detail since I have only summary-level access. This convergence is
  exactly the kind of case the README asks for: two papers agreeing tightly
  is itself informative and should tighten, not loosen, this particular
  number, even though my access to either paper's raw methods is imperfect.

---

## Kenyon cell odor sparseness — the number *and* its criterion

### T-MB-13  Population sparseness: 6 ± 5% of KCs respond to a given odor (electrophysiology)

- **Quantity** — fraction of the recorded KC population that spikes in
  response to a given odor (population sparseness)
- **Value** — **6 ± 5%** (mean ± SD across odors), n = 71 KCs, 25-odor
  panel. For comparison, the same criterion applied to the KCs' direct
  inputs (projection neurons, PNs) gives 59 ± 14% (n = 37 PNs) responding
  to a given odor — PNs are far more broadly responsive.
- **Type** — steady-state
- **Method** — in vivo whole-cell patch-clamp (current clamp, Axoclamp-2B,
  bridge mode, signals filtered 3 kHz / acquired 10 kHz)
- **Observation model** — **this is the criterion the project needs**: a KC
  was counted as "responsive" to an odor if its firing rate (measured in
  successive 200-ms bins, averaged across trials) **crossed a threshold of
  3.5 SD above its own baseline firing rate at any point in the 0–2 s
  window after odor onset**, and did so on **at least half the trials**
  (typically 3 of 6). PNs used the same procedure with a slightly more
  conservative 4 SD threshold. This reliability requirement was added
  specifically because KC baseline rates are so low that a single lucky
  trial could otherwise count as a "response."
- **Conditions** — wild-type Canton-S females, 1–2 days post-eclosion;
  in vivo preparation (head capsule opened, epoxy-fixed); odors at
  effective 1:1,000 dilution (1:100 in mineral oil, further 1:10 in the
  carrier airstream), 500-ms stimulus, 22-s inter-stimulus interval,
  6 trials/odor; recording temperature not stated in the paper
- **Source** — Turner, Bazhenov, Laurent (2008) "Olfactory representations
  by Drosophila mushroom body neurons," *J Neurophysiol* 99:734–746.
  https://doi.org/10.1152/jn.01283.2007
- **Confidence** — high. This is a direct measurement with a fully
  specified, reproducible criterion — exactly the kind of number the
  project's extractor should be built to replicate (bin the simulated
  spike train the same way, threshold at 3.5 SD over baseline in a 0–2 s
  post-odor window, require ≥half of repeated trials). It is **not** the
  same criterion as "firing rate above 1 Hz," and it does not need to be:
  the 3.5 SD criterion is self-normalizing to each simulated cell's own
  baseline noise, the same way it is to each recorded cell's baseline.
  For context (not a target in its own right): the identical criterion
  applied to locust KCs by tetrode recording gives 11% responding
  (Perez-Orive et al. 2002, cited in this paper) — a different species,
  included only to show the method transfers and gives a comparable
  order of magnitude.

### T-MB-14  Lifetime sparseness: 6 ± 12% of odors evoke a response in a given KC

- **Quantity** — fraction of a fixed odor panel that drives a spiking
  response in a given KC (tuning width / lifetime sparseness — the
  complementary measure to T-MB-13's population sparseness)
- **Value** — **6 ± 12%** of odors evoke a response in a given KC (each KC
  tested with 10 odors on average, range 6–14). PNs, by contrast: 53 ± 39%
  of odors evoke a response.
- **Type** — steady-state
- **Method / Observation model** — identical recording and 3.5 SD/0–2 s/
  ≥half-of-trials criterion as T-MB-13, just tabulated per-cell-across-odors
  instead of per-odor-across-cells
- **Conditions** — as T-MB-13
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high, same basis as T-MB-13. Numerically the two
  sparseness measures come out nearly identical here (~6%), but they are
  conceptually distinct and an extractor should compute both rather than
  assume they must match.

### T-MB-15  KC subtype differences in responsiveness

- **Quantity** — odor responsiveness broken down by anatomical KC class
  (γ, α′β′, αβ)
- **Value** — α′β′ KCs are significantly more broadly tuned than the other
  two classes (P < 0.05, one-way ANOVA) and have the highest baseline
  firing rate and most vigorous odor responses: **4.9 ± 3.0 spikes**
  during an odor response, vs. **2.2 ± 1.2 spikes** for αβ KCs (P = 0.007,
  t-test). γ KCs are the least responsive by a wide margin: only 1 of 15
  γ KCs tested with the main odor panel (and only 1 of 23 γ KCs recorded
  across all odor concentrations tested in the study) produced any spiking
  response at all, although all γ KCs showed clear subthreshold synaptic
  responses.
- **Type** — steady-state
- **Method / Observation model** — same as T-MB-13
- **Conditions** — as T-MB-13
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high for the ordering (α′β′ > αβ > γ) and the αβ vs.
  α′β′ spike-count comparison; the γ-KC numbers rest on a small sample
  (15–23 cells, 1 responder) so treat the γ "almost never spikes" claim as
  qualitatively solid but not a precise rate.

### T-MB-16  Calcium-imaging sparseness estimate (~5–10%) and its pixel-level criterion

- **Quantity** — population sparseness as measured by calcium imaging
  (rather than electrophysiology), and the exact per-pixel/per-cell
  responsiveness criterion used
- **Value** — "only ~5–10% of Kenyon cells respond to any given odor"
  under control conditions. **This specific figure is stated by Lin et al.
  (2014) as background, citing the imaging literature (Honegger, Campbell &
  Turner 2011 and related work) rather than as a number newly measured with
  its own N in this paper** — flag it as a converging estimate, not an
  independent replication.
- **Type** — steady-state
- **Method** — two-photon imaging, GCaMP3, 910 nm excitation, frame time
  interpolated to 0.09 s (~11 Hz effective sampling)
- **Observation model** — **exact pixel-level criterion, quoted directly**:
  "If ΔF/F of a pixel was less than twice the standard deviation (σ) of the
  intensity of that pixel during the pre-stimulus interval, the pixel was
  considered unresponsive." Baseline = average fluorescence over the
  pre-stimulus interval. Odors delivered at 10⁻² dilution as 5-s pulses.
  Separately, Campbell et al. (2013) — the follow-up imaging paper in the
  same lineage (Honegger/Campbell/Turner 2011) — computed response
  amplitude as the mean ΔF/F in a **0.5–4.5 s window after stimulus
  onset**, i.e., a fixed post-onset integration window rather than a
  per-trial peak.
- **Conditions** — as T-MB-01 (same lab/prep lineage)
- **Source** — Lin, Bygrave, de Calignon, Lee, Miesenböck (2014), as above,
  for the ~5–10% figure and the 2 SD pixel criterion; Campbell, Honegger,
  Qin, Li, Demir, Turner (2013) "Imaging a Population Code for Odor
  Identity in the Drosophila Mushroom Body," *J Neurosci* 33:10568–10581,
  https://www.jneurosci.org/content/33/25/10568, for the 0.5–4.5 s
  integration window; Honegger, Campbell, Turner (2011) "Cellular-Resolution
  Population Imaging Reveals Robust Sparse Coding in the Drosophila
  Mushroom Body," *J Neurosci* 31:11772–11785,
  https://www.jneurosci.org/content/31/33/11772, is the original source of
  the imaging-based sparseness estimate but I could not extract its own
  exact percentage/N/threshold text directly (fetch attempts returned
  navigation/paywall content, not the article body) — **this is a gap**:
  the 2011 paper is the one that should be read directly (or via its PMC
  copy, if one exists) for the primary imaging number and criterion, rather
  than relying on how later papers cite it.
- **Confidence** — medium. The ~5–10% figure is widely repeated and
  consistent with the independent electrophysiological 6±5% in T-MB-13
  (good agreement across modalities), but I do not have it pinned to a
  single paper's own N and full statistics the way T-MB-13 is pinned. The
  2 SD pixel criterion and the 0.5–4.5 s window are each solidly sourced to
  a specific paper, just not the same paper as the percentage.

### T-MB-17  Two sparseness criteria disagree in absolute magnitude only mildly — set a loose, not tight, tolerance

- **Quantity** — meta-note on T-MB-13 vs. T-MB-16
- **Value** — electrophysiology (3.5 SD firing-rate threshold, 0–2 s
  window): 6 ± 5%. Calcium imaging (2 SD pixel ΔF/F threshold, 5 s odor
  pulse, various integration windows across papers): commonly cited as
  ~5–10%. These agree reasonably well in magnitude but use **different
  thresholds, different time windows, and different underlying signals**
  (spikes vs. ΔF/F), so agreement in the headline percentage does not mean
  the criteria are interchangeable.
- **Type** — steady-state (methodological note)
- **Method / Observation model** — n/a — this entry exists to record that
  the project should **not** average T-MB-13 and T-MB-16 into one number.
  Fit against whichever one matches the extractor's own observation model:
  if the simulator's readout is an instantaneous firing rate, use T-MB-13's
  criterion; if the readout is convolved into a calcium-like signal, use
  T-MB-16's.
- **Conditions** — n/a
- **Source** — synthesis of T-MB-13 and T-MB-16
- **Confidence** — high that both numbers are individually real; the
  "5–10%" imaging figure specifically should be given a loose tolerance
  since (per T-MB-16) it is itself a citation chain rather than one paper's
  direct result.

---

## Kenyon cell physiology

### T-MB-18  Resting/holding membrane potential

- **Quantity** — KC membrane potential at rest (no current injection, no
  odor)
- **Value** — **−58 ± 2 mV (SD)**, reported for the general recorded
  population; separately, **−57.8 mV** average holding potential for the
  n = 17 subsample used to compute spike threshold (T-MB-21). Treat these as
  the same underlying quantity from the same paper via two slightly
  different subsamples/sentences, not two independent measurements.
- **Type** — steady-state
- **Method** — in vivo whole-cell patch-clamp, current clamp
- **Observation model** — measured with no current injection ("held at")
  — note the paper's own phrasing ("held at") leaves some ambiguity about
  whether small holding current was used to standardize across cells versus
  this being purely passive rest; treat as "resting potential" with that
  caveat
- **Conditions** — Canton-S females, 1–2 days post-eclosion, in vivo,
  temperature not stated
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high.

### T-MB-19  Input resistance: >10 GΩ (lower bound only)

- **Quantity** — KC somatic input resistance
- **Value** — **>10 GΩ** at the soma. Reported only as a threshold/lower
  bound ("input resistance at the soma was >10 GΩ") — no mean ± SD is given
  anywhere in the paper.
- **Type** — steady-state
- **Method** — whole-cell patch-clamp, small-tip (<0.5 µm) low-resistance
  pipettes
- **Observation model** — n/a
- **Conditions** — as T-MB-18
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high that it exceeds 10 GΩ (stated plainly, twice, in
  the paper); no confidence possible on how far above 10 GΩ it actually is.
  This is an unusually high input resistance (consistent with KCs' very
  small soma size) and matters a great deal for how much current a single
  synaptic event can deliver.

### T-MB-20  Membrane time constant: >200 ms (lower bound only)

- **Quantity** — KC passive membrane time constant
- **Value** — **>200 ms**, measured at the soma via hyperpolarizing
  current injection. Again reported only as a lower bound, no mean ± SD.
- **Type** — steady-state
- **Method** — whole-cell patch-clamp, hyperpolarizing current steps
- **Observation model** — n/a
- **Conditions** — as T-MB-18
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high for the qualitative "very long" / >200 ms claim;
  no precise value available. Note this is unusually long relative to the
  fast (~2 ms rise, ~11.5 ms decay) EPSPs the same cells receive (T-MB-25) —
  the paper uses exactly this mismatch to argue that KCs integrate inputs
  over a much shorter effective window than their own membrane time
  constant would suggest, because of how electrotonically compact/leaky
  the dendrite is relative to the soma recording site.

### T-MB-21  Spike threshold: −36.3 mV (model value fit to the physiology)

- **Quantity** — KC spike threshold, as a membrane voltage
- **Value** — the gap between resting potential and spike threshold was
  **21.5 ± 5.6 mV** (n = 17 KCs), measured as the peak of the second time
  derivative of the membrane potential trace on odor responses containing
  four or fewer action potentials. Combined with the −57.8 mV average
  holding potential for that subsample, the paper sets **Vth = −36.3 mV**
  for use in its own companion conductance-based model. This is the
  authors' own back-calculated model value, not a separately, independently
  stated absolute threshold voltage — but it is the number they judged
  matched their own data and used for simulation.
- **Type** — steady-state
- **Method** — whole-cell patch-clamp; threshold detection via second
  derivative of Vm
- **Observation model** — n/a
- **Conditions** — as T-MB-18, n = 17 KCs for the 21.5 ± 5.6 mV figure
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high for the 21.5 ± 5.6 mV rest-to-threshold gap (direct
  measurement); medium for treating −36.3 mV as a universal absolute
  threshold, since it is derived by adding that gap to a separately
  averaged holding potential rather than measured as an absolute voltage
  per cell.

### T-MB-22  Spike amplitude: <15 mV at the soma

- **Quantity** — KC action potential amplitude as recorded at the soma
- **Value** — **typically <15 mV**, in every KC recorded, evoked by
  depolarizing current injection; effectively blocked by 1 µM TTX,
  confirming a sodium-channel origin. No spike width/duration value is
  given anywhere in the paper.
- **Type** — steady-state
- **Method** — whole-cell patch-clamp with current injection; TTX
  pharmacology
- **Observation model** — n/a
- **Conditions** — as T-MB-18
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high. The small somatic amplitude is expected given
  KCs' very high input resistance and small soma, with spikes likely
  initiating some electrotonic distance away and attenuating by the time
  they reach the recording site.

### T-MB-23  Spontaneous firing rate: 0.1 ± 0.4 Hz, most cells effectively silent

- **Quantity** — KC baseline (odor-absent) spiking rate
- **Value** — **0.1 ± 0.4 spikes/s** (mean ± SD, n = 71 KCs). **14 of the
  71 KCs fired zero spontaneous action potentials during the entire
  recording session** (all could still be driven to spike by current
  injection, so this is not a recording-quality artifact). Despite this,
  KCs receive frequent subthreshold synaptic bombardment: spontaneous EPSP
  rate 32.6 ± 12.7 s⁻¹ (n = 27 KCs) — abundant depolarizing input that
  essentially never crosses spike threshold at rest.
- **Type** — steady-state
- **Method** — in vivo whole-cell current-clamp, spikes identified by
  amplitude/sharpness via a custom time-derivative algorithm
- **Observation model** — spontaneous rate computed over the full
  inter-trial recording period, excluding odor-response windows
- **Conditions** — as T-MB-18
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high. A second, independent paper from the same lab
  (Gruntman & Turner 2013) states only qualitatively that "most cells had
  a baseline rate of zero" without its own Hz figure — consistent in
  direction, not an independent quantitative check.

### T-MB-24  Spontaneous calcium transients: 10–20/hour — cultured pupal KCs, NOT adult in vivo

- **Quantity** — rate of spontaneous calcium transients, in the specific
  unit the project asked to preserve (events/hour rather than Hz)
- **Value** — **10–20 transients/hour**, described as "a frequency similar
  to calcium oscillations in vivo." **Important caveat: this measurement is
  from dissociated Kenyon cells cultured from late-stage Drosophila pupae —
  not intact adult flies, not in vivo.** The paper's own "in vivo" point of
  comparison is a citation to older population-level work, not an
  independent re-measurement in the same paper. Also note: these transients
  are "not unique to Kenyon cells" — they occur in ~60% of all cultured
  central-brain neurons in the same prep, so this may not be a
  KC-specific phenomenon at all.
- **Type** — steady-state
- **Method** — Fura-2 ratiometric calcium imaging, dissociated primary
  cell culture from late pupal stage
- **Observation model** — transient = a detected Fura-2 ratio event;
  exact per-event amplitude/duration threshold not resolved from the
  accessible text
- **Conditions** — cultured, dissociated, pupal — explicitly **not** the
  adult intact-brain condition this project models
- **Source** — Jiang, Campusano, Su, O'Dowd (2005) "Drosophila mushroom
  body Kenyon cells generate spontaneous calcium transients mediated by
  PLTX-sensitive calcium channels," *J Neurophysiol* 94:491–500.
  https://doi.org/10.1152/jn.00096.2005
- **Related cross-check (different technique, ex vivo adult, not cultured)**
  — Rosay, Armstrong, Wang, Kaiser (2001) "Synchronized neural activity in
  the Drosophila memory centers and its modulation by amnesiac," *Neuron*
  30:759–770, found KCs in **dissected adult** brains show synchronous
  intracellular calcium oscillation with a **mean period of ~4 minutes**
  (bioluminescent apoaequorin reporter, not a fluorescent Ca²⁺ dye),
  persisting for hours in saline. A ~4-min period is arithmetically
  ~15 cycles/hour — in the same range as the cultured-pupal 10–20/h figure
  above, but from a different technique, a different (ex vivo adult, not
  cultured) prep, and a population-synchrony measure rather than a
  single-cell event rate. I have deliberately not treated these as the same
  measurement, only as loosely consistent.
- **Confidence** — low-to-medium, and explicitly **not** a validated adult
  in vivo number. **Gap**: I could not find any modern (GCaMP-era,
  intact/awake adult fly) paper reporting KC spontaneous activity in
  per-hour or per-minute units. If this unit is important for fitting,
  it needs a dedicated literature search beyond what I could do here —
  the two sources above are both from 2001–2005 and neither is the
  in vivo adult measurement the project likely wants.

### T-MB-25  Spontaneous synaptic input rate (EPSPs)

- **Quantity** — rate and amplitude of spontaneous excitatory synaptic
  events onto KCs
- **Value** — spontaneous EPSP rate **32.6 ± 12.7 s⁻¹** (n = 27 KCs);
  after blocking spiking with 1 µM TTX (isolating "mini" EPSPs, i.e.
  spontaneous vesicle release), rate drops to **1.8 ± 1.3 s⁻¹** (n = 8 KCs,
  same subsample's control rate was 19.8 ± 13.2 s⁻¹) — i.e., ~90% of
  spontaneous EPSPs are spike-driven (network activity in upstream PNs),
  not pure minis. Mean EPSP amplitude 1.4 ± 0.8 mV (control) vs. 1.0 ± 0.5
  mV (TTX/mini) mV. EPSP kinetics: 10–90% rise time 2.1 ± 0.5 ms, decay
  time constant 11.5 ± 5.3 ms (49–50 well-isolated EPSPs, 7 different KC
  recordings). For comparison, spontaneous PN spike rate was 4.6 ± 4.2 s⁻¹
  (n = 37 PNs).
- **Type** — steady-state
- **Method** — whole-cell current-clamp (EPSPs) and voltage-clamp (EPSCs,
  held at −60 mV), event detection via time-derivative peak-finding
- **Observation model** — n/a (this is a synaptic-input characterization,
  not a spiking criterion)
- **Conditions** — as T-MB-18
- **Source** — Turner, Bazhenov, Laurent (2008), as above
- **Confidence** — high.

### T-MB-26  PN→KC convergence: anatomical consensus ~6–7, vs. a physiological estimate of ~10 — conflict, use a loose tolerance

- **Quantity** — number of distinct projection neurons (equivalently,
  number of dendritic claws) each KC samples from
- **Value** — **anatomical/connectomic counts cluster around 6–7 and
  agree reasonably well with each other:**
  - Caron, Ruta, Abbott, Axel (2013): single-KC dye-fill/photoactivation,
    claws per KC range **2–11, average = 7** (n = 200 KCs, main olfactory
    calyx only). Of 200 KCs, only 11 receive two inputs from the same
    glomerulus and none receive three or more (i.e., repeat sampling of one
    glomerulus is rare) — 654 of 683 identified inputs connect to PNs
    covering 49 of 51 antennal-lobe glomeruli.
  - Gruntman & Turner (2013): "KCs typically have 5 to 7 claws" (citing
    prior anatomy); their own two-photon dendritic imaging gives **7 claws
    on average** (n = 34 KCs, sample biased toward α′β′ by design); a
    separate dye-fill/optogenetic dataset found cells connected via 1–5
    claws (distribution: 17, 14, 6, 2 KCs for 1/2/3/5 claws respectively,
    out of 39 adequately filled cells).
  - Li et al. (2020), hemibrain EM connectome: **5.6 claws/KC** overall
    mean (stated in Results text), vs. "six" given as a rounded figure in
    the paper's own schematic legend. By KC subtype (reported in the paper
    as "boutons per KC," which given 1:1 claw:bouton wrapping should
    track claw count, but note the paper's own wording): **KCα′/β′ 4.40 ±
    1.58, KCαβ 4.67 ± 1.78, KCγ 8.49 ± 2.17** — γ KCs have roughly double
    the claws of the other two classes. Note also an active dispute in the
    literature the paper itself flags: a re-analysis of a different EM
    dataset (FAFB, Zheng et al. 2020) found PN→KC convergence
    "inconsistent with random sampling," contradicting the randomness
    conclusion of Caron (2013) and Eichler (2017).
  - **In contrast, Turner, Bazhenov, Laurent (2008) — a physiological,
    model-based estimate, not a direct anatomical count — states "~10 PNs
    per KC on average"** in its own abstract.
- **Type** — steady-state
- **Method** — anatomical: single-cell dye/photoactivation fills (Caron
  2013), two-photon dendritic imaging + optogenetic dye-fill (Gruntman &
  Turner 2013), dense EM reconstruction (Li et al. 2020, hemibrain).
  Physiological: indirect estimation from response statistics (Turner et
  al. 2008).
- **Observation model** — n/a (structural/connectivity parameter — this
  project already has ground-truth connectivity from its own connectome
  import, so this target is best used as a sanity check on that import
  rather than something to fit)
- **Conditions** — adult flies throughout (see individual sources for
  sex/age); larval connectome numbers exist (Eichler et al. 2017,
  *Nature* 548:175–182) but are not comparable to this adult-modeling
  project and are noted here only to rule them out: larval KCs are
  categorized as single-claw (17–19 of ~72–73 mature KCs per hemisphere)
  vs. multi-claw (2–6 PN inputs), with claw number correlating with
  developmental birth order — a larva-specific phenomenon.
- **Source** — Caron, Ruta, Abbott, Axel (2013) "Random convergence of
  olfactory inputs in the Drosophila mushroom body," *Nature* 497:113–117,
  https://doi.org/10.1038/nature12063 (PMC4148081); Gruntman & Turner
  (2013), as cited under T-MB-27; Li et al. (2020), as cited under T-MB-32;
  Turner, Bazhenov, Laurent (2008), as above.
- **Confidence** — medium-to-high for the ~6–7 anatomical consensus (three
  independent methods agree); the conflict with Turner 2008's "~10" is
  real and unresolved in what I could access — **give this target a loose
  tolerance (roughly 5–10) rather than pinning to any single number**,
  and prefer the anatomical figures (6–7) if the model needs one specific
  value, since they come from three independent direct-counting methods
  against one indirect estimate.

### T-MB-27  Single-claw response criteria (calcium and spiking)

- **Quantity** — responsiveness criteria used at the individual-claw /
  single-PN-input level (finer grain than whole-cell sparseness)
- **Value** — for ratiometric calcium imaging of individual dendritic
  claws: responsive if **ΔG/R exceeded 2 SD above baseline**. For somatic
  spiking responses to single-claw optogenetic PN activation: a "reliable"
  response was defined as **>0.5 spikes/trial**. Claws integrate close to
  linearly for two connected claws (response ≈ 2× single-claw response),
  trending sublinear for three or more claws, most pronounced for
  five-claw KCs.
- **Type** — steady-state
- **Method** — whole-cell patch-clamp with intracellular dye fill (Alexa
  Fluor 568 hydrazide), optogenetic (ChR2) activation of single identified
  PN boutons/claws, light pulses of 1–250 ms
- **Observation model** — as stated (2 SD for imaging; >0.5 spikes/trial
  for spiking reliability)
- **Conditions** — 2–5 day old females (imaging), 4–7 day old females
  (ChR2 experiments), reared/fed at 25 °C
- **Source** — Gruntman, Turner (2013) "Integration of the olfactory code
  across dendritic claws of single mushroom body neurons," *Nat Neurosci*
  16:1821–1829. https://doi.org/10.1038/nn.3547 (PMC3908930)
- **Confidence** — high for the criteria as stated; this paper does not
  report resting potential, input resistance, or an absolute spike
  threshold voltage (checked directly — not just absent from what I could
  fetch).

---

## MBON and dopaminergic neurons

### T-MB-28  MBON-α3 passive membrane properties and spontaneous firing rate

- **Quantity** — resting potential, membrane resistance, and spontaneous
  firing rate of an identified MBON
- **Value** — resting membrane potential **−56.7 ± 2.0 mV** (n = 5 cells);
  membrane resistance **926 ± 55 MΩ**; spontaneous firing rate **12.1 Hz**
  (average).
- **Type** — steady-state
- **Method** — ex vivo whole-cell patch-clamp electrophysiology, combined
  with EM-derived synaptic connectivity for the same identified neuron
- **Observation model** — n/a
- **Conditions** — ex vivo, room temperature, series resistance kept below
  90 MΩ, up to 35% compensation
- **Source** — Hafez, Escribano, Ziegler, Hirtz, Niebur, Pielage (2023)
  "The cellular architecture of memory modules in Drosophila supports
  stochastic input integration," *eLife* 12:e77578.
  https://doi.org/10.7554/eLife.77578
- **Confidence** — high for a single identified MBON type; this is the
  clearest direct MBON electrophysiology found for this survey and should
  not be generalized to all ~21 MBON types without more sources — see
  T-MB-30 for the gap on that point.

### T-MB-29  MBON-α3 Kenyon cell convergence

- **Quantity** — number of presynaptic KCs and total synapse count onto a
  single identified MBON
- **Value** — **948 presynaptic KCs**, **12,770 total synapses**, average
  **13.47 synapses per KC** onto MBON-α3.
- **Type** — steady-state
- **Method** — EM connectome reconstruction (hemibrain) combined with the
  same patch-clamp study as T-MB-28
- **Observation model** — n/a (structural — cross-check against this
  project's own connectome import for the same MBON identity)
- **Conditions** — n/a (EM reconstruction)
- **Source** — Hafez et al. (2023), as above
- **Confidence** — high.

### T-MB-30  MBONs are broadly tuned to odor (unlike sparse KC coding) — but the quantitative electrophysiology remains a gap

- **Quantity** — breadth of odor tuning across the MBON population, and
  whether baseline/evoked firing rates are available per MBON type
- **Value** — "any given odor results in a response in most MBONs,
  although the magnitude of the response varies among MBON cell types" —
  stated in the 2014 anatomical/behavioral paper as a citation to
  then-unpublished data ("Hige et al., unpublished") that became Hige et
  al. (2015) (T-MB-10). I checked Aso et al. (2014) directly and confirmed
  it contains **no quantitative baseline firing rates, evoked-response
  magnitudes, or response latencies for any MBON type** — it is a circuit
  architecture / optogenetic behavior paper (21 MBON types and 20 DAN types
  are anatomically defined there), not an electrophysiology paper.
- **Type** — steady-state
- **Method** — n/a (qualitative claim only, from anatomy/behavior paper)
- **Observation model** — not available
- **Conditions** — not available
- **Source** — Aso, Sitaraman, Ichinose, et al., Rubin (2014) "The neuronal
  architecture of the mushroom body provides a logic for associative
  learning," *eLife* 3:e04577 (this is the correct article — note it is a
  companion paper to, and easily confused with, Aso et al.'s "Mushroom
  body output neurons encode valence..." eLife 3:e04580, which is about
  behavior/optogenetics, not baseline physiology either)
- **Confidence** — high that the qualitative "MBONs are broadly tuned"
  claim is correct and widely accepted. **Explicit gap**: despite
  searching Aso et al. (2014), Aso & Rubin (2016), and Ichinose et al.
  (2015) directly, I found **no paper reporting baseline/spontaneous
  firing rates in Hz for PPL1 or PAM dopaminergic neurons**, and no
  systematic per-MBON-type baseline firing rate table beyond the single
  MBON-α3 result in T-MB-28. If these numbers exist in the literature I
  was not able to locate them — this should be treated as an open gap
  rather than filled with an inferred number.

### T-MB-31  Compartment-specific "memory-writing" dose differs sharply between DAN types

- **Quantity** — number of training repetitions needed for a single DAN
  type to write a 24-hour memory
- **Value** — PAM-α1 can induce a 24-hour memory with a **single 1-minute**
  training session; PPL1-α3 requires **10 repetitions** of the same
  training to induce a 24-hour memory. Separately, PAM-α1 can write a new
  memory without erasing an existing one, whereas PPL1-γ1pedc activation
  extinguishes an existing memory when writing a new one.
- **Type** — perturbation (differential training-dose requirement,
  revealed by cell-type-specific optogenetic activation)
- **Method** — optogenetic activation (CsChrimson) of specific DAN types
  during odor presentation, paired with behavioral memory assays
- **Observation model** — light protocol as reported elsewhere for this
  lab's optogenetic activation (e.g., 1-s red light pulses); exact
  shock-equivalent parameters for this specific comparison not fully
  resolved from what I could access
- **Conditions** — not fully resolved
- **Source** — Aso, Rubin (2016) "Dopaminergic neurons write and update
  memories with cell-type-specific rules," *eLife* 5:e16135.
  https://doi.org/10.7554/eLife.16135
- **Confidence** — high for the qualitative 1-repetition vs. 10-repetition
  contrast (directly checked against the paper); this paper otherwise
  reports **behavioral** memory phenotypes, not baseline DAN
  electrophysiology — confirmed directly, it does not contain spontaneous
  firing rates or odor/shock-evoked response magnitudes for PPL1 or PAM
  neurons (reinforcing the gap noted in T-MB-30).

### T-MB-32  Adult mushroom body connectome: cell-type counts

- **Quantity** — number of identified KC, MBON, and DAN cell types and
  total cell counts in the adult mushroom body
- **Value** — **1,927 Kenyon cells** in one hemisphere (1,664 olfactory-only
  + 102 olfactory+thermo/hygrosensory + 161 olfactory+visual); **23 MBON
  types** (20 conventional + 3 reclassified as atypical); **21 dopaminergic
  neuron types (6 PPL1 + 15 PAM)**. APL provides **9.5%** of the inputs to
  KCs in the main calyx (synapse-count based; no absolute APL↔KC synapse
  totals given in this specific paper — see T-MB-08 for those, from a
  different paper using the same hemibrain dataset).
- **Type** — steady-state (connectomic)
- **Method** — dense EM reconstruction, hemibrain dataset, single adult
  female, right hemisphere
- **Observation model** — n/a (structural — useful as a cross-check
  against this project's own MaleCNS-derived counts, which will not be
  identical since it is a different connectome/individual; the project's
  own theory review already notes KC number varies roughly two-fold
  between individuals/datasets)
- **Conditions** — n/a
- **Source** — Li, Lin, et al., Aso, Rubin (2020) "The connectome of the
  adult Drosophila mushroom body provides insights into function," *eLife*
  9:e62576. https://doi.org/10.7554/eLife.62576
- **Confidence** — high for the cell-type counts (this is a primary EM
  connectome paper); note this is the hemibrain dataset, a different
  reconstruction from the MaleCNS dataset this project uses, so exact
  counts should not be expected to match one-for-one.

---

## Summary of explicit gaps (things I could not find, not things I inferred)

- **PPL1 and PAM baseline/spontaneous firing rates in Hz** — searched
  extensively (Aso et al. 2014, Aso & Rubin 2016, Ichinose et al. 2015,
  Cohn et al. 2015 summaries) and did not find a directly reported number
  for either cluster. T-MB-28 gives one MBON's rate (12.1 Hz) but nothing
  equivalent was found for any DAN type.
- **The exact pre/post population-sparseness percentages behind T-MB-02**
  (Lin et al. 2014, Figure 5) — the qualitative direction and significance
  are stated in text; the numbers themselves are only in the figure and I
  could not extract them from what I fetched.
- **Honegger, Campbell & Turner (2011) full text** — this is arguably the
  primary imaging-based sparseness paper, and I was only able to source its
  headline number and threshold indirectly, through how later papers
  (Lin 2014, Campbell 2013) cite it. It should be read directly before the
  ~5–10% figure in T-MB-16 is treated as pinned down the way T-MB-13 is.
- **A modern (GCaMP, intact awake adult fly) measurement of KC spontaneous
  activity in per-hour or per-minute units** — the only two sources found
  (T-MB-24) are a 2005 cultured-pupal-cell paper and a 2001 dissected-brain
  bioluminescence paper. Neither is the adult-in-vivo measurement this
  project would ideally want for that specific unit.
- **Handler et al. (2019) full methods** — Cell's paywall blocked direct
  access; T-MB-11's "<1 second" headline claim is corroborated by multiple
  independent summaries but I could not verify it against primary text or
  recover the full timing-vs-valence dataset.
- **Butcher, Friedrich, Lu, Tanimoto, Meinertzhagen (2012)** — this paper
  is about the **adult** calyx (not larval, correcting an assumption in
  how this survey was scoped), but it is not open access and I could only
  reach its abstract, which does not itself state a claws-per-KC number.
