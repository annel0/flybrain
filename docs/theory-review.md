# What the literature says that our model does not have

A survey done after the practical work, deliberately including critiques and
hypotheses rather than only the paper we were implementing. Organised by what
it changes for us.

---

## 1. The antennal lobe interneurons should not be spiking at all

Our worst remaining artefact is that antennal lobe local interneurons (`lLN*`)
fire at 350 Hz and smear activity across glomeruli, blurring the labelled line
down to 2-6x selectivity.

There is a named cause. [Nonspiking interneurons in the Drosophila antennal
lobe](https://www.eneuro.org/content/10/1/ENEURO.0109-22.2022) (eNeuro 2022)
shows a population of local interneurons that **transcribe the voltage-gated
sodium channel gene `para` but do not translate it**. Voltage clamp finds no
TTX-sensitive sodium current. They cannot spike; they release transmitter by
graded potential. The paper characterises one population and does not quantify
what fraction of all LNs is non-spiking.

This is the same lesson vision taught us, in the circuit we actually chose:
part of the antennal lobe is not a spiking system, and a leaky
integrate-and-fire network cannot represent it. Our hottest cells are cells
that in the animal do not fire at all.

**Action:** give the LNs graded output instead of spikes. Highest-value fix
available, and it targets the specific number that is wrong.

## 2. Gap junctions are missing, and they matter in the same place

Electrical synapses in Drosophila are built from innexins; four are expressed
in neurons (`inx5`, `inx6`, `inx7`, `shakB`). [Innexin 7 contributes to
synchronised activity in the antennal lobe and regulates olfactory
function](https://pmc.ncbi.nlm.nih.gov/articles/PMC12062127/) — again, the
circuit we are working in. `shakB` forms the rectifying electrical synapses of
the giant fibre escape system.

EM connectomes map chemical synapses. Electrical coupling is a separate layer
that is not in our graph and not in anyone's fly simulation.

## 3. Most peptide signalling does not travel along wires at all

For C. elegans the second layer has been mapped: [the neuropeptidergic
connectome](https://www.cell.com/neuron/fulltext/S0896-6273(23)00756-0)
(Ripoll-Sánchez et al., Neuron 2023) finds that the peptidergic and synaptic
networks **overlap for only 5% of peptidergic connections**. Ninety-five
percent of that signalling follows paths that do not exist in the wiring
diagram — it diffuses.

No fly equivalent exists yet, though the ingredients do (single-cell receptor
expression). If the worm number carries over even approximately, a synaptic
connectome is a minority of the communication.

## 4. One connectome is one individual, and individuals differ a lot

From [whole-brain annotation and multi-connectome cell
typing](https://www.nature.com/articles/s41586-024-07686-5) (Nature 2024),
comparing hemibrain and FlyWire:

- most cell types are highly stereotyped, but **connection weights are
  "surprisingly variable" within and across animals**
- only connections above ~10 synapses, or providing >1% of a target's input,
  are highly conserved — and our graph keeps everything down to one synapse
- about a third of hemibrain cell types could not be robustly identified in
  FlyWire
- **the most common Kenyon cell type is nearly twice as numerous in FlyWire as
  in the hemibrain**

That last point lands directly on our planned first experiment. Kenyon cell
number varies about two-fold between individuals, naturally. That is a free
control: our "add Kenyon cells" manipulation starts inside the range biology
already explores, and a doubling has a natural comparison. It also means our
single MaleCNS count is one draw, not a constant.

For C. elegans the [State of Brain Emulation Report
2025](https://arxiv.org/abs/2510.15745) puts it harder: 40-50% of synaptic
connections differ between genetically identical worms.

## 5. Synapse count as weight is defensible — this one we got right

[Synaptic counts approximate synaptic contact area in
Drosophila](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0266064)
(PLOS One 2022): total synaptic contact area from one neuron to another is
accurately predicted by the number of contacts, across transmitters. Using
count as a strength proxy is supported.

The caveat is separate and sharp: [the effectome
paper](https://www.nature.com/articles/s41586-024-07982-0) (Nature 2024) notes
the connectome gives the paths by which neurons *can* affect each other, not
how strongly they *do* in vivo. Count predicts anatomy well and causal
influence poorly.

## 6. The operating point has a theory, and it makes a prediction we can test

Our problem — cells sitting too far below threshold to pass anything on, then
saturating when the weight is raised — is the classic balanced-network
question. [van Vreeswijk and Sompolinsky](http://www.gatsby.ucl.ac.uk/~pel/tnlectures/papers/vanv_somp.pdf):
excitation and inhibition nearly cancel, the mean membrane potential sits just
below threshold, firing is driven by fluctuations rather than by mean drive,
and **synaptic couplings scale as 1/sqrt(K)** with in-degree K.

That is a quantitative prediction rather than a fit. Our mean degree is 153.5
against roughly 72 for the brain-only FlyWire graph, a ratio of about 2.1, so
the scaling law predicts a weight of 0.275 / sqrt(2.1) ≈ **0.19 mV**. We fitted
**0.075**. The factor of 2.5 between them is not explained, and finding out why
is more informative than the fit itself.

## 7. A cheap diagnostic we are not using: avalanche statistics

The [criticality hypothesis](https://arxiv.org/pdf/2306.05635) holds that
networks sit near a phase transition between order and randomness, where
avalanche sizes follow a power law. Whether or not one believes the hypothesis,
the measurement is nearly free for us — we already record every spike — and a
network that is either dead or saturated fails it obviously. It is a
sanity check on the operating point that does not require any new biology.

## 8. Behavioural state rewires the gain, and we have one state

Octopamine release at the onset of flight [immediately changes the gain of
directionally selective visual neurons](https://pubmed.ncbi.nlm.nih.gov/23142045/),
and behavioural state alters the baseline and temporal tuning of T4 and its
inputs Mi1, Tm3, Mi4 and Mi9. A resting fly and a walking fly do not have the
same brain. Ours has exactly one state, and no mechanism to have another.

---

## Why not to trust any single source, including ours

**Jonas and Kording, [Could a neuroscientist understand a
microprocessor?](https://www.biorxiv.org/content/10.1101/055624v1)** They took
a 6502 — complete connectome, unlimited perturbation, every transistor
observable, ground truth fully known — and applied standard neuroscience
analysis. It recovered correlations, lesion effects and tuning curves, and
never recovered fetch-decode-execute. Worse, lesioning found transistors
"specific to" one game, a conclusion that is simply wrong about what the chip
does. Complete observability did not produce understanding.

**OpenWorm.** C. elegans has had a complete connectome since 1986 and 302
neurons. Fourteen years of a dedicated project have not produced a working
emulation. The reasons given are ours: a connectome is not a circuit schematic,
it comes from a dead animal, and the electrophysiology needed to parameterise
it mostly does not exist.

**Marder's degeneracy — the one that applies most directly to us.**
[Variability, compensation and modulation in neurons and
circuits](https://www.pnas.org/doi/10.1073/pnas.1010674108) (PNAS 2011): the
stomatogastric ganglion shows **2-6 fold variability** in the parameters that
determine circuit dynamics, and **many different parameter sets produce the
same circuit output**. Circuits are not hard-wired to one behaviour; modulators
reconfigure them.

Applied to us: we fitted one free parameter against one observable and got
5.6% Kenyon cell recruitment, which looks like a success. Degeneracy says a
family of parameter sets would produce that same number, and matching one
observable does not select the right member of the family, or even establish
that the right member is in it. The fit is a constraint, not a validation.

**And the report on the field as a whole** ([State of Brain Emulation
2025](https://arxiv.org/abs/2510.15745)) says the bottleneck is data, not
compute: no organism has whole-brain recording at single-neuron resolution,
calcium imaging runs at 1-30 Hz against real firing rates, and recordings last
minutes. Which is the opposite of where we have been spending effort.

---

## What to do with this

Ordered by value per unit of work:

1. **Make antennal lobe local interneurons graded rather than spiking.**
   Targets the specific artefact we measured, and has a specific citation.
2. **Test the 1/sqrt(K) scaling** instead of trusting the free fit, and find
   out where the remaining factor of 2.5 comes from.
3. **Measure avalanche statistics** — free, and it says whether the operating
   point is defensible at all.
4. **Check the fit's degeneracy**: sweep other parameters and see how large the
   family of settings reproducing 5.6% is. If it is large, say so.
5. **Use the two-fold natural variation in Kenyon cell number** as the control
   for the planned capacity experiment, rather than treating the MaleCNS count
   as a constant.
6. Gap junctions and a second behavioural state are real gaps, but they are
   projects, not fixes.

---

# What disease research adds

Added after the survey above, on the suggestion that illness might be
informative. It was, in three distinct ways.

## 1. Our failure mode is a named disease, not a bug

At the published weight the network saturated: 100% of Kenyon cells at 195 Hz.
That is the textbook definition of a seizure — "seizures develop as a
consequence of the predominance of excitatory over inhibitory processes"
([Frontiers in Molecular Neuroscience
2023](https://www.frontiersin.org/journals/molecular-neuroscience/articles/10.3389/fnmol.2023.1116000/full)).

Drosophila is a standard epilepsy model with real mutants. `para-bss1`
("bang-senseless") is a **gain-of-function mutation in the voltage-gated
sodium channel** that shifts inactivation and makes neurons more excitable; it
has the lowest seizure threshold of the bang-sensitive series
([Genetics 2011](https://academic.oup.com/genetics/article/187/2/523/6063291)).
`easily shocked` hits ethanolamine kinase and membrane lipid synthesis.

So an over-excitable version of this model is not merely broken — it is a
perturbation with a literature, a molecular cause and a measurable phenotype.
That reframes it from a bug to be avoided into a state to be entered
deliberately: what structural change pushes this brain over that edge, and
what holds it back.

## 2. The brake has a name, and it works in our model

Sparse coding in the mushroom body is not a consequence of general weight
tuning. It is enforced by a specific negative feedback loop: the giant
GABAergic **APL** neuron receives from Kenyon cells and inhibits them back
([Lin et al., Nature Neuroscience
2014](https://www.nature.com/articles/nn.3660); [Amin et al.,
eLife 2020](https://elifesciences.org/articles/56954)).

That loop is complete in our graph — 2 APL cells, GABAergic, ~2,300
connections each onto Kenyon cells at ~98,000 synapses, plus 4,693 feedback
connections from Kenyon cells back. **APL supplies 80% of all inhibition
reaching Kenyon cells** and 9% of their total input.

Blocking APL's output, as the experiments do:

| | APL rate | Kenyon cells recruited |
|---|---|---|
| intact | 241 Hz | **5.6%** |
| APL output blocked | 384 Hz | **89.2%** |

The sparseness collapses, +83.6 percentage points — which is qualitatively
what blocking APL does in the animal. This is the first causal validation this
model has passed, and it says the 5.6% comes from the circuit that produces it
in the fly rather than only from the weight we fitted.

**The caveat is real and specific.** APL fires at 241 Hz here, and in the
animal APL is a graded, largely non-spiking neuron whose inhibition is
**spatially localised**: "individual Kenyon cells inhibit themselves via APL
more strongly than they inhibit other individual Kenyon cells", and APL
differentially inhibits different mushroom body compartments. A point neuron
collapses the entire cell into one voltage and destroys exactly that
locality. So we have the right mechanism implemented with the wrong physics —
and this lands directly on the planned Kenyon cell capacity experiment, since
compartmentalised inhibition is part of what sets capacity.

## 3. Subtraction has a literature; addition does not

Connectome-based modelling of disease is a mature methodology and it is
precisely our method, run in the other direction: [connectome-based modelling
of neurodegenerative diseases](https://www.nature.com/articles/s41583-023-00731-8)
(Nature Reviews Neuroscience 2023). Pathology spreads along connectome paths,
network diffusion models predict where atrophy goes next, and **hub regions
are selectively vulnerable** — in Huntington's, rich-club regions carry the
structural loss ([Brain 2015](https://academic.oup.com/brain/article/138/11/3327/331512)).

The fly connectome has a documented rich club — about 30% of neurons, by the
[network statistics paper](https://www.nature.com/articles/s41586-024-07968-y).

The methodological point is the useful one. Removing things from a connectome
and simulating the consequence is a validated technique with published results
to check against. Adding things is not. So the machinery for structural
manipulation should be **calibrated on subtraction first** — targeted hub
removal, cell-type ablation, the APL block above — where there is literature
to be wrong against, and only then turned around to do addition, where there
is not.

A caution from the same literature: [Drosophila appear resistant to
trans-synaptic tau propagation](https://pubmed.ncbi.nlm.nih.gov/39130515/), so
the spreading models that work in mammals may not transfer to flies. The
method transfers; the specific disease process may not.

## What this changes in the plan

- **The APL block is our first passed validation.** Keep it as a regression
  test: any future version of the model must still lose sparseness when APL is
  silenced.
- **Compartmentalised APL inhibition is a prerequisite** for the Kenyon cell
  capacity experiment, not an optional refinement. A point-neuron APL is the
  wrong instrument for a question about capacity.
- **Calibrate structural manipulation on removal before addition**: hub
  ablation and cell-type silencing have published expectations; adding cells
  does not.
- The saturated state is worth keeping as a deliberate condition rather than
  only avoiding — it corresponds to a real, genetically defined fly phenotype.
