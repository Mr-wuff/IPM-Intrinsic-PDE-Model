# IPM-PDEBench-PB1-Q8-FIX3-FIX1 Results — Conservative Observation Operator Attribution

## Integrity

Result ZIP SHA256:

`dd5077214911dce01e527e928674b1126be525d37d78be6796d51e92742b881b`

Detached checksum matches exactly.

Internal result manifest: **19/19 payload entries match** by byte size and SHA256.

Protocol SHA256:

`9e2624b4a5cbd8597779f451b5a427dc6ec43d4cbf938343da16513c72369656`

Executed notebook SHA256:

`d706a1625aa2e8f7b0ea8f0a7de41c73f39c66e5e140a0c5e3548b3b6f89f65d`

The executed notebook contains 8 code cells, no runtime error output, and the frozen protocol hash.

Official test accessed: **false**.

## Frozen attribution result

- A1 FULL1024 conservation: **PASS**
- A2 AVG4 conservation: **PASS**
- A3 stride reduction breaks conservation evidence: **PASS**
- A4 conservative observation improves weak identification: **FAIL**
- A5 conservative observation improves runtime law quality: **FAIL**
- A6 coefficient stability: **PASS**
- A7 conservative runtime integrity: **PASS**

Frozen route:

**WEAK_CONTRACT_UNRESOLVED**

No architecture transition and no official-test unlock are authorized.

## Observation-operator result

Maximum normalized spatial-mean drift:

- FULL1024: **1.4432e-5**
- AVG4-256: **1.4432e-5**
- STRIDE4-256: **1.31377e-2**

Stride / conservative-average drift ratio:

**910.3x**

Thus the Q8-FIX3 conservation-detector failure on `::4` observations was indeed dominated by the non-conservative stride restriction.

The original N=1024 finite-volume trajectory and conservative AVG4 restriction preserve global mean to approximately 1e-5.

## But observation repair does not repair WCFC

Three-fold confirm weak-joint mean:

- FULL1024: **0.210969**
- AVG4-256: **0.212015**
- STRIDE4-256: **0.217767**

Ratios:
- FULL / STRIDE: **0.96878**
- AVG / STRIDE: **0.97359**

The frozen A4 threshold required <=0.70.

Thus removing the observation-conservation defect changes the weak residual by only about 2.6%-3.1%.

## Runtime result

On the official STRIDE4-256 internal target:

- WCFC fit on STRIDE4: **0.124432**
- WCFC fit on AVG4: **0.122595**
- WCFC fit on FULL1024: **0.123722**
- exact reporting-only law: **0.008892**

The best conservative-observation fit improves the stride-fit WCFC runtime by only about **1.48%**.

On the AVG4 target:

- AVG4-fit WCFC: **0.122253**
- exact law: **0.006235**

Therefore observation repair is real but not the cause of the remaining learned/oracle gap.

## Coefficient stability

Median standardized coefficient cosine:

- FULL1024: **0.999950**
- AVG4: **0.999949**
- STRIDE4: **0.999955**

The weak fit remains highly reproducible across disjoint trajectory folds.

## Coefficient pattern

FULL1024 three-fold mean approximately:
- f1 = 6.9e-5
- f2 = 0.50848
- f3 = -1.47e-4
- f4 = -0.02630
- kappa = 0.00031457

Reporting-only Burgers values:
- f1 = 0
- f2 = 0.5
- f3 = 0
- f4 = 0
- kappa = epsilon/pi ≈ 0.00031831

The main quadratic flux and diffusion are close, but a systematic quartic compensation term remains even at FULL1024.

## Critical oracle weak-equation audit

Using the reporting-only exact Burgers coefficients on the same confirm rows:

Weak-joint residual:
- FULL1024: **0.282386**
- AVG4: **0.283380**
- STRIDE4: **0.287573**

For FULL1024 specifically:
- exact-law weak integral residual: **0.105938**
- exact-law weak differential residual: **0.385047**

The fitted WCFC can obtain a lower joint residual (~0.211) than the exact PDE law itself.

This is decisive evidence that the remaining problem is not simply flux-basis capacity.

The current weak observation contract — especially central-secant differential constraints at saved temporal spacing and/or high Fourier modes near shocks — is biased relative to the continuum generator.

The fit introduces the stable quartic flux term to compensate for that contract mismatch.

## Scientific conclusion

Q8-FIX3-FIX1 establishes two separate facts:

1. spatial stride reduction is non-conservative and must be treated as a physical observation operator, not innocuous preprocessing;
2. correcting that operator does **not** solve the WCFC learned/oracle gap.

The next attribution must therefore target the weak temporal/test-function contract.

Priority hypothesis:
- the central-secant weak differential equation is the dominant biased component;
- integral weak balance is substantially closer to the exact law;
- high Fourier modes may amplify shock/discrete-time mismatch.

No change to the conservative FV2-MC-CFL runtime is supported.
