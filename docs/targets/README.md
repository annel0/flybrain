# Fitting targets

Measured invariants of the *Drosophila* nervous system that a model should
reproduce, collected with the measurement protocol that produced each one.

The point of the protocol column is that we compare like with like: if a number
came from calcium imaging at 5 Hz with a dF/F threshold, our extractor must
convolve spikes with the indicator, downsample, and apply the same threshold,
rather than reading an instantaneous rate out of the simulator. A target
without its measurement method is not usable.

## Priority

**Perturbation results outrank steady-state numbers.** "Silencing X raises Y"
pins a causal relation that a global rescaling cannot fake; "Y equals 5%" is
one number many parameter sets can hit. Collect perturbations first.

## Format

One entry per target, in the file for its domain:

```markdown
### T-<domain>-<n>  <short name>

- **Quantity** — what is measured, in one line
- **Value** — number, with spread and N if reported
- **Type** — perturbation | steady-state | dynamic response
- **Method** — recording technique, indicator, sampling rate, window
- **Observation model** — what our extractor must replicate to compare fairly
  (threshold, integration time, subsampling, baseline subtraction)
- **Conditions** — preparation, temperature, sex, age, anaesthesia, behaviour
- **Source** — authors, year, journal, link
- **Confidence** — high / medium / low, and any conflict with other reports
```

Where two papers disagree, record **both** and say so. A conflict is
information: it sets the tolerance, and a target whose true value is disputed
must not be given a tight one.
