# IPM-PDEBench-PB1-Q4 Run Record

Notebook:
`IPM_PDEBench_PB1_Q4_Native_Flow_Gain_Closure_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`eedc782fb810b1496abf5f0227b03391685c94c4c5195d621dc49e7a70c47475`

Embedded executable protocol SHA256:
`4be13efe79a7a2d8f267e22518bc0243ea9d5d8dfd87cff3f63b288eb22e834f`

Pinned IPM commit:
`29edcc751f157100e5d332e677c8611c4fc815f8`

Manual uploads:
**none**

## Purpose

PB1-Q4 is the final cheap closure qualification before any full standard-data training.

It preserves the PB1-Q3-FIX1 learned principal polynomial shapes and optimizes only the same four RTDS gains, but performs that refinement through the exact differentiable native compiled flow instead of only the central-secant proxy.

The official PDEBench test block remains untouched.

## Frozen scientific contract

The scientific contract remains the preregistered PB1-Q4 contract:
- IDTC fit: first 1000 official-training trajectories;
- gain/flow calibration: next 128;
- validation: next 256;
- native-time IDTC fit, 20 epochs, 400 optimizer updates;
- only g_R, g_T, g_D, g_S are refined through the native flow;
- 160 gain-refinement updates, 16 calibration trajectories/update, 4-step compiled rollout;
- objective = normalized 4-step compiled rollout + 0.25 secant-preservation + 0.002 relative gain-prior;
- no exact PDE RHS, known equation coefficients, equation-specific pruning, or official test data.

The regenerated executable artifact adds only implementation/audit details needed to make the preregistered contract self-contained (including a finite/non-zero gain-gradient semantic audit and deterministic packaging). It does not relax or alter any scientific gate.

## Formal rule

No 500-epoch run is allowed unless at least one frozen candidate passes every PB1-Q4 runtime, absolute-rollout, non-regression, secant-preservation, bounded-gain, and geometric-improvement gate on both PDEs.

If no candidate passes, the next experiment must expand/repair principal algebra or normal-form closure. Training scale must not be increased.
