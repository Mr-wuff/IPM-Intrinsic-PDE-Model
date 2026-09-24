# IPM-PDEBench-PB1-Q4 Run Record

Notebook:
`IPM_PDEBench_PB1_Q4_Native_Flow_Gain_Closure_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`caef36b9e338b2b5529bb30b2d8cbd0bfafefc6831ce5d967cb623b596942010`

Protocol SHA256:
`05b0f241a710e12fcbd1924917096e3a04187cabfb9ac7507b5c5177122771c8`

Pinned IPM commit:
`29edcc751f157100e5d332e677c8611c4fc815f8`

Manual uploads:
**none**

## Purpose

PB1-Q4 is the final cheap closure qualification before any full standard-data training.

It preserves the Q3-FIX1 learned principal polynomial shapes and optimizes only the same four RTDS gains, but performs that refinement through the exact differentiable native compiled flow instead of only the central-secant proxy.

The official PDEBench test block remains untouched.

## Formal rule

No 500-epoch run is allowed unless at least one frozen candidate passes every PB1-Q4 runtime, absolute-rollout, non-regression, secant-preservation, and bounded-gain gate on both PDEs.

If no candidate passes, the next experiment must expand/repair principal algebra or normal-form closure. Training scale must not be increased.
