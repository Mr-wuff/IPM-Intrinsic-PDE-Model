# IPM-M4-FIX1 — Resolution-Covariant Spectral-Bandwidth Jet

## Motivation

M4 produced a CONDITIONAL result.

The fixed observation lift

[
k_c=0.5k_{Nyquist}
]

strongly improved robustness under 1–5% noise, but introduced clean/sparse bias and is itself discretization dependent.

M4 also contained an evaluation-interface bug: `hidden_q_eval()` fed raw jets to ScaleJet models. M4-FIX1 corrects this by requiring every method to be evaluated through the same observation lift used in training.

The IPM mathematical core remains frozen.

## First-principles observation lift

For an observation (y), compute the real Fourier spectrum

[
Y(k)=mathcal F[y].
]

Estimate the white-noise spectral floor from the upper quarter of the spectrum:

[
widehat P_n
=
rac{operatorname{median}_{|k|>0.75k_N}|Y(k)|^2}{ln 2}.
]

Define trusted signal power

[
P_s(k)=max(|Y(k)|^2-6widehat P_n,0).
]

Let (k_E) be the smallest physical wavenumber containing 99.5% of the cumulative trusted spectral energy.

The filter cutoff is

[
k_c
=
min(2k_E,;0.9k_N),
]

with a minimum (k_c=2).

The observation lift is

[
W(k)=exp[-(|k|/k_c)^8],
]

[
J^3_{conf}y
=
left(
mathcal F^{-1}[WY],
mathcal F^{-1}[ikWY],
mathcal F^{-1}[(ik)^2WY],
mathcal F^{-1}[(ik)^3WY]
ight).
]

The key difference from M4 is that (k_c) is determined by **physical signal bandwidth**, not a fixed fraction of grid Nyquist.

For the same band-limited physical field sampled at different resolutions, (k_E) should remain invariant.

This is a deterministic observation interface, not a learnable IPM component.

## Methods

1. **CleanIntegralFlow** — clean dense upper reference.
2. **RawJetIntegralFlow** — corrupted observations, no spectral reliability lift.
3. **FixedScaleJetIntegralFlow** — M4 fixed (0.5k_N) lift.
4. **AdaptiveBandwidthJetIntegralFlow** — proposed resolution-covariant lift.

M3-FIX1 already established matched-budget equivalence between IntegralFlow and Secant supervision. M4-FIX1 therefore holds the identification objective fixed and isolates the observation lift.

## Fairness

For every PDE/seed:
- identical initial state_dict;
- identical source trajectories;
- identical sampled triplets;
- identical spatial/noise/time corruption schedule;
- identical batch size;
- identical optimizer and LR schedule;
- exactly 960 updates;
- final checkpoint only.

## Training observation distribution

- spatial points (Min{32,64,128})
- temporal factor (gin{1,2,4})
- noise (hoin{0,0.005,0.01,0.02})

## Evaluation

### Corrected clean-law evaluation
Every model is evaluated using its own training-time lift.

### Noise / sparsity
- 1%, 2%, unseen 3%, extreme 5% noise
- M=32,64,128
- unseen M=48,96
- extreme M=24

### Resolution
Clean rollout at:
- N=64
- N=128
- N=256
- N=512

N=512 is now a formal gate rather than diagnostic-only.

### Structural
- PDE-law Jacobian cosine
- spurious differential-order sensitivity

### Temporal
- unseen factor (g=3) integral consistency at M=48/96

### Efficiency
Compare:
- repeated complex FFT jet
- fused real-FFT/batched-irFFT jet
- Q-only latency
- full jet+Q latency

## Frozen gates

G0 — protocol/core/lift integrity PASS.  
G1 — all methods receive exactly 960 matched updates.  
G2 — raw real-FFT jet matches the reference repeated-FFT jet to relative L2 <2e-6.  
G3 — analytic physical-bandwidth covariance: estimated (k_E) varies by <=1 Fourier mode across N=64/128/256/512 and adaptive clean-jet relative error vs raw <0.02.  
G4 — AdaptiveBandwidthJet hidden clean-Q mean <=1.10x RawJet hidden clean-Q mean.  
G5 — unseen 3% noise Q error <=0.75x RawJet.  
G6 — extreme M=24 Q error <=1.10x RawJet.  
G7 — clean N=512 rollout error <=2.0x AdaptiveBandwidthJet N=128 error.  
G8 — 64/128/256 mean grid degradation <=1.25x N=128 baseline.  
G9 — Jacobian cosine >=0.80 on >=4/5 PDE families.  
G10 — spurious-order ratio <=0.25 on >=4/5 PDE families.  
G11 — all formal evaluations finite.  
G12 — noisy-robustness direction AdaptiveBandwidthJet < RawJet reproduced in >=4/5 seeds.  
G13 — fused real-FFT jet latency <=0.75x repeated-FFT jet at N=128 and N=512.

Decision:
- PASS_M4_FIX1: G0/G1/G2/G3/G11 mandatory and >=6 of G4–G10/G12/G13.
- CONDITIONAL_M4_FIX1: mathematical/implementation gates pass but observation robustness or N=512 behavior remains incomplete.
- FAIL_M4_FIX1: adaptive physical-bandwidth lift is unstable or breaks the frozen IPM law.

## Advancement

PASS_M4_FIX1 closes both remaining qualification issues:
1. sparse/noisy observations;
2. the repeated N=512 high-frequency failure.

The project then enters paper-scale public benchmarking without further modification of the IPM core.
