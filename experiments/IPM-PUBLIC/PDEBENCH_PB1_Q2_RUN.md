# IPM-PDEBench-PB1-Q2 Frozen Run Record

Notebook:
`IPM_PDEBench_PB1_Q2_Temporal_Identification_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`5e93a488d31fc9d6e7f8f670b34c04aaa35e0b5d8abeb60f45313e7064e1a4cb`

Protocol SHA256:
`bbfd6eb0cf155ed796953cccc485dad20068dc3df1b45c7113f7ac772af72fbc`

Pinned repository commit:
`3342f699639374177c6c287d254c32cb77bf91b5`

Purpose:
- diagnose PB1-Q1 standard-data training failure before any new long run;
- compare temporally reduced vs architecture-native local sampling;
- use training-only validation for selection;
- block any 500-epoch continuation unless a preregistered native-time candidate passes.

Manual parent-result uploads required: **none**.

Official held-out PDEBench test data are not used to select the next training contract.
