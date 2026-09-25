# IPM-PDEBench-PB1-Q8-FIX3 — Weak Conservative Flux-Core Qualification

## Motivation

PB1-Q8-FIX2-FIX1 repaired the low-viscosity native executor:

- exact-law legacy SL5 Rel-L2: `0.272472`
- exact-law FV2-MC-CFL Rel-L2: `0.009638`
- exact-law mean drift: `6.75e-5`
- learned-law legacy mean: `0.263593`
- learned-law FV2-MC-CFL mean: `0.088384`

Seven of eight frozen gates passed. Only C4 failed because the exact-law conservative runtime became much more accurate than the strong-form DIC-DCC35 -> P13 learned law.

The frozen learned P13 programs retain nonzero reaction/source polynomials and show 4.7%-12.2% periodic-domain mean drift under the conservative executor.

The next stage therefore changes the **identification representation only for an empirically detected conservation-law regime**.

## New internal split

The official first 1,000 trajectories remain sealed.

To avoid reusing Q8's development rows for the new identification rule, Q8-FIX3 uses previously unused training-block rows:

- weak fit fold A: 4352:5376
- weak fit fold B: 5376:6400
- weak fit fold C: 6400:7424
- weak validation: 7424:7936
- weak confirm: 7936:8448

All indices are relative to the 9,000-trajectory official training block after skipping the first 1,000 official test trajectories.

## Conservation-regime detector

Before fitting a conservative law, measure normalized spatial-mean drift on the new fit/validation blocks.

A conservative branch may be activated only if:

`max_t |mean(u_t)-mean(u_0)| / RMS(u_0) <= 1e-3`

on all three fit folds and validation.

No known Burgers equation or coefficient is used in this detector.

## Weak Conservative Flux Core (WCFC-5)

Assume only the scalar periodic conservation-diffusion form:

`u_t + dF(u)/dx = kappa*u_xx`.

Use a generic polynomial flux:

`F(u)=f1*u + f2*u^2 + f3*u^3 + f4*u^4`.

Unknown scalars:

`theta = [f1,f2,f3,f4,kappa]`.

No reaction/source term is present once the data-driven conservation detector activates.

This is not Burgers hard-coding: the four flux coefficients and diffusion coefficient are all identified from trajectories.

## Weak trajectory equations

Use periodic Fourier test functions for modes m=1..32, both sine and cosine.

For every trajectory/time center:

### Differential weak equation

`<phi,(u_+-u_-)/(2dt)> = <phi_x,F(u_0)> + kappa<phi_xx,u_0>`.

### Integral weak equation

`<phi,u_+-u_-> = (dt/3) [B(u_-)+4B(u_0)+B(u_+)]`

where

`B(u)=<phi_x,F(u)> + kappa<phi_xx,u>`.

The differential and integral equation families are normalized by their own target RMS and stacked with equal dimensionless weight.

All equations are linear in the five unknown coefficients and are solved by normalized ridge normal equations with alpha=`1e-8`.

No pointwise spatial derivative of the observed field is used.

## Frozen runtime

Compile WCFC-5 to P13:

- `T(u) = -F'(u)`
- `D = 2*kappa`
- `R = 0`
- `S = 0`

All gains are fixed to one.

Execute with the already-qualified structural candidate:
- conservative flux compiler;
- MUSCL + MC limiter;
- Rusanov flux;
- SSP-RK3;
- adaptive CFL target 0.25.

## Controls

On the new confirm block:
- reporting-only exact law;
- three previously frozen strong DIC-DCC35 -> P13 laws;
- three new WCFC-5 laws.

Known Burgers coefficients are reporting-only and never used in fitting/gates.

## Frozen gates

### W0 — conservation-regime evidence

All three weak-fit folds and validation satisfy normalized spatial-mean drift <= `1e-3`.

### W1 — weak differential-integral fit

On weak confirm, WCFC-5 normalized weak residual:
- three-fold mean <= `0.10`
- max fold <= `0.12`.

### W2 — coefficient stability

Median pairwise cosine of the three normalized 5-scalar WCFC vectors >= `0.995`.

### W3 — conservative runtime closure

Three WCFC FV2-MC-CFL programs:
- mean 31-step Rel-L2 <= `0.03`
- max fold <= `0.04`.

### W4 — repair of Q8-FIX2-FIX1 C4

`WCFC_runtime_mean / exact_runtime <= 1.20`.

### W5 — causal improvement over strong-form law

`WCFC_runtime_mean / frozen_strong_DIC_runtime_mean <= 0.50`.

### W6 — conservation

For each WCFC program, maximum relative periodic-domain mean drift over 31 official steps <= `1e-4`.

### W7 — finite/CFL execution

All WCFC trajectories remain finite; all 31 intervals complete; maximum observed Courant <= `0.250001`.

## Decision

If W0-W7 all pass:

**WCFC-5 is qualified as the conservation-law identification branch for scalar periodic transport-diffusion regimes.**

Authorize the regime-dependent native path:

`trajectory conservation detected -> weak flux identification -> conservative flux compiler -> FV2-MC-CFL executor`.

DIC-DCC35 remains the generic strong-form canonical identifier for smooth regimes.

No official epsilon=0.001 test trajectory is opened in Q8-FIX3.

The next independent confirmation must use a new viscosity not used in Q2-Q8-FIX3, preferably `epsilon=0.002` or `0.004`.

No 500-epoch training is authorized.
