# IPM-A2-Q3 — Intrinsic Principal-Flow Compiler

## Motivation

A2-Q2 failed long-horizon stability but produced three important results:

1. IDTC has only 35 trainable parameters (0.0693% of official FNO).
2. End-to-end Euler physical-step latency is ~10.0x faster than FNO on Advection and ~3.06x faster on Burgers.
3. The learned algebra has physically meaningful dominant structure:
   - Advection: dominant first-derivative coefficient ~ -0.903.
   - Burgers: quadratic u*u_x coefficient ~ -1.002 across seeds.

One-step IDTC errors are already small (~1-3%), but repeated explicit Euler/Heun/RK4 flow becomes non-finite by horizon 5-10.

Therefore Q3 tests whether the learned differential law can generate its **own stable numerical flow**, instead of being inserted into a generic explicit ODE integrator.

No neural architecture is enlarged and no new trainable module is added.

## Principle

For a local characteristic
[
u_t=Q(a_0,a_1,a_2,a_3),
]
with Taylor-jet coordinates
[
a_0=u,quad a_1=u_x,quad a_2=u_{xx}/2,quad a_3=u_{xxx}/6,
]
define local principal coefficients
[
c_1=rac{partial Q}{partial a_1},qquad
c_2=rac{partial Q}{partial a_2}.
]

The transport speed is
[
v=-c_1.
]

The physical diffusion coefficient associated with the Taylor coordinate is
[

u=c_2/2.
]

Define the residual source
[
S=Q-c_1a_1-c_2a_2.
]

The macro flow is:
1. semi-Lagrangian periodic transport using v;
2. local Gaussian diffusion using nonnegative sample-level robust nu;
3. explicit residual-source correction.

This is an **Intrinsic Principal-Flow Compiler (IPFC)**: the model's differential Jacobian determines how its learned PDE law is numerically advanced.

## Algebra-degree selection

Q2 full cubic IDTC can contain small high-degree contaminating terms.

For every frozen Q2 checkpoint construct:
- D1: linear+bias only
- D2: linear+quadratic
- D3: full cubic

No coefficients are refit.

Degree is selected only on an independent calibration subset from the PDEBench training pool that was not used in Q2 fitting:
- Q2 fit trajectories: training-pool samples 0..127
- Q3 calibration trajectories: training-pool samples 128..159

Selection:
1. evaluate 10-step IPFC calibration rollout for D1/D2/D3;
2. discard non-finite degree;
3. choose the lowest calibration error;
4. if two degrees are within 5%, choose the lower degree.

The official first-10% test split is never used for degree selection.

## Formal methods

Per seed/task:
- Q2-IDTC full + Euler (archived instability reference)
- Q2-IDTC full + RK4 (archived instability reference)
- Q3-IPFC selected degree (proposed)

External reference:
- frozen official NeuralOperator FNO accuracy/latency from Q0/Q2.

## Public data

Same official PDEBench files:
- Advection beta=1.0
- Burgers nu=0.01

Same spatial stride 4.

Formal seeds:
101, 202, 303.

## Evaluation

- algebra-degree chosen per seed/task
- 1/5/10/20/40-step rollout Rel-L2
- finite-horizon rate
- 1% observation-noise stress
- resolution /2 and /4
- end-to-end physical-step latency
- grid-points/s
- learned transport-speed statistics
- learned diffusion statistics
- residual-source RMS fraction
- comparison with official FNO native step

## Gates

Q3-0 Q2 result SHA and official dataset MD5 match.

Q3-1 degree selection uses calibration pool only.

Q3-2 all selected Q3 flows remain finite for 40 test steps in 3/3 seeds.

Q3-3 mean 40-step rollout:
- Advection <= 0.12
- Burgers <= 0.40.

Q3-4 end-to-end step latency:
- <= 0.50x official FNO on both tasks.

Q3-5 1% noise degradation <= 1.15x native.

Q3-6 resolution /2 <= 1.20x native and /4 <= 1.50x native.

Q3-7 selected degree is reproducible in at least 2/3 seeds per PDE.

Decision:
- A2_Q3_PASS: Q3-0..Q3-4 mandatory + at least 2 of Q3-5..Q3-7.
- A2_Q3_CONDITIONAL: finite + speed pass, but one accuracy threshold misses by <=25%.
- A2_Q3_FAIL: principal-flow compilation does not rescue the compact core.

## Scope

Q3 is limited to first/second-order principal-flow structure because the public qualification tasks are Advection and viscous Burgers.

Dispersion (KdV), reaction/source dynamics and multi-D mixed derivatives remain separate later qualification stages.

No claim of universal PDE coverage is permitted from Q3.
