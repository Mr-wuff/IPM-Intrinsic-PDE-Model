# IPM-A2-Q1 — Holonomic Prolonged Integral Flow Qualification

## Motivation

A2-Q0 passed the public PDEBench engineering qualification but exposed a real scientific failure:

- Advection beta=1:
  - official NeuralOperator FNO rollout Rel-L2 = 0.06495
  - IPMAdaptive = 0.11239
- Burgers nu=0.01:
  - official FNO = 0.12561
  - IPMAdaptive = 0.93001

The Burgers failure is already present in the trajectory integral training objective:
- FNO final pilot loss = 3.89e-4
- IPMAdaptive final pilot loss = 3.12e-1

A2-FULL is therefore blocked.

Q1 does **not** add a new neural-network component. It tests a stronger consequence of the jet-state hypothesis.

## First-principles mechanism

For a holonomic field,
[
u_t=Q_	heta(j^k u)
]
implies for every derivative order (r):
[
partial_t D_x^r u = D_x^r Q_	heta(j^k u).
]

Therefore over a time interval:
[
D_x^r[u(t+2h)-u(t)]
=
int_t^{t+2h} D_x^rQ_	heta(j^k u(s)),ds.
]

Using the same Simpson quadrature as Q0:
[
R_r=
D_x^r(u_2-u_0)
-rac{h}{3}
left[
D_x^rQ_0+4D_x^rQ_1+D_x^rQ_2
ight].
]

The training objective is:
[
mathcal L_R=
sum_{r=0}^{R}
rac{|R_r|_2^2}
{|D_x^r(u_2-u_0)|_2^2+epsilon}.
]

This is **holonomic prolonged integral flow matching**.

It adds no learned module and no known PDE formula. It only requires one learned characteristic (Q_	heta) to generate a mutually consistent evolution for the observed jet.

## Models

All models use exactly the same 9,889-parameter IPMAdaptive architecture.

- P0: order-0 integral law only (Q0 objective)
- P1: prolonged orders r={0,1}
- P2: prolonged orders r={0,1,2}

Same initialization seed within each replicate, same batches, same optimizer, same 1,200 updates.

Three formal qualification seeds:
- 101
- 202
- 303

This separates:
- more optimization time (P0-1200)
from
- actual prolonged-jet supervision (P1/P2).

## Public data

Same official PDEBench files and MD5s as Q0:
- Advection beta=1.0
- Burgers nu=0.01

Same spatial stride 4 and official first-10%-test split.

## Frozen Q0 diagnostic

Before retraining, load Q0 checkpoints and measure:
1. held-out order-0/1/2 integral residual;
2. central-secant generator proxy error;
3. RK4 substep sensitivity for substeps {1,2,4,8};
4. raw/adaptive jet-order RMS vs resolution.

This diagnoses whether Q0 failure comes primarily from:
- generator identification,
- numerical integration,
- or jet-conditioning/resolution effects.

## Evaluation

For P0/P1/P2:
- held-out integral residual r=0,1,2;
- 40-step rollout Rel-L2;
- rollout curve vs horizon;
- 1% observation-noise stress;
- N/2 and N/4 resolution transfer;
- central-secant generator proxy error;
- parameter count;
- training time;
- inference latency.

Official NeuralOperator FNO Q0 result is retained only as an external reference and is not retrained in Q1.

## Gates

Q1-0 Q0 result ZIP SHA matches
`6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`.

Q1-1 official public dataset MD5s match.

Q1-2 P0/P1/P2 have identical trainable parameter counts.

Q1-3 all three seeds complete finite training/rollout.

Q1-4 at least one prolonged model P1/P2 reduces mean Burgers held-out order-0 integral residual by >=30% relative to matched P0-1200.

Q1-5 the same selected prolonged model reduces mean Burgers 40-step rollout error by >=30% relative to P0-1200.

Q1-6 Advection rollout regresses by no more than 20% relative to P0-1200.

Q1-7 noise degradation ratio <=1.05 on both PDEs.

Q1-8 resolution degradation:
- N/2 <=1.20x native on both PDEs
- N/4 <=1.50x native on both PDEs.

Q1-9 inference latency <=1.15x P0 because the architecture is unchanged.

Decision:
- A2_Q1_PASS: Q1-0..Q1-5 mandatory and at least 3 of Q1-6..Q1-9.
- A2_Q1_CONDITIONAL: structural mechanism improves residual but rollout criterion is incomplete.
- A2_Q1_FAIL: no reproducible prolonged-flow benefit.

A2-FULL remains blocked unless A2_Q1_PASS.
