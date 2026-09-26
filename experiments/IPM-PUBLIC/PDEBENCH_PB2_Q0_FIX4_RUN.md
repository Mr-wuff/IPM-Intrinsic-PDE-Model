# PB2-Q0-FIX4 Frozen Run Record

Experiment:
`IPM-PDEBench-PB2-Q0-FIX4 — Multi-Environment Reaction-Diffusion Identifiability Audit`

Frozen notebook:
`IPM_PDEBench_PB2_Q0_FIX4_MultiEnvironment_ReactionDiffusion_Identifiability_Audit_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`badf1233bdb2137eb5848f0e0519232776402dfce1901bb15cc1121bd0459557`

Protocol SHA256:

`67c3732aaa0c2cb704232a4baa76bdf9acc5c570207355cff804f62456677c71`

Pinned preregistration commit:

`d52a3a22a38281a89c31839fc386cf897f875bf8`

Development environments:
- Nu=0.5, Rho=1.0
- Nu=0.5, Rho=2.0
- Nu=1.0, Rho=1.0

Frozen identification:
- FULL1024
- LocalTaylor R4/D5/order3 float64
- per-environment generator-validity gate
- S2 integral-only
- P13
- independent-ridge baseline
- deterministic multi-environment row-group sparse FISTA
- support shared across environments; amplitudes environment-specific

Lambda selection uses validation residual, support size and fold support Jaccard only.

All first 1,000 official trajectories in every environment remain sealed.

No architecture transition, official-test unlock or 500-epoch training is authorized.
