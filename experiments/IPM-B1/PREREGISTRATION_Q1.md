# IPM-B1-Q1 — Three-Seed Matched-Update Neural Benchmark

## Purpose

B1-Q0-FIX1 qualified the first six neural surrogate/operator adapters.

B1-Q1 is the first formal neural-model benchmark against frozen IPM-v1.

No IPM-v1 mathematics, compiled coefficients, role mask, or runtime is modified.

## Primary scientific question

Under a shared trajectory-only one-step supervision regime and fixed optimizer-update budget, how do conventional neural surrogates and neural operators compare with frozen IPM-v1 in:

- 40-step rollout accuracy
- rollout stability
- corrected spectral error
- parameter/checkpoint cost
- training wall time
- peak training VRAM
- inference latency / throughput
- resolution contract
- accuracy-latency-size Pareto position

B1-Q1 is a **matched-update controlled benchmark**, not yet a best-practice hyperparameter leaderboard.

## Primary grid

Use the same PDEBench downsampled grid as B0 / frozen IPM:

- raw N = 1024
- spatial stride = 4
- formal N = 256

This avoids comparing neural models at N=1024 against an IPM result measured at N=256.

## PDE tasks

Official PDEBench:
- 1-D periodic Advection beta=1.0
- 1-D periodic Burgers nu=0.01

Test split:
- first 10% trajectories
- formal evaluation uses first 32 test trajectories

Training pool:
- first 128 trajectories immediately after the official test block

No test trajectory is used for optimization.

## Models

Controlled conventional surrogates:
1. ResNet1D
2. UNet1D

Official NeuralOperator:
3. FNO
4. TFNO
5. UNO

Official DeepXDE:
6. DeepONetCartesianProd

Frozen comparison:
7. IPM-v1

## External source freezes

NeuralOperator:
- repository: `neuraloperator/neuraloperator`
- commit: `00b7d86f8d74ff0af55da53eb585fe26df9c71f0`

DeepXDE:
- repository: `lululxvi/deepxde`
- commit: `99b6620386d18cefb1549dddb7b7fe468cfad607`

## Neural training protocol

Seeds:
- 101
- 202
- 303

For every neural model x PDE x seed:
- same initialization seed within the model
- same deterministic sampled trajectory/time schedule shared across all six models for that PDE/seed
- batch size = 16
- optimizer = AdamW
- learning rate = 1e-3
- weight decay = 1e-5
- updates = **1536**
- gradient clipping = 1.0
- direct normalized one-step MSE
- no early stopping
- final checkpoint only is used for formal evaluation

The common residual wrapper remains:
[
hat u_{t+Delta t}=u_t+Delta_	heta(u_t).
]

The wrapper is external and identical for all six neural baselines.

## Diagnostic nodes

At optimizer updates:
- 128
- 384
- 768
- 1536

record:
- trailing training MSE
- held-out one-step Rel-L2 on a frozen diagnostic mini-set
- 8-step diagnostic rollout on four test trajectories

Diagnostic nodes do not alter optimization and do not select the final checkpoint.

## Frozen IPM-v1 comparison

Use repository-stored frozen programs:
- seeds 101 / 202 / 303
- Advection T program
- Burgers T+D+S program

IPM receives raw physical fields and is not retrained.

The formal test contract is identical:
- state index 9 as initial condition
- predict states 10..49
- 40 physical steps
- N=256

IPM reproduction target:
- Advection mean 40-step aggregate Rel-L2 = 0.07976008455
- Burgers mean = 0.19279542069

Absolute reproduction tolerance:
[
2	imes10^{-4}.
]

## Formal accuracy metrics

For every method/PDE/seed:

1. one-step Rel-L2 at frozen time index 20
2. 40-step aggregate Rel-L2 over all 40 predicted states
3. final-state Rel-L2 at step 40
4. cumulative horizon Rel-L2 at 1 / 5 / 10 / 20 / 40
5. RMSE
6. spatial-mean drift
7. finite/non-finite status
8. corrected Fourier-band relative error:
   - low modes m <= 4
   - mid modes 4 < m <= 8
   - high modes m > 8
9. predicted/reference energy ratio in each band

The band error is:
[
E_B =
rac{|(hat u-u^*)_B|_2}
     {|u^*_B|_2+epsilon}.
]

High-band values are interpreted together with reference band energy and energy ratio.

## Formal inference timing

Timing model checkpoint:
- neural seed 202 final checkpoint
- IPM seed 202 frozen program

Batches:
- 1
- 16
- 64

For each method/PDE/batch measure:

### Eager
- one-step latency
- 40-step autoregressive horizon latency
- peak inference VRAM
- fields/s and grid-points/s

### Whole-horizon CUDA Graph
Attempt fixed-shape capture of all 40 steps.

If capture succeeds, require:
[
rac{|u_{m graph}-u_{m eager}|_2}
{|u_{m eager}|_2+epsilon}
le 2	imes10^{-6}.
]

For the primary Pareto table, use the fastest numerically equivalent backend available to each method.

No method is penalized for failed graph capture; eager remains valid.

## Training-cost accounting

For every neural model/PDE/seed:
- trainable parameters
- final checkpoint bytes
- total 1536-update wall time
- peak train VRAM
- updates/s

IPM training/discovery cost is not re-estimated in Q1 and is not mixed into matched-update training-time comparisons.

IPM contributes:
- deployment effective scalar count
- program/checkpoint bytes
- inference latency
- rollout accuracy

Historical IPM discovery cost will be handled separately in the final amortized-cost analysis.

## Statistical reporting

For neural accuracy:
- mean
- standard deviation
- seed-level raw values

For method-vs-IPM comparisons on seeds 101/202/303:
- paired differences where seed identity is aligned
- 95% bootstrap confidence interval over the six PDE x seed paired observations for the global summary
- PDE-specific three-seed differences are reported descriptively because n=3 is too small for strong inferential claims

No winner is part of the experiment gate.

## Qualification gates

Q1-0 source commits and PDEBench MD5s match.

Q1-1 all 36 neural training runs complete 1536 finite updates.

Q1-2 all diagnostic nodes and final checkpoints export.

Q1-3 all 36 formal neural rollout evaluations are finite for all 40 steps.

Q1-4 frozen IPM reproduces both parent mean errors within 2e-4.

Q1-5 all 36 neural cost records export with no missing params/checkpoint/train-time/VRAM values.

Q1-6 eager inference timing is complete for all 7 methods x 2 PDEs x 3 batches = 42 rows.

Q1-7 every accepted CUDA-Graph row satisfies <=2e-6 final-state defect against eager.

Q1-8 formal accuracy, horizon, spectral, timing, training-cost, and Pareto tables export.

Decision:
- **B1_Q1_COMPLETE** if Q1-0..Q1-8 pass.
- **B1_Q1_INCOMPLETE** otherwise.

The decision gate is infrastructure/completeness only; it does not depend on any model winning.

## Next stages

After Q1:
- B1-Q2 adds additional official operator families on compatible tasks: CNO, WNO, OFormer, GNOT, Galerkin/Fourier Transformer and other relevant operators.
- B1-FULL performs broader 5-seed / best-practice / compute-aware analysis.
- B2 covers PINN / physics-informed operator families.
