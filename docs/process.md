# End-to-end process

## 1. Establish the evidence boundary

Review course slides, report, and code in place. Record design claims separately from implemented operations. Do not copy archives, notebooks, embedded figures, model objects, or clinical tables into the public project. The 2022 reference informs the question; it does not establish the user's methods or results.

## 2. Translate the question into a protocol

Specify eligibility, time zero, strategies, follow-up, outcomes, estimand, and analysis. Track which elements are supported by the course record and which remain proposals. Resolve daily-versus-hourly timing, delayed-versus-never-treated terminology, and urgent treatment exceptions before interpreting a clinical contrast.

## 3. Build an independent synthetic example

Generate baseline covariates, confounded treatment assignment, and potential event times from explicit equations. Use fixed seeds. Keep oracle risks outside the estimator feature matrix. The generator reads no patient file and does not learn distributions from restricted records.

## 4. Estimate and diagnose

Use held-out nuisance predictions for IPW and AIPW. Inspect overlap, balance, effective sample size, clipping, and weight tails. Estimate a separate Cox working summary and weighted survival point curves. Optionally fit a causal forest to demonstrate heterogeneous-effect modeling.

## 5. Challenge the analysis

Compare with the known synthetic risk contrast, vary clipping thresholds, compare a weight-cap sensitivity, test temporal boundary failures, and check recovery with a separate fixed sample. Investigate discrepancies rather than interpreting agreement among models as causal proof.

## 6. Publish only reviewed artifacts

Release the newly written documentation, synthetic code, schematic figures, and aggregate synthetic outputs. A checksum manifest fixes the reviewed payload; the release checker fails on altered or unexpected files. It is a packaging guard, not an automated certification that arbitrary future content is safe.

## 7. Keep clinical research separate

Any future clinical adapter, result reproduction, or longitudinal emulation must run in the approved research environment. Its outputs need their own review. Adding a data loader or copying a source notebook is outside the current public release boundary.
