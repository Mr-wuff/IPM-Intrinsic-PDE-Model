# IPM-M2-FIX1 Results

## Formal decision
**PASS_M2_FIX1**

Result ZIP SHA256:
`c5666312809929f2ba5a7973ccb9afa9176c8ca4e1bce4723d2abc82d10158a6`

The checksum matches the returned `.sha256` file.

The executed notebook source is identical to the frozen notebook source. The notebook-file hash differs only because execution outputs and metadata were added.

## Gate summary

Passed:
- G0 integrity
- G1 analytic Cartan identity
- G2 learned Cartan (D_xQ)
- G3 learned-flow temporal identity (V_Q(Q))
- G4 PDE-law Jacobian cosine
- G5 spurious-order suppression
- G6 instantaneous law validation
- G7 base rollout
- G9 five-seed differential-order reproducibility

Failed:
- G8 grid transfer

The preregistered decision rule therefore gives **PASS_M2_FIX1**.

## Structural evidence

### Analytic Cartan identity
Relative error across 64/128/256/512:
~5.01e-8.

### Learned Cartan spatial derivative
Mean relative error:
[
5.91	imes 10^{-5}.
]

### Learned-flow temporal identity
Mean relative error:
[
9.22	imes 10^{-4}.
]

This confirms that, when the finite-difference audit follows the learned flow itself, the evolutionary identity (V_Q(Q)) is numerically consistent.

## Differential-order discovery

Every law received the same overcomplete (J^3u=(u,u_x,u_{xx},u_{xxx})), without being told its physical PDE order.

Mean Jacobian attribution:

| PDE | Jacobian cosine | Relative Jacobian error | Spurious-order ratio |
|---|---:|---:|---:|
| Advection | 0.99196 | 0.12470 | 0.10671 |
| Allen-Cahn | 0.84204 | 0.55199 | 0.04455 |
| Burgers | 0.94620 | 0.33246 | 0.00427 |
| Heat | 0.95736 | 0.30156 | 0.26588 |
| KdV | 0.95568 | 0.30435 | 0.01582 |

Four of five PDEs pass the frozen 0.85 Jacobian-cosine requirement.

Four of five PDEs pass the frozen <=0.20 spurious-order sensitivity requirement.

The direction of differential-order discovery is reproduced in all five formal seeds.

## Instantaneous-law fitting

Mean validation relative RMSE:
- Advection: 0.0558
- Heat: 0.0620
- KdV: 0.1265
- Burgers: 0.1786
- Allen-Cahn: 0.2251

Allen-Cahn is the only family above the 0.20 gate.

## Base rollout

Common external RK4 mean final field Rel-L2:
- Heat: 0.00218
- Allen-Cahn: 0.00669
- Advection: 0.00775
- KdV: 0.01099
- Burgers: 0.02387

All five PDE families pass the <=0.10 base-rollout criterion.

## Grid transfer

The only failed formal gate is G8.

Mean final errors:

| PDE | N=64 | N=128 | N=256 | N=512 |
|---|---:|---:|---:|---:|
| Advection | 0.00324 | 0.00325 | 0.00326 | 0.05343 |
| Allen-Cahn | 0.00351 | 0.00357 | 0.00359 | 0.00973 |
| Burgers | 0.00940 | 0.00953 | 0.00961 | 0.03922 |
| Heat | 0.00042 | 0.00042 | 0.00042 | 0.00042 |
| KdV | 0.00499 | 0.00504 | 0.00531 | 0.02931 |

A crucial observation is that transfer from N=64 through N=256 is essentially resolution-invariant for every family. The degradation is concentrated at N=512.

This suggests a high-frequency/continuous-law extrapolation limitation rather than a generic grid-index dependence. Because the local law is pointwise, the current hypothesis is that finer grids admit high-frequency jet states outside the spectral distribution seen during training.

## Core conclusion

M2-FIX1 supplies the first convincing evidence for freezing the mathematical IPM core:

1. overcomplete holonomic local jet;
2. learned local characteristic (Q_	heta);
3. Cartan total-derivative prolongation;
4. induced evolutionary vector field (V_Q);
5. solver-independent continuous-flow interpretation.

The numerical integrator is not part of the architecture definition.

## Remaining limitations before paper benchmark
- N=512 high-frequency grid transfer;
- Allen-Cahn law-fitting quality;
- Heat spurious high-order sensitivity;
- current training still uses exact instantaneous RHS labels.

## Next stage
**IPM-M3 — Trajectory-Only Integral Flow Identification**

The model will no longer receive (u_t) / PDE RHS targets.

Training will use only observed trajectories and the fundamental flow identity:

[
u(t_b)-u(t_a)=int_{t_a}^{t_b}Q_	heta(j^3u(t),lambda),dt.
]

This tests whether the frozen first-principles IPM core can identify the local PDE law directly from solution trajectories.
