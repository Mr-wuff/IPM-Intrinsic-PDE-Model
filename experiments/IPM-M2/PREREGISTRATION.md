# IPM-M2 Formal Preregistration

## Experiment
**IPM-M2 — Cartan-Lifted Evolutionary Field Qualification**

## Frozen architecture

For each controlled PDE family, train a minimal pointwise characteristic law

[
Q_	heta(j^k u,lambda)approx u_t.
]

No family token is used. A separate law is trained for each PDE family in this mechanism experiment.

The IPM core is the mathematical lift:

[
D_x=sum_{r=0}^{K-1}rac{r+1}{ell}a_{r+1}rac{partial}{partial a_r},
]

for Taylor coordinates

[
a_r=rac{ell^r}{r!}partial_x^r u.
]

The characteristic induces the evolutionary vector field

[
V_Q=sum_r rac{ell^r}{r!}D_x^rQ,rac{partial}{partial a_r}.
]

The intrinsic temporal curvature is

[
u_{tt}=V_Q(Q).
]

The native second-order IPM flow is

[
u(t+Delta t)approx u+Delta t Q+rac{Delta t^2}{2}V_Q(Q).
]

## No-component rule

The defining architecture contains no:
- convolution;
- attention;
- Fourier neural operator;
- symbolic PDE term library;
- PINN residual;
- Sobolev loss;
- spectrum loss;
- rollout fine-tuning;
- family embedding.

A small MLP is used only as the universal approximator for the unknown scalar constitutive law (Q_	heta). It is not treated as the IPM innovation.

## PDE families and physical order
- Advection: k=1
- Heat: k=2
- Burgers: k=2
- Allen-Cahn: k=2
- KdV: k=3

For the second temporal derivative, the support jet uses order K=2k.

## Training
Train (Q_	heta) only from instantaneous (u_t) targets.

## Rollout methods using the exact same trained Q
1. Euler
2. external Heun
3. intrinsic Cartan-T2

No method gets separately trained weights.

## Formal seeds
11, 29, 47, 71, 97.

## Gates
G0 — frozen protocol and frozen Cartan-core source hashes pass.  
G1 — analytic Cartan derivative identity max relative error < 1e-7 in float64.  
G2 — learned-law Cartan (D_xQ) vs spectral (D_xQ) relative error < 2e-3 on smooth audit states.  
G3 — intrinsic (V_Q(Q)) temporal curvature vs small-h finite-difference learned-law curvature relative error < 5e-2 on average.  
G4 — all law models and all rollout methods remain finite on base tests.  
G5 — at 2x and 4x training dt, Cartan-T2 beats Euler mean field error on at least 4/5 PDE families.  
G6 — Cartan-T2 mean field error across all dt tests <=1.15x external Heun.  
G7 — Cartan-T2 worst grid-transfer degradation <=1.25x external Heun.  
G8 — learned physical-law Jacobian cosine similarity to analytic PDE Jacobian >=0.80 on at least 4/5 PDE families.  
G9 — in at least 4/5 formal seeds, Cartan-T2 large-dt mean field error <=1.15x Heun and < Euler.

Decision:
- PASS_M2: G0–G4 mandatory and at least 4/5 of G5–G9.
- CONDITIONAL_M2: structural gates pass, but empirical time-flow or law-attribution evidence is incomplete.
- FAIL_M2: Cartan construction itself is numerically invalid or unstable.

## Advancement

PASS_M2 freezes the first-principles IPM mathematical core for subsequent A0 paper benchmark development.
