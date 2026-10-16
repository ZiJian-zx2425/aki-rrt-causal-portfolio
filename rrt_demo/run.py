"""Run the synthetic-only demo: python -m rrt_demo.run --output demo_output."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from .synthetic import generate
from .estimators import estimate, weighted_cox, causal_forest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", type=Path, default=Path("demo_output"))
    parser.add_argument("--forest", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    df, oracle = generate(args.n, args.seed)
    result, e, w, balance = estimate(df, args.seed)
    result.update({"data_origin": "ENTIRELY SYNTHETIC; no patient-derived parameters",
        "n": args.n, "seed": args.seed, "estimand": "30-day risk difference: baseline A=1 minus A=0",
        "oracle_mean_risk_difference": float(np.mean(oracle["risk1"] - oracle["risk0"])),
        "cox": weighted_cox(df, w),
        "versions": {p: importlib.metadata.version(p) for p in ["numpy", "pandas", "scikit-learn", "lifelines"]}})
    if args.forest:
        result["causal_forest"] = causal_forest(df, args.seed)
        result["versions"]["econml"] = importlib.metadata.version("econml")
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    balance.to_csv(args.output / "balance.csv", index=False)
    # No row-level data or fitted models are exported, including synthetic rows.
    colors = ["#147D92", "#D7773B"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                         "axes.spines.right": False, "font.size": 10})
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), constrained_layout=True)
    a = df.treatment.to_numpy()
    for g in [0, 1]:
        axes[0].hist(e[a == g], bins=np.linspace(0, 1, 26), alpha=0.55, density=True,
                     label=f"Baseline A={g}", color=colors[g])
    axes[0].set(xlabel="Out-of-fold propensity", ylabel="Density", title="Overlap")
    axes[0].legend(frameon=False)
    yy = np.arange(len(balance))
    axes[1].scatter(balance.smd_before.abs(), yy, label="Unweighted", color=colors[1])
    axes[1].scatter(balance.smd_after.abs(), yy, label="Weighted", color=colors[0])
    axes[1].set_yticks(yy, balance.feature)
    axes[1].axvline(0.1, color="#9CA3AF", linestyle="--")
    axes[1].set(xlabel="Absolute standardized mean difference", title="Covariate balance")
    axes[1].legend(frameon=False)
    for g in [0, 1]:
        mask = a == g
        km = KaplanMeierFitter(label=f"Baseline A={g}")
        # Point curves only: naive KM variance is unsuitable for estimated IPTW.
        import warnings
        from lifelines.exceptions import StatisticalWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", StatisticalWarning)
            km.fit(df.followup_days[mask], df.event[mask], weights=w[mask])
        km.plot_survival_function(ax=axes[2], ci_show=False, color=colors[g])
    axes[2].set(xlabel="Days from baseline", ylabel="Survival", title="IPTW survival point estimates", ylim=(0, 1))
    axes[2].legend(frameon=False)
    fig.suptitle("SYNTHETIC DEMONSTRATION  |  Not clinical evidence", fontsize=16, fontweight="bold")
    fig.savefig(args.output / "diagnostics.png", dpi=200)
    fig.savefig(args.output / "diagnostics.svg")
    plt.close(fig)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
