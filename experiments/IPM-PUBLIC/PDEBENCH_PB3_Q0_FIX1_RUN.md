# PB3-Q0-FIX1 Frozen Run Record

Experiment:

`IPM-PDEBENCH-PB3-Q0-FIX1`

Preregistration commit:

`231ff9c32051b6a52970070a47399b0c21d342ce`

Frozen notebook:

`IPM_PDEBench_PB3_Q0_FIX1_RobustTemporalGate_2D_Coupled_ReactionDiffusion_PDENative_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`62bf65628ce652daf173211b045f34b8222ec3b225bd05ecddd829ddcbd3d942`

Protocol SHA256:

`174371484e61d71cc9f8ef64ac0ba18b1a0bbed780a619a37c387de63157dee1`

Formal change from PB3-Q0:

Only the temporal generator-validity normalization is changed.

Frozen FIX1 rule:
1. curvature_ratio <= 0.40;
2. compute median signal among curvature-admissible centers;
3. retain centers with signal >= that median;
4. require at least 8;
5. if >8, full-C2D20 target-free D-optimal B=8;
6. no fallback.

All downstream discovery/compiler/official-test gates remain frozen from PB3-Q0.

Expected outputs:
- `IPM_PDEBENCH_PB3_Q0_FIX1_RESULTS.zip`
- `IPM_PDEBENCH_PB3_Q0_FIX1_RESULTS.zip.sha256`
- executed notebook.

Official last-100 seed groups remain sealed until G0-G8 all pass.
