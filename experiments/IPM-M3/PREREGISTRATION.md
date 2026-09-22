# IPM-M3 — Trajectory-Only Integral Flow Identification

## Purpose

M2-FIX1 passed the first-principles mechanism qualification and freezes the mathematical IPM core:

1. overcomplete holonomic jet;
2. learned local characteristic (Q_\theta);
3. Cartan total derivative / prolongation;
4. induced evolutionary vector field (V_Q);
5. solver-independent continuous-flow interpretation.

M3 removes the final strong supervision used so far: exact instantaneous (u_t) / PDE RHS targets.

The proposed IPM learner sees only solution trajectories, physical parameters, and observation times.

## First-principles training identity

For a learned local PDE law

[
u_t = Q_\theta(j^3u,\lambda),
]

the fundamental theorem of calculus gives

[
u(t_b)-u(t_a)
=
\int_{t_a}^{t_b} Q_\theta(j^3u(t),\lambda)\,dt.
]

M3 uses observed trajectory states to approximate this integral. No numerical time derivative is required for the proposed training objective.

For three equally spaced observed states (u_0,u_1,u_2) with spacing (h),

[
u_2-u_0
\approx
\frac{h}{3}
\left[
Q_\theta(j^3u_0)
+4Q_\theta(j^3u_1)
+Q_\theta(j^3u_2)
\right].
]

Training uses multiple observed spacings to discourage a law that only matches one temporal discretization.

## What is and is not claimed

Integral-form system identification and trajectory-based continuous-time learning already exist. The M3 novelty claim is **not** the Simpson quadrature loss itself.

M3 tests whether the previously frozen IPM mathematical core can be identified from trajectory data alone while preserving:
- Cartan consistency;
- differential-order discovery;
- solver-independent rollout.

## Methods

All methods use exactly the same local characteristic architecture and the same overcomplete (J^3u).

1. **OracleRHS** — exact (u_t) supervision; upper-bound reference only.
2. **SecantDerivative** — trajectory-only central finite-difference derivative labels.
3. **IntegralFlowIPM** — proposed trajectory-only integral-flow matching; no derivative labels.

## Data contract

The proposed IntegralFlowIPM trainer receives only:
- observed field states;
- physical parameters;
- observation spacing.

Its dataset contains no (u_t), PDE RHS, PDE-family equation terms, or analytic Jacobian.

The notebook hashes the proposed learner source and performs an explicit no-RHS-leakage audit.

## PDE suite

Every model receives the same overcomplete local state:

[
J^3u=(u,u_x,u_{xx},u_{xxx}).
]

Families:
- Heat
- Linear advection
- Viscous Burgers
- Allen-Cahn
- KdV

Separate local laws are trained per family in M3. Cross-family sharing remains outside this mechanism stage.

## Trajectory observation protocol

Base observation spacing:
[
\Delta t_{obs}=1.25\times10^{-3}.
]

IntegralFlowIPM trains on Simpson windows with stride:
[
s\in\{1,2,4\}.
]

A held-out stride (s=3) is used for integral-law consistency evaluation.

## Formal seeds

11, 29, 47, 71, 97.

## Evaluation

Analytic PDE information is permitted **only after training** for controlled evaluation:
- hidden exact-(Q) relative RMSE;
- PDE-law Jacobian cosine;
- spurious derivative-order sensitivity;
- learned Cartan (D_xQ) identity;
- common external RK4 rollout;
- grid transfer 64/128/256;
- N=512 diagnostic only;
- held-out integral-window residual;
- five-seed reproducibility.

## Frozen gates

G0 — protocol/core/learner-source integrity and no-RHS-leakage audit PASS.  
G1 — IntegralFlowIPM training finite on all families/seeds.  
G2 — hidden exact-Q relative RMSE <=0.30 on >=4/5 families.  
G3 — IntegralFlowIPM exact-Q RMSE <=1.35x SecantDerivative average and <=2.0x OracleRHS average.  
G4 — Jacobian cosine >=0.80 on >=4/5 families.  
G5 — spurious-order sensitivity <=0.25 on >=4/5 families.  
G6 — base common-RK4 rollout finite on all families/seeds and mean final Rel-L2 <=0.12 on >=4/5 families.  
G7 — held-out stride-3 normalized integral residual <=1.10x the training-stride mean residual.  
G8 — 64/128/256 grid-transfer mean degradation <=1.50x the N=128 baseline; N=512 is reported separately.  
G9 — IntegralFlowIPM beats SecantDerivative on either exact-Q error or base-rollout error in >=3/5 PDE families.  
G10 — trajectory-only differential-order discovery direction is reproduced in >=4/5 formal seeds.

Decision:
- PASS_M3: G0/G1 mandatory plus at least 7 of G2–G10.
- CONDITIONAL_M3: integrity/training passes but trajectory-only law identification is incomplete.
- FAIL_M3: proposed integral-flow learner cannot identify a stable IPM characteristic.

## Advancement

PASS_M3 establishes that the frozen IPM core can be learned from trajectories without exact RHS labels.

The next stage would address sparse/noisy observations and the unresolved extreme-resolution/high-frequency regime before the full paper benchmark.
