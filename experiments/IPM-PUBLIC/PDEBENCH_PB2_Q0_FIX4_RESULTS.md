# IPM-PDEBench-PB2-Q0-FIX4 Results — Multi-Environment Reaction-Diffusion Identifiability Audit

## Integrity

Result ZIP SHA256:

`759db8038f47cdfe680a121fe5cff7c7e9aa602efd44b6039d52b139c9cf3272`

Detached checksum matches exactly.

Internal result manifest: **31/31 payload entries match** by byte size and SHA256.

Protocol SHA256:

`67c3732aaa0c2cb704232a4baa76bdf9acc5c570207355cff804f62456677c71`

Executed notebook SHA256:

`77f4cab415a1c7d7f66c7ff1a5c1ddadc90c6167c6b586aa06fd19b19c56c010`

The executed notebook contains 9 code cells and no runtime errors. The embedded protocol object exactly matches the packaged protocol. No post-registration threshold relaxation was found.

Official test accessed: **false**.

## Formal outcome

Frozen gates:
- M1 environment generator-validity viability: **PASS**
- M2 multi-environment residual closure: **FAIL**
- M3 support stability/sparsity: **PASS**
- M4 true-support recovery, reporting-only: **FAIL**
- M5 coefficient fidelity, reporting-only: **FAIL**
- M6 improvement over independent identification: **FAIL**

Primary route:

**MULTI_ENVIRONMENT_SUPPORT_INSUFFICIENT**

No architecture transition, official-test unlock, or long training is authorized.

## Generator-valid centers

Data-only gates:

- E0 Nu0.5/Rho1.0: `[2,3,4,5,6,7,8]`
- E1 Nu0.5/Rho2.0: `[2,3,4,5,6,7,8,9,10,11,12,13]`
- E2 Nu1.0/Rho1.0: `[2,3,4,5,6]`

All satisfy the frozen 3..12-center viability requirement.

## Independent S2-P13 baseline

### E0 Nu0.5/Rho1.0
Confirm integral:
- 0.064065
- 0.063909
- 0.064035

Mean: **~0.06400**

The diffusion constant is stable near 1.05–1.08, but reaction coefficients remain fold-unstable.

### E1 Nu0.5/Rho2.0
Confirm integral:
- 0.037977
- 0.037984
- 0.037987

Mean: **~0.03798**

This environment is substantially more identifiable than E0.

Recovered coefficients are already qualitatively close to the reporting-only physical structure:
- R_u ≈ 2.50–2.58
- R_u2 ≈ -2.91 to -3.15
- D0 ≈ 1.046–1.051

A cubic reaction compensation remains, but signs and role structure are much more stable.

Reporting-only active coefficient relative L2:
- 0.359
- 0.347
- 0.430

### E2 Nu1.0/Rho1.0
Confirm integral:
- 0.712572
- 0.715518
- 0.716160

Mean: **~0.71475**

This environment fails the frozen S2 observation contract before any multi-environment support inference.

Its independent physical coefficient errors are extremely large and unstable.

## Critical causal conclusion

The three-environment experiment mixed two distinct questions:

1. whether multiple valid environments improve structural identifiability;
2. whether every environment is itself compatible with the frozen saved-time S2 contract.

E0 and E1 are compatible with S2.
E2 is not.

Therefore the failure of the three-environment joint fit cannot be interpreted as a clean falsification of multi-environment identifiability.

## Group-sparse result

Validation selected:

`lambda/lambda_max = 0.01`

The support is identical across all three folds:

`[R0, R_u3, D0, D_u2]`

Support Jaccard median:

**1.0**

Thus the group-sparse optimizer itself is stable.

However the stable support is an effective closure, not the physical law.

Confirm integral means:
- E0: **0.06540**
- E1: **0.04545**
- E2: **0.73013**

Overall mean:

**0.28033**

The E2 environment dominates the failure.

Reporting-only common-support metrics:
- precision: **0.25**
- recall: **0.3333**
- F1: **0.2857**

Expected physical common support:
`[R_u, R_u2, D0]`

The selected support therefore fails physical-law recovery.

## Lambda path

The support path is orderly and stable:
- lambda=0: 13 terms
- 0.001: <=6 terms
- 0.003: <=5 terms
- 0.01: 4 terms, Jaccard=1.0
- 0.03: 3 terms, Jaccard=1.0
- 0.1: 2 terms
- 0.4: 1 term

The problem is not numerical instability of FISTA; it is that the joint objective is asked to share support with an environment whose temporal contract does not close.

## Scientific conclusion

FIX4 does **not** justify abandoning multi-environment excitation.

Instead it establishes an additional requirement:

**an environment must itself satisfy the frozen generator-observation contract before it is allowed to contribute to shared-support identification.**

The next experiment should isolate the reaction-strength intervention axis at fixed diffusion, because both Nu0.5/Rho1 and Nu0.5/Rho2 are already S2-compatible.

A rho-sweep environment qualification should be performed before another group-sparse shared-support fit.
