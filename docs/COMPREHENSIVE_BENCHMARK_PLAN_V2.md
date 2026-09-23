# IPM Comprehensive Paper Benchmark Plan v2

## Goal

The final benchmark for *Make PDE integrated into model native* will measure whether IPM provides a useful new point on the PDE-computation frontier:

**quality / physical reliability / end-to-end speed / memory / parameter count / training cost / amortized simulation cost.**

It will not be limited to FNO.

The benchmark will cover the major reproducible families of:
1. classical PDE numerical solvers;
2. conventional neural surrogates;
3. neural operators;
4. operator transformers;
5. physics-informed neural networks;
6. physics-informed neural operators;
7. pretrained/foundation PDE models;
8. PDE law-discovery systems.

No single global ranking is allowed across incompatible information contracts.

---

## A. Information-contract regimes

### Regime E — Equation-known solver

The governing PDE, parameters, ICs and BCs are given.

Methods:
- classical numerical solvers;
- PINNs and their variants.

This regime measures solve-time/cost/accuracy when the equation is explicitly available.

### Regime D — Data-trained surrogate

Training trajectories are given; the explicit PDE is not supplied to the model.

Methods:
- IPM trajectory-only variants;
- FNO and neural operators;
- U-Net/ResNet/transformer surrogates.

This is the main regime for evaluating learned simulation engines.

### Regime P — Pretrained/foundation model

A pretrained model may contain information from other PDEs.

Report separately:
- zero-shot;
- linear/readout adaptation if supported;
- full fine-tuning.

Pretraining cost is reported separately and never silently ignored.

### Regime L — Law discovery

Observed trajectories are given and the task is governing-law identification.

Methods:
- IPM intrinsic-law audit;
- PDE-FIND/SINDy;
- Weak-SINDy/WSINDy;
- PDE-Net 2.0;
- DeepMoD;
- other stable public discovery implementations.

---

## B. Classical numerical PDE baselines

Where mathematically applicable, include:

### Spectral
- Fourier pseudo-spectral + RK4
- Fourier pseudo-spectral + adaptive RK
- ETDRK4
- exact Fourier propagator for linear PDEs as an oracle/reference

### Finite difference
- first-order upwind
- second-order central
- fourth-order centered
- Lax-Wendroff where applicable
- Crank-Nicolson
- implicit/IMEX time stepping

### Finite volume / conservation-law solvers
- Godunov
- Rusanov / local Lax-Friedrichs
- MUSCL
- WENO5 + SSPRK

### Other task-dependent numerical baselines
- semi-Lagrangian advection
- finite element / discontinuous Galerkin for geometry benchmarks
- reference solver supplied by the public benchmark

Every numerical solver records:
- spatial resolution;
- temporal tolerance/CFL;
- order;
- number of RHS evaluations / linear solves;
- CPU/GPU backend;
- total wall time.

Numerical solvers are evaluated by **error-versus-cost curves**, not one arbitrary resolution.

---

## C. Conventional learned surrogates

At minimum:
- pointwise MLP
- temporal MLP
- ResNet
- Dilated ResNet
- U-Net 2015
- modern U-Net
- U-FNet / Fourier U-Net
- standard Transformer
- Swin-style structured-grid baseline where applicable

PDEArena configurations are preferred whenever supported to avoid custom weak baselines.

---

## D. Neural operators

### Official NeuralOperator 2.x family
Where the task/domain contract supports the model:
- FNO
- TFNO
- LocalNO
- UNO
- RNO
- GINO
- FNOGNO
- OTNO
- UQNO
- CODANO
- SFNO for spherical tasks only

### Major external neural-operator families
- DeepONet
- CNO
- WNO
- MWT
- U-FNO
- F-FNO
- Geo-FNO where geometry applies
- Galerkin Transformer
- OFormer
- GNOT
- LSM
- FactFormer
- ONO
- Transolver
- UPT

Use official repositories or a recognized unified benchmark implementation whenever possible.

---

## E. Physics-informed methods

### PINNacle family

Use the published PINNacle implementations where the PDE contract is supported:

- vanilla PINN
- PINN Adam + L-BFGS
- PINN-LRA
- PINN-NTK
- RAR
- MultiAdam
- gPINN
- hp-VPINN
- LAAF
- GAAF
- FBPINN

### Additional important PINN variants

Where reproducible and task-compatible:
- cPINN
- XPINN
- SA-PINN
- causal PINN / time-causal weighting

### Physics-informed operator methods
- PINO
- PI-DeepONet
- PhysicsNeMo/PhysicsInformer implementation as an equation-known physics-informed reference

PINNs are not forced into the same training contract as data-only operators. Their equation access is shown explicitly.

---

## F. PDE foundation / multi-PDE models

When pretrained weights and task adapters are publicly available:

- DPOT
- Poseidon
- PDEformer / PDEformer-2
- PROSE-PDE / PROSE-FD
- UPT pretrained settings where available

Report:
- pretrained parameter count;
- pretraining data;
- zero-shot error;
- fine-tuned error;
- adaptation cost;
- inference cost.

Do not compare a pretrained foundation model to a from-scratch IPM as if total training cost were identical.

---

## G. PDE discovery

Keep the A1 law-identification benchmark as a separate table:

- strong SINDy / PDE-FIND
- WeakPDELibrary / Weak-SINDy
- WSINDy
- PDE-Net 2.0
- DeepMoD
- IPM intrinsic Jacobian/algebra audit

