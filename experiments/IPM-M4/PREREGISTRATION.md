# IPM-M4 — Sparse / Noisy Trajectory Qualification

## Purpose

M3-FIX1 established that the frozen IPM core can identify local PDE characteristics from trajectories without exact instantaneous RHS labels under dense, clean observations.

M4 asks whether this result survives realistic observation degradation without changing the IPM mathematical core.

The frozen core remains:

[
J^K u ightarrow Q_	heta ightarrow D_x ightarrow V_Q.
]

No learned denoiser, attention block, neural operator, or new PDE-specific module is introduced.

## Observation model

Observed states are generated as

[
y(x_j,t_n)=u(x_j,t_n)+epsilon_{j,n},
qquad
epsilonsimmathcal N(0,ho^2,mathrm{std}(u)^2).
]

Training observation conditions are sampled from:

- spatial points (Min{32,64,128});
- temporal subsampling factor (gin{1,2,4});
- relative noise (hoin{0,0.005,0.01,0.02}).

The same underlying clean trajectory is used for all compared methods.

## Observation lifts

### Raw spectral jet

Construct

[
J^3 y=(y,D_xy,D_x^2y,D_x^3y)
]

directly on the observed periodic grid.

This is expected to expose derivative-noise amplification.

### Scale-space jet

Use one fixed, non-learned Fourier smoothing operator

[
S_sigma,
qquad
widehat{S_sigma y}(k)=
exp[-(|k|/k_c)^8]hat y(k),
]

with

[
k_c=0.5,k_{mathrm{Nyquist}}.
]

Then construct

[
J^3_sigma y =
(S_sigma y,D_xS_sigma y,D_x^2S_sigma y,D_x^3S_sigma y).
]

Because differentiation and the translation-invariant smoothing operator commute,

[
D_x^r S_sigma y=S_sigma D_x^r y.
]

This is an observation interface, not part of the frozen IPM core.

## Methods

1. **CleanIntegralFlow** — clean dense upper reference.
2. **RawJetIntegralFlow** — proposed trajectory integral objective with raw corrupted jets.
3. **ScaleJetIntegralFlow** — same objective with scale-space observation lift.
4. **ScaleJetSecant** — same scale-space observations but central-secant derivative supervision.

For every PDE family and seed:
- identical base initialization;
- identical clean source trajectories;
- identical observation-condition schedule;
- identical sampled triplets;
- identical batch size;
- identical optimizer-step budget;
- identical optimizer/LR schedule.

Only the observation lift and/or identification objective differ.

## PDE suite

- Heat
- Advection
- Burgers
- Allen–Cahn
- KdV

Every characteristic sees an overcomplete (J^3) state and is not told the physical PDE order.

## Formal seeds

11, 29, 47, 71, 97.

## Training budget

- 48 matched corrupted triplet batches / epoch
- 20 epochs
- 960 optimizer updates per family/seed/method
- final checkpoint only

## Held-out robustness tests

In-distribution matrix:
- (Min{32,64,128})
- (hoin{0,0.01,0.02})
- (gin{1,2,4})

Unseen conditions:
- (M=48,96)
- (ho=0.03)
- (g=3)

Extreme diagnostics:
- (ho=0.05)
- (M=24)

## Evaluation

Hidden clean exact-law evaluation:
- exact (Q) Rel-RMSE;
- Jacobian cosine;
- spurious derivative-order sensitivity.

Trajectory evaluation:
- common external RK4 rollout from clean initial state;
- common external RK4 rollout from corrupted reconstructed initial observation;
- held-out observation-condition integral consistency.

Robustness:
- degradation vs dense clean reference;
- condition-wise failure rate;
- five-seed reproducibility.

Efficiency diagnostic:
- naive repeated-FFT jet construction;
- fused one-forward-FFT jet construction;
- (Q_	heta)-only latency;
- full jet+(Q_	heta) RHS latency.

## Frozen gates

G0 — protocol/core/observation-lift source integrity PASS.  
G1 — equal optimizer-step counts and matched condition/triplet schedule PASS.  
G2 — fused jet agrees with naive jet to relative L2 <1e-6 when filtering is disabled.  
G3 — ScaleJetIntegralFlow hidden clean-Q mean <=1.35x CleanIntegralFlow.  
G4 — ScaleJetIntegralFlow hidden clean-Q mean <=0.80x RawJetIntegralFlow.  
G5 — ScaleJetIntegralFlow hidden clean-Q mean <=1.20x ScaleJetSecant.  
G6 — Jacobian cosine >=0.80 on >=4/5 PDE families for ScaleJetIntegralFlow.  
G7 — spurious-order ratio <=0.25 on >=4/5 PDE families.  
G8 — under unseen (ho=0.03), ScaleJetIntegralFlow corrupted-observation rollout error <=0.80x RawJetIntegralFlow.  
G9 — under unseen (M=48/96,g=3), ScaleJetIntegralFlow degradation <=2.0x dense-clean baseline.  
G10 — no NaN/Inf in all formal in-distribution and unseen-condition evaluations.  
G11 — robustness direction (ScaleJet better than RawJet on noisy conditions) reproduced in >=4/5 formal seeds.  
G12 — fused jet constructor latency <=0.60x naive repeated-FFT jet latency at N=128 and N=512.

Decision:
- PASS_M4: G0/G1/G2/G10 mandatory and at least 7 of G3–G9/G11/G12.
- CONDITIONAL_M4: integrity/stability pass but sparse/noisy robustness is incomplete.
- FAIL_M4: corrupted-observation IPM cannot recover a stable local characteristic.

## Advancement

PASS_M4 freezes the observation-robust trajectory-identification protocol.

The next qualification stage will isolate the remaining N=512 high-frequency extrapolation failure before paper-scale benchmarking.
