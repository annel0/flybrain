# flybrain — GPU feasibility probe for structural connectome experiments

Goal of this stage: find out what an RTX 3060 actually delivers for a
MaleCNS-sized spiking simulation, before designing experiments around it.
Nothing here models fly behaviour or validates biology.

## Data

MaleCNS v1.0 flat connectome (Janelia / MRC LMB / Google Research, CC-BY),
`minconf 0.5`. Node policy: entries with an assigned superclass, excluding
entries annotated as glia. Edge policy: every released edge between retained
nodes, no extra threshold.

Import reproduces the published counts exactly:

```
166,700 neurons   25,582,938 directed edges   mean out-degree 153.5
30.8% of cells carry an inhibitory predicted transmitter (GABA / glutamate)
```

`src/import_graph.py` writes a 240 MiB CSR npz. Signs are a modelling choice
applied on top of the released transmitter predictions; the connectome itself
states no sign.

## Measured on RTX 3060 (12 GiB, 28 SMs), dt = 0.1 ms, 5 Hz mean rate

Aggregate throughput = replicas x simulated-seconds per wall second.

| network | device | best aggregate | at batch |
|---|---|---|---|
| full CNS, 166,700 neurons | RTX 3060 | **2.07x** realtime | 128 (saturated from 32) |
| full CNS, 166,700 neurons | Ryzen 7 5700G, 16 threads | 0.41x realtime | 1 |
| full CNS, 166,700 neurons | Ryzen 7 5700G, 1 thread | 0.27x realtime | 1 |
| 10,000-neuron subgraph | RTX 3060 | **31.1x** realtime | 256, still climbing |

GPU memory is never the constraint: 0.69 GiB at batch 128 on the full graph.

## Where the time goes (batch 64, full graph, 3200 us per step)

| part | us/step | note |
|---|---|---|
| membrane update | 2000 | unfused: every operation allocates a temporary |
| spike select | 1447 | compare + `nonzero` |
| synaptic scatter | 1115 | 127M synaptic events per simulated second |
| host sync | 51 | constant, irrelevant above batch 8 |

Card's measured copy ceiling is **290 GB/s**. `torch.compile` on the membrane
update alone: 1993 us -> 575 us, **3.5x**, reaching 223 GB/s — 77% of that
ceiling. So the membrane update is a solved problem once fused, and the
remaining cost is spike selection and scatter.

## What this means

1. **Batch size does not rescue the full CNS.** Throughput saturates at ~2x
   because the membrane state of 166,700 neurons crosses the memory bus
   10,000 times per simulated second. That is a bandwidth wall, not a
   programming mistake.
2. **Batch size transforms a circuit-sized network.** At 10,000 neurons the
   same card reaches 31x and has not saturated. Below the bandwidth wall,
   replicas are nearly free.
3. **Batch 1 costs the same regardless of network size** (0.27x at both
   166,700 and 10,000 neurons): a single replica is pure launch overhead.
   Never run one replica at a time on the GPU.
4. Realistic ceiling for the full graph after fusing everything: roughly
   3-5x aggregate. Worth doing, but it does not change the conclusion.

## Layout

```
src/import_graph.py     released feather files -> CSR npz
bench/bench_lif.py      batched event-driven LIF, --mode harness|dynamics
bench/profile_step.py   cost share of each part of a step
bench/test_fusion.py    unfused vs torch.compile vs raw copy bandwidth
out/*.json              raw measurements
```

Environment: `uv venv --python 3.11`, torch 2.14.0+cu130.

## Precision: what lower-precision storage costs

Storage in fp16/bf16, arithmetic always fp32 inside the fused kernel — the LLM
weight-quantisation idea applied to neuron state. Membrane voltage is stored as
a deviation from rest so the accumulator sits near zero.

Full graph, 500 ms, ~5 Hz mean rate, per-cell background drive frozen across
variants. Two controls included, because a spiking network is chaotic and any
error figure is meaningless without them.

