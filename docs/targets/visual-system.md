# Optic lobes and visual processing

Scope: fitting targets for the early visual system — photoreceptors, lamina
(L1–L3), medulla ON/OFF pathway neurons (Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4,
Tm9), the elementary motion detectors T4/T5, and the perturbation/behavioural
literature that constrains all of the above.

## Why collect this, given the model can't represent it

The early visual system (photoreceptors through at least L1–L3, and very
likely through T4/T5 too — see T-VIS-010) is **non-spiking**: these neurons
communicate with graded, continuous membrane-potential changes, not action
potentials. A leaky integrate-and-fire (LIF) network has no graded-potential
mode; it can only threshold into a spike or stay silent. That is a structural
mismatch, not a tuning problem, and no amount of parameter fitting closes it.

We collect these targets anyway because (1) they quantify *how wrong* a
spiking approximation is, which is itself useful information, and (2) this is
the best-documented case anywhere in the fly connectome-modeling literature of
a model validated end-to-end against cell-type-resolved physiology, so the
comparison methodology and the experimental numbers are both worth having on
file even for an architecture that cannot fully use them.

**Relationship to `prior-validation.md`.** That file already covers FlyVis's
own *aggregate* accuracy claims (32/32 ON/OFF match, the 9-untuned/12-tuned
direction-selectivity classification, the r=0.60 task-performance-vs-biology
correlation, the named Tm4 polarity failure) — T-PRIOR-003 through T-PRIOR-005.
**Do not re-derive those numbers from this file.** What follows instead is the
per-cell-type *experimental* physiology — the roughly two dozen primary papers
that FlyVis (and the wider field) validated against — reusable independently
of whether FlyVis itself got each one right. FlyVis's own units, for context,
are continuous graded dynamical variables (leaky linear-nonlinear elements),
not spiking units either — which is one reason it could match this data at
all; this is background knowledge about the architecture, not a re-statement
of its accuracy scores.

## Quick reference: spiking or graded, per cell type

| Cell type(s) | Status | Basis |
|---|---|---|
| Photoreceptors R1–R8 | **GRADED** | Directly recorded as graded voltage throughout (Juusola & Hardie 2001; explicitly called "nonspiking" in Weckström-lab modelling work, PMID 15636117) |
| Lamina L1–L5 | **GRADED** | Classic and consistently reported as graded (Hardie 1989; Rister 2007; Freifeld 2013; Silies 2013) |
| Medulla Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9 | **GRADED** | Patch-clamp shows smooth graded (de)polarization, no spikes reported (Behnia 2014 for Mi1/Tm3/Tm1/Tm2; inferred for Mi4/Mi9/Tm4/Tm9 by consistency with the rest of the medulla and with Strother 2017/Serbe 2016, not independently re-confirmed per cell type) |
| T4, T5 | **GRADED** | Two-photon voltage imaging (ArcLight) shows continuous, graded membrane potential, not discrete spikes (Mishra et al. 2023, T-VIS-010) — but see caveat there about how most other T4/T5 literature actually measures *calcium*, not voltage |
| L1/L2/L3-associated wide-field tangential cells (HS, VS) | **GRADED, dominant** | Recorded as graded "peak-to-peak" potentials in the behavioural-state literature (Chiappe 2010, Maimon 2010); the broader Diptera literature also reports small superimposed Na⁺ spikelets in some LPTCs, so treat as graded-dominant rather than purely graded — not resolved further in this pass |
| LPLC2 / other lobula(-plate) looming-selective columnar neurons | **Not confirmed** | Studied by calcium imaging and whole-cell recording; Klapoetke et al. 2017 does not explicitly classify it either way |
| Giant Fiber descending neuron | **SPIKING** | Classic, well-established fact about the fly escape circuit (general knowledge, not re-confirmed against a primary source in this pass) |

---

## Perturbations

### T-VIS-001 L1 vs L2 silencing splits ON and OFF optomotor responses
- **Quantity** — optomotor turning response to moving ON (brightness increment) vs OFF (decrement) edges after genetically silencing L1 or L2 synaptic output
- **Value** — blocking L1 output eliminates the behavioural/physiological response to moving ON edges; blocking L2 output eliminates the response to moving OFF edges. Reconstituting photoreceptor input to only L1, or only L2, alone still gives near-normal responses to the corresponding edge type — apparent redundancy resolved by electrical coupling between L1 and L2.
- **Spiking/Graded** — L1, L2 = GRADED
- **Type** — perturbation
- **Method** — genetic synaptic silencing (shibire-ts, temperature-shift block), optomotor turning behaviour to moving gratings, plus intracellular electrophysiology from downstream lobula-plate tangential cells
- **Observation model** — extractor must be able to zero out a single named channel's output and score ON-edge and OFF-edge responses *separately*, not as one combined-contrast metric
- **Conditions** — adult *Drosophila*, tethered, restrictive temperature for shibire-ts block
- **Source** — Joesch M, Schnell B, Raghu SV, Reiff DF, Borst A. "ON and OFF pathways in Drosophila motion vision." *Nature* 468, 300–304 (2010). PMID 21068841
- **Confidence** — high — classic, widely replicated finding; abstract-level extraction only (full text not fetched this pass)

### T-VIS-002 L1/L2/L3/amc-T1 contrast-dependent division of labour
- **Quantity** — contribution of each lamina output channel (L1, L2, L3, amc/T1) to motion-dependent behaviour, and the directional polarity each one carries, as a function of pattern contrast
- **Value** — L1 and L2 together are necessary and largely sufficient for motion-dependent behaviour. At **high** contrast the two are redundant. At **intermediate** contrast they carry opposite directional polarity: L2 mediates front-to-back motion, L1 mediates back-to-front motion. At **low** contrast L1 and L2 become mutually dependent (neither alone suffices). Of the minor pathways: amc/T1 specifically boosts the L1 pathway at intermediate contrast; L3 does not contribute to motion behaviour at all, only to orientation behaviour.
- **Spiking/Graded** — L1, L2, L3 = GRADED
- **Type** — perturbation
- **Method** — genetic silencing of L1, L2, L3, amc/T1 individually and in combination; optomotor behavioural assay swept across contrast levels
- **Observation model** — extractor needs a contrast sweep (not one operating point) with separately scored ON/OFF edge motion, because the L1/L2 division of labour itself changes qualitatively with contrast
- **Conditions** — adult *Drosophila*, tethered walking/optomotor assay
- **Source** — Rister J et al. "Dissection of the peripheral motion channel in the visual system of Drosophila melanogaster." *Neuron* 56(1):155–70 (2007). PMID 17920022
- **Confidence** — high — abstract-level extraction only

