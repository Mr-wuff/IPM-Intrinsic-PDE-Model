# IPM-A2-Q3-FIX1 — Canonical Differential-Algebra Compiler

## Motivation

Q3 preserved a 2.19-5.27x end-to-end speed advantage but failed physical reliability.

The failure is now attributable to the compiler rather than to the frozen 35-parameter IDTC itself.

Q3 made two structural mistakes:

1. it selected polynomial degree as one indivisible block, causing Burgers to fall back to D1 and delete the learned quadratic transport term (u u_x);
2. it compiled only first/second derivative principal pieces, leaving small higher-derivative terms such as Advection (u_{xxx}) in an explicit source, which becomes stiff at full resolution.

FIX1 keeps the Q2 IDTC checkpoints frozen and compiles the **canonical monomials** of the full learned algebra.

No neural model is retrained and no true PDE equation is supplied.

## Exact canonical expansion

The frozen IDTC is expanded exactly as
[
Q(a)=b+sum_i l_i a_i+sum_{ij}A_{ij}a_ia_j+sum_{ijk}B_{ijk}a_ia_ja_k,
]
with
[
a_0=u,quad a_1=u_x,quad a_2=u_{xx}/2,quad a_3=u_{xxx}/6.
]

The expansion is converted to canonical monomial exponent tuples
[
(e_0,e_1,e_2,e_3).
]

An equivalence gate requires the canonical polynomial to reconstruct the frozen IDTC output to relative max defect <=1e-6 on calibration states.

## Differential-role classification

The compiler classifies a monomial by algebraic structure, not by PDE identity.

### Reaction/source
Only powers of (a_0=u):
[
R(u).
]

### Principal derivative family
Exactly one derivative coordinate appears to first power:
[
f_r(u)a_r,quad rin{1,2,3}.
]

This automatically includes:
- constant transport (c,u_x);
- nonlinear transport (f(u)u_x), including Burgers-like (u u_x);
- state-dependent diffusion (g(u)u_{xx});
- dispersive terms (h(u)u_{xxx}).

### Nuisance/cross-derivative family
Terms with:
- powers (a_r^p, p>=2) for derivative coordinates;
- products of multiple derivative coordinates.

These are not assumed invalid. Their measured contribution determines whether they are retained.

## Calibration-only contribution pruning

Use the same disjoint PDEBench training-pool calibration trajectories as Q3.

For each canonical monomial compute
[
ho_m = rac{mathrm{RMS}(Q_m)}{mathrm{RMS}(Q)}.
]

Candidate contribution thresholds:
[
0, 10^{-4}, 3	imes10^{-4}, 10^{-3}, 3	imes10^{-3}, 10^{-2}, 3	imes10^{-2}.
]

A threshold removes terms with (ho_m) below threshold.

No coefficient is refit.

For each seed/task, select the threshold by 20-step calibration rollout over starts 10/60/120.
Reject non-finite candidates.
If candidates are within 5%, choose the larger threshold (simpler compiled law).

The official first-10% PDEBench test split is never used for selection.

## Native compiled flow

For the selected canonical program:

### Transport
[
f_1(u)a_1=f_1(u)u_x
]
is advanced with periodic semi-Lagrangian transport using
[
v=-f_1(u).
]

### Diffusion
[
f_2(u)a_2=rac{f_2(u)}{2}u_{xx}.
]
Use the robust sample-level median
[

u = mathrm{median}_x(f_2(u)/2),
]
clamped nonnegative for the present Advection/Burgers qualification scope.

### Dispersion
[
f_3(u)a_3=rac{f_3(u)}{6}u_{xxx}.
]
Use the robust sample-level median
[
gamma=mathrm{median}_x(f_3(u)/6).
]

Diffusion and dispersion are combined into one exact periodic spectral linear step:
[
hat u_kleftarrow
exp[(-
u k^2+gamma(ik)^3)Delta t]hat u_k.
]

### Reaction/source
(R(u)) is advanced by a local Heun step.

### Retained nuisance terms
If calibration keeps nuisance terms, evaluate them from the local Taylor jet and apply a bounded/tamed explicit correction. Their contribution and latency are reported separately.

## Why this is still PDE-native rather than a hand-written Burgers solver

The compiler never receives:
- the PDE name;
- the true terms;
- the true coefficients.

It operates only on the frozen IDTC polynomial and generic differential-role rules that apply to any 1D local polynomial characteristic of the supported jet order.

## Formal data

Same official PDEBench files:
- Advection beta=1.0
- Burgers nu=0.01

Frozen Q2 IDTC seeds:
101, 202, 303.

No retraining.

## Evaluation

- canonical reconstruction defect
- selected contribution threshold
- number of retained terms by role
- learned transport/diffusion/dispersion diagnostics
- 1/5/10/20/40-step rollout
- 1% noise
- resolution /2 and /4
- full physical-step latency
- grid-points/s
- speedup vs official frozen NeuralOperator FNO
- comparison with Q3 compiler and Q2 generic Euler/RK4 references

## Gates

F0 Q2 parent SHA and official dataset MD5 match.

F1 exact canonical reconstruction <=1e-6.

F2 calibration-only selection is disjoint from Q2 fit and official test data.

F3 all 3 seeds remain finite through 40 test steps on both PDEs.

F4 mean 40-step Rel-L2:
- Advection <=0.12
- Burgers <=0.35.

F5 end-to-end physical-step latency <=0.50x official FNO on both PDEs.

F6 1% noise degradation <=1.15x native.

F7 resolution /2 <=1.20x and /4 <=1.50x native.

F8 selected threshold reproducible in at least 2/3 seeds per PDE.

Decision:
- A2_Q3_FIX1_PASS: F0-F5 mandatory + at least 2 of F6-F8.
- A2_Q3_FIX1_CONDITIONAL: finite+speed pass and one accuracy threshold misses by <=25%.
- A2_Q3_FIX1_FAIL otherwise.

Full broad paper benchmark remains blocked until a stable compact IPM deployment point is frozen.
