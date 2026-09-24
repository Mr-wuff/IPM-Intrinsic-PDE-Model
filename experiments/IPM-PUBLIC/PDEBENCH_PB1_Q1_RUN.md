# IPM-PDEBench-PB1-Q1 Run Record

Experiment:
`IPM-PDEBench-PB1-Q1 — Standard-Data / Same-Scale Fairness Benchmark`

Notebook:
`IPM_PDEBench_PB1_Q1_StandardData_SameScale_Fairness_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`c2d96c686598ece0b832d498133cc77c4a15c2470f823e35339540f90df01afc`

Protocol SHA256:
`8504bfb85b9e65303070a71dd18d2dac0e5d2073dc37914243a84125be293692`

Pinned IPM source:
`dc0032c5dbdd954b44a6870427212c5905ceda7b`

Pinned PDEBench source:
`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

## Formal fairness contract

For each PDE and seed:
- official 90% PDEBench training split;
- spatial reduction 4;
- temporal reduction 5;
- batch size 50;
- 500 epochs;
- 180 trajectory batches/epoch when N_train=9000;
- 90,000 optimizer updates;
- 4,500,000 trajectory exposures.

Seeds:
- 101
- 202
- 303

Tasks:
- Advection beta=1.0
- Burgers nu=0.01

## Training policy

Only IPM is trained.

Official PDEBench FNO and U-Net are loaded from the official DaRUS pretrained release using the exact target checkpoint filenames.

A 5-epoch / 1000-trajectory pilot gate must pass for both tasks before formal training starts.

Formal IPM checkpoints are saved every 25 epochs to an external deterministic resume directory so interrupted local WSL/Jupyter runs can continue without restarting.

## Scientific boundary

The schedule matches raw data availability, split, reduction, batch size, epoch count and nominal optimizer-update count.

It does not claim identical FLOPs or identical internal loss geometry. Official FNO/U-Net use autoregressive 10-step-context learning, while IPM uses the frozen trajectory-only Simpson-integral characteristic objective.
