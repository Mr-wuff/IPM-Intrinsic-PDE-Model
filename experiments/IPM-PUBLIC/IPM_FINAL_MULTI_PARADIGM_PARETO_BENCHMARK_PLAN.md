# IPM Final Multi-Paradigm Pareto Benchmark Plan

## Purpose

The final IPM paper must not reduce evaluation to a single accuracy table.

IPM spans multiple scientific-computing functions:
1. trajectory-to-future prediction;
2. trajectory-to-governing-law identification;
3. explicit PDE compilation;
4. structure-consistent physical execution.

Therefore comparisons must be organized by **task and information budget** before Pareto aggregation.

No method may be credited with information that competing methods are not given.

## Public benchmark anchors

Primary:
- PDEBench: shared PDE datasets and official FNO / U-Net / PINN baselines.
- PDEArena: scalable surrogate framework with FNO, ResNet, U-Net, UNO and efficiency statistics.
- PINNacle: physics-informed benchmark and multiple PINN variants.

Equation-discovery references:
- PDE-FIND / SINDy
- WSINDy
- WeakIdent or another reproducible weak PDE discovery baseline where code/data compatibility permits.

Physics-informed operator references:
- PINO
- optionally one modern reproducible physics-informed/variational operator method if a fair implementation on selected tasks is available.

Classical numerical reference:
- the benchmark data-generating numerical solver or a matching high-quality finite-volume / spectral solver where reproducible.

## Method families

### A. Pure data-driven surrogates
Mandatory:
- FNO
- U-Net

Strong recommended:
- DeepONet
- CNO or UNO
- PDEArena modern U-Net/ResNet representative where applicable

### B. Physics-informed neural solvers
Mandatory:
- vanilla PINN
- PINN Adam+L-BFGS or the official PDEBench/PINNacle recommended implementation

Recommended representative variants:
- PINN-LRA or PINN-NTK
- RAR
- gPINN
- hp-VPINN

Do not run every PINNacle variant on every PDE if computational cost is prohibitive. Pre-register a representative subset and use the full PINNacle suite on a smaller common task set.

### C. Physics-informed neural operators
Mandatory if compatible:
- PINO

Optional:
- VINO or another reproducible variational operator method

### D. Equation-discovery methods
Mandatory:
- PDE-FIND
- WSINDy

Recommended:
- WeakIdent or equivalent robust weak sparse-discovery method

### E. Classical numerical solvers
At least one matching reference solver per PDE family:
- finite volume / finite difference / spectral as appropriate

### F. IPM
Report:
- generic DIC-DCC35 strong branch
- WCFC low-mode integral weak branch when conservation/shock semantics activate
- structure-aware compiler
- corresponding native executor

## Fair comparison tracks

### Track 1 — Same-data prediction / rollout
All learned methods receive the same trajectory count, temporal history, spatial observation and train/test split.

Compare:
- IPM
- FNO
- U-Net
- DeepONet/CNO/UNO representatives

PINN/PINO may enter only if their PDE knowledge is explicitly declared.

### Track 2 — Known-PDE physics-informed solving
The governing PDE is supplied.

Compare:
- PINN family
- PINO
- numerical solver
- IPM execution using an already-identified frozen law, clearly marked as requiring prior identification data.

This track measures solving/execution, not equation discovery.

### Track 3 — Unknown-PDE equation discovery
Only trajectories are supplied; true PDE terms and coefficients are hidden.

Compare:
- IPM
- PDE-FIND
- WSINDy
- WeakIdent where available

Metrics emphasize equation recovery plus future rollout of the recovered law.

### Track 4 — OOD/operator generalization
Hold out physical parameters, initial-condition families, temporal sampling and/or spatial resolutions.

Compare operator/generalization methods under identical information budgets.

### Track 5 — Efficiency Pareto
Same hardware, same batch sizes where meaningful, synchronized timing, warm-up excluded.

