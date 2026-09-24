# IPM-PDEBench-PB1-Q4 — Native-Flow Gain Closure Qualification

## Motivation

PB1-Q3-FIX1 validated the gain-aware runtime and showed that four train-only principal-role gains strongly improve both characteristic agreement and actual compiled rollout.

The only frozen gate failure is the absolute Advection 8-step rollout threshold:
- T1_S111_NATIVE_LOCAL: 0.527312
- T1_S124_NATIVE: 0.550621
- required: <= 0.50

All relative calibration/rollout gates pass on both PDEs, and Burgers is already below 0.20.

PB1-Q4 therefore tests one narrowly defined remaining hypothesis:

> The remaining error is caused by calibrating the four role gains against an infinitesimal central-secant proxy while deployment uses a discrete native compiled flow.

PB1-Q4 does not expand the principal algebra and does not increase training scale.

## Frozen data contract

Official PDEBench:
- Advection beta=1
- Burgers nu=0.01

Inside the official 90% training block:
- IDTC fit: first 1000 trajectories
- flow/gain calibration: next 128 trajectories
- validation: next 256 trajectories

Official held-out test data are not accessed.

Spatial reduction: 4.

IDTC identification uses native raw time.

Candidates:
- `T1_S111_NATIVE_LOCAL`: strides (1,1,1)
- `T1_S124_NATIVE`: strides (1,2,4)

Per fit:
- seed 202
- 20 epochs
- batch 50
- 400 optimizer updates
- Adam lr 1e-3
- weight decay 1e-4

## Native-flow closure

First reproduce the Q3-FIX1 central-secant four-gain calibration.

Then construct a differentiable instance of the exact repository `IPMStep`.

Frozen during closure:
- all IDTC parameters;
- all principal polynomial coefficients;
- RTDS mask;
- native split execution order.

Trainable:
- only `g_R, g_T, g_D, g_S`.

Initialization:
- Q3-FIX1 central-secant gains.

Flow-refinement schedule:
- 160 updates
- 16 calibration trajectories/update
- 4-step compiled rollout
- Adam lr 0.02
- gain absolute clip: 6

Objective:
- normalized exact compiled 4-step rollout loss;
- + 0.25 normalized central-secant preservation loss;
- + 0.002 relative gain-prior penalty around the Q3-FIX1 secant-calibrated gains.

No exact PDE RHS, known PDE coefficient, equation-specific pruning, or test data are used.

## Semantic qualification

Before science:
1. non-unit gains must alter the runtime output;
2. runtime-gain execution must agree with gain-folded polynomial coefficients within `2e-6`;
3. gradients through the compiled flow with respect to gains must be finite and non-zero.

Failure stops the experiment.

## Formal gate

A candidate passes only if both PDEs satisfy:

- finite fit and rollout;
- runtime parity defect <= 2e-6;
- refined 8-step validation rollout Rel-L2 <= 0.50;
- per-task refined/baseline rollout ratio <= 1.10;
- refined central-secant error / secant-gain baseline <= 1.15;
- max absolute gain <= 6;

and across the two PDEs:

- geometric-mean refined/baseline rollout ratio <= 0.99.

If both candidates pass, select the one with lower geometric-mean refined 8-step rollout error.

If neither candidate passes:
- no 500-epoch run is authorized;
- the next phase must upgrade the principal algebra / normal-form closure rather than repeat scalar gain tuning.

## Interpretation policy

A PB1-Q4 pass means the same four-scalar principal closure is sufficient once calibrated against its actual discrete native flow.

A PB1-Q4 fail means the remaining error cannot be closed by role amplitudes alone and requires a richer compiled algebra or a revised normal-form contract.
