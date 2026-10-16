# Methodology

## Three distinct layers

The course evidence supports propensity modeling, weighted Cox analysis, temporal preprocessing, and causal-forest exploration. The public demo implements a new, auditable baseline-treatment analysis. The clinical protocol describes requirements for a future longitudinal TTE. Results or capabilities must not be transferred between these layers.

## Synthetic data-generating process

Let `X = (age_z, severity, renal_marker, comorbidity)`. The first three variables are independent standard normal draws; comorbidity is Bernoulli with probability 0.35. These names are illustrative and do not encode a clinical severity instrument or calibrated laboratory measurement.

```
e(X) = expit(-0.3 + 0.25 age_z + 0.7 severity + 0.4 renal_marker + 0.3 comorbidity)
lambda_0(X) = exp(-4.4 + 0.25 age_z + 0.55 severity + 0.35 renal_marker + 0.3 comorbidity)
lambda_1(X) = lambda_0(X) * exp(-0.35 + 0.20 severity)
T(a) = E / lambda_a(X), where E ~ Exponential(rate=1)
Y(a) = 1[T(a) <= 30]
mu_a(X) = 1 - exp(-30 lambda_a(X))
```

The oracle benchmark is the mean of `mu_1(X) - mu_0(X)` over the generated covariates. Observed treatment is Bernoulli with probability `e(X)`, independent of the event-time draw given X. All coefficients were chosen for this educational example, not fitted to EHR data. Oracle quantities are stored separately and never supplied as model features.

## Nuisance estimation and cross-fitting

Five treatment-stratified folds produce held-out predictions for every observation. Each fold fits a scaled logistic propensity model and separate random-forest outcome regressions within each treatment arm. Imputation and scaling are fitted only on the training fold; the default generator has no missing values. An explicit feature allowlist excludes treatment, outcome, follow-up, identifiers, and oracle quantities.

The implementation clips held-out propensity estimates to `[0.01, 0.99]` and reports the fraction affected. Clipping controls numerical instability but may introduce bias; it does not establish overlap. Additional thresholds are sensitivity analyses, not evidence that positivity holds.

## IPW and diagnostics

For treatment prevalence `p`, stabilized weights are:

```
w_i = A_i p/e_i + (1-A_i)(1-p)/(1-e_i)
```

The IPW risk difference subtracts the weighted mean outcome in A=0 from the weighted mean in A=1, normalizing within each arm. The primary demo does not cap these weights; a separate 99th-percentile-cap comparison is reported.

Balance uses the difference in means divided by the **unweighted pooled standard deviation**, with that denominator fixed for before/after comparisons. This formula works for both the continuous covariates and the binary comorbidity indicator. Effective sample size in each arm is `(sum w)^2 / sum(w^2)`. Overlap histograms, maximum weights, clipping fractions, and absolute standardized mean differences complement the effect estimate. An SMD threshold such as 0.1 is a diagnostic convention, not proof of exchangeability.

## Cross-fitted AIPW

For observed binary outcome Y and fitted conditional risks m0 and m1:

```
psi_i = m1_i - m0_i
        + A_i (Y_i - m1_i) / e_i
        - (1-A_i) (Y_i - m0_i) / (1-e_i)
ATE_hat = mean(psi)
SE_hat = sd(psi) / sqrt(n)
```

The interval is `ATE_hat ± 1.96 SE_hat`, an asymptotic influence-function interval for independent observations under nuisance-estimation regularity conditions. It is not a finite-sample guarantee. Clipping can affect the target approximation; poor overlap or nuisance fits can undermine coverage. The tests verify expected large-sample double robustness with oracle nuisances and a deliberately misspecified alternative, plus recovery with fitted models on a fixed synthetic sample. They do not validate clinical conclusions or certify interval coverage.

## Weighted survival analysis

A treatment-only Cox model uses stabilized baseline weights and robust variance. No identifier can enter its formula. Its hazard ratio is a working proportional-hazards summary; it is not a risk ratio or the AIPW risk difference. The generator has effect heterogeneity, so marginal hazards need not be proportional. The reported Cox interval treats fitted weights as fixed and does not incorporate all nuisance-estimation uncertainty.

The plotted survival curves are weighted Kaplan–Meier **point estimates**, without confidence bands. Their construction is separate from model-standardized Cox predictions. Original materials mixed these descriptions; this implementation labels the actual estimator explicitly. These baseline weights do not adjust for time-varying confounders or informative discharge.

## Optional causal forest

The optional EconML CausalForestDML component uses internally cross-fitted nuisance models and honest trees. It estimates a conditional effect function in the synthetic baseline problem. The output is the average of fitted CATE predictions, explicitly labeled exploratory. It is not the separately computed AIPW estimate, and it has no claimed confidence interval in this demo. A CATE is a conditional average, not an observed individual treatment effect or a clinical treatment recommendation.

## Clinical analysis gaps

Baseline balancing cannot repair future-defined treatment assignment, post-baseline covariates, missing mortality ascertainment, unmeasured severity, or ill-defined strategies. A longitudinal analysis requires a different data structure and analysis plan. See the [evidence audit](evidence-audit.md) and [protocol](study-protocol.md).
