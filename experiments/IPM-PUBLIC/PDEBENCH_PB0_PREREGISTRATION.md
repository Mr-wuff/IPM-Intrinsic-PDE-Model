# IPM-PB0 — PDEBench Official Evaluator Qualification

## Purpose

This experiment is the first public-benchmark-first evaluation of frozen IPM-v1.

It does **not** retrain any competing baseline.

It uses the official PDEBench repository, official PDEBench data contract, and official `metric_func` implementation at runtime.

Primary goal:

> Verify that frozen IPM-v1 can be inserted into the official PDEBench forward-evaluation contract without modifying PDEBench metrics or changing the IPM architecture.

## Official benchmark source

PDEBench repository:
`pdebench/PDEBench`

Pinned commit:
`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

The official repository currently documents compatibility of core forward-model components with newer PyTorch/Python environments while retaining the original benchmark interfaces.

The official metric implementation is imported directly from the cloned PDEBench source at runtime. No copy of PDEBench metric code is committed into the IPM repository.

## Official 1-D protocol

For both Advection and Burgers, use the official PDEBench configuration values:

- `reduced_resolution = 4`
- `reduced_resolution_t = 5`
- `initial_step = 10`
- `t_train = 200`

Official benchmark datasets:
- `1D_Advection_Sols_beta1.0.hdf5`
- `1D_Burgers_Sols_Nu0.01.hdf5`

The official forward script explicitly includes these exact files for FNO/U-Net/PINN.

## Frozen IPM entry

Use frozen IPM-v1 programs from the repository:
- seeds 101 / 202 / 303
- no retraining
- no benchmark-specific calibration
- no use of official test data for fitting

This entry is therefore labeled:

`IPM-v1 frozen / historical-low-data`

It is **not** claimed to have used the same training-data budget as the official PDEBench pretrained baselines.

## Temporal contract

After official temporal reduction by factor 5, the physical step becomes:

[
Delta t_{m PB}=5Delta t_{m raw}.
]

IPM uses its frozen learned characteristic with the official reduced temporal step.

For each test trajectory:
- the first 10 reduced-time snapshots are copied as the benchmark initial context;
- the final context state is used as the IPM initial state;
- IPM autoregresses over all remaining reduced-time snapshots.

This preserves the official output tensor contract expected by PDEBench.

## Official metrics

Call PDEBench's pinned official `metric_func` directly.

Report:
- RMSE
- normalized RMSE
- conserved-variable error
- maximum error
- boundary RMSE
- Fourier low/mid/high error

Use official defaults:
- iLow = 4
- iHigh = 12
- initial_step = 10

No locally defined replacement metric is allowed in the headline table.

## Internal cross-check

A local independently implemented RMSE/nRMSE calculation may be exported only as an audit.

It must agree numerically with the corresponding official metric to within floating-point tolerance.

## Seeds

Evaluate frozen IPM seeds:
- 101
- 202
- 303

Report seed mean/std.

## Runtime

Runtime is secondary in PB0.

Record:
- eager full official-horizon wall time
- CUDA-Graph full-horizon wall time when capturable
- peak VRAM

Do not compare these timings to published PDEBench baseline timings unless hardware/runtime contracts match.

## Gates

PB0-0 pinned IPM and PDEBench source provenance verified.

PB0-1 official PDEBench data MD5s verified.

PB0-2 official spatial and temporal reductions reproduce N=256 and the expected reduced time axis.

PB0-3 all six IPM task x seed trajectories are finite over the full official benchmark horizon.

PB0-4 official PDEBench metric_func returns finite RMSE/nRMSE/CSV/Max/BD/Fourier metrics for all six runs.

PB0-5 local RMSE/nRMSE audit agrees with official outputs within 1e-6 relative tolerance.

PB0-6 complete seed-level and mean/std public-benchmark tables export.

Decision:
- **PDEBENCH_PB0_PASS** if PB0-0..PB0-6 all pass.
- **PDEBENCH_PB0_FAIL** otherwise.

## Next public benchmark stage

PB1 will use:
- official PDEBench pretrained FNO
- official PDEBench pretrained U-Net
- official PDEBench pretrained PINN

downloaded from the official DaRUS pretrained-model release and evaluated through the same pinned PDEBench code.

The purpose is to avoid retraining these baselines ourselves.

## Broader public-benchmark roadmap

After PDEBench:
1. Representative PDE Benchmarks / CNO on compatible tasks;
2. PDEArena after a separately validated 2-D / multifield IPM extension;
3. The Well after multidimensional/multifield IPM is frozen.
