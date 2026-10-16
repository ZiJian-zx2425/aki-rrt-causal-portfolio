# Reproducibility

Run commands from the repository root. The example requires no data download, login, secret, database connection, or institutional access. Package installation is the only network-dependent step.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m rrt_demo.run --n 4000 --seed 2026 --output demo_output
```

On Windows activate with `.venv\Scripts\activate` instead. To run the optional forest, install `requirements-forest.txt` and add `--forest` to the analysis command. The forest dependency has native numerical dependencies; the core demo remains usable without it.

## Outputs

| File | Meaning |
| --- | --- |
| `summary.json` | Seed, sample size, package versions, oracle contrast, unadjusted/IPW/AIPW estimates, interval, weighting diagnostics, sensitivity results, Cox summary, and optional forest summary |
| `balance.csv` | Before/after standardized mean differences using a fixed unweighted denominator |
| `diagnostics.png` / `.svg` | Propensity overlap, balance, and weighted survival point estimates |

Every value is synthetic. The oracle is a mean conditional risk difference for the generated covariates, not an estimate from patient records. Tests compare estimators to the appropriate risk contrast; Cox HR is a different estimand and is not expected to numerically match it.

## Determinism and environment

Seeds are explicit and model parallelism is restricted to one worker. Numerical details may vary by Python, platform, and dependency versions. Direct dependencies are pinned in the requirements files. `environment-tested.txt` records the local resolved environment and is a reproducibility record, not a promise of cross-platform wheel availability. The generated JSON records key versions for each run.

## Validation scope

Tests cover deterministic simulation, administrative censoring, double robustness with oracle nuisances, fitted-model recovery under known truth, continuous-feature SMD scale invariance, and timeline rejection/boundaries. The optional forest is exercised by a full example run. These checks are synthetic statistical and software checks; they do not validate the original clinical analysis, the full TTE protocol, or confidence-interval coverage.

The AIPW interval is asymptotic. Cox uncertainty treats estimated weights as fixed. The survival curves intentionally have no uncertainty bands. Forest predictions are exploratory and do not come with a claimed aggregate-effect interval.

## Rebuild figures and review the release

```bash
python scripts/draw_workflow.py
python scripts/check_release.py
```

Re-rendered images may differ in metadata or layout between environments; if hashes change, review the images and update the release manifest before a new release. The provided manifest verifies this release, not arbitrary generated outputs. `demo_output/`, caches, and virtual environments are excluded from the release payload.
