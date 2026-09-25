# IPM-PDEBench-PB1-Q7-FIX1 Results — Differential-Integral Consistent DCC Qualification

## Integrity

Result ZIP SHA256:

`3ce2c9f8f13c38680fbeca19ccd0d9dd60991cac6115f833f5cfcc2e0907d875`

Detached manifest: **28/28 payload entries match** by byte size and SHA256.

Protocol SHA256:

`1e8f1230292c2beb1e9dd14bc5786d397498ec8e5de8eb71b2527f6d65854459`

Official PDEBench test trajectories were not loaded.

The executed notebook reports:
- Tesla T4
- 3 disjoint 1,024-trajectory fit folds
- 256 calibration trajectories
- 512 validation trajectories
- 512 confirmatory internal trajectories

No 500-epoch training was performed.

## Frozen gate result

All eight preregistered gates passed:

- F1 characteristic closure: **PASS**
- F2 integral preservation: **PASS**
- F3 long-horizon closure: **PASS**
- F4 objective repair: **PASS**
- F5 generic-space viability: **PASS**
- F6 coefficient stability: **PASS**
- F7 projection viability: **PASS**
- F8 basis consistency: **PASS**

Formal decision:

**PB1-Q7-FIX1 PASS**

Architecture transition:

**IDTC-35 -> DIC-DCC35 AUTHORIZED**

No new 500-epoch run is authorized.

## Core metrics

DIC-DCC35 confirm characteristic:
- mean: **0.1579636**
- max fold: **0.1596299**

DIC-DCC35 confirm Simpson-integral residual:
- mean: **0.1049802**
- max fold: **0.1066127**

Integral-only DCC35 confirm characteristic:
- mean: **0.2184209**

Thus differential-integral consistency reduces the full-space characteristic error by:

`0.1579636 / 0.2184209 = 0.7232`

or **27.68%**, while keeping the integral residual inside the preregistered preservation bound.

## Generic-space result

DIC-P13 confirm characteristic mean:

**0.1720698**

DIC-DCC35 / DIC-P13 characteristic ratio:

**0.9180203**

Therefore the complete generic 35-term canonical space is not merely tolerated; under the repaired identification contract it is more accurate than its exact 13-term principal subspace on instantaneous characteristic recovery.

## Native-flow result

Projected/refined DIC-DCC35 31-step confirm rollout:
- mean: **0.1875445**
- max: **0.1907483**

Direct DIC-P13 refined 31-step rollout:
- mean: **0.1831625**

Projected/full-space over direct-P13 rollout ratio:

**1.023924**

Thus the generic full-space law can be compiled to the tiny RTDS/P13 runtime with only about **2.4%** 31-step rollout overhead.

## Stability

Three disjoint DIC-DCC35 fold coefficient cosines:
- 0.999967
- 0.999989
- 0.999990

Median:

**0.9999888**

The recovered law is therefore exceptionally stable across disjoint trajectory subsets.

## Basis consistency

The principal deployment basis is corrected to the exact total-degree<=3 P13 subspace.

Runtime coefficients corresponding to:
- `u^3 a1`
- `u^3 a2`
- `u^3 a3`

are exactly zero for all folds.

## Learned Burgers law

Reporting-only, never used for fitting or gates:

DIC-DCC35 `u*a1` coefficients:
- fold 0: -0.995133
- fold 1: -1.000482
- fold 2: -1.003379

The nonlinear transport term is recovered essentially at unit amplitude.

DIC-DCC35 `a2` coefficients:
- 0.006862
- 0.007002
- 0.007071

Diffusion remains attenuated relative to the Taylor-coordinate reporting-only value 0.02 for nu=0.01, but the joint differential-integral contract materially improves both characteristic and long-horizon behavior.

## Scientific conclusion

PB1-Q7-FIX1 resolves the only failed Q7 gate.

The evidence now supports the following identification architecture:

`Trajectory -> Local Taylor Jet -> Direct Canonical 35-term Differential Law -> Differential-Integral Consistency Solve -> Exact P13 Projection -> Four-Gain Native-Flow Closure -> Tiny RTDS Runtime`

The architecture change is now qualified on the already-observed Burgers nu=0.01 training block.

The next required stage is independent confirmation on unseen physical parameters or a new PDE family. The nu=0.01 official test set must not be reused as fresh confirmation.
