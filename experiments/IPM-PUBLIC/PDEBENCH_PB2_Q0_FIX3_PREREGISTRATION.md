# IPM-PDEBench-PB2-Q0-FIX3 — Temporal Generator-Validity Gated Integral Qualification

## Motivation

PB2-Q0-FIX2 ruled out:
- float32 precision as the dominant error source;
- LocalTaylor-vs-generator-matched FD2 discretization as the dominant error source;
- naive high-signal early-center selection as a sufficient repair.

The FIX2 data show why the naive observability score failed:
- center 1 has the largest dynamical signal;
- but its temporal curvature/signal ratio is ~0.80;
- the continuum-law Simpson integral mismatch at center 1 is correspondingly very large.

In contrast, centers roughly 2..7 retain meaningful signal with much lower temporal curvature.

FIX3 tests a stricter concept:

**generator-valid observation = enough dynamical signal + sufficiently low finite-time curvature. The 15% signal floor deliberately excludes the long low-signal relaxation tail instead of allowing near-equilibrium samples to dominate the algebra.**

No known PDE coefficient is used to select time centers or model candidates.

## Dataset

PDEBench 1D Reaction-Diffusion:
- Nu=0.5
- Rho=1.0
- file: `ReacDiff_Nu0.5_Rho1.0.hdf5`
- URL: `https://darus.uni-stuttgart.de/api/access/datafile/133177`
- MD5: `69a429239778d529cd419ed5888ea835`

Official rows 0:1000 remain sealed.

Relative train-only splits:
- fit A: 0:512
- fit B: 512:1024
- fit C: 1024:1536
- center-calibration block: 1536:1600
- validation: 3072:3328
- confirm: 3584:3840
- runtime diagnostic: first 64 confirm trajectories

## Frozen spatial state

FULL1024 identification observation.

LocalTaylor:
- radius 4
- degree 5
- order 3
- float64 arithmetic

Canonical spaces:
- DCC35
- P13

No change to the spatial jet definition.

## Data-only generator-validity gate

For each saved-time center c from 2 through 98, on the center-calibration block only:

Signal:
`s_c = RMS(u_{c+1}-u_{c-1})`

Curvature:
`k_c = RMS(u_{c+1}-2u_c+u_{c-1})`

Curvature ratio:
`r_c = k_c/(s_c+1e-12)`

Let `s_max=max_c s_c`.

A center is generator-valid iff:

- `s_c >= 0.15*s_max`
- `r_c <= 0.40`

All qualifying centers form the frozen set `GENVALID`.

No top-k ranking and no oracle coefficient enters this gate.

Viability requirement:
- at least 3 and at most 12 GENVALID centers.

If this requirement fails, the run stops before fitting.

## Temporal integral contracts

No centered differential equation is used in the candidate fits.

### S2 — Simpson-2 integral

`u_{c+1}-u_{c-1} ≈ dt/3 * [Q_{c-1}+4Q_c+Q_{c+1}]`

### S4 — composite Simpson-4 integral

`u_{c+2}-u_{c-2} ≈ dt/3 * [Q_{c-2}+4Q_{c-1}+2Q_c+4Q_{c+1}+Q_{c+2}]`

The same GENVALID centers are used for both contracts.

## Identification

For each:
- space in {DCC35, P13}
- temporal contract in {S2, S4}
- fold in {A,B,C}

Fit normalized ridge:
- alpha=1e-8
- column normalization
- no SGD
- no known physical coefficient.

## Candidate selection

Only P13 candidates are eligible for deployment selection.

Eligibility:
- all finite;
- median standardized coefficient cosine >=0.995.

Select between S2 and S4 using the lowest three-fold mean validation integral residual.

No known Reaction-Diffusion coefficient and no runtime result is used for selection.

## Internal qualification gates

### V1 — data-only gate viability

GENVALID contains 3..12 centers.

### V2 — governing-law integral closure

Selected P13 confirm integral residual:
- mean <=0.15
- max fold <=0.20.

### V3 — causal improvement over PB2-Q0

Selected confirm integral mean / frozen CURRENT_SPARSE+DIC P13 confirm integral <=0.40.

Frozen denominator:

`0.4958194410829113`

### V4 — coefficient stability

Selected median standardized coefficient cosine >=0.995.

### V5 — physical-law plausibility

Reporting-only after selection.

For the known PDE:

`u_t=u-u^2+0.5*u_xx`

and Taylor `a2=u_xx/2`, expected P13:
- R_u=+1
- R_u2=-1
- D0=+1
- all other principal coefficients zero.

Pass if:
- R_u positive in all three folds;
- R_u2 negative in all three folds;
- D0 positive in all three folds;
- mean P13 coefficient-vector relative L2 error <=0.50.

These values are not used for center selection or S2/S4 candidate selection.

## Runtime diagnostic — not a qualification gate

The current `IPMStep` coarse-stride runtime is already known to execute the exact continuum law poorly on this benchmark (~0.217 Rel-L2), while an effective closure obtains ~0.039.

Therefore runtime accuracy must not be used to reject an otherwise physically correct law in FIX3.

Report both:
- FULL1024 native runtime;
- official STRIDE4-256 native runtime;
for the selected P13 programs.

Requirements:
- all trajectories must remain finite.

Runtime error is diagnostic only and will be repaired separately if law identification succeeds.

### V6 — finite runtime integrity

All selected-program FULL1024 and STRIDE4 rollouts remain finite.

### V7 — DCC35 attribution

Reporting:
- DCC35/P13 integral residual ratio;
- condition-number ratio;
- nonprincipal coefficient magnitude.

V7 is diagnostic, not a pass/fail gate.

## Routing

If V1-V6 all pass:

`TEMPORAL_VALIDITY_GATED_STRONG_INTEGRAL_SUPPORTED`

If V2/V3/V4/V6 pass but V5 fails:

`FINITE_TIME_EFFECTIVE_CLOSURE_ONLY`

If V1 passes but V2/V3 fail:

`STRONG_INTEGRAL_IDENTIFICATION_INSUFFICIENT`

Otherwise:

`REACTION_DIFFUSION_STRONG_BRANCH_UNRESOLVED`

No official test access, architecture freeze, or 500-epoch training is authorized.

If the first route is reached, the next experiment must independently confirm the frozen identification contract on previously unused Reaction-Diffusion Nu/Rho pairs before any official-test unlock.
