# IPM-PDEBench-PB1-Q9 — Independent Weak-Conservative Branch Confirmation

## Purpose

PB1-Q8-FIX3-FIX2 resolved the low-viscosity weak-identification mechanism on Burgers epsilon=0.001.

The frozen mechanism is:
- FULL1024 observation for identification;
- Fourier weak modes K=4;
- four-saved-interval composite Simpson integral-only weak balance;
- WCFC-5 flux/diffusion law;
- exact compilation to P13 transport/diffusion;
- FV2-MC-Rusanov adaptive-CFL execution with CFL=0.25;
- gains fixed to one.

PB1-Q9 is an **independent physical-parameter confirmation**. No contract selection or architecture tuning is allowed.

Use two previously unused PDEBench viscosities:
- epsilon=0.002
- epsilon=0.004

The epsilon=0.001 mechanism-development parameter is not used.

## Frozen official assets

Pinned PDEBench commit:

`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

### epsilon=0.002
- `1D_Burgers_Sols_Nu0.002.hdf5`
- URL: `https://darus.uni-stuttgart.de/api/access/datafile/268193`
- MD5: `edf1cd13622d151dfde3e4e5af7a95b4`

### epsilon=0.004
- `1D_Burgers_Sols_Nu0.004.hdf5`
- URL: `https://darus.uni-stuttgart.de/api/access/datafile/268191`
- MD5: `435e1fecb8a64a0b4563bb8d09f81c33`

Official test block:
- first 1,000 trajectories per viscosity.

The official test blocks remain sealed until every internal gate passes for both viscosities.

## Frozen identification contract

WCFC-5:

`u_t + dF(u)/dx = kappa*u_xx`

`F(u)=f1*u+f2*u^2+f3*u^3+f4*u^4`

Unknown vector:
`theta=[f1,f2,f3,f4,kappa]`

Identification:
- FULL1024 finite-volume observations;
- Fourier sine/cosine modes 1..4 only;
- no central differential equation;
- composite Simpson integral balance across four saved intervals;
- normalized ridge alpha=1e-8;
- no SGD;
- no known PDE coefficient in fitting.

## Internal split per viscosity

After the sealed first 1,000 test trajectories:
- fit A: 0:1024
- fit B: 1024:2048
- fit C: 2048:3072
- validation: 3072:3584
- confirm: 3584:4096

All three folds are fit independently.

## Runtime

Each fitted WCFC law is compiled exactly:
- `T(u)=-F'(u)`
- `D=2*kappa`
- `R=0`
- `S=0`
- gains = 1

Runtime:
- official spatial target: STRIDE4-256, matching the PDEBench forward benchmark observation;
- MUSCL + MC limiter;
- Rusanov flux;
- SSP-RK3;
- adaptive CFL=0.25.

## Frozen internal gates, for each unseen viscosity

### I1 — weak integral closure
Confirm integral residual:
- three-fold mean <= 0.015
- max fold <= 0.020

### I2 — coefficient stability
Median pairwise standardized coefficient cosine >= 0.995.

### I3 — internal runtime closure
31-step STRIDE4-256 confirm Rel-L2:
- three-fold mean <= 0.030
- max fold <= 0.040.

### I4 — conservative runtime integrity
For all three programs:
- finite for all 31 steps;
- max Courant <= 0.250001;
- normalized predicted-domain mean drift <= 1e-4.

Only if I1-I4 pass for **both** viscosities may official test be opened.

## Sealed official test confirmation

After all six programs are frozen and both viscosities pass internal gates, access the first 1,000 trajectories exactly once.

Evaluate on official spatial reduction 4 and temporal reduction 5.

### E1 — finite test rollout
All three programs finite through all 31 future steps.

### E2 — full-horizon relative L2
Per viscosity:
- three-fold mean <= 0.050
- max fold <= 0.060.

### E3 — official PDEBench nRMSE
Per viscosity:
- three-fold mean <= 0.080
- max fold <= 0.100.

### E4 — test conservation integrity
For every fold:
- max normalized predicted-domain mean drift <= 1e-4.

## Reporting-only physics audit

Only after fitting and gate evaluation, report:
- f2 relative error to 0.5;
- kappa relative error to epsilon/pi;
- magnitudes of f1, f3, f4;
- compiled transport and diffusion coefficients.

These values are never used for fit, candidate selection, or qualification.

## Decision

PB1-Q9 PASS only if I1-I4 and E1-E4 all pass for both epsilon=0.002 and epsilon=0.004.

If PB1-Q9 passes:
- freeze the scalar periodic low-viscosity conservation branch:
  `FULL observation -> K4 Simpson4 integral WCFC-5 -> conservative compiler -> FV2-MC-CFL`;
- end Burgers mechanism development;
- proceed to PB2 new-PDE-family validation.

No 500-epoch training is authorized.
