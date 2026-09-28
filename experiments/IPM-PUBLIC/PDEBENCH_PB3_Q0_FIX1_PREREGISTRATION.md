# IPM-PDEBench-PB3-Q0-FIX1 — Robust Temporal-Gate 2D Coupled PDE-Native Qualification

## Motivation

PB3-Q0 is formally invalid because the frozen temporal generator-validity gate produced zero centers and the executed notebook replaced the hard failure with a post-registration fallback.

The failure mechanism is now known.

The first random-initial-condition transition has signal ~0.9945 and dominates the global peak, while nearly all later smooth dynamics have signal ~0.002–0.025. Therefore the frozen condition:

`signal >= 0.15 * global_peak_signal`

cannot coexist with the curvature gate.

The downstream diagnostic run nevertheless recovered the exact 2D physical support and near-exact coefficients, suggesting the C2D-20 / native-compiler architecture is viable.

FIX1 changes **only the temporal generator-validity normalization**. The PDE library, support search, data splits, physical oracle, compiler, gates, and official-test policy remain unchanged.

## Dataset

Same public PDEBench file:

`2D_diff-react_NA_NA.h5`

URL:
`https://darus.uni-stuttgart.de/api/access/datafile/133017`

MD5:
`b8d0b86064193195ddc30c33be5dc949`

Pinned PDEBench commit:
`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Official split:
- sorted seed groups 0:900 development
- sorted seed groups 900:1000 sealed official test.

## Frozen splits

- fit fold A: 0:100
- fit fold B: 100:200
- fit fold C: 200:300
- temporal calibration: 300:340
- validation: 500:600
- confirm: 700:800
- runtime diagnostic: first 32 confirm samples.

## FIX1 robust temporal generator-validity gate

Candidate centers:
`c=1..99`

For each center compute, across both channels and all calibration samples/spatial cells:

`signal_c = RMS(X[c+1]-X[c-1])`

`curvature_ratio_c = RMS(X[c+1]-2X[c]+X[c-1])/(signal_c+1e-12)`

### Stage A — local-linearity admissibility

A center is curvature-admissible iff:

`curvature_ratio_c <= 0.40`

Require at least 8 curvature-admissible centers.

### Stage B — robust excitation floor

Let:

`s_ref = median(signal_c | curvature-admissible)`

A center enters the robust valid pool iff:

- curvature-admissible;
- `signal_c >= s_ref`.

This retains the upper half of excitation levels **within the already smooth temporal regime**.

The median is frozen at preregistration. No target y, PDE coefficient, support, validation residual, or official data enter this gate.

Require at least 8 robust-valid centers.

There is **no fallback**. If fewer than 8 centers survive, FIX1 fails immediately.

### Stage C — target-free temporal budget

Budget:
`B=8`

If robust-valid pool size is exactly 8, use all.

If >8, use the same target-free greedy D-optimal full-C2D20 S2 design as PB3-Q0:
- calibration block only;
- pooled column normalization;
- delta=1e-6;
- no target y.

The selected eight centers are frozen before any true-law oracle or support discovery.

## Reporting-only gate diagnostic

Report, but never use for selection:
- original PB3-Q0 global-peak valid count;
- robust-valid count;
- ratio of first-center signal to robust median signal.

This quantifies the transient-outlier problem.

## Everything after center freezing is unchanged from PB3-Q0

### C2D-20 library

Reaction terms:
- 1
- u
- v
- u²
- uv
- v²
- u³
- u²v
- uv²
- v³

First derivatives:
- u_x
- u_y
- v_x
- v_y

Isotropic diffusion:
- Lap(u)
- Lap(v)

Anisotropy/mixed diagnostics:
- u_xx-u_yy
- u_xy
- v_xx-v_yy
- v_xy.

### Observation oracle

Known public PDE:
- saved-time S2 integral residual;
- native 2D reaction-diffusion finite-time compiler.

Frozen oracle gates:
- native compiler combined increment <=0.05;
- each channel <=0.07;
- S2 combined integral <=0.20;
- each channel <=0.25.

Only if the robust temporal gate and all oracle gates pass may support discovery run.

### Support search

For each equation enumerate all C2D-20 supports of size 1..5:

`21699`

Selection:
- validation mean;
- near-optimal <=1.05 * best;
- smallest support;
- lower validation residual;
- lexicographic tie-break.

No true support is used.

### Internal gates

Unchanged:
- confirm integral closure;
- fold support Jaccard >=0.80;
- reporting-only support recall 1.0 / precision >=0.80;
- reporting-only coefficient fidelity;
- learned native compiler increment closure.

### Official unlock

Only after all internal gates G0-G8 pass.

The final 100 seed groups are then read exactly once with:
- no support reselection;
- no coefficient refitting.

Official gates remain unchanged.

## Decision

If all internal and official gates pass:

`PB3_2D_COUPLED_PDE_NATIVE_QUALIFIED`

If robust temporal gate fails:
`2D_ROBUST_TEMPORAL_GATE_FAIL`

If native compiler passes but S2 oracle fails:
`2D_FINITE_TIME_COMPILER_REQUIRED`

If support discovery fails:
`2D_CANONICAL_SUPPORT_UNRESOLVED`

No 500-epoch neural training is authorized.

## Stop rule

If FIX1 passes formally, PB3-Q0 is frozen and the project moves directly to:
1. PB3-Q1 robustness / resolution / noise;
2. final cross-paradigm Pareto benchmark.

No further tuning of the 2D Reaction-Diffusion discovery mechanism is allowed unless PB3-Q1 exposes a specific failure.