| variant | population rate error | per-neuron rate corr | extra silent cells | speed @ batch 64 |
|---|---|---|---|---|
| fp32 rerun, identical config | 0% (bit-identical) | 1.0000 | 0 | 1.00x |
| fp32 + 1e-4 mV nudge (chaos floor) | 0.02% | 0.9998 | -16 | — |
| **all fp16** | **2.50%** | 0.9985 | +681 | **1.33x** |
| all bf16 | 42.66% | 0.9162 | +17,523 | 1.33x |
| v fp32, g+refr fp16 | 1.18% | 0.9995 | +41 | **0.39x** |
| g fp32, v+refr fp16 | 2.58% | 0.9985 | +684 | 0.38x |
| v+g fp32, refr fp16 | 1.14% | 0.9995 | +46 | 0.40x |

Reading these:

1. The fp32 rerun is bit-identical, so the scatter is deterministic here and
   every difference below is a real precision effect, not run-to-run noise.
2. The chaos floor over this window is 0.02%. The fp16 error is ~125x that,
   so it is a genuine systematic effect — and it is a **bias**, not noise:
   rates always fall, never rise, and 681 cells stop firing. It does not
   average out across replicas.
3. **bf16 is unusable.** 8 mantissa bits cannot resolve the per-step increment
   of an accumulator; 13% of the firing population goes silent. This is the
   opposite of the usual ML preference and follows directly from the arithmetic.
4. The accumulator is the culprit, as expected: moving only `v` to fp32 halves
   the error, moving only `g` changes nothing.
5. **But mixed precision is 2.5x slower here.** torch.compile does not generate
   a good fused kernel when the arrays disagree in dtype. The accurate option
   is currently the slow one; making it fast needs a hand-written kernel.

Net: all-fp16 buys 1.33x for a 2.5% systematic rate bias. Acceptable for
screening and ranking variants, not for quoting absolute rates. Measured at one
rate over one window; a different regime or a much longer run needs its own check.

Where the LLM analogy genuinely fits is the other array: the graph weights
(25.6M synapse counts, static, read-only) are the true equivalent of LLM
weights and would take int8 comfortably. They are just not the bottleneck.

## Fixing mixed precision with a hand-written kernel

The mixed-precision layout was the accurate one (1.09% error against 2.47%)
but `torch.compile` made it 2.5x slower than fp32, which made it useless.
Inductor will not generate a single good kernel when the state arrays disagree
in dtype. Writing that one kernel by hand removes the constraint — loads widen
to fp32 in registers, stores narrow back per array, one pass over memory.
`bench/kernels.py`, about 25 lines of Triton, which ships with PyTorch.

Membrane update, full graph, batch 64:

| state layout | torch.compile | hand-written Triton | rate error |
|---|---|---|---|
| fp32 | 2558 us (1.00x) | 2835 us (0.90x) | — |
| all fp16 | 1911 us (**1.34x**) | 1943 us (1.32x) | 2.47% |
| **v fp32, g+refr fp16** | 6661 us (**0.38x**) | 2143 us (**1.19x**) | **1.09%** |

So the choice is now real rather than forced:

- **all fp16** — 1.34x faster, 2.5% systematic rate bias
- **v fp32, rest fp16** — 1.19x faster, 1.09% bias, less than half the error

Inductor still wins on the uniform-fp32 path; it is only the mixed layout it
handles badly. Our Triton kernel is untuned (fixed 1024-wide blocks, a modulo
for the per-cell drive), so the gap on fp32 is likely closable.

The membrane update is now no longer the bottleneck. At batch 64 the fused
membrane is ~575 us of a ~2500 us step; the rest is `nonzero` plus the
synaptic scatter. Those are the next target — and `nonzero` in particular is
avoidable, by having the kernel write a compacted spike list with an atomic
counter instead of materialising a dense mask.

### Kernel-authoring options in Python, for the record

