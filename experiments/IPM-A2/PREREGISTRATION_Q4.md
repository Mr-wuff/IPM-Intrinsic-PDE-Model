# IPM-A2-Q4 — Full-Symbol Quasilinear Flow Compiler

## Motivation

A2-Q3 failed physical reliability while preserving the Q2 compactness/speed signal.

Q3 diagnosis is now specific:

- Advection D1 contains a tiny learned third-derivative term.
- Q3 handles a1 and a2 specially but places a3 into an explicit residual source.
- At N=256, L=1, dt=0.01, the learned physical u_xxx coefficient produces a Nyquist explicit-step stiffness scale of roughly 46-52.
- This explains the exact observed pattern: native N=256 blows up while N/2 and N/4 remain stable.

For Burgers, Q2 already learned the dominant nonlinear transport coefficient:
[
2A_{a_0,a_1}approx -1,
]
but Q3 D2/D3 become unstable under the incomplete compiler, so calibration chooses D1 and discards the nonlinear transport interaction.

Q4 therefore changes the **compiler**, not the learned 35-parameter IDTC.

No neural model is retrained.

## Quasilinear normal form from the learned characteristic

For a frozen degree-d IDTC law
[
Q(a_0,a_1,a_2,a_3),
]
define the derivative-zero anchor
[
a^circ=(a_0,0,0,0).
]

The compiler extracts

[
S(u)=Q(a^circ)
]

and

[
c_r(u)=
left.
rac{partial Q}{partial a_r}
ight|_{a^circ},
qquad r=1,2,3.
]

The compiled local normal form is

[
Q_{mathrm{QL}}=
S(u)+c_1(u)a_1+c_2(u)a_2+c_3(u)a_3.
]

This retains quasilinear interactions such as
[
u,u_x
]
because they appear through the u-dependence of (c_1(u)).

Derivative-nonlinear terms such as (u_x^2), (u_xu_{xx}), etc. are excluded from the runtime normal form. Their omitted energy is measured explicitly against the full frozen IDTC law.

No true PDE equation, symbolic term list or PDE coefficient is provided to the compiler.

## Stable full-symbol flow

Taylor coordinates:
[
a_1=u_x,quad
a_2=u_{xx}/2,quad
a_3=u_{xxx}/6.
]

Define physical coefficients:
[
v(u)=-c_1(u),
quad

u(u)=c_2(u)/2,
quad
gamma(u)=c_3(u)/6.
]

### Constant-transport branch

If the spatial coefficient of variation of v is below 2%, compile transport + diffusion + dispersion into a single exact Fourier multiplier:

[
hat u_{n+1}
=
expleft[
Delta t
left(
-c,ik
+
u(ik)^2
+gamma(ik)^3
ight)
ight]hat u_n.
]

Robust sample medians are used for c, nu and gamma.

### Variable-transport branch

Otherwise:
1. semi-Lagrangian periodic transport using local v(u);
2. exact spectral exponential for robust sample-level nonnegative nu and real gamma.

Thus the high-order odd derivative is never placed into an explicit Euler source.

### Source

The anchor source S(u) is integrated with a local Heun step when enabled.

Source on/off is a calibration candidate, not fixed from PDE knowledge.

## Algebraic complexity selection

For each frozen Q2 checkpoint, candidates are:
- degree D1/D2/D3
- source OFF/ON

Selection uses only the disjoint PDEBench training-pool calibration trajectories introduced in Q3.

The official test split is untouched.

Candidate score:
- mean 20-step calibration rollout Rel-L2 over starts {10,60,120}
- non-finite candidates rejected
- within 5% of best score, prefer lower algebraic degree
- within the same degree and 5%, prefer source OFF

## Formal evaluation

Three frozen Q2 seeds:
101, 202, 303.

Tasks:
- PDEBench Advection beta=1.0
- PDEBench Burgers nu=0.01

Report:
- selected degree/source mode
- full-IDTC to quasilinear-normal-form defect
- coefficient variation statistics
- 1/5/10/20/40-step test rollout
- 1% observation-noise stress
- resolution /2 and /4
- end-to-end physical-step latency
- grid-points/s
- speedup vs official frozen NeuralOperator FNO
- runtime branch statistics (constant vs variable transport)

## Gates

Q4-0 Q2/Q3 result SHA and official dataset MD5 match.

Q4-1 normal-form compiler analytic equivalence for extracted anchor/Jacobian:
relative defect <=1e-6.

Q4-2 all selected flows remain finite for 40 official-test steps in all 3 seeds.

Q4-3 mean 40-step rollout:
- Advection <=0.12
- Burgers <=0.40.

Q4-4 end-to-end physical-step latency <=0.50x official FNO on both tasks.

Q4-5 1% noise degradation <=1.15x native.

Q4-6 resolution /2 <=1.20x native and /4 <=1.50x native.

Q4-7 selected algebraic degree is reproducible in at least 2/3 seeds per PDE.

Q4-8 quasilinear normal-form defect <=0.20 on calibration data for the selected model.

Decision:
- A2_Q4_PASS: Q4-0..Q4-4 mandatory and at least 3 of Q4-5..Q4-8.
- A2_Q4_CONDITIONAL: finite+speed pass and one accuracy threshold misses by <=25%.
- A2_Q4_FAIL otherwise.

## Benchmark transition

If Q4 passes, A2 qualification ends and the project enters the comprehensive paper benchmark.

The benchmark will not be restricted to FNO. It will include:
- classical PDE numerical solvers;
- conventional neural baselines;
- the major neural-operator families with reproducible implementations;
- the major PINN families through PINNacle/DeepXDE/PhysicsNeMo-compatible protocols;
- physics-informed neural operators;
- operator transformers and PDE foundation models where the task contract is valid;
- PDE discovery baselines in the law-identification regime.

Comparisons will be separated by information contract so equation-known numerical/PINN solvers are not naively ranked together with trajectory-only learned surrogates.
