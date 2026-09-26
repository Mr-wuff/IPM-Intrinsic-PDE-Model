# IPM-PDEBench-PB2-Q0-FIX5 — Environment-Qualified Rho-Sweep Shared-Support Audit

## Motivation

PB2-Q0-FIX4 showed that the three-environment joint fit was confounded by one environment whose own frozen temporal contract does not close:

- Nu0.5/Rho1.0: S2-P13 confirm ~0.064
- Nu0.5/Rho2.0: S2-P13 confirm ~0.038
- Nu1.0/Rho1.0: S2-P13 confirm ~0.715

Therefore a multi-environment support learner must not pool environments before checking that each environment is itself compatible with the frozen generator-observation contract.

FIX5 isolates the reaction-strength intervention axis by holding diffusion fixed:

- Nu=0.5
- Rho in {1,2,5,10}

Only environments that pass a data-driven S2 closure screen are allowed to contribute to shared-support identification.

No official test data are opened.

## Environment pool

### R1
Nu=0.5, Rho=1.0  
`ReacDiff_Nu0.5_Rho1.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133177`  
MD5: `69a429239778d529cd419ed5888ea835`

### R2
Nu=0.5, Rho=2.0  
`ReacDiff_Nu0.5_Rho2.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133179`  
MD5: `ac907daa7e483d203a5c77567cdea561`

### R5
Nu=0.5, Rho=5.0  
`ReacDiff_Nu0.5_Rho5.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133180`  
MD5: `fb149e7540d8977af158bb8fec1048a3`

### R10
Nu=0.5, Rho=10.0  
`ReacDiff_Nu0.5_Rho10.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133178`  
MD5: `ff7c724b18e7ebe02e19c179852f48ee`

The first 1,000 rows of every file remain sealed.

## Splits per environment

Relative to the 9,000-row training portion:

- fit fold A: 0:512
- fit fold B: 512:1024
- fit fold C: 1024:1536
- generator-validity calibration: 1536:1600
- environment screen: 2048:2304
- lambda validation: 3072:3328
- final internal confirm: 3584:3840

The screen and lambda-validation blocks are disjoint.

## Frozen state and temporal contract

FULL1024.

LocalTaylor:
- radius 4
- degree 5
- order 3
- float64.

Canonical space:
- P13 only.

Per-environment generator-validity gate:
- centers 2..98;
- signal >=15% of that environment's peak;
- temporal curvature / signal <=0.40;
- require 3..12 centers.

Temporal equation:
- S2 Simpson integral-only.

Normalized ridge alpha:
- 1e-8.

No DCC35, S4, or centered differential equation is evaluated.

## Stage A — environment qualification

For each environment and each of three fit folds:

- fit independent P13 on the fit fold;
- evaluate on the disjoint environment-screen block.

An environment is **contract-qualified** iff:

1. generator-validity center count is 3..12;
2. three-fold mean screen integral residual <=0.12;
3. maximum fold screen residual <=0.15;
4. all coefficients are finite.

No true PDE coefficient or support is used for environment qualification.

Require at least two qualified environments.

The set of qualified environments is frozen before any group-sparse lambda fit.

## Stage B — shared-support fit on qualified environments only

Each qualified environment keeps an independent P13 coefficient vector.

Fit row-group sparse standardized coefficients:

`sum_e L_e(z_e) + lambda * sum_j ||Z[j,:]||_2`

using deterministic FISTA.

Lambda fractions:

`[0,1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,2e-1,4e-1]`

Active support:
- standardized row group norm >1e-5.

## Lambda selection

On the disjoint lambda-validation block:

Eligibility:
- validation mean <=1.05 * best validation mean on the grid;
- support size <=6;
- median three-fold support Jaccard >=0.80.

Selection:
1. smallest support size;
2. lower validation residual;
3. larger lambda fraction if still tied.

If no lambda is eligible, the experiment fails without threshold relaxation.

## Final internal confirm

Freeze qualified-environment set and selected lambda.

Evaluate every selected fold/environment on confirm rows.

## Reporting-only physical audit

Only after all data-driven selection is frozen.

For every qualified environment, the expected continuum support is:

- R_u
- R_u2
- D0

Expected coefficients:
- R_u = rho
- R_u2 = -rho
- D0 = 1 because Nu=0.5

No true coefficient or support is used for qualification or lambda selection.

Report:
- consensus support precision / recall / F1;
- sign correctness;
- active physical coefficient relative L2;
- spurious-support terms;
- improvement versus independent ridge.

## Frozen gates

### Q1 — environment qualification
At least two environments are contract-qualified.

### Q2 — confirm closure
Across qualified environments:
- all-env/fold confirm mean <=0.10;
- maximum qualified-environment mean <=0.12.

### Q3 — support stability
- median fold-pair support Jaccard >=0.80;
- maximum selected support size <=6.

### Q4 — physical support recovery
Reporting-only:
- recall of {R_u,R_u2,D0} =1.0;
- precision >=0.75.

### Q5 — coefficient fidelity
Reporting-only:
- R_u positive in every qualified env/fold;
- R_u2 negative in every qualified env/fold;
- D0 positive in every qualified env/fold;
- overall active physical coefficient relative L2 mean <=0.30;
- maximum qualified-environment mean <=0.40.

### Q6 — benefit versus independent ridge
At least half of the qualified environments (ceiling division) improve their mean reporting-only active physical coefficient error relative to independent ridge.

## Routing

If Q1-Q6 all pass:

`RHO_AXIS_SHARED_SUPPORT_SUPPORTED`

If Q1-Q3 pass but Q4/Q5 fail:

`RHO_AXIS_EFFECTIVE_SUPPORT_ONLY`

If Q1 fails:

`INSUFFICIENT_CONTRACT_QUALIFIED_ENVIRONMENTS`

If Q1 passes but Q2/Q3 fail:

`RHO_AXIS_SHARED_SUPPORT_INSUFFICIENT`

Otherwise:

`REACTION_DIFFUSION_IDENTIFIABILITY_UNRESOLVED`

No official test access, architecture transition, or 500-epoch training is authorized.

If the first route is reached, the next experiment must independently confirm the frozen support on held-out parameter environments and separately address the diffusion-axis temporal-contract mismatch.
