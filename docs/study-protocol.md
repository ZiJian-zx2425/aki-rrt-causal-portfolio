# Study protocol

## Clinical target trial specification

This is a **design specification and implementation checklist**, not a claim that the original clinical analysis satisfied every item. The intended population is hospitalized adults who newly reach stage 3 AKI. The recorded research question compares initiation within an early window with no initiation during that window, allowing later treatment or no treatment in the comparator.

| Element | Target trial | Observational implementation requirement |
| --- | --- | --- |
| Eligibility | Adults with incident stage 3 AKI during hospitalization, before RRT initiation | Validate the AKI phenotype, baseline creatinine, prior RRT and dialysis status, and timestamps. Restrict using information available at eligibility. |
| Time zero | First qualifying stage 3 AKI decision time | Synchronize eligibility, strategy assignment, and follow-up. Do not replace negative treatment offsets with zero. |
| Strategy A | Initiate within 24 hours, with a prespecified initiation policy within the window | Define exact boundary, allowable treatment versions, urgent indications, and how treatment timing within the window is governed. A bare deadline is not a fully specified dynamic strategy. |
| Strategy B | No initiation in the first 24 hours; subsequent usual care | Distinguish this strategy from “never RRT.” Prespecify rescue treatment rules or exclude urgent indications at baseline, with clinical input. |
| Assignment | Randomize at time zero in the hypothetical trial | Observed future initiation is not baseline randomization. A grace-period-aware approach is required. |
| Outcome | Death from any cause within 30 days of time zero | Establish complete follow-up including after discharge; otherwise redefine the outcome or model censoring explicitly. Do not interpret missing death dates as proof of survival. |
| Follow-up | Time zero through death, 30 days, or genuine loss of observation | Discharge is not death and does not automatically provide a known 30-day mortality outcome. |
| Causal contrast | Difference in 30-day mortality risk under adherence to the two specified strategies | A per-protocol strategy contrast requires adherence and censoring adjustment. Do not label a future-defined exposure comparison intention-to-treat. |
| Analysis | Estimate standardized risks, risk difference, risk ratio, and survival curves | If using clone–censor–weight, model artificial and observation censoring, use longitudinal history available before decisions, and cluster uncertainty by original person. |
| Sensitivity | 72-hour window as an alternative target trial | Rebuild assignment and censoring rules for that protocol. Relabeling exposure alone does not solve grace-period bias. |

The original materials used hospitalization length and admission-day onset restrictions. A future design must check whether these can be known at time zero; a rule based on eventual length of stay can select on the future. ESKD, chronic dialysis, transplant status, and urgent indications need explicit definitions and verified implementation before clinical emulation.

## Proposed grace-period analysis, not implemented here

1. Define clinically coherent strategies, including what happens before the deadline, rescue indications, and deaths during the window.
2. At eligibility, create one copy per compatible strategy. Retain deaths occurring while a copy remains compatible; do not exclude early deaths because treatment was not yet received.
3. Censor a copy when observed treatment deviates from its assigned strategy. For example, a no-early-initiation copy deviates at early initiation; an early-initiation copy still untreated at its deadline deviates then, provided it remains alive and observed.
4. Estimate probabilities of remaining uncensored conditional on prior measured history. Accumulate inverse-probability weights over time; combine with observation-censoring weights where needed.
5. Estimate strategy-specific survival and 30-day risks. Use a patient-level bootstrap that repeats all nuisance fitting, cloning, and censoring, or another valid clustered variance procedure.
6. Inspect positivity, weight tails, balance over time, and sensitivity to model choices and window definitions.

This outline is not a drop-in clinical algorithm: a within-window initiation policy and full censoring models still have to be specified. The repository does **not** claim to implement cloning, sequential MSM weights, or time-varying confounding control.

## Executable synthetic protocol

The demo deliberately addresses a simpler, fully specified question:

- Generate four baseline covariates from declared distributions; no patient-derived parameters.
- At time zero, assign a binary treatment using a known logistic propensity depending on those covariates.
- Draw potential event times from exponential distributions with a heterogeneous treatment effect. Follow everyone through death or administrative censoring at 30 days.
- Estimate the 30-day risk difference, `E[Y(1)] - E[Y(0)]`, using IPW and AIPW. A positive value means more simulated events under treatment.
- There is no treatment grace period, switching, discharge censoring, or unmeasured confounding in this simulation. The known oracle risks provide a benchmark.

Baseline A=1/A=0 labels in the example are synthetic interventions; they must not be reinterpreted as a valid clinical early/delayed RRT assignment. This separation makes it possible to test estimators without misrepresenting a longitudinal TTE.

## Identification assumptions

Clinical causal interpretation requires well-defined treatment strategies and consistency, conditional exchangeability, positivity, accurate timing and measurement, appropriate handling of informative censoring, and no relevant interference. The synthetic generator satisfies these assumptions by construction for its baseline intervention. Successful simulation checks do not establish them in EHR data.

See [Hernán et al.](https://pubmed.ncbi.nlm.nih.gov/27237061/) on synchronization and design-related bias.
