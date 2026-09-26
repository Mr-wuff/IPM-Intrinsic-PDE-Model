# IPM-PDEBench-PB1-Q8-FIX3-FIX2 — Weak Temporal/Test-Function Contract Attribution

## Motivation

PB1-Q8-FIX3-FIX1 established:
- FULL1024 and conservative AVG4 observations preserve global mass;
- official STRIDE4 decimation breaks conservation by ~910x;
- however, correcting the observation operator changes WCFC weak residual and rollout only marginally.

A reporting-only oracle audit reveals the deeper mismatch:
- exact Burgers weak-joint residual at FULL1024: ~0.282
- exact-law weak integral residual: ~0.106
- exact-law weak differential residual: ~0.385

The fitted WCFC can achieve a lower joint residual (~0.211) than the exact PDE law itself.

Therefore the current weak identification contract is biased relative to the continuum generator.

Q8-FIX3-FIX2 isolates:
1. central-secant differential constraints;
2. temporal quadrature span;
3. Fourier test-function bandwidth.

No architecture transition is authorized in this attribution run.

## Data

PDEBench Burgers epsilon=0.001.

Official first 1,000 trajectories remain sealed.

Reuse the same mechanism-development fit folds:
- fold A: 4352:5376
- fold B: 5376:6400
- fold C: 6400:7424
- validation: 7424:7936

Use the previously unused tail:
- final internal confirm: 8448:9000

Indices are relative to the 9,000-row official training block after the sealed test block.

## Observation representations

Primary:
- FULL1024

Secondary:
- AVG4-256 conservative block average

STRIDE4 is retained only as a reporting control.

## WCFC-5 algebra

Frozen:
`F(u)=f1*u+f2*u^2+f3*u^3+f4*u^4`

plus one diffusion coefficient `kappa`.

No known Burgers coefficient enters fitting or candidate selection.

## Candidate test-function bandwidths

Fourier modes:
- K4: modes 1..4
- K8: modes 1..8
- K16: modes 1..16
- K32: modes 1..32

## Candidate temporal contracts

### T0 — DIFF+SIMPSON2 baseline
Current Q8-FIX3 contract:
- central weak differential equation over t-dt to t+dt;
- two-step Simpson weak integral equation;
- equal dimensionless weight.

### T1 — SIMPSON2-INTEGRAL-ONLY
Remove the central differential equation.
Use only:
`<phi,u_{t+dt}-u_{t-dt}> = dt/3 [B_- + 4 B_0 + B_+]`.

### T2 — TRAPEZOID1-INTEGRAL-ONLY
One saved interval:
`<phi,u_{t+dt}-u_t> = dt/2 [B_t+B_{t+dt}]`.

### T3 — SIMPSON4-INTEGRAL-ONLY
Composite Simpson across four saved intervals:
`<phi,u_{t+2dt}-u_{t-2dt}> = dt/3 [B_-2 + 4B_-1 + 2B_0 + 4B_+1 + B_+2]`.

## Candidate selection

For each observation representation and each of the 16 contract/bandwidth combinations:
- fit all three independent folds;
- measure validation weak residual;
- measure standardized coefficient cosine.

A candidate is eligible only if:
- all metrics finite;
- median coefficient cosine >= 0.995.

Within each observation representation, select the eligible candidate with the lowest three-fold mean **validation integral weak residual**.

Known Burgers coefficients and runtime results are not used for selection.

The selected candidate is frozen before the 8448:9000 final internal confirm block is evaluated.

## Attribution hypotheses

### T1 — differential equation is the dominant bias
Supported if the selected integral-only candidate has final-confirm integral residual <= 0.75 times the DIFF+SIMPSON2 K32 baseline.

### T2 — low-mode weak testing is beneficial
Supported if the selected K is <=16 and its validation integral residual is <=0.85 times the same temporal contract at K32.

### T3 — exact-law consistency improves
Reporting-only diagnostic:
selected candidate exact-law final-confirm integral residual <=0.08.

This diagnostic is not used for selection.

### T4 — learned law runtime repair
Compile the selected WCFC law to:
- T(u)=-F'(u)
- D=2*kappa
- R=S=0
and run frozen FV2-MC-CFL.

On the final internal confirm block:
- three-fold mean 31-step Rel-L2 <=0.05
- max fold <=0.06.

### T5 — causal improvement over baseline WCFC
Selected candidate runtime mean / DIFF+SIMPSON2-K32 runtime mean <=0.60 on the same final-confirm block.

### T6 — coefficient stability
Selected candidate median standardized coefficient cosine >=0.995.

### T7 — runtime integrity
All selected-candidate trajectories finite;
max Courant <=0.250001;
predicted periodic mean drift <=1e-4.

## Routing

If T1/T4/T5/T6/T7 pass:
`INTEGRAL_WEAK_CONTRACT_SUPPORTED`.

If T2 also passes:
`LOW_MODE_INTEGRAL_WEAK_CONTRACT_SUPPORTED`.

If runtime remains >0.05 despite improved integral residual:
`WEAK_TO_RUNTIME_MAPPING_UNRESOLVED`.

Otherwise:
`WEAK_TEMPORAL_CONTRACT_UNRESOLVED`.

No official test access and no 500-epoch training are authorized.
