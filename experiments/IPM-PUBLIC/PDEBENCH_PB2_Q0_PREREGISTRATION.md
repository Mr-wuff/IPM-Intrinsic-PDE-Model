# IPM-PDEBench-PB2-Q0 — Reaction-Diffusion Zero-Tuning New-Family Qualification

## Purpose

PB1 Burgers mechanism development is complete.

PB2-Q0 is the first genuinely new-PDE-family qualification of the frozen IPM strong/classical branch.

Target:
- PDEBench 1D Reaction-Diffusion
- train file: `ReacDiff_Nu0.5_Rho1.0.hdf5`
- pinned datafile URL: `https://darus.uni-stuttgart.de/api/access/datafile/133177`
- MD5: `69a429239778d529cd419ed5888ea835`

The first 1,000 trajectories are the sealed official PDEBench forward test block.
No official-test row is loaded until every internal gate passes.

## Why this PDE family

Reaction-Diffusion removes Burgers transport/shock semantics and introduces a qualitatively different coupling:
- nonlinear local reaction;
- diffusion;
- no required advective transport.

The frozen strong branch must discover this structure without using the known equation.

## Frozen strong-branch architecture

Observation:
- FULL1024 for identification.

Differential state:
- Local Taylor jet R4 / degree-5 / order-3;
- `j=(u,a1,a2,a3)`;
- `a_r = d^r u / (r! dx^r)`.

Discovery space:
- DCC35, the complete total-degree<=3 polynomial basis in `(u,a1,a2,a3)`.

Identification:
- DIC joint differential + Simpson-2 integral equations;
- each family normalized by its own target RMS;
- equal dimensionless weight;
- normalized ridge alpha=1e-8;
- no SGD;
- no known reaction/diffusion coefficient.

Deployment projection:
- exact total-degree<=3 P13 RTDS subspace;
- gains fixed to one;
- no compiler-in-loop coefficient fitting.

Runtime:
- existing P13 native strong-flow executor `IPMStep`;
- official PDEBench spatial reduction 4;
- saved-time step directly, temporal reduction 1.

## Data split

Official first 1,000 trajectories: sealed.

After the official block:
- fit fold A: 0:1024
- fit fold B: 1024:2048
- fit fold C: 2048:3072
- validation: 3072:3584
- confirm: 3584:4096

Indices are relative to the 9,000-trajectory training portion.

Saved-time centers:
- 10,20,30,40,50,60,70,80,90

## Frozen internal gates

### I1 — DCC35 characteristic closure
Confirm characteristic Rel-RMS:
- three-fold mean <= 0.10
- max fold <= 0.12.

### I2 — DCC35 integral closure
Confirm Simpson-integral Rel-RMS:
- three-fold mean <= 0.08
- max fold <= 0.10.

### I3 — coefficient stability
Median pairwise standardized DCC35 coefficient cosine >= 0.995.

### I4 — principal-program sufficiency
Confirm P13 characteristic / DCC35 characteristic:
- mean ratio <= 1.20
- max fold ratio <= 1.30.

### I5 — native full-horizon closure
Using official spatial reduction 4 and all future times after PDEBench initial_step=5:
- three-fold mean relative L2 <= 0.06
- max fold <= 0.08.

### I6 — finite native execution
All P13 rollouts finite over the full future horizon.

Only if I1-I6 all pass may the official first 1,000 trajectories be opened.

## Sealed official-test gates

PDEBench forward convention:
- spatial reduction 4;
- temporal reduction 1;
- initial_step=5;
- evaluate every remaining saved time.

### E1 — finite full-horizon rollout
All three programs remain finite.

### E2 — future relative L2
- three-fold mean <= 0.08
- max fold <= 0.10.

### E3 — official PDEBench nRMSE
- three-fold mean <= 0.10
- max fold <= 0.12.

### E4 — OOD-horizon stability
No fold has non-finite state or absolute state magnitude > 10 times the maximum absolute target magnitude.

## Reporting-only physics audit

Only after fitting/gate decisions, report the known generator law:

`u_t = rho*u*(1-u) + nu*u_xx`.

With Taylor coordinate `a2=u_xx/2`, the expected P13 coefficients for Nu=0.5, Rho=1.0 are:
- R(u): `+1*u -1*u^2`;
- D constant: `2*nu = 1`;
- other RTDS coefficients: zero.

Report:
- reaction u and u^2 relative errors;
- diffusion a2 relative error;
- total spurious principal coefficient magnitude;
- nonprincipal DCC35 magnitude.

These known values are never used for fitting or qualification.

## Decision

PB2-Q0 PASS only if I1-I6 and E1-E4 all pass.

If PASS:
- strong DIC-DCC35 -> P13 branch receives new-family support on a non-transport PDE;
- authorize PB2-Q1 parameter/OOD confirmation across additional Nu/Rho pairs;
- no architecture tuning on Nu0.5/Rho1.0 is permitted.

No 500-epoch training is authorized.
