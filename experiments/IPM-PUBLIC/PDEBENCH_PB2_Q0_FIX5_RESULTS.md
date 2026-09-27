# IPM-PDEBench-PB2-Q0-FIX5 Results — Environment-Qualified Rho-Sweep Shared-Support Audit

## Integrity

Result ZIP SHA256:

`e727ade7ba24b4d0bb848f726e5cb1f2c53ab6ab245fbdc2ff4ba7ab31933848`

Detached checksum matches exactly.

Internal manifest: **28/28 tracked payload entries match** by byte size and SHA256.

Protocol SHA256:

`1465e3936ab0ee53a9b301e7a8ca7d3a14d2f450e2d00e1bd949ea698b7c62c1`

Executed notebook SHA256:

`265940aee8e7413e9dbc0ae45c1c79f55843c35699b11b36d76e7bf3c13ad294`

Frozen source notebook SHA256 from the run record:

`a21c8f731174c7efc372a85e4ef079c9bf914a31adcbf6e000c0034060c55959`

The embedded frozen protocol matches exactly. The executed notebook has 9 code cells and no runtime-error outputs. Full-file source-byte identity is not claimed because execution outputs change the notebook hash.

Official test accessed: **false**.

## Formal outcome

Frozen gates:

- Q1 at least two contract-qualified environments: **PASS**
- Q2 confirm residual closure: **PASS**
- Q3 support stability/sparsity: **PASS**
- Q4 physical support recovery, reporting-only: **FAIL**
- Q5 physical coefficient fidelity, reporting-only: **FAIL**
- Q6 benefit versus independent ridge: **PASS**

Primary route:

**RHO_AXIS_EFFECTIVE_SUPPORT_ONLY**

No architecture transition, official-test unlock, or long training is authorized.

## Generator-validity pools

Data-only generator-valid centers:

- Rho1: 7 centers, [2..8]
- Rho2: 12 centers, [2..13]
- Rho5: 38 centers, [2..39]
- Rho10: 25 centers, [2..26]

The frozen protocol required 3..12 centers.

Therefore:
- Rho1 qualified for independent screen evaluation;
- Rho2 qualified for independent screen evaluation;
- Rho5 and Rho10 were excluded **before** screen fitting solely because their valid-center pools exceeded the pre-registered maximum of 12.

No S2 residual conclusion can be drawn for Rho5 or Rho10 from FIX5.

This is an important design finding: having more than 12 generator-valid centers is not evidence that an environment is physically invalid. The upper bound acted as a computational/selection budget but was encoded as a validity rejection.

## Environment qualification

### Rho1
- center count: 7
- screen residual mean: **0.058790**
- screen residual max: **0.058819**
- qualified: yes

### Rho2
- center count: 12
- screen residual mean: **0.037091**
- screen residual max: **0.037094**
- qualified: yes

### Rho5
- center count: 38
- not evaluated under S2 because center-count gate failed
- qualified: no

### Rho10
- center count: 25
- not evaluated under S2 because center-count gate failed
- qualified: no

Thus the group-support stage used only Rho1 and Rho2.

## Group-sparse selection

Validation lambda path is smooth and stable.

Selected:

`lambda/lambda_max = 0.0001`

Three-fold supports are identical:

`[R0, R_u, R_u3, D0, D_u, D_u2]`

Support Jaccard median:

**1.0**

Standardized coefficient-matrix cosine median:

**0.9997195**

This is not an optimizer-instability failure.

## Confirm closure

### Rho1
Three folds:
- 0.064279
- 0.064131
- 0.064298

Mean:

**0.064236**

### Rho2
Three folds:
- 0.038267
- 0.038299
- 0.038302

Mean:

**0.038289**

Overall confirm mean:

**0.051263**

Therefore Q2 passes comfortably.

## Physical support audit

Reporting-only true continuum common support:

`[R_u, R_u2, D0]`

Selected consensus support:

`[R0, R_u, R_u3, D0, D_u, D_u2]`

Metrics:
- support precision: **0.3333**
- support recall: **0.6667**
- F1: **0.4444**

The physically essential quadratic reaction term `R_u2` is absent.

The shared-support model therefore finds a highly stable **effective proxy support**, not the governing support.

## Physical coefficients

Joint-support fits set `R_u2=0` in all folds.

Rho1:
- R_u ≈ 0.198–0.255
- D0 ≈ 1.013–1.018
- physical active-coefficient relative error mean: **0.7304**

Rho2:
- R_u ≈ 0.822–0.890
- D0 ≈ 0.987–0.990
- physical active-coefficient relative error mean: **0.7664**

Diffusion remains accurately represented, while the reaction decomposition is wrong.

## Independent-ridge comparison

Independent physical active-coefficient error:
- Rho1 mean: **0.7631**
- Rho2 mean: **0.3785**

Joint shared-support:
- Rho1 improves slightly to **0.7304**
- Rho2 worsens strongly to **0.7664**

One of two environments improves, satisfying the frozen Q6 ceiling-half rule, but the shared-support prior clearly harms the more informative Rho2 environment.

## Scientific conclusion

FIX5 demonstrates:

1. environment qualification before support pooling is necessary;
2. Rho1 and Rho2 are both compatible with the frozen S2 contract;
3. group-sparse support is numerically stable and gives excellent integral closure;
4. nevertheless it selects correlated proxy terms instead of the physical reaction support;
5. the stronger-reaction Rho5/Rho10 environments were not actually tested because the pre-registered 12-center upper bound excluded them.

The next experiment should therefore address two distinct confounds:

### A. Generator-validity budget semantics
A large valid-center pool should be deterministically down-selected to a fixed information budget rather than rejected as an invalid environment.

### B. Group-lasso support-selection bias
Because P13 has only 13 terms, a deterministic exhaustive common-support audit over small supports is feasible and can directly determine whether the physical support is distinguishable from effective proxy supports without relying on shrinkage.

No threshold relaxation is justified.
