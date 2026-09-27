# IPM-PDEBench-PB2-Q0-FIX6 — Budget-Normalized Rho-Sweep Exhaustive Common-Support Audit

## Motivation

PB2-Q0-FIX5 established two facts:

1. Rho1 and Rho2 satisfy the frozen generator-valid S2 observation contract and yield low integral residuals.
2. Group-lasso nevertheless selects a stable proxy support and suppresses the physically required quadratic reaction term.

FIX5 also did **not** actually test Rho5 or Rho10 under S2, because their generator-valid center pools contained more than the pre-registered maximum of 12 centers. A large valid pool should be treated as an information-budget problem, not as evidence that the environment is invalid.

FIX6 therefore separates:

- temporal-center budget normalization;
- environment contract qualification;
- common-support identifiability;
- group-lasso shrinkage bias.

No official test block is opened and no architecture transition is authorized.

## Environment pool

All environments use Nu=0.5:

- Rho1: `ReacDiff_Nu0.5_Rho1.0.hdf5`, datafile 133177, MD5 `69a429239778d529cd419ed5888ea835`
- Rho2: `ReacDiff_Nu0.5_Rho2.0.hdf5`, datafile 133179, MD5 `ac907daa7e483d203a5c77567cdea561`
- Rho5: `ReacDiff_Nu0.5_Rho5.0.hdf5`, datafile 133180, MD5 `fb149e7540d8977af158bb8fec1048a3`
- Rho10: `ReacDiff_Nu0.5_Rho10.0.hdf5`, datafile 133178, MD5 `ff7c724b18e7ebe02e19c179852f48ee`

The first 1,000 rows of every file remain sealed.

## Splits

Relative to the training portion after the first 1,000 rows:

- fit A: 0:512
- fit B: 512:1024
- fit C: 1024:1536
- center-calibration: 1536:1600
- environment screen: 2048:2304
- support validation: 3072:3328
- final confirm: 3584:3840

## Frozen state and temporal contract

- FULL1024
- LocalTaylor R4 / degree5 / order3
- float64 arithmetic
- P13 canonical space only
- S2 Simpson integral-only
- normalized ridge alpha=1e-8

No DCC35, S4, or centered differential equation is used.

## Stage A — data-only valid-center pool

For each environment and each center c=2..98 on the calibration block:

`s_c = RMS(u_{c+1}-u_{c-1})`

`r_c = RMS(u_{c+1}-2u_c+u_{c-1})/(s_c+1e-12)`

A center enters the valid pool iff:

- `s_c >= 0.15 * max_c s_c`
- `r_c <= 0.40`

Require at least 3 pool centers.

There is **no upper validity bound**.

## Stage B — fixed information budget

Temporal center budget:

`B = 8`

If the valid pool contains <=8 centers, use all centers.

If it contains >8 centers, choose exactly 8 with a deterministic greedy D-optimal design using only the calibration-block P13 S2 design matrix.

D-optimal procedure:

1. Build the S2 P13 design matrix for every valid center on the calibration block.
2. Compute one pooled column scale across all valid centers.
3. Normalize all 13 columns by that pooled scale.
4. For each center compute its normalized Gram contribution.
5. Starting from an empty set, greedily add the center maximizing

`logdet(delta*I + sum_selected G_c)`

with `delta=1e-6`.

6. Ties are broken by smaller center index.

No target y, true PDE coefficient, or physical support is used in center-budget selection.

The resulting set is `BGENVALID_e`.

## Stage C — environment qualification

For every environment and every fit fold:

- fit independent restricted-full-P13 ridge on `BGENVALID_e`;
- evaluate on the disjoint environment-screen block.

An environment is contract-qualified iff:

- BGENVALID has >=3 centers;
- three-fold mean screen residual <=0.12;
- max fold screen residual <=0.15;
- all coefficients finite.

Require at least **3 qualified environments**.

The qualified set is frozen before support search.

## Stage D — exhaustive common-support search

P13 has 13 terms.

Enumerate every non-empty common support of size 1..6:

`sum_{k=1}^6 C(13,k)=4095`

For every support S:

- for each fold and qualified environment, fit coefficients only on S using normalized ridge;
- coefficient amplitudes remain environment-specific;
- evaluate on the support-validation block.

Primary validation score:

mean integral residual across all qualified environments and folds.

Let `E_best` be the minimum validation score over all 4095 supports.

A support is near-optimal iff:

`E_val <= 1.05 * E_best`.

Global selected support:

1. smallest support size among near-optimal supports;
2. lowest mean validation residual;
3. lexicographically smallest support-index tuple if still tied.

No true support or coefficient enters support selection.

## Fold-specific stability audit

For each fit fold separately:

- evaluate the same 4095 support candidates averaged over qualified environments;
- define the fold near-optimal set as <=1.05 times that fold's best validation score;
- choose by the same smallest-support / residual / lexicographic rule.

Require median pairwise Jaccard of the three fold-selected supports >=0.80.

## Stage E — final confirm

Freeze:
- BGENVALID per environment;
- qualified environment set;
- global common support.

Fit each fold/environment on the frozen support and evaluate on final confirm.

## Reporting-only physical audit

Only after all data-driven decisions are frozen.

Expected continuum common support:

`{R_u, R_u2, D0}`

Expected coefficients for every qualified environment:
- R_u = rho
- R_u2 = -rho
- D0 = 1

Report:
- support precision / recall / F1;
- active-coefficient relative L2;
- signs;
- spurious support;
- comparison against independent full-P13 ridge;
- reporting-only true-support validation rank and validation ratio to the selected support.

The true support is never used for fitting or selection.

## Frozen gates

### X1 — environment qualification
At least 3 environments qualify.

### X2 — final confirm closure
Across qualified env/folds:
- overall confirm mean <=0.10
- maximum environment mean <=0.12.

### X3 — support stability
- selected common support size <=6;
- fold-specific support median Jaccard >=0.80.

### X4 — physical support recovery
Reporting-only:
- recall of {R_u,R_u2,D0} =1.0
- precision >=0.75.

### X5 — coefficient fidelity
Reporting-only:
- correct signs in every qualified env/fold;
- overall active coefficient relative L2 mean <=0.30;
- maximum environment mean <=0.40.

### X6 — benefit versus independent ridge
At least ceil(N_qualified/2) environments improve mean active-coefficient relative error versus independent full-P13 ridge.

## Reporting-only support-equivalence diagnostic

After selection, compute:

`true_support_validation_ratio = E_val(true support) / E_val(selected support)`

and its rank among all 4095 candidates.

This diagnostic does not affect X1-X6.

## Routing

If X1-X6 all pass:

`RHO_AXIS_EXHAUSTIVE_SUPPORT_SUPPORTED`

If X1-X3 pass, X4/X5 fail, and true-support validation ratio <=1.05:

`SUPPORT_EQUIVALENCE_AMBIGUITY`

If X1-X3 pass, X4/X5 fail, and true-support validation ratio >1.05:

`FINITE_TIME_PROXY_SUPPORT_DOMINATES`

If X1 fails:

`INSUFFICIENT_BUDGET_QUALIFIED_ENVIRONMENTS`

If X1 passes but X2/X3 fail:

`RHO_AXIS_COMMON_SUPPORT_UNSTABLE`

Otherwise:

`REACTION_DIFFUSION_IDENTIFIABILITY_UNRESOLVED`

No official-test access, architecture transition, or 500-epoch training is authorized.
