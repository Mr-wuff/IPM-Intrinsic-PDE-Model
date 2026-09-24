# IPM-PDEBench-PB1-Q3-FIX1 — Gain-Aware Principal Closure Qualification

## Why FIX1 is required

PB1-Q3 learned non-unit train-only calibration gains and showed a large improvement in principal-characteristic agreement with the central-secant proxy.

However, the repository runtime used by Q3 stored `FrozenProgram.gains` but did not apply those gains in `IPMStep`.

This is directly visible in the Q3 result:
- calibrated and unit-principal characteristic errors differ substantially;
- calibrated gains are far from one;
- yet calibrated and unit-principal rollout errors are exactly identical for every task/candidate.

Therefore the Q3 rollout/calibration hypothesis test is invalid.

The runtime contract has been repaired in IPM v1.0.2:
- R gain scales reaction;
- T gain scales transport velocity polynomial;
- D gain scales the diffusion characteristic before the Taylor-coordinate /2 conversion;
- S gain scales the dispersion characteristic before the Taylor-coordinate /6 conversion.

No learned coefficient is changed.

## Scientific purpose

Re-run only the cheap native-time closure qualification with the corrected gain-aware runtime.

Questions:

1. Does train-only four-role calibration improve the actual compiled physical rollout?
2. Does principal closure remain sufficient after gain calibration?
3. Which of the two predeclared native-time contracts, if any, qualifies for the final 500-epoch standard-data run?

## Data

Official PDEBench Advection beta=1 and Burgers nu=0.01.

Inside the official 90% training block:
- fit: first 1000 trajectories;
- calibration: next 128 trajectories;
- validation: next 256 trajectories.

The official held-out test block is never accessed.

Spatial reduction:
- 4.

Training temporal resolution:
- native raw time.

## Candidates

- `T1_S124_NATIVE`: strides (1,2,4)
- `T1_S111_NATIVE_LOCAL`: strides (1,1,1)

For each PDE/candidate:
- seed 202;
- 20 epochs;
- batch 50;
- 400 optimizer updates;
- Adam lr 1e-3;
- weight decay 1e-4.

## Gain calibration

Fit four ridge gains on calibration trajectories only:

[
q_{sec}
approx
g_RR+g_TT+g_DD+g_SS.
]

All four roles remain present.
No equation-specific pruning or known PDE coefficient is supplied.

## Runtime semantic qualification

Before any scientific gate:

1. a non-unit-gain synthetic program must produce a different output than its unit-gain counterpart;
2. gain-aware execution must match a mathematically equivalent program where each role gain is folded into that role's polynomial coefficients:
   [
   E_{m gain-fold}le2	imes10^{-6}.
   ]

If this fails, the experiment stops.

## Metrics

For each task/candidate:

- 20-epoch training loss ratio;
- full IDTC vs central-secant Rel-L2/correlation/amplitude;
- unit principal vs central-secant;
- calibrated principal vs central-secant;
- unit principal compiled 8-step validation rollout;
- calibrated principal compiled 8-step validation rollout;
- gain-aware vs gain-folded runtime parity;
- corrected runtime gain sensitivity.

The full-IDTC explicit RK4 rollout is retained only as a diagnostic and is **not a formal gate**, because previous M-series experiments already established that unrestricted learned differential algebra can be stiff under generic explicit integration. The compiler/runtime is the deployment object.

## Formal candidate gate

A candidate passes only if, on both PDEs:

- training and compiled rollout are finite;
- calibrated principal central-secant Rel-L2 <= 0.70 × unit-principal central-secant Rel-L2;
- calibrated compiled 8-step rollout Rel-L2 <= 0.70 × unit-principal compiled rollout Rel-L2;
- calibrated compiled 8-step rollout Rel-L2 <= 0.50 absolute;
- corrected gain-aware runtime and gain-folded reference agree <=2e-6.

If both candidates pass, select the one with the lower geometric mean calibrated rollout Rel-L2 across Advection/Burgers.

If neither passes, no 500-epoch run is authorized.

## Historical-result audit policy

Because runtime v1.0.0-v1.0.1 ignored stored gains, previously reported repository-runtime public-benchmark numbers for frozen programs must be treated as provisional until a separate gain-aware audit is completed.

Q3-FIX1 does not use the official test split to repair those historical numbers. That audit occurs only after the training contract is frozen.
