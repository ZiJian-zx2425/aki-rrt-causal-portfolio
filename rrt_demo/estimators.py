"""Cross-fitted risk estimators and a separate weighted Cox working model."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .synthetic import FEATURES


def aipw_scores(a, y, e, m0, m1):
    e = np.asarray(e)
    if np.any((e <= 0) | (e >= 1)):
        raise ValueError("AIPW requires propensity strictly between zero and one.")
    return m1 - m0 + a * (y - m1) / e - (1 - a) * (y - m0) / (1 - e)


def crossfit(df, seed=2026, folds=5):
    x = df[FEATURES].to_numpy()
    a, y = df.treatment.to_numpy(), df.outcome_30d.to_numpy()
    e, m0, m1 = [np.empty(len(df)) for _ in range(3)]
    split = StratifiedKFold(folds, shuffle=True, random_state=seed)
    for k, (train, test) in enumerate(split.split(x, a)):
        ps = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                           LogisticRegression(C=100, max_iter=2000))
        ps.fit(x[train], a[train])
        e[test] = ps.predict_proba(x[test])[:, 1]
        for arm, destination in [(0, m0), (1, m1)]:
            selected = train[a[train] == arm]
            outcome = make_pipeline(SimpleImputer(strategy="median"),
                RandomForestRegressor(n_estimators=120, min_samples_leaf=25,
                                      max_depth=7, random_state=seed + k, n_jobs=1))
            outcome.fit(x[selected], y[selected])
            destination[test] = outcome.predict(x[test])
    return e, m0, m1


def stabilized_weights(a, e, cap_quantile=None):
    p = np.mean(a)
    w = np.where(a == 1, p / e, (1 - p) / (1 - e))
    if cap_quantile is not None:
        w = np.minimum(w, np.quantile(w, cap_quantile))
    return w


def balance(df, a, weights):
    rows = []
    for col in FEATURES:
        x = df[col].to_numpy()
        # Keep the unweighted pooled SD fixed across before/after comparisons.
        denom = np.sqrt((x[a == 1].var(ddof=1) + x[a == 0].var(ddof=1)) / 2)
        if denom == 0:
            raise ValueError("Constant covariate cannot have an SMD.")
        before = (x[a == 1].mean() - x[a == 0].mean()) / denom
        after = (np.average(x[a == 1], weights=weights[a == 1]) -
                 np.average(x[a == 0], weights=weights[a == 0])) / denom
        rows.append({"feature": col, "smd_before": before, "smd_after": after})
    return pd.DataFrame(rows)


def estimate(df, seed=2026):
    a, y = df.treatment.to_numpy(), df.outcome_30d.to_numpy()
    raw_e, m0, m1 = crossfit(df, seed)
    e = np.clip(raw_e, 0.01, 0.99)
    w = stabilized_weights(a, e)
    score = aipw_scores(a, y, e, m0, m1)
    se = score.std(ddof=1) / np.sqrt(len(score))
    estimate = score.mean()
    result = {
        "unadjusted_risk_difference": float(y[a == 1].mean() - y[a == 0].mean()),
        "ipw_risk_difference": float(np.average(y[a == 1], weights=w[a == 1]) -
                                     np.average(y[a == 0], weights=w[a == 0])),
        "aipw_risk_difference": float(estimate),
        "aipw_se": float(se), "aipw_ci95": [float(estimate - 1.96 * se), float(estimate + 1.96 * se)],
        "propensity_range": [float(raw_e.min()), float(raw_e.max())],
        "propensity_clipped_fraction": float(np.mean(e != raw_e)),
        "weight_max": float(w.max()),
        "ess_by_arm": {str(g): float(w[a == g].sum() ** 2 / (w[a == g] ** 2).sum()) for g in [0, 1]},
    }
    result["sensitivity"] = []
    for clip in [0.01, 0.025, 0.05]:
        ec = np.clip(raw_e, clip, 1 - clip)
        result["sensitivity"].append({"propensity_clip": clip,
            "aipw_risk_difference": float(aipw_scores(a, y, ec, m0, m1).mean()),
            "fraction_clipped": float(np.mean(ec != raw_e))})
    capped = stabilized_weights(a, e, 0.99)
    result["ipw_rd_weight_cap_99pct"] = float(
        np.average(y[a == 1], weights=capped[a == 1]) - np.average(y[a == 0], weights=capped[a == 0]))
    return result, e, w, balance(df, a, w)


def weighted_cox(df, weights):
    from lifelines import CoxPHFitter
    data = df[["treatment", "followup_days", "event"]].copy()
    data["weight"] = weights
    model = CoxPHFitter()
    model.fit(data, duration_col="followup_days", event_col="event",
              weights_col="weight", robust=True, formula="treatment")
    row = model.summary.loc["treatment"]
    return {"hazard_ratio": float(row["exp(coef)"]),
            "ci95": [float(row["exp(coef) lower 95%"]), float(row["exp(coef) upper 95%"])],
            "interpretation": "Weighted proportional-hazards working summary; not a risk ratio. "
                              "CI treats estimated weights as fixed. Heterogeneous simulated hazards need not be marginally proportional."}


def causal_forest(df, seed=2026):
    from econml.dml import CausalForestDML
    x = df[FEATURES].to_numpy()
    model = CausalForestDML(
        model_t=make_pipeline(StandardScaler(), LogisticRegression(C=100, max_iter=2000)),
        model_y=RandomForestRegressor(n_estimators=120, min_samples_leaf=25, random_state=seed, n_jobs=1),
        discrete_treatment=True, cv=3, n_estimators=200, min_samples_leaf=25,
        honest=True, random_state=seed, n_jobs=1)
    model.fit(df.outcome_30d.to_numpy(), df.treatment.to_numpy(), X=x)
    effects = model.effect(x)
    return {"mean_predicted_cate": float(effects.mean()),
            "interpretation": "Exploratory average of fitted CATE predictions, not the separately computed AIPW estimate."}
