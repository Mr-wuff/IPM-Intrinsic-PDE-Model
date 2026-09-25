# IPM-PDEBench-PB1-Q7-FIX1 Frozen Run Record

Notebook:
`IPM_PDEBench_PB1_Q7_FIX1_Differential_Integral_Consistent_DCC_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`5cfadd0dbb7bdeb4e777eb98608af6fc95ff8dc978749494aa102e74fb33a36c`

Embedded protocol SHA256:

`1e8f1230292c2beb1e9dd14bc5786d397498ec8e5de8eb71b2527f6d65854459`

Pinned repository commit:

`c5eab689eaa92892e2488e6b4e86423ce118aa32`

Manual uploads: none.

Official first 1,000 PDEBench test trajectories are never loaded.

The run compares:
- INT-DCC35 control
- SEC-DCC35 diagnostic
- DIC-DCC35 candidate
- DIC-P13 exact principal ablation

The only architecture change under qualification is the trajectory-only differential-integral identification contract plus mathematically consistent DCC35/P13 basis relation.

No 500-epoch training is authorized by this run.