- **Triton** — ships with PyTorch, nothing to install. Used here.
- **numba-cuda** (`@cuda.jit`) — NVIDIA's SIMT Python kernel language.
- **cutile-python** — NVIDIA's tile/block model; **cuTeDSL** for tensor cores.
- **NVIDIA Warp** (`@wp.kernel`) — built for simulation, first-class sparse
  scatter/gather, and **reverse-mode autodiff through the kernels**. That last
  property matters later: a trainable module inside the graph, or structural
  plasticity driven by gradients, needs derivatives through the simulation, and
  Triton does not provide them for free.

## Optimisation pass: 2.6x -> 8.9x aggregate

Everything below is measured on the full graph at ~4.8 Hz, verified against
the original torch implementation on per-neuron rates before being timed.

| step | us @ batch 64 | aggregate | note |
|---|---|---|---|
| v0 torch.compile + torch scatter | 2416 | 2.65x | starting point |
| v1 Triton membrane, torch scatter | 2657 | 2.41x | **regression**, see below |
| v2 + compact spike list | 2224 | 2.88x | `nonzero` and both host syncs gone |
| v3 + Triton scatter | 1349 | 4.74x | eight launches become one |
| v5 + int8 refractory counter | 1141 | 5.61x | 25% fewer state bytes, exact |
| v5 + fp16 storage | 789 | 8.11x | 1.4% rate error |

Best aggregate is **8.93x realtime at batch 4 in fp16**; throughput now peaks
at batch 4-16 rather than 128, because a single replica is no longer starved
by launch overhead. Batch 1 went from 0.26x to about 3x.

fp32 correctness after every change: 0.000% population rate error, per-neuron
correlation 1.00000 against the original implementation.

### What the profile says now (batch 64, fp32)

| part | us | share | note |
|---|---|---|---|
| membrane | 769 | 59% | 250 GB/s, 86% of the card's measured ceiling |
| scatter | 299 | 23% | |
| `cnt.zero_` | 3 | 0.2% | |
| gaps between launches | ~230 | 18% | |

The membrane kernel is finished. At 86% of peak bandwidth no tuning will move
it; only moving fewer bytes will, which is exactly what fp16 does and what the
int8 refractory counter did.

### Three things that did not work, and why

- **Triton on the uniform fp32 path is slower than Inductor** (2657 vs 2416).
  Inductor's elementwise codegen is good; it is only the *mixed*-dtype case it
  handles badly. Keep both.
- **Lane-splitting the scatter made it 2.9x slower** (up to 1340 us at 16
  lanes). The diagnosis behind it was wrong: the 44x out-degree imbalance was
  not the bottleneck. The grid was sized to the spike *buffer* (65,536 slots)
  while a step produces ~1,200 spikes, so 54 of every 55 programs launched
  only to read a counter and exit — and lanes multiplied that waste. Sizing
  the grid to the work and striding over it gave 148 -> 102 us instead.
- **CUDA graphs gained nothing** (1611 vs 1601). Once the host syncs were gone
  the per-step launch cost was already immaterial.

### A real bug this found

`scatter_stride` trusted the spike counter without clamping it to the buffer
capacity. The counter reports how many spikes were *seen*, which on an
overflowing step exceeds what fitted, so the kernel read past the end of the
buffer — an illegal access, caught when a profiling harness let the counter
grow. It now clamps to capacity and relies on the overflow flag.

### What is left

Not kernel engineering. The membrane kernel is at the memory ceiling and it is
59% of the step, so the remaining levers are about moving or doing less:

1. **fp16** — already measured: 1.44x for 1.4% systematic rate error.
2. **Lazy updates.** 82% of cells never fire, yet every one of them is read and
   written 10,000 times per simulated second. Skipping cells that are at rest
   with negligible input would change the complexity class rather than the
   constant. It is a modelling decision, not an optimisation, and needs its own
   correctness argument.
3. **Larger dt**, as before: a 5x lever that costs a stability argument.

## Running the whole CNS, unstimulated

`bench/run_fly.py` advances the full released graph with no stimulus, no body
and no task, to price the run and to see what the network settles into.

**Cost, one replica, fp32:**

