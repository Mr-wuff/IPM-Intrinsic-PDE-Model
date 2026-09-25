# IPM-PDEBench-PB1-Q8-FIX2 — Conservative Native-Flow Qualification

## Motivation

PB1-Q8-FIX1 established:

- the raw DIC-DCC35 Burgers law at epsilon=0.001 is physically close to the pinned PDEBench generator;
- higher spatial point resolution does not reduce the strong-form oracle residual;
- alternative local/spectral jet estimators do not pass the frozen repair threshold;
- the current semi-Lagrangian IPMStep still yields about 0.337 exact-law 31-step Rel-L2 at N=256;
- five raw-time substeps improve that only to about 0.272;
- gain closure distorts already-correct coefficients substantially while improving rollout by only about 9.5%.

The remaining route is therefore a native-runtime repair.

The key structural observation is that the P13 transport role

`u_t = T(u) u_x + ...`

has an exact conservation-law form

`u_t + dF(u)/dx = ...`

with

`F'(u) = -T(u)`.

For the Burgers law `T(u)=-u`, this gives `F(u)=u^2/2`.

For smooth solutions the characteristic and conservative forms agree. Near shocks, only the conservative flux form defines the correct weak/entropy solution.

Q8-FIX2 tests whether a parameter-free strong-to-weak conservative compiler repairs the low-viscosity runtime.

## Frozen data

PDEBench:
- file: `1D_Burgers_Sols_Nu0.001.hdf5`
- official test first 1,000 trajectories remain sealed.

Only the Q8/Q8-FIX1 training-block confirm rows are used.

## Frozen laws

No re-identification occurs.

The three N=256 DIC-DCC35 coefficient vectors from PB1-Q8-FIX1 are embedded and projected to exact P13.

All runtime gains are fixed to 1.

A reporting-only exact-law oracle is also evaluated:

`Q = -u*a1 + (2*epsilon/pi)*a2`.

## Runtime controls

### Legacy control

Current `IPMStep`:
- semi-Lagrangian transport;
- existing spectral diffusion/dispersion;
- current reaction splitting.

Evaluate with:
- one coarse official-interval step;
- five raw-time substeps.

### Conservative control — FV1

Replace only the transport backend by first-order local Lax-Friedrichs/Rusanov finite-volume flux.

The flux polynomial is compiled analytically from the learned transport polynomial:

If

`T(u)=c0+c1*u+c2*u^2+c3*u^3`,

then

`F(u)=-(c0*u+c1*u^2/2+c2*u^3/3+c3*u^4/4)`.

Use periodic boundaries and Rusanov interface flux:

`H = 0.5(F_L+F_R) - 0.5*a*(u_R-u_L)`

with

`a=max(|F'(u_L)|,|F'(u_R)|)=max(|-T(u_L)|,|-T(u_R)|)`.

All non-transport roles keep the same runtime semantics as the frozen P13 law.

### Primary candidate — FV2-MC

Use the same conservative flux, with second-order MUSCL reconstruction and the monotonized-central limiter:

`slope = minmod(2*du_L, 0.5*(du_L+du_R), 2*du_R)`.

Advance the conservative transport substep with SSP-RK3.

For each official interval use exactly five raw-time substeps.

No parameter is learned or searched.

FV1 is diagnostic; all formal gates apply to FV2-MC.

## Frozen gates

Let:
- `E_legacy_oracle` = exact-law legacy IPMStep, five substeps;
- `E_fv2_oracle` = exact-law FV2-MC, five substeps;
- `E_legacy_learned` = mean three-fold learned-law legacy IPMStep, five substeps;
- `E_fv2_learned` = mean three-fold learned-law FV2-MC, five substeps.

### C1 — exact-law conservative closure

`E_fv2_oracle <= 0.22`

### C2 — conservative improvement

`E_fv2_oracle / E_legacy_oracle <= 0.80`

### C3 — learned-law runtime closure

Three-fold learned FV2-MC:
- mean 31-step Rel-L2 <= 0.25
- max fold <= 0.28

### C4 — runtime/law separation

`E_fv2_learned / E_fv2_oracle <= 1.20`

### C5 — learned improvement over frozen legacy executor

`E_fv2_learned / E_legacy_learned <= 0.90`

### C6 — exact-law conservation

For the exact-law FV2-MC rollout, maximum relative periodic-domain mean drift over 31 official steps <= `1e-4`.

### C7 — finite execution

All exact-law and three learned FV2-MC trajectories remain finite for all 31 steps.

## Decision

If C1-C7 all pass:

**Conservative transport compilation is runtime-qualified for P13 transport laws.**

Authorize the runtime transition:

`semi-Lagrangian T(u)u_x executor -> conservation-law flux compiler + FV2-MC native transport`

for conservation-form P13 transport.

This does not alter DIC-DCC35 identification and does not unlock the already-used epsilon=0.001 parameter as a fresh independent confirmation.

The next independent confirmation must use a new viscosity parameter not used in Q2-Q8-FIX2.

No 500-epoch training is authorized.
