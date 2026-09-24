# IPM-PDEBench-PB1-Q5 — Formal Standard-Data Native-Closure 3-Seed Run

## Authorization

PB1-Q4 formally authorized one final full-scale standard-data run and selected:

`T1_S111_NATIVE_LOCAL`

PB1-Q5 is not an architecture search. The training/closure contract is frozen before any official test access.

## Tasks

Official PDEBench:
- 1-D Advection beta=1
- 1-D Burgers nu=0.01

Pinned PDEBench source:

`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

## Formal data and optimization budget

For every task and seed:
- official training block: 9,000 trajectories;
- official held-out test block: 1,000 trajectories;
- spatial reduction: 4;
- native raw-time identification;
- strides: (1,1,1);
- epochs: 500;
- batch size: 50;
- 180 trajectory batches/epoch;
- 90,000 optimizer updates;
- 4,500,000 trajectory exposures;
- Adam lr 1e-3;
- weight decay 1e-4;
- StepLR step 100, gamma 0.5;
- seeds: 101, 202, 303.

No exact PDE RHS, target PDE coefficient, or equation-specific pruning is used.

## Frozen closure contract

After each 500-epoch IDTC fit:
1. project to dense RTDS principal polynomial roles;
2. fit four role gains to training-block central secants;
3. refine only g_R, g_T, g_D, g_S through the exact differentiable native compiled flow.

The PB1-Q4 refinement contract is unchanged:
- 160 updates;
- 16 calibration trajectories/update;
- 4-step native rollout;
- lr 0.02;
- secant-preservation weight 0.25;
- gain-prior weight 0.002;
- absolute gain clip 6.

Training-block safety diagnostics are recorded but do not select or drop seeds.

## Official-test firewall

All six task/seed compiled programs must be frozen before the notebook loads any official test trajectory.

On the official test:
- temporal reduction = 5;
- initial context = 10 frames;
- future horizon = 31 autoregressive native steps;
- official pinned PDEBench `metric_func` is used;
- all three seeds are reported;
- no best-seed selection is permitted.

## Runtime and integrity

The notebook must:
- validate differentiable-flow / repository-runtime parity <= 2e-6;
- require finite/non-zero gain gradients;
- checkpoint every 25 epochs and support exact resume;
- record wall time and peak VRAM;
- report same-hardware IPM full-horizon latency at batch 1/16/64;
- independently audit official RMSE/nRMSE;
- package detached SHA256 manifests.

## Interpretation

PB1-Q5 determines the paper-eligible standard-data IPM accuracy distribution after the training/closure contract was fixed entirely from training-block mechanism experiments.

No further Advection/Burgers training-contract adjustment is allowed after official test results are observed.
