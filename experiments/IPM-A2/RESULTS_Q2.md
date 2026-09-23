# IPM-A2-Q2 Results — Native Differential Core / Speed-First Qualification

## Integrity

Decision: **A2_Q2_FAIL**

Result ZIP SHA256:
`23f7af45c0318992b6ae2fd6570a06a04ddd06c258463aaff9e9e3d9f0020b77`

The supplied SHA256 matches exactly.

Executed notebook:
- 12 code cells
- 11/12 are byte-for-byte identical to the frozen notebook
- the only runtime edit adds `weights_only=False` to two `torch.load` calls for the frozen Q0/Q1 checkpoints; this is an implementation compatibility repair and does not change the experiment hypothesis or model.

## Gates

Passed:
- Q2-0 parent/data integrity
- Q2-1 Local Taylor clean analytic audit
- Q2-3 IDTC <=1% of FNO parameters
- Q2-5 end-to-end speed

Failed:
- Q2-2 finite three-seed rollout
- Q2-4 physical reliability floor
- Q2-6 noise robustness
- Q2-7 resolution robustness
- Q2-8 IDTC not slower than LocalMLP

## Local Taylor lift

Clean analytic worst-case relative error:
- order 1: 0.00580
- order 2: 0.06931
- order 3: 0.04390

Thus the frozen clean derivative gate passes.

However 1% white-noise worst-case errors are:
- order 1: 0.298
- order 2: 8.15
- order 3: 650

Therefore the local Taylor lift is fast and accurate on smooth clean fields but is not yet a robust noisy-observation lift.

Lift latency, batch 16 at public N=256:
- AdaptiveSpectralJet: ~1.05-1.17 ms
- LocalTaylorJet: ~0.20 ms

The local lift is about 5.3-5.8x faster.

## IDTC compactness

Trainable parameters:
- official NeuralOperator FNO: 50,529
- LocalMLP: 9,889
- IDTC: **35**

IDTC/FNO parameter fraction:
[
6.93	imes10^{-4}=0.0693%.
]

Checkpoint size is ~4 KiB for IDTC vs ~44 KiB for LocalMLP.

## End-to-end physical-step speed

Mean eager latency on Tesla T4:

### Advection
- FNO native step: 7.983 ms
- IDTC Euler: 0.798 ms
- IDTC Heun: 1.583 ms
- IDTC RK4: 3.211 ms
- SpectralMLP-P0 RK4: 10.260 ms

### Burgers
- FNO native step: 3.433 ms
- IDTC Euler: 1.121 ms
- IDTC Heun: 2.191 ms
- IDTC RK4: 4.492 ms
- SpectralMLP-P0 RK4: 6.988 ms

The frozen Q2 speed gate therefore passes:
- Advection Euler speedup: ~10.0x
- Burgers Euler speedup: ~3.06x

This is the first valid end-to-end evidence that a PDE-native algebraic core can be substantially faster than the official FNO step.

## Accuracy / stability

All three IDTC seeds become non-finite in long rollout for all Euler/Heun/RK4 variants.

However the one-step errors are low:

### Advection
- Euler: 0.0226
- Heun: 0.00955
- RK4: 0.01044

### Burgers
- Euler: 0.0285
- Heun: 0.0122
- RK4: 0.0126

The failure emerges after repeated evolution:
- Advection IDTC already explodes by horizon 5-10.
- Burgers IDTC remains accurate at horizon 5 for some RK4 seeds (~0.039) but becomes non-finite by horizon 10.

Thus Q2 does **not** show a poor one-step characteristic. It shows an unstable repeated flow.

## IDTC algebra audit

Three-seed algebra expansion reveals a strong reproducible structure.

### Advection beta=1

Mean linear coefficient on first Taylor-jet derivative coordinate:
[
c_{a_1}=-0.9033pm0.0100.
]

Because (a_1=u_x), the dominant learned law is approximately
[
Qapprox-0.903u_x.
]

The remaining linear/quadratic/cubic coefficients are much smaller and less seed-consistent.

### Burgers nu=0.01

The symmetric quadratic matrix has
[
2A_{a_0,a_1}=-1.0018pm0.0118,
]
so the dominant quadratic law is
[
Qapprox-1.002,u,u_x.
]

This almost exactly recovers the nonlinear transport coefficient without an explicit Burgers term library.

The learned coefficient multiplying the Taylor second-order coordinate (a_2=u_{xx}/2) is
[
c_{a_2}=0.00652pm0.00008.
]

Therefore the learned diffusion contribution has the correct derivative direction but underestimates the true coefficient in physical (u_{xx}) units.

Cubic tensor norms are small for most runs but are not guaranteed harmless because high-order jet coordinates can be large outside the training manifold.

## LocalMLP control

Changing only the lift from AdaptiveSpectralJet to LocalTaylorJet substantially hurts long rollout:
- Advection LocalMLP RK4: 0.145 vs frozen SpectralMLP-P0 0.059
- Burgers LocalMLP RK4: 8.32 vs frozen SpectralMLP-P0 0.514

Thus the speed gain of the local lift is real, but a naive clean local-derivative interface is insufficient for robust long-horizon dynamics.

## Scientific interpretation

Q2 falsifies the claim that the raw LocalTaylorJet + full cubic IDTC can directly replace the current IPM core.

But it establishes a much more interesting intermediate result:

1. a 35-parameter differential algebra can recover the dominant public Advection/Burgers PDE structure from trajectory-only training;
2. one-step physical accuracy is already strong;
3. end-to-end step speed can exceed official FNO by ~3-10x;
4. the remaining failure is repeated-flow stability, not lack of a meaningful learned PDE law;
5. local Taylor derivatives need a separate robustness solution before noisy deployment.

The next experiment should therefore preserve the learned IDTC and test **algebraic compilation / degree projection / stability envelopes**, rather than replacing it with a larger neural architecture.
