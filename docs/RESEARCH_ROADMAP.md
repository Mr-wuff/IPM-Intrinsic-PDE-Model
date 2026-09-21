# IPM Research Roadmap

## Project
**Model:** Intrinsic PDE Model (IPM)  
**Paper:** *Make PDE integrated into model native*

## Scientific boundary
The paper is exclusively about IPM. No CIDM mechanism is part of the architecture, experiments, claims, or ablations.

## Core architectural claim to test
A PDE should not merely supervise or condition a generic network. IPM should internalize differential structure as part of the model's admissible state and transition law.

A candidate formalization is built around:
- jet-state representation;
- holonomic/integrable state constraints;
- total-derivative/prolongation consistency;
- intrinsic infinitesimal evolution;
- architecture-level conservation/symmetry modules where applicable;
- continuous-time integration separated from the learned generator.

This formalization is provisional until the theory qualification stage passes.

## Stage T0 — Novelty and mathematical specification
Deliverables:
- exact IPM mathematical definition;
- relation to jet bundles, contact structure, prolongation, differential operators;
- explicit distinction from PINN/PINO, FNO/DeepONet, PDE-Net, neural ODEs, symbolic PDE encoders, and PDE foundation models;
- falsifiable theorem/proposition targets;
- minimal counterexamples showing what 'derivative features' do not guarantee.

Gate:
No training begins until the architecture can be written without relying on 'PDE residual loss makes it physical' as the defining mechanism.

## Stage T1 — Minimal mechanism qualification
PDEs:
- heat/diffusion;
- linear advection;
- viscous Burgers;
- wave equation;
- Allen-Cahn/reaction-diffusion.

Required matched baselines:
- field-state network;
- derivative-feature network;
- Neural ODE / continuous-time field model;
- FNO;
- DeepONet where suitable;
- PINN/PINO where the task definition is fair;
- PDE-Net-style differential-operator baseline when relevant.

Tests:
- one-step;
- rollout;
- derivative-state consistency;
- PDE residual (evaluation metric, not the sole defining loss);
- coefficient interpolation/extrapolation;
- dt shift;
- grid shift;
- initial-condition shift;
- noise robustness;
- data efficiency.

Gate:
IPM must beat or match strong baselines on a meaningful subset while showing a unique structural benefit attributable to intrinsic state/evolution constraints.

## Stage T2 — Architecture ablation and causal attribution
Ablate independently:
- jet order k;
- state consistency;
- evolution/prolongation consistency;
- projection/retraction to admissible state;
- explicit vs learned differential operators;
- integrator;
- conservation module;
- symmetry/equivariance module;
- parameter sharing across derivative orders.

Use parameter/FLOP/training-budget matched controls.

Gate:
The claimed 'intrinsic PDE' mechanism must survive capacity-matched controls.

## Stage T3 — Generalization stress tests
Dimensions of generalization:
- unseen coefficients;
- unseen forcing;
- unseen boundary/initial conditions;
- unseen temporal resolution;
- unseen spatial resolution;
- irregular grids / geometry;
- unseen equation combinations;
- longer time horizon than training.

Report failure boundaries, not only mean scores.

## Stage T4 — 2-D and hard-regime physics
Candidate systems:
- 2-D reaction-diffusion;
- 2-D shallow-water;
- incompressible Navier-Stokes;
- compressible flow / shock-containing conservation laws only after smooth-regime qualification.

Tests include conservation error, spectrum error, phase error, shock/front position, invariant drift, and long-rollout stability.

## Stage T5 — Multi-PDE generalist IPM
Train one IPM across heterogeneous PDE families.

Questions:
- Does a shared intrinsic differential state support transfer?
- Is a symbolic PDE description required?
- Can IPM adapt to a new PDE with few samples?
- Can components/generalized operators recombine compositionally?

Compare with PDE foundation models such as PDEformer/Poseidon-class systems using fair compute/data settings.

## Stage T6 — Paper-scale benchmark
Benchmark suites:
- PDEBench;
- The Well subsets where suitable;
- task-specific high-quality reference solvers;
- controlled synthetic suite for exact attribution.

Primary metrics:
- relative L2 / normalized RMSE;
- long-rollout error vs physical time;
- conservation/invariant drift;
- spectrum/gradient error;
- residual and consistency defect;
- dt/grid/OOD degradation ratio;
- data efficiency;
- inference latency and throughput;
- memory and FLOPs;
- calibration if probabilistic variants are introduced.

Statistics:
- >= 5 seeds for core claims;
- confidence intervals;
- paired significance tests/effect sizes where appropriate;
- no cherry-picked trajectories.

## Stage T7 — Theory + paper freeze
Paper evidence should support four layers:
1. mathematical novelty;
2. mechanistic causality;
3. empirical superiority/competitiveness;
4. generalization and efficiency.

No universal-PDE claim unless empirically and theoretically justified.

## Git workflow
- `main`: only frozen research artifacts.
- `exp/<stage>-<name>`: each experiment.
- Each formal experiment records: hypothesis, gate, config, code, results, report, manifest, commit SHA.
- Failed experiments remain reproducible but are clearly marked failed; invalid pre-freeze prototypes are not used as paper evidence.

## Planned repository layout
```
ipm/
  model/
  geometry/
  operators/
  integrators/
  constraints/
benchmarks/
experiments/
configs/
tests/
docs/
paper/
scripts/
```
