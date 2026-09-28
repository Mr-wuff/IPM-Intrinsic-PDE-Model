# IPM-PDEBench-PB2-Q1-FIX2 Results — Discrete-Generator / Finite-Time Semigroup Attribution

## Integrity

Result ZIP SHA256:

`583f402961cec1fb03639bfe635f0454f84145a1c4ce0df34b60615ee7ba8fb9`

Detached checksum matches exactly.

Internal result manifest: **10/10 tracked payload entries match** by byte size and SHA256.

Protocol SHA256:

`569376bfe0d00cfb3d2e77de93dca0789ebb145357e3ea6cbdb954c60f5ba778`

Frozen source notebook SHA256:

`b5f45244a20f9203c30951d81c26ebe17c0af1a9fbcba9e184cd827e0ebbaa80`

Executed notebook SHA256:

`f6a922b927acab2b516dc098508bf765c0f5d4e0c286b3fd173a93b72d93ec7e`

Direct cell-source comparison against the frozen notebook found **zero source differences**. The hash difference is caused only by execution outputs / metadata.

The executed notebook has 7 code cells and no runtime errors.

Official test accessed: **false**.

## Frozen attribution result

Independent recomputation reproduces:

- B1 spatial derivative mismatch: **false**
- B2 finite-time semigroup closure: **true**
- B3 discrete-vs-continuum semigroup advantage: **false**
- B4 semigroup convergence: **true**
- B5 effective diffusion mismatch: **false**

Primary route:

**FINITE_TIME_SEMIGROUP_CONTRACT_CONFIRMED**

No support change, official-test unlock, architecture transition, or long training is authorized by this attribution run.

## True-law saved-time oracle residuals

Using the true continuum coefficients:

### Nu1 / Rho2
- LocalTaylor S2: **1.2034**
- LocalTaylor TR1: **1.1885**
- FD2 S2: **9.5470**
- FD2 TR1: **9.4238**
- spectral S2: **17.8511**
- spectral TR1: **17.6205**

### Nu1 / Rho5
- LocalTaylor S2: **0.7452**
- LocalTaylor TR1: **0.6413**
- FD2 S2: **5.9121**
- FD2 TR1: **5.0842**
- spectral S2: **11.0544**
- spectral TR1: **9.5064**

### Nu1 / Rho10
- LocalTaylor S2: **0.5674**
- LocalTaylor TR1: **0.4767**
- FD2 S2: **4.5013**
- FD2 TR1: **3.7792**
- spectral S2: **8.4164**
- spectral TR1: **7.0663**

Thus an instantaneous true generator integrated only through saved-time Simpson/trapezoid observations is badly aliased under strong diffusion.

FD2/spectral derivatives are actually worse in the instantaneous quadrature audit because they faithfully retain stiff high-frequency diffusion rates that decay inside the unobserved subinterval.

## One-save-step semigroup replay

The exact physical coefficients are then used in finite-time split flow:

- exact logistic reaction;
- exact continuum or periodic-FD2 diffusion semigroup;
- Strang composition.

### Nu1 / Rho2

Screen, discrete-FD2 Strang:
- state Rel-L2: **0.000310**
- increment Rel-L2: **0.022960**

Confirm:
- state Rel-L2: **0.000311**
- increment Rel-L2: **0.023073**

### Nu1 / Rho5

Screen:
- state Rel-L2: **0.000221**
- increment Rel-L2: **0.016212**

Confirm:
- state Rel-L2: **0.000214**
- increment Rel-L2: **0.015584**

### Nu1 / Rho10

Screen:
- state Rel-L2: **0.000233**
- increment Rel-L2: **0.010952**

Confirm:
- state Rel-L2: **0.000221**
- increment Rel-L2: **0.010295**

B2 passes in all three environments.

## Microstep convergence

For all environments, m=1,2,4,8,16,32 are almost identical.

Example screen increment Rel-L2:

### Rho2
- m1: 0.022964
- m16: 0.022960
- m32: 0.022960

### Rho5
- m1: 0.016221
- m16: 0.016212
- m32: 0.016212

### Rho10
- m1: 0.010973
- m16: 0.010952
- m32: 0.010951

Thus a single Strang step per saved interval is already on the finite-time replay plateau.

B4 passes in all environments.

## Continuum versus discrete diffusion semigroup

Continuum-spectral Strang and discrete-FD2 Strang are numerically indistinguishable at the reported precision.

Therefore B3 is false: there is no meaningful discrete-grid semigroup advantage in these trajectories.

This supports use of the continuum spectral diffusion semigroup as the native smooth diffusion compiler.

## Effective diffusion scan

Reporting-only discrete-FD2 Strang m=16 scan:

Best nu_eff in all three held-out environments:

`nu_eff = 1.0`

### Rho2
- nu=1 increment Rel-L2: **0.022960**
- nu=0.67: 0.221246
- nu=1.2: 0.123699

### Rho5
- nu=1: **0.016212**
- nu=0.67: 0.119505
- nu=1.2: 0.067189

### Rho10
- nu=1: **0.010952**
- nu=0.67: 0.088008
- nu=1.2: 0.049085

Therefore B5 is false.

The HDF5 Nu=1 attribute is fully consistent with the finite-time trajectory when the correct semigroup semantics are used.

## Source provenance diagnostic

Public HDF5:
- N=1024
- L=1
- dt_save≈0.01
- attributes Nu/rho match filenames.

Pinned multi YAML for Nu=1:
- nx=512
- CFL=0.25.

This repository/public-data resolution discrepancy remains a provenance note, but it does not explain the physical trajectory mismatch because the actual-HDF5-grid continuum and FD2 semigroups both close the one-step map.

## Scientific conclusion

FIX2 resolves the Nu=1 diffusion-axis attribution.

The Reaction-Diffusion law and public parameter semantics are not the problem.

The failure comes from using sparse saved frames to approximate the integral of a **stiff instantaneous diffusion generator**.

High-frequency diffusion rates are large instantaneously but decay inside the unobserved subinterval. A saved-time S2/TR1 quadrature therefore cannot faithfully invert the infinitesimal coefficient, which explains the systematic D0 attenuation seen in Q1/FIX1.

In contrast, the finite-time native flow:

`reaction exact flow -> diffusion semigroup -> reaction exact flow`

reproduces the public trajectory extremely accurately with the true coefficients.

The next experiment should freeze:
- support [R_u,R_u2,D0];
- continuum spectral diffusion semigroup;
- one Strang step per saved interval;

and perform **compiler-in-loop nonlinear coefficient identification** directly against one-step trajectory increments.

If that independently recovers the three physical coefficients and passes the still-sealed official block without refitting, PB2 Reaction-Diffusion can be frozen.
