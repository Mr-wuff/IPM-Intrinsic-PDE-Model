# IPM-A1 — Official Equation-Discovery Benchmark

## Purpose

A0/A0-FIX1 closed the controlled predictive benchmark.

A1 tests a different claim: whether the trajectory-trained IPM law is competitive with **official sparse equation-discovery methods** at recovering governing PDE structure and coefficients.

The frozen IPM core is not modified.

## External baseline

Use **PySINDy 2.1.0** from the official dynamicslab/pysindy package/repository.

PySINDy 2.1.0 is pinned for reproducibility.

Official feature libraries:
1. `PDELibrary` + `STLSQ` — strong-form PDE-FIND-style sparse identification.
2. `WeakPDELibrary` + `STLSQ` — weak/integral sparse identification designed to reduce derivative sensitivity.

No custom reimplementation of SINDy is labeled as an official baseline.

## PDE suite

- Heat
- Advection
- Burgers
- Allen-Cahn
- KdV

True governing terms:

### Heat
[
u_t=
u u_{xx}
]

### Advection
[
u_t=-c u_x
]

### Burgers
[
u_t=-a u u_x+
u u_{xx}
]

### Allen-Cahn
[
u_t=D u_{xx}+r u-r u^3
]

### KdV
[
u_t=-a u u_x-eta u_{xxx}
]

## Candidate library

PySINDy uses:
- PolynomialLibrary degree 3 without duplicate bias;
- PDE spatial derivatives through order 3;
- derivative/function interactions enabled;
- STLSQ with threshold selected only from a frozen training-side grid.

The library intentionally contains irrelevant terms so support recovery is nontrivial.

## Data

Use the frozen A0 domain, IC generator, temporal sampling, PDE definitions and formal seeds, but equation-discovery cases use **fixed coefficients per PDE** at the center of the A0 training range.

This is necessary because classical PDE-FIND/SINDy identifies one governing equation at a time, whereas the A0 IPM checkpoint receives PDE parameters as inputs and was trained across coefficient ranges.

For each formal seed and PDE:
- generate six fixed-coefficient identification trajectories;
- generate four independent fixed-coefficient test trajectories;
- use the same underlying trajectories for PySINDy strong/weak baselines and IPM evaluation.

This information-contract difference is reported explicitly rather than hidden.

Observation conditions:
- clean dense;
- 0.5% noise;
- 1% noise;
- 2% noise;
- unseen 3% noise.

Optional spatial sparsity diagnostic:
- N=64
- N=32

## IPM comparator

Load frozen A0 checkpoints:
- IPMRaw
- IPMAdaptive

No IPM retraining is allowed.

IPM governing coefficients are estimated directly from its local-law Jacobian, without fitting another neural model:

- advection speed from (partial Q/partial u_x);
- heat diffusivity from (partial Q/partial u_{xx});
- Burgers/KdV transport coefficient from the relation (partial Q/partial u_x=-a u);
- diffusion/dispersion coefficients from (partial Q/partial u_{xx}) or (partial Q/partial u_{xxx});
- Allen-Cahn reaction coefficient from (partial Q/partial u=r(1-3u^2)).

This creates an interpretable coefficient-recovery test for IPM rather than a post-hoc symbolic neural network.

## Metrics

### Equation-discovery metrics
For PySINDy:
- explicit selected equation;
- support precision / recall / F1;
- false-positive term count;
- normalized coefficient error.

For IPM:
- physically relevant derivative-order support;
- coefficient recovery error from local Jacobian structure;
- Jacobian cosine / spurious-order sensitivity.

### Predictive law metrics
All methods:
- held-out clean exact-Q relative RMSE;
- noise-condition exact-Q relative RMSE.

### Robustness
- performance vs noise;
- five-seed reproducibility;
- per-PDE results.

### Efficiency
- equation-fit wall time;
- inference/evaluation time;
- peak CPU memory where available;
- IPM checkpoint parameter count retained from A0.

## Fairness policy

This benchmark does not pretend neural IPM and sparse regression have identical computational contracts.

Instead it explicitly reports their information and model assumptions:

- PySINDy assumes a hand-specified finite candidate term library and promotes sparsity.
- IPM does not receive the true candidate equation library; it learns a nonlinear local characteristic from trajectories.
- PySINDy returns an explicit symbolic equation.
- IPM returns a differentiable local law whose governing coefficients can be audited through its Jacobian.

No aggregate winner score is used.

## Integrity checks

D0 — PySINDy version == 2.1.0.  
D1 — official PySINDy classes are used.  
D2 — A0 input ZIP checksum matches supplied checksum.  
D3 — all 50 required IPM checkpoints exist.  
D4 — no IPM retraining occurs.  
D5 — all formal results are finite.  
D6 — all selected equations, coefficients, raw metrics, timing and seeds are exported.  
D7 — threshold selection uses training-side data only.

Decision:
- DISCOVERY_BENCHMARK_COMPLETE
- DISCOVERY_BENCHMARK_INCOMPLETE

There is no winner-dependent gate.

## Advancement

After A1:
1. official NeuralOperator FNO / PDEBench predictive benchmark;
2. PDEArena / RPB;
3. selected The Well tasks;
4. foundation PDE models where compatible.
