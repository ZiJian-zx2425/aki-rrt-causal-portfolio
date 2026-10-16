"""Generate records entirely from a declared mathematical model."""
import numpy as np
import pandas as pd

FEATURES = ["age_z", "severity", "renal_marker", "comorbidity"]


def generate(n=4000, seed=2026):
    if n < 200:
        raise ValueError("Use at least 200 synthetic observations.")
    rng = np.random.default_rng(seed)
    age, severity, renal = rng.normal(size=(3, n))
    comorb = rng.binomial(1, 0.35, n)
    x = np.column_stack([age, severity, renal, comorb])
    propensity = 1 / (1 + np.exp(-(-0.3 + 0.25 * age + 0.7 * severity
                                  + 0.4 * renal + 0.3 * comorb)))
    a = rng.binomial(1, propensity)
    hazard0 = np.exp(-4.4 + 0.25 * age + 0.55 * severity + 0.35 * renal + 0.3 * comorb)
    hazard1 = hazard0 * np.exp(-0.35 + 0.20 * severity)
    # Shared random variate defines a joint potential-outcome simulation.
    exponential = rng.exponential(size=n)
    t0, t1 = exponential / hazard0, exponential / hazard1
    event_time = np.where(a == 1, t1, t0)
    df = pd.DataFrame(x, columns=FEATURES)
    df["treatment"] = a
    df["outcome_30d"] = (event_time <= 30).astype(int)
    df["followup_days"] = np.minimum(event_time, 30)
    df["event"] = df["outcome_30d"]
    # Oracle information is separate and never enters an estimator's feature set.
    oracle = {"propensity": propensity, "risk0": 1 - np.exp(-30 * hazard0),
              "risk1": 1 - np.exp(-30 * hazard1)}
    return df, oracle
