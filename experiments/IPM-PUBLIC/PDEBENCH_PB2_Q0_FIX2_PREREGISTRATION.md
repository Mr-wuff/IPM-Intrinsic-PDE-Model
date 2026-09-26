# IPM-PDEBench-PB2-Q0-FIX2 — Reaction-Diffusion Discrete-Generator / Observability Attribution

## Motivation

PB2-Q0-FIX1 showed:
- current sparse DCC35/P13 governing-law residuals remain ~0.43-0.50;
- adding more temporal centers improves conditioning but worsens residuals;
- DCC35 redundancy is not the dominant explanation;
- the nominal continuum oracle executed by the current coarse-grid P13 runtime is worse than the learned effective closure;
- per-center relative oracle residuals become numerically meaningless after the physical evolution signal collapses toward zero.

The pinned PDEBench generator is a periodic finite-volume reaction-diffusion solver with:
- nx=1024, L=1;
- rho=1, nu=0.5;
- exact logistic reaction substep;
- second-order finite-volume diffusion flux;
- dt_save=0.01.

FIX2 separates:
1. temporal-observation bias;
2. LocalTaylor derivative/precision error;
3. discrete-generator mismatch;
4. low-signal equilibrium contamination;
5. effective coarse-grid closure.

No official test access and no architecture transition are allowed.

## Data

Same PDEBench file:
`ReacDiff_Nu0.5_Rho1.0.hdf5`

Official rows 0:1000 remain sealed.

Train-only audit rows:
- signal/jet audit: relative rows 3584:3648
- fit folds:
  - 0:512
  - 512:1024
  - 1024:1536
- validation: 3072:3328
- confirm: 3584:3840

## Frozen continuum law for reporting-only diagnostics

`Q_cont = u - u^2 + 0.5*u_xx`.

In Taylor coordinates:
`Q_cont = u-u^2+a2`.

This law is never used to select a data-driven candidate.

## Spatial-generator representations

### J0 — LT32
Current LocalTaylorJet R4/D5/order3 evaluated in float32.

### J1 — LT64
Same exact stencil/order, but all jet calculations performed in float64.

### J2 — FD2-GENERATOR
Generator-matched second-order periodic finite-difference Laplacian:
`u_xx ≈ (u_{i+1}-2u_i+u_{i-1})/dx^2`.

The reporting-only exact discrete generator is:
`Q_fd = u-u^2 + 0.5*lap_fd(u)`.

### J3 — SPECTRAL
Periodic spectral second derivative on FULL1024:
`Q_spec = u-u^2 + 0.5*u_xx,spectral`.

J2/J3 are diagnostics only.

## Residual metrics

Do not average per-center relative residuals as the primary oracle metric.

For any center set, report:

### Global signal-weighted differential residual
`sqrt(sum ||Q-y_t||^2 / sum ||y_t||^2)`.

### Global signal-weighted Simpson integral residual
`sqrt(sum ||I_Q-(u_+-u_-)||^2 / sum ||u_+-u_-||^2)`.

Also report absolute residual RMS and target/change RMS per center.

This avoids the near-equilibrium denominator degeneracy discovered in FIX1.

## Data-only temporal observability score

For every center c=1..99 on train-only rows, compute:

- signal:
  `s_c = RMS(u_{c+1}-u_{c-1})`
- temporal curvature:
  `k_c = RMS(u_{c+1}-2u_c+u_{c-1})`

Define:
`score_c = s_c^2 / (k_c + 0.01*max_c s_c + 1e-12)`.

This score uses trajectories only, not the known PDE.

Freeze two data-only center sets:
- OBS8: top 8 scoring centers
- OBS12: top 12 scoring centers

No manual center editing after scores are computed.

## Data-driven identification matrix

Fit both DCC35 and P13 under:

Center sets:
- CURRENT_SPARSE
- OBS8
- OBS12

Objectives:
- DIC: centered differential + Simpson-2 integral, equal normalized weight
- INT_ONLY: Simpson-2 integral only

Jet used for fitting:
- LT64, to remove arithmetic precision as a confound while keeping the same local Taylor state definition.

Normalized ridge alpha=1e-8.

No known equation coefficient enters fitting or selection.

## Candidate selection

Within P13 only, candidate selection is based on validation data:

Eligibility:
- standardized coefficient cosine median >=0.995
- all coefficients finite

Choose the eligible P13 candidate with minimum validation **integral residual**.

DCC35 remains an attribution control and is not selected for deployment in this run.

The selected P13 candidate is evaluated on confirm rows and internal runtime only.

No official test is opened.

## Frozen attribution hypotheses

### G1 — discrete-generator compatibility
Supported if FD2-GENERATOR global signal-weighted Simpson residual on centers 2..8 <=0.05.

### G2 — LocalTaylor representation penalty
Supported if LT64 continuum-oracle residual / FD2-generator residual >=1.5 on the same centers.

### G3 — arithmetic-precision contribution
Supported if LT64 oracle residual <=0.80 times LT32 oracle residual.

### G4 — data-only observability repair
Supported if selected P13 confirm integral residual <=0.15 and <=0.50 times CURRENT_SPARSE+DIC P13 confirm integral residual.

### G5 — governing-law plausibility
Reporting-only after selection:
- reaction-u coefficient sign positive;
- reaction-u2 coefficient sign negative;
- diffusion coefficient sign positive;
- selected physical-coefficient L2 relative error <=0.30.

This diagnostic is not used for candidate selection.

### G6 — runtime closure
Selected P13 internal full-horizon Rel-L2 <=0.06 and finite.

### G7 — continuum-oracle / discrete-observation gap
Supported if the generator-matched FULL1024 discrete oracle is substantially more consistent with saved-time data than the continuum LT oracle, while the coarse-stride continuum runtime remains worse than learned effective closure.

## Routing

Priority:

1. If G1 and G2:
   `JET_DISCRETIZATION_MISMATCH`

2. Else if G3 and not G2:
   `JET_PRECISION_LIMITED`

3. Else if G4 and G6:
   `TEMPORAL_OBSERVABILITY_REPAIR_SUPPORTED`

4. Else if G1 but not G4:
   `IDENTIFICATION_OBJECTIVE_UNRESOLVED`

5. Else:
   `REACTION_DIFFUSION_CONTRACT_UNRESOLVED`

Multiple supporting hypotheses may be true; primary route follows the priority above.

No official test access, architecture freeze, or 500-epoch training is authorized.
