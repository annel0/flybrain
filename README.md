# flybrain

A fast GPU simulator for connectome-constrained spiking models of the
*Drosophila* central nervous system — and an honest record of what it could
and could not establish.

**[Читать по-русски](README.ru.md)**

---

## What this is

It started as a joke. Some people had wired a fly connectome up to Doom, and
the obvious next question was: everyone is *reading* this brain, nobody is
*changing* it. What happens if you add neurons to a brain?

The joke survived contact with the problem; the naivety did not. This
repository is what came out: a simulator that turned out to be quite fast, a
replication that says the simulator is correct, and a long list of specific,
measured reasons why the original question cannot currently be answered
honestly.

The spirit is Ig Nobel — an absurd premise studied by an honest method. What
separates that from the viral fly-brain demos is not seriousness of tone. It is
that we ran the controls, published the failures, and checked our numbers
against someone else's.

## The engine

The simulation is a leaky integrate-and-fire network over the released
connectome, held in CSR form and advanced by hand-written Triton kernels. Four
choices do most of the work.

**Spikes are compacted in the kernel that produces them.** The usual pattern —
threshold into a dense `[batch, neurons]` mask, then `nonzero` — materialises
10 MB and synchronises with the host to find the ~0.05% of cells that fired.
Here the membrane kernel appends spiking cells to a compact list through an
atomic counter, so the mask never exists and the step contains no host
synchronisation at all.

**Axonal delay costs almost nothing.** The usual implementation is a dense
`[delay_slots, batch, neurons]` ring of conductances, which roughly doubles the
step's memory traffic. Because delay here is per source cell rather than per
synapse, the ring can hold *spike indices* instead: 32 slots of 16k int32,
2 MB, and cost proportional to spikes rather than to population.

**State is sized to what it holds.** The refractory counter was an fp32 array
holding a countdown that never exceeds 22; as an int8 step counter it is exact
and removes a quarter of the membrane kernel's traffic. Membrane time constants
are per cell, because they are measured to differ by an order of magnitude
between types — Kenyon cells exceed 200 ms against a generic 20 ms.

**The scatter grid is sized to the work, not to the buffer.** An earlier
version launched one program per slot of the spike buffer, and the buffer is
sized for the worst case: 54 of every 55 programs existed only to read a
counter and exit.

### What that buys

| | |
|---|---|
| aggregate throughput | **8.9x realtime** (batch 4, fp16) |
| one fly, full CNS | **2.4x realtime** — faster than the animal lives |
| membrane kernel | 250 GB/s, **86%** of the card's measured ceiling |
| hardware | one RTX 3060, 12 GB |
| verified against | a reference PyTorch implementation, bit-identical in fp32 |

Ten seconds of simulated central nervous system takes 4.1 seconds of wall
time. The optimisation pass that got there is documented step by step in
[docs/benchmarks.md](docs/benchmarks.md), including the three changes that made
things *slower* and were reverted.

## Does it actually work?

Yes, and this is the one claim here checked against numbers we did not produce.

Shiu et al. (*Nature* 2024) published a leaky integrate-and-fire model of this
brain with a supplementary table of exact firing rates for fifteen named
neurons under a fully specified protocol. Their cell-type names appear nowhere
in the MaleCNS annotations, so their predictions cannot be transferred to our
dataset — but they can be replicated on theirs. We imported FlyWire 783 exactly
as shipped with their code and ran their protocol:

| neuron | published | ours |
|---|---|---|
| **MN9_r** | **68.0 Hz** | **67.8 Hz** |
| Zorro_l | 102.2 | 107.2 |
| Rattle_l | 75.4 | 77.2 |
| Phantom_l | 57.6 | 58.4 |

**Median ratio 1.01, correlation 0.970** across thirteen neurons. The motor
neuron their paper is built around matches to 0.3%.

The first pass was 17% low across the board — the signature of one shared
constant rather than a wiring error. Their source sets the refractory period of
Poisson-driven neurons to zero and ours did not, so a cell asked for 100 Hz
delivered 82. Predicted 0.82, observed 0.83.

## Does the connectome do anything?

