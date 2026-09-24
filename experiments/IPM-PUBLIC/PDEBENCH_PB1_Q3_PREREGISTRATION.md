# IPM-PDEBench-PB1-Q3 — Characteristic Closure and Train-Only Gain Calibration Qualification

## Purpose

PB1-Q2 showed that native fine-time sampling substantially reduces the Simpson trajectory-identification loss, but the improvement does not survive the current principal RTDS compilation.

The compiler defect for the two architecture-native candidates was ~0.39-0.55, far above the preregistered 0.05 tolerance.

PB1-Q3 separates three questions before any new full-scale run:

1. Is the full learned IDTC characteristic itself consistent with a training-only central-secant generator proxy?
2. Is the principal RTDS projection discarding useful learned differential algebra?
3. Can a task-agnostic, train-only four-role gain calibration recover the physical generator amplitude without equation-specific pruning?

No official PDEBench test trajectory is used for training, calibration, selection, or gating.

## Data split within the official training split

Official first 10% test block remains untouched.

From the official 90% training block:
- fit: first 1000 trajectories;
- gain calibration: next 128 trajectories;
- validation: next 256 trajectories.

Spatial reduction:
- 4

Training temporal resolution:
- native raw time (reduction 1)

## Trained candidates

Only the two predeclared architecture-native candidates from PB1-Q2:

- `T1_S124_NATIVE` with strides (1,2,4)
- `T1_S111_NATIVE_LOCAL` with strides (1,1,1)

For each PDE:
- seed 202
- 20 epochs
- batch 50
- Adam lr 1e-3
- weight decay 1e-4
- exactly 400 optimizer updates.

No 500-epoch training occurs.

## Train-only central-secant diagnostic

On disjoint calibration / validation trajectories, construct:

[
q_{sec}(t)=rac{u(t+Delta t)-u(t-Delta t)}{2Delta t}.
]

This is not an exact PDE RHS and is never used in the 20-epoch IDTC optimization.

It is used only after fitting to diagnose the learned continuous characteristic.

## Three characteristic forms

### Full IDTC

[
Q_{full}(J^3u)
]

from the 35-scalar learned tensor core.

### Unit-gain principal closure

Extract the principal R/T/D/S polynomial roles from the exact canonical expansion and use unit gains.

### Calibrated principal closure

On the disjoint calibration subset only, fit four ridge gains:

[
q_{sec}
approx
g_RR+g_TT+g_DD+g_SS.
]

All four roles are retained.

No role pruning and no equation label/known coefficient is used.

## Characteristic metrics

On the disjoint validation trajectories report:

- Rel-L2 to central secant;
- Pearson correlation;
- amplitude ratio;
- full-IDTC vs unit-principal defect;
- full-IDTC vs exact-canonical parity;
- calibrated-principal vs central-secant Rel-L2.

Exact canonical parity must be <=1e-6.

## Flow evaluation

Using only validation trajectories:

1. Full IDTC generator integrated with common RK4 at raw-time substeps over each official 5-dt physical step.
2. Unit-gain principal RTDS using the native compiled IPM runtime.
3. Calibrated principal RTDS using the same native compiled runtime.

Evaluate an 8-step official-time rollout.

This separates characteristic quality from principal compilation and from stable deployment.

## Hypothesis interpretation

### H-FULL

Supported if full-IDTC RK4 rollout materially improves over PB1-Q2's unit-principal compiled result.

### H-CALIBRATION

Supported if calibrated principal closure reduces validation central-secant error and 8-step rollout error by >=30% versus unit-gain principal on both PDEs.

### H-PROJECTION

Supported if full-IDTC is substantially better than unit-principal and the full/principal characteristic defect is >0.1.

### H-OBJECTIVE

Supported if even full-IDTC has poor central-secant agreement and poor common rollout, indicating that the remaining problem is identification/conditioning rather than compilation.

## Formal-run authorization

A new 500-epoch public standard-data run is authorized only if one candidate satisfies, on both PDEs:

- finite full and calibrated rollouts;
- exact canonical parity <=1e-6;
- calibrated principal validation central-secant Rel-L2 <=0.7 times unit-principal;
- calibrated principal 8-step rollout Rel-L2 <=0.7 times the PB1-Q2 unit-principal result;
- calibrated principal 8-step rollout Rel-L2 < 0.50 absolute;
- no official test data used.

If both candidates pass, choose the one with the lower geometric mean calibrated rollout error across the two PDEs.

Otherwise formal training remains blocked.
