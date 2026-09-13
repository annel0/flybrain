"""The measured quantities a fitted model has to reproduce.

Each target carries the value, a tolerance, and the id of the entry in
docs/targets/ that it came from, so every number here is traceable to a paper
rather than to us. Tolerances are deliberately loose where the sources
disagree or report a bound rather than a value -- a disputed quantity must not
be given a tight tolerance, or the fit will chase noise.

`fit` targets drive the optimisation. `holdout` targets are never shown to the
optimiser and are scored afterwards. Without that split, fitting N parameters
against N observables reproduces exactly what it was told and demonstrates
nothing.

Direction targets carry `at_least` or `at_most` rather than a value, because
some of the strongest constraints are causal statements rather than numbers:
"blocking APL raises Kenyon cell recruitment a lot" cannot be faked by a
global rescaling the way a single rate can.
"""

TARGETS = [
    # ---- mushroom body -------------------------------------------------
    dict(id="T-MB-13", obs="kc_recruited_pct", value=6.0, tol=5.0, split="fit",
         note="6 +- 5% of KCs respond to an odour, n=71, electrophysiology, "
              "3.5 SD threshold. T-MB-17 says explicitly: loose tolerance."),
    dict(id="T-MB-01/02", obs="apl_block_delta_pp", at_least=20.0, tol=10.0,
         split="fit",
         note="blocking APL raises KC odour response and reduces sparseness. "
              "A direction, which a global rescaling cannot produce."),
    dict(id="T-MB-09", obs="apl_rate_hz", at_most=5.0, tol=5.0, split="fit",
         note="APL does not fire action potentials. Our spiking APL should at "
              "least not run hot; a graded APL would satisfy this exactly."),
    dict(id="T-WB-3", obs="kc_baseline_hz", at_most=0.5, tol=0.5, split="fit",
         note="Kenyon cells are close to silent at baseline, by circuit design."),

    # ---- antennal lobe --------------------------------------------------
    dict(id="T-AL-16", obs="pn_peak_hz", value=160.0, tol=60.0, split="fit",
         note="Rmax fitted per glomerulus: 170, 167, 163, 144 spikes/s. "
              "Tolerance spans the spread plus room for our different drive."),
    dict(id="T-MB-02", obs="kc_odor_overlap", at_most=0.3, tol=0.2, split="holdout",
         note="two different odours recruit largely non-overlapping Kenyon cell "
              "populations; blocking APL raises the correlation between them. "
              "Held out because it tests the mushroom body's function rather "
              "than any firing rate, so nothing in the fitted set implies it."),
    dict(id="T-AL-19", obs="ln_rate_hz", at_most=60.0, tol=40.0, split="holdout",
         note="a substantial population of antennal lobe local interneurons "
              "does not spike at all; the fraction is not quantified. Held out "
              "because our 227 Hz is so far off that fitting to it would "
              "dominate everything else."),

    # ---- brain-wide -----------------------------------------------------
    dict(id="T-WB-2", obs="pn_gap_in_sd", at_most=3.0, tol=2.0, split="fit",
         note="projection neurons rest close to spike threshold. No published "
              "number exists in fluctuation widths, so this encodes 'close' "
              "loosely. Moved into the fitted set after the first run left "
              "membranes 11 widths from threshold while satisfying everything "
              "it was shown."),
    dict(id="T-WB-1", obs="silent_fraction_pct", at_most=60.0, tol=20.0,
         split="fit",
         note="no brain-wide rate distribution has ever been measured, so this "
              "is not a measurement -- it encodes only that a brain in which "
              "four cells in five never fire is not a plausible resting state. "
              "Moved into the fitted set after the first run met every fitted "
              "target while leaving 90% of the network silent."),
    dict(id="internal", obs="spontaneous_hz", value=1.0, tol=1.5, split="fit",
         note="not from a paper: the order of magnitude implied by the "
              "per-cell-type recordings we do have. Marked internal so it is "
              "never cited as measured."),
]


def fit_targets():
    return [t for t in TARGETS if t["split"] == "fit"]


def holdout_targets():
    return [t for t in TARGETS if t["split"] == "holdout"]


def score(target, value):
    """Normalised miss: 0 when satisfied, growing in units of the tolerance."""
    if value is None or value != value:            # None or NaN
        return 10.0                                # a failed run is a bad one
    tol = max(target.get("tol", 1.0), 1e-9)
    if "value" in target:
        return abs(value - target["value"]) / tol
    if "at_least" in target:
        return max(0.0, target["at_least"] - value) / tol
    if "at_most" in target:
        return max(0.0, value - target["at_most"]) / tol
    raise ValueError(f"target {target['id']} has no value, at_least or at_most")


# Parameter space. Bounds come from the literature where it gives them and
# from plain plausibility where it does not; `log` marks parameters searched
# on a log scale because they span orders of magnitude.
PARAMS = [
    dict(name="w_syn", lo=0.005, hi=5.0, log=True,
         note="published 0.275 (fitted there, against a female connectome); "
              "our earlier fit 0.075. Ceiling raised from 1.0 after the first "
              "run pressed against it"),
    dict(name="inh_gain", lo=0.5, hi=40.0, log=True,
         note="inhibition relative to excitation per synapse; balanced-network "
              "models commonly use 4-8. Ceiling raised from 16 after the first "
              "run pressed against it"),
    dict(name="tau_syn", lo=1.0, hi=15.0, log=False,
         note="published 5 ms; ionotropic GABA and GABA-B differ by 10-100x, "
              "which one constant cannot represent"),
    dict(name="v_th", lo=4.0, hi=12.0, log=False,
         note="published threshold sits 7 mV above rest"),
    dict(name="sigma", lo=0.0, hi=0.4, log=False,
         note="background noise. Ours, not the published model's, which has "
              "none -- so it is fitted rather than assumed"),
    dict(name="tau_mem", lo=5.0, hi=60.0, log=False,
         note="published 20 ms, applied to every cell. Floor lowered from 10 "
              "after the first run pressed against it"),
    dict(name="delay_ms", lo=0.8, hi=2.0, log=False,
         note="the published 1.8 ms is one number for every connection, but "
              "measured giant-fibre latencies are 0.93-1.46 ms across one "
              "synapse and 1.44-1.85 ms across two, so a hop costs far less "
              "than the base. Bounded by those measurements"),
    dict(name="tau_mem_kc", lo=150.0, hi=500.0, log=False,
         note="Kenyon cells are measured at >200 ms, a lower bound. Searched "
              "below it too, so the fit can disagree with the measurement "
              "visibly rather than silently"),
]
