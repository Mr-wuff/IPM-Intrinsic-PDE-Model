# IPM-A2-Q3 Frozen Run

Notebook:
`IPM_A2_Q3_Intrinsic_Principal_Flow_Compiler_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`8f23bd5eec0552c6842053032c4c103c17d920ee40fc6d794e4010999dcaa290`

Frozen Protocol SHA256:
`4017038399c5ed015d1ae94d888b08513638047789c5bb03534576ecc5185281`

Required parent:
- `IPM_A2_Q2_RESULTS.zip`
- expected SHA256:
  `23f7af45c0318992b6ae2fd6570a06a04ddd06c258463aaff9e9e3d9f0020b77`

No network retraining is performed in Q3.

Formal mechanism:
- frozen 35-parameter Q2 IDTC
- algebra degree projection D1/D2/D3
- training-pool-only degree calibration
- principal coefficients from dQ/da1 and dQ/da2
- semi-Lagrangian transport
- exponential diffusion
- residual source correction
- official test split used only after selection is frozen
