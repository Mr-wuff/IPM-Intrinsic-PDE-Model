# PDEBench PB1-Q1 Run

Experiment:
`IPM-PDEBench-PB1-Q1 — Standard-Data / Same-Scale Fairness Benchmark`

Frozen notebook:
`IPM_PDEBench_PB1_Q1_StandardData_SameScale_Fairness_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`cd62c72d09136adda16b9eb82e9a5e4de08652c36470b7950655ffc94f3d5957`

Protocol SHA256:
`59936faab4c98cbdde14293367927ec832a4c355a5fb04ebc5c02d46b4e59b94`

Pinned IPM source commit used by the notebook:
`dc0032c5dbdd954b44a6870427212c5905ceda7b`

Pinned PDEBench source:
`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Manual input uploads:
**none**

Formal standard-data budget:
- 2 PDEs
- 3 IPM seeds
- 500 epochs
- batch 50
- 9,000 official training trajectories when the pinned datasets retain their current 10,000-trajectory shape
- 90,000 optimizer updates per task/seed
- 540,000 total formal IPM optimizer updates

The notebook first runs a 5-epoch training-only pilot and blocks the formal stage automatically if the preregistered qualification gate fails.

Formal training is deterministically resumable from 25-epoch checkpoints under `IPM_PERSIST_DIR` when configured.

No FNO/U-Net baseline retraining occurs. Exact official pretrained beta=1.0 / nu=0.01 checkpoints are used.
