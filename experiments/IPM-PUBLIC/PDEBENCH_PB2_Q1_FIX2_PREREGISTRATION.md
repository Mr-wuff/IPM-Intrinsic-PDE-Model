# IPM-PDEBench-PB2-Q1-FIX2 — Discrete-Generator / Finite-Time Semigroup Attribution

## Motivation

PB2-Q1-FIX1 falsified four simple explanations for the Nu=1 held-out failure:

- exact FIX6-style D-optimal budgeting does not repair the failure;
- using all valid centers helps but does not close the contract;
- reducing the temporal span from S2 (0.02) to TR1 (0.01) is insufficient;
- the residual is broad-band rather than dominated by high spatial frequencies.

At the same time, for Rho5 and Rho10 the reaction pair transfers accurately while the fitted diffusion coefficient is systematically attenuated to roughly 31–34% of the continuum Taylor-coordinate expectation.

The frozen support remains:

`[R_u, R_u2, D0]`

FIX2 therefore audits whether the remaining mismatch comes from representing a stiff finite-time diffusion flow with a saved-time quadrature of an instantaneous continuum generator.

No support search or official-test access is permitted.

## Data

Same held-out public PDEBench files:

- Nu1/Rho2 — datafile 133183 — MD5 `112c01a76447162bd67c8c1073f58ca2`
- Nu1/Rho5 — datafile 133184 — MD5 `fa224c9d143de37ac6914d391e70f425`
- Nu1/Rho10 — datafile 133182 — MD5 `a94e65631881a27ddae3ef74caf53093`

Rows 0:1000 remain sealed.

Internal blocks:
- calibration: 1536:1600 after the first 1000
- screen: 2048:2112
- confirm: 3584:3648

The smaller screen/confirm sample count is intentional because this experiment evaluates finite-time replay operators rather than fitting a large regression model.

## Source semantics audit

Pinned PDEBench source commit:

