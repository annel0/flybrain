# Shiu, Sterne et al. 2024 — perturbation predictions

Source paper: Shiu, P. K., Sterne, G. R. et al. "A *Drosophila* computational brain
model reveals sensorimotor processing." *Nature* **634**, 210–219 (2024).
DOI: [10.1038/s41586-024-07763-9](https://doi.org/10.1038/s41586-024-07763-9).
Open access (CC BY 4.0).

This file covers only this paper's perturbation predictions, per the project's
priority rule that perturbations outrank steady-state numbers. It does not
attempt the rest of the MaleCNS/FlyWire fitting-target space.

## Sources consulted (all fetched and read in full for this file)

- Nature article (13-page PDF, main text + Methods + Extended Data):
  <https://www.nature.com/articles/s41586-024-07763-9> — fetched via the
  Oxford ORA mirror below, since nature.com itself redirects to a login wall
  for automated fetches.
- bioRxiv preprint (earlier version, title differs: "A leaky integrate-and-fire
  computational model based on the connectome of the entire adult *Drosophila*
  brain reveals insights into sensorimotor processing"):
  <https://www.biorxiv.org/content/10.1101/2023.05.02.539144> (not re-extracted
  separately — the published Nature version supersedes it and is what the
  164-prediction / 91% figure comes from; bioRxiv returned HTTP 429 on the
  automated fetch and was not retried since the Nature text was already in
  hand).
- Oxford University Research Archive record (open PDFs of the final article
  and its Reporting Summary):
  <https://ora.ox.ac.uk/objects/uuid:9422e222-dc23-4182-b183-19b92505a7db>
- **Supplementary Information workbook** — the primary source for everything
  concrete in this file — fetched directly from Springer's static content
  server (open access, no login needed):
  <https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07763-9/MediaObjects/41586_2024_7763_MOESM2_ESM.xlsx>
  This is a 27-sheet Excel workbook containing Supplementary Tables 1–12. The
  "Table legends" sheet is a text box (not cells) giving one-paragraph
  descriptions of each table; all data sheets were read directly with
  `openpyxl`.
- Reporting Summary PDF (methods checklist only, no prediction data):
  <https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07763-9/MediaObjects/41586_2024_7763_MOESM1_ESM.pdf>
- Author code repository:
  <https://github.com/philshiu/Drosophila_brain_model> — specifically
  [`model.py`](https://github.com/philshiu/Drosophila_brain_model/blob/main/model.py)
  (the Brian2 model and simulation protocol),
  [`figures.ipynb`](https://github.com/philshiu/Drosophila_brain_model/blob/main/figures.ipynb)
  (the exact FlyWire ID lists and frequencies used for every figure),
  [`utils.py`](https://github.com/philshiu/Drosophila_brain_model/blob/main/utils.py),
  and
  [`sez_neurons.pickle`](https://github.com/philshiu/Drosophila_brain_model/blob/main/sez_neurons.pickle)
  (name → FlyWire-ID-list mapping for the 106 split-GAL4 cell types in the
  unbiased SEZ screen — unpickled directly to recover the IDs below).
- Raw per-run spike-time archive (not downloaded — see "What we did not
  extract" below): Edmond (Max Planck Digital Library),
  DOI [10.17617/3.CZODIW](https://doi.org/10.17617/3.CZODIW), also reachable at
  <https://edmond.mpdl.mpg.de/dataset.xhtml?persistentId=doi:10.17617/3.CZODIW>.

## General protocol (applies to every T-SHIU target below unless noted)

**Computational side** — leaky integrate-and-fire model, Brian2, over the
FlyWire adult female central-brain connectome (public materialization v630,
127,400 proofread neurons, ~50M synapses):

- `dv/dt = (g − (v − v_rest)) / t_mbr`, `dg/dt = −g/tau`; spike when `v > v_th`,
  then `v → v_rst`, refractory period `t_rfc`.
- `v_rest = v_rst = −52 mV`, `v_th = −45 mV`, `t_mbr = 20 ms`, `tau = 5 ms`
  (synaptic/conductance decay), `t_rfc = 2.2 ms`, `t_dly = 1.8 ms`
  (spike-to-postsynaptic-effect delay).
- Synaptic weight `w_syn = 0.275 mV` per synapse — **the model's single free
  parameter**, multiplied by the connectome's synapse count and by neuro­
  transmitter sign (+1 excitatory ACh/DA/OA/5-HT, −1 inhibitory GABA/Glut,
  predicted per-neuron from Eckstein et al. 2024, cleft-score cutoff 50, a
  neuron is called inhibitory if >50% of its presynaptic sites are
  GABA/Glut).
- Manipulated ("activated") neurons receive **Poisson-distributed spike
  input** via `PoissonInput`, target rate `r_poi` (varies by experiment,
  paper's default/reference rate is 150 Hz — matches this project's stated
  protocol), scaled by `f_poi = 250` (`weight = w_syn × f_poi`); the
  refractory period of activated neurons is set to 0 ms. A second,
  independently-set-rate class `r_poi2` exists for two-population
  co-activation experiments (e.g. sugar + bitter).
  Reference: [`model.py`](https://github.com/philshiu/Drosophila_brain_model/blob/main/model.py),
  function `poi()`.
- "Silencing" a neuron = setting the weights of **all** its outgoing synapses
  to 0 mV (function `silence()` in `model.py`) — a lesion of transmission,
  not a change to its own excitability.
- Every experiment: **30 independent runs (`n_run = 30`) of 1000 ms
  (`t_run`) each**, wall-clock ≈5 min/trial/CPU thread; reported "firing
  rate" = spikes in the 1000 ms window, mean and s.d. across the 30 runs.
- `w_syn` was hand-tuned so that unilateral sugar-GRN activation at 100 Hz
  produces ≈80% of the maximal MN9 firing rate (citing Dahanukar et al. 2007
  and Inagaki et al. 2012 for the target saturation level) — this is the
  **calibration criterion for the model's only free parameter** and is
  itself one of the most important numbers in this file (T-SHIU-2).
- Housekeeping note that matters for ID lookups: the FlyWire/FAFB volume is
  left–right inverted relative to true fly anatomy. The paper reports true
  biological side throughout, so "right hemisphere GRNs" in this 2024 paper
  = "left hemisphere GRNs" in the group's earlier 2022 eLife paper. All
  FlyWire IDs quoted below are taken verbatim from the authors' own files, so
  this inversion is already handled correctly in them — it only matters if
  you go back to raw connectome coordinates yourself.

**Experimental side** (varies by figure, given per-target below): optogenetic
activation with CsChrimson (635 nm, 153 µW/mm², retinal-fed 2–4 days) or
silencing with GtACR1 (532 nm green) / anion-channelrhodopsin, scored as
proboscis extension response (PER) / rostrum extension in head-fixed,
3–5-day-old mated female flies, blind to genotype, or ΔF/F calcium imaging
(GCaMP6s/jGCaMP7b) of a named second-order neuron. All flies female (the
connectome itself is from a female brain).

**Overall result these targets decompose**: *"Across 164 predictions we were
able to test empirically, 91% were consistent with our empirical results...
Excluding our optogenetic split-GAL4 experiments (Fig. 2)... the accuracy of
the model is 84%."* (main text, p. 218; exact figures below in T-SHIU-1).

---

### T-SHIU-1  Overall validation: 164 predictions, 91.5% accuracy (84.5% excluding the SEZ screen)

- **Quantity** — fraction of independent model predictions (activate/silence
  a named, identified neuron or neuron-class computationally; compare the
  qualitative or thresholded outcome against a real optogenetic/behavioural/
  calcium-imaging result) that the LIF model got right, broken down by the
  sub-study that generated each batch of predictions.
- **Value** — **150/164 correct = 91.46%** overall (main text; Supplementary
  Table 9 [sic — this is a typo in the source: the number is confirmed in
  **Supplementary Table 10**, "Overall predictions", which is the sheet that
  actually contains this breakdown]). **49/58 = 84.48%** excluding the Fig. 2
  SEZ split-GAL4 screen (Supplementary Table 10, second block). Category
  breakdown (verbatim from Supplementary Table 10, sheet "Supp Table 10
  Overall predictio[n]" in the MOESM2 workbook):

  | # | Prediction category | Figure | Correct | Total | Fraction | Correct-prediction citations | Incorrect-prediction citations |
  |---|---|---|---|---|---|---|---|
  | 1 | Ipsilateral MN9 responds more weakly than contralateral MN9 | 1C, Ext.Data 1D | 2 | 2 | 1.00 | MN9: Schwarz et al., 2017 | — |
  | 2 | Neurons that respond to sugar stimulation | 1D, Supp.Table 1 | 12 | 14 | 0.857 | Zorro, G2N-1, Rattle, Clavicle, FMIn, Roundup, Phantom, MN6, MN9, Bract, Fdg: Shiu, Sterne et al. 2022 / Flood et al. 2013 / Gordon & Scott 2009; Fudog: this paper | Usnea: Shiu, Sterne et al. 2022; TH-VUM: Marella et al. 2012 |
  | 3 | Neurons required for sugar feeding (>20% MN9 decrease when silenced vs. real GtACR1 silencing) | 1F, Supp.Table 1 | 6 | 10 | 0.60 | Bract, Clavicle, G2N-1, Phantom, Fdg, Zorro | FMIn, Rattle, Roundup, Usnea |
  | 4 | Neurons sufficient for proboscis extension (SEZ split-GAL4 screen, 50 Hz) | 2A | 101 | 106 | 0.953 | this paper — see T-SHIU-6 below | this paper — see T-SHIU-6 below |
  | 5 | Bitter & Ir94e are aversive; bitter (not Ir94e) can fully block strong-sugar-driven MN9 | 3B–C | 4 | 4 | 1.00 | this paper, Fig. 3 | — |
  | 6 | Water-responsive neurons | 4A | 8 | 10 | 0.80 | Clavicle, Phantom, Rattle, Usnea: Shiu, Sterne et al. 2022; MN6, MN9, Zorro, Fudog: this paper | G2N-1, Roundup: Shiu, Sterne et al. 2022 |
  | 7 | Neurons required for water feeding (>20% MN9 decrease when silenced vs. real GtACR1 silencing) | 4C | 10 | 11 | 0.909 | Bract, Clavicle, G2N-1, Phantom, Rattle, Roundup, Tophat, Tulip, Fudog, Zorro | Usnea |
  | 8 | Neurons responding to JON (mechanosensory) activation | 5B | 3 | 3 | 1.00 | aBN1, aDN1, aDN2: Hampel et al. 2015 | — |
  | 9 | Neurons required for JON-driven grooming output | 5D | 2 | 2 | 1.00 | aBN1, aBN2: Hampel et al. 2015 | — |
  | 10 | aBN1 activity from JO-CE vs. JO-F activation | listed as "5I" in the source table (calcium-imaging panel, Fig. 5h) | 2 | 2 | 1.00 | this paper | — |
  | — | **Total** | | **150** | **164** | **0.9146** | | |
  | — | **Total excluding row 4 (Fig. 2)** | | **49** | **58** | **0.8448** | | |

  Row 4 (the unbiased SEZ split-GAL4 screen) alone supplies 106/164 = 65% of
  all tested predictions — see T-SHIU-6 for the full per-neuron table.
- **Type** — perturbation (aggregate over many independent activation/
  silencing perturbations; not itself a single manipulation).
- **Method (computational)** — general protocol above, one model run per
  named neuron/category, mostly at 50 Hz (SEZ screen) or the frequency
  stated per row.
- **Method (experimental)** — heterogeneous: CsChrimson/GtACR1 behaviour,
  calcium imaging, and — for roughly a third of the 164 — comparison against
  **previously published** results (Shiu, Sterne et al. 2022 eLife; Flood et
  al. 2013 *Nature*; Gordon & Scott 2009 *Neuron*; Hampel et al. 2015 eLife;
  Marella et al. 2012 *Cell*) rather than new experiments run for this paper.
- **Observation model** — a "correct" prediction is a match between (a) a
  binary or thresholded computational readout (nonzero firing at a stated
  activation frequency; >20% firing decrease under silencing at a stated
  frequency) and (b) a binary or thresholded experimental readout (nonzero
  behavioural/imaging response; statistically significant decrease under
  real silencing). To reproduce this number from a re-implementation, you
  must apply the *same* per-category threshold, not a global one — thresholds
  differ (see individual T-SHIU entries below) and are not literal 0/0
  boundaries in all cases (some "required" calls use a 20%-decrease cutoff
  specifically).
- **Conditions** — aggregate; see per-category entries.
- **Source** — Shiu, Sterne et al., *Nature* 634:210–219 (2024), main text
  p. 218 and Supplementary Table 10 (in
  [MOESM2 workbook](https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-024-07763-9/MediaObjects/41586_2024_7763_MOESM2_ESM.xlsx),
  sheet "Supp Table 10 Overall predictio").
- **Confidence** — high for the two headline fractions (91.46%, 84.48%),
  which we recomputed by summing the table's own Correct/Total columns and
  they match the main-text prose exactly. Medium for the attribution of any
  *single* named neuron to "correct" vs. "incorrect" within categories 2, 3,
  6, 7 beyond what's quoted verbatim above, since the citation strings
  sometimes bundle 2–3 neurons per clause.

---

### T-SHIU-2  Free-parameter calibration criterion (w_syn)

- **Quantity** — the single free parameter of the whole model, `w_syn`
  (post-synaptic depolarization/hyperpolarization per synapse), is not fit to
  the 164 predictions — it is fixed *before* any of them by one calibration
  rule against real physiology.
- **Value** — `w_syn = 0.275 mV`, chosen such that **unilateral unilateral
  sugar-GRN Poisson activation at 100 Hz produces ≈80% of the maximal
  (saturating) MN9 firing rate**, citing Dahanukar et al. 2007 (*Neuron* 56)
  and Inagaki et al. 2012 (*Cell* 148) as the source of the 80%-of-max
  target. `f_poi = 250` is a separate, fixed scaling factor applied only to
  the Poisson-input synapses onto directly-activated neurons ("sufficient to
  cause spiking" per the code comment), not a fitted quantity.
- **Type** — perturbation (defines the response curve of a perturbation:
  sugar-GRN activation → MN9 firing, at the single calibration point of
  100 Hz).
- **Method** — general LIF/Brian2 protocol above; the 20 right-hemisphere(**)
  labellar sugar GRNs are the 20 FlyWire IDs listed in T-SHIU-5 below,
  Poisson-activated at exactly 100 Hz, `f_poi=250`, 30×1000 ms runs; contra­
  lateral MN9 mean firing read out and compared to the same neuron's firing
  at saturating GRN drive.
  (** the paper's left/right-hemisphere labelling follows true fly anatomy,
  which is mirrored relative to raw FlyWire/FAFB coordinates — see the
  general-protocol note above.)
- **Observation model** — "maximal MN9 firing" = the plateau value of the
  MN9-firing-rate-vs-GRN-frequency curve (Fig. 1c) at high drive; the
  calibration target is the ratio of the 100 Hz point to that plateau, not
  an absolute Hz value — so reproducing this target requires running the
  full frequency sweep (the paper uses 10–200 Hz in Fig. 1d, we don't have
  the exact plateau-defining frequency they used beyond "high").
- **Conditions** — computational only; no live-fly conditions apply to this
  specific calibration step (the 80%-of-max *target value* itself derives
  from Dahanukar 2007 / Inagaki 2012 physiology, not re-derived here).
- **Source** — Methods, "Computational model" section, p. 11 of the article
  PDF (page numbering as extracted, i.e. the un-numbered Methods section
  immediately following the References).
- **Confidence** — high for the value and the qualitative rule; medium for
  the exact plateau frequency used as "maximal," which is not stated as a
  single number in the text we extracted.

---

### T-SHIU-3  Connectivity-shuffling control: MN9 activation requires the real wiring

- **Quantity** — whether sugar-GRN-driven MN9 activation depends on actual
  FlyWire connectivity, tested by randomly reassigning synaptic connectivity
  (preserving the global weight distribution) and re-running the identical
  activation protocol.
- **Value** — with correct connectivity, sugar-GRN activation at 100 Hz
  activates MN9 in **100% of simulations** (in the sense that all 30 runs at
  100 Hz give appreciable firing — see the individual named-neuron rates
  below). Across **100 independently shuffled connectivity matrices**, MN9
  fired in only **1 of 100** (mean predicted MN9_r firing across the 100
  shuffles = 0.0043 Hz, s.d. 0.043 Hz, vs. 68 Hz [MN9_r] / 49.0 Hz [MN9_l]
  with real connectivity). Full per-neuron table (15 named feeding-circuit
  neurons, correct vs. mean-of-100-shuffles vs. per-shuffle s.d.), from
  Supplementary Table 1D:

  | Neuron | FlyWire ID | Firing, real connectivity (Hz) | Mean firing, 100 shuffles (Hz) | s.d. across shuffles |
  |---|---|---|---|---|
  | Zorro_l | 720575940629888530 | 102.2 | 2.75 | 7.17 |
  | G2N-1_l | 720575940620874757 | 69.4 | 4.86 | 11.11 |
  | Rattle_l | 720575940638103349 | 75.4 | 2.71 | 7.14 |
  | Usnea_l | 720575940632648612 | 72.6 | 5.39 | 9.48 |
  | Clavicle_l | 720575940655014049 | 54.0 | 3.60 | 7.61 |
  | FMIn_l | 720575940614763666 | 61.3 | 4.08 | 9.82 |
  | MN9_r | 720575940660219265 | 68.0 | 0.0043 | 0.043 |
  | Phantom_l | 720575940616103218 | 57.6 | 4.16 | 9.14 |
  | Roundup_l | 720575940623211725 | 46.3 | 0 | 0 |
  | MN9_l | 720575940645521262 | 49.0 | 0 | 0 |
  | Fdg_l | 720575940631997032 | 38.3 | 0.49 | 2.57 |
  | MN6_r | 720575940628826128 | 31.7 | 0 | 0 |
  | Fudog_l | 720575940612648106 | 0.5 | 3.06 | 7.76 |
  | Bract_l | 720575940610001220 | 5.1 | 0.019 | 0.19 |
  | TH-VUM | 720575940616857174 | 32.8 | 0 | 0 |

  This is the source of the exact FlyWire IDs used throughout the paper for
  these 15 named neurons; cross-checked against `figures.ipynb` and
  `sez_neurons.pickle` where those neurons also appear there, with no
  conflicts found.
- **Type** — perturbation (a perturbation of the connectome itself, not of a
  neuron — included here because it's the paper's positive control that the
  *other* 164 predictions are only meaningful given the real connectome).
- **Method** — identical LIF/Brian2 protocol; connectivity matrix
  reassigned uniformly at random 100 times, preserving the global
  distribution of connection weights; sugar GRNs activated at 100 Hz,
  `f_poi=250`, 30×1000 ms runs per shuffle.
- **Observation model** — "activation" = nonzero mean firing across the 30
  runs at that shuffle; the headline "100% vs. 1/100" claim in the main text
  is evaluated on MN9 specifically.
- **Conditions** — computational only.
- **Source** — main text p. 212 ("Although modelling using the correct
  connectome results in robust activation of MN9 in 100% of simulations...
  only 1 of 100 shuffled simulations did"); Supplementary Table 1D (MOESM2
  workbook, sheet "ST 1D Shuffled Connectivity").
- **Confidence** — high; the underlying numbers were read directly from the
  supplementary spreadsheet, not estimated.

---

### T-SHIU-4  Unilateral sugar-GRN activation drives contralateral MN9 more than ipsilateral MN9

- **Quantity** — asymmetry between ipsilateral and contralateral MN9 firing
  rate as a function of unilateral (right-hemisphere, true-anatomy) sugar-GRN
  Poisson activation frequency.
- **Value** — monotonic increase in both MN9s with GRN frequency (0–180 Hz
  tested), contralateral > ipsilateral at every frequency above the lowest;
  Mann-Whitney U p-values at each of 7 frequency points ranging 3.4×10⁻¹⁷ to
  0.14 (the 0.14 point is the lowest/no-drive comparison, i.e. not
  significant, as expected). Also replicated activating the opposite
  (left, true-anatomy) hemisphere GRNs (Extended Data Fig. 1D): p = 1.4×10⁻¹⁰
  and 7.1×10⁻¹¹ at the two frequencies reported there. Matches "MN9: Schwarz
  et al., 2017" per Supplementary Table 10 row 1 (2/2 correct) — we did not
  independently verify this citation's full bibliographic details or
  fetch it; it does not appear in this paper's own numbered reference list,
  so it may be an unpublished or informally-cited source.
- **Type** — perturbation.
- **Method (computational)** — the 20 sugar GRNs (see T-SHIU-5 for IDs),
  activated unilaterally at 10–200 Hz (Fig. 1c/d) or a comparable sweep for
  the opposite hemisphere (Ext. Data 1D); 30×1000 ms runs; `f_poi=250`,
  `w_syn=0.275 mV`.
- **Observation model** — predicted firing rate = mean spike count / 1 s
  across 30 runs, separately for the MN9 ipsilateral and contralateral to
  the activated GRNs; compared with Mann-Whitney U test across runs at each
  frequency, not a single-point threshold.
- **Conditions** — computational; behavioural analog cited is unilateral
  leg/labellum taste stimulation producing proboscis extension curved toward
  the stimulated side (directional PER), which is qualitative corroboration
  rather than a matched quantitative behavioural measurement in this paper.
- **Source** — main text p. 212, Fig. 1c, Extended Data Fig. 1D;
  Supplementary Table 10 row 1.
- **Confidence** — high for the computational asymmetry itself (directly
  read from the paper); low for the "Schwarz et al., 2017" attribution,
  which we could not locate or verify.

---

### T-SHIU-5  Identity of sugar-responsive / sufficient / necessary neurons in the feeding-initiation circuit

- **Quantity** — for each of the 10 previously-characterized feeding-circuit
  neuron classes (Shiu, Sterne et al. 2022 eLife, plus MN9 from Gordon &
  Scott 2009), three separate binary predictions: (1) does it respond to
  sugar-GRN activation (nonzero firing), (2) is activating it alone
  sufficient to fire MN9, (3) is silencing it (during 50 Hz sugar-GRN
  activation) sufficient to reduce MN9 firing by >20% ("required").
- **Value** — verbatim from Supplementary Table 2 (MOESM2 workbook, sheet
  "Supplemental Table 2 Sugar Pred"), with FlyWire IDs merged in from
  Supplementary Table 1D and `sez_neurons.pickle` (both independently give
  the same IDs where they overlap):

  | Neuron | FlyWire ID(s) | Responds to sugar? | Predicted to respond? | Sufficient for PER? | MN9 rate @200 Hz sugar (Hz) | Required for PER to 50 mM sucrose? |
  |---|---|---|---|---|---|---|
  | Bract (Bract1+Bract2) | 720575940626557442, 720575940645045527, 720575940627285267, 720575940610001220 (4 total; Bract1/2 assumed identical phenotype) | Yes | Yes | Yes | 63.97 | No |
  | Clavicle | 720575940632648868, 720575940655014049 | Yes | Yes | Yes | 77.57 | Yes |
  | Fdg | 720575940647030324, 720575940631997032 | Yes | Yes | Yes | 74.77 | Yes (Flood 2013) / No (Shiu 2022) — mixed |
  | FMIn | 720575940636675214, 720575940614763666 | Yes | Yes | Yes | 32.27 | Yes (1 of 2 split-GAL4 lines) |
  | G2N-1 | 720575940623718380, 720575940620874757 | Yes | Yes | Yes | 80.2 | Yes |
  | MN9 | 720575940660219265 (r), 720575940645521262 (l) | Yes (Gordon & Scott 2009) | Yes | Yes | 191.07 | Yes |
  | Phantom | 720575940637763135, 720575940616103218 | Yes | Yes | Yes | **0** (model predicts inhibitory, fails here — see below) | No |
  | Rattle | 720575940630461660, 720575940638103349 | Yes | Yes | Yes | 39.6 | Yes |
  | Roundup | 720575940607272649, 720575940623211725 | Yes | Yes | Yes | 154.7 | No |
  | Usnea | 720575940641366517, 720575940632648612 | **No** (model fails) | Yes | Yes | **0** | Yes |
  | Zorro | 720575940629888530 (only the left/`_l` ID recovered — see note) | Yes | Yes | Yes | 3.53 | Yes |

  Aggregate (Supplementary Table 10): "responds to sugar" 12/14 correct
  (10 neurons above + MN6, MN8/MN11-type entries counted elsewhere bring the
  denominator to 14 — the extra 4 are not separately named in Table 2);
  "required for feeding" 6/10 correct.
  **Known failure mode, stated explicitly in the main text**: Phantom is
  predicted inhibitory and therefore predicted *not* to activate MN9 (since
  the model's baseline firing rate is 0 Hz, an inhibitory neuron with no
  tonic drive to inhibit has no effect) — this is wrong; Phantom's real
  silencing/activation phenotype is strong. The authors' explanation: Phantom
  → Scapula (also inhibitory) → Roundup (strongest premotor driver of MN9);
  disinhibition, not direct excitation, may be the true mechanism, which a
  zero-baseline LIF model cannot express. **Usnea** is a second stated
  failure: it has a strong experimental activation/silencing phenotype but
  is neuropeptidergic (the authors show *Amontillado* RNAi phenocopies the
  Usnea-silencing PER defect), which the model — connectivity/fast-synapse
  only — cannot capture.
- **Type** — perturbation.
- **Method (computational)** — activation: single named neuron(s) or the
  20-neuron sugar-GRN set, `r_poi` swept, `f_poi=250`; silencing: sugar GRNs
  activated at 50–120 Hz in 10 Hz steps while the named neuron's outputs are
  zeroed, "required" = MN9 firing ≤80% of unsilenced control at *any* of the
  8 tested frequencies. Sugar-GRN set (20 labellar sugar GRNs, right
  hemisphere/true anatomy), from `figures.ipynb`:
  `720575940624963786, 720575940630233916, 720575940637568838, 720575940638202345, 720575940617000768, 720575940630797113, 720575940632889389, 720575940621754367, 720575940621502051, 720575940640649691, 720575940639332736, 720575940616885538, 720575940639198653, 720575940620900446, 720575940617937543, 720575940632425919, 720575940633143833, 720575940612670570, 720575940628853239, 720575940629176663, 720575940611875570`.
  A separate 10-GRN **left**-hemisphere sugar set exists for Extended Data
  Fig. 1D / S1D (not re-quoted here — see `figures.ipynb` cell under
  "Figure S1D").
- **Observation model** — "responds" = nonzero mean firing over 30×1000 ms
  runs; "sufficient" = activating that neuron alone at 25–200 Hz gives
  nonzero MN9 firing; "required" = ≥20% MN9 firing decrease vs. unsilenced
  control, matched against real GtACR1/Kir2.1 silencing scored as
  significantly reduced PER (Fisher's exact test) in the group's earlier
  2022 eLife paper (ground truth for 9 of the 10 rows) or this paper's own
  new optogenetics (Fdg discrepancy, Usnea, Zorro, Clavicle, G2N-1, Rattle,
  Roundup, Bract confirmed here too — Fig. 4d panel, which is nominally the
  *water* experiment but reuses these same neurons).
- **Conditions** — real-fly side: 3–5-day-old mated female flies,
  CsChrimson/GtACR1, retinal-fed 48 h, CO₂-anesthetized and mounted, 22 °C,
  blind scoring; taste stimulus 50 mM sucrose to the labellum.
- **Source** — main text pp. 212–213; Supplementary Table 2 (MOESM2
  workbook); Shiu, Sterne, Engert, Dickson & Scott, "Taste quality and hunger
  interactions in a feeding sensorimotor circuit," *eLife* 11:e79887 (2022),
  <https://elifesciences.org/articles/79887> (ground truth for most rows).
- **Confidence** — high for the table contents (read directly from the
  supplement) and for the two named failure modes (stated explicitly by the
  authors as such). Medium for the Zorro FlyWire ID — only one ID
  (`_l`) was recoverable from the sources we mined; Zorro is *not* one of
  the 106 cell types in `sez_neurons.pickle`, so we could not cross-check a
  second (right-hemisphere) copy the way we could for the other 9 neurons.

---

### T-SHIU-6  SEZ split-GAL4 unbiased screen: 106 identified cell types, computational vs. optogenetic MN9/rostrum activation

This is the single largest block of individual predictions in the paper
(106 of the 164, all newly generated for this paper rather than compared to
prior literature) and the best-documented one — every row below has a
FlyWire ID set, a predicted firing curve, a real split-GAL4 behavioural
result, and an explicit correct/incorrect call.

- **Quantity** — for 106 SEZ (subesophageal zone) cell types with validated
  split-GAL4 driver lines (out of 138 in the Sterne et al. 2021 eLife
  collection; 106 were matched to FlyWire neurons), whether computationally
  activating that cell type at 50 Hz predicts nonzero MN9 firing, compared
  against whether optogenetically activating the same cell type with
  CsChrimson elicits rostrum extension (the MN9-controlled proboscis
  segment) in real flies (n=10 flies/genotype for the initial screen; the
  highest-scoring split-GAL4 line per cell type is used where several
  existed for one cell type).
- **Value** — confusion matrix (Fig. 2c, main text p. 213): of 11 cell types
  predicted positive at 50 Hz, 10/11 actually caused rostrum extension
  (91% positive predictive value); of 95 predicted negative, 91/95 correctly
  had no/negligible extension (4 false negatives). Overall **101/106 = 95.3%
  accuracy** (this is category 4 in the T-SHIU-1 table). At 200 Hz instead of
  50 Hz, 5 additional false positives appear. At 10 Hz, 6 predicted positive,
  of which the paper states "of these five, six do indeed cause proboscis
  extension" (main text — this sentence appears to contain a typo/off-by-one
  in the original: "these five" vs. "six," so we quote it as written rather
  than resolve the discrepancy ourselves).

  Full per-cell-type table, from Supplementary Table 3 (MOESM2 workbook,
  sheet "Sup Table 3 Predicted MN9 vs. o[ptogenetic]"), FlyWire IDs merged
  in from `sez_neurons.pickle` (exact match by name for all 106 rows):

  | Name | FlyWire ID(s) | Predicted MN9 @ 50 Hz, L/R (Hz) | Predicted+ | Actual fraction extending rostrum | Actual+ | Match | Synapses to MN9 | Split-GAL4 line(s): individual PER fraction |
  |---|---|---|---|---|---|---|---|---|
  | roundup | 2 IDs, e.g. 720575940607272649 | 79.5 / 82.7 | Y | 1.00 | Y | yes | 1 | SS47730: .9, SS47731: .8, SS47744: 1, SS47745: .9 |
  | diatom | 14 IDs, e.g. 720575940626679317 | 29.1 / 28.3 | Y | 0.60 | Y | yes | 2 | SS40945: 0.4; SS35298: .6 |
  | sink_sync | 4 IDs, e.g. 720575940622624214 | 22.2 / 22.8 | Y | 0.20 | Y | yes | 1 | SS31372: 0.2 |
  | G2N_1 | 2 IDs | 12.4 / 14.0 | Y | 1.00 | Y | yes | 2 | SS56399: 1 |
  | clavicle | 2 IDs | 10.5 / 7.1 | Y | 0.50 | Y | yes | 2 | SS48947: 0.5 |
  | Fdg | 2 IDs | 22.5 / 20.3 | Y | 0.80 | Y | yes | 2 | SS31333: 0.8 |
  | bract | 4 IDs | 33.7 / 25.2 | Y | 0.80 | Y | yes | 2 | SS31320: 0.8, SS31386: 0.5 |
  | vice | 6 IDs, e.g. 720575940621431884 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS49415: 0 |
  | rattle | 2 IDs | 1.9 / 1.2 | Y | 0.90 | Y | yes | 2 | SS46917: .9; SS50091: .9 |
  | FMIn | 2 IDs | 0.4 / 0.1 | Y | 1.00 | Y | yes | 2 | SS48944: 0.7, SS48949: 0.7, SS48948: 1 |
  | TH_VUM | 720575940616857174 | 0.0 / 2.5 | Y | 1.00 | Y | yes | 1 | SS46885: .9, SS46889: 1 |
  | aster | 4 IDs, e.g. 720575940621982413 | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS45679/80/82: 0 |
  | seagull | 720575940626278974 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS41402: 0 |
  | mist | 2 IDs, e.g. 720575940646530612 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS34739: 0 |
  | **kitty** | 4 IDs, e.g. 720575940644669732 | **7.3 / 10.9** | **Y** | **0.00** | **N** | **NO (false positive)** | 2 | SS41391: 0 |
  | fudog | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS35291: 0 |
  | aDT6 | 11 IDs, e.g. 720575940630165007 | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | SS39040/52/54: 0 |
  | aSG1 | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | No path | SS45907/98/45913: 0 |
  | aSG7 | 5 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | 7 lines, all 0 |
  | amulet | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS32423: 0 |
  | asteroid | 3 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS35282/42335: 0 |
  | bamboo | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS44928/37: 0 |
  | basket | 15 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | SS29227: 0 |
  | bluebell | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS31328/41: 0 |
  | bobber | 720575940621628582 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS29032: 0 |
  | box | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS35283: 0 |
  | bridle | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | No path | SS50095/120: 0 |
  | brontosaraus | 12 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS40950: 0 |
  | broom | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS39923: 0 |
  | buddy | 3 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 1 | SS47281/83: 0 |
  | coy | 720575940618156689 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS51996/97: 0 |
  | crab | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS45693/94/45700: 0 |
  | cradle | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS48137: 0 |
  | damsel | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS38113: 0 |
  | doublescoop | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS47081: 0 |
  | earmuff | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS31063: 0 |
  | eiffel | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS52029/34: 0 |
  | fluff | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS44912: 0 |
  | foxglove | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS40909/26: 0 |
  | gallinule | 10 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | 4 lines, all 0 |
  | gazebo | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS28878: 0 |
  | genie | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS35835: 0 |
  | gnome | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS37818: 0 |
  | good_dog | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS47293: 0 |
  | gumdrop | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS46373: 0 |
  | handle | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS42328/47287: 0 |
  | handup | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 1 | SS47287: 0 |
  | haystack | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS32391: 0 |
  | horn | 3 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS38555: 0 |
  | horntail | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS51950: 0 |
  | horseshoe | 9 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | 3 lines, all 0 |
  | hound | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS47232: 0 |
  | hyacinth | 6 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS39890: 0 |
  | justice | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS29813: 0 |
  | kelp | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | 3 lines, all 0 |
  | knees | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | SS42927: 0 |
  | kokopelli | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS38523: 0 |
  | landslide | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS38119: 0 |
  | lion | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS36657: 0 |
  | mandala | 10 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS38164/65: 0 |
  | **marge** | 2 IDs, e.g. 720575940620262465 | 0.0 / 0.0 | N | **0.10** | **Y** | **NO (false negative)** | 2 | SS32463: 0.1 |
  | meteor | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS35420: 0 |
  | mime | 14 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS47275: 0 |
  | moor | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | 3 lines, all 0 |
  | mothership | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS38535: 0 |
  | mute | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | No path | SS42606: 0 |
  | nagini | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS47322: 0 |
  | nori | 3 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 1 | SS50701: 0 |
  | oink | 9 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS47078: 0 |
  | OinkT | 6 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS32394: 0 |
  | oval | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS39916: 0 |
  | pSG1 | 6 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | 3 lines, all 0 |
  | peacock (†) | 4 IDs, e.g. 720575940612030899 | 0.0 / 0.03 | N* | 0.00 | N | yes* | 3 | SS30409: 0 |
  | peafowl | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | SS37792: 0 |
  | peahen (†) | 4 IDs | 0.0 / 0.03 | N* | 0.00 | N | yes* | 4 | SS39038: 0 |
  | **phantom** | 2 IDs | 0.0 / 0.0 | N | **0.60** | **Y** | **NO (false negative)** | 2 | SS44877: 0.6 |
  | planter | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS36658: 0 |
  | pleco | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS41967: 0 |
  | pringle | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | 3 lines, all 0 |
  | puddle | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | 3 lines, all 0 |
  | rocket | 18 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | 3 lines, all 0 |
  | rose | 720575940624101524 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS46955: 0 |
  | ruby | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 5 | SS43355/59: 0 |
  | Salivary_MN13 | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | No path | SS35823: 0 |
  | shark | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | No path | SS45729: 0 |
  | snake | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS31705/08: 0 |
  | spirit | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS49430: 0 |
  | spray | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS39867: 0 |
  | sullivan | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | SS42638/39: 0 |
  | sundrop | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | 4 lines, all 0 |
  | **tentacular** | 2 IDs, e.g. 720575940620673985 | 0.0 / 0.0 | N | **0.50** | **Y** | **NO (false negative)** | 2 | SS51930: .5 |
  | tinctoria | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS39007/20: 0 |
  | tophat | 4 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS39932/93: 0 |
  | TPN4 | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 4 | SS44856/66: 0 |
  | trident | 720575940624163303 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | 3 lines, all 0 |
  | trogon | 720575940631595603 | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS45730: 0 |
  | trumpet | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS42603: 0 |
  | tulip | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS45941: 0 |
  | tundra | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS41386: 0 |
  | turner | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS45676/49422: 0 |
  | twirl | 720575940636034661 | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS51958: 0 |
  | **usnea** | 2 IDs | 0.0 / 0.0 | N | **1.00** | **Y** | **NO (false negative)** | 3 | SS37122: 1; SS31022: 1 |
  | wafflecone | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS50698: 0 |
  | weaver | 13 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 3 | SS39883: 0 |
  | web | 6 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 1 | SS41434/48: 0 |
  | whisker | 2 IDs | 0.0 / 0.0 | N | 0.00 | N | yes | 2 | SS39947/42349: 0 |

  (†) `peacock`/`peahen` show a borderline nonzero predicted rate (0.033 Hz
  — i.e. 1 spike total across 30×1000 ms runs) at 50 Hz on one side only.
  Treating any-nonzero as "predicted positive" makes these 2 rows disagree
  with our recomputed match column; treating this as simulation noise
  (not a real prediction) instead reproduces the paper's stated 101/106
  exactly, and reconciles cleanly against the paper's own named failure
  examples: our reconstruction's 5 true mismatches are exactly **kitty**
  (the 1 false positive: predicted 7.3–10.9 Hz, 0% extension) and
  **phantom, tentacular, usnea, marge** (4 false negatives: predicted 0 Hz,
  nonzero extension) — 106 − 5 = 101, matching the paper exactly. Phantom,
  Tentacular and Usnea are the ones the main text names explicitly ("Fig. 2
  ... when the neurons tested were predicted to be inhibitory (i.e.
  Tentacular or Phantom) or neuromodulatory (Usnea)"); Marge and Kitty are
  not individually named in the main text, only recovered by us from the
  raw table.
- **Type** — perturbation (106 independent single-cell-type activation
  perturbations, run at a shared protocol/frequency).
- **Method (computational)** — each of the 106 named cell types' full
  FlyWire ID set (from `sez_neurons.pickle`) Poisson-activated together at
  10, 20, 30, 40, 50, 100, 150, 200 Hz; 30×1000 ms runs each; `f_poi=250`,
  `w_syn=0.275 mV`; MN9 mean firing read out on both sides (columns "L"/"R"
  above — the paper does not specify which side is "predicted" for the
  confusion matrix when they differ, so we report both and call a row
  "predicted positive" if *either* side is nonzero, per the general 0 Hz
  activation-threshold rule stated elsewhere in the paper).
  Cell-type-to-FlyWire-ID matching used two independent methods (NBLAST
  against light-microscopy dotprops, and manual skeleton tracing from
  registered confocal images), cross-checked between two sets of
  researchers, keeping only cell types with clear consensus (Methods,
  "Identification of SEZ split-GAL4 neurons").
- **Method (experimental)** — CsChrimson (635 nm, 153 µW/mm²) optogenetic
  activation of each split-GAL4 line, retinal-fed 48 h, scored for rostrum
  (MN9-controlled segment) extension within 5 s of light onset, n=10
  flies/genotype for the initial screen (any-movement scoring), then a
  second independent cross scored specifically for rostrum extension for any
  line with a positive first-pass result; where multiple lines exist for one
  cell type, the highest-scoring line's fraction is reported.
- **Observation model** — "predicted positive" = nonzero mean MN9 firing at
  50 Hz across the 30-run window (see caveat above re: near-zero noise);
  "actual positive" = fraction of flies extending rostrum > 0. To
  reproduce the paper's exact 101/106, a re-implementation should either
  round very small (≲0.05 Hz) predicted rates to zero, or otherwise match
  the specific 5 discordant cases named above rather than relying on a
  literal floating-point >0 test.
- **Conditions** — 3–5-day-old female flies, standard cornmeal-yeast-
  molasses medium, 0.4 mM all-trans-retinal for 48 h before testing,
  CO₂-anesthetized and slide-mounted, 2 h recovery, tested blind to
  genotype at room temperature (22 °C implied but not restated in this
  section of Methods).
- **Source** — main text pp. 213, 217 (Fig. 2, and the "poorly modelled
  circuits" discussion of Tentacular/Phantom/Usnea); Methods, "Identification
  of SEZ split-GAL4 neurons..."; Supplementary Table 3 (MOESM2 workbook);
  cell-type collection from Sterne, Otsuna, Dickson & Scott, "Classification
  and genetic targeting of cell types in the primary taste and premotor
  center of the adult *Drosophila* brain," *eLife* 10:e71679 (2021),
  <https://elifesciences.org/articles/71679>.
- **Confidence** — high for all FlyWire IDs and raw predicted/actual values
  (read directly from the supplementary spreadsheet and the pickle file,
  cross-checked against each other by name — no conflicts found across
  106 names). Medium for the exact match/mismatch call on `peacock` and
  `peahen` specifically, for the reason given in the (†) note. The
  overwhelming majority of rows (all-zero predicted, all-zero actual) are
  unambiguous.

---

### T-SHIU-7  Bitter and Ir94e taste modalities inhibit sugar-driven proboscis extension

- **Quantity** — four related predictions about aversive-taste GRN
  co-activation with sugar GRNs: (a) bitter GRN co-activation inhibits
  sugar-driven MN6/MN9 firing; (b) this matches prior calcium-imaging
  evidence that bitter inhibits at the level of premotor neurons; (c) Ir94e
  GRN activation, previously uncharacterized for feeding, is newly predicted
  to *inhibit* (not promote) MN9 firing; (d) optogenetic activation of
  either bitter or Ir94e GRNs is sufficient to suppress real PER to 50 mM
  sucrose, with bitter (but not Ir94e) also suppressing PER to 1 M sucrose.
- **Value** — Supplementary Table 10 row 5: **4/4 correct**. Quantitative
  behavioural results (Fig. 3d–e, n=26–32 flies/condition, exact n in
  Supplementary Table 9):
  - 50 mM sucrose + Gr66a(bitter)>CsChrimson: PER drops on light-on,
    P=2.0×10⁻⁹ (Fisher's exact, vs. light-off same genotype).
  - 1 M sucrose + Gr66a>CsChrimson: PER drops to ~0, P=5.5×10⁻¹².
  - 50 mM sucrose + Ir94e>CsChrimson: PER drops, P=3.6×10⁻⁹.
  - 1 M sucrose + Ir94e>CsChrimson: PER drop not significant, P=0.099 (i.e.
    Ir94e activation does *not* override strong sugar drive — matches the
    model's *quantitative* prediction that bitter, but not Ir94e, can zero
    out MN9 firing at high sugar-GRN rates, Fig. 3b vs. 3c).
  - Overlap analysis (Fig. 3f): at the sugar/water frequency giving 40 Hz
    MN9, sugar activates 377 neurons and water 391, sharing 250; only 2
    neurons shared between sugar-activated and bitter-suppressing sets, and
    30 shared between sugar-activated and Ir94e-suppressing sets — i.e. the
    model predicts near-total segregation of appetitive vs. aversive taste
    representations, consistent with the group's own prior calcium-imaging
    finding that 0/9 sugar-responsive cell types respond to a bitter mix.
- **Type** — perturbation (co-activation of two Poisson-driven populations
  in the model; two-channel optogenetic activation in the fly — though
  actually the real-fly experiment activates only one channel [bitter or
  Ir94e] against a fixed real sugar stimulus, not two simultaneous optogenetic
  channels).
- **Method (computational)** — sugar GRNs (`r_poi`, 20–200 Hz) and
  bitter or Ir94e GRNs (`r_poi2`, 20–200 Hz, independent Poisson class)
  co-activated; 30×1000 ms runs per (sugar-freq, other-freq) grid point;
  bitter GRN set (21 IDs) and Ir94e GRN set (18 IDs), from `figures.ipynb`:
  bitter = `720575940621778381, 720575940602353632, 720575940617094208, 720575940619197093, 720575940626287336, 720575940618600651, 720575940627692048, 720575940630195909, 720575940646212996, 720575940610483162, 720575940645743412, 720575940627578156, 720575940622298631, 720575940621008895, 720575940629146711, 720575940610259370, 720575940610481370, 720575940619028208, 720575940614281266, 720575940613061118, 720575940604027168`;
  Ir94e = `720575940614211295, 720575940638218173, 720575940628832256, 720575940626016017, 720575940621375231, 720575940612920386, 720575940614273292, 720575940628198503, 720575940626241636, 720575940619387814, 720575940624604560, 720575940615274425, 720575940610683315, 720575940627265265, 720575940624079544, 720575940629211607, 720575940615089369, 720575940631082124`.
- **Method (experimental)** — CsChrimson activation of Gr66a-GAL4 (bitter)
  or Ir94e-GAL4, retinal-fed 4 days, PER scored to 50 mM or 1 M sucrose
  delivered 3× to the labellum, blind to genotype, Fisher's exact test vs.
  no-retinal/no-light controls.
- **Observation model** — computational: MN9 firing rate at each
  (sugar-Hz, aversive-Hz) grid cell, read as mean over 30×1000 ms runs;
  behavioural: fraction of flies extending proboscis at least once across 3
  presentations, Wilson score 95% CI, Fisher's exact test light-on vs.
  light-off.
- **Conditions** — 3–4-day-old female flies, retinal-fed (48 h for GtACR1
  panels, 4 days for the Ir94e/Gr66a activation panels per Methods), water-
  satiated before testing (for the sucrose PER assays), CO₂-anesthetized,
  22 °C.
- **Source** — main text pp. 213–214, Fig. 3; Supplementary Table 4
  (interaction firing-rate data — not separately extracted row-by-row here,
  see "what we did not extract" below) and Supplementary Table 9 (exact n
  per condition, partially extracted in T-SHIU note below); Supplementary
  Table 10 row 5.
- **Confidence** — high; all values above are quoted directly from the
  article's figure legends/main text, which state exact P-values and n
  ranges.

---

### T-SHIU-8  Identity of water-responsive / sufficient / necessary neurons

- **Quantity** — same three-way prediction structure as T-SHIU-5, but for
  the water-taste pathway (11 named neurons, tested via pseudo-desiccation
  rather than starvation).
- **Value** — Supplementary Table 10 row 6 ("water-responsive neurons"):
  8/10 correct; row 7 ("required for water PER"): 10/11 correct. Per-neuron
  table, from Supplementary Table 5 (MOESM2 workbook, sheet "Supplemental
  Table 5 Water Pred"):

  | Neuron | FlyWire ID(s) | Responds to water (pseudo-desiccated)? | Predicted to respond? | Sufficient for PER? | MN9 rate @200 Hz water (Hz) | Required for water PER? |
  |---|---|---|---|---|---|---|
  | Bract | (see T-SHIU-5) | Not tested | Yes | Yes | 63.97 | Yes (this paper) |
  | Clavicle | (see T-SHIU-5) | Yes | Yes | Yes | 77.57 | Yes (this paper) |
  | G2N-1 | (see T-SHIU-5) | **No significant response** | Yes | Yes | 80.2 | No (this paper) |
  | MN9 | (see T-SHIU-5) | — | Yes | Yes | 191.07 | Not tested |
  | Phantom | (see T-SHIU-5) | Yes in starved flies, not tested pseudo-desiccated | Yes | Yes | 0 | No (this paper) |
  | Rattle | (see T-SHIU-5) | Yes | Yes | Yes | 39.6 | Yes (this paper) |
  | Roundup | (see T-SHIU-5) | **No significant response** | Yes | Yes | 154.7 | Yes (this paper) |
  | Tophat | 4 IDs (see T-SHIU-6 table) | Not tested | Yes | **No** (this paper) | 0 | No (this paper) |
  | Tulip | 2 IDs (see T-SHIU-6 table) | Not tested | Yes | **No** (this paper) | 0 | No (this paper) |
  | Usnea | (see T-SHIU-5) | Yes | Yes | Yes | 0 | Yes (this paper) |
  | Zorro | 720575940629888530 | Yes, this paper (Ext. Data 4A) | Yes | Yes | 3.53 | Yes (this paper) |

  Two additional neurons contribute to the official "8/10" count without
  being rows in this table: **MN6** (responds, confirmed) and **Fudog**
  (responds, confirmed by calcium imaging, Ext. Data Fig. 3a) — per the
  citation string in Supplementary Table 10 row 6. We could not fully
  reconcile the exact denominator (Table 5 has 11 rows, 3 "not tested" =
  8 testable, but the official total is 10) — see "what we could not find"
  below.
  Sugar/water synergy: co-activation increases MN9 firing more than either
  alone (Fig. 4e); silencing sugar GRNs reduces water-driven PER
  (Fig. 4f, P=1.5×10⁻⁶, n=39–40) even though only water GRNs were previously
  known to be required for water PER — a genuinely novel (not
  literature-matched) prediction confirmed experimentally in this paper.
- **Type** — perturbation.
- **Method (computational)** — 18-neuron labellar water-GRN set (right
  hemisphere/true anatomy), 20–260 Hz sweep, from `figures.ipynb`:
  `720575940612950568, 720575940631898285, 720575940606002609, 720575940612579053, 720575940622902535, 720575940616177458, 720575940660292225, 720575940622486922, 720575940613786774, 720575940629852866, 720575940625861168, 720575940613996959, 720575940617857694, 720575940644965399, 720575940625203504, 720575940630553415, 720575940635172191, 720575940634796536`.
  Silencing/required test: water GRNs activated at 160–220 Hz in 10–20 Hz
  steps, each of the top-200 water-responsive neurons silenced individually,
  "required" = MN9 ≤80% of unsilenced control at any tested frequency
  (identical rule to the sugar case).
- **Method (experimental)** — GtACR1 (green light) optogenetic silencing
  during real water presentation to the proboscis, PER scored, n=40–50
  flies; pseudo-desiccation (high-osmolarity AHL bath, 1 h) used instead of
  starvation as the "thirsty-like" internal state for calcium imaging.
- **Observation model** — identical rule structure to T-SHIU-5 but with
  "pseudo-desiccated" as the internal-state control for physiological
  water-responsiveness, and GtACR1 (not Kir2.1) as the silencing tool for
  the "required" behavioural comparisons.
- **Conditions** — female flies; calcium imaging at 14–21 days
  post-eclosion (older than the PER cohorts); pseudo-desiccation = dissected
  brain bathed in ~350 mOsm AHL for 1 h before imaging (vs. ~250 mOsm
  normal AHL).
- **Source** — main text pp. 214–216, Figs. 4a–f; Supplementary Table 5
  (MOESM2 workbook); Supplementary Table 10 rows 6–7.
- **Confidence** — high for the per-neuron table contents; medium for the
  exact 8/10 and 10/11 denominators, since (as noted) they don't cleanly
  match a simple count of this table's rows.

---

### T-SHIU-9  Antennal grooming circuit: JON activation identifies aBN1, aBN2, aDN1, aDN2

- **Quantity** — computational activation of the full population of
  Johnston's-organ mechanosensory neurons (JONs) is predicted to drive the
  four previously-characterized grooming-command neurons (aBN1, aBN2, aDN1,
  aDN2) among the responsive population, without those four being specified
  as targets in advance (purely a "sensory input → find the known circuit"
  test, the grooming-circuit analogue of the sugar-GRN-network experiment).
- **Value** — Supplementary Table 10 row 8: **3/3 correct** (aBN1, aDN1,
  aDN2 [reported as "DN2" in the citation, presumably aDN2] all found among
  JON-responsive neurons, matching Hampel et al. 2015's description of the
  circuit). We independently confirmed nonzero, dose-dependent predicted
  firing for all three in the supplementary per-neuron activation table:
  aBN1 (`720575940630907434`) rises from ~6 Hz (JON@20Hz) to ~68 Hz
  (JON@200Hz) in both the aDN1-readout and aDN2-readout tables; aDN2_l
  (`720575940629806974`) rises similarly when JONs drive aDN1's readout
  table; aDN1_l (`720575940616185531`) is (trivially) driven when JONs
  directly target it.
- **Type** — perturbation.
- **Method (computational)** — 145 JON IDs Poisson-activated together at
  20–220 Hz (11-point sweep), 30×1000 ms runs; top-300 JON-responsive
  neurons then individually re-activated at 25–200 Hz to test which can
  drive aDN1/aDN2. JON ID lists (from `figures.ipynb`; note the paper's main
  text states "147 JONs of the JO-C, JO-E, JO-F and JO-m subclasses" — the
  three lists we recovered from the code total 145, a small, unexplained
  discrepancy we did not resolve):
  - JO-CE (69 IDs): `720575940619341105, 720575940630122015, 720575940611061526, 720575940615848788, 720575940628444667, 720575940627941431, 720575940632449619, 720575940650244342, 720575940631866508, 720575940638681845, 720575940628978450, 720575940609522461, 720575940621442224, 720575940602506208, 720575940629022149, 720575940627109991, 720575940630020111, 720575940615986459, 720575940618684481, 720575940620382889, 720575940630080071, 720575940626565455, 720575940630319671, 720575940602720940, 720575940630564179, 720575940637632419, 720575940615809349, 720575940626042149, 720575940637054835, 720575940602132509, 720575940614188149, 720575940616951124, 720575940628101126, 720575940629055721, 720575940616589878, 720575940622449388, 720575940614427195, 720575940625797617, 720575940638664437, 720575940618467195, 720575940621729757, 720575940613971485, 720575940627585688, 720575940629650997, 720575940630059847, 720575940608742409, 720575940614351477, 720575940633153375, 720575940622937528, 720575940604753437, 720575940611783464, 720575940618599872, 720575940609541917, 720575940637410869, 720575940630070343, 720575940621397417, 720575940614035485, 720575940610018266, 720575940626307902, 720575940634634606, 720575940614060829, 720575940624799290, 720575940641921421, 720575940623298559, 720575940625559358, 720575940629138959, 720575940621625597, 720575940625962568, 720575940632767383, 720575940624915230`
  - JO-F (60 IDs): `720575940606239243, 720575940626956777, 720575940604973746, 720575940622222856, 720575940642517284, 720575940629719404, 720575940616613022, 720575940604299454, 720575940615473186, 720575940622217992, 720575940606800341, 720575940629267498, 720575940637366335, 720575940624224408, 720575940609543197, 720575940633364179, 720575940629502009, 720575940606431189, 720575940625733960, 720575940638529525, 720575940617524053, 720575940628935564, 720575940624308355, 720575940631170346, 720575940627704375, 720575940625885512, 720575940614929245, 720575940647493241, 720575940618888368, 720575940625087546, 720575940606657493, 720575940617273560, 720575940640591861, 720575940639410035, 720575940621532413, 720575940627523584, 720575940621521917, 720575940621097398, 720575940625915338, 720575940606222428, 720575940627868471, 720575940622179497, 720575940608297774, 720575940614026269, 720575940613012959, 720575940628100614, 720575940606611401, 720575940628649465, 720575940610008217, 720575940623791152, 720575940625571240, 720575940634923621, 720575940609530653, 720575940635968745, 720575940625703434, 720575940613105311, 720575940629386819, 720575940623077389, 720575940625763015, 720575940628359017`
  - JO-mz (16 IDs, variable name `neu_JON_D_m` in the source — we could not
    confirm whether "D_m" denotes a distinct "JO-D" subclass or is simply
    the code's internal label for JO-mz): `720575940630834171, 720575940622892988, 720575940621289537, 720575940641395163, 720575940616064546, 720575940628978409, 720575940652566177, 720575940627493096, 720575940619085397, 720575940635545310, 720575940645728803, 720575940629141775, 720575940626557995, 720575940631098338, 720575940639904475, 720575940635067034`
- **Observation model** — "responds" = nonzero mean firing across
  30×1000 ms runs when the full JON population is activated; compared
  qualitatively against the neurons' inclusion in Hampel et al. 2015's
  circuit diagram (aBN1, aBN2 interneurons → aDN1, aDN2 descending neurons),
  not a quantitative behavioural readout.
- **Conditions** — computational only for this specific sub-result (no new
  fly experiment; ground truth is the cited 2015 anatomical/functional
  circuit description).
- **Source** — main text p. 216, Fig. 5a–b; Supplementary Table 7A/B/C
  (MOESM2 workbook); Hampel, Franconville, Simpson & Seeds, "A neural
  command circuit for grooming movement control," *eLife* 4:e08758 (2015),
  <https://elifesciences.org/articles/08758>.
- **Confidence** — high for the FlyWire IDs (aBN1/aDN1/aDN2, cross-validated
  across `figures.ipynb`, Supplementary Table 7B and 7C — identical in all
  three) and for the qualitative 3/3 result; low-medium for the exact JON
  membership lists given the 145-vs-147 discrepancy noted above (small,
  likely a version/annotation-update effect between when the code was
  written and when the final paper's numbers were locked).

---

### T-SHIU-10  Neurons required for JON-driven grooming output: aBN1 and aBN2

- **Quantity** — of the neurons found to respond to JON activation (see
  T-SHIU-9), which ones are required to drive the descending neuron aDN1,
  tested by silencing each individually during full-population JON drive.
- **Value** — Supplementary Table 10 row 9: **2/2 correct** — aBN1 and aBN2
  are each at least partially required for antennal grooming per Hampel et
  al. 2015, and the model predicts exactly these (plus aDN2 itself and one
  further un-named descending BN2-class member) among the handful of
  neurons whose silencing reduces aDN1 firing by >20% at 140 Hz JON drive.
  Quantitatively (main text p. 216): "only three neurons, besides aDN1
  itself, were identified that reduced aDN1 activity by more than 20% at
  140 Hz JON activation: aBN1; a descending member of the BN2 class; and
  aDN2." Separately, only 4 neurons (besides aDN1 itself) were found
  *sufficient* to elicit aDN1 activity at all: aBN1, aDN2, and two further
  neurons eliciting <2 Hz aDN1 firing (FlyWire IDs `720575940653315489` and
  `720575940644072483`, un-named in the paper; predicted aDN1-eliciting
  firing at 200 Hz JON drive: 0.33 Hz and 1.07 Hz respectively — i.e. real
  but far weaker than aBN1's 68.5 Hz or aDN2's 33.6 Hz at the same drive).
- **Type** — perturbation.
- **Method (computational)** — full 145-JON population activated at 140,
  150, 160, 170, 180 Hz; each of the top-300 JON-responsive neurons silenced
  individually (one at a time) during that drive; aDN1 (and separately,
  aDN2) firing recorded relative to unsilenced control.
- **Observation model** — "required" (for this figure) = >20% *decrease* in
  aDN1 firing at 140 Hz JON drive when silenced, vs. Hampel et al. 2015's
  behavioural/optogenetic demonstration that silencing aBN1 or aBN2 disrupts
  grooming. We attempted to reproduce the exact silencing-effect numbers
  directly from Supplementary Table 7D but found the "normalized" column
  values cluster near 1.0 (no effect) for the ~300 JON rows we sampled,
  consistent with most individual JONs having negligible individual effect
  on aDN1 when 145 are driven together — we did not exhaustively re-derive
  the >20%-decrease threshold crossing for aBN1/aBN2/aDN2 specifically from
  the raw table within the scope of this pass; the quoted 2/2 and the named
  three neurons above are taken directly from the main text, not
  re-derived.
- **Conditions** — computational (silencing) vs. Hampel et al. 2015 (prior,
  independent optogenetic silencing/anatomical necessity evidence — no new
  fly experiment for this specific sub-result).
- **Source** — main text p. 216; Supplementary Table 7D/7E (MOESM2
  workbook, sheets "Supp Table 7D aDN1 firing upon [silencing]" and
  "...7E aDN2 firing upon [silencing]"); Hampel et al. 2015 (as above).
- **Confidence** — high for the qualitative 2/2 claim and the named
  neurons/IDs (aBN1, aDN2, plus the two weakly-sufficient un-named IDs,
  all read directly from the supplementary table); medium for the
  underlying %-decrease numbers, which we did not fully recompute from
  the raw 300-row silencing matrix (see "what we did not extract").

---

### T-SHIU-11  JO-CE vs. JO-F differentially activate aBN1 despite both synapsing onto it

- **Quantity** — whether the two JON subpopulations JO-CE and JO-F, which
  both synapse directly onto aBN1 (103 and 78 synapses respectively),
  produce different amounts of predicted aBN1 activity — a genuinely novel
  (not literature-derived) prediction, tested by calcium imaging in this
  paper.
- **Value** — Supplementary Table 10 row 10: **2/2 correct**. Quantitative
  values at 150 Hz population activation (Supplementary Table 8, row for
  aBN1, FlyWire ID `720575940630907434`): JO-CE drives aBN1 to **50.77 Hz**
  (s.d. 1.36); JO-F drives aBN1 to only **1.23 Hz** (s.d. 0.92) — i.e. despite
  comparable direct synapse counts, the model predicts a >40-fold difference
  in functional drive. Confirmed by calcium imaging (Fig. 5h, ΔF/F in aBN1,
  n≥5 flies/condition): JO-CE optogenetic activation produces a robust ΔF/F
  transient in aBN1, JO-F activation does not.
- **Type** — perturbation.
- **Method (computational)** — JO-CE (69 IDs, listed in T-SHIU-9) and JO-F
  (60 IDs, listed in T-SHIU-9) activated as separate populations at 150 Hz
  (part of a 20–220 Hz sweep, Fig. 5g); aBN1 firing read out per population.
- **Method (experimental)** — dual binary expression (LexA/LexAop +
  GAL4/UAS) to express CsChrimson in JO-CE- or JO-F-specific driver lines
  and GCaMP6 in aBN1 in the same fly; 590 nm 2 ms light pulses; ΔF/F imaged
  in an aBN1-specific ROI.
- **Observation model** — computational: mean firing over 30×1000 ms runs
  per population at 150 Hz; experimental: ΔF/F time course, qualitative
  robust-vs-absent comparison (no single P-value given for this specific
  panel in the text we extracted).
- **Conditions** — as per general grooming-circuit imaging setup; specific
  fly age/sex not restated separately for this panel beyond the general
  female/3–5-day convention used throughout.
- **Source** — main text p. 216, Fig. 5g–h; Supplementary Table 8 (MOESM2
  workbook, sheet "Supp Table 8 JO-CE and JO-F fir[ing]"); Supplementary
  Table 10 row 10.
- **Confidence** — high; the 50.77 vs. 1.23 Hz values were read directly
  from the supplementary spreadsheet's aBN1 row, and the qualitative
  calcium-imaging confirmation is stated plainly in the main text.

---

### Untested / model-only prediction (explicitly flagged as not yet validated)

The paper reports one further grooming-circuit manipulation that is
**explicitly stated as not experimentally tested** and therefore is *not*
part of the 164/91% figure — recorded here separately because it is exactly
the kind of causal, falsifiable prediction this project wants, just with the
"observed" side still empty:

- **Prediction**: JO-F neurons fail to robustly activate aBN1 (T-SHIU-11)
  because three putative inhibitory interneurons
  (`720575940636066222, 720575940609957315, 720575940624986407`) sit
  directly downstream of JO-F and synapse directly onto aBN1. Computationally
  silencing all three while activating JO-F (20–220 Hz sweep) permits JO-F
  to drive aBN1 robustly (Extended Data Fig. 4c, Supplementary Table 8-
  adjacent data referenced as "Figure_s5" in `figures.ipynb`'s
  `JON_F_Three_Silenced` experiment).
- Main text, p. 216: "Computational silencing of these three neurons
  permits JO-F neurons to activate aBN1, **but this remains to be tested
  empirically**."
- This is a ready-made, concrete, already-specified computational
  perturbation (3 named FlyWire IDs to silence + a named population to
  activate + a named readout neuron) that has no experimental ground truth
  yet — worth flagging for anyone using this project's model to generate
  new falsifiable predictions rather than only fit old ones.

---

### T-SHIU-12  Model sensitivity to the free parameter and to modelling assumptions

- **Quantity** — how much the 164-prediction accuracy changes when the
  model's one free parameter or its categorical assumptions are perturbed,
  reported by the authors as a robustness/sensitivity check rather than a
  fitting target per se — included here because it directly bounds how
  tightly a re-implementation needs to match `w_syn` to reproduce the
  paper's headline accuracy.
- **Value** (Supplementary Table 11, summarized in Methods p. 11):

  | Perturbation | Agreement with default-model predictions | Resulting accuracy (of 164) |
  |---|---|---|
  | Default (`w_syn = 0.275 mV`) | — | 91% |
  | `w_syn` − 30% | 90.2% | 85% |
  | `w_syn` + 30% | 95% | 88% |
  | Inhibitory:excitatory weight ratio − 50% | 95% | 88% |
  | Inhibitory:excitatory weight ratio + 50% | 96% | 89% |
  | Glutamate assumed excitatory (default: inhibitory) | not separately quantified as a single % | eliminates the bitter/Ir94e-are-inhibitory result entirely; raises the SEZ-screen false-positive rate from 1% to 16% |

  Sensory input was re-scaled to compensate when `w_syn` changed (e.g.
  increased sugar-GRN firing to compensate for decreased `w_syn`), so this
  is a test of qualitative robustness, not literally the same stimulus at a
  different gain.
- **Type** — perturbation (meta-level: repeats the same 164 perturbations
  under 5 alternative parameterizations).
- **Method** — identical LIF/Brian2 protocol and identical 164-prediction
  comparison set, with one parameter changed at a time (never combined).
- **Observation model** — "% agreement with default" = fraction of the 164
  predictions unchanged between the perturbed and default model (not
  necessarily correct — just unchanged); "resulting accuracy" = fraction of
  164 still matching real data under the perturbed model.
- **Conditions** — computational only.
- **Source** — Methods, "Assessment of model robustness to parameters and
  assumptions," p. 11; Supplementary Table 11 (A–F) (MOESM2 workbook; we
  read the sheet names and header rows but did not extract the full
  per-prediction row-by-row detail for this table — see below).
- **Confidence** — high for the six summary percentages (quoted directly
  from Methods prose); we did not independently recompute them from
  Supplementary Table 11's raw rows.

---

## What we could not find / did not extract (please read before assuming completeness)

- **We did not obtain a single flat list of all 164 individual predictions
  in one place.** No such list exists as a single table in the
  supplement — the 164 are spread across Supplementary Tables 1–2 (sugar,
  ~24 predictions), 3 (SEZ screen, 106 predictions — fully extracted, see
  T-SHIU-6), 4 (taste interactions, partially extracted via T-SHIU-7's
  figure-legend numbers only, not the full interaction-firing-rate table),
  5–6 (water, ~21 predictions), and 7–8 (grooming, ~7 predictions), with
  Table 10 giving only the *category*-level counts (which we did fully
  extract and reproduce in T-SHIU-1). We are confident the **106 SEZ
  split-GAL4 predictions (T-SHIU-6) are complete and exact**; the remaining
  ~58 are accurately summarized by category but not itemized as 58
  individual rows anywhere in the source material we found — Supplementary
  Tables 2 and 5 (10–11 rows each) get us most of the way, but the
  category totals in Table 10 (14, 10, 10, 11) don't all cleanly divide into
  named rows we could locate (noted individually in T-SHIU-5 and T-SHIU-8).
- **Supplementary Table 4** (taste-modality interaction firing rates,
  neurotransmitter breakdown for 613 taste-responsive neurons) was opened
  (confirmed to exist, ~1000 declared rows) but not extracted row-by-row;
  we relied on the pre-computed Venn-diagram numbers already stated in the
  Fig. 1h/3f/4 legends instead.
- **Supplementary Tables 1A/1B/1C and 6A/6B/6C** (the raw per-neuron firing
  curves underlying the Fig. 1d–f and Fig. 4a–c heatmaps, ~1000 rows each,
  mostly anonymous FlyWire IDs without assigned names) were not extracted —
  these are the source data for population-level heatmaps rather than
  individual named predictions, and at this depth mining every row did not
  seem to add fitting targets beyond what the named-neuron tables (2, 3, 5)
  already give.
- **Supplementary Tables 7B/7C/7D/7E in full** (300-row grooming
  activation/silencing matrices): we scanned 7B and 7C exhaustively for
  nonzero rows (successfully finding aBN1, aDN1, aDN2 and the two weak
  <2 Hz contributors — see T-SHIU-9/10) but did not exhaustively recompute
  the >20%-decrease silencing threshold crossing for 7D/7E against all 300
  rows; the specific named results we report there (aBN1, aDN2, "a
  descending BN2-class member") are quoted from the main text rather than
  independently re-derived from the raw matrix.
- **bioRxiv preprint full text** was not independently re-fetched (HTTP 429
  on the one attempt) — not needed in the end, since the published Nature
  version (fetched successfully via the Oxford ORA mirror) is the version
  that contains the 164/91% headline figure and all the supplementary
  tables used throughout this file. The preprint's title and abstract
  differ slightly (mechanosensory/grooming content was added between
  preprint and publication per the GitHub README), so numbers in this file
  should not be assumed to appear in the original 2023 preprint.
- **Raw spike-time archive** (Edmond/MPDL, DOI 10.17617/3.CZODIW,
  described by the authors as "several GB") was not downloaded — the
  Supplementary Excel tables already contain the pre-aggregated firing
  rates needed for every prediction comparison in this file, so the raw
  per-spike data was judged out of scope for a "predictions" catalogue.
- **"Schwarz et al., 2017"** (cited in Supplementary Table 10 row 1 as the
  real-world ground truth for the ipsi/contralateral MN9 asymmetry,
  T-SHIU-4) does not appear in this paper's own numbered reference list and
  we could not locate/verify it independently; treat that one citation as
  unverified.
- **MN6, MN8, MN11 FlyWire IDs**: the paper states computational sugar-GRN
  activation drives "MNs 6, 8, 9 and 11" (Fig. 1c), and MN6's ID
  (`720575940628826128`, right side) turned up incidentally in Supplementary
  Table 1D, but we did not locate FlyWire IDs for MN8 or MN11 in any of the
  sources searched.
- We did **not** attempt to independently re-run the model (e.g. via Google
  Colab / the repo's `example.ipynb`) to verify any of the reported firing
  rates by simulation — everything in this file is transcribed/recomputed
  from the authors' own published numbers and files, not independently
  regenerated from the connectome.
