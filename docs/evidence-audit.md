# Evidence and TTE audit

Reviewed locally on 2026-10-16. The review inspected report text, slide text, and selected source cells inside an archived course project. It did not execute restricted clinical data, validate all stored notebook outputs, or establish publication rights to the original materials. The report was available as a previously saved Overleaf source snapshot; its current online revision was not verified.

## Evidence ledger

| Claim | Evidence | Public wording |
| --- | --- | --- |
| UF Causal AI course project on RRT timing in severe AKI | Final-presentation materials and report agree on subject and author | Course project investigating early versus delayed/no RRT |
| Clinical time zero and timing windows | Report specifies stage 3 onset, a 24-hour primary window, 72-hour alternative, and 30-day endpoint | Documented design intent |
| Longitudinal preprocessing | Archived source builds daily rows and aligns AKI and treatment dates | Temporal feature engineering was explored |
| Propensity weighting and survival modeling | Selected final-analysis cells use regularized logistic propensity and weighted Cox fitting | Baseline propensity-weighted Cox analysis is supported |
| Causal machine learning | Archived homework/analysis cells instantiate CausalForestDML | Causal forest exploration is supported |
| Fully implemented sequential MSM | Report describes daily weights; reviewed final-analysis cells subset to baseline | Not verified; do not claim completed time-varying adjustment |
| Cloning and artificial-censoring weights | No implementation established in reviewed source | Proposed extension only |
| Clinical effect estimates | Report and slides contain estimates, with version disagreement in ATE values | Excluded from this public release; not independently reproduced |

## Material discrepancies and design risks

1. **Grace-period assignment.** A final-analysis function labels early treatment using future initiation while follow-up is aligned to AKI onset. Without a suitable strategy-assignment procedure, this can misalign assignment and follow-up. Changing a cutoff from one day to three does not address the design problem.
2. **Time resolution.** Calendar-day differences do not establish exact 24-hour or 72-hour elapsed windows. Within-day covariates may also occur after treatment. Exact boundary rules and timestamp resolution need verification.
3. **Prevalent treatment.** A reviewed preprocessing function clamps negative offsets to zero. Pre-baseline RRT must instead trigger eligibility review; it cannot be converted into incident treatment at time zero.
4. **Covariate timing.** A reviewed creatinine alignment step chooses a nearest measurement using absolute time difference. That can select a post-onset measurement; the baseline measurement window must be restricted explicitly.
5. **Outcome and follow-up.** Missing death dates are replaced with a future date in reviewed source, while report follow-up can end at discharge. Neither establishes complete post-discharge all-cause mortality ascertainment.
6. **MSM specification.** Daily stabilized weighting is described in the report, but reviewed final Cox code uses baseline rows, a single propensity weight, a penalty, and additional covariates. That is not evidence of a sequential treatment-weight product. The reviewed Cox input also retains an identifier outside the explicit cluster field, requiring a feature-exclusion audit.
7. **Weight truncation.** The report describes both-tail truncation; the reviewed final code caps only the upper tail. The public demo specifies its actual rules separately.
8. **Survival estimator.** The report calls the curves Kaplan–Meier, while reviewed source averages Cox-predicted survival under treatment overrides. These are different estimators.
9. **Forest versus AIPW.** Original materials use both labels; reviewed forest cells compute CausalForestDML effects or their mean. That alone does not establish execution of the report's explicit AIPW equation. The public demo implements and labels these separately.
10. **Result lineage.** Two presentation versions contain different ATE values, and multiple notebooks exist. A canonical analysis version and input provenance must be established before reporting clinical estimates.
11. **Imputation and preprocessing.** Reviewed source uses a single deterministic iterative imputation, not pooled multiple-imputation inference. Some exploratory ML cells scale data before splitting and use a binary SMD formula across standardized continuous features. The new demonstration fits transformations within folds and uses a continuous-compatible SMD definition.

These observations apply to the inspected source paths and versions. Other unreviewed analyses may differ. A correction plan should trace each estimate to an immutable code version and an authorized input cohort before making stronger claims.

## TTE naming decision

Use **“Target trial design and causal ML for RRT timing”** or **“TTE-oriented methods portfolio.”** The original title used TTE, but a title alone does not validate implementation. This release must not be described as a completed clinical TTE, a replication of the reference paper, or evidence that early RRT causes harm or benefit.

## What would upgrade the claim

Verify the clinical phenotype and exact timestamps; lock a fully specified target protocol; implement compatible assignment and censoring rules; establish outcome capture; audit all feature timing; validate sequential weights where applicable; reproduce results from approved data in the authorized environment; reconcile report and source; and obtain any required institutional release clearance. None of those requirements can be replaced by a successful synthetic run.
