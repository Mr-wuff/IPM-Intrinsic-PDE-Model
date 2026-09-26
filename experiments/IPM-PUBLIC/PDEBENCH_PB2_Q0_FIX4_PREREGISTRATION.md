# IPM-PDEBench-PB2-Q0-FIX4 — Multi-Environment Reaction-Diffusion Identifiability Audit

## Motivation

PB2-Q0-FIX3 is formally protocol-deviated because the executed notebook relaxed the frozen coefficient-cosine eligibility threshold from 0.995 to 0.99.

Its diagnostic data nevertheless provide a decisive observation:

- GENVALID=[2,3,4,5,6,7,8] is data-only and physically sensible;
- S2 integral-only P13 confirm residual is ~0.064;
- diffusion D0 is stable at ~1.05–1.08;
- reaction coefficients vary strongly across folds.

Thus the remaining problem is not trajectory-integral closure. It is **coefficient identifiability inside one physical parameter environment**.

FIX4 tests whether multiple Reaction-Diffusion environments provide the missing structural excitation.

No official test block is opened and no architecture transition is authorized.

## Development environments

Use three PDEBench training files:

### E0
Nu=0.5, Rho=1.0  
`ReacDiff_Nu0.5_Rho1.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133177`  
MD5: `69a429239778d529cd419ed5888ea835`

### E1
Nu=0.5, Rho=2.0  
`ReacDiff_Nu0.5_Rho2.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133179`  
MD5: `ac907daa7e483d203a5c77567cdea561`

### E2
Nu=1.0, Rho=1.0  
`ReacDiff_Nu1.0_Rho1.0.hdf5`  
URL: `https://darus.uni-stuttgart.de/api/access/datafile/133181`  
MD5: `bd73c2f3448d03e95e98c3831fc8fa70`

These three environments independently vary reaction and diffusion strength.

All first 1,000 rows in every file remain sealed.

## Splits per environment

Relative to the training portion after the first 1,000 rows:

- fit fold A: 0:512
- fit fold B: 512:1024
- fit fold C: 1024:1536
- center-calibration: 1536:1600
- validation: 3072:3328
- confirm: 3584:3840

## Frozen state representation

FULL1024.

LocalTaylor:
- radius 4
- degree 5
- order 3
- float64.

Canonical deployment space:
- P13 only.

FIX4 does not revisit DCC35.

## Per-environment data-only generator-validity gate

For each environment separately, centers c=2..98:

`s_c = RMS(u_{c+1}-u_{c-1})`

`r_c = RMS(u_{c+1}-2u_c+u_{c-1})/(s_c+1e-12)`

A center is valid iff:
- signal >= 15% of that environment's peak signal;
- curvature/signal <=0.40.

Require 3..12 valid centers per environment.

## Frozen temporal contract

Use S2 integral-only only:

`u_{c+1}-u_{c-1} = dt/3 [Q_{c-1}+4Q_c+Q_{c+1}]`

This is frozen from the valid diagnostic result in FIX3.

No S4 and no differential equation are evaluated.

## Stage A — independent P13 baseline

For each environment and fold:
- fit normalized ridge P13;
- alpha=1e-8;
- report validation/confirm residual;
- report coefficient stability and normalized Gram condition number.

This stage asks whether parameter changes naturally improve single-environment identifiability.

## Stage B — multi-environment shared-support P13

Let each environment have its own standardized coefficient vector `z_e`.

Fit all environments jointly with a row-group sparse penalty:

`sum_e L_e(z_e) + lambda * sum_j ||Z[j,:]||_2`

where each row j is one P13 canonical term shared across environments.

The penalty shares **support only**. Coefficient amplitudes remain environment-specific.

Optimization:
- deterministic FISTA proximal-gradient;
- no SGD;
- maximum 5000 iterations;
- tolerance 1e-10.

Lambda grid as fractions of lambda_max:

`[0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 2e-1, 4e-1]`

## Lambda selection

For each lambda:
- fit the three independent trajectory folds;
- compute mean validation integral residual across environments and folds;
- determine active support with standardized group-row norm >1e-5;
- compute support Jaccard across folds.

Eligibility:
- mean validation residual <=1.05 times the minimum validation residual on the grid;
- support size <=6;
- median fold-pair support Jaccard >=0.80.

Among eligible candidates choose:
1. smallest support size;
2. then lower validation residual.

If no lambda is eligible, the audit fails without threshold relaxation.

## Confirm evaluation

Freeze the selected lambda.

Evaluate:
- confirm integral residual per environment and fold;
- coefficient matrix stability;
- support stability;
- physical coefficients reporting-only.

No runtime is used for lambda selection.

## Reporting-only physics audit

After selection only.

For each environment the known continuum P13 support is:
- R_u
- R_u2
- D0

Expected coefficients:
- R_u = rho
- R_u2 = -rho
- D0 = 2*nu

All other P13 terms are zero.

Report:
- support precision/recall/F1;
- coefficient relative error per environment;
- sign correctness;
- spurious active terms.

The known values never enter fitting or lambda selection.

## Frozen hypotheses

### M1 — generator-validity viability
All three environments produce 3..12 data-only valid centers.

### M2 — multi-environment residual closure
Selected joint-support model:
- mean confirm integral residual across all env/folds <=0.10;
- max environment mean <=0.12.

### M3 — support stability
- median fold-pair Jaccard >=0.80;
- selected support size <=6.

### M4 — governing-support recovery
Reporting-only:
- recall of {R_u,R_u2,D0} = 1.0;
- precision >=0.75.

### M5 — coefficient fidelity
Reporting-only:
- signs correct for R_u, R_u2, D0 in every environment/fold;
- mean physical active-coefficient relative L2 error <=0.30;
- max environment mean <=0.40.

### M6 — improvement over independent single-environment identifiability
At least two of three environments show lower fold-to-fold physical active-coefficient CV or relative error under the joint-support fit than under independent ridge.

## Routing

If M1-M6 all pass:

`MULTI_ENVIRONMENT_IDENTIFIABILITY_SUPPORTED`

If M1-M3 pass but M4/M5 fail:

`SHARED_SUPPORT_EFFECTIVE_CLOSURE_ONLY`

If M1 passes but M2/M3 fail:

`MULTI_ENVIRONMENT_SUPPORT_INSUFFICIENT`

Otherwise:

`REACTION_DIFFUSION_IDENTIFIABILITY_UNRESOLVED`

No official test access, architecture freeze, or 500-epoch training is authorized.

If the first route is reached, the next experiment must independently confirm the frozen support-learning protocol on previously unused environments, e.g. Nu=1,Rho=2 and Nu=2,Rho=1.
