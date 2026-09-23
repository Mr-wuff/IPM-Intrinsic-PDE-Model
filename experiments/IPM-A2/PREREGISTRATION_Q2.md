# IPM-A2-Q2 — Native Differential Core / Speed-First Qualification

## Why Q2 exists

A2-Q1 failed its preregistered advancement gate.

Q1 nevertheless established two useful facts:

1. equal-weight jet prolongation can improve long-horizon nonlinear Burgers rollout (P2 improves mean 40-step error by 35.3%), but does not improve the instantaneous order-0 characteristic and damages Advection;
2. current IPM speed evidence is incomplete because prior latency tables time only one characteristic evaluation, while the deployed IPM uses four such evaluations per RK4 physical step.

The central IPM objective is therefore sharpened:

> make the PDE law an intrinsic computational object whose state representation and evolution are both physically interpretable and substantially cheaper than a global neural operator.

Q2 targets **end-to-end simulation speed** and a more PDE-native computation core. It does not add attention, convolutions, transformers, operator blocks, or a larger MLP.

## First-principles architecture hypothesis

### 1. Local Taylor Jet Lift

A k-jet is the local Taylor germ of a field.

Instead of constructing derivatives by a global FFT, Q2 computes the jet from a local least-squares Taylor projection on a periodic stencil:

[
u(x_i+sDelta x)
approx
sum_{r=0}^{p} c_r s^r,
qquad
D_x^r u(x_i)
=
rac{r!}{Delta x^r}c_r.
]

The projection matrix is fixed, not learned.

Formal configuration:
- polynomial degree = 5
- radius = 4
- stencil width = 9
- jet order = 3

This makes the lift local, parallel, grid-scaled and directly tied to the mathematical definition of a jet.

### 2. Intrinsic Differential Tensor Core (IDTC)

The current IPM characteristic is a generic tanh MLP.

Q2 tests a low-rank differential algebra directly over the normalized jet:

[
z = J^3u / s.
]

The characteristic is

[
Q_	heta(z)
=
q_s
left[
b + w^	op z
+
sum_{m=1}^{R_2}alpha_m(v_m^	op z)^2
+
sum_{n=1}^{R_3}eta_n(r_n^	op z)^3
ight].
]

Formal ranks:
- quadratic rank (R_2=4)
- cubic rank (R_3=2)

The model does not receive the true PDE formula or a hand-selected list of Burgers/Advection terms.

This is a low-rank differential tensor algebra, not an enumerated SINDy term library.

It can be expanded after training into explicit linear/quadratic/cubic coefficients for audit.

### 3. Native time stepping

The same trained characteristic is evaluated with:
- Euler: 1 characteristic/lift evaluation
- Heun: 2 evaluations
- RK4: 4 evaluations

The main speed metric is **end-to-end physical-step latency**, not characteristic-forward latency.

## Attribution ladder

All formal models use the same public PDEBench subset and trajectory-only order-0 integral objective.

1. Q1-P0 Spectral-MLP — frozen parent checkpoint, current architecture.
2. LocalJet-MLP — only jet lift changes.
3. LocalJet-IDTC — local lift + proposed differential tensor core.

This separates:
- derivative/lift cost;
- generic neural characteristic cost;
- PDE-native algebraic core.

No prolongation loss is used in Q2 because Q1 showed it is not a universal law-identification improvement.

## Public data

Same official PDEBench files:
- Advection beta=1.0
- Burgers nu=0.01

Same:
- official first-10%-test split;
- spatial stride 4;
- 128 training trajectories;
- 32 test trajectories;
- 1,200 optimizer updates;
- seeds 101, 202, 303.

## Stage J0 — Local Taylor lift qualification

Analytic Fourier-mode audit:
- N = 64, 128, 256
- modes k = 1, 3, 5, 7
- derivative orders 0,1,2,3
- clean and 1% noise

Also benchmark lift-only latency at batch=16, N=256:
- AdaptiveSpectralJet
- LocalTaylorJet

J0 is recorded before any Q2 model training.

## Evaluation

### Accuracy / physical reliability
- held-out order-0 integral residual
- central-secant characteristic proxy error
- 40-step rollout Rel-L2
- horizon curves 1/5/10/20/40
- 1% noise
- resolution /2 and /4

### Algebra audit
Expand IDTC into monomial coefficients and report:
- linear coefficient vector
- symmetric quadratic coefficient matrix
- cubic tensor norm
- effective-rank amplitudes
- fraction of coefficient energy associated with physically expected derivative coordinates (diagnostic only; no true terms used in training)

### Cost
- trainable parameters
- checkpoint bytes
- training wall time
- peak training VRAM
- lift-only latency
- characteristic-only latency
- **end-to-end Euler/Heun/RK4 physical-step latency**
- grid-points/second
- speedup against official frozen Q0 NeuralOperator FNO native one-step forward

## External baselines

Reuse frozen Q0 official NeuralOperator FNO checkpoints for both tasks.

Reconstruct with the same official
`neuralop.models.FNO`
configuration and load the frozen Q0 state dict.

No FNO retraining is performed.

## Gates

Q2-0 parent Q1 ZIP SHA and public dataset MD5s match.

Q2-1 Local Taylor analytic derivative audit:
- worst clean r1 error <= 0.02
- worst clean r2 error <= 0.10
- worst clean r3 error <= 0.10
for the frozen analytic suite.

Q2-2 all formal models complete three seeds finite.

Q2-3 LocalJet-IDTC trainable parameters <= 1% of official FNO.

Q2-4 one of Euler/Heun/RK4 for LocalJet-IDTC reaches:
- Advection 40-step Rel-L2 <= 0.10
- Burgers 40-step Rel-L2 <= 0.30.

Q2-5 that same integrator has native end-to-end physical-step latency <= 0.50x official FNO one-step latency on both tasks.

Q2-6 noise degradation <= 1.10x native on both tasks.

Q2-7 resolution /2 degradation <= 1.20x and /4 <= 1.50x native.

Q2-8 LocalJet-IDTC is not slower end-to-end than LocalJet-MLP at the selected integrator.

Decision:
- A2_Q2_PASS: Q2-0..Q2-5 mandatory and at least 2 of Q2-6..Q2-8.
- A2_Q2_CONDITIONAL: speed target passes but one physical-reliability accuracy threshold misses by <=25%.
- A2_Q2_FAIL: no credible speed/accuracy advantage.

## Novelty boundary

Q2 does **not** claim that polynomial/product neural networks or Taylor time integration are individually new.

Before paper freeze, the architecture must be audited against:
- polynomial neural ODE / Pi-Net style models;
- PDE discovery models;
- neural Taylor-expansion operators;
- mechanistic PDE networks;
- classical Lax-Wendroff / Cauchy-Kowalevski / ADER ideas.

The candidate IPM contribution is the integrated object:
**holonomic local jet state + learned low-rank differential algebra characteristic + native continuous evolution + explicit cost/physical audit**.