Metrics:
- symbolic term precision/recall/F1 when meaningful;
- coefficient error;
- differential-order support;
- held-out law error;
- noise/sparsity robustness;
- discovery time.

---

## H. Public benchmark suites

### Primary
- PDEBench

### Secondary
- PDEArena
- Representative PDE Benchmarks from CNO
- The Well representative subsets
- PINNacle equation-known problems

### Optional domain/geometry expansion
- NeuralSolver standard FNO/Geo-FNO benchmarks
- irregular-geometry tasks for GINO/GNOT/Transolver/UPT

Not every model is required to run on every dataset. Eligibility is determined before seeing test results.

---

## I. Common accuracy / physics metrics

For every compatible method:
- RMSE
- normalized RMSE
- relative L2
- rollout error vs physical horizon
- one-step error
- maximum stable horizon
- NaN/divergence rate
- Fourier-band error
- gradient/jet error where meaningful
- conserved-variable drift
- mass/momentum/energy drift where applicable
- PDE residual when the governing equation is known
- shock/front position error where applicable
- phase error for waves/advection
- grid-transfer error
- dt-transfer error
- parameter OOD
- IC/BC OOD
- 1%, 3% and task-dependent observation noise
- sparse-observation robustness

Use 5 seeds for final headline experiments unless the external pretrained model is deterministic and prohibitively expensive; exceptions must be documented.

---

## J. Speed and cost metrics

### Runtime decomposition

For IPM:
- observation/jet lift
- intrinsic law / algebra
- compiler
- one physical step
- full rollout

For neural models:
- model forward
- autoregressive state update
- one physical step
- full rollout

For numerical solvers:
- spatial operator
- time step / nonlinear solve
- adaptive substeps
- full physical horizon

### Headline speed metrics
- batch-1 latency
- batch-16 throughput
- end-to-end physical-step latency
- grid-points / second
- full-horizon wall time
- real-time factor:
  [
  mathrm{RTF}=
  rac{	ext{simulated physical time}}{	ext{wall time}}
  ]
- speedup vs matched-accuracy numerical solver
- speedup vs neural operator

### Cost / footprint
- trainable parameters
- checkpoint bytes
- peak inference VRAM
- peak training VRAM
- FLOPs/MACs where meaningful
- training wall time
- GPU-hours
- number of training trajectories
- data-generation cost
- compilation/calibration cost
- energy estimate only when measurement is reliable

---

## K. Matched-error benchmarking

A central paper plot will not compare speed at arbitrary configurations.

For each method construct the curve:

[
	ext{error}
quad	ext{vs}quad
	ext{wall-time}.
]

For numerical methods vary:
- grid resolution;
- time step/tolerance;
- solver order.

For neural methods vary:
- model size where official variants exist;
- integrator/rollout operating point where legitimate.

Report:
- fastest method at fixed error targets;
- lowest error at fixed latency budgets;
- Pareto frontier.

This directly answers:
**how fast and how cheap can IPM be for a specified physical-quality target?**

---

## L. Amortization / break-even analysis

Numerical solvers usually have no training cost.

Learned solvers have up-front training cost.

Therefore report total cost after M simulations:

[
C_{mathrm{learned}}(M)
=
C_{mathrm{train}}
+
M C_{mathrm{infer}},
]

[
C_{mathrm{numerical}}(M)
=
M C_{mathrm{solve}}.
]

Compute the break-even simulation count:

[
M^*
=
rac{C_{mathrm{train}}}
{C_{mathrm{solve}}-C_{mathrm{infer}}}.
]

For IPM also report a second number where the intrinsic law is reused across resolutions/time-step choices.

This is essential for digital-twin and repeated-simulation claims.

---

## M. Fairness protocol

Three neural comparison regimes:

1. **capacity matched**
2. **compute/training-budget matched**
3. **best-practice native configuration**

In addition, information access is always shown:
- PDE equation known?
- coefficient known?
- training trajectories?
- pretraining?
- history length?
- test-time calibration?

No single scalar score may hide these differences.

---

## N. Main paper presentation

Recommended headline figures:

1. **Accuracy vs end-to-end physical-step latency**
2. **Error vs full-horizon wall time**
3. **Error vs parameter count**
4. **Error vs peak VRAM**
5. **Matched-error speedup vs numerical solvers**
6. **Real-time factor vs grid size**
7. **Training/amortized break-even cost**
8. **Physical reliability / invariant drift**
9. **Resolution and dt transfer**
10. **Intrinsic-law interpretability / recovered differential structure**

The central claim must be supported by a Pareto frontier, not a handpicked single baseline.

---

## O. Benchmark execution order

### B0 — Infrastructure qualification
- standardized timing harness
- numerical-solver reference implementations
- PDEArena/NeuralOperator/PINNacle adapters
- hardware/timing reproducibility

### B1 — 1D canonical PDE suite
- Advection
- Heat
- Burgers
- Allen-Cahn
- KdV / Wave where model contract supports them

### B2 — PDEBench broader suite
- multiple parameters
- 1D/2D tasks

### B3 — PDEArena / CNO representative benchmarks

### B4 — foundation models / pretrained comparison

### B5 — numerical matched-error and amortization study

A paper benchmark begins only after the IPM core reaches a stable qualification point. Negative results are retained.
