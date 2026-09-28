# IPM-PDEBench-PB2-Q1 — Held-Out Diffusion-Axis Independent Confirmation

## Purpose

PB2-Q0-FIX6 recovered the Reaction-Diffusion common physical support on the development rho-sweep at Nu=0.5:

`[R_u, R_u2, D0]`

This support is now frozen.

PB2-Q1 tests whether that support transfers to completely unused diffusion-axis environments without any support re-selection.

Held-out environments:
- Nu=1.0, Rho=2.0
- Nu=1.0, Rho=5.0
- Nu=1.0, Rho=10.0

None of these environments participated in PB2 support selection.

The first 1,000 trajectories of every held-out file remain sealed until all internal gates pass.

## Data

### H1
`ReacDiff_Nu1.0_Rho2.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133183`  
MD5: `112c01a76447162bd67c8c1073f58ca2`

### H2
`ReacDiff_Nu1.0_Rho5.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133184`  
MD5: `fa224c9d143de37ac6914d391e70f425`

### H3
`ReacDiff_Nu1.0_Rho10.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133182`  
MD5: `a94e65631881a27ddae3ef74caf53093`

Per environment, rows after the first 1,000:
- fit fold A: 0:512
- fit fold B: 512:1024
- fit fold C: 1024:1536
- generator-validity calibration: 1536:1600
- environment screen: 2048:2304
- validation: 3072:3328
- confirm: 3584:3840

Official block:
- rows 0:1000, sealed until internal unlock.

## Frozen representation and temporal contract

- FULL1024
- LocalTaylor R4 / degree5 / order3
- float64
- S2 Simpson integral-only
- normalized ridge alpha=1e-8

Frozen support:

`S* = [R_u, R_u2, D0]`

No other P13 term may be fitted.
No support search is permitted.

## Data-only generator-validity pool

For centers c=2..98:

`s_c = RMS(u_{c+1}-u_{c-1})`

`r_c = RMS(u_{c+1}-2u_c+u_{c-1})/(s_c+1e-12)`

Valid iff:
- signal >=15% of environment peak;
- curvature/signal <=0.40.

Require at least 3 valid centers.

## Fixed temporal information budget

Budget B=8.

If pool size <=8:
- use all valid centers.

If pool size >8:
- use the exact FIX6 target-free greedy D-optimal procedure on the calibration-block frozen-support S2 design matrix;
- pooled column normalization;
- delta=1e-6;
- ties by smaller center index.

No target y or true coefficient enters center selection.

## Environment contract qualification

Using the frozen support only:

For each fit fold:
- fit the three support coefficients on training rows;
- evaluate S2 integral residual on the disjoint screen block.

Environment qualifies iff:
- >=3 budgeted centers;
- screen mean <=0.12;
- screen max fold <=0.15;
- all coefficients finite.

Require at least **2 of 3** held-out environments to qualify.

Qualified-environment set is frozen before validation/confirm.

## Internal validation and confirm

No model or support selection occurs.

For every qualified environment/fold, report:
- validation S2 residual;
- confirm S2 residual;
- coefficient stability across folds.

## Reporting-only physical law

Only after internal calculations are frozen.

For Nu=1:
- expected D0 = 2

For each environment:
- R_u = rho
- R_u2 = -rho

No expected value is used in fitting or qualification.

## Frozen internal gates

### I1 — held-out environment viability
At least 2 of 3 environments qualify.

### I2 — confirm closure
Across qualified env/folds:
- overall mean <=0.10
- max qualified-environment mean <=0.12
- max single fold <=0.15.

### I3 — coefficient stability
For each qualified environment:
- median pairwise coefficient cosine >=0.995.

### I4 — sign correctness, reporting-only
Every qualified env/fold:
- R_u >0
- R_u2 <0
- D0 >0.

### I5 — coefficient fidelity, reporting-only
Across qualified environments:
- overall physical 3-coefficient relative L2 mean <=0.20
- max qualified-environment mean <=0.30.

Only if I1-I5 all pass may the first 1,000 official trajectories be opened.

## Sealed official-block confirmation

For each qualified environment:

Use the three frozen fold-specific coefficient programs fitted only on post-test training rows.

Evaluate S2 integral residual on official rows 0:1000 using the already frozen budgeted center set.

No refitting on official rows.

### E1 — finite
All official residuals finite.

### E2 — external integral closure
Across all qualified env/folds:
- overall mean <=0.12
- max environment mean <=0.15
- max single fold <=0.18.

### E3 — no degradation cliff
For each environment:

`official_mean / internal_confirm_mean <= 1.50`

## Decision

PB2-Q1 PASS only if I1-I5 and E1-E3 all pass.

If PASS:
- freeze the Reaction-Diffusion strong identification support:
  `Generator-Validity Gate -> D-optimal temporal budget -> S2 integral-only -> [R_u,R_u2,D0]`;
- mark PB2 Reaction-Diffusion new-family identification as independently confirmed across a held-out diffusion axis;
- authorize transition to the next PDE-family / 2D qualification stage;
- do not continue tuning Reaction-Diffusion support.

If internal gates fail:
- official block remains sealed;
- route by whether failure is environment-contract viability, coefficient stability, or coefficient fidelity.

No 500-epoch training is authorized.
