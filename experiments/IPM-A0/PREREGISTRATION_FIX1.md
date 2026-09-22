# IPM-A0-FIX1 — Evaluation Audit (No Retraining)

## Motivation

IPM-A0 completed successfully, but two evaluation metrics require correction before paper use.

### 1. High-frequency metric

A0 computed:

[
rac{|(hat u-hat u^*)_{HF}|}{|hat u^*|_{all}},
]

which is not a true high-frequency relative error and can make an over-smoothed model look artificially good.

A0-FIX1 replaces it with physical-band relative spectral errors:

[
E_B=
rac{|(hat u-hat u^*)_B|_2}
{|hat u^*_B|_2+epsilon}.
]

Bands are defined in absolute physical Fourier modes, not as fractions of grid Nyquist:
- low: |k| <= 4
- mid: 4 < |k| <= 8
- high: |k| > 8

Also report predicted/reference spectral-energy ratio in each band.

### 2. Temporal transfer metric

A0 changed the external RK4 macro-step while re-substepping internally to approximately the same learned micro-step. Consequently all methods produced nearly identical dt-factor curves.

This is retained as solver-step invariance but is not used as evidence of temporal-law extrapolation.

A0-FIX1 instead evaluates trajectory-integral consistency on observation strides:

Training strides:
[
sin{1,2,4}.
]

Held-out:
[
sin{3,5,8}.
]

For every learned continuous RHS:

[
R_s=
rac{
left|
u_{i+2s}-u_i-rac{sDelta t}{3}
(Q_i+4Q_{i+s}+Q_{i+2s})
ight|_2
}{
|u_{i+2s}-u_i|_2+epsilon
}.
]

This directly tests whether the learned continuous law explains unseen temporal observation spacings.

## Frozen artifacts

No model is retrained.

Input:
- `IPM_A0_RESULTS.zip`
- its frozen 175 checkpoints
- frozen A0 protocol and data-generation seeds

The notebook verifies the input ZIP SHA256 when a matching `.sha256` file is supplied.

## Methods

All seven A0 methods are reevaluated:
- IPMRaw
- IPMAdaptive
- FieldMLP
- ResNet1D_RHS
- FNO1D_RHS
- UNet1D_RHS
- ConvDeepONet1D_RHS

## Evaluation

1. base rollout using the exact A0 deterministic cases;
2. physical-band spectral relative errors;
3. physical-band predicted/reference energy ratios;
4. integral consistency at s=1,2,3,4,5,8;
5. paired five-seed/PDE bootstrap or t-interval comparisons for:
   - final field error;
   - high-band error;
   - held-out stride residual.

## Integrity

E0 — input ZIP checksum matches supplied checksum if present.  
E1 — all 175 expected checkpoints exist.  
E2 — checkpoint protocol/source identity matches A0.  
E3 — all reevaluated outputs are finite.  
E4 — no checkpoint weights are modified.  
E5 — all raw paired results are exported.

Decision is only:
- EVALUATION_AUDIT_COMPLETE
- EVALUATION_AUDIT_INCOMPLETE

There is no winner-dependent gate.
