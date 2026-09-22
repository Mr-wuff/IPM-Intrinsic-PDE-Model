# IPM-A1-FIX1 Run

Notebook:
`IPM_A1_FIX1_WeakSINDy_Qualification_LeakageFree_Audit_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`23fecb72a3d3dbd6c9d4833faff3c7f34f0c5bd1d3400ad49313cbea406668df`

Frozen protocol SHA256:
`6741d1afedf238fb3b20a271d84848a6c99d676cadf4d332f2e1667143922d66`

Purpose:
- qualify WeakPDELibrary on training-side data before formal comparison;
- allow strong-form PySINDy its own training-side qualification;
- remove clean-state leakage from noisy IPM coefficient extraction;
- separate symbolic term support from IPM differential-order support;
- reuse the 50 frozen A0 IPM checkpoints with no retraining.

Required input:
- `IPM_A0_RESULTS.zip`
- `IPM_A0_RESULTS.zip.sha256` recommended.

Outputs:
- `IPM_A1_FIX1_RESULTS.zip`
- `IPM_A1_FIX1_RESULTS.zip.sha256`
