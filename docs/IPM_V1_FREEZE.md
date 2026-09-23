# IPM-v1 Freeze — Mathematical Core and Parallel Runtime

## Frozen mathematical core

Source: A2-Q3-FIX2.

The deployment program is the calibrated principal normal form compiled from the frozen 35-parameter IDTC:

[
Q_P=
lambda_RR(u)
+lambda_Tf_T(u)u_x
+lambda_Df_D(u)rac{u_{xx}}2
+lambda_Sf_S(u)rac{u_{xxx}}6.
]

No mixed-derivative nuisance terms are used at deployment.

## Frozen role programs

PDEBench qualification:
- Advection beta=1: role mask T
- Burgers nu=0.01: role mask T+D+S

The role mask and gains are training-side calibrated and frozen before official test evaluation.

## Frozen execution runtime

Source: A2-Q4.

- Portable/reference runtime: E0 eager
- Fast repeated-step runtime: E4 single-step CUDA Graph
- Fast fixed-horizon runtime: E5 horizon CUDA Graph

Optimized execution must remain numerically equivalent to E0.

## Current qualification evidence

Q3-FIX2:
- Advection 40-step Rel-L2: 0.07976
- Burgers: 0.19280
- finite 3/3 seeds
- 1% noise robust
- Advection coarse /4-grid transfer remains a limitation

Q4:
- batch-1 physical-step speedup vs official FNO:
  - Advection 48.81x
  - Burgers 17.50x
- batch-16:
  - Advection 45.23x
  - Burgers 17.71x
- E5 40-step horizon speedup vs E0:
  - batch1 ~7.02x / 4.79x
  - batch16 ~3.54x / 4.84x

## Freeze rule

From this point forward, broad paper benchmarking must not modify the IPM mathematical architecture based on baseline-specific test results.

Allowed:
- exact execution backends;
- hardware-specific compilation;
- numerical-equivalence-preserving kernel fusion;
- benchmark adapters;
- bug fixes that do not change the model.

Not allowed without a new clearly separated post-v1 experiment:
- changing role masks using official test data;
- refitting gains on test data;
- changing IDTC architecture;
- adding baseline-specific neural modules;
- altering the PDE program to target a competing baseline.

## Next phase

B-series comprehensive benchmark:
1. B0 classical numerical solver speed-quality frontier
2. B1 neural surrogate/operator suite
3. B2 PINN and physics-informed operator suite
4. B3 discovery/mechanistic and foundation PDE models
5. B4 unified Pareto / amortized-cost analysis

The final paper reports native/best-practice contracts rather than forcing all method families into an artificial single training regime.