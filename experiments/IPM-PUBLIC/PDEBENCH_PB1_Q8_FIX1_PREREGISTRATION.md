# IPM-PDEBench-PB1-Q8-FIX1 — Low-Viscosity Discretization Attribution

## Motivation

PB1-Q8 failed only because the unseen low-viscosity Burgers regime `epsilon=0.001` did not pass internal I1/I2/I3.

However, a post-run audit using the pinned PDEBench generator shows that the recovered differential-law coefficients are already close to the actual PDE law.

PDEBench Burgers uses:

`u_t = -u u_x + (epsilon/pi) u_xx`

and with the IPM Taylor coordinate `a2=u_xx/2` the exact reporting-only canonical law is:

`Q = -u*a1 + (2*epsilon/pi)*a2`.

For `epsilon=0.001`, Q8 recovered approximately:
- transport coefficient: `-0.967` mean versus `-1`;
- diffusion coefficient: `0.000647` mean versus `2e-3/pi = 0.00063662`.

Therefore Q8-FIX1 is a **discretization attribution study**, not an identification-architecture search.

No official test trajectory is loaded.

## Frozen architecture

DIC-DCC35 remains unchanged:
- total-degree<=3 35-term direct canonical law;
- equal differential-integral consistency;
- ridge alpha `1e-8`;
- exact P13 deployment projection.

No new law capacity is introduced.

## Dataset

PDEBench:
- `1D_Burgers_Sols_Nu0.001.hdf5`
- official test first 1,000 trajectories remain sealed.

Use only the same training-block rows used by Q8.

## Attribution axes

### A. Spatial-resolution sweep

Run the same R4/D5 DIC-DCC35 identification at:
- spatial reduction 4 -> N=256
- spatial reduction 2 -> N=512
- spatial reduction 1 -> N=1024

Use the same three 1,024-trajectory fit folds and the same internal confirm rows.

Measure:
- DIC characteristic Rel-RMS;
- DIC integral Rel-RMS;
- learned transport/diffusion coefficients;
- exact-law oracle characteristic and integral residual using the same jet.

### B. Jet-estimator sweep at the official N=256 grid

Compare:
- LocalTaylor R4/D5
- LocalTaylor R6/D7
- LocalTaylor R8/D7
- periodic spectral jet

For each estimator, measure the exact-law oracle residual and DIC-DCC35 residual on the same training-only confirm block.

This is diagnostic only and does not authorize a jet change.

### C. Native-runtime attribution

At N=256, 512, 1024 compare:
- exact-law oracle P13 runtime;
- learned DIC-DCC35 -> P13 runtime.

For each program compare:
- one coarse step per official interval: `dt_step = 5*dt_raw`;
- five native substeps: `dt_step = dt_raw`, repeated 5 times.

Evaluate train-only confirm 31-step Rel-L2.

No gain refinement is applied in this attribution stage: gains are fixed to 1 so the runtime is tested against the identified physical law without compensating scalar distortion.

### D. Q8 gain-compensation audit

Record the already-archived Q8 epsilon=0.001 result:
- raw 31-step confirm about 0.33;
- refined 31-step confirm about 0.298;
- refined gain closure moved the effective diffusion to roughly 2.95x the exact coefficient while producing only modest rollout improvement.

This is evidence that gains were compensating for discretization mismatch.

## Frozen attribution hypotheses

### H1 — law identification is already physically correct
At official N=256, three-fold mean raw DIC coefficients must satisfy:
- `u*a1` amplitude error <= 5%;
- `a2` coefficient error relative to `2*epsilon/pi` <= 10%.

### H2 — spatial observation/jet resolution bottleneck
Supported if either:
- exact-law oracle characteristic residual at N=1024 / N=256 <= 0.70; or
- DIC characteristic residual at N=1024 / N=256 <= 0.70.

### H3 — local jet estimator bottleneck at fixed N=256
Supported if the best alternative estimator's exact-law characteristic residual / R4D5 exact-law residual <= 0.75.

### H4 — native spatial runtime bottleneck
Supported if exact-law 31-step rollout at N=1024 / N=256 <= 0.70.

### H5 — temporal runtime bottleneck
Supported if N=256 exact-law five-substep rollout / one-coarse-step rollout <= 0.80.

### H6 — gain compensation
Supported if Q8 gain closure changed either effective transport or diffusion by >30% from the already-correct raw law while improving 31-step rollout by <15%.

## Decision

Q8-FIX1 does not pass/fail the DIC-DCC35 architecture and never opens official test data.

It returns one of:
- `JET_RESOLUTION_REPAIR`
- `NATIVE_RUNTIME_REPAIR`
- `JET_AND_RUNTIME_REPAIR`
- `UNRESOLVED_LOW_VISCOSITY`

The next experiment may modify only the layer(s) supported by these attribution hypotheses.

No 500-epoch training is authorized.
