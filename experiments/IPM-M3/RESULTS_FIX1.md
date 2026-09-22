# IPM-M3-FIX1 Results — Matched-Budget Identification

## Formal decision
**PASS_M3_FIX1**

Result ZIP SHA256:
`57a5b6aa6f255ad526b1c7ba3a83e092205f23f323ef347b15a84b548c3505b2`

The returned checksum matches the supplied `.sha256` file.

## User-side script correction

The released notebook embedded JSON booleans (`true`) directly into Python source, causing a `NameError` before execution.

The executed notebook changes only:
- `true -> True` for three Boolean values in `FROZEN_PROTOCOL`.

All other code cells are identical to the released notebook. After the correction:
- protocol integrity PASS;
- IPM core integrity PASS;
- IntegralFlow objective integrity PASS;
- matched sampler integrity PASS;
- no-RHS leakage audit PASS.

This is an implementation/serialization fix before training and does not change the logical protocol. Future notebooks must embed protocol data via a Python-safe representation or parse canonical JSON explicitly.

## Frozen fairness audit

Every method used:
- identical initial weights per PDE/seed;
- identical sampled trajectory triplets per optimizer step;
- identical stride schedule;
- identical batch size;
- identical AdamW/LR schedule;
- exactly 1536 optimizer updates;
- final checkpoint only.

All optimizer-step and deterministic-triplet audits passed.

## Headline matched-budget result

Mean hidden exact-Q Rel-RMSE:
- IntegralFlowIPM: **0.0701412**
- SecantDerivative: **0.0701303**
- OracleRHS: **0.0701689**

Mean base rollout Rel-L2:
- IntegralFlowIPM: **0.00426161**
- SecantDerivative: **0.00426116**
- OracleRHS: **0.00425843**

The differences are extremely small. Paired comparisons across 25 PDE-seed pairs give no statistically meaningful superiority for IntegralFlow:
- Integral vs Secant hidden-Q mean difference ~1.09e-5;
- Integral vs Secant rollout mean difference ~4.46e-7;
- paired 95% intervals include zero.

Therefore the correct paper-level interpretation is **performance equivalence under matched budget**, not superiority.

## Per-family IntegralFlowIPM hidden-Q Rel-RMSE
- Advection: 0.02776
- Allen-Cahn: 0.18106
- Burgers: 0.06325
- Heat: 0.02247
- KdV: 0.05616

## Differential-law structure

IntegralFlowIPM mean Jacobian cosine:
- Advection: 0.99835
- Allen-Cahn: 0.92663
- Burgers: 0.98308
- Heat: 0.97674
- KdV: 0.98994

Mean spurious-order ratio:
- Advection: 0.04014
- Allen-Cahn: 0.03886
- Burgers: 0.00166
- Heat: 0.18061
- KdV: 0.00490

All five PDE families pass the frozen Jacobian and spurious-order gates.

## Held-out observation spacing

Stride-3 held-out integral residual:
- 0.0699988

Mean training-stride residual:
- 0.0700222

The unseen temporal spacing is essentially indistinguishable from the training strides, supporting a continuous-law interpretation.

## Grid transfer

IntegralFlowIPM mean final field errors:

| PDE | N=64 | N=128 | N=256 | N=512 |
|---|---:|---:|---:|---:|
| Advection | 0.001159 | 0.001173 | 0.001181 | 0.043206 |
| Allen-Cahn | 0.003639 | 0.003694 | 0.003721 | 0.013558 |
| Burgers | 0.002837 | 0.002878 | 0.002905 | 0.039390 |
| Heat | 0.000378 | 0.000381 | 0.000382 | 0.000383 |
| KdV | 0.002185 | 0.002214 | 0.002387 | 0.030352 |

64/128/256 transfer remains essentially invariant. N=512 remains the unresolved high-frequency regime.

## Scientific conclusion

M3-FIX1 establishes:

1. the IPM characteristic can be identified from trajectories without instantaneous RHS labels;
2. under strictly matched compute and observations, IntegralFlow is **statistically equivalent** to central-secant and exact-RHS supervision at the present approximation floor;
3. trajectory-only training preserves differential-order discovery;
4. the learned local law remains resolution-stable through N=256;
5. the remaining core limitation is extreme-resolution/high-frequency behavior, not ordinary grid dependence.

The next paper-development stages should focus on:
- sparse/noisy trajectory observations;
- high-frequency robustness and N=512 diagnosis;
- multi-PDE/unseen-PDE generalization;
- comprehensive accuracy/efficiency benchmarking.
