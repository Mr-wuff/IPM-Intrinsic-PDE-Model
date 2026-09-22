# IPM-A0 Controlled Paper Benchmark — Results

## Integrity
**BENCHMARK_COMPLETE_A0**

Result ZIP SHA256:
`33be4009b7f329af5e4799feb56f9ce46e93a45c8792d7bda7d185d736f6270b`

All B0–B7 benchmark-integrity checks passed:
- frozen protocol/source hashes match;
- all methods received exactly 1152 optimizer updates per run;
- all formal results are finite;
- shared deterministic test cases were used;
- efficiency metadata were recorded;
- dt comparisons preserve physical horizon;
- all five seeds were exported;
- raw per-run tables are present.

The executed notebook has 11 code cells and they are byte-for-byte identical to the released notebook code cells.

## Controlled methods
- IPMRaw
- IPMAdaptive
- FieldMLP
- ResNet1D_RHS
- FNO1D_RHS
- UNet1D_RHS
- ConvDeepONet1D_RHS

These are controlled implementations, not official external-repository reproductions.

## ID hidden exact-Q Rel-RMSE

| Method | Mean |
|---|---:|
| ResNet1D_RHS | 0.04837 |
| UNet1D_RHS | 0.06771 |
| IPMRaw | 0.09102 |
| IPMAdaptive | 0.10126 |
| FNO1D_RHS | 0.10157 |
| FieldMLP | 0.82138 |
| ConvDeepONet1D_RHS | 0.86990 |

At the training grid N=128, the local convolutional ResNet is the strongest controlled baseline.

Paired over 25 PDE×seed cases:
- IPMRaw − ResNet hidden-Q mean difference: +0.04266, 95% CI [+0.02471,+0.06060].
- IPMRaw − FNO hidden-Q mean difference: −0.01055, 95% CI [−0.03000,+0.00890].

Thus IPMRaw is statistically worse than ResNet at the training grid, while IPMRaw and FNO are much closer in hidden-Q accuracy.

## Base rollout Rel-L2

Mean:
- ResNet1D_RHS: 0.000676
- UNet1D_RHS: 0.000862
- IPMRaw: 0.001148
- IPMAdaptive: 0.001174
- FNO1D_RHS: 0.001506
- ConvDeepONet1D_RHS: 0.015354
- FieldMLP: 0.016839

Paired IPMRaw − FNO base-rollout mean difference:
- −3.58e−4
- 95% CI [−6.72e−4,−4.29e−5]

So IPMRaw has lower rollout error than the controlled FNO despite similar hidden-Q accuracy.

## Grid transfer

Mean final rollout Rel-L2:

| Method | N=64 | N=128 | N=256 | N=512 | 512/128 |
|---|---:|---:|---:|---:|---:|
| IPMAdaptive | 0.001438 | 0.001456 | 0.001464 | 0.001470 | 1.010 |
| FNO1D_RHS | 0.001293 | 0.001313 | 0.001323 | 0.001328 | 1.011 |
| FieldMLP | 0.012234 | 0.012262 | 0.012276 | 0.012283 | 1.002 |
| ConvDeepONet1D_RHS | 0.011728 | 0.011751 | 0.011782 | 0.011799 | 1.004 |
| IPMRaw | 0.001154 | 0.001172 | 0.001182 | 0.009133 | 7.793 |
| UNet1D_RHS | 0.010315 | 0.001026 | 0.006761 | 0.009691 | 9.442 |
| ResNet1D_RHS | 0.012047 | 0.000691 | 0.006541 | 0.009498 | 13.737 |

Key observation:
- ResNet/U-Net dominate at N=128 but are strongly tied to the training discretization.
- FNO and IPMAdaptive are the two accurate methods that remain essentially resolution-invariant through N=512.
- Raw IPM again exposes the high-frequency-jet failure without the adaptive observation lift.

This supports a discretization-stability claim for IPMAdaptive, not an absolute accuracy claim.

## Generalization

