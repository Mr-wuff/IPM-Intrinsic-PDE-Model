# IPM-M2-FIX1 — Overcomplete Jet Law Discovery and Solver-Agnostic Cartan Qualification

## Motivation

M2 validated the Cartan spatial lift and PDE-law Jacobian attribution, but failed when the evolutionary vector field was forcibly truncated into an explicit second-order Taylor time integrator (Cartan-T2), especially for KdV and high-resolution stiff regimes.

The revised IPM definition is:

[
oxed{	ext{IPM core} = Q_	heta + 	ext{holonomic jet geometry} + 	ext{Cartan prolongation} + V_Q}
]

The numerical time integrator is a replaceable approximation to the continuous flow and is not part of the architecture claim.

## New first-principles question

Can a learned local characteristic infer the PDE's intrinsic differential dependence from an **overcomplete jet** without being told the physical PDE order?

Every PDE is presented with:

[
J^3u=(u,u_x,u_{xx},u_{xxx}).
]

The network is not told whether the true law is first-, second-, or third-order.

## Architecture

Each PDE family trains a separate minimal smooth local law

[
Q_	heta:J^3E	imesLambda	o mathbb R.
]

A support jet through order 6 is reconstructed only when the Cartan operator requires higher coordinates.

No:
- convolution;
- attention;
- FNO/neural operator layer;
- PDE-family token;
- PDE residual loss;
- symbolic term library;
- Sobolev/spectrum loss;
- rollout fine-tuning;
- learned integrator.

## Structural tests

### 1. Cartan spatial identity
For the learned law:

[
D_xQ_	heta
=
sum_{r=0}^{5}
rac{r+1}{ell}a_{r+1}
rac{partial Q_	heta}{partial a_r}
]

is compared against direct spectral differentiation of the learned scalar field.

### 2. Learned-flow temporal identity
The intrinsic temporal derivative

[
V_Q(Q)
]

is compared with:

[
rac{Q_	heta(j^3(u+hQ_	heta))-Q_	heta(j^3u)}{h},
]

which follows the **learned flow**, not the reference PDE flow.

### 3. Differential-order discovery
The model receives all orders 0–3. We evaluate:

[
rac{partial Q_	heta}{partial u_r}
]

against the analytic PDE Jacobian padded to the overcomplete jet.

Metrics:
- Jacobian cosine similarity;
- relative Jacobian error;
- spurious-order sensitivity ratio on analytically unused derivative orders.

### 4. Solver-agnostic rollout
The learned Q is rolled out with one common external RK4 interface. The solver is not an IPM contribution.

The reference solver restores a resolution- and derivative-order-aware stiffness guard.

## PDE families
- Advection
- Heat
- Burgers
- Allen-Cahn
- KdV

## Formal seeds
11, 29, 47, 71, 97

## Frozen gates

G0 — protocol/core integrity PASS.  
G1 — analytic Cartan implementation relative error < 1e-7.  
G2 — learned (D_xQ) consistency mean relative error < 2e-3.  
G3 — learned-flow (V_Q(Q)) finite-difference identity mean relative error < 2e-2.  
G4 — Jacobian cosine similarity >= 0.85 on at least 4/5 PDE families.  
G5 — spurious-order sensitivity <= 0.20 on at least 4/5 PDE families.  
G6 — instantaneous Q validation relative RMSE <= 0.20 on at least 4/5 PDE families.  
G7 — common-RK4 base rollout remains finite for all PDEs/seeds and mean field Rel-L2 <= 0.10 on at least 4/5 PDE families.  
G8 — grid transfer N=64/128/256/512 remains finite for all valid reference cases; mean 64/256/512 degradation <=2.0x N=128 baseline.  
G9 — differential-order discovery direction reproduced in >=4/5 seeds.

Decision:
- PASS_M2_FIX1: G0–G3 mandatory and >=5 of G4–G9.
- CONDITIONAL_M2_FIX1: structural Cartan gates pass but law discovery/generalization is incomplete.
- FAIL_M2_FIX1: the corrected first-principles Cartan/evolutionary formulation itself fails.

## Advancement

A PASS freezes the IPM mathematical core:
1. overcomplete holonomic jet;
2. learned local characteristic;
3. Cartan prolongation;
4. evolutionary vector field;
5. solver-independent continuous flow definition.

The next stage would then move from exact RHS supervision to trajectory-only identification.