### T-VIS-003 L3 silencing: behaviour-specific deficit, not a general one
- **Quantity** — behavioural deficit from silencing L3 alone, vs. L3+L2 together, for (a) optomotor turning and (b) forward-walking speed modulation
- **Value** — L3 silenced alone: **no significant deficit** in turning to rotating gratings/edges, but a deficit in forward-walking speed modulation to back-to-front motion, "particularly at higher contrast frequencies." L3+L2 silenced together: flies show **no turning at all** to a rotating dark edge (L3 is a redundant dark-edge channel with L2). L2+L3 silenced together: "very little modulation of forward walking speed" to front-to-back motion and no detectable slowing to back-to-front motion.
- **Spiking/Graded** — L1, L2, L3 = GRADED
- **Type** — perturbation
- **Method** — shibire-ts synaptic silencing of L3 and L2 alone/combined; two separate behavioural readouts (optomotor turning; forward-walking speed modulation) on a tethered fly on an air-supported ball
- **Observation model** — needs both a turning-behaviour channel and an independent forward-speed-modulation channel, because L3's effect is behaviour-specific — a model that only scores turning will conclude (wrongly) that L3 does nothing
- **Conditions** — adult *Drosophila*, tethered on air-supported ball
- **Source** — Silies M et al. "Modular use of peripheral input channels tunes motion-detecting circuitry." *Neuron* 79(1):111–27 (2013). PMID 23849199, PMC3713415
- **Confidence** — high — full text read via PMC

### T-VIS-004 Columnar medulla cells necessary for HS/VS wide-field motion responses
- **Quantity** — effect of silencing specific columnar medulla input neurons (incl. Mi1) on motion responses of downstream wide-field tangential cells (HS/VS)
- **Value** — silencing the identified columnar input cells is reported to be necessary for normal HS/VS motion responses; qualitative necessity established, but I could not extract an exact percent-reduction figure (paper is not on PMC and only the abstract was read).
- **Spiking/Graded** — Mi1 = GRADED; HS/VS = GRADED-dominant (see quick-reference table)
- **Type** — perturbation
- **Method** — genetic silencing of specific columnar cell types + intracellular recording from HS/VS during grating motion
- **Observation model** — extractor must zero out one named upstream unit and measure the change in one named downstream unit, not a lumped pathway-level effect
- **Conditions** — adult *Drosophila*, in vivo electrophysiology
- **Source** — Schnell B, Raghu SV, Nern A, Borst A. "Columnar cells necessary for motion responses of wide-field visual interneurons in Drosophila." *J Comp Physiol A* 198(5):389–95 (2012). PMID 22411431
- **Confidence** — medium — abstract only; magnitude not found, full text not accessible (no PMC link)

### T-VIS-005 Loom-sensitive lobula neurons are both necessary and sufficient for escape
- **Quantity** — necessity (silencing) and sufficiency (optogenetic activation) of identified loom-sensitive optic-lobe neurons for looming-evoked escape/takeoff behaviour
- **Value** — silencing the identified loom-sensitive neurons reduces escape behaviour; optogenetically activating them is sufficient to trigger escape/jump behaviour even with no looming visual stimulus present. I could not extract the exact behavioural percentage change (only qualitative necessity/sufficiency; full paper not fetched, only the abstract and a partial secondary extraction).
- **Spiking/Graded** — not stated for these neurons; not independently confirmed
- **Type** — perturbation
- **Method** — genetic silencing + optogenetic activation (channelrhodopsin-class tool) of loom-sensitive lobula neurons; behavioural scoring of escape/jump
- **Observation model** — needs an "escape probability" readout drivable purely from one cell type's simulated activity, decoupled from the rest of the visual stimulus, to test the sufficiency claim
- **Conditions** — adult *Drosophila*, tethered or loosely restrained
- **Source** — de Vries SE, Clandinin TR. "Loom-sensitive neurons link computation to action in the Drosophila visual system." *Curr Biol* 22(5):353–62 (2012). PMID 22305754, PMC3298569 (per elink; full text not fetched this pass)
- **Confidence** — medium — abstract-level and partial secondary-extraction only

### T-VIS-006 LPLC2: ultra-selective looming detection via radial motion opponency
- **Quantity** — LPLC2 response selectivity for looming vs. wide-field translational motion, dark vs. bright looming, receptive-field size, and downstream connectivity to the escape circuit
- **Value** — LPLC2 does **not** respond to wide-field motion stimuli that strongly drive T4/T5; it **is** highly responsive to dark looming "across all measured speeds," and only slightly responsive to bright looming. Selectivity arises because each of LPLC2's four cross-shaped dendritic arms is locally direction-selective for *outward* (radial/looming) motion along its own preferred axis, and receives local inhibition selective for the opposing *inward* motion — this radial opponency cancels responses to non-looming wide-field patterns (translation, rotation, uniform luminance change). Individual-LPLC2 receptive field size has an upper bound of **~60°**. The LPLC2 population densely tiles visual space and terminates onto the Giant Fibre descending neuron, which drives the jump-muscle motor neuron.
- **Spiking/Graded** — LPLC2 not explicitly classified (calcium imaging + whole-cell recording used); Giant Fibre = SPIKING (general knowledge, not re-confirmed here)
- **Type** — steady-state (selectivity profile) + dynamic response
- **Method** — in vivo two-photon Ca²⁺ imaging of LPLC2 dendrites/axon under looming, translating, rotating, and luminance-change stimuli; single-cell anatomical tracing; connectivity mapping to the Giant Fibre
- **Observation model** — the selectivity is a *geometric, per-dendritic-arm* comparison of local outward vs. inward motion, not a scalar "looming index" computed after the fact — a model must implement the opponency structurally (per-arm local direction preferences that are compared against each other) to reproduce this, not just tune a single looming-detector neuron's overall gain
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging, tethered
- **Source** — Klapoetke NC et al. "Ultra-selective looming detection from radial motion opponency." *Nature* 551, 237–241 (2017). PMID 29120418, PMC7457385 (full text read)
- **Confidence** — high for the selectivity/receptive-field numbers (direct quotes from full text); **low** for exact behavioural escape-rate percentages under LPLC2 silencing — the paper's Extended Data Fig. 3f reports this only graphically (N > 130 flies/condition, 2,811 flies total), and I could not extract a numeric percentage from the rendered text

### T-VIS-007 LPLC2 silencing reduces takeoff and abolishes Giant Fibre spiking (numbers not confirmed)
- **Quantity** — takeoff rate and Giant Fibre (GF) spike occurrence in response to looming, with vs. without LPLC2 synaptic output
- **Value** — "Silencing LPLC2 with TNT or Kir reduced overall takeoff rates to looming stimuli... and almost completely abolished GF [spiking]" — this is a paraphrase captured from a search snippet, not a verified direct quote; exact percentages were not obtained.
- **Spiking/Graded** — LPLC2 = not confirmed (presumed graded by consistency with other lobula columnar neurons); Giant Fibre = SPIKING
- **Type** — perturbation
- **Method** — genetic silencing (TNT, Kir2.1) of LPLC2 + high-speed videography of takeoff + electrophysiological recording of GF spikes during looming
- **Observation model** — same as T-VIS-006, plus an explicit GF-spike-count readout as the final common pathway
- **Conditions** — adult *Drosophila*, tethered/restrained, looming stimulus
- **Source** — Ache JM et al., "Neural Basis for Looming Size and Velocity Encoding..." *Curr Biol* (2019), found via a ScienceDirect search snippet (S0960982219301381). PMID not independently looked up this pass.
- **Confidence** — low — retrieved only as a search-engine snippet/paraphrase, not the primary abstract or full text. Treat this entry as a pointer to go verify, not as a load-bearing number.

