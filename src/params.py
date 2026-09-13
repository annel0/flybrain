"""Published model parameters, with the source for each one.

These are not our choices. They are the constants used by Shiu et al.,
Nature 2024, "A Drosophila computational brain model reveals sensorimotor
processing", taken from the accompanying implementation at
github.com/philshiu/Drosophila_brain_model (model.py, `default_params`).
Each carries the citation that paper gives for it.

We had reconstructed four of these correctly and three wrongly; the wrong ones
are noted, because they explain a result. Weight per synapse in particular was
5.5x too weak here, which is why a light response died within one synapse.
"""

# Kakaria and de Bivort 2017, https://doi.org/10.3389/fnbeh.2017.00008
V_REST_MV = -52.0          # resting potential
V_RESET_MV = -52.0         # reset after a spike -- equal to rest, NOT below it
V_THRESH_MV = -45.0        # spike threshold
TAU_MEMBRANE_MS = 20.0     # capacitance 0.002 uF x resistance 10 Mohm

# Jürgensen et al., https://doi.org/10.1088/2634-4386/ac3ba6
TAU_SYNAPSE_MS = 5.0

# Lazar et al., eLife, https://doi.org/10.7554/eLife.62362
REFRACTORY_MS = 2.2

# Paul et al. 2015, https://doi.org/10.3389/fncel.2015.00029
DELAY_MS = 1.8             # one fixed post-synaptic delay for every connection

# Free parameter in the source paper -- fitted there, not measured, and
# fitted against FlyWire. It does not transfer to this dataset: MaleCNS keeps
# every released connection at confidence 0.5, mean out-degree 153.5 against
# roughly 72, so one spike distributes ~120 mV across its targets against a
# 7 mV threshold. At 0.275 the network saturates: 100% of Kenyon cells at
# 195 Hz. Refitted here against sparse coding in the mushroom body, which is
# measured and independent of the quantity being fitted.
PUBLISHED_WEIGHT_PER_SYNAPSE_MV = 0.275
WEIGHT_PER_SYNAPSE_MV = 0.075       # gives 5.6% Kenyon cell recruitment
WEIGHT_REFIT_NOTE = (
    "0.075 mV chosen so that driving one glomerulus' receptor neurons "
    "recruits 5.6% of Kenyon cells; the same value comes out whether or not "
    "the FlyWire >=5-synapse convention is applied, so connection density "
    "alone does not explain the difference from 0.275.")

# Optogenetic activation in that model is Poisson spiking, not a step current.
POISSON_RATE_HZ = 150.0
POISSON_SCALE = 250.0      # weight = WEIGHT_PER_SYNAPSE_MV * POISSON_SCALE

# On a spike their model sets `v = v_rst; w = 0; g = 0*mV` -- the synaptic
# conductance is cleared as well, which we had not been doing.
RESET_CONDUCTANCE_ON_SPIKE = True

# Their network has no background noise: it is silent until something is
# stimulated. Ours adds noise to obtain spontaneous activity, which is a
# departure and has to be reported as one.
BACKGROUND_NOISE = "not present in the published model"

CITATION = ("Shiu, Sterne et al., Nature 634:210-219 (2024); "
            "code github.com/philshiu/Drosophila_brain_model")
