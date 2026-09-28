# IPM-PDEBench-PB3-Q0 — 2D Coupled Reaction-Diffusion PDE-Native Qualification

## Purpose

PB2 is frozen after independent held-out diffusion-axis confirmation.

PB3-Q0 tests the next architectural boundary:

- 1D -> 2D;
- scalar field -> coupled two-field PDE;
- single spatial derivative axis -> isotropic/anisotropic 2D role decomposition;
- fixed PDE algebra -> explicit multi-field canonical program.

Public benchmark:

`2D_diff-react_NA_NA.h5`

PDEBench datafile:
`https://darus.uni-stuttgart.de/api/access/datafile/133017`

MD5:
`b8d0b86064193195ddc30c33be5dc949`

Pinned PDEBench commit:

`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

No long neural training is performed.

## PDEBench source semantics

Pinned generator:

`pdebench/data_gen/src/sim_diff_react.py`

Public configuration:
- Du = 1e-3
- Dv = 5e-3
- k = 5e-3
- t in [0,5]
- 101 saved frames
- 128 x 128 cell-centered grid
- domain [-1,1] x [-1,1]
- 1000 random initial-condition samples
- zero-flux / finite-volume boundary semantics
- adaptive solve_ivp time integration.

Continuum equations:

`u_t = u - u^3 - k - v + Du * Lap(u)`

`v_t = u - v + Dv * Lap(v)`

The known equation is used only for oracle/reporting gates, never to select centers or discovered support.

## Official benchmark split

PDEBench FNODatasetMult uses the final 10% of sorted HDF5 seed groups as test.

Therefore:
- internal train/development groups: sorted indices 0:900
- sealed official groups: sorted indices 900:1000.

The official groups must not be read before all internal discovery gates pass.

## Internal splits

Within the first 900 groups:

- fit fold A: 0:100
- fit fold B: 100:200
- fit fold C: 200:300
- center calibration: 300:340
- validation: 500:600
- confirm: 700:800
- runtime diagnostic: first 32 confirm samples.

## Stage A — data-only generator-valid temporal observation

Candidate centers c=1..99.

Across both fields and all calibration samples/spatial cells:

`signal_c = RMS(X[c+1]-X[c-1])`

`curvature_c = RMS(X[c+1]-2X[c]+X[c-1])`

Valid iff:
- signal >= 15% of peak signal;
- curvature / signal <= 0.40.

Require at least 3 valid centers.

Temporal information budget:
- B=8.

If pool size <=8, use all.
If >8, use target-free greedy D-optimal selection computed from the full C2D-20 S2 design matrix on the calibration block.

No target y or true PDE coefficient is used in center selection.

## C2D-20 canonical library

Each output equation uses the same 20 candidate terms.

### Reaction polynomial, total degree <=3 in (u,v)
1. 1
2. u
3. v
4. u^2
5. u*v
6. v^2
7. u^3
8. u^2*v
9. u*v^2
10. v^3

### First-order transport diagnostics
11. u_x
12. u_y
13. v_x
14. v_y

### Isotropic diffusion roles
15. Lap(u)
16. Lap(v)

### Anisotropic second-order diagnostics
17. u_xx - u_yy
18. u_xy
19. v_xx - v_yy
20. v_xy

Spatial derivatives use the actual HDF5 cell spacing.

- Laplacians use the source-compatible zero-flux finite-volume boundary stencil.
- transport and anisotropy diagnostics use centered interior differences with zero normal diagnostic derivative at the boundary.

Expected support is not used for discovery.

Reporting-only expected support:

For u_t:
- 1
- u
- v
- u^3
- Lap(u)

For v_t:
- u
- v
- Lap(v)

## Stage B — observation-contract oracle

After the data-only center set is frozen, evaluate the **known public PDE** on internal validation/confirm.

### B0 saved-time S2 oracle

For each channel:

`X[c+1]-X[c-1] ≈ dt/3 * [Q(c-1)+4Q(c)+Q(c+1)]`

using source-compatible finite-volume Laplacians.

### B1 native finite-time oracle

One saved interval is compiled with a Strang-style native physical flow:

1. coupled local reaction RK4 over dt/2 using two fixed RK4 microsteps;
2. exact 2D Neumann diffusion semigroup for each field;
3. coupled local reaction RK4 over dt/2 using two fixed RK4 microsteps.

The diffusion semigroup uses the eigendecomposition of the exact source-compatible 1D zero-flux finite-volume Laplacian along each axis.

Report one-step state Rel-L2 and increment Rel-L2.

## Observation-contract gate

### G0
- MD5 exact;
- 1000 seed groups;
- official last 100 groups remain sealed.

### G1
Generator-valid pool contains >=3 centers.

### G2
Native true-law compiler on internal confirm:
- combined-field increment Rel-L2 mean <=0.05;
- each channel mean <=0.07.

### G3
S2 true-law oracle:
- combined-field integral Rel-L2 mean <=0.20;
- each channel mean <=0.25.

Only if G0-G3 pass may Stage C support discovery run.

If G2 passes but G3 fails, route immediately to:

`2D_FINITE_TIME_COMPILER_REQUIRED`

and do not perform/support-claim linear saved-time PDE discovery.

## Stage C — deterministic support discovery

Only if G0-G3 pass.

For each fit fold and each output equation:
- accumulate normalized S2 sufficient statistics for C2D-20;
- normalized ridge alpha=1e-8.

Enumerate every support of size 1..5:

`sum_{k=1}^5 C(20,k)=21699`

per output equation.

For each support:
- fit each of the three folds independently;
- score mean validation S2 residual.

Define near-optimal:
`E_val <= 1.05 * E_best`.

Global selected support:
1. smallest support size among near-optimal candidates;
2. lower validation residual;
3. lexicographically smaller support if still tied.

Fold-specific selected supports use the same rule.

No true support is used in selection.

## Stage D — internal physical qualification

### G4 — confirm closure
For both equations:
- mean confirm integral Rel-L2 <=0.12;
- max fold <=0.15.

### G5 — support stability
For each equation:
- median pairwise fold support Jaccard >=0.80.

### G6 — reporting-only physical support
For each equation:
- support recall =1.0;
- support precision >=0.80.

### G7 — reporting-only coefficient fidelity

u-equation:
- coefficients of u, v, u^3 have correct signs;
- large-reaction coefficient relative error mean <=0.15;
- constant term negative and absolute error <=0.01;
- Lap(u) coefficient positive and within [0.5,1.5] * Du.

v-equation:
- u positive, v negative;
- reaction pair relative error <=0.15;
- Lap(v) positive and within [0.5,1.5] * Dv.

### G8 — learned-program native compiler

Only if selected supports contain only reaction terms plus the correct own-field isotropic Laplacian.

Compile each fold's learned coefficients with the same native 2D Strang flow.

On the first 32 confirm samples:
- combined increment Rel-L2 mean <=0.12;
- each channel mean <=0.15;
- all outputs finite.

Only if G4-G8 pass may the official last 100 seed groups be opened.

## Official confirmation

No support selection or refitting after unlock.

Use the six frozen programs:
- 3 folds x 2 output equations.

Evaluate:
- saved-time S2 residual;
- native compiler one-step increment Rel-L2.

### O1
All finite.

### O2
Official compiler:
- combined increment Rel-L2 mean <=0.15;
- each channel mean <=0.18.

### O3
No degradation cliff:
- official compiler mean / internal confirm compiler mean <=1.50.

### O4
Official S2 residual:
- each equation mean <=1.50 times its internal confirm mean.

## Decision

PB3-Q0 PASS iff G0-G8 and O1-O4 all pass.

If G2 passes but G3 fails:
`2D_FINITE_TIME_COMPILER_REQUIRED`

If G3 passes but G4-G7 fail:
`2D_CANONICAL_SUPPORT_UNRESOLVED`

If G4-G7 pass but G8 fails:
`2D_NATIVE_COMPILER_UNRESOLVED`

If all pass:
`PB3_2D_COUPLED_PDE_NATIVE_QUALIFIED`

A PASS authorizes PB3-Q1 robustness / resolution / noise qualification.

No 500-epoch neural training is authorized in PB3-Q0.