| | wall per 2 s of simulated time | speed |
|---|---|---|
| unoptimised (torch.compile + torch scatter) | 7.85 s | 0.255x realtime |
| optimised kernels | 0.84 s | 2.37x realtime |
| | | **9.29x speedup** |

The gain is far larger here than the 2.1x measured at batch 64, because a
single replica was dominated by host synchronisation and launch overhead,
which the compact spike list removed. Ten seconds of simulated CNS time now
costs 4.1 s of wall time on one RTX 3060.

**What the network does:** stable — population rate drifts +1.4% over ten
simulated seconds, no runaway, no die-off. Mean 5.19 Hz.

**But the activity regime is wrong, and the shape of the result hides it.**
81% of cells never fire at all, while the 19% that do sit at a median of
23.5 Hz with a maximum of 399 Hz. The rate histogram is a hump centred near
25 Hz, not the long low-rate tail that recordings from central neurons show.
This is a property of the background drive — a Gaussian straddling threshold
produces exactly this split, cells above it firing hard and cells below it
never firing — and not a property of the connectome. The per-superclass and
per-transmitter tables inherit the same artefact, so nothing in them should be
read as a finding about fly physiology.

Making the regime realistic is a separate piece of work: cell-type-specific
membrane parameters, synaptic delays (absent here, present in doomfly),
receptor identity beyond an excitatory/inhibitory sign, sensory input instead
of noise, and calibration against published baseline firing rates.

## Delays and sensory input

Two additions aimed at one symptom — activity with no spatial structure.

### Synaptic delay, at almost no cost

Spikes no longer arrive in the step they are emitted. Delay is per source cell,
computed from the reconstruction's own geometry: a fixed 0.8 ms synaptic
component plus the mean soma-to-target distance at 0.5 m/s. Median 1.01 ms,
mean distance to targets 107 um, clamped to 3.1 ms.

The usual implementation is a dense `[D, batch, n]` conductance ring, which
would roughly double the step's memory traffic — the one thing the profile said
we cannot afford. Because the delay is per cell rather than per synapse, the
ring can hold *spike indices* instead: 32 slots of 16k int32, 2 MB, and cost
proportional to spikes rather than to the population. Speed went from 2.37x to
1.42x realtime, and most of that is the always-on spike tally, not the delay.

### Background noise instead of a constant current

A constant drive cannot produce graded spontaneous activity: a cell is either
above threshold and fires forever or below it and never fires. That is exactly
the 81%-silent / 23 Hz-median split the earlier runs showed — it was an
artefact of the drive, not a property of the connectome. Background is now a
per-step Gaussian in the membrane kernel, calibrated to **0.97 Hz spontaneous**.
Mean rate under stimulation is 2.49 Hz, against 5.2 Hz with 81% silent before.

### Light enters backwards, which is correct

All 6,098 photoreceptors are histaminergic, and histamine is inhibitory in
Drosophila. Their targets are exactly the textbook ones — L1, L2, L3, Dm8,
Dm9, Mi1 — with mean weight -8.7, and T4/T5 correctly receive no direct input.
So a photoreceptor *holds its targets down* in darkness, and light releases
them. Driving photoreceptors is darkness, not light. The first version of the
protocol had this backwards and measured no response, because there was nothing
to suppress at a 1 Hz baseline.

Corrected protocol: photoreceptors held depolarised, light *lowers* the drive
on one eye, alternating every 250 ms.

| | response to light on a cell's own side |
|---|---|
| photoreceptors *(driven)* | -47.1 / -47.2 Hz |
| **lamina L1-L5** | **+0.057 / +0.060 Hz** |
| medulla Mi/Tm/Dm | +0.016 / +0.012 Hz |
| T4/T5 | ~0 |
| central brain | not distinguishable from noise |

Per hemisphere the lamina lateralises correctly, with opposite signs:
left-half +0.148 Hz, right-half -0.112 Hz on a ~0.4 Hz baseline, about 30%
modulation in the right direction.

**So the signal is real, correctly signed and correctly lateralised, and it
dies within one or two synapses.**

### Two measurement errors caught here, both mine

