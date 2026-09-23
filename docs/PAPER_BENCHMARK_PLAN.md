# Paper-Level Comprehensive Benchmark Plan v2

## Goal

The final IPM paper must answer four distinct questions:

1. **Quality:** how close is the simulated field to trusted numerical/reference solutions?
2. **Physical reliability:** does the method preserve the differential law, invariants, spectra, stability and transfer behavior?
3. **Speed:** how many physical grid-points and physical time units can be simulated per second?
4. **Total cost:** what are the parameter, memory, training, compilation and amortized deployment costs?

IPM is evaluated as a **PDE-native computation architecture**, not only as a next-frame predictor.

The final benchmark should be as exhaustive as reproducibly practical. “All models” means all major relevant method families with maintained/open implementations and task-compatible contracts; the paper must not force an architecture onto a task it cannot naturally represent.

---

## Tier 0 — Classical numerical PDE solvers

These are mandatory. They define the accuracy/speed/cost frontier that learned methods must actually beat.

### Finite difference
- first-order upwind
- central difference where stable/applicable
- Lax–Friedrichs
- Lax–Wendroff / MacCormack
- high-order compact / centered differences where appropriate
- WENO5 + SSP-RK3 for nonlinear hyperbolic/conservation tasks

### Finite volume
- Godunov
- Rusanov / local Lax–Friedrichs
- HLL / HLLC where the PDE system supports them
- MUSCL reconstruction where appropriate

### Spectral / pseudo-spectral
- Fourier spectral differentiation
- pseudo-spectral RK
- integrating-factor / ETDRK4 on compatible periodic stiff PDEs

### Diffusion / parabolic
- explicit finite difference at stable CFL
- backward Euler
- Crank–Nicolson
- spectral exponential diffusion

### Transport
- semi-Lagrangian interpolation
- spectral phase shift when periodic constant-coefficient transport admits it

### Reference-solver protocol
For every numerical solver report a tolerance/resolution curve rather than one arbitrary configuration:
- error vs wall time
- error vs grid size
- error vs physical-step size
- CPU and GPU implementation when a credible implementation is available

A high-resolution trusted numerical/reference solution is used only as ground truth and is reported separately from deployable solver baselines.

---

## Tier A — Conventional neural surrogates

Mandatory:
- pointwise MLP / local-law MLP
- ResNet
- Dilated ResNet
- original U-Net
- modern U-Net
- U-FNet / Fourier U-Net where available
- recurrent/autoregressive CNN control where appropriate

Purpose:
- establish whether IPM gains come from PDE-native structure rather than ordinary neural capacity.

PDEArena currently provides FNO, ResNet, DilResNet, multiple U-Net variants, U-FNet and UNO in a common framework, and also reports parameters, memory and timing. Prefer official implementations where possible.

---

## Tier B — Physics-informed neural networks

Core mandatory:
- vanilla PINN
- gPINN / gradient-enhanced PINN
- VPINN / variational PINN
- hp-VPINN where task-compatible
- cPINN for conservation laws
- XPINN for domain-decomposition experiments
- causal/time-marching PINN variant for long temporal domains

Recommended when maintained implementations are reproducible:
- adaptive-weight / self-adaptive PINN
- Fourier-feature PINN / multi-scale PINN
- weak-form PINN
- conservative / entropy-aware PINN variants for hyperbolic equations

Important reporting distinction:
PINNs usually optimize a solution for a particular PDE instance, while IPM/operator methods amortize learning across trajectories/instances. Therefore report:
- per-instance optimization time
- inference/evaluation time after optimization
- total time-to-solution
- memory
- accuracy
rather than inference latency alone.

---

## Tier C — Physics-informed neural operators

Mandatory where task-compatible:
- PINO
- physics-informed FNO / current NeuralOperator physics-informed implementation
- operator + test-time PDE optimization setting when officially supported

Report separately:
1. supervised/pretrained operator cost;
2. PDE-loss training cost;
3. test-time optimization cost;
4. final inference cost.

---

## Tier D — Neural operators

Core mandatory:
- FNO
- TFNO
- DeepONet
- U-NO / UNO
- CNO
- WNO
- GNO / graph neural operator where applicable
- OFormer
- GNOT
- Galerkin Transformer
- U-FNet / Fourier-U-Net operator-style baseline

Add when reliable official implementations support the target task:
- Geo-FNO for irregular geometry
- Clifford/Fourier operator variants for vector-field tasks
- factorized/spectral operator variants available in the official NeuralOperator package

Use official NeuralOperator implementations when available and keep version/hash in the manifest.

---

## Tier E — PDE temporal / iterative surrogates

Mandatory on suitable tasks:
- PDE-Refiner
- modern autoregressive U-Net
- diffusion/refinement PDE surrogate when official code supports the benchmark
- Neural ODE local-generator baseline

Purpose:
- compare long-rollout stability and iterative correction, especially against IPM’s continuous local law.

---

## Tier F — PDE discovery / mechanistic models

Mandatory:
- PDE-FIND / SINDy
- Weak-SINDy / WSINDy
- PDE-Net 2.0
- DeepMoD where a stable reproducible implementation is available

Recommended:
- mechanistic PDE networks / differentiable PDE-solver models when task-compatible

These are not merged into the prediction leaderboard blindly. They receive a law-discovery table:
- term support
- coefficient error
- noise robustness
- identified differential order
- time to identify the law
- time to simulate the identified law with a numerical solver

