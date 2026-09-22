# IPM-A0 — Controlled Paper Benchmark

## Status

The M-series mechanism qualification is closed after PASS_M4_FIX1.

A0 begins paper-scale benchmarking. It does not modify the frozen IPM core.

## Goal

Compare IPM against representative field-based continuous-RHS learners under a strictly controlled trajectory-only setting.

This benchmark is **descriptive, not winner-gated**. No advancement rule requires IPM to outperform a baseline.

## Frozen task

PDE families:
- Heat
- Advection
- Burgers
- Allen-Cahn
- KdV

Training:
- periodic domain L=2pi
- grid N=128
- observation dt=0.00125
- trajectory-only supervision
- matched trajectory triplets
- same IntegralFlow objective for every continuous-RHS method
- same external RK4 solver at evaluation
- same optimizer-step budget
- same parameter ranges and data splits

## Methods

### IPM-Raw
Frozen IPM local characteristic on the raw holonomic Taylor jet.

### IPM-Adaptive
Same IPM core with the resolution-covariant adaptive spectral-bandwidth observation lift from M4-FIX1.

### Field-MLP
Pointwise field-only local characteristic Q(u,lambda).

### ResNet1D-RHS
Convolutional residual field model predicting Q(x).

### FNO1D-RHS
Fourier neural operator-style field model predicting Q(x).

### UNet1D-RHS
U-Net field model predicting Q(x).

### ConvDeepONet1D-RHS
Controlled DeepONet-style baseline with a convolutional branch encoder and coordinate trunk.

Important: these are controlled implementations for mechanism comparison. They are not claimed to be official repository reproductions. Official external implementations are reserved for later public-benchmark stages.

## Fairness

For each PDE family and formal seed:
- same source trajectories;
- same train/validation/test split;
- same sampled triplet schedule;
- same physical parameters;
- same number of optimizer updates;
- same AdamW schedule;
- final checkpoint only;
- same RK4 rollout solver for all continuous-RHS models.

All models train with the same trajectory integral identity:

[
u_2-u_0 approx rac{h}{3}[Q(u_0)+4Q(u_1)+Q(u_2)].
]

## Formal seeds

11, 29, 47, 71, 97.

## Evaluation axes

### Accuracy
- hidden exact-Q relative RMSE
- base rollout Rel-L2
- rollout error vs horizon
- gradient error
- high-frequency spectral error

### Generalization
- grid: 64 / 128 / 256 / 512
- dt factors: 0.5 / 1 / 2 / 3 / 4 at fixed physical horizon
- coefficient OOD
- high-frequency IC OOD
- 1% input-noise robustness

### IPM structural metrics
- PDE-law Jacobian cosine
- spurious derivative-order sensitivity
- Cartan D_xQ consistency

These structural metrics are not forced onto baselines that do not expose a local jet law.

### Efficiency
Measured on identical hardware and dtype:
- parameter count
- checkpoint size
- Q-only / RHS latency
- one common RK4 physical-step latency
- full rollout latency
- peak inference VRAM
- peak training VRAM
- training wall time
- throughput
- N-scaling
- accuracy-vs-parameter Pareto
- accuracy-vs-latency Pareto

## Benchmark integrity criteria

B0 — protocol/source hashes match.  
B1 — every method/family/seed receives exactly the frozen update count.  
B2 — all formal runs finish without NaN/Inf.  
B3 — evaluation uses the same test cases across methods.  
B4 — all method parameter counts/checkpoint sizes/latencies are recorded.  
B5 — grid and dt comparisons preserve physical final time.  
B6 — five-seed mean/std and paired per-case tables are exported.  
B7 — raw per-run results are saved; no aggregate-only reporting.

A0 is considered complete when B0–B7 pass, regardless of which method is best.

## Next stages

A1: official PDE discovery baselines and official public benchmark implementations.  
A2: PDEBench / PDEArena / RPB / selected The Well tasks.  
A3: pretrained/foundation PDE models such as Poseidon, PDEformer, PROSE-PDE, MPP/DPOT/UPT where task contracts are compatible.
