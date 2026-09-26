# IPM-PDEBench-PB1-Q8-FIX3-FIX2 Frozen Run Record

Experiment:
`IPM-PDEBENCH-PB1-Q8-FIX3-FIX2`

Notebook:
`IPM_PDEBench_PB1_Q8_FIX3_FIX2_Weak_Temporal_TestFunction_Contract_Attribution_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`8114ae8ccf516dc3a45b79c50356fa09aeefe493bfbbf082518bcc77ebe3038a`

Protocol SHA256:
`6f1bac5bcfddb6bb153c6e8ea8e320d27d97bb35d2e8cb1de26bde85032adf97`

Pinned repository commit:
`7775ed31bde132917d619c82dc83b5bd538148be`

Policy:
- official first 1,000 epsilon=0.001 trajectories remain sealed;
- candidate selection uses validation integral residual and coefficient stability only;
- known Burgers coefficients are reporting-only;
- final internal confirm uses training tail 8448:9000;
- no architecture transition is authorized in this attribution run;
- no 500-epoch training.
