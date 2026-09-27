# PB2-Q0-FIX6 Frozen Run Record

Experiment:
`IPM-PDEBench-PB2-Q0-FIX6 — Budget-Normalized Rho-Sweep Exhaustive Common-Support Audit`

Frozen notebook:
`IPM_PDEBench_PB2_Q0_FIX6_BudgetNormalized_RhoSweep_Exhaustive_CommonSupport_Audit_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`57f4ff095d4f05adf5a3c0a86ccbc73b77fb60d8d2725f89ce2b1072e1ee2daa`

Protocol SHA256:

`ba965f7ff0ed93f2cfa0836af061140327be74ea59ca73c4a708f66644815ea9`

Pinned preregistration commit:

`957a55c49479ec3fd08e4ecdcf9b70978d4cc67c`

Frozen environment pool:
- Nu0.5/Rho1
- Nu0.5/Rho2
- Nu0.5/Rho5
- Nu0.5/Rho10

Key frozen changes relative to FIX5:
- no upper bound on generator-valid pool size;
- target-free greedy D-optimal temporal budget B=8;
- environment screen still precedes any support pooling;
- require at least 3 qualified environments;
- exhaustive common-support search over all 4095 non-empty P13 supports of size 1..6;
- global and fold-specific support selection uses validation only;
- true physical support is reporting-only.

Official first 1,000 rows remain sealed in every environment.

No architecture transition, official-test unlock, or 500-epoch training is authorized by this run record.
