# IPM-M4-FIX1 Results

## Formal decision
**PASS_M4_FIX1**

Result ZIP SHA256:
`e91c3a7a346bffb18ca83e049d9615cea0e2032c452714c7e15b7b588ddf91ca`

The returned checksum matches the supplied `.sha256` file.

The executed notebook code cells are identical to the released notebook code cells.

## Gate summary

Passed:
- G0 integrity
- G1 equal optimizer updates
- G2 raw real-FFT jet equivalence
- G3 physical-bandwidth covariance
- G5 unseen 3% noise
- G6 extreme M=24
- G7 N=512 rollout
- G8 64/128/256 grid transfer
- G9 Jacobian discovery
- G10 spurious-order suppression
- G11 finite formal evaluation
- G12 five-seed noise robustness

Failed:
- G4 clean-bias control
- G13 real-FFT efficiency target

The preregistered PASS rule is satisfied.

## Physical-bandwidth covariance

For the analytic signal containing modes 2, 5 and 6, the adaptive estimator returns:

| N | k_E | k_c | adaptive-vs-raw jet Rel-L2 |
|---:|---:|---:|---:|
| 64 | 6 | 12 | 0.002419 |
| 128 | 6 | 12 | 0.002419 |
| 256 | 6 | 12 | 0.002419 |
| 512 | 6 | 12 | 0.002419 |

This confirms the observation lift is tied to physical spectral content rather than a fixed Nyquist fraction.

## Hidden clean-law accuracy

Mean exact-Q Rel-RMSE:
- CleanIntegralFlow: 0.11644
- RawJetIntegralFlow: 0.17917
- FixedScaleJetIntegralFlow: 0.19153
- AdaptiveBandwidthJetIntegralFlow: 0.20139

Adaptive / Raw:
[
1.124.
]

Therefore the adaptive lift still carries about 12.4% clean-law bias relative to raw corrupted-observation training and misses the frozen <=1.10 threshold.

## Noise robustness

Mean observed-state Q Rel-RMSE:

| Condition | Raw | Fixed Scale | Adaptive Bandwidth |
|---|---:|---:|---:|
| dense clean | 0.2419 | 0.2580 | 0.2723 |
| dense 1% noise | 0.6733 | 0.3551 | 0.2731 |
| dense 2% noise | 0.7963 | 0.4964 | 0.2751 |
| unseen 3% noise | 0.6524 | 0.3091 | 0.2790 |
| extreme 5% noise | 0.7908 | 0.3646 | 0.2913 |
| unseen M=48 | 0.3339 | 0.2573 | 0.2700 |
| unseen M=96 | 0.5750 | 0.2922 | 0.2724 |
| extreme M=24 | 0.2691 | 0.3586 | 0.2706 |

At unseen 3% noise, Adaptive/Raw is:
[
0.428,
]
a ~57.2% error reduction.

At 5% noise, Adaptive/Raw is:
[
0.368,
]
a ~63.2% reduction.

Extreme M=24 is essentially neutral relative to Raw (ratio ~1.006), while avoiding the strong fixed-filter bias.

Noise-robustness direction is reproduced in 5/5 seeds.

## N=512 closure

AdaptiveBandwidthJet mean rollout error:

| PDE | N=64 | N=128 | N=256 | N=512 | 512/128 |
|---|---:|---:|---:|---:|---:|
| Advection | 0.01126 | 0.01132 | 0.01135 | 0.01136 | 1.004 |
| Allen-Cahn | 0.00637 | 0.00644 | 0.00648 | 0.00650 | 1.009 |
| Burgers | 0.01076 | 0.01087 | 0.01092 | 0.01095 | 1.007 |
| Heat | 0.000770 | 0.000774 | 0.000776 | 0.000777 | 1.004 |
| KdV | 0.00864 | 0.00872 | 0.00875 | 0.00876 | 1.005 |

Aggregate N=512/N=128:
[
1.006.
]

This closes the repeated extreme-resolution failure seen in M2-FIX1, M3 and M4.

For comparison, RawJet aggregate N=512/N=128 is ~1.824, with Burgers ~2.20 and KdV ~2.46.

## Differential-law structure

Adaptive mean Jacobian cosine:
- Advection: 0.9843
- Burgers: 0.9528
- Heat: 0.9468
- KdV: 0.9633
- Allen-Cahn: 0.7688

Four of five pass 0.80.

Spurious-order ratio:
- Advection: 0.0652
- Burgers: 0.00237
- Heat: 0.2887
- KdV: 0.0101
- Allen-Cahn: 0.0297

Four of five pass 0.25.

The remaining structural weaknesses are Allen-Cahn Jacobian alignment and Heat unused-order leakage.

## Held-out sparse-time consistency

At unseen temporal factor g=3:
- Adaptive mean residual: 0.8642
- Fixed Scale: 0.8974
- Raw: 0.9460

Adaptive improves the result but the absolute residual remains high. This is a remaining limitation for sparse-time local-law identification and should be evaluated in the paper benchmark rather than hidden by further architecture changes.

## Efficiency

Repeated FFT vs new real-FFT/batched-irFFT jet:
- N=128 ratio: 1.003
- N=512 ratio: 0.897

The new implementation is numerically equivalent but does not satisfy the <=0.75 speed target.

Measured T4 latency for Adaptive IPM:
- Q only: 0.302 / 0.348 / 0.587 / 0.877 ms at N=64/128/256/512
- full jet + Q RHS: ~1.48–1.67 ms over the same range

The characteristic network remains inexpensive; observation-jet construction dominates end-to-end RHS latency.

## Research-stage conclusion

The M-series mechanism qualification is complete.

Established:
1. frozen holonomic jet / characteristic / Cartan / evolutionary-field core;
2. trajectory-only law identification;
3. matched-budget equivalence to derivative/RHS supervision;
4. strong noise robustness with a deterministic observation lift;
5. resolution-covariant N=64–512 behavior;
6. reproducible differential-law attribution.

Remaining issues are now benchmark-level questions, not reasons to continue modifying the core:
- clean-vs-noise observation-lift Pareto;
- sparse-time identification;
- Allen-Cahn/Heat structural attribution;
- implementation-level jet latency.

Next stage: IPM-A0 controlled paper benchmark, followed by official public benchmark suites and official external baseline implementations.
