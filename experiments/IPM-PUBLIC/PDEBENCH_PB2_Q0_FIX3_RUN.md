# PB2-Q0-FIX3 Frozen Run Record

Experiment:
`IPM-PDEBench-PB2-Q0-FIX3 — Temporal Generator-Validity Gated Integral Qualification`

Frozen notebook:
`IPM_PDEBench_PB2_Q0_FIX3_Temporal_Generator_Validity_Gated_Integral_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`55a7a95e665316be7dca525ee172f6c378710b3f510f84d3c2dae4c32fddcd80`

Protocol SHA256:

`fb52b1f2071ef4e56923d92dddd3cfe1805c8963ccfb7a8431647cb319ad915c`

Pinned preregistration commit:

`8a6adecacfc419ff3099e7e8d33d5ab5d1bb1bbe`

Frozen data-only generator-validity rule:
- signal >= 15% of calibration-block peak signal
- temporal curvature / signal <= 0.40
- centers restricted to 2..98
- 3..12 qualifying centers required

Candidate fits:
- LocalTaylor R4/D5/order3 float64
- DCC35 and P13
- integral-only
- Simpson-2 and composite Simpson-4
- P13 temporal contract chosen by validation integral residual subject to cosine stability >=0.995

Official first 1,000 Reaction-Diffusion trajectories remain sealed.

Runtime accuracy is diagnostic only in this run because PB2-Q0-FIX1 already established a coarse-runtime mismatch for the exact continuum law.

No architecture transition, official-test unlock, or 500-epoch training is permitted by this run record.
