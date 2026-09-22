# IPM-M4 Results

## Formal notebook decision
**CONDITIONAL_M4**

Result ZIP SHA256:
`2427f54eac5bddce45563045d0ce776708ca7a68dcde5110df9668f1a434c866`

The checksum matches the returned `.sha256` file.

## User-side implementation correction

The executed notebook differs from the released notebook in exactly one code cell.

Original robustness evaluation created CPU noise and added it to a CUDA tensor:

```python
noise=torch.randn(clean.shape,generator=g,dtype=clean.dtype)
noisy=clean + float(rho)*clean.std(dim=-1,keepdim=True).cpu()*noise
```

The executed notebook changed this to:

```python
noise=torch.randn(clean.shape,generator=g,dtype=clean.dtype).to(clean.device)
noisy=clean + float(rho)*clean.std(dim=-1,keepdim=True)*noise
```

This correction occurs only in post-training robustness evaluation. Training code and saved checkpoints are unchanged. It is accepted as a device-consistency bug fix.

## Gate summary

Passed:
- G0 integrity
- G1 equal optimizer updates
- G2 fused-jet numerical equivalence
- G5 ScaleJet IntegralFlow vs ScaleJet Secant
- G6 Jacobian discovery
- G7 spurious-order suppression
- G8 unseen 3% noise robustness
- G9 unseen sparse degradation
- G10 finite formal evaluation
- G11 five-seed robustness direction

Failed:
- G3 ScaleJet vs clean hidden-Q
- G4 ScaleJet vs raw hidden-Q
- G12 fused-jet speed target

## Critical evaluation-interface issue

The M4 function `hidden_q_eval()` evaluates **every** method with:

```python
fused_jet(..., scale_filter=False)
```

including ScaleJetIntegralFlow and ScaleJetSecant.

Those models were trained on the scale-space observation lift, so G3/G4 use an interface inconsistent with the ScaleJet training contract. Their numerical values must not be treated as valid method-comparison evidence.

The separate observation-robustness evaluation correctly applies each method's own lift and is therefore the stronger evidence for the scale-space tradeoff.

## Observation robustness evidence

Mean Q Rel-RMSE:

| Condition | RawJet | ScaleJet | Scale/Raw |
|---|---:|---:|---:|
| dense clean | 0.2414 | 0.2580 | 1.069 |
| dense 1% noise | 0.6736 | 0.3551 | 0.527 |
| dense 2% noise | 0.7974 | 0.4964 | 0.623 |
| sparse 64 + 1% | 0.4124 | 0.2646 | 0.642 |
| sparse 32 + 1% | 0.2653 | 0.2567 | 0.968 |
| unseen M=48 | 0.3335 | 0.2573 | 0.772 |
| unseen M=96 | 0.5750 | 0.2921 | 0.508 |
| unseen 3% noise | 0.6529 | 0.3091 | 0.473 |
| extreme 5% noise | 0.7922 | 0.3646 | 0.460 |
| extreme M=24 | 0.2687 | 0.3586 | 1.335 |

The fixed scale-space lift therefore strongly suppresses derivative-noise amplification, but introduces bias in clean and extremely sparse regimes.

The robustness direction is reproduced in 5/5 seeds.

## Structural evidence

ScaleJetIntegralFlow mean Jacobian cosine:
- Advection: 0.9832
- Burgers: 0.9504
- Heat: 0.9481
- KdV: 0.9605
- Allen-Cahn: 0.7758

Four of five families pass the 0.80 criterion.

Spurious-order sensitivity:
- Advection: 0.0656
- Burgers: 0.00173
- Heat: 0.2868
- KdV: 0.00994
- Allen-Cahn: 0.0281

Four of five pass the 0.25 criterion.

## Held-out sparse-time consistency

At unseen temporal factor 3 and unseen M=48/96, ScaleJet improves the integral residual relative to RawJet, but absolute normalized residuals remain high (~0.89 average). Sparse/noisy integral consistency is therefore not yet solved.

## Efficiency

Fused vs repeated-FFT jet construction:
- N=128 ratio: 0.741
- N=512 ratio: 0.748

The fused implementation is ~25% faster, but the preregistered <=0.60 speed target was too aggressive for the current FFT/IFFT call pattern.

Current Q-only latency:
- N=64: 0.367 ms
- N=128: 0.347 ms
- N=256: 0.600 ms
- N=512: 0.904 ms

Current full jet+Q RHS latency is ~1.02 ms in this T4 run.

## Scientific diagnosis

The fixed filter

[
k_c=0.5k_{Nyquist}
]

solves part of the noise-amplification problem but is not resolution-covariant: its physical cutoff changes whenever grid resolution changes.

This explains the observed tradeoff:
- high-noise/high-resolution conditions benefit;
- clean and very sparse conditions suffer smoothing bias.

The next experiment should replace Nyquist-fraction smoothing with a deterministic **spectral-confidence observation lift** whose effective physical bandwidth is estimated from the observed signal-to-noise spectrum.

This remains an observation interface and does not modify the frozen IPM core.