`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

The published ReactionDiffusion generator uses:
- exact logistic reaction update;
- second-order periodic diffusion flux;
- diffusion CFL `0.5*dx^2/nu * CFL`;
- saved-time interval `dt_save=0.01`.

Pinned multi YAMLs for Nu=1 declare:
- CFL=0.25;
- xL=0, xR=1;
- nx=512.

The public HDF5 files observed in Q1/FIX1 contain 1024 spatial cells.

FIX2 records this repository/public-data configuration discrepancy but does not assume it explains the trajectory.

The HDF5 coordinate arrays are authoritative for all numerical operators in this run.

## Frozen support / field representation

Physical support is not re-selected:

`S*=[R_u,R_u2,D0]`

LocalTaylor:
- radius 4
- degree 5
- order 3
- float64.

True reporting-only continuum coefficients for Nu=1:
- R_u=rho
- R_u2=-rho
- D0=2.

Known coefficients are used only for oracle attribution, not for model selection.

## Stage A — true-law saved-time oracle residuals

On the internal screen block and the complete data-only valid-center pool, evaluate the true physical law under three spatial generator representations:

### A0 LocalTaylor
`Q_LT = rho*u - rho*u^2 + 2*nu*a2`

### A1 FD2
`Q_FD2 = rho*u - rho*u^2 + nu*D2_FD(u)`

where D2_FD is the periodic second-order central finite-difference Laplacian on the actual HDF5 grid.

### A2 spectral continuum
`Q_SPEC = rho*u-rho*u^2+nu*D2_spectral(u)`

For each spatial generator report:
- S2 integral residual;
- TR1 integral residual.

This is reporting-only oracle attribution.

## Stage B — one-save-step finite-time replay

Predict:

`u(t+dt_save)`

directly from observed `u(t)`.

### B0 instantaneous Euler controls
- LocalTaylor Euler with the true law;
- FD2 Euler with the true law.

### B1 continuum spectral Strang flow
For microstep count m in:
`[1,2,4,8,16,32]`

each microstep performs:
1. exact logistic reaction for h/2;
2. exact continuum spectral diffusion semigroup for h;
3. exact logistic reaction for h/2.

### B2 discrete-FD2 Strang flow
Same reaction splitting, but diffusion uses the exact semigroup of the periodic second-order FD2 operator:

`lambda_k = -4*sin^2(pi*k/N)/dx^2`

and multiplier:

`exp(nu*lambda_k*h)`.

All operators use the actual public HDF5 N and dx.

Metrics:
- state relative L2:
  `||u_pred-u_next|| / ||u_next||`
- increment relative L2:
  `||u_pred-u_next|| / ||u_next-u_current||`

Evaluate screen and confirm blocks.

No replay method is promoted in this attribution experiment.

## Stage C — effective diffusion scan

Reporting-only diagnostic.

Fix the reaction coefficients to their public HDF5 rho attributes.

For the discrete-FD2 Strang flow with m=16, scan:

`nu_eff in [0.20,0.25,0.30,0.35,0.40,0.50,0.67,0.80,1.00,1.20,1.50]`

Choose the screen-block nu_eff minimizing one-step increment relative L2 and report confirm error with that frozen diagnostic value.

This scan does not alter the IPM support or produce a deployment model.

## Stage D — source-config discrepancy audit

Record:
- public HDF5 N, dx, L, dt;
- HDF5 Nu/rho attributes;
- pinned generator config N/CFL for the same parameter family.

This is a provenance diagnostic only.

## Frozen hypotheses

### B1 — spatial derivative mismatch
Supported if true-law FD2 S2 residual is <=0.75 times true-law LocalTaylor S2 residual in at least 2/3 environments.

### B2 — finite-time semigroup closure
Supported if discrete-FD2 Strang at m=16 or m=32 achieves, in at least 2/3 environments:

- screen state relative L2 <=0.02;
- screen increment relative L2 <=0.20;
- confirm increment relative L2 <=0.25.

### B3 — discrete versus continuum semigroup effect
Supported if, in at least 2/3 environments at the same m=16:

`E_increment(FD2-Strang) <= 0.80 * E_increment(continuum-Strang)`.

### B4 — semigroup convergence
Supported if, in all environments:

`E_increment(m=32) <= 1.05 * E_increment(m=16)`

for FD2-Strang.

This tests whether m=16 is already near the replay plateau.

### B5 — public effective-diffusion mismatch
Reporting-only, supported if in at least 2/3 environments the best screen nu_eff lies outside [0.8,1.2] and improves increment error by >=30% relative to nu_eff=1.

## Primary routing

Priority:

1. If any MD5 mismatch:
   `DATA_FILE_INTEGRITY_FAILURE`

2. If B2 and not B5:
   `FINITE_TIME_SEMIGROUP_CONTRACT_CONFIRMED`

3. If B2 and B5:
   `SEMIGROUP_CLOSES_WITH_EFFECTIVE_DIFFUSION_MISMATCH`

4. If B5 and not B2:
   `PUBLIC_DATA_EFFECTIVE_DIFFUSION_MISMATCH`

5. If B1:
   `DISCRETE_SPATIAL_GENERATOR_MISMATCH`

6. Otherwise:
   `PUBLIC_GENERATOR_SEMANTICS_UNRESOLVED`

B3/B4 are secondary causal diagnostics and do not override the primary route.

## Next-step rule

- FINITE_TIME_SEMIGROUP_CONTRACT_CONFIRMED:
  preregister compiler-in-loop identification of the frozen three coefficients through the finite-time semigroup, then repeat held-out qualification.

- SEMIGROUP_CLOSES_WITH_EFFECTIVE_DIFFUSION_MISMATCH or PUBLIC_DATA_EFFECTIVE_DIFFUSION_MISMATCH:
  stop model modification and audit public-data provenance / generator configuration before reattempting Q1.

- DISCRETE_SPATIAL_GENERATOR_MISMATCH:
  qualify a discrete-grid observation adapter while preserving the physical support.

- PUBLIC_GENERATOR_SEMANTICS_UNRESOLVED:
  perform a source-matched discrete-flow replay audit before any architecture change.

No official-test access, support search, architecture transition, or 500-epoch training is authorized.