Hidden-Q mean:
- coefficient OOD: ResNet 0.2148, U-Net 0.2063, FNO 0.2389, IPMRaw 0.3581, IPMAdaptive 0.3585.
- high-frequency IC OOD: ResNet 0.3017, U-Net 0.5020, IPMRaw 0.7185, IPMAdaptive 0.7185, FNO 0.9063.
- 1% noise: U-Net 0.07135, ResNet 0.09459, FNO 0.10261, IPMAdaptive 0.10306, IPMRaw 1.33903.

IPMAdaptive successfully closes the raw-jet noise failure and is essentially tied with controlled FNO on noisy hidden-Q, but it is not the best OOD model in this A0 setting.

Rollout OOD:
- coefficient OOD best: U-Net 0.00219, FNO 0.00258, ResNet 0.00277, IPMRaw 0.00407, IPMAdaptive 0.00413.
- IC OOD best: ResNet 0.00677, U-Net 0.01632, IPMRaw 0.02390, IPMAdaptive 0.02456, FNO 0.03297.
- 1% noisy initial state: ResNet/U-Net/IPMAdaptive/FNO cluster tightly around 0.00839–0.00856.

## Continuous-time / dt result

All continuous-RHS models give essentially identical error across external dt factors 0.5/1/2/3/4 because the evaluation uses the same learned continuous RHS with internal substepping to a nearly fixed substep size.

This result should be described as **solver-step invariance**, not strong evidence of learned dt extrapolation. Future public benchmarks should use a more discriminating temporal-sampling test.

## IPM structural attribution

Mean over all families:
- IPMRaw Jacobian cosine: 0.97961
- IPMAdaptive Jacobian cosine: 0.97870
- IPMRaw spurious-order ratio: 0.04839
- IPMAdaptive spurious-order ratio: 0.05130
- Cartan D_xQ relative error: ~2e−4

The controlled baselines can outperform IPM on field error while IPM retains an explicit, correctly attributed local differential law. These are distinct evaluation axes.

## Efficiency

Mean training time per family/seed on Tesla T4:
- FieldMLP: 5.20 s
- IPMRaw: 7.59 s
- IPMAdaptive: 9.81 s
- ConvDeepONet: 10.08 s
- ResNet: 21.15 s
- FNO: 21.84 s
- U-Net: 25.20 s

At N=128, RHS latency:
- FieldMLP: 0.276 ms
- ConvDeepONet: 0.777 ms
- IPMRaw: 1.081 ms
- IPMAdaptive: 1.481 ms
- U-Net: 1.620 ms
- ResNet: 1.831 ms
- FNO: 1.895 ms

Common RK4 physical-step latency at N=128:
- FieldMLP: 7.89 ms
- ConvDeepONet: 17.79 ms
- IPMRaw: 21.34 ms
- IPMAdaptive: 31.52 ms
- ResNet: 35.85 ms
- U-Net: 36.05 ms
- FNO: 40.33 ms

Parameter counts:
- IPMRaw/IPMAdaptive: 10,081
- ResNet: 14,137
- U-Net: 15,601
- FNO: 26,017

IPMRaw trains ~2.79× faster than ResNet, ~2.88× faster than FNO, and ~3.32× faster than U-Net in this controlled benchmark. Its N=128 RHS is ~1.69×, ~1.75×, and ~1.50× faster respectively.

## Scientific interpretation

A0 falsifies any claim that IPM is automatically the most accurate architecture at the training grid.

What A0 supports instead:
1. IPMRaw is competitive with controlled FNO and can achieve lower rollout error with fewer parameters and lower latency.
2. IPMAdaptive and FNO are the two accurate controlled methods with near-perfect N=64–512 grid transfer.
3. ResNet/U-Net achieve stronger in-grid accuracy but severe off-grid degradation.
4. Adaptive bandwidth is essential for IPM noise and extreme-resolution robustness.
5. IPM uniquely provides explicit local differential-law attribution and Cartan consistency.
6. The strongest current IPM story is an accuracy–efficiency–resolution–interpretability Pareto, not single-metric dominance.

## Next stage

Proceed to external/official benchmarking:
- official PySINDy strong/weak PDE discovery baselines for governing-law identification;
- official PDEBench datasets and official/reference baseline protocols;
- official NeuralOperator FNO implementation;
- later PDEArena/RPB/The Well and pretrained PDE foundation models.

Do not modify the frozen IPM core in response to A0.
