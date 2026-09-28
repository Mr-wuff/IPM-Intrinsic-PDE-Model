# IPM-PDEBench-PB2-Q0-FIX6 Results — Budget-Normalized Rho-Sweep Exhaustive Common-Support Audit

## Integrity

Result ZIP SHA256:

`5d1292f5d4472473b49f4ce788d341728c660018b6e5d9a10624b7d6f3bc547b`

Detached checksum matches exactly.

Internal result manifest: **25/25 tracked payload entries match** by byte size and SHA256.

Protocol SHA256:

`ba965f7ff0ed93f2cfa0836af061140327be74ea59ca73c4a708f66644815ea9`

Frozen source notebook SHA256:

`57f4ff095d4f05adf5a3c0a86ccbc73b77fb60d8d2725f89ce2b1072e1ee2daa`

Executed notebook SHA256:

`43be68b9fb0f848e49b1304ed94bcd977d712dea392a37b74d5864edb23a0975`

The executed notebook contains 9 code cells and no runtime-error outputs.

A direct cell-by-cell comparison against the frozen source notebook shows **zero source-cell differences**. The file hash differs only because execution outputs / notebook metadata were embedded.

Official test accessed: **false**.

## Formal outcome

All frozen gates pass:

- X1 environment qualification: **PASS**
- X2 final confirm closure: **PASS**
- X3 support stability: **PASS**
- X4 physical support recovery, reporting-only: **PASS**
- X5 physical coefficient fidelity, reporting-only: **PASS**
- X6 benefit versus full-P13 ridge: **PASS**

Primary route:

**RHO_AXIS_EXHAUSTIVE_SUPPORT_SUPPORTED**

No architecture transition or official-test unlock is authorized by this run itself; the next step is independent held-out parameter confirmation of the frozen support-learning result.

## Valid pools and target-free D-optimal budget

Raw valid pools:
- Rho1: 7 centers
- Rho2: 12 centers
- Rho5: 38 centers
- Rho10: 25 centers

Frozen budgeted centers:
- Rho1: [2,3,4,5,6,7,8]
- Rho2: [2,3,4,5,6,7,8,13]
- Rho5: [2,3,4,5,6,23,31,39]
- Rho10: [2,3,4,5,6,13,23,26]

The D-optimal budget therefore successfully converts large valid pools into fixed-size identification designs instead of rejecting them.

## Environment qualification

All four development environments qualify:

### Rho1
- screen mean: **0.058790**
- max fold: **0.058819**

### Rho2
- screen mean: **0.032668**
- max fold: **0.032671**

### Rho5
- screen mean: **0.029227**
- max fold: **0.029298**

### Rho10
- screen mean: **0.018413**
- max fold: **0.018427**

Thus X1 passes with four qualified environments.

## Exhaustive common-support search

All 4,095 non-empty P13 supports of size 1..6 were evaluated.

Absolute best validation support:

`[R_u, R_u2, R_u3, D0, D_u, D_u2]`

Validation mean:

**0.0338003**

The globally selected frozen near-optimal support is:

`[R_u, R_u2, D0]`

Validation mean:

**0.0342002**

This is only:

**1.183%**

above the absolute best six-term support and therefore lies inside the frozen 1.05x near-optimal set.

It is also the **only size-3 support** in the near-optimal set.

Fold-specific selected supports:
- fold 0: [R_u, R_u2, D0]
- fold 1: [R_u, R_u2, D0]
- fold 2: [R_u, R_u2, D0]

Median fold-pair Jaccard:

**1.0**

Thus the support is both minimal and fold-stable.

## Final internal confirm

Overall confirm integral mean:

**0.0370608**

Per environment:
- Rho1: **0.0650204**
- Rho2: **0.0341962**
- Rho5: **0.0302010**
- Rho10: **0.0188255**

All are comfortably within the frozen closure gates.

## Reporting-only physical support audit

Expected common continuum support:

`[R_u, R_u2, D0]`

Selected common support:

`[R_u, R_u2, D0]`

Therefore:
- support precision: **1.0**
- support recall: **1.0**
- support F1: **1.0**

The exact physical support is recovered without being used in center selection, environment qualification, or support selection.

## Reporting-only coefficient recovery

### Rho1
Three folds:
- R_u ≈ 0.681–0.702
- R_u2 ≈ -0.575 to -0.611
- D0 ≈ 0.9941–0.9948

Mean active-coefficient relative L2 error:

**0.29547**

### Rho2
- R_u ≈ 2.028–2.038
- R_u2 ≈ -2.034 to -2.052
- D0 ≈ 0.9910–0.9917

Mean error:

**0.01788**

### Rho5
- R_u ≈ 5.031–5.061
- R_u2 ≈ -5.043 to -5.091
- D0 ≈ 0.9915–0.9923

Mean error:

**0.01216**

### Rho10
- R_u ≈ 10.106–10.124
- R_u2 ≈ -10.136 to -10.163
- D0 ≈ 0.9911–0.9917

Mean error:

**0.01349**

Overall reporting-only physical active-coefficient relative L2:

**0.08475**

All signs are correct in every environment and fold.

## Benefit versus independent full-P13 ridge

Mean reporting-only active-coefficient error:

### Rho1
- independent: 0.76310
- selected physical support: 0.29547

### Rho2
- independent: 0.52465
- selected: 0.01788

### Rho5
- independent: 0.15453
- selected: 0.01216

### Rho10
- independent: 0.05128
- selected: 0.01349

All four environments improve.

Thus X6 passes strongly.

## Support-equivalence diagnostic

The reporting-only true physical support is exactly the selected support.

Its validation mean is:

**0.0342002164**

Absolute best validation mean among all 4095 candidates:

**0.0338002991**

Ratio:

**1.01183**

Validation rank of the physical support by raw residual alone:

**137 / 4095**

This apparent rank is expected because larger supports can make tiny residual improvements.

Crucially, among the frozen <=1.05x near-optimal candidates:
- 213 supports are near-optimal;
- exactly **one** has size 3;
- that unique minimal near-optimal support is the physical support.

Therefore model selection by minimal near-optimal support resolves the proxy-support ambiguity without any physical-label leakage.

## Scientific conclusion

FIX6 resolves the principal PB2 Reaction-Diffusion identifiability bottleneck on the fixed-Nu rho-sweep development axis.

Two previous confounds are now causally separated:

1. large generator-valid pools must be budget-normalized rather than rejected;
2. group-lasso shrinkage can select stable proxy terms when canonical features are strongly correlated.

With target-free D-optimal temporal budgeting and exhaustive minimal-near-optimal common-support selection, IPM recovers the correct Reaction-Diffusion support:

`R_u + R_u2 + D0`

across Rho=1,2,5,10, with exact fold support stability and low coefficient error.

The next experiment must be an independent held-out **diffusion-axis** confirmation using previously unused parameter environments. The support itself is now frozen and must not be re-selected there.
