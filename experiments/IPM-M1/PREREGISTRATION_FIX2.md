# IPM-M1-FIX2 — Pointwise Intrinsic Generator and Spectral-Stability Qualification

## Motivation

M1-FIX1 repaired the independent-jet drift problem but exposed three remaining failures:

1. Raw unnormalized jet input is catastrophically unstable.
2. HolonomicIPM strongly outperforms normalized concatenation baselines, but remains ~5.95x worse than FieldState in mean base field error.
3. Grid transfer degrades sharply as N increases, suggesting that the Conv1D generator introduces a grid-index receptive field inconsistent with the intended local PDE generator.

For a finite-order local evolution PDE,

[
u_t(x)=F(j^k u(x),lambda),
]

the learned generator should act pointwise in jet space. FIX2 therefore removes spatial convolution from the proposed IPM generator.

## Hypothesis

A pointwise, derivative-order-structured jet-space generator with exact master-field holonomic reconstruction and resolution-invariant derivative normalization will reduce high-frequency contamination and improve grid/time transfer relative to the convolutional HolonomicIPM.

## Null hypothesis

The observed FIX1 advantage was mainly due to capacity or normalization. A pointwise intrinsic generator provides no reproducible benefit over a pointwise normalized-jet MLP or the strong FieldState baseline.

## Models

1. **FieldStateConv** — strong convolutional field-only baseline.
2. **ConvHolonomicIPM** — FIX1-style convolutional IPM control.
3. **PointwiseJetMLP** — pointwise MLP over normalized jet coordinates with no derivative-order structure.
4. **PointwiseOrderIPM** — proposed pointwise order-factorized IPM.
5. **PointwiseOrderIPM-NoSobolev** — same architecture trained without generator Sobolev fidelity, isolating the effect of the training objective.

RawJetGenerator is retained only as an archived catastrophic-failure control from FIX1 and is not used as a denominator in any winner gate.

## Intrinsic state normalization

For each sample and derivative order r,

[
s_r=sqrt{langle (D_x^r u)^2angle}+epsilon,
qquad
	ilde u_r = rac{D_x^r u}{s_r}.
]

All log-scales (log s_r) are passed to the generator context.

This directly equalizes differential orders instead of approximating them with (A k_{m rms}^r).

## Generator fidelity objective

All finite formal models except the explicit NoSobolev ablation receive the same supervised generator objective:

[
L = L_0 + lambda_1 L_{D_xQ} + lambda_s L_{m spectrum},
]

where the known PDE is used only to create reference generator targets. No analytic PDE residual is inserted as a model-specific loss.

A short trajectory-consistency fine-tuning stage is applied equally to the comparable formal models.

## Numerical stabilization

The learned generator is passed through the same resolution-aware spectral de-aliasing projector for every model before Heun integration. This is treated as the common numerical integrator interface, not an IPM-specific mechanism.

## Formal PDE suite

- Heat
- Linear advection
- Viscous Burgers
- Allen–Cahn
- KdV

## Pre-training gates

- protocol SHA256 integrity;
- multi-function float64 spectral derivative audit;
- per-order normalization condition-number audit;
- circular-shift equivariance of pointwise IPM;
- same-analytic-state 128/256 resolution consistency at shared points;
- tiny-set overfit sanity check;
- finite 20-step smoke rollout on all five PDEs.

Formal training is blocked if any structural gate fails.

## Evaluation

- field Rel-L2;
- jet Rel-L2;
- gradient Rel-L2;
- generator Rel-L2;
- high-frequency spectral error;
- dt transfer;
- grid transfer (64/128/256/512);
- parameter OOD;
- IC OOD;
- noise robustness;
- data efficiency;
- latency / memory;
- 5 formal seeds.

## Frozen M1-FIX2 gates

G0 protocol integrity PASS.  
G1 derivative audit PASS.  
G2 normalization ratio max/min <= 2.5 on audit distribution.  
G3 pointwise translation equivariance defect <= 1e-5.  
G4 base rollout stable for all PDEs × 5 seeds.  
G5 PointwiseOrderIPM beats PointwiseJetMLP in mean field error by >=15% OR mean jet error by >=25% with <=5% field regression.  
G6 PointwiseOrderIPM base mean field error <=1.50x FieldStateConv and is <=1.25x FieldStateConv on at least 3/5 PDE families.  
G7 mean jet error <=3.0x FieldStateConv.  
G8 worst dt-transfer degradation <=1.35x FieldStateConv.  
G9 worst grid-transfer degradation <=1.50x FieldStateConv.  
G10 parameter-OOD field error <=1.35x FieldStateConv.  
G11 PointwiseOrderIPM beats PointwiseJetMLP in at least 4/5 seeds.  
G12 inference latency <=4x FieldStateConv.

Decision:
- PASS_M1_FIX2: G0–G5 and G11 mandatory, plus at least 5 of G6–G10/G12.
- CONDITIONAL_M1_FIX2: structural/stability gates pass but paper-level competitiveness/generalization remains incomplete.
- FAIL_M1_FIX2: structural stability fails or pointwise intrinsic mechanism has no reproducible benefit.

## Advancement rule

IPM-A0 remains blocked unless FIX2 is PASS. A conditional result triggers another M-stage repair, not scaling.
