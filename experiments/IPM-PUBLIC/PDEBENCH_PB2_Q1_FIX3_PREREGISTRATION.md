# IPM-PDEBench-PB2-Q1-FIX3 — Semigroup Compiler-in-Loop Coefficient Identification

## Motivation

PB2-Q1-FIX2 established:

- the frozen physical support remains `[R_u,R_u2,D0]`;
- true instantaneous saved-time S2/TR1 quadrature fails under Nu=1 stiff diffusion;
- the true physical finite-time Reaction-Diffusion flow reproduces one saved HDF5 interval with increment Rel-L2 ~0.011–0.023;
- continuum spectral and discrete-FD2 semigroups are numerically indistinguishable;
- one Strang step is already on the replay plateau;
- the reporting-only effective-Nu scan is uniquely minimized at Nu=1 for all three held-out environments.

Therefore the identification objective, not the physical law, must change.

FIX3 fits the three frozen physical coefficients **through the native finite-time compiler itself**.

No support search is permitted.

## Held-out environments

Same diffusion-axis environments:

- H1: Nu=1, Rho=2 — MD5 `112c01a76447162bd67c8c1073f58ca2`
- H2: Nu=1, Rho=5 — MD5 `fa224c9d143de37ac6914d391e70f425`
- H3: Nu=1, Rho=10 — MD5 `a94e65631881a27ddae3ef74caf53093`

The first 1,000 trajectories in each file remain sealed until all internal gates pass.

## Data splits

Relative to the 9,000-row training portion after the first 1,000 rows:

- fit fold A: 0:512
- fit fold B: 512:1024
- fit fold C: 1024:1536
- generator-validity calibration: 1536:1600
- screen: 2048:2304
- validation: 3072:3328
- confirm: 3584:3840

Compiler optimization uses exactly 64 deterministic evenly-spaced trajectories from each 512-row fit fold.

All screen/validation/confirm evaluations use the full blocks.

## Frozen support

Exactly:

`S*=[R_u,R_u2,D0]`

No other P13 term may be introduced.

The physical PDE represented by a coefficient vector `c=(a,b,D0)` is:

`u_t = a*u + b*u^2 + (D0/2)*u_xx`

because the canonical Taylor coordinate is `a2=u_xx/2`.

## Generator-valid temporal centers

Same data-only gate as FIX6/Q1:

For centers c=2..98:
- signal >=15% of the environment peak;
- curvature/signal <=0.40.

All valid centers are used for compiler-in-loop fitting and evaluation.

No D-optimal down-selection is used in FIX3.

## Frozen native finite-time compiler

One saved interval is compiled as a single Strang step:

1. exact quadratic-reaction flow for dt/2;
2. exact continuum spectral diffusion semigroup for dt;
3. exact quadratic-reaction flow for dt/2.

### Reaction flow

For:
`du/dt = a*u + b*u^2`

use the analytic flow:

`u(h)=u0*exp(a*h) / [1-(b/a)*u0*expm1(a*h)]`

with the continuous a->0 limit:
`u(h)=u0/(1-b*u0*h)`.

### Diffusion flow

Diffusion coefficient:
`kappa=D0/2`

Fourier multiplier:
`exp(-kappa*k^2*dt)`.

FIX2 established that one Strang step is already equivalent to m=16/32 at the reported precision.

## Parameterization

Optimization variables are unconstrained theta mapped to:

- `a = 20*tanh(theta_a)`
- `b = 20*tanh(theta_b)`
- `D0 = 5*sigmoid(theta_D)`

These broad bounds are fixed before execution.

They are not environment-specific and do not use the true coefficients.

## Data-only initialization

For each environment/fold:

1. fit the same frozen three coefficients with normalized-ridge S2 integral equations;
2. use that S2 coefficient vector as the primary nonlinear initialization;
3. create deterministic restart scales `[0.75,1.0,1.25]` applied to the full S2 initialization;
4. transform each restart into theta-space.

No true coefficient is used for initialization.

## Compiler-in-loop objective

For every selected fit trajectory and every generator-valid center:

- input: `u_c`
- target: `u_{c+1}`
- prediction: compiled one-step Strang flow.

Optimize normalized increment MSE:

`L = sum ||u_pred-u_next||^2 / sum ||u_next-u_c||^2`.

For each restart:
- Adam: 120 full-batch steps, lr=0.05;
- then LBFGS: max_iter=40, history_size=10, tolerance_grad=1e-10, tolerance_change=1e-12.

Choose the restart with the lowest final fit loss.

This is optimizer-restart selection only; support and compiler remain fixed.

## Controls

For every environment/fold retain the initial S2 coefficient vector.

Evaluate that S2 vector through the **same finite-time compiler** on screen/confirm.

This isolates improvement caused by compiler-in-loop coefficient identification.

## Reporting-only physical coefficients

Only after optimization and internal metrics are frozen.

Expected:
- `a=rho`
- `b=-rho`
- `D0=2` for Nu=1.

The known values do not enter fitting, restart selection, or official-test unlock.

## Internal gates

### C1 — optimization integrity
All 9 fits:
- finite coefficients;
- finite fit loss;
- final fit increment Rel-L2 <=0.10.

### C2 — screen finite-time closure
Across all environment/fold fits:
- mean increment Rel-L2 <=0.06;
- max environment mean <=0.08;
- max single fold <=0.10.

### C3 — confirm finite-time closure
- overall mean increment Rel-L2 <=0.06;
- max environment mean <=0.08;
- max single fold <=0.10.

### C4 — coefficient stability
For every environment:
- median pairwise coefficient cosine across three folds >=0.995.

### C5 — reporting-only physical fidelity
Every fold:
- a>0;
- b<0;
- D0>0.

Across all fits:
- overall physical coefficient relative L2 mean <=0.15;
- max environment mean <=0.20;
- every environment mean D0/2 lies in [0.80,1.20].

### C6 — causal improvement over saved-time S2 identification
On confirm, using the same finite-time compiler:

For every environment:
`E_compiler-fit / E_S2-init <=0.35`.

Only if C1-C6 all pass may the official first-1,000 trajectories be opened.

## Official-block confirmation

No refitting.

Use the nine frozen compiler-fit coefficient vectors on official rows 0:1000.

### O1 — finite
All official predictions and metrics finite.

### O2 — external finite-time closure
- overall official increment Rel-L2 <=0.08;
- max environment mean <=0.10;
- max single fold <=0.12.

### O3 — no degradation cliff
For each environment:

`official_mean / internal_confirm_mean <=1.50`.

## Decision

PB2-Q1-FIX3 PASS iff:
- C1-C6 all pass;
- official block is then opened exactly once;
- O1-O3 all pass.

If PASS:
- PB2 Reaction-Diffusion identification is independently confirmed across the held-out diffusion axis;
- freeze the strong smooth Reaction-Diffusion compiler:
  `Generator-Validity -> frozen physical support -> semigroup compiler-in-loop coefficient identification -> native finite-time flow`;
- stop Reaction-Diffusion mechanism tuning;
- authorize transition to PB3 new-PDE / 2D qualification.

If C1-C4 pass but C5 fails:
`SEMIGROUP_EFFECTIVE_COEFFICIENTS_ONLY`

If C2/C3 fail:
`SEMIGROUP_IDENTIFICATION_CLOSURE_FAIL`

If C6 fails:
`COMPILER_IN_LOOP_NO_CAUSAL_GAIN`

No 500-epoch training is authorized.
