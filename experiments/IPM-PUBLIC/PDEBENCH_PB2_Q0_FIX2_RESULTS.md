# IPM-PDEBench-PB2-Q0-FIX2 Results — Reaction-Diffusion Discrete-Generator / Observability Attribution

## Integrity

Result ZIP SHA256:

`2b020fcbd00f7aa4063af4b521f9e793a133c7fcb2da0bb09e47ec626538305d`

Detached checksum matches exactly.

Internal result manifest: **50/50 payload entries match** by byte size and SHA256.

Protocol SHA256:

`b47909481940266da5577b6912af34e40b9f07ce670f34c895416090b6f114ce`

Executed notebook SHA256:

`020ac7f1d4c7353162dbeacda3a0102ea27346c4835d674a23a134b3a50e18e2`

Frozen source notebook SHA256 from the run record:

`9ba6da8df90ee62f8beb159d9b1c8a688016b31e3d91116167259c96122ac052`

The executed notebook contains 8 code cells and no runtime-error outputs. The embedded frozen protocol matches. The full notebook hash differs because execution outputs are embedded.

Official test accessed: **false**.

## Frozen attribution outcome

- G1 generator-matched FD2 closure: **FAIL**
- G2 LocalTaylor-vs-FD2 discretization penalty: **FAIL**
- G3 float64 precision repair: **FAIL**
- G4 data-only observability repair: **FAIL**
- G5 governing-law plausibility: **FAIL**
- G6 selected-candidate runtime closure: **PASS**
- G7 continuum/discrete observation gap hypothesis: **FAIL**

Primary route:

**REACTION_DIFFUSION_CONTRACT_UNRESOLVED**

No architecture transition, test unlock, or long training is authorized.

## Temporal observability

The data-only score selects:

OBS8:
`[1,2,3,4,5,6,7,8]`

OBS12:
`[1,2,3,4,5,6,7,8,9,10,11,12]`

Thus the score correctly identifies the early transient as the only high-signal region.

However, center 1 has very large temporal curvature relative to its signal, so high signal alone is not sufficient for local-generator identification.

The trajectory signal decays rapidly:
- center 1 signal ~0.273
- center 2 ~0.073
- center 8 ~0.0113
- center 12 ~0.00584
- center 27 ~2.58e-4
- center 28 onward is numerically zero for the audited rows, except tiny float-level artifacts.

This confirms an extremely short identifiability window.

## Spatial/discrete oracle attribution

On centers 2..8, signal-weighted Simpson integral residual:

- LT32: **0.06998**
- LT64: **0.06988**
- generator-matched FD2: **0.07186**
- spectral: **0.07580**

Therefore:
- LT64 / LT32 = **0.99867**
- LT64 / FD2 = **0.97242**

Float precision does not explain the failure.
The LocalTaylor derivative representation is not materially worse than the generator-matched second-order finite-difference Laplacian in the informative early window.

The frozen G1 threshold (FD2 <=0.05) is missed narrowly, but the decisive point is that FD2 does not outperform LocalTaylor.

## Data-driven identification matrix

CURRENT_SPARSE remains the validation-selected P13 candidate.

CURRENT_SPARSE + DIC + P13:
- validation integral mean: **0.49925**
- confirm integral mean: **0.49637**
- confirm characteristic mean: **0.50129**
- condition number median: **6.61e5**
- coefficient cosine median: **0.99752**

OBS8/OBS12 substantially reduce condition number, but worsen law closure and/or coefficient stability.

For example:

OBS8 + DIC + P13:
- confirm integral mean: **0.75826**
- cosine median: **0.96463**

OBS12 + integral-only + P13:
- confirm integral mean: **0.71748**
- cosine median: **0.99739**

Thus simply selecting the highest-signal early centers is not enough.

## Important interpretation of the failed observability score

OBS8 starts at center 1.

For center 1:
- signal RMS ≈ 0.2726
- temporal curvature RMS ≈ 0.2184
- curvature/signal ≈ 0.80

This interval has strong dynamics but is far from a locally linear-in-time generator observation.

The score used in FIX2 over-rewarded signal magnitude and did not reject high temporal curvature.

Centers 2..8 have a much more favorable reporting-only continuum-law integral closure (~0.07), but center 1 dominates the OBS8 finite-time mismatch.

Therefore the next temporal audit must distinguish:

**large signal** from **valid infinitesimal/finite-time generator observation**.

## Selected runtime

Selected CURRENT_SPARSE + DIC P13 programs:

- fold 0: 0.03696
- fold 1: 0.03690
- fold 2: 0.03666
- mean: **0.03684**

Previous PB2-Q0 effective closures:
- mean: **0.03936**

The new selected effective closure is slightly better at trajectory prediction despite still being physically wrong.

This reinforces the separation between:
- trajectory closure;
- governing-law identification.

## Reporting-only physical coefficients

Selected physical-law relative L2 error:
- fold 0: 6.14
- fold 1: 6.35
- fold 2: 4.10
- mean: **5.53**

Reaction signs remain wrong:
- R_u is negative;
- R_u2 is positive.

Diffusion D0 is positive, but accompanied by large state-dependent diffusion compensation.

Therefore G5 correctly fails.

## Scientific conclusion

FIX2 rules out three tempting explanations:

1. float32 arithmetic precision is not the dominant cause;
2. LocalTaylor-vs-FD2 spatial discretization mismatch is not the dominant cause;
3. generic early high-signal center selection is not sufficient.

The remaining evidence points to a **temporal generator-validity / structural excitation problem**.

Reaction-Diffusion has a very short transient:
- center 1 is strong but temporally highly curved;
- centers roughly 2..7 retain meaningful signal while being substantially less curved;
- later centers rapidly lose generator information as the field approaches equilibrium.

The next experiment should therefore use a data-only temporal-validity gate combining:
- minimum dynamical signal;
- maximum temporal-curvature ratio;
and compare Simpson-2 vs composite Simpson-4 integral identification without using the known PDE for selection.

No official test should be opened.
