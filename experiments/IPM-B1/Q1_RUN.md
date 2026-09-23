# IPM-B1-Q1 Frozen Run Record

Notebook:
`IPM_B1_Q1_ThreeSeed_MatchedUpdate_Neural_Benchmark_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`34a51844b1ed82fafc45e0661377e793a2916dc4d7c350d2f129e61089870ce1`

Protocol SHA256:
`88fc0925420d7c623f16cae072fba69ac98bc5f3d506187db2fef7e46e09673f`

Pinned repository code commit used by the notebook:
`85a13e885a80458b36dd5b2e890962463953721d`

Pinned NeuralOperator commit:
`00b7d86f8d74ff0af55da53eb585fe26df9c71f0`

Pinned DeepXDE commit:
`99b6620386d18cefb1549dddb7b7fe468cfad607`

Manual input uploads required: **none**.

The notebook downloads and MD5-verifies PDEBench data and installs all model code from pinned Git commits.

Formal workload:
- 6 neural models
- 2 PDEs
- 3 seeds
- 1536 updates per neural run
- 36 total neural training attempts
- N=256 formal grid
- 40-step rollout
- frozen IPM-v1 seeds 101/202/303
- eager + whole-horizon CUDA Graph runtime audit
- accuracy / spectral / cost / Pareto exports

The notebook itself is distributed as the run artifact associated with this record; the repository contains the reusable implementation and frozen protocol.

Formal-run hygiene: the notebook removes any pre-existing `IPM_B1_Q1_RESULTS/` directory at startup before creating the new result tree, preventing stale partial-run artifacts from entering the packaged ZIP.
