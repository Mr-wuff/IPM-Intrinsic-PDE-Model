# IPM-PDEBench-PB1-Q6 Run Record

Notebook:
`IPM_PDEBench_PB1_Q6_Burgers_Causal_Bottleneck_Audit_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`cc7a0d611195bda13c747e7e8c952ab4f9f965dfd475a946e2995aef46d12014`

Embedded executable protocol SHA256:
`cadbf36032905413e566fe83e4fe182c1655ff815fc4c61195e16251a4c10ab3`

Embedded frozen Q5 state artifact SHA256:
`7abe2862914e0a987f8afa4b8fb213391e7e5c01aba7ad830c157f8b2942d54a`

Pinned repository commit:
`4a6dc239c1d3a880cae6da74237d467f002dfdef`

PB1-Q5 source result ZIP SHA256:
`71a7c3e42726c5727584f0d9f7ffcfdbae15fb00bece443fa376c38072aae1b3`

Manual uploads:
**none**

## Purpose

PB1-Q6 is a zero-long-training causal audit of the PB1-Q5 Burgers failure.

It compares the frozen Q5 IDTC against:
- direct 16-scalar principal canonical fits;
- multiple local Taylor-jet estimators;
- a spectral-jet diagnostic upper bound;
- direct full 35-term canonical algebra;
- train-only native-flow gain refinement;
- internal 1/2/4/8/16/31-step rollout drift;
- gradient-regime characteristic errors.

The official first 1,000 PDEBench test trajectories are never loaded.

No new 500-epoch Advection/Burgers run is authorized by this stage itself.

Return the result ZIP, detached SHA256, and executed notebook for audit.
