# IPM-PDEBench-PB1-Q2 Results — Temporal Identification Contract Qualification

Formal decision: **NO 500-EPOCH RUN AUTHORIZED**

Result ZIP SHA256:
`9caf42aa0bc38cc1ac1ebfe17d541260878862169ba28109ab577ec396052c42`

Executed notebook SHA256:
`d8b5cc645f41d6090d3c4b9e240e63799606747443705ef970d245ebde222a5f`

Frozen notebook SHA256:
`5e93a488d31fc9d6e7f8f670b34c04aaa35e0b5d8abeb60f45313e7064e1a4cb`

All 7 code cells are byte-for-byte identical to the frozen notebook. The detached manifest contains 21 entries and all 21 match the archived file bytes.

## Formal hypothesis report

- H_TEMPORAL_SUPPORTED: **false**
- H_LONGSTRIDE_SUPPORTED: **false**
- H_LOADER_REFUTED: **true**
- H_COMPILER_NOT_PRIMARY: **false**
- FORMAL_500_EPOCH_RUN_AUTHORIZED: **false**
- SELECTED_VARIANT: **null**

## Main finding

Fine temporal sampling strongly improves the trajectory-identification objective, but this improvement does not translate into a sufficiently better compiled 8-step physical rollout.

### Advection beta=1

Control `T5_S124_CONTROL`:
- final/first loss ratio: **0.98317**
- held-out integral residual: **0.97562**
- common 8-step rollout Rel-L2: **0.82086**
- compiler defect: **0.06946**

Native-time variants:
- `T1_S124_NATIVE`: loss ratio **0.25498**, integral residual **0.22699**, rollout **0.93268**, compiler defect **0.55447**
- `T1_S111_NATIVE_LOCAL`: loss ratio **0.20586**, integral residual **0.17627**, rollout **0.90634**, compiler defect **0.48012**

Thus native temporal sampling improves the fitted integral objective by ~4-5x, but the current principal compiler loses ~48-55% of the full IDTC characteristic and physical rollout gets worse.

Physical-window match:
- `T1_S5_10_20_PHYSICAL_MATCH` rollout **0.82078**
- control rollout **0.82086**
- corresponding integral residuals **0.97564** and **0.97562**

These are nearly identical.

### Burgers nu=0.01

Control:
- loss ratio **0.93006**
- integral residual **0.93155**
- rollout **0.31096**
- compiler defect **0.79346**

Native:
- `T1_S124_NATIVE`: loss ratio **0.42865**, integral residual **0.39353**, rollout **0.28042**, compiler defect **0.42257**
- `T1_S111_NATIVE_LOCAL`: loss ratio **0.27088**, integral residual **0.20103**, rollout **0.27392**, compiler defect **0.39043**

Fine time improves Burgers rollout modestly (~10-12%) and substantially improves the integral objective, but still fails the preregistered >=40% rollout-improvement gate.

The coarse-time local variant `T5_S111_LOCAL` is unstable at the compiled-flow level (8-step Rel-L2 ~1065.7) despite a lower integral residual than the T5 control.

Physical-window match:
- `T1_S5_10_20_PHYSICAL_MATCH` rollout **0.30916**
- control **0.31096**

Again the behavior is nearly identical.

## Interpretation

The loader representation is not the dominant problem. Raw-time samples with physically matched 5/10/20-step windows reproduce the reduced-time 1/2/4 behavior very closely.

Therefore the important variable is the physical identification window, not whether the tensor was materialized with temporal reduction 1 or 5.

However, simply shortening the physical window also does not solve the public-benchmark problem:
- it improves the Simpson objective dramatically;
- it makes the full IDTC use substantially more non-principal differential algebra;
- the current principal RTDS compiler no longer preserves the learned characteristic closely;
- the compiled rollout consequently fails to realize the optimization gain.

## Critical next question

PB1-Q3 must separate:
1. whether the full learned IDTC characteristic itself is physically correct;
2. whether the principal compiler is discarding useful learned differential algebra;
3. whether the dominant remaining error is only a train-only amplitude/role calibration problem.

The next qualification should therefore compare, on training-only validation:
- full IDTC vs central-secant characteristic;
- unit-gain principal RTDS vs central-secant characteristic;
- training-only ridge-calibrated R/T/D/S principal roles vs central secant;
- full-IDTC flow vs principal compiled flow vs calibrated compiled flow.

No new 500-epoch run is authorized until this closes.
