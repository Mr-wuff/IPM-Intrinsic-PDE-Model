# IPM-PDEBench-PB1-Q7 Results — Direct Canonical Integral Core Qualification

## Integrity

Result ZIP SHA256:

`085ca327ba2a90e7d8b5df1d28284229f693d16490a1241872f73476c60319b5`

Detached manifest: **22/22 payload entries match** by byte size and SHA256.

Protocol SHA256:

`0fed71fbee5bcffed09266508e419c421e817bb9a10f0dae9ac69a1784a274d6`

The official first 1,000 PDEBench test trajectories were not loaded.

## Execution deviation

The executed notebook differs from the frozen Q7 notebook by one necessary implementation repair in the DCC35 -> principal projection:

Frozen:
`vals=[c35[FULL_INDEX[e]] for e in PRINCIPAL_EXPS]`

Executed:
`vals=[c35[FULL_INDEX[e]] if e in FULL_INDEX else 0.0 for e in PRINCIPAL_EXPS]`

Reason: DCC-35 is the complete total-degree <=3 polynomial basis. The legacy 16-term RTDS principal list also contains `u^3 a1`, `u^3 a2`, and `u^3 a3`, which have total degree 4 and therefore do not exist in DCC-35.

The repair assigns those absent terms coefficient zero. No data split, objective, threshold, metric, fit coefficient, or result gate was changed.

This exposes a basis-definition mismatch that must be removed in the next stage. The mathematically consistent principal subspace of DCC-35 has 13 terms:
- R: `1,u,u^2,u^3`
- T/D/S: `a_r, u a_r, u^2 a_r`

## Frozen gate outcome

- DCC35 confirm characteristic mean: **0.218421**
- DCC35 confirm characteristic max: **0.221060**
- DCC-P16 confirm characteristic mean: **0.198081**
- DCC35 / P16 characteristic ratio: **1.102684**
- DCC35 / frozen-Q5-principal characteristic ratio: **0.311592**
- DCC35 refined 31-step confirm rollout mean: **0.201368**
- DCC35 refined 31-step confirm rollout max: **0.203990**
- DCC-P16 refined 31-step rollout mean: **0.178964**
- projected DCC35 / P16 rollout ratio: **1.125186**
- median cross-fold DCC35 coefficient cosine: **0.999993745**

Gate status:
- Q7-1 direct canonical identification: **FAIL**
- Q7-2 trajectory-integral closure: PASS
- Q7-3 factorization repair: PASS
- Q7-4 full-space viability: PASS
- Q7-5 coefficient stability: PASS
- Q7-6 no hidden expanded deployment need: PASS

Formal status:

**PB1-Q7 FAIL — 5/6 GATES PASS; ARCHITECTURE TRANSITION NOT AUTHORIZED**

The preregistered characteristic threshold is not relaxed post hoc.

## Key scientific evidence

### 1. DCC is a strong repair despite formal failure

Relative to the frozen Q5 principal characteristic error `0.700983`, DCC-35 reaches `0.218421`, a **68.84% reduction**.

Its compiled/refined 31-step internal rollout is also stable at about `0.20`.

Thus the direct canonical approach is viable, but the generic full-space identification contract is not yet sufficiently accurate to freeze.

### 2. Integral-only full-space identification reveals an identifiability gap

DCC-35 has lower confirm Simpson-integral residual than DCC-P16:
- DCC35: about **0.075**
- DCC-P16: about **0.100**

Yet DCC-35 has worse instantaneous characteristic error:
- DCC35: **0.2184**
- DCC-P16: **0.1981**

The column-normalized normal-system condition number is also very different:
- DCC35: about **1.95e5 to 2.18e5**
- DCC-P16: about **30 to 37**

This indicates that the full 35-term canonical space contains trajectory-integral alias/null directions: multiple local laws can explain the finite-time Simpson increments similarly while differing more strongly in their instantaneous differential characteristic.

### 3. Coefficient instability is not the issue

Despite the poor full-space conditioning, three disjoint DCC35 fit folds are almost identical:

median pairwise cosine = **0.999994**.

Therefore the failure is not random fit instability. It is a systematic identification-contract bias/aliasing problem.

### 4. The main Burgers law is recovered

Across folds, DCC35 reporting-only coefficients are approximately:
- `u*a1`: **-0.998 to -1.000**
- `a2`: **0.00618 to 0.00629**

The nonlinear transport coefficient is essentially recovered. Diffusion remains attenuated relative to the reporting-only Taylor-coordinate value `0.02`.

### 5. The basis mismatch must be removed

The generic DCC35 space is total-degree <=3, while legacy P16 contains three total-degree-4 monomials.

Future direct-canonical experiments must use the exact 13-term principal subspace of DCC35 (P13), with missing quartic principal coefficients identically zero in the runtime.

## Next mechanism

The next stage should not add model capacity or run long SGD.

It should repair the identification contract using **differential-integral consistency**:
- preserve trajectory-only Simpson integral equations;
- add a dimensionless central-difference differential consistency equation from the same trajectories;
- solve one joint linear canonical system;
- use the mathematically consistent DCC35/P13 basis relation.

This directly targets the only Q7 failure: full-space instantaneous-law identifiability under integral-only constraints.
