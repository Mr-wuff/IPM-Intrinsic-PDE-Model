# IPM-PDEBench-PB1-Q8-FIX2-FIX1 — Frozen Run Record

Experiment:

`IPM-PDEBENCH-PB1-Q8-FIX2-FIX1`

Notebook:

`IPM_PDEBench_PB1_Q8_FIX2_FIX1_CFL_Aware_Conservative_Native_Flow_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`0213b7f817d32474e012d1dc836fd4f118de3c259e6b83e51c632295acb23b33`

Protocol SHA256:

`26d4766873a8a87a74e31c263ca4e09e45d106cd38323e033f5a08bfed3ce724`

Embedded three-law SHA256:

`bab3a6073944144784d81649f53ee71f5ab1bea8597d71ac0dbf3772c9613994`

Pinned preregistration commit:

`a1397c5c660897b24b104b189ce3f4f3ec09ac3a`

Frozen numerical policy:
- official test remains sealed;
- DIC-DCC35 law identification unchanged;
- conservative flux compiler unchanged from Q8-FIX2;
- adaptive CFL target = 0.25;
- no CFL search;
- maximum 4096 conservative substeps per official interval;
- Q8-FIX2 accuracy/conservation gates retained unchanged;
- new C0 gate verifies actual CFL compliance.

The run automatically packages a ZIP, detached SHA256, manifest, runtime matrix, adaptive CFL diagnostics, latency diagnostics, programs, figures, and qualification report.
