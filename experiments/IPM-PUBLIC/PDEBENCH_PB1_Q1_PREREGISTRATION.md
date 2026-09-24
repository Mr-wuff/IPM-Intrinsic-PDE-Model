# IPM-PDEBench-PB1-Q1 — Standard-Data Same-Scale Fairness Benchmark

## Purpose

The user requested a stricter fairness regime: train IPM with the same public benchmark data and nominal training scale used by the official PDEBench FNO/U-Net baselines.

PB1-Q1 therefore adds a new entry:

`IPM-v1 standard-data / same-scale`

The frozen mathematical architecture is unchanged. Only the learned 35-scalar IDTC program is re-estimated from the official PDEBench training split.

This entry is reported alongside:
- frozen historical-low-data IPM-v1;
- exact official pretrained PDEBench FNO;
- exact official pretrained PDEBench U-Net;
- PINN only under its protocol-native contract if executable.

## Why there are two IPM entries

The paper must separate two different scientific questions.

### Frozen transfer track

`IPM-v1 frozen / historical-low-data`

Question:
Can an already frozen low-data IPM transfer into a third-party benchmark without benchmark-specific fitting?

### Fair standard-data track

`IPM-v1 standard-data / same-scale`

Question:
If IPM is granted the same PDEBench training data and nominal training schedule as the official operator baselines, what accuracy-efficiency point does the architecture achieve?

Neither entry replaces the other.

## Official data contract

Pinned PDEBench source:
`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Tasks:
- 1-D Advection beta=1.0
- 1-D Burgers nu=0.01

Official FNO/U-Net settings:
- reduced_resolution = 4
- reduced_resolution_t = 5
- initial_step = 10
- batch_size = 50
- epochs = 500
- test_ratio = 0.1

For the single-file loader, the first 10% is the official held-out split and the remaining 90% is the training split.

The current target data contain 10,000 trajectories, giving:
- 1,000 official held-out trajectories;
- 9,000 official training trajectories.

PB1-Q1 verifies these counts dynamically rather than assuming them.

## Nominal same-scale IPM budget

For each task and seed:

- train trajectories: exactly the official 90% training split;
- spatial reduction: 4;
- temporal reduction: 5;
- batch size: 50 trajectories;
- epochs: 500;
- trajectory batches per epoch: 180 when N_train=9000;
- optimizer updates: 90,000 when N_train=9000;
- optimizer: Adam;
- learning rate: 1e-3;
- weight decay: 1e-4;
- StepLR: step_size=100 epochs, gamma=0.5.

Seeds:
- 101
- 202
- 303

Thus the standard-data IPM receives the same raw training trajectories and the same nominal epoch/batch/update scale as the official FNO/U-Net recipe.

## Important fairness boundary

The per-update supervision geometry is not identical across architectures.

Official FNO/U-Net autoregress through the reduced trajectory using a 10-step input context.

IPM learns a continuous local characteristic from trajectory triplets using its frozen Simpson-integral trajectory-only objective.

PB1-Q1 therefore claims:
- **same raw data availability**
- **same train/test split**
- **same spatial/temporal reduction**
- **same batch size**
- **same epoch count**
- **same nominal optimizer-update count**

It does **not** claim identical FLOPs or identical number of scalar target terms per update.

Training wall time, peak VRAM and trajectory exposure are exported so the compute difference is visible rather than hidden.

## Frozen IPM training architecture

No new neural module is introduced.

Use:
- LocalTaylorJet(radius=4, degree=5, order=3);
- IDTC(jet_dim=4, rank2=4, rank3=2);
- 35 trainable scalars;
- trajectory-only Simpson integral residual;
- training strides 1, 2 and 4.

For every trajectory exposure in an epoch, one valid triplet is sampled for each of the three frozen strides.

No exact PDE RHS, symbolic coefficient, or equation label is given to the optimizer.

## Pilot-before-formal gate

Before the 500-epoch run, execute a cheap pilot using only the official training split:
- seed 202;
- first 1,000 official training trajectories;
- 5 epochs;
- same batch size and optimizer family.

The formal 500-epoch stage starts automatically only if both tasks satisfy:
- finite loss throughout;
- final epoch loss <= 0.8 * first epoch loss;
- learned characteristic finite on a held-out training-only diagnostic subset;
- dense compiled RTDS runtime gives a finite 8-step diagnostic rollout.

The pilot is not continued into the formal model. Formal training restarts from the frozen seed.

## Program compilation

After training, convert the IDTC polynomial into the principal normal-form role coefficients using the frozen `principal_role_coeffs` map.

For the primary standard-data result, use a **dense RTDS compiler mask**:
`RTDS`

This avoids using equation-specific prior knowledge or a hand-chosen role mask.

A separate role-contribution table is exported for interpretability.

No target-equation information is used to remove roles.

## Evaluation entries

Evaluate on the same official held-out trajectories with the official PDEBench `metric_func`:

1. IPM-v1 frozen / historical-low-data
2. IPM-v1 standard-data / dense-RTDS
3. official pretrained FNO exact target checkpoint
4. official pretrained U-Net exact target checkpoint

Exact official target checkpoints:
- Advection FNO beta=1.0
- Advection U-Net beta=1.0 PF-20
- Burgers FNO nu=0.01
- Burgers U-Net nu=0.01 PF-20

PINN is exported separately under the official PINN-native evaluation protocol because PDEBench's PINN training/evaluation contract is not the same multi-trajectory operator-learning problem.

## Official metrics

Headline public metrics come only from the pinned PDEBench `metric_func`:
- RMSE
- nRMSE
- conserved-variable error
- maximum error
- boundary RMSE
- Fourier low/mid/high error

## Runtime and deployment cost

On the same GPU/process:
- batch 1 / 16 / 64;
- full official future horizon;
- eager timing for all executable entries;
- CUDA Graph timing where numerically equivalent;
- peak inference VRAM;
- parameter/effective-scalar count;
- checkpoint/program bytes.

IPM training cost is also reported:
- formal wall time;
- peak training VRAM;
- optimizer updates;
- trajectory exposures.

## Statistical reporting

For IPM standard-data:
- seeds 101/202/303;
- mean and sample standard deviation.

Official FNO/U-Net are released single checkpoints, so no fabricated seed variance is attached to them.

The paper must not treat a single official checkpoint as a 3-seed baseline.

## Gates

PB1Q1-0 official source/data/artifact provenance and exact target checkpoint names verified.

PB1Q1-1 pilot gate passes for both PDEs before formal training.

PB1Q1-2 all six formal IPM standard-data runs complete the exact nominal 500 epochs / expected optimizer-update count without non-finite optimization.

PB1Q1-3 all six trained IDTC models compile to finite dense-RTDS programs and complete the full official horizon.

PB1Q1-4 exact target official FNO and U-Net checkpoints strictly load with no missing/unexpected keys and complete the full official horizon.

PB1Q1-5 all headline predictions are evaluated by the pinned official PDEBench metric function and return finite metrics.

PB1Q1-6 train split, batch size, epoch count, optimizer-update count, trajectory exposures, wall time and VRAM audits export.

PB1Q1-7 official-vs-local metric audit and result manifest integrity pass.

Decision:
- **PDEBENCH_PB1_Q1_COMPLETE** if PB1Q1-0..PB1Q1-7 pass.
- **PDEBENCH_PB1_Q1_INCOMPLETE** otherwise.

No accuracy winner is part of the completion gate.
