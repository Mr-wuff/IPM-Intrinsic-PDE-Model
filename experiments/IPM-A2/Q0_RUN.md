# IPM-A2-Q0 Run Record

## Experiment

IPM-A2-Q0 — PDEBench + Official NeuralOperator FNO Qualification

Notebook:
`IPM_A2_Q0_PDEBench_NeuralOperator_FNO_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`8a28a5dba0e95985cbc08139a36291451b714c8c17a2d8178bd5757cf94631f3`

Frozen protocol SHA256:
`d04560b17b2647cab1ee9feefda47a0a9bc8322b1e583d2fd696fe40abe99da7`

## Public data

Official PDEBench files downloaded directly from DaRUS:

- Advection beta=1.0
  - `1D_Advection_Sols_beta1.0.hdf5`
  - datafile 255675
  - MD5 `1fe41923a4123db55bf4e89bea32e142`

- Burgers nu=0.01
  - `1D_Burgers_Sols_Nu0.01.hdf5`
  - datafile 281363
  - MD5 `e6d9a4f62baf9a29121a816b919e2770`

## Baselines

Official NeuralOperator package:
- `neuraloperator==2.0.0`
- `from neuralop.models import FNO`

IPM variants:
- IPMRaw
- IPMAdaptive

## Qualification scale

- spatial stride 4
- 128 training trajectories
- 32 official-test trajectories
- 600 optimizer updates/model
- batch size 16
- FNO temporal history 10
- rollout 40 public time steps

## Gate policy

This is a qualification run, not a winner-gated benchmark.

A2-FULL advances only if:
- official dataset MD5/schema pass;
- official FNO and IPM public-batch forward/backward pass;
- both reduce pilot loss;
- both produce finite public rollouts;
- metrics/efficiency artifacts export successfully.

## Outputs

Expected:
- `IPM_A2_Q0_RESULTS.zip`
- `IPM_A2_Q0_RESULTS.zip.sha256`

Large PDEBench HDF5 files are intentionally excluded from result packaging.
