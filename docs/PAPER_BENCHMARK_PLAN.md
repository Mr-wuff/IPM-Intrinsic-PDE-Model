# Paper-Level Benchmark Plan

## Principle

The benchmark must evaluate IPM as a **PDE-native local law model**, not only as a next-frame surrogate.

No single baseline family is sufficient. The paper will use layered comparisons so that each claimed advantage has a relevant competitor.

## Tier A — Classical and simple neural controls

Mandatory:
- Spectral / finite-difference numerical solver reference
- MLP / pointwise local-law baseline
- ResNet / Dilated ResNet
- U-Net / modern U-Net

Purpose:
- establish absolute solver error and conventional finite-dimensional neural baselines;
- quantify accuracy/efficiency Pareto behavior.

## Tier B — Physics-informed learning

Mandatory:
- PINN
- gPINN
- PINO

Optional task-dependent:
- XPINN / cPINN for domain-decomposition or conservation experiments

Purpose:
- distinguish IPM's architecture-native differential structure from external PDE residual regularization.

## Tier C — PDE discovery / system identification

Mandatory:
- PDE-FIND / sparse regression
- WSINDy
- PDE-Net 2.0
- DeepMoD if a stable maintained implementation is available

Purpose:
- compare trajectory-only law recovery, derivative-order identification, coefficient recovery, noise robustness, and interpretability.

## Tier D — Neural operators

Core mandatory:
- FNO
- DeepONet
- CNO
- U-NO / UNO
- WNO
- OFormer
- GNOT

Recommended:
- Galerkin Transformer
- TFNO where benchmark infrastructure supports it

Purpose:
- compare solution-operator accuracy, grid transfer, long rollout, parameter OOD, and cost.

## Tier E — Strong temporal PDE surrogates

Mandatory on suitable 2D fluid tasks:
- PDE-Refiner
- modern U-Net / U-FNet baselines from PDEArena

Purpose:
- test long-horizon stability and high-frequency fidelity.

## Tier F — Multi-physics / foundation PDE models

Where data/task contracts are compatible:
- PDEformer-1 for 1D multi-PDE experiments
- PDEformer-2 for 2D multi-PDE / inverse problems
- Poseidon
- PROSE-PDE
- MPP
- DPOT
- UPT

These models must not be forced into an unfair task. Report:
1. zero-shot/pretrained setting when official checkpoints match the task;
2. fine-tuned setting under a documented compute budget;
3. from-scratch matched-budget setting only when meaningful.

## Public benchmark suites

Primary:
- PDEBench
- PDEArena
- Representative PDE Benchmarks (CNO/RPB)
- The Well

Controlled IPM suite:
- Heat
- Advection
- Burgers
- Allen-Cahn
- KdV
- Wave
- later reaction-diffusion, shallow-water, Navier-Stokes

Use the controlled suite for mechanism attribution and public suites for external validity.

## Accuracy / physics metrics

Report at minimum:
- field relative L2 / RMSE
- rollout error vs physical horizon
- derivative / jet error
- gradient error
- high-frequency spectral error
- conservation / invariant drift where applicable
- PDE-law Jacobian attribution for methods with identifiable local laws
- coefficient recovery / term-selection F1 for discovery tasks
- dt transfer
- grid transfer
- parameter OOD
- IC/BC OOD
- sparse-data and noisy-data robustness
- sample efficiency
- five-seed confidence intervals and paired effect sizes

## Efficiency benchmark

Measure on exactly the same hardware, dtype, batch, grid, horizon, and compilation mode.

### Model complexity
- trainable parameters
- checkpoint size
- activation memory
- peak GPU memory
- FLOPs / MACs where well-defined

### Training efficiency
- wall-clock to fixed validation target
- wall-clock per epoch
- samples / grid-points per second
- optimizer updates to target accuracy
- GPU-hours
- energy proxy if reliably measurable

### Inference efficiency
Report four separate timings for IPM:
1. characteristic network Q only on a precomputed jet;
2. jet construction only;
3. one full RHS evaluation: jet + Q;
4. one physical rollout step including the common numerical integrator.

Also report:
- latency at batch 1
- throughput at benchmark batch
- full-horizon latency
- peak inference memory
- scaling with N=64/128/256/512 and 2D grid size
- accuracy-vs-latency Pareto
- accuracy-vs-parameter Pareto
- error-vs-GPU-memory Pareto

This separation is essential because current IPM has a very small characteristic network but its end-to-end cost includes differential-state construction and multiple solver RHS evaluations.

## Current IPM efficiency reference

The present local characteristic has approximately **10,081 trainable parameters** (width 96, input dimension 6).

This is orders of magnitude smaller than many operator/foundation baselines, but no paper claim should be made from parameter count alone.

The current reference implementation is not yet latency-optimized:
- each Q evaluation constructs first/second/third spectral derivatives;
- the current implementation repeats the forward FFT for each derivative;
- the external RK4 interface performs multiple Q evaluations per physical step.

Before final efficiency benchmarking, implement a mathematically equivalent fused jet constructor that computes one forward FFT and reuses it for all derivative orders. Both naive and optimized implementations should be regression-tested for numerical equivalence.

## Fair-comparison policy

Use three comparison regimes:

### Capacity-matched
Match trainable parameter count as closely as practical.

### Compute-matched
Match GPU-hours or optimizer-step / token-point budget.

### Best-practice
Use each baseline's recommended configuration and report its true size/cost.

This prevents a tiny IPM from being unfairly compared only against very large foundation models and simultaneously prevents size matching from hiding the performance of state-of-the-art systems.

## Benchmark reporting

The main paper should use a compact representative table, while the supplement contains the complete model matrix.

No global rank or aggregate score should hide task-specific behavior. Report Pareto fronts and per-regime results.
