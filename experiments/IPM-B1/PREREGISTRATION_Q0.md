# IPM-B1-Q0 — Neural Surrogate / Neural Operator Adapter Qualification

## Purpose

B0-FIX1 closed the known-equation classical-solver harness and validated the repository-native workflow.

Before any expensive formal neural benchmark, B1-Q0 qualifies the actual software adapters, tensor contracts, parameter counts, one-step optimization behavior, and inference timing for the first 1-D neural baseline suite.

This is a **mechanism / infrastructure qualification**, not a paper leaderboard.

No IPM-v1 mathematics is modified.

## Frozen IPM

IPM-v1 is imported from the repository package and remains frozen:
- Advection beta=1: T program
- Burgers nu=0.01: T+D+S program
- no refitting
- no test-set adaptation

## External source freezes

### NeuralOperator
Official repository:
`neuraloperator/neuraloperator`

Pinned source commit:
`00b7d86f8d74ff0af55da53eb585fe26df9c71f0`

Architectures used in Q0:
- FNO
- TFNO
- UNO

### DeepXDE
Official repository:
`lululxvi/deepxde`

Pinned source commit:
`99b6620386d18cefb1549dddb7b7fe468cfad607`

Architecture:
- DeepONetCartesianProd through a thin 1-D adapter

## Controlled surrogates

Repository-native:
- ResNet1D
- UNet1D

These are controlled conventional neural surrogates, not claimed as official external reproductions.

## Why this is staged

The final B1 family is broader than this Q0 set.

Later B1 stages will add task-compatible official implementations for:
- CNO
- WNO
- OFormer
- GNOT
- Galerkin/Fourier Transformer
- additional NeuralOperator models such as LocalNO / GINO where the data geometry is appropriate

CNO/GNOT/OFormer/GINO are not forced into this 1-D regular-grid preflight when their native contracts target different geometries or dimensionalities. They remain mandatory candidates for the later comprehensive benchmark on compatible tasks.

## Data contract

Official PDEBench:
- 1-D Advection beta=1.0
- 1-D Burgers nu=0.01

Q0 uses only the training pool for optimization qualification.

Input:
[
u_t(x)
]

Target:
[
u_{t+Delta t}(x)
]

No future state is supplied as an input.

Formal public first-10% test trajectories are used only for a final one-step smoke evaluation after the optimizer protocol is frozen.

## Models

1. ResNet1D
2. UNet1D
3. official FNO
4. official TFNO
5. official UNO
6. official DeepONet

## Qualification budget

For each model and PDE:
- seed = 202
- 128 training trajectories
- deterministic sampled time pairs
- batch size 16
- AdamW
- 128 optimizer updates
- same direct one-step MSE objective

Q0 is intentionally short. It is only intended to answer whether formal training is worth launching.

## Metrics

For each model/task:
- construction success
- forward shape
- finite forward
- trainable parameter count
- checkpoint bytes
- initial normalized one-step error
- final normalized one-step error after 128 updates
- loss reduction fraction
- peak training VRAM
- batch-1 latency
- batch-16 latency
- batch-64 latency when memory permits
- test one-step Rel-L2 after the short qualification run
- NaN/OOM/error diagnostics

## Grid-contract probe

Without retraining:
- N=128
- N=256
- N=512

This is only a forward/API probe.

A model is marked:
- native variable-grid
- fixed-branch-grid
- unsupported

No quality claim is made from this probe.

## Gates

Q0-0 repository/package source hashes and PDEBench MD5s match.

Q0-1 all six architectures construct successfully.

Q0-2 all six architectures produce finite [B,1,N] output at N=256.

Q0-3 all 12 model x PDE short runs finish without OOM/non-finite loss.

Q0-4 at least 10/12 runs reduce normalized training error by >=10%.

Q0-5 all six models export parameter count, latency, VRAM and checkpoint-size records.

Q0-6 official FNO/TFNO/UNO provenance is NeuralOperator pinned commit, and DeepONet provenance is DeepXDE pinned commit.

Decision:
- **B1_Q0_PASS** if Q0-0..Q0-3, Q0-5, Q0-6 pass and Q0-4 passes.
- **B1_Q0_CONDITIONAL** if infrastructure gates pass but 8-9/12 short runs meet the 10% reduction threshold.
- **B1_Q0_FAIL** otherwise.

## Transition

If Q0 passes/conditional:
- B1-Q1 launches matched formal 3-seed training on the qualified suite.
- B1-Q2 adds additional official operator families / task-compatible adapters.
- B1-FULL produces the neural-model Pareto frontier.

No model is removed from the final benchmark merely because it loses Q0 performance; Q0 only removes technically invalid or incompatible adapters.