The Digital Sphinx (Brunton & Tuthill 2026) attached a *worm* connectome to a
fly body, trained the interface, and got realistic fly walking — so behavioural
realism proves nothing, and a real-versus-rewired control is close to a minimum
bar. We ran it.

Compared at matched spontaneous activity, a degree-preserving rewiring of the
same graph spreads activity over eight times as many cells, recruits a quarter
as many Kenyon cells, produces no projection-neuron response to stimulating one
glomerulus, and leaves the APL neuron **completely silent**, so the mushroom
body's feedback loop is simply absent. The APL block effect falls from +83.5 to
+0.0 percentage points.

The wiring is doing work its degree distribution does not.

## What this could not establish

The original question — what happens if you add neurons — is not answerable
with this model, for reasons that are measured rather than suspected:

- **57% of the network does not spike.** The whole optic lobe pathway signals
  with graded potentials, including T4 and T5. That is 95,501 of 166,700
  neurons modelled as something they are not.
- **Under 1% of cell types have measured physiology.** Roughly 20-40 of ~5,000
  have ever been characterised by patch clamp. It is a structural ceiling, not
  a temporary gap.
- **The mechanism that sets sparseness cannot be represented.** APL's
  inhibition is spatially localised and largely self-directed per Kenyon cell;
  a point neuron collapses it into one voltage. Since that is what would set
  memory capacity, the capacity experiment would measure our simplification.
- **The parameters are degenerate.** Several produce the same output, so
  fitting one observable constrains the model without identifying it.
- **Our own better-looking result leaned on an artefact.** Glomerular
  selectivity of 2-6x turned out to depend on local interneurons spiking — the
  cells with the clearest evidence that they should not.

All of it is in [docs/lab-notebook.md](docs/lab-notebook.md), including the
mistakes, in the order they were made and corrected.

## The research notes

Alongside the code there is a literature collection: **222 targets across
eleven domains**, each carrying the measurement protocol that produced it,
because a number is not comparable to a simulation until you know how it was
measured. Of those, 53 are directly comparable to what this model produces,
124 are behavioural readouts it structurally cannot produce, 22 are quantities
nobody has ever measured, and 16 need an indicator model first.

- [docs/targets/](docs/targets/) — the collection, organised by circuit
- [docs/theory-review.md](docs/theory-review.md) — what the literature has that
  this model does not, deliberately including critiques
- [docs/lab-notebook.md](docs/lab-notebook.md) — one entry per experiment

These stay in English.

## Reproducing

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv torch numpy pyarrow pandas matplotlib

python src/import_graph.py            # MaleCNS v1.0 -> CSR  (~1.2 GB download)
python src/delays.py                  # axonal delays from the reconstruction
python bench/replicate_shiu.py        # the replication above
python bench/rewire_control.py        # the rewiring control
```

Needs a CUDA GPU. Every experiment writes a machine-readable summary to `out/`
and a verbatim log to `logs/` via `run_experiment.sh`, failures included.

## Provenance

The code, experiments, measurements and literature review in this repository
were produced by **Claude Opus 5** (Anthropic) over an interactive session,
working under the direction of the repository owner, who set the goals, made
the methodological calls and repeatedly caught framing errors.

That matters most for one section. The critical assessments of other
projects — in [docs/theory-review.md](docs/theory-review.md) and
[docs/targets/prior-validation.md](docs/targets/prior-validation.md) — are that
model's readings of published sources. Every claim is cited inline and should
be checked against the source rather than taken on this repository's word. They
are offered as a reading, not a verdict, and several such readings were wrong
during the session and were corrected; those corrections are in the lab
notebook alongside everything else.

If something here misrepresents your work, that is an error rather than a
position, and a correction is welcome.


## Credits

The connectomes are not ours, and they are the reason any of this is possible:
the **FlyEM team at Janelia**, the **MRC LMB**, the **University of Cambridge**
and **Google Research** for MaleCNS v1.0; the **FlyWire Consortium** at
Princeton for FAFB. Both CC-BY.

**Shiu, Sterne et al.** published their model, their parameters and their data,
which is the only reason the replication above was possible at all. Most of the
physiological constants here are theirs, with their citations.

Code is MIT. See [LICENSE](LICENSE) for the data terms, which are separate.

---

*Not peer reviewed. Not a fly.*
