# IPM-M3-FIX1 — Compute- and Observation-Matched Identification

## Purpose

IPM-M3 passed all preregistered gates and established that the frozen IPM core can be identified from trajectories alone.

However, IntegralFlowIPM received approximately 2.72x more optimizer steps per epoch than OracleRHS and SecantDerivative because its multi-stride dataset produced more windows.

M3-FIX1 removes this confound without changing the IPM mathematical core.

## Frozen IPM core

Unchanged from M3:
1. overcomplete holonomic J3 state;
2. local characteristic Q_theta;
3. Cartan total derivative / prolongation;
4. solver-independent continuous-flow interpretation.

No new neural architecture components are introduced.

## Fairness protocol

For each PDE family and formal seed:

- all three methods start from the exact same initial state_dict;
- all methods consume the exact same sampled trajectory triplets;
- all methods use the same stride schedule;
- all methods use the same batch size;
- all methods execute exactly the same number of optimizer steps;
- all methods use the same optimizer and LR schedule;
- all methods are evaluated on the same held-out trajectory states.

Only the training objective changes.

## Shared triplet

Each sampled item is:
[
(u_i,u_{i+s},u_{i+2s},lambda,h=sDelta t).
]

Methods:

### OracleRHS
Use the middle state only:
[
Q_	heta(j^3u_{i+s},lambda)approx u_t(t_{i+s}).
]

### SecantDerivative
Use the same triplet:
[
Q_	heta(j^3u_{i+s},lambda)
approx
rac{u_{i+2s}-u_i}{2h}.
]

### IntegralFlowIPM
Use the same triplet:
[
u_{i+2s}-u_i
approx
rac{h}{3}
[Q_i+4Q_{i+s}+Q_{i+2s}].
]

Thus all three methods receive one matched triplet per training sample.

## Stride schedule

Training strides:
[
sin{1,2,4}.
]

The sampler draws strides with equal probability using a deterministic seed.

Held-out stride:
[
s=3.
]

## Formal training budget

- batch size: 12 triplets
- steps per epoch: 64
- epochs: 24
- optimizer: AdamW
- same cosine LR schedule
- 5 formal seeds

Every method therefore receives exactly:
[
64	imes24=1536
]
optimizer updates per family/seed.

## Evaluation

- hidden exact-Q Rel-RMSE;
- common external RK4 rollout;
- differential-law Jacobian cosine;
- spurious-order sensitivity;
- held-out stride-3 integral residual;
- 64/128/256 grid transfer;
- N=512 diagnostic;
- five-seed reproducibility.

## Gates

G0 — protocol/core/source integrity PASS.  
G1 — optimizer-step counts exactly equal for all methods/families/seeds.  
G2 — IntegralFlow hidden-Q mean <=1.25x SecantDerivative mean.  
G3 — IntegralFlow base-rollout mean <=1.25x SecantDerivative mean.  
G4 — IntegralFlow beats SecantDerivative on hidden-Q or rollout in >=3/5 PDE families.  
G5 — IntegralFlow Jacobian cosine >=0.80 on >=4/5 PDE families.  
G6 — spurious-order ratio <=0.25 on >=4/5 PDE families.  
G7 — held-out stride-3 residual <=1.10x mean training-stride residual.  
G8 — 64/128/256 grid degradation <=1.50x N=128 baseline.  
G9 — comparison direction vs SecantDerivative reproduced in >=4/5 formal seeds.  
G10 — OracleRHS is no worse than 1.25x IntegralFlow hidden-Q mean after budget matching. This is a fairness sanity check, not a requirement that Oracle must win.

Decision:
- PASS_M3_FIX1: G0/G1 mandatory and >=7 of G2–G10.
- CONDITIONAL_M3_FIX1: integrity/fairness pass but objective comparison remains mixed.
- FAIL_M3_FIX1: matched-budget trajectory identification becomes unstable or loses the M3 structural result.

## Advancement

PASS_M3_FIX1 permits the trajectory-only identification result to be used as a paper-level method comparison.

The next research stage then targets sparse/noisy observations and the extreme high-frequency regime, without changing the frozen IPM core.