### T-VIS-008 L1+L2 and Foma1 silencing reduce looming jump odds (preprint, numbers given)
- **Quantity** — jump-escape odds ratio (permissive vs. restrictive temperature for shibire-ts block) for flies with L1+L2 silenced, or with the looming-sensitive lobula-plate tangential neuron "Foma1" silenced, relative to control
- **Value** — L1+L2 silenced: jump odds ratio **0.067** (95% CI 0.009–0.494, p = 8.6×10⁻⁴); a logistic model on the same data gives **0.025** (CI 0.003–0.187, p = 8.6×10⁻⁷). Foma1 silenced: jump odds ratio **0.024** (CI 0.003–0.180, p = 6.0×10⁻⁷). Control flies show no temperature dependence of jump odds (p = 0.20). Baseline short-mode escape-jump fraction in control flies ≈ **19%** (n = 233 jump trials).
- **Spiking/Graded** — L1, L2 = GRADED; Foma1 = not confirmed
- **Type** — perturbation
- **Method** — shibire-ts genetic silencing (temperature-shift), dark-looming-square and reverse-contrast (light-square-on-dark) visual stimuli, funnel/holder behavioural assay, logistic regression on jump probability
- **Observation model** — the temperature-shift silencing logic itself isn't directly reproducible in a static model, but the *ratio* of jump probability with vs. without a given cell type's output is directly comparable to a model's silenced-vs-intact output ratio
- **Conditions** — adult *Drosophila*, funnel/holder assay, temperature-inducible silencing
- **Source** — bioRxiv 2019.12.26.883587, "Neuronal ON/OFF Motion Detection Circuits Underlying Looming-Evoked Escape Behavior in Drosophila." **This is an unreviewed preprint** — I did not independently confirm authorship, publication status, or read the methods beyond the search snippet.
- **Confidence** — medium — numbers are direct quotes from the preprint text via a search snippet, but the source itself is unreviewed and only partially read

---

## T4 / T5 direction selectivity and their inputs

### T-VIS-009 T4/T5 cardinal direction map and ON/OFF segregation
- **Quantity** — directional tuning of T4 vs. T5 subtypes, contrast-polarity segregation, velocity/temporal-frequency tuning peak, and tuning width
- **Value** — T4 responds selectively to moving ON edges, T5 selectively to moving OFF edges (confirmed both by imaging and by silencing: blocking T4 output selectively compromises turning to ON edges, blocking T5 compromises OFF-edge turning). Four subtypes each (T4a–d, T5a–d) are tuned to the four cardinal directions (front-to-back, back-to-front, upward, downward) and terminate in one of four lobula-plate layers, matched between T4 and T5 by direction. **Velocity/temporal-frequency tuning:** T4 peaks at a stimulus velocity of 30°/s, corresponding to a temporal frequency of **1 Hz**; T5 shows a similar dependency with a peak at essentially the same temporal frequency — "no obvious difference in velocity tuning between T4 and T5." **Directional tuning width** (T4-specific driver): half-width of roughly **60–90°**, with peak responses in each of the four lobula-plate layers offset by 90° from each other; no detectable calcium decrease for motion in the null (opposite-to-preferred) direction, i.e. a strongly one-sided response at this stage rather than push-pull.
- **Spiking/Graded** — T4, T5 = GRADED (see T-VIS-010 for the important caveat that almost all of this is a *calcium* signal, not membrane voltage)
- **Type** — dynamic response (direction/velocity tuning) + perturbation (silencing sub-component)
- **Method** — in vivo two-photon Ca²⁺ imaging (GCaMP5/GCaMP6f, R42F06 driver) of T4/T5 axon terminals in the lobula plate; moving sinusoidal gratings at 12 directions and velocities spanning two orders of magnitude; shibire-ts silencing of T4 or T5 output plus recording from postsynaptic lobula-plate tangential cells and tethered-walking turning behaviour
- **Observation model** — extractor must (a) apply the same voltage-to-calcium-like transform as T-VIS-010 before computing a tuning curve from a simulated graded signal, (b) convert velocity to temporal frequency using the model's own photoreceptor spacing (~5° in *Drosophila*), and (c) use ON-only / OFF-only edge stimuli, not combined contrast
- **Conditions** — adult *Drosophila*, in vivo, tethered, two-photon imaging
- **Source** — Maisak MS et al. "A directional tuning map of Drosophila elementary motion detectors." *Nature* 500, 212–216 (2013). PMID 23925246. **Not available on PMC** (elink returned no `pubmed_pmc` link this pass). The velocity/tuning-width numbers above were extracted from a co-author-archived copy of the paper text (LMU Munich repository) rather than from the typeset Nature version, and are qualitatively corroborated by later citing papers (e.g. Fisher et al. 2015; Zhao et al. 2022, PMC10169962).
- **Confidence** — high for the qualitative ON/T4–OFF/T5 segregation and cardinal-direction map (extremely widely replicated); **medium** for the specific 1 Hz peak and 60–90° width numbers (single-source extraction, not cross-checked against the original typeset figures)

