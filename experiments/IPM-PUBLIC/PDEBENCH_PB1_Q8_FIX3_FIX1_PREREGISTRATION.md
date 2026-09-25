# IPM-PDEBench-PB1-Q8-FIX3-FIX1 — Conservative Observation Operator Attribution

## Motivation

PB1-Q8-FIX3 attempted weak conservative flux identification on the official N=256 reduced observations, but the preregistered conservation detector failed.

The executed notebook then bypassed the required stop condition, so the downstream WCFC results are diagnostic only.

A source audit identifies a likely protocol-level observation mismatch:

- the pinned PDEBench Burgers generator is a periodic finite-volume method on N=1024 cell centers;
- its update is an interface-flux difference, so the full discrete solution is globally conservative;
- the official PDEBench model loader reduces spatial resolution by stride sampling;
- Q8-FIX3 likewise used `tensor[..., ::4]`;
- stride decimation is not a conservative coarse-grid restriction for moving shocks.

Q8-FIX3-FIX1 isolates whether this non-conservative observation operator caused the failed W0 detector and the spurious weak-law terms.

This is an attribution experiment only. No architecture transition is authorized.

## Dataset and sealed test

PDEBench Burgers epsilon=0.001.

Official first 1,000 trajectories remain sealed.

Reuse the Q8-FIX3 train-only mechanism rows:
- fit fold A: 4352:5376
- fit fold B: 5376:6400
- fit fold C: 6400:7424
- validation: 7424:7936
- confirm: 7936:8448

Indices are relative to the 9,000-trajectory training block after the sealed official test block.

These rows are reused specifically because this run diagnoses the Q8-FIX3 observation contract rather than providing independent confirmation.

## Frozen observation operators

### O1 — FULL1024

Use all original finite-volume cells.

### O2 — STRIDE4-256

Use the official benchmark reduction:

`u_coarse[j] = u_fine[4*j]`.

### O3 — AVG4-256

Use conservative block restriction:

`u_coarse[j] = mean(u_fine[4*j : 4*j+4])`.

The coarse coordinate is the mean of the four fine cell-center coordinates.

AVG4 preserves the full-grid discrete spatial mean exactly.

## Frozen weak law

Use the same WCFC-5 representation for every observation operator:

`u_t + dF(u)/dx = kappa*u_xx`

with

`F(u)=f1*u+f2*u^2+f3*u^3+f4*u^4`.

Unknowns:
`[f1,f2,f3,f4,kappa]`.

Use exactly the Q8-FIX3 identification contract:
- Fourier modes 1..32, sine + cosine;
- differential weak equation;
- Simpson-integral weak equation;
- each equation family normalized by its own target RMS;
- equal dimensionless weighting;
- ridge alpha 1e-8.

No pointwise spatial derivative of observed data is used.

Known Burgers coefficients remain reporting-only.

## Runtime

For each fitted law:
- compile `T(u)=-F'(u)`;
- compile `D=2*kappa`;
- set `R=S=0`;
- gains fixed to one;
- execute with frozen FV2-MC-Rusanov adaptive-CFL backend at CFL=0.25.

Runtime comparisons are made on:
1. STRIDE4-256 confirm trajectories;
2. AVG4-256 confirm trajectories.

The exact reporting-only law is evaluated as a diagnostic oracle on both targets.

FULL1024 runtime is not a formal requirement; the purpose of FULL1024 is to diagnose conservation and weak identification without observation reduction.

## Frozen attribution hypotheses

### A1 — full-grid conservation

FULL1024 maximum normalized spatial-mean drift across all fit folds and validation <= `1e-4`.

### A2 — conservative restriction conservation

AVG4-256 maximum normalized spatial-mean drift <= `1e-4`.

### A3 — stride reduction breaks conservation evidence

STRIDE4-256 maximum normalized mean drift >= `1e-3`
and

`drift_stride / drift_avg >= 10`.

### A4 — conservative observation improves weak identification

At least one of FULL1024 or AVG4-256 satisfies:

`weak_joint_mean / weak_joint_STRIDE4 <= 0.70`.

### A5 — conservative observation improves runtime law quality

On the STRIDE4-256 runtime target, the best of FULL1024-fit or AVG4-fit WCFC laws satisfies:

- three-fold mean Rel-L2 <= `0.06`;
- best mean / STRIDE4-fit WCFC mean <= `0.60`.

### A6 — coefficient stability

For FULL1024 and AVG4-256 separately, median pairwise cosine of standardized 5-scalar vectors >= `0.995`.

### A7 — conservative runtime integrity

For every runtime program evaluated:
- finite through 31 steps;
- maximum observed Courant <= `0.250001`;
- WCFC predicted-domain mean drift <= `1e-4`.

## Routing

If A1-A3 pass and A4/A5 show that AVG4 fixes the weak law:

`CONSERVATIVE_RESTRICTION_REQUIRED`.

If A1-A3 pass and FULL1024 fixes the weak law but AVG4 does not:

`FULL_RES_WEAK_IDENTIFICATION_REQUIRED`.

If A1/A2 fail:

`DATA_CONSERVATION_ASSUMPTION_INVALID`.

Otherwise:

`WEAK_CONTRACT_UNRESOLVED`.

No official test access, no architecture freeze, and no 500-epoch training are authorized in this run.
