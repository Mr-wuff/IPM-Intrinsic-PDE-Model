# IPM-PDEBench-PB3-Q0 Results — Protocol-Deviated Diagnostic Run

## Formal status

**FORMAL INVALID / DIAGNOSTIC ONLY**

The run produced strong 2D PDE recovery results, but it modified the frozen generator-validity failure behavior during execution.

Frozen source behavior:

`if len(VALID) < min_centers: raise RuntimeError(...)`

Executed behavior:

- print a warning;
- replace the empty frozen-valid pool with the three centers having the smallest curvature ratio;
- continue the entire discovery and official-unlock pipeline.

The frozen protocol required:
- signal >= 15% of the global temporal signal peak;
- curvature/signal <= 0.40;
- at least 3 valid centers.

The actual data produced **zero** centers satisfying both conditions.

Therefore G1 should have failed under the frozen protocol, and all downstream support discovery / official-test access would have been blocked.

The downstream numerical results must be treated as diagnostic evidence only and cannot be used as formal PB3-Q0 evidence.

## Integrity

Result ZIP SHA256:

`e5394493e24828e8a5fd47158f214fce6e6c13cdf4cd3e7181eaea1b33c9a508`

Detached checksum matches exactly.

Internal result manifest: **22/22 tracked payload entries match**.

Frozen source notebook SHA256:

`37eb8245e80208881f0378750505961b4507b04f81f73cb177dfaa4ddd8942c9`

Executed notebook SHA256:

`0d819fc92d34e4d36dc0f5da75ec9bfb8b46115557dd036d961cf639f0262f6f`

No runtime errors were found.

## Why the frozen gate failed

The temporal signal profile is dominated by the random-initial-condition transient:

- center 1 signal ≈ 0.9945, curvature ratio ≈ 0.9895;
- center 2 signal ≈ 0.0501, curvature ratio ≈ 0.4488;
- center 3 signal ≈ 0.0251, curvature ratio ≈ 0.2910;
- later dynamically smooth centers have signal ≈ 0.0023–0.0040.

The global-peak rule:

`signal >= 0.15 * max(signal)`

therefore requires signal >= ~0.149, while every center satisfying the curvature gate is far below that value.

Counts:
- curvature-ratio <= 0.40: 97 centers;
- global 15%-peak signal gate: 1 center;
- intersection: **0 centers**.

Thus the failure is caused by a gate-normalization semantics issue: a single large initial transient defines the global signal peak and invalidates all later smooth generator observations.

## Diagnostic-only downstream results

The executed run substituted centers:

`[92,97,78]`

chosen by smallest curvature ratio.

With those centers, the rest of the pipeline produced unusually strong results.

### Recovered support

u-equation:

`[1, u, v, u^3, lap_u]`

v-equation:

`[u, v, lap_v]`

These exactly match the reporting-only PDEBench source support.

Fold-specific support is identical in all three folds for both equations.

Support Jaccard:
- u: 1.0
- v: 1.0

Support precision / recall:
- u: 1.0 / 1.0
- v: 1.0 / 1.0

### Internal confirm residual

u:
- ~0.016819 in all folds

v:
- ~0.044266 in all folds

### Reporting-only physical coefficients

Across three folds:

u-equation:
- large-reaction relative error ≈ 0.38–0.42%
- constant ≈ -0.00497 versus true -0.005
- Du ≈ 0.001012–0.001013 versus true 0.001

v-equation:
- reaction-pair relative error ≈ 2.87–3.14%
- Dv ≈ 0.004900–0.004910 versus true 0.005

### Native compiler

Internal combined increment Rel-L2:

`~0.02198`

Official combined increment Rel-L2:

`~0.02194`

Official channel means:
- u ≈ 0.01529
- v ≈ 0.03304

Official/internal degradation is essentially 1.

These values are **diagnostic only** because official access occurred after a protocol-deviated G1 repair.

## Scientific interpretation

The diagnostic results strongly suggest that the 2D coupled C2D-20 algebra and native reaction-diffusion compiler are viable.

The apparent PB3-Q0 failure is specifically the temporal generator-validity normalization:

**global peak normalization is not robust to a one-step random-initial-condition relaxation transient.**

The next experiment must preregister a robust, target-free temporal excitation gate before rerunning any support selection.

No result from this run should be reported as a formal PB3 PASS.