- The first "optic lobe +1.76 Hz" response was the stimulated photoreceptors
  themselves, counted inside the group they were supposed to be driving:
  2,106 cells at +39 Hz over 46,713 gives exactly the +1.78 observed. Response
  groups must exclude driven cells.
- Noise calibration reported 0.00 Hz at every amplitude because the spike tally
  only ran when frames were being recorded, and calibration recorded none.

### What this points at next

Not delays and not the input. The cells sit too far below threshold to pass
anything on: removing a few mV of inhibition from a cell resting well below
threshold changes little. A realistic network operates near threshold, where
fluctuations decide the output. Setting that operating point — excitation and
inhibition balanced so the population sits just under threshold — is the next
calibration, and it is what determines whether anything propagates past the
lamina.

## Reading the published model instead of guessing

The model this work reimplements is published with its parameters, and the
source is open. Checking ours against `default_params` in
github.com/philshiu/Drosophila_brain_model:

| parameter | published | ours was | source given there |
|---|---|---|---|
| resting potential | -52 mV | -52 mV | Kakaria & de Bivort 2017 |
| **reset potential** | **-52 mV** | **-55 mV** | same |
| threshold | -45 mV | -45 mV | same |
| membrane time constant | 20 ms | 20 ms | same |
| synaptic time constant | 5 ms | 5 ms | Jürgensen et al. |
| refractory period | 2.2 ms | 2.2 ms | Lazar et al., eLife |
| delay | 1.8 ms fixed | 1.01 ms from geometry | Paul et al. 2015 |
| **clear g on spike** | **yes** | **no** | — |
| **weight per synapse** | **0.275 mV** | **0.05 mV** | *"Free parameter"* |

Four matched, three did not. Reset below rest and the uncleared conductance
were plain errors and are fixed.

### The weight does not transfer, and it says so itself

The one parameter we were furthest from is the one the source model labels
`# Free parameter`: it was fitted, not measured, and fitted against FlyWire.
Applied to MaleCNS it saturates the network — 100% of Kenyon cells at 195 Hz —
because this dataset is denser: every released connection at confidence 0.5,
mean out-degree 153.5 against roughly 72, so one spike distributes about
120 mV across its targets against a 7 mV threshold.

Refitted against a measured invariant instead: an odour recruits only a few
percent of Kenyon cells.

| w_syn | Kenyon cells active | KC mean | network mean |
|---|---|---|---|
| 0.275 (published) | 100% | 188 Hz | 10.9 Hz |
| 0.100 | 21.4% | 5.5 Hz | 1.6 Hz |
| **0.075** | **5.6%** | **1.1 Hz** | **1.0 Hz** |
| 0.050 | 0.2% | 0.0 Hz | 0.5 Hz |

The same 0.075 comes out with the FlyWire >=5-synapse convention applied
(5.2%), so connection density alone is not the explanation.

### Vision was the wrong pathway, and not by our mistake

The fly's early visual system is largely **non-spiking**: photoreceptors and
the lamina monopolar cells L1-L3 signal with graded potentials. A leaky
integrate-and-fire network cannot represent them. This is why the published
spiking model of this brain was validated on taste and grooming rather than
vision, and why the visual system has a separate model built from graded
units. Our light experiments were fighting that.

### The olfactory pathway does work

Driving one glomerulus' receptor neurons as a Poisson source, at the refitted
weight:

- **ORN_DA1 -> DA1_lPN** appears among the top responders. The model located
  the correct glomerulus-specific projection neuron without being told the
  anatomy.
- Own-glomerulus selectivity: DA1 2x, VA1v 4x, DM1 6x above the median other
  projection neuron.
- **5.6% of Kenyon cells recruited** — the sparse-coding range that is
  measured experimentally.

Still wrong: absolute rates. Projection neurons reach 165-325 Hz and antennal
lobe local interneurons 350 Hz, which is far too hot, and that excess blurs
the labelled line — the own glomerulus leads by 2-6x where it should dominate.
Balancing excitation against inhibition is the next calibration, and the
lateral interneurons are where to start.
