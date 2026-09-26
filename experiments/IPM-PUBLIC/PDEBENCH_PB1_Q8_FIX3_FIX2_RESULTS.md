# IPM-PDEBench-PB1-Q8-FIX3-FIX2 Results — Weak Temporal/Test-Function Contract Attribution

## Integrity

Result ZIP SHA256:

`a67828f4f6c612b0838beec8ab2f6f5daefb8ef1b8a01703590d32f6d2cc1ead`

Detached checksum matches exactly.

Internal result manifest: **10/10 payload entries match** by byte size and SHA256.

Protocol SHA256:

`6f1bac5bcfddb6bb153c6e8ea8e320d27d97bb35d2e8cb1de26bde85032adf97`

Executed notebook SHA256:

`a6d1c45343e130ee22d3a3f40040bc9f1be85033ce6a026511fa97cd5f838b31`

The executed notebook has 8 code cells, exactly matching the frozen code cells, with no runtime errors.

Official test accessed: **false**.

## Frozen attribution outcome

All preregistered gates pass:

- T1 differential-contract bias repair: **PASS**
- T2 low-mode weak testing: **PASS**
- T3 exact-law integral consistency: **PASS**
- T4 learned-law runtime repair: **PASS**
- T5 causal improvement over baseline WCFC: **PASS**
- T6 coefficient stability: **PASS**
- T7 runtime integrity: **PASS**

Primary route:

**LOW_MODE_INTEGRAL_WEAK_CONTRACT_SUPPORTED**

This attribution run does not itself authorize an architecture transition or official-test access.

## Selected contract

For FULL1024, validation-only selection chooses:

- Fourier modes: **K=4**
- temporal contract: **SIMPSON4_INT**
- differential weak constraint: **disabled**

The selected contract is a four-saved-interval composite Simpson weak balance.

## Weak-law closure

Final untouched internal confirm (training tail 8448:9000):

Selected FULL1024 K4/SIMPSON4 integral residual:
- fold 0: 0.000987
- fold 1: 0.000983
- fold 2: 0.000984
- mean: **0.00098473**

Frozen DIFF+SIMPSON2 K32 baseline:
- fold 0: 0.160811
- fold 1: 0.159789
- fold 2: 0.162935
- mean: **0.161178**

Selected / baseline ratio:

**0.0061096**

Thus the selected weak temporal/test-function contract reduces final-confirm integral residual by approximately **99.39%**.

## Validation structure

FULL1024 validation integral means:

- K4 SIMPSON4_INT: **0.000930**
- K4 SIMPSON2_INT: **0.000934**
- K8 SIMPSON4_INT: **0.001687**
- K8 SIMPSON2_INT: **0.001714**
- K4 TRAP1_INT: **0.002982**
- K4 DIFF_SIMPSON2: **0.004393**
- K32 SIMPSON2_INT: **0.086869**
- K32 SIMPSON4_INT: **0.096802**
- K32 DIFF_SIMPSON2: **0.152491**
- K32 TRAP1_INT: **0.186606**

Two effects are therefore independently visible:

1. removing the central differential weak constraint materially improves the fit;
2. restricting the weak test bandwidth to low Fourier modes is essential in the low-viscosity shock regime.

## Exact-law consistency

Reporting-only exact Burgers law under the selected contract:

FULL1024 K4/SIMPSON4 final-confirm integral residual:

**0.00145219**

This passes the frozen exact-law diagnostic threshold by a wide margin and contrasts with the prior K32 differential/joint contract where the exact PDE itself had a large residual.

The selected identification objective is therefore consistent with the known continuum law at the saved-data temporal resolution.

## Runtime closure

Selected FULL1024 laws compiled to the frozen FV2-MC-Rusanov adaptive-CFL executor:

- fold 0: **0.010247**
- fold 1: **0.010282**
- fold 2: **0.010244**
- mean: **0.0102574**
- max: **0.0102819**

Baseline DIFF+SIMPSON2-K32 laws on the same final-confirm block:

mean: **0.107274**

Selected / baseline runtime ratio:

**0.09562**

Thus the repaired weak identification contract reduces final rollout error by approximately **90.44%** without changing the runtime.

All selected runs:
- remain finite;
- max Courant = 0.25;
- normalized mean drift is approximately 6.4e-5 to 6.7e-5.

## Coefficient stability and physical audit

Median standardized coefficient cosine:

**0.9999999977**

Selected FULL1024 three-fold coefficients:

- f1: approximately -1e-5 to -3e-6
- f2: **0.499959 to 0.499992**
- f3: approximately 3e-6 to 1.2e-5
- f4: approximately 2.5e-5 to 4.1e-5
- kappa: approximately 0.000352 to 0.000354

Reporting-only Burgers values:
- f1 = 0
- f2 = 0.5
- f3 = 0
- f4 = 0
- kappa = epsilon/pi ≈ 0.00031831

The quadratic flux coefficient is recovered to about 5e-5 relative error. The previous systematic quartic compensation term (~-0.026) collapses to O(1e-5), confirming that it was caused by the biased weak temporal/high-frequency contract rather than a real physical term.

The diffusion coefficient retains an approximately 10.9% positive bias, which should be tracked in independent confirmation.

## Scientific conclusion

The low-viscosity weak-branch failure is resolved at the mechanism level.

The correct trajectory-only shock-regime contract is supported as:

`FULL conservative observation -> low-mode weak moments -> integral-only finite-time balance -> WCFC-5 flux law -> conservative FV2-MC-CFL execution`

The decisive design principles are:
- do not identify a shock generator using saved-time central differential secants;
- do not over-weight high-frequency Fourier weak tests at finite temporal resolution;
- use low-mode finite-time weak balance directly.

The next experiment must be an independent confirmation on previously unused Burgers viscosities. No further epsilon=0.001 mechanism tuning is justified.