### T-VIS-010 Voltage-to-calcium transformation inflates T4's apparent direction selectivity
- **Quantity** — direction selectivity index (DSI) of T4 measured via a genetically encoded **voltage** indicator (ArcLight) vs. a **calcium** indicator (GCaMP6f), and the transform between them
- **Value** — calcium-signal DSI is reported as "significantly higher" than voltage-signal DSI in Mishra et al.'s own paired recordings. A companion/citing paper in the same *J Neurosci* issue, doing the same ArcLight-vs-GCaMP6f comparison, reports specific values: DSI ≈ **0.4** for ArcLight (voltage) vs. DSI ≈ **0.9** for GCaMP6f (calcium) — **I was not able to fully confirm whether these exact numbers belong to Mishra et al. itself or to the companion paper**; treat the 0.4/0.9 figures as indicative, not confirmed, pending a full-text read of PMID 36849417. The qualitative direction of the effect (calcium DSI >> voltage DSI) is stated directly in Mishra et al.'s own abstract and is high-confidence. Mishra et al. fit an explicit cascade — thresholding, temporal filtering, a static nonlinearity — that reproduces the calcium response from the recorded voltage response.
- **Spiking/Graded** — T4 = GRADED. This entire paper's premise is that T4's membrane potential is a continuous graded signal that is then nonlinearly transformed into the calcium signal that essentially all other T4/T5 studies in this file (Maisak 2013, Arenz 2017, Strother 2017, Klapoetke 2017) actually report.
- **Type** — dynamic response (transformation characterization)
- **Method** — paired in vivo two-photon imaging of ArcLight and GCaMP6f in T4 dendrites/axon of female *Drosophila*, same stimulus set; nonlinear cascade model fit (threshold + temporal filter + static nonlinearity) mapping voltage → calcium
- **Observation model** — **this is the single most important observation-model note in this file for T4/T5.** Because nearly every T4/T5 target above and below is a calcium measurement, comparing a model's raw graded-voltage DSI (or response amplitude) directly against a reported calcium DSI will systematically read as too low. An extractor must apply an equivalent threshold + temporal-filter + static-nonlinearity cascade to the model's simulated voltage trace before comparing to any calcium-based T4/T5 target in this file.
- **Conditions** — adult female *Drosophila*, in vivo two-photon, head-fixed
- **Source** — Mishra A, Serbe-Kamp E, Borst A, Haag J. "Voltage to Calcium Transformation Enhances Direction Selectivity in Drosophila T4 Neurons." *J Neurosci* 43(14) (2023). PMID 36849417. The 0.4/0.9 DSI values were found via a search snippet from jneurosci.org/content/jneuro/43/14/2497 during this same search, and may belong to a companion paper rather than to Mishra et al. itself.
- **Confidence** — medium overall — high confidence on the qualitative claim (direct quote from the target paper's own abstract), low confidence on the specific 0.4/0.9 numbers (sourcing ambiguity, not independently resolved)

### T-VIS-011 Mi1/Tm3 and Tm1/Tm2 as delay-line pairs (Hassenstein-Reichardt inputs)
- **Quantity** — response latency (time-to-peak) and onset/offset amplitude asymmetry of Mi1, Tm3 (ON pathway) and Tm1, Tm2 (OFF pathway) to contrast steps
- **Value** — **Mi1** peak response time: **71 ms** (SEM 3.8 ms) after a contrast change; **Tm3**: **53 ms** (SEM 5.2 ms) — an **18 ms** difference, with Mi1 delayed relative to Tm3. **Tm1** peak response time: **56 ms** (SEM 3.8 ms); **Tm2**: **43 ms** (SEM 2.7 ms) — a **13 ms** difference, Tm1 delayed relative to Tm2. Offset (opposite-contrast) response as a fraction of the onset (preferred-contrast) response: **Mi1 11%** (SEM 3.5%) vs. **Tm3 36.6%** (SEM 7.1%) — Mi1 is more rectified/ON-selective than Tm3. **Tm1 26.1%** (SEM 3.8%) vs. **Tm2 17.7%** (SEM 2.3%) — Tm2 more rectified than Tm1. Feeding these measured delay and rectification values into a Hassenstein-Reichardt correlator model reproduces the independently measured ~1 Hz peak temporal-frequency tuning (T-VIS-009) and ON/OFF edge specificity of the downstream motion detectors.
- **Spiking/Graded** — Mi1, Tm3, Tm1, Tm2 = GRADED (patch-clamp shows smooth graded (de)polarization, no spikes reported)
- **Type** — dynamic response (temporal filtering) + steady-state (rectification ratio)
- **Method** — in vivo whole-cell patch-clamp of membrane potential in Mi1, Tm3, Tm1, Tm2 to full-field contrast steps; HRC model constructed from the fitted delay + rectification parameters
- **Observation model** — extractor must fit peak-latency and offset/onset ratio from a simulated **step** response (not a moving grating) using genuinely graded membrane-potential-like output, matching the patch-clamp recording modality
- **Conditions** — adult *Drosophila*, in vivo whole-cell patch-clamp
- **Source** — Behnia R, Clark DA, Carter AG, Clandinin TR, Desplan C. "Processing properties of ON and OFF pathways for Drosophila motion detection." *Nature* 512, 427–430 (2014). PMID 25043016, PMC4243710 (full text read)
- **Confidence** — high — direct quotes from full text

### T-VIS-012 Direction selectivity emerges in T4 dendrites, not in its major inputs
- **Quantity** — direction selectivity of the major T4-input neuron types (highest-synapse-count inputs, i.e. Mi1, Mi4, Mi9, Tm3), individually, before vs. after the T4 dendrite
- **Value** — none of the major input neuron types tested are themselves directionally selective by calcium imaging; direction selectivity first arises in the T4 dendrites, downstream of all of them. Silencing each input type individually identifies which are necessary for T4 direction selectivity and for ON-motion behavioural responses. Single-cell photoactivation maps the sign (excitatory/inhibitory) of each input-to-T4 connection. The overall computational architecture is described as "a hybrid of classic theoretical models" (i.e., not a pure two-input Hassenstein-Reichardt correlator, nor a pure Barlow-Levick model).
- **Spiking/Graded** — Mi1, Mi4, Mi9, Tm3 = GRADED (consistent with T-VIS-011); T4 = GRADED (T-VIS-010)
- **Type** — steady-state (non-selectivity of inputs) + perturbation (silencing)
- **Method** — two-photon Ca²⁺ imaging of individually labelled input types; targeted silencing of each input type with behavioural/T4-calcium readout; single-cell photoactivation for synaptic sign
- **Observation model** — a strong structural constraint: the model must show **zero** direction selectivity for Mi1/Mi4/Mi9/Tm3 individually under the same moving-grating stimulus used for T4, with selectivity appearing only at the T4 unit — this rules out any model design that pre-bakes directional tuning into the input layer
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging + optogenetics
- **Source** — Strother JA et al. "The Emergence of Directional Selectivity in the Visual Motion Pathway of Drosophila." *Neuron* 94(1):168–182 (2017). PMID 28384470. **Not on PMC** (no `pubmed_pmc` link found).
- **Confidence** — medium — abstract-level detail only; specific effect sizes and the exact excitatory/inhibitory sign of each connection were not extracted this pass

### T-VIS-013 Tm1/Tm2/Tm4/Tm9 as T5's four OFF-pathway inputs
- **Quantity** — contribution of each of T5's four major input neuron types to T5's OFF-direction-selective response
- **Value** — T5 is confirmed as the first direction-selective stage within the OFF pathway (none of its four inputs are individually direction-selective — consistent with T-VIS-012's finding for the ON/T4 side). The four input types (Tm1, Tm2, Tm4, Tm9) provide "an array of spatiotemporal filters" to T5 with distinct dynamics from one another. Silencing them in various single and combinatorial patterns shows that **all four** are involved in OFF motion detection "to varying degrees" — the classical two-input correlator model is described as insufficient here; at least four filtered input lines converge on T5.
- **Spiking/Graded** — Tm1, Tm2, Tm4, Tm9 = GRADED
- **Type** — steady-state (filter diversity) + perturbation (combinatorial silencing)
- **Method** — two-photon Ca²⁺ imaging of Tm1/Tm2/Tm4/Tm9; genetic silencing of synaptic output singly and in combination; T5 calcium readout
- **Observation model** — extractor needs at least four separably-filtered OFF-pathway input channels feeding a T5 unit, each independently silenceable, to compare against the combinatorial-silencing results
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging
- **Source** — Serbe E, Meier M, Leonhardt A, Borst A. "Comprehensive Characterization of the Major Presynaptic Elements to the Drosophila OFF Motion Detector." *Neuron* 89(4):829–841 (2016). PMID 26853306. **Not on PMC.**
- **Confidence** — medium — abstract-level only; per-cell-type contribution magnitudes not extracted. **Note:** this is also the paper underlying FlyVis's own named failure case (Tm4 polarity predicted wrong — see `prior-validation.md` T-PRIOR-005); the real Tm4 physiology reported here is the ground truth FlyVis itself got wrong, which makes independent access to this paper's actual Tm4 numbers a high-value follow-up

### T-VIS-014 Tm2 and L4 are direction-unselective but necessary for the OFF response
- **Quantity** — direction selectivity and behavioural necessity of Tm2 and L4 for downstream OFF-edge responses
- **Value** — Tm2 and L4 both respond to moving OFF edges with an **increase** in activity, in a direction-**un**selective manner (consistent with T-VIS-013: selectivity hasn't emerged yet at this stage). Silencing either Tm2 or L4 output **completely abolishes** the OFF-edge response of downstream lobula-plate tangential cells.
- **Spiking/Graded** — Tm2, L4 = GRADED
- **Type** — perturbation + steady-state
- **Method** — Ca²⁺ imaging of Tm2, L4; shibire-ts silencing + electrophysiological recording from downstream tangential cells during moving OFF-edge stimuli
- **Observation model** — a clean zero-out test: silencing either unit in the model should drop the downstream OFF response to baseline noise, not partially reduce it
- **Conditions** — adult *Drosophila*, in vivo
- **Source** — "Neural circuit components of the Drosophila OFF motion vision pathway." *Curr Biol* 24(4):385–92 (2014). PMID 24508173. Author list not independently confirmed this pass (title/journal/year/PMID confirmed via efetch; likely a Borst-lab paper by continuity with the OFF-pathway literature above, but I did not verify the byline).
- **Confidence** — high for the quoted findings (direct abstract quotes); medium on attribution details (author list unverified)

---

## Lamina: L1, L2, L3

### T-VIS-015 L2 receptive field structure and light-response polarity
- **Quantity** — L2 spatial receptive-field structure (center/surround) and response polarity relative to light
- **Value** — center radius **3–5°**; an antagonistic surround peaking **~10°** from center and extending to **15° or more**. Response sign is *spatially context-dependent, not fixed*: "L2 cells with RF centers directly under the stimulus **hyperpolarized** to light, while cells at the periphery of the screen... **depolarized**." At the axon terminal: Ca²⁺ **decreases** with light increments and **increases** with light decrements (consistent with center hyperpolarization to ON). Both ON and OFF response components are biphasic; the two differ mainly in **amplitude**, not kinetics — no separate ms-scale time constants are given for the two signs.
- **Spiking/Graded** — L2 = GRADED
- **Type** — steady-state (receptive field) + dynamic response (biphasic kinetics, qualitative only)
- **Method** — two-photon Ca²⁺ imaging of L2 axon terminals in the medulla; small-spot and annulus stimuli to map center vs. surround; genetic/pharmacological implication of GABAergic lateral inputs (partly presynaptic)
- **Observation model** — L2 cannot be modelled as a point sensor: it needs a narrow, directly-driven center (3–5°) plus a much wider antagonistic surround (~10–15°) before its polarity even makes sense — a point-input L2 unit will get the periphery sign-reversal wrong by construction
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging
- **Source** — Freifeld L, Clark DA, Schnitzer MJ, Horowitz MA, Clandinin TR. "GABAergic lateral interactions tune the early stages of visual processing in Drosophila." *Neuron* 78(6):1075–89 (2013). PMID 23791198, PMC3694283 (full text read)
- **Confidence** — high — direct quotes from full text

### T-VIS-016 L3 has a ~3x slower filter than L1/L2/L4, and is rectified
- **Quantity** — L3's temporal filter decay time relative to L1/L2/L4, and its rectification (gain asymmetry between ON and OFF)
- **Value** — L1, L2, and L4 linear filters all decay to baseline in **under 400 ms**. L3's filter takes "almost three times as long to decay to baseline," i.e. roughly ~1.2 s by extension of that ratio — stimulus features hundreds of ms in the past still contribute to the current L3 signal. Unlike L1/L2/L4 (similar gain to increments and decrements), **L3 is rectified**, with higher gain for contrast **decrements** than increments.
- **Spiking/Graded** — L1, L2, L3, L4 = GRADED
- **Type** — dynamic response (filter time course) + steady-state (rectification)
- **Method** — linear filter estimation (reverse correlation) from two-photon Ca²⁺ imaging responses to a defined/white-noise-like contrast stimulus, run in parallel for L1, L2, L3, L4
- **Observation model** — the ~3x figure is a *ratio to L1/L2/L4 measured the same day/same method*, not a standalone absolute time constant — extractor should fit all four lamina cell types' filters from the same simulated stimulus and compare the ratio, not just L3's number in isolation
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging
- **Source** — Silies M et al., *Neuron* 79(1):111–27 (2013). PMID 23849199, PMC3713415 (full text read)
- **Confidence** — medium — the ~3x decay-time ratio is a direct quote (high confidence); a secondary numeric detail (R² = 93.4 / 94.8 for increment/decrement filter fits) surfaced during extraction but reads like a fit-quality statistic rather than a gain magnitude and is very likely a mis-parse of the source figure — **do not use those two numbers without checking the original paper**

### T-VIS-017 Lamina monopolar cells themselves are not ON/OFF selective
- **Quantity** — whether L1–L5 themselves show ON/OFF (light-increment vs. decrement) selectivity, vs. the immediately downstream medulla neurons
- **Value** — LMCs (L1–L5) are confirmed **not** responsible for light-on/light-off selectivity — at the LMC stage, responses are not yet split into separate rectified ON and OFF channels. Prominent ON/OFF selectivity first appears one synapse downstream, in specific medulla layers associated with the L1 and L2 pathways respectively, and specifically in **Mi1** (ON-selective) and **Tm1** (OFF-selective) among the cells examined.
- **Spiking/Graded** — L1–L5 = GRADED; Mi1, Tm1 = GRADED
- **Type** — steady-state (negative result for LMCs; positive result for Mi1/Tm1)
- **Method** — two-photon Ca²⁺ imaging, pan-neural and cell-type-specific, across medulla layers, to ON/OFF flash and moving-edge stimuli
- **Observation model** — directly relevant to FlyVis's own stated limitation (their ON/OFF metric "cannot capture" R1–R8, L1, L2 because these are "unrectified," per `prior-validation.md`): an extractor must **not** force a rectified ON/OFF label onto a simulated L1–L5 unit, because the real cells don't carry one — only compute contrast-selectivity metrics starting at Mi1/Tm1 and downstream
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging
- **Source** — "Direct observation of ON and OFF pathways in the Drosophila visual system." *Curr Biol* (2014). PMID 24704075. Author list not confirmed this pass.
- **Confidence** — medium — clear abstract-level statement; full text not fetched, so magnitude/statistics behind the claim are not verified

---

## Photoreceptors

### T-VIS-018 Histamine is a sign-inverting (inhibitory) neurotransmitter at the first visual synapse
- **Quantity** — postsynaptic LMC response to the photoreceptor neurotransmitter, histamine
- **Value** — LMCs respond to light with a rapid, chloride-mediated **hyperpolarization**, reproducible by direct application of histamine — establishing histamine as an inhibitory, sign-inverting transmitter (photoreceptor depolarizes to light → releases histamine → LMC hyperpolarizes to light).
- **Spiking/Graded** — photoreceptors = GRADED; LMCs = GRADED
- **Type** — steady-state (synaptic pharmacology / sign)
- **Method** — isolated large monopolar cell (LMC) preparation, patch/voltage clamp, iontophoretic or bath histamine application, ligand-gated Cl⁻ channel characterization
- **Observation model** — the ground-truth sign inversion any model must reproduce **structurally**: the photoreceptor→L1/L2/L3 connection must be inhibitory (sign-flipping), not the naive excitatory default a generic feedforward network might assume — this is a wiring-sign target, not a tuning target
- **Conditions** — blowfly (*Calliphora*), isolated LMCs — not *Drosophila* directly, but the same mechanism is confirmed in *Drosophila* by T-VIS-019
- **Source** — Hardie RC. "A histamine-activated chloride channel involved in neurotransmission at a photoreceptor synapse." *Nature* 339, 704–706 (1989). PMID 2472552
- **Confidence** — high — foundational, extensively replicated

### T-VIS-019 Drosophila histamine receptors (ort/hclA, hclB): channel biophysics and null-mutant phenotypes
- **Quantity** — role of the two *Drosophila* histamine-gated Cl⁻ channel genes at/near the photoreceptor-LMC synapse; effect of null mutants on the electroretinogram (ERG)
- **Value** — **ort/hclA** null mutants **abolish** the ERG synaptic on/off transients entirely (i.e., abolish the LMC-driven signal) — this is the receptor actually expressed **in LMCs**. hclA homomeric channel: histamine EC₅₀ = **25 µM**; single-channel conductances ≈ **25, 40, 60 pS** (the 60 pS state strongly voltage-dependent). **hclB**, by contrast, is expressed only in lamina **glia**, not in LMCs; hclB null mutants show ERG "on" transients **approximately two-fold enhanced**, with LMC intracellular recordings showing **slower kinetics** — i.e. glial hclB normally shapes/speeds the LMC response via a non-neuronal pathway. hclB homomers: EC₅₀ = **14 µM**; heteromeric hclA/hclB: EC₅₀ = **1.2 µM**; hclB conductance ≈ **4 pS**.
- **Spiking/Graded** — photoreceptors, LMCs = GRADED
- **Type** — steady-state (receptor pharmacology) + perturbation (null mutants)
- **Method** — heterologous expression (*Drosophila* S2 cells) + patch clamp for EC₅₀/conductance; in vivo ERG and LMC intracellular recording for mutant phenotypes
- **Observation model** — the ~2-fold ERG enhancement in hclB mutants is a usable perturbation number, but it reflects a **glial feedback pathway that a photoreceptor→LMC-only model cannot represent at all** — flag this explicitly as outside the architecture's reach, not merely mis-fit
- **Conditions** — adult *Drosophila*, in vivo ERG/LMC recording; S2 cells for channel biophysics
- **Source** — Gengs C et al., *J Biol Chem* 277(45):42113–20 (2002), PMID 12196539 (ort/hclA identity); Pantazis A et al., *J Neurosci* 28(29):7250–9 (2008), PMID 18632929 (hclA vs. hclB distinct roles, EC₅₀/conductance, 2-fold ERG enhancement); Gisselmann G et al., *Invert Neurosci* 8(4):171–80 (2008), PMID 18839229 (hclB/ivermectin pharmacology, enlarged ERG transients)
- **Confidence** — high for the channel biophysics numbers (direct quotes); medium for the general functional interpretation of the glial pathway

### T-VIS-020 Light adaptation: response gets larger, faster, and more informative with background intensity
- **Quantity** — photoreceptor graded-voltage response dynamics and information capacity across a 4-log-unit background light intensity range, and their temperature dependence
- **Value** — as background intensity rises (over a 4-log-unit range at 25°C), voltage responses to a fixed contrast become larger, faster, and more accurate; information capacity increases with light adaptation and **saturates at approximately 200 bits/s**. Raising temperature from 15–30°C further speeds phototransduction and membrane dynamics, broadening bandwidth, with an effective **Q₁₀ for information capacity of 6.5**.
- **Spiking/Graded** — photoreceptors = GRADED — this pair of papers is essentially the foundational quantitative characterization of graded photoreceptor coding used throughout the field
- **Type** — dynamic response (adaptation) + steady-state (information-rate ceiling)
- **Method** — in vivo intracellular recording, dark- and light-adapted, naturalistic fluctuating-contrast stimuli plus current injection, signal/noise (Shannon information) analysis, temperature-controlled (15–30°C)
- **Observation model** — extractor must reproduce a background-intensity-**dependent** gain/speed change (not a single fixed linear filter), and should not expect an information-rate comparison to exceed ~200 bits/s at the stated conditions; temperature must be matched (main numbers are at 25°C)
- **Conditions** — adult *Drosophila*, in vivo, 15–30°C (main results at 25°C)
- **Source** — Juusola M, Hardie RC. "Light adaptation in Drosophila photoreceptors: I. Response dynamics and signaling efficiency at 25°C." *J Gen Physiol* 117(1):3–25 (2001), PMID 11134228. "II. Rising temperature increases the bandwidth of reliable signaling." *J Gen Physiol* 117(1):27–42 (2001), PMID 11134229.
- **Confidence** — high — direct quotes

### T-VIS-021 Shaker K+ channel loss halves photoreceptor information capacity
- **Quantity** — contribution of the voltage-gated K⁺ conductance Shaker to photoreceptor signal-to-noise ratio and information capacity
- **Value** — loss of the Shaker K⁺ conductance produces a **50% decrease** in photoreceptor information capacity under fully light-adapted conditions, via attenuated voltage-signal amplification and a compensatory decrease in impedance.
- **Spiking/Graded** — photoreceptors = GRADED — the paper explicitly frames Shaker's role as "selectively amplifying **graded** signals in neurons"
- **Type** — perturbation (channel knockout)
- **Method** — intracellular recording, wild-type vs. Shaker-mutant photoreceptors, in vivo, naturalistic contrast stimuli, information-theoretic analysis + biophysical modelling
- **Observation model** — a clean information-theoretic (bits/s) readout for a channel-level perturbation — useful as a check on whatever intrinsic-conductance assumptions (if any) a photoreceptor model makes
- **Conditions** — adult *Drosophila*, in vivo, fully light-adapted
- **Source** — Niven JE, Vähäsöyrinki M, Kauranen M, Hardie RC, Juusola M, Weckström M. "The contribution of Shaker K+ channels to the information capacity of Drosophila photoreceptors." *Nature* 421, 630–634 (2003). PMID 12571596
- **Confidence** — high

### T-VIS-022 Loss of histamine causes a photoreceptor→interneuron→photoreceptor feedback overload
- **Quantity** — effect of removing histamine entirely (hdc null mutant — cannot transmit the photoreceptor→interneuron signal) on photoreceptor operating range and information sampling
- **Value** — hdc(JK910) mutant R1–R6 photoreceptors sample a similar *amount* of information from naturalistic stimuli as wild-type, but package it into **smaller responses**, especially at bright illumination. Mechanism proposed: loss of inhibitory histaminergic feedback depolarizes the postsynaptic interneurons, which then increases their **excitatory** feedback *back onto* the photoreceptors, tonically depolarizing them toward saturation and **reducing their operating range**. Restoring histamine specifically at the interneurons (genetic rescue) restores normal phasic feedback and normal photoreceptor output dynamics.
- **Spiking/Graded** — photoreceptors = GRADED
- **Type** — perturbation (neurotransmitter-null mutant + rescue)
- **Method** — intracellular recording, wild-type vs. hdc(JK910) mutant R1–R6, in vivo, naturalistic light stimuli, information-theoretic analysis, genetic rescue
- **Observation model** — identifies an **excitatory feedback loop (interneuron → photoreceptor)** that a typical feedforward visual model omits by construction — flag explicitly as outside the architecture's reach rather than silently mismatched, unless a return synapse is added
- **Conditions** — adult *Drosophila*, in vivo, hdc(JK910) null vs. wild-type, genetic rescue arm
- **Source** — "Evidence for Dynamic Network Regulation of Drosophila Photoreceptor Function from Mutants Lacking the Neurotransmitter Histamine." *Front Neural Circuits* (2016). PMID 27047343. Author list not confirmed this pass.
- **Confidence** — medium — abstract-level detail; exact magnitude of the "smaller response" not extracted

### T-VIS-023 Microvillus-level stochastic adaptation, with a ~100–200 ms refractory period
- **Quantity** — mechanism and time course of light adaptation at the single-microvillus level
- **Value** — each of the ~30,000 microvilli per photoreceptor produces stochastic "quantum bump" responses to single photons. After each bump, an individual microvillus is refractory for **~100–200 ms**, reducing quantum efficiency as intensity rises. This refractoriness — not a global gain change alone — is a primary mechanism opposing saturation and implementing adaptive sampling; intracellular calcium and voltage separately adapt bump amplitude and waveform.
- **Spiking/Graded** — photoreceptors = GRADED
- **Type** — dynamic response (adaptation mechanism, quantal level)
- **Method** — biophysically realistic stochastic microvillus/phototransduction-cascade modelling, validated against single-cell intracellular recordings under naturalistic contrast stimuli
- **Observation model** — the ~100–200 ms microvillus refractory period is a hard lower bound on any fast adaptation time constant a photoreceptor model claims to reproduce; a model with no adaptation faster than, e.g., a second is missing this entire component
- **Conditions** — adult *Drosophila*, in vivo intracellular recording + stochastic simulation
- **Source** — "Stochastic, adaptive sampling of information by microvilli in fly photoreceptors." *Curr Biol* (2012). PMID 22704990. Author list not confirmed this pass.
- **Confidence** — high — direct quotes

---

## Behavioural state modulation

### T-VIS-024 Flight roughly doubles VS-cell visual-motion gain
- **Quantity** — gain of wide-field motion-sensitive VS-cell responses, rest vs. flight
- **Value** — peak-to-peak voltage responses of vertical-system (VS) neurons to visual motion **doubled (~2x)** during flight compared to rest, in the same fly.
- **Spiking/Graded** — VS cells = GRADED-dominant (see quick-reference table)
- **Type** — dynamic response (behavioural-state gain modulation)
- **Method** — whole-cell patch-clamp recording from VS neurons in a rigidly tethered fly, comparing visually evoked responses during spontaneous quiescence vs. tethered flight
- **Observation model** — needs two distinct operating-gain states ("rest" vs. "flight") for the same downstream unit; a single fixed-gain model cannot be validly compared against both conditions at once — the extractor must pick or explicitly parametrize a state
- **Conditions** — adult *Drosophila*, tethered, within-fly comparison (rest vs. flight bouts)
- **Source** — Maimon G, Straw AD, Dickinson MH. "Active flight increases the gain of visual motion processing in Drosophila." *Nat Neurosci* 13(3):393–9 (2010). PMID 20154683. **Not on PMC** (no `pubmed_pmc` link found this pass).
- **Confidence** — medium — the "doubled" figure came from an abstract-level summary, not a verified direct quote with SEM/n; treat ~2x as approximate pending a full-text check

### T-VIS-025 Walking multiplies HS-cell gain 3–16x and shifts the tuning peak higher
- **Quantity** — gain and temporal-frequency tuning-curve shift of horizontal-system (HS) cell responses, quiescence vs. walking
- **Value** — mean response gain (walking/quiescent) = **2.96** across trials within one fly (n = 5 trials); mean gain = **6.5 ± 4.4** (range **2.7–16**) across n = 8 different flies. Stationary tuning-curve peak is at ~1 Hz; during walking, in 6/8 flies the peak shifted to significantly higher temporal frequencies (Mann-Whitney p < 0.001), with the maximum response gain occurring at **6 Hz** (tested range 0.25–10 Hz). Amplification is significant at all tested frequencies (p < 0.05 to p < 0.001 depending on frequency).
- **Spiking/Graded** — HS cells = GRADED-dominant
- **Type** — dynamic response (multiplicative, frequency-dependent gain + tuning-curve shift)
- **Method** — imaging/recording of HS cells in a tethered fly walking on an air-supported ball vs. quiescent, moving gratings at 0.25–10 Hz
- **Observation model** — needs a walking/quiescence classifier applied to the *same* simulated motion response, and must reproduce a **multiplicative, frequency-dependent** gain change (up to 6–16x in the best flies) with the peak temporal frequency itself shifting higher during walking — not just an additive offset. This is a strong, precisely numeric target.
- **Conditions** — adult *Drosophila*, tethered, walking on air-supported ball vs. quiescent, room temperature
- **Source** — Chiappe ME, Seelig JD, Reiser MB, Jayaraman V. "Walking modulates speed sensitivity in Drosophila motion vision." *Curr Biol* 20(16):1470–5 (2010). PMID 20655222, PMC4435946 (full text read)
- **Confidence** — high — direct quotes from full text

### T-VIS-026 Octopamine neurons are necessary and sufficient for the flight-induced gain boost
- **Quantity** — necessity/sufficiency of octopaminergic neurons for the flight-induced visual gain increase in VS cells
- **Value** — octopamine neurons are "both necessary and sufficient" for the flight-induced visual response boost in VS cells: silencing them abolishes the flight-related gain increase; artificially activating them mimics it. Exact fold-change under direct octopamine-neuron manipulation was not extracted (abstract-level only).
- **Spiking/Graded** — VS cells = GRADED-dominant; octopaminergic neurons not addressed here
- **Type** — perturbation (neuromodulatory silencing/activation)
- **Method** — genetic silencing/activation of octopaminergic neurons + patch-clamp recording from VS cells during rest vs. flight
- **Observation model** — pins the flight-gain change (T-VIS-024) to a specific, separately manipulable neuromodulatory pathway — a model would need an explicit external gain-control input correlated with flight motor state, rather than an intrinsic state-dependent nonlinearity built into the visual neuron itself
- **Conditions** — adult *Drosophila*, tethered flight
- **Source** — Suver MP, Mamiya A, Dickinson MH. "Octopamine neurons mediate flight-induced modulation of visual processing in Drosophila." *Curr Biol* 22(24):2294–302 (2012). PMID 23142045
- **Confidence** — medium — abstract-level; fold-change numbers not extracted

### T-VIS-027 Octopamine silencing slows visually evoked flight-speed acceleration, not baseline speed
- **Quantity** — behavioural flight-speed acceleration response to visual motion, with vs. without octopamine-neuron silencing
- **Value** — flies with silenced octopamine neurons "accelerated more slowly in response to visual motion than control flies, but maintained nearly the same baseline flight speed" — i.e. octopamine affects the visually evoked *gain* of speed regulation, not the baseline set-point.
- **Spiking/Graded** — not addressed at the single-cell level (behavioural paper)
- **Type** — perturbation (behavioural readout, complementing T-VIS-026)
- **Method** — genetic silencing of octopaminergic neurons + magnetically tethered flight simulator measuring forward flight-speed responses to visual motion
- **Observation model** — a purely behavioural cross-check of the octopamine/gain story: the model's downstream speed-control output should show reduced motion-gain but unchanged baseline under a simulated octopamine-knockout condition
- **Conditions** — adult *Drosophila*, magnetic tether, flight simulator
- **Source** — "Octopaminergic modulation of the visual flight speed regulator of Drosophila." *J Exp Biol* (2014). PMID 24526725. Author list not confirmed this pass (very likely Suver/Dickinson-lab by subject continuity, not verified).
- **Confidence** — medium — abstract-level paraphrase only

### T-VIS-028 Food deprivation suppresses the walking-induced visual gain boost
- **Quantity** — dependence of the walking-induced motion-vision gain increase (cf. T-VIS-025) on nutritional/food-deprivation state
- **Value** — the walking-induced enhancement of motion-vision gain and optomotor responses is **reduced** in food-deprived flies relative to fed flies — the state-dependent gain boost is itself gated by a second, slower internal-state variable, not solely by walking/flight motor state. Exact magnitude of the reduction was not extracted.
- **Spiking/Graded** — presumed same tangential-cell population as T-VIS-024/025 (GRADED-dominant); not independently confirmed here
- **Type** — dynamic response (second-order state-dependent modulation)
- **Method** — (imaging or electrophysiology of motion-sensitive tangential cells, per the broader literature this paper sits in) combined with optomotor behaviour, fed vs. food-deprived, walking vs. quiescent
- **Observation model** — before comparing a model's walking-gain output to T-VIS-025's numbers, note that those numbers implicitly assume a "fed" state — if the model has any analogous slow internal variable it should be controlled for; if not, only compare against the fed-state condition
- **Conditions** — adult *Drosophila*, fed vs. food-deprived, tethered walking
- **Source** — Longden KD, Muzzu T, Cook DJ, Schultz SR, Krapp HG. "Nutritional State Modulates the Neural Processing of Visual Motion." *Curr Biol* 24(8):890–5 (2014). PMID 24684935
- **Confidence** — medium — abstract-level paraphrase from a search snippet, not a verified direct full-text quote; exact magnitude not obtained

### T-VIS-029 Octopamine speeds T4/T5 tuning by speeding their inputs, not T4/T5 intrinsically
- **Quantity** — shift in T4/T5 temporal-frequency tuning under octopamine-receptor activation, and whether it is inherited from a corresponding shift in the input elements' own dynamics
- **Value** — pharmacological/genetic octopamine-receptor activation shifts T4/T5 temporal tuning toward **higher frequencies**; this shift is "fully explained" by a concomitant speeding of the columnar input elements' own temporal dynamics — i.e., the behavioural-state tuning shift is inherited from upstream presynaptic dynamics, not implemented de novo in T4/T5 or via a separate neuromodulatory input onto T4/T5 directly. The same study comprehensively measured all T4/T5 columnar inputs' spatiotemporal response properties by two-photon Ca²⁺ imaging and found large differences in temporal dynamics between them, motivating a three-input (not two-input) algorithmic model of direction selectivity.
- **Spiking/Graded** — T4, T5, and all named inputs = GRADED
- **Type** — dynamic response (state-dependent tuning shift) + steady-state (baseline per-input dynamics — values not extracted, see confidence note)
- **Method** — two-photon Ca²⁺ imaging of all major T4/T5 columnar inputs and of T4/T5 themselves, moving gratings across temporal frequencies, before/after pharmacological or genetic octopamine-receptor activation
- **Observation model** — this is the mechanistic link between the wide-field behavioural-state targets (T-VIS-024/025/026) and the T4/T5 tuning targets (T-VIS-009/011): a correct model should shift the **input layer's** time constants under a simulated "aroused" state and show the T4/T5-level shift **emerge** from that, rather than hand-tuning a T4/T5-level gain knob directly
- **Conditions** — adult *Drosophila*, in vivo two-photon imaging, pharmacological/genetic octopamine-receptor activation
- **Source** — Arenz A, Drews MS, Richter FG, Ammer G, Borst A. "The Temporal Tuning of the Drosophila Motion Detectors Is Determined by the Dynamics of Their Input Elements." *Curr Biol* 27(7):929–944 (2017). PMID 28343964. **Confirmed not on PMC** (elink with explicit `linkname=pubmed_pmc` returned no linksetdb for this PMID).
- **Confidence** — high for the qualitative "shift explained by input speeding" claim (direct quote); **low** for any specific per-cell-type time constant — full text is not accessible via PMC, and I could not retrieve the actual filter time constants for Mi1/Tm3/Mi4/Mi9/Tm1/Tm2/Tm4/Tm9 reported in this paper

---

## What I could not find / would need to verify further

- **FlyVis's exact per-cell-type comparison table.** The paper states it checked model predictions against "26 previously reported studies" (Supplementary Note 3, Supplementary Data files 5 and 6), but those supplementary files did not render through the tools available this session. I reconstructed a plausible, largely-overlapping reading list independently (the papers cited T-VIS-009 through T-VIS-017 above are the obvious candidates by cell type and content) but **cannot confirm FlyVis actually used these exact papers**, nor recover its own per-cell-type match/mismatch scoring beyond what `prior-validation.md` already documents in aggregate.
- **Maisak et al. 2013's own reported DSI values.** I obtained velocity-tuning and tuning-width numbers from a self-archived copy of the text, but the specific per-cell-type DSI distribution (the "25/49 clones had DSI ≥ 0.6" style statistic) actually comes from a *later* paper (Fisher et al. 2015) using Maisak's stimulus/methodology, not from Maisak's own reported summary statistic. Not resolved this pass.
- **LPLC2 silencing behavioural escape-rate percentages** (Klapoetke 2017, T-VIS-006/007) — reported only graphically in the source figures; I have the statistical significance context (chi-squared p-values from a related 2025 paper) but not the actual percentage-point numbers.
- **Per-cell-type time constants for Mi1, Tm3, Mi4, Mi9, Tm1, Tm2, Tm4, Tm9 from Arenz et al. 2017** (T-VIS-029) — this is likely the single richest available source for exactly the numbers priority #2 of this task asked for, but it is not open-access on PMC and I could not retrieve its figures/tables this pass.
- **Individual physiological values for Mi4 and Mi9 specifically** — both are named throughout (Strother 2017, Arenz 2017) as characterized T4 inputs, but I did not find a source giving their individual response amplitudes, latencies, or contrast tuning the way Behnia 2014 gives for Mi1/Tm3/Tm1/Tm2.
- **A single clean "operating range in mV" number for photoreceptors** — I have adaptation dynamics, information rates, and channel contributions (T-VIS-020/021/023), but not one canonical peak-to-peak voltage range figure.
- **Whether T4/T5, LPLC2, and the wide-field tangential cells (HS/VS) ever fire true sodium spikes vs. pure graded potentials** is not fully resolved here — I've marked HS/VS as "graded-dominant" based on the behavioural-state literature's framing ("peak-to-peak" continuous responses) and general knowledge of superimposed spikelets in some large fly interneurons, but did not chase down a primary source specifically characterizing this for *Drosophila* HS/VS. Same caveat for LPLC2.
- I did not investigate Mi2, Mi10, C2, C3, T2, T3, T4/T5's other named subtypes' individual inputs beyond the eight the task named, nor the lobula-plate tangential cell (LPTC) population beyond HS/VS used for the behavioural-state numbers.
