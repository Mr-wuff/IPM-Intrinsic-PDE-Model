# PB2-Q0-FIX5 Frozen Run Record

Experiment:
`IPM-PDEBench-PB2-Q0-FIX5 — Environment-Qualified Rho-Sweep Shared-Support Audit`

Frozen notebook:
`IPM_PDEBench_PB2_Q0_FIX5_Qualified_RhoSweep_SharedSupport_Audit_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`a21c8f731174c7efc372a85e4ef079c9bf914a31adcbf6e000c0034060c55959`

Protocol SHA256:

`1465e3936ab0ee53a9b301e7a8ca7d3a14d2f450e2d00e1bd949ea698b7c62c1`

Pinned preregistration commit:

`4cfb087a0a9af1c7caee8750d40b98364c3112a2`

Frozen environment pool:
- Nu0.5/Rho1
- Nu0.5/Rho2
- Nu0.5/Rho5
- Nu0.5/Rho10

Frozen environment qualification:
- per-environment data-only generator-validity gate;
- S2 integral-only P13;
- dedicated screen block 2048:2304;
- screen mean <=0.12;
- max fold <=0.15;
- at least two qualified environments.

Only qualified environments may enter the group-sparse shared-support fit.

Lambda is selected on a disjoint validation block by:
- within 1.05x best validation;
- support size <=6;
- support Jaccard >=0.80;
- smallest support, then lower validation residual.

Official first 1,000 rows remain sealed in all environments.

No architecture transition, official-test unlock, or 500-epoch training is authorized by this run record.
