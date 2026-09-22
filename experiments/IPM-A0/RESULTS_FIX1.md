# IPM-A0-FIX1 Evaluation Audit Results

## Decision
**EVALUATION_AUDIT_COMPLETE**

Result ZIP SHA256:
`44ef2e47c8b462e38dc07822f686fc801443a7fba1701f037722dfc24648e3c5`

Input A0 ZIP SHA256:
`33be4009b7f329af5e4799feb56f9ce46e93a45c8792d7bda7d185d736f6270b`

All E0–E5 audit checks passed:
- input checksum matched;
- all 175 A0 checkpoints were present;
- frozen A0 protocol/source identity matched;
- reevaluated outputs were finite;
- checkpoints were read-only;
- raw paired results were exported.

The executed FIX1 notebook contains 9 code cells and all 9 are byte-for-byte identical to the released notebook.

## Corrected physical-band spectral metric

A0-FIX1 evaluates fixed physical Fourier bands:
- low: |k| <= 4
- mid: 4 < |k| <= 8
- high: |k| > 8

Mean base-rollout metrics:

| Method | Field Rel-L2 | Low-band Rel | Mid-band Rel | High-band Rel |
|---|---:|---:|---:|---:|
| ResNet1D_RHS | 0.000676 | 0.000443 | 0.002668 | 15.871 |
| UNet1D_RHS | 0.000862 | 0.000534 | 0.003438 | 21.602 |
| IPMRaw | 0.001148 | 0.000838 | 0.004442 | 12.552 |
| IPMAdaptive | 0.001174 | 0.000855 | 0.004632 | 12.385 |
| FNO1D_RHS | 0.001506 | 0.001077 | 0.005233 | 13.274 |
| ConvDeepONet1D_RHS | 0.015354 | 0.010530 | 0.069616 | 1.414 |
| FieldMLP | 0.016839 | 0.013154 | 0.065047 | 6.804 |

### Interpretation caveat

The corrected high-band metric is mathematically valid, but for PDE/case combinations with extremely little true energy above |k|>8, the denominator becomes very small and the relative number can become very large.

This is visible in advection and heat. Therefore the paper should report:
1. high-band relative error;
2. high-band predicted/reference energy ratio;
3. per-PDE results rather than only one aggregate high-band mean.

For Burgers/KdV, where high-band energy is materially present, IPM is competitive:
- Burgers high-band: ResNet 0.0727, IPMRaw 0.0850, IPMAdaptive 0.0896, U-Net 0.1168, FNO 0.2139.
- KdV high-band: ResNet 0.1077, IPMRaw 0.1709, IPMAdaptive 0.1735, U-Net 0.1958, FNO 0.2348.

## Paired base-rollout result

Across 25 PDE×seed pairs:
- IPMRaw − FNO field error: **−3.58e−4**, 95% CI **[−6.72e−4, −4.29e−5]**.
- IPMAdaptive − FNO field error: **−3.32e−4**, 95% CI **[−6.50e−4, −1.40e−5]**.
- IPMRaw remains worse than ResNet and U-Net on field error.

For high-band relative error:
- IPMRaw vs U-Net: mean difference **−9.05**, 95% CI **[−17.47, −0.64]**.
- IPMAdaptive vs U-Net: mean difference **−9.22**, 95% CI **[−17.86, −0.57]**.
- IPM vs FNO high-band differences are not statistically resolved because of large per-PDE variance.

## Temporal-law stride audit

Training observation strides:
[
sin{1,2,4}
]

Held-out:
[
sin{3,5,8}
]

Mean normalized integral residuals are nearly invariant across stride for every method.

Seen vs held-out mean residual:

| Method | Seen 1/2/4 | Held-out 3/5/8 | Held/Seen |
|---|---:|---:|---:|
| ResNet1D_RHS | 0.04584 | 0.04581 | 0.9992 |
| UNet1D_RHS | 0.05680 | 0.05668 | 0.9980 |
| FNO1D_RHS | 0.09977 | 0.09960 | 0.9983 |
| IPMRaw | 0.10288 | 0.10264 | 0.9977 |
| IPMAdaptive | 0.10515 | 0.10496 | 0.9982 |
| FieldMLP | 0.80089 | 0.80089 | 1.0000 |
| ConvDeepONet1D_RHS | 0.82342 | 0.82341 | 1.0000 |

This confirms that the learned RHS laws do not break when evaluated at unseen trajectory observation spacings up to stride 8.

However, this audit does **not** show an IPM-specific temporal-generalization advantage:
- ResNet and U-Net have lower absolute integral residual.
- IPMRaw and FNO are statistically close on held-out strides (paired 95% CI crosses zero).

The original A0 external-dt experiment should therefore be described only as solver-step invariance, while A0-FIX1 supplies the valid unseen-observation-spacing result.

## Final A0/A0-FIX1 interpretation

The controlled benchmark evidence now supports:
1. ResNet/U-Net are strongest at the training discretization and on absolute local-law accuracy.
2. IPMRaw/Adaptive are competitive with controlled FNO and achieve lower rollout error in the matched controlled setting.
3. IPMAdaptive and FNO are the accurate models with near-perfect N=64–512 resolution transfer.
4. IPM provides explicit differential-law attribution and Cartan consistency absent from ordinary field baselines.
5. IPM has a favorable parameter/training/latency Pareto relative to the controlled FNO/ResNet/U-Net implementations.
6. There is no evidence that IPM uniquely improves held-out temporal-stride consistency; all competent continuous-RHS models remain stable across the tested strides.
7. High-frequency evaluation must be reported per PDE with energy context.

The controlled-suite stage is closed. Next stage: official equation-discovery baselines and official public benchmark implementations.
