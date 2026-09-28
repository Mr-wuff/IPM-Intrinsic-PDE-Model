# IPM-PDEBench-PB2-Q1-FIX1 — Diffusion-Axis Temporal-Stiffness / Budget-Transfer Attribution

## Motivation

PB2-Q1 failed before official-test unlock:

- Nu1/Rho2 S2 screen mean ~0.736
- Nu1/Rho5 ~0.662
- Nu1/Rho10 ~0.490

No environment qualified.

The frozen physical support itself is not reopened:

`[R_u,R_u2,D0]`

Diagnostic coefficients show:
- reaction terms become physically plausible for Rho5/Rho10;
- D0 remains around 0.67–0.70 instead of the reporting-only continuum expectation 2;
- fold coefficient stability is extremely high.

This suggests a diffusion-axis observation-contract problem rather than support instability.

FIX1 causally separates:

1. a Q1 temporal-budget transfer change;
2. saved-time temporal stiffness;
3. residual localization in high spatial frequencies;
4. dataset metadata inconsistency.

No official rows 0:1000 may be read.

## Held-out environments

Same as Q1:
- Nu1/Rho2, datafile 133183, MD5 `112c01a76447162bd67c8c1073f58ca2`
- Nu1/Rho5, datafile 133184, MD5 `fa224c9d143de37ac6914d391e70f425`
- Nu1/Rho10, datafile 133182, MD5 `a94e65631881a27ddae3ef74caf53093`

Only rows >=1000 are used.

## Frozen support

Exactly:

`S*=[R_u,R_u2,D0]`

No support search, extra PDE term, or coefficient prior is permitted.

## Frozen jet

- LocalTaylor radius 4
- degree 5
- order 3
- float64
- actual HDF5 x-coordinate used for grid spacing.

## Stage A — metadata audit

For every HDF5:
- record tensor shape;
- x-coordinate min/max/dx/domain length;
- t-coordinate min/max/dt;
- HDF5 attributes, including Nu/rho when present;
- MD5.

Metadata mismatch is diagnostic only unless the file identity itself is wrong.

## Stage B — generator-valid pool

Same data-only rule as FIX6/Q1:

For centers c=2..98 on calibration rows 1536:1600 after the first 1000:

`signal_c = RMS(u_{c+1}-u_{c-1})`

`curvature_ratio_c = RMS(u_{c+1}-2u_c+u_{c-1})/(signal_c+1e-12)`

Valid iff:
- signal >=15% of environment peak;
- curvature ratio <=0.40.

Require >=3 centers.

## Stage C — temporal-budget attribution

Freeze three center sets per environment.

### C0 CURRENT_Q1
Exact Q1 rule:
- B=8
- target-free D-optimal design using the frozen three-term support matrix.

### C1 FIX6_STYLE
Exact FIX6 budgeting semantics:
- B=8
- target-free D-optimal design using the full P13 S2 design matrix;
- no target y.

### C2 ALL_VALID
Use every valid center from the generator-valid pool.

No center set is selected using residual or physical coefficients.

## Stage D — temporal-contract attribution

For each center set and each of three fit folds, fit the frozen three coefficients under two linear finite-time contracts.

### T0 S2
Current Q1:
`u_{c+1}-u_{c-1} = dt/3 [Q_{c-1}+4Q_c+Q_{c+1}]`

### T1 TR1
Single-save-step trapezoid:
`u_{c+1}-u_c = dt/2 [Q_c+Q_{c+1}]`

TR1 uses half the temporal span of S2.

Fit:
- normalized ridge alpha=1e-8
- no physical coefficient prior.

Evaluate every fit on the disjoint screen block and confirm block using the same center set and same temporal contract.

No model is promoted in this attribution run.

## Stage E — spectral-band residual localization

For every environment, fold, center-set, and temporal contract:

On the screen block compute residual field r(x) and target field y(x).

Using periodic rFFT, report cumulative low-mode relative residual:

`E_K = sqrt(sum_{|k|<=K}|r_k|^2 / sum_{|k|<=K}|y_k|^2)`

for:
- K=4
- 8
- 16
- 32
- 64
- FULL.

Also report the fraction of residual spectral energy above K=32.

This is diagnostic only and never used for fitting or selection.

## Reporting-only continuum coefficient audit

After all data-driven fits are frozen:

Expected:
- R_u = rho
- R_u2 = -rho
- D0 = 2 for Nu=1.

Report coefficient relative L2 and D0 attenuation ratio:
`D0/2`.

The known coefficients do not enter any fit or route threshold except the explicitly reporting-only coefficient diagnostics.

## Frozen hypotheses

### A1 — Q1 budget-transfer confound
Supported if FIX6_STYLE+S2:
- screen mean across environments <=0.15;
or
- improves screen mean by >=50% relative to CURRENT_Q1+S2 in every environment.

### A2 — all-valid budget insufficiency
Supported if ALL_VALID+S2:
- screen mean <=0.15 in at least 2 environments;
and
- <=0.60 times CURRENT_Q1+S2 in those environments.

### A3 — saved-time stiffness / temporal-span effect
Supported if, for the same center design in at least 2 environments:
- TR1 screen residual <=0.60 times S2;
and
- TR1 screen residual <=0.20.

### A4 — high-frequency localization
Supported if, in at least 2 environments under the best predeclared diagnostic pair among:
- FIX6_STYLE+S2
- ALL_VALID+S2
- FIX6_STYLE+TR1
- ALL_VALID+TR1

the residual satisfies either:
- E_16 <=0.40 * E_FULL,
or
- >70% of residual spectral energy lies above K=32.

This is a diagnostic hypothesis only; no best-pair promotion occurs.

### A5 — reaction-transfer / diffusion-attenuation pattern
Reporting-only, supported if for Rho5 and Rho10:
- reaction pair relative error <=0.15;
- D0/2 <=0.50.

## Primary routing

Priority:

1. If file MD5 mismatch:
   `DATA_FILE_INTEGRITY_FAILURE`

2. Else if A1:
   `DOPT_BUDGET_TRANSFER_MISMATCH`

3. Else if A3 and A4:
   `SAVED_TIME_DIFFUSION_STIFFNESS`

4. Else if A3:
   `TEMPORAL_SPAN_MISMATCH`

5. Else if A4:
   `HIGH_FREQUENCY_OBSERVATION_MISMATCH`

6. Else if A2:
   `TEMPORAL_BUDGET_INSUFFICIENT`

7. Else:
   `DIFFUSION_AXIS_CONTRACT_UNRESOLVED`

No official-test access, support change, architecture transition, or 500-epoch training is authorized.

## Next-step rule

- Budget mismatch route -> rerun Q1 with exact FIX6 budgeting and otherwise unchanged support/contract.
- Temporal stiffness route -> preregister a semigroup-/split-aware finite-time diffusion executor/identifier; do not alter support.
- High-frequency-only route -> qualify a band-limited / scale-aware observation contract before reattempting Q1.
- Unresolved route -> audit PDEBench discrete diffusion semantics and HDF5 metadata before any new model mechanism.