Report wall-clock and hardware costs separately for:
- identification/training;
- single-step inference;
- 31-step/full-horizon rollout;
- memory;
- artifact/model size.

## Core metric families

### 1. Predictive accuracy
- RMSE
- nRMSE
- relative L2
- maximum error
- boundary RMSE where applicable
- spectral-band error
- long-rollout error vs horizon
- failure/non-finite rate

### 2. Physical consistency
Problem-dependent, computed from predictions without using the metric to train unless declared:
- PDE residual in appropriate strong or weak form
- conservation drift: mass, momentum, energy, enstrophy or other invariants
- boundary-condition violation
- positivity / boundedness violation
- entropy-condition violation for conservation laws where measurable
- divergence error for incompressible flow
- symmetry/equivariance error where relevant
- physically invalid-state rate

### 3. Governing-law fidelity
For discovery-capable methods:
- active-term precision / recall / F1
- coefficient relative error
- coefficient cosine
- cross-fold coefficient stability
- correct physical role recovery
- spurious-term magnitude
- recovered-law rollout error
- identifiability under noise and subsampling

### 4. Trustworthiness / reliability
Avoid a vague single "trust score".

Report measurable components:
- seed/fold variance
- calibration of probabilistic models if probabilistic outputs exist
- OOD degradation ratio
- catastrophic-failure/non-finite rate
- conservation-violation tail quantiles
- sensitivity to temporal/spatial perturbation
- coefficient stability for explicit-law methods
- reproducibility across independent splits

### 5. Computational efficiency
- train/identification wall time
- GPU-hours / CPU-hours
- peak GPU memory
- peak host RAM
- parameter count
- active scalar law count
- serialized model/program size
- forward latency
- rollout latency
- throughput
- energy estimate where trustworthy measurement is available
- amortization break-even versus numerical solver

### 6. Data efficiency
Repeat standardized subsets:
- 1%
- 5%
- 10%
- 25%
- 50%
- 100%

Report accuracy and physical metrics versus number of trajectories / collocation points.

### 7. Robustness
Controlled perturbations:
- observation noise
- temporal subsampling
- spatial downsampling
- physics-preserving versus non-preserving observation operators
- unseen PDE parameters
- unseen initial-condition distributions
- optional missing/corrupted measurements

## Pareto reporting

Do **not** collapse all metrics into one arbitrary weighted score as the primary result.

Primary reporting:
- accuracy vs inference cost
- accuracy vs training/identification cost
- accuracy vs data volume
- physical consistency vs predictive error
- law fidelity vs discovery cost
- OOD degradation vs model size

Use Pareto fronts and capability matrices.

A secondary normalized radar or aggregate score may be shown only as visualization, with weights declared and sensitivity analysis included.

## Information-budget ledger

Every result table must declare:
- Is the true PDE known?
- Are coefficients known?
- Are boundary/initial conditions known?
- Number of trajectories used
- Spatial/temporal resolution
- Whether full-resolution data are available
- Whether simulator queries/collocation points are available
- Whether labels/future targets are used
- Whether external pretraining is used

This ledger is mandatory for fairness.

## Same-hardware protocol

For final performance claims:
- one frozen GPU model/hardware class;
- fixed software stack;
- deterministic seeds when supported;
- >= 3 seeds/folds;
- warm-up before timing;
- CUDA synchronize around timing;
- report median and p10/p90 or mean/std;
- separate Python/eager reference runtime from optimized/compiled runtime;
- do not compare IPM optimized kernels to baseline eager code without also providing matched compiled/eager controls.

## Final paper message

The benchmark should test the hypothesis that IPM offers a distinct Pareto region:

- near-explicit numerical-physics consistency;
- interpretable/recoverable governing laws;
- much smaller learned state/program size;
- low identification/training cost;
- competitive trajectory prediction;
- fast amortized execution after compilation.

The paper should not claim universal superiority. It should identify the regimes in which IPM is advantageous and the regimes in which conventional numerical solvers, neural operators or PINNs remain preferable.
