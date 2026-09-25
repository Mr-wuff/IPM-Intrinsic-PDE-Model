# IPM-PDEBench-PB1-Q8-FIX3 Frozen Run Record

Experiment:

`IPM-PDEBENCH-PB1-Q8-FIX3`

Notebook:

`IPM_PDEBench_PB1_Q8_FIX3_Weak_Conservative_Flux_Core_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`9dde5ebb1e7e45586fc641189f9151b4bf7d657496c371aa0703bf944a62d51f`

Protocol SHA256:

`f431c9a19e8306dbe334fa2a3a61904e2be52e88ec15e6c0cdd2ae427235310e`

Frozen strong-law SHA256:

`bab3a6073944144784d81649f53ee71f5ab1bea8597d71ac0dbf3772c9613994`

Pinned repository commit used by the notebook:

`3fe42d12bdf9a35faee43a60b9511891a0ac842c`

Policy:
- official first 1,000 epsilon=0.001 trajectories remain sealed;
- previously unused training-block rows are used for the weak-law folds/validation/confirm;
- WCFC-5 is fit from trajectory-only Fourier weak differential + Simpson-integral equations;
- known Burgers coefficients are reporting-only;
- FV2-MC adaptive-CFL runtime is frozen from Q8-FIX2-FIX1;
- no 500-epoch training;
- no threshold changes after result observation.
