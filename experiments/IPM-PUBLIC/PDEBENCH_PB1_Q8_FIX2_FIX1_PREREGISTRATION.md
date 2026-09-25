# IPM-PDEBench-PB1-Q8-FIX2-FIX1 — CFL-Aware Conservative Native-Flow Qualification

## Motivation

PB1-Q8-FIX2 introduced the correct structural runtime candidate:

`T(u)u_x -> -dF(u)/dx, with F'(u)=-T(u)`

followed by conservative finite-volume execution.

However, every FV1/FV2 run became non-finite because the preregistered fixed-five-substep execution contract violated the explicit finite-volume CFL stability condition.

The executed run records:
- N=256
- dx=0.00390625
- saved-data dt≈0.01
- five FV substeps per official interval -> dt_FV≈0.01

For Burgers wave speeds O(1), the nominal Courant number is already O(2.56), before accounting for the actual maximum state amplitude.

The pinned PDEBench multi-solution Burgers generator uses adaptive explicit stepping with:

`CFL=0.25`.

Q8-FIX2-FIX1 changes **only** the invalid fixed-substep time contract.

No law, basis, flux, limiter, split order, performance threshold, or official-test policy is changed.

## Frozen laws

Use exactly:
- the reporting-only exact epsilon=0.001 Burgers law;
- the three N=256 DIC-DCC35 laws frozen in PB1-Q8-FIX1.

DIC-DCC35 identification is not rerun.

All gains are fixed to one.

## Frozen conservative compiler

For the P13 transport polynomial

`T(u)=c0+c1*u+c2*u^2+c3*u^3`,

compile

`F(u)=-(c0*u+c1*u^2/2+c2*u^3/3+c3*u^4/4)`.

No parameter is learned.

## Runtime controls

### Legacy control

Current semi-Lagrangian `IPMStep`, five saved-time substeps per official interval.

### FV1 diagnostic

Piecewise-constant Rusanov flux with adaptive CFL subcycling.

### Formal candidate: FV2-MC-CFL

- MUSCL reconstruction;
- monotonized-central limiter;
- Rusanov interface flux;
- SSP-RK3 conservative transport;
- existing reaction/diffusion/dispersion role semantics;
- adaptive subcycling inside every official interval.

## CFL policy

Frozen:

`CFL_target = 0.25`

taken directly from the pinned PDEBench multi-solution Burgers generator for epsilon=0.001.

At every conservative substep:

`dt_step = min(dt_remaining, CFL_target*dx/max(|F'(u)|))`.

Use the global maximum wave speed over the current batch and domain.

No CFL search is permitted.

Safety:
- maximum 4096 substeps per official interval;
- every accepted substep must satisfy observed Courant <=0.250001;
- all 31 official intervals must be completed.

## Formal gates

The Q8-FIX2 accuracy/conservation gates are retained unchanged.

### C0 — CFL contract

For exact-law and all three learned FV2-MC-CFL runs:
- all 31 intervals complete;
- no interval exceeds 4096 substeps;
- maximum observed Courant <= 0.250001.

### C1 — exact-law conservative closure

Exact-law FV2-MC-CFL 31-step Rel-L2 <= **0.22**.

### C2 — conservative improvement

Exact-law FV2-MC-CFL / exact-law legacy-five-substep <= **0.80**.

### C3 — learned-law runtime closure

Three learned FV2-MC-CFL programs:
- mean 31-step Rel-L2 <= **0.25**
- max fold <= **0.28**

### C4 — runtime/law separation

learned FV2 mean / exact-law FV2 <= **1.20**.

### C5 — learned improvement over legacy

learned FV2 mean / learned legacy-five-substep mean <= **0.90**.

### C6 — exact-law conservation

Maximum relative periodic-domain mean drift over all 31 official steps <= **1e-4**.

### C7 — finite execution

All exact-law and learned FV2 trajectories remain finite.

## Latency

Measure same-hardware batch-64 latency and average/max adaptive substeps per official interval.

Latency is diagnostic only and is not a qualification gate at this stage.

## Decision

If C0-C7 all pass:

**CFL-aware conservative transport compilation is runtime-qualified for P13 conservation-form transport laws.**

Authorize:

`semi-Lagrangian transport -> conservative flux compiler + FV2-MC-CFL executor`

for conservation-form P13 transport.

No official test trajectory is opened in this run.

The next independent confirmation must use a Burgers viscosity not used in Q2-Q8-FIX2-FIX1.

No 500-epoch training is authorized.
