# IPM-A2-Q0 — PDEBench + Official NeuralOperator FNO Qualification

## Purpose

A1 equation-discovery benchmarking is closed.

A2-Q0 is a public-data/interface qualification before expensive public benchmark training.

It uses official PDEBench HDF5 data and the official NeuralOperator FNO implementation.

No claim from Q0 is used as a final paper benchmark result unless the data/schema/baseline qualification gates pass.

## Official external sources

PDEBench repository:
- pdebench/PDEBench

NeuralOperator repository/package:
- neuraloperator/neuraloperator
- neuraloperator==2.0.0

## Public datasets

Q0 uses two canonical 1D periodic PDEBench datasets:

1. Advection
   - file: 1D_Advection_Sols_beta1.0.hdf5
   - DaRUS datafile: 255675
   - official MD5: 1fe41923a4123db55bf4e89bea32e142

2. Burgers
   - file: 1D_Burgers_Sols_Nu0.01.hdf5
   - DaRUS datafile: 281363
   - official MD5: e6d9a4f62baf9a29121a816b919e2770

The notebook downloads only these two files with resume support.

## Split contract

Follow PDEBench FNODatasetSingle split convention:
- first 10% of samples: test
- remaining 90%: training pool

Q0 uses deterministic subsets of these pools for qualification.

## Models

### IPM-Public
Frozen IPM mathematical core:
- observed field -> raw/adaptive holonomic jet
- local characteristic Q_theta(j^3 u)
- continuous-time master-field integration
- no explicit PDE equation is supplied

This is newly trained on the public trajectories; A0 checkpoints are not reused because the public data distribution/domain differs.

### NeuralOperator-FNO
Official:
`from neuralop.models import FNO`

PDEBench-style autoregressive contract:
- 10 previous time fields as input channels
- predict the next field
- recursively rollout

This deliberately gives FNO temporal history while IPM uses the current field only.

## Qualification training

Q0 is not the final public-data run.

For each dataset:
- deterministic subset <= 256 training trajectories
- <= 64 test trajectories
- one seed for architecture/data qualification
- bounded pilot epochs/updates

A2-FULL is blocked unless Q0 passes.

## Metrics

- one-step Rel-L2
- autoregressive rollout Rel-L2 vs horizon
- RMSE / nRMSE
- conservation-variable error
- physical Fourier-band error
- N/2 and N/4 downsampled resolution transfer
- 1% observation-noise stress
- parameter count
- training wall time
- peak training/inference VRAM
- per-step inference latency

## Qualification gates

Q0-0 official dataset MD5s match.
Q0-1 HDF5 schema is valid: tensor, x-coordinate, t-coordinate.
Q0-2 official NeuralOperator FNO imports and passes finite forward/backward smoke.
Q0-3 IPM passes finite forward/backward smoke on the same public batches.
Q0-4 both methods reduce pilot validation loss from initialization.
Q0-5 both methods complete finite rollout on Advection and Burgers.
Q0-6 public-data metrics and efficiency tables export successfully.

Decision:
- A2_Q0_PASS
- A2_Q0_FAIL

No method needs to beat the other for qualification.

## Next stage

If Q0 passes, A2-FULL will expand to:
- multiple PDEBench Advection coefficients;
- multiple Burgers viscosities;
- official NeuralOperator FNO;
- PDEBench U-Net reference implementation where license/runtime permits;
- multi-seed train/test reporting;
- full PDEBench metric suite;
- matched and native-contract efficiency tables.