This last item is important because a discovered explicit PDE can itself become a very fast deployment solver.

---

## Tier G — Multi-PDE / foundation models

Where official checkpoints and task contracts are compatible:
- PDEformer-1
- PDEformer-2
- Poseidon / ScOT
- DPOT
- PROSE-PDE
- MPP
- UPT
- other openly released multi-PDE foundation models that are current at benchmark freeze

Report separate regimes:
1. official pretrained / zero-shot;
2. official pretrained + finetune;
3. from-scratch only when scientifically meaningful.

Do not pretend pretraining cost is zero. Report:
- checkpoint/model size
- published/pretraining compute when available
- downstream finetune compute
- deployment latency

---

## Public benchmark suites

### Primary
- PDEBench
- PDEArena
- Representative PDE Benchmarks (CNO/RPB)
- The Well

### Controlled IPM mechanism suite
- Heat
- Advection
- Burgers
- Allen–Cahn
- KdV
- Wave
- reaction–diffusion
- later shallow-water and Navier–Stokes

Controlled data are for mechanism attribution. Public benchmark data are for external validity.

---

## Accuracy and physical-reliability metrics

Minimum:
- field Rel-L2
- RMSE / nRMSE
- one-step error
- error-vs-physical-horizon curve
- failure/non-finite horizon
- gradient / jet error
- Fourier-band error
- phase error for transport/wave systems
- conservation/invariant drift
- entropy/monotonicity diagnostics where applicable
- PDE residual / learned-law residual
- coefficient/term recovery for interpretable methods
- IC OOD
- BC OOD
- PDE-parameter OOD
- time-step transfer
- grid/resolution transfer
- sparse observation robustness
- additive noise robustness
- sample efficiency
- five-seed confidence intervals / paired effects

---

## Speed benchmark — headline IPM claim

The primary deployment metric is **end-to-end physical simulation throughput**.

Report:

### Latency
- batch-1 physical-step latency
- benchmark-batch physical-step latency
- full physical-horizon latency
- cold-start latency
- warm steady-state latency

### Throughput
- grid-points / second
- physical-time-units / wall-second
- trajectories / second

### Scaling
- 1D: N=64/128/256/512/1024 where supported
- 2D: multiple grid sizes
- batch scaling
- CPU vs GPU scaling
- FP32; optional BF16/FP16 only when accuracy remains valid

For IPM explicitly separate:
1. observation/jet construction;
2. intrinsic characteristic/algebra;
3. compiler/solver step;
4. complete physical step.

Never use characteristic-only latency as the headline speed number.

---

## Cost benchmark

### Deployment cost
- trainable parameters
- non-trainable state/constants
- checkpoint bytes
- peak inference VRAM/RAM
- FLOPs/MACs where meaningful
- kernel launches where informative
- compiled model/binary size

### Training cost
- wall-clock
- GPU-hours
- peak VRAM
- optimizer steps
- data volume consumed
- time-to-fixed-quality threshold

### Amortized cost
For a requested number of trajectories/queries Q:
[
C_{total}(Q)=C_{train}+Q,C_{inference}.
]

Plot break-even Q against:
- classical numerical solver
- PINN per-instance optimization
- neural operators
- IPM

This is essential for digital-twin/repeated-simulation applications.

---

## Fairness regimes

Every major comparison is reported under the appropriate contract rather than one global rank.

### Native/best-practice
Use each method the way its authors intend.

### Matched data
Same training trajectories / observations when possible.

### Matched compute
Same GPU-hours or update budget where meaningful.

### Matched quality
Find the fastest configuration of each method that reaches a common error threshold.

### Matched speed
Compare the best quality each method achieves under the same latency budget.

### Parameter-matched
Useful as an ablation, but not a substitute for best-practice comparison.

---

## Main figures

The paper should include Pareto plots, not a single scalar leaderboard:

1. rollout error vs end-to-end physical-step latency
2. rollout error vs total horizon wall-time
3. error vs parameter count
4. error vs peak memory
5. error vs training GPU-hours
6. physical reliability vs speed
7. speedup vs classical numerical solver at matched quality
8. amortized total cost vs number of simulation queries

IPM should only claim a speed/cost advantage when it lies on a non-dominated Pareto frontier under a clearly specified quality floor.

---

## Current IPM lineage reference

Earlier IPM:
- pointwise MLP characteristic: ~9.9k parameters
- AdaptiveSpectralJet: robust but globally FFT-based

Current speed-first candidate:
- Local Taylor jet
- IDTC: **35 trainable parameters**
- Q2 demonstrated ~3–10x end-to-end step speed potential against the official FNO, but long-horizon stability failed
- Q3 preserved ~2.2–5.3x speed but the first principal-flow compiler was incomplete

Therefore full paper benchmark execution remains blocked until a stable compact IPM operating point is frozen.

---

## Benchmark freeze rule

Before benchmark execution:
1. freeze one primary IPM architecture;
2. freeze one robust deployment mode and one maximum-speed deployment mode if both are scientifically justified;
3. freeze datasets/splits;
4. freeze hardware/software precision;
5. freeze baseline implementations/commits;
6. preregister the metric and timing protocol.

After benchmark start, no baseline-specific IPM tuning is permitted on the official test sets.
