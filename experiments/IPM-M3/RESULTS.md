# IPM-M3 Results

## Formal preregistered decision
**PASS_M3**

Result ZIP SHA256:
`798f539da61c0f09ce9cb332fe1ee2a873387faed1589ff7465a0312c286fdb5`

The checksum matches the returned `.sha256` file. The executed notebook code cells are identical to the frozen released notebook.

## Gate result
All 11 preregistered gates passed.

Key derived metrics:
- IntegralFlow hidden exact-Q mean Rel-RMSE: **0.05255**
- SecantDerivative: **0.07935**
- OracleRHS: **0.07939**
- hidden-Q good PDE families: **5/5**
- Jacobian-discovery good families: **5/5**
- spurious-order suppression good families: **5/5**
- base-rollout good families: **5/5**
- held-out stride residual: **0.05243**
- training-stride residual: **0.05245**
- formal 64/128/256 grid degradation: **0.9968**
- family wins vs SecantDerivative: **5/5**
- seed discovery reproducibility: **5/5**

## Per-family trajectory-only law recovery

| PDE | IntegralFlow hidden Q Rel-RMSE | Base rollout Rel-L2 | Jacobian cosine | Spurious-order ratio |
|---|---:|---:|---:|---:|
| Advection | 0.01966 | 0.00146 | 0.99926 | 0.02809 |
| Allen-Cahn | 0.14624 | 0.00502 | 0.94648 | 0.02892 |
| Burgers | 0.04281 | 0.00490 | 0.98430 | 0.00120 |
| Heat | 0.01622 | 0.00047 | 0.98725 | 0.12993 |
| KdV | 0.03782 | 0.00305 | 0.99320 | 0.00340 |

This is strong evidence that the frozen IPM core can be identified from trajectories without exact instantaneous RHS labels.

## Held-out temporal-window evidence

The stride-3 residual, which was not used for training, is essentially identical to the mean training-stride residual.

This supports a continuous-law interpretation rather than simple memorization of one observation interval.

## Grid transfer

From N=64 through N=256, the trajectory-trained local law is almost perfectly resolution invariant.

The previously observed extreme N=512 degradation remains:
- Advection: ~0.0353
- Allen-Cahn: ~0.0138
- Burgers: ~0.0331
- Heat: ~0.00030
- KdV: ~0.0287

N=512 remains a separate high-frequency diagnostic issue.

## Critical fairness audit

Although the preregistered M3 decision is PASS, the direct performance ordering between IntegralFlowIPM, SecantDerivative, and OracleRHS is confounded by unequal optimization budgets.

With trajectory_steps=32 and train_traj=18:

- IntegralFlow windows per epoch:
  [
  18[(32-2+1)+(32-4+1)+(32-8+1)] = 1530
  ]
- Center-window samples for Oracle/Secant:
  [
  18(32-1)=558
  ]

At batch size 12 this gives approximately:
- IntegralFlow: **128 optimizer steps/epoch**
- Oracle/Secant: **47 optimizer steps/epoch**

Ratio:
[
128/47 approx 2.72.
]

Therefore the surprising result that IntegralFlow outperforms even exact-RHS Oracle supervision cannot yet be attributed to the identification principle itself.

## Correct scientific interpretation

M3 establishes:
1. trajectory-only integral-flow training can recover an accurate IPM local law;
2. the recovered law preserves differential-order discovery and Cartan consistency;
3. trajectory-only rollout and 64–256 grid transfer are strong.

M3 does **not yet establish** that IntegralFlow is intrinsically superior to SecantDerivative or OracleRHS.

## Required replication

**IPM-M3-FIX1 — Compute- and Observation-Matched Identification**

The mathematical IPM core remains frozen.

The three objectives will use:
- identical initial weights per family/seed;
- identical sampled trajectory triplets;
- identical stride schedule;
- identical batch size;
- identical optimizer-step count;
- identical learning-rate schedule.

Only the objective differs.

This replication is required before any paper claim comparing IntegralFlow against derivative supervision is frozen.
