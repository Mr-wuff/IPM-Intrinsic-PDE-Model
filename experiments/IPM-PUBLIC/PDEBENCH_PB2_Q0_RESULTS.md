# IPM-PDEBench-PB2-Q0 Results — Reaction-Diffusion Zero-Tuning New-Family Qualification

## Integrity

Result ZIP SHA256:

`da7317d184926d9ed58ed28a2dfd80dc787df19404d0b443dad4bbddc3b76786`

Detached checksum matches exactly.

Internal result manifest: **15/15 payload entries match** by byte size and SHA256.

Protocol SHA256 embedded in the run:

`9adc985af56371c452d4ab276783c539c78d324bb6998b43682e246a64592c3d`

Executed notebook SHA256:

`8eb325cb31e3778f6133d8b3b8f34c0e07f69ad725f68b9c9a4ec30d1fc7147c`

The executed notebook contains 8 code cells and no error outputs.

The frozen source notebook hash from the run record differs because the user repaired one observed HDF5 indexing failure. The repaired internal-runtime read uses a standard slice:

`tensor[row0:row1, ::tr, ::sr]`

instead of a list of all temporal indices.

For this frozen task `tr=1`, these select exactly the same temporal samples. The embedded frozen protocol is unchanged. This is treated as a protocol-preserving execution repair, not a scientific-condition change.

## Formal outcome

**PB2-Q0 FAIL**

Official test accessed: **false**.

The official first 1,000 trajectories remain sealed.

Frozen internal gates:

- I1 DCC35 characteristic closure: **FAIL**
- I2 DCC35 integral closure: **FAIL**
- I3 coefficient stability: **PASS**
- I4 P13 sufficiency: **FAIL**
- I5 native full-horizon closure: **PASS**
- I6 finite native execution: **PASS**

No external gate is evaluated and no PB2-Q1 parameter/OOD run is authorized.

## Identification metrics

Three independent folds:

Characteristic confirm residual:
- fold 0: 0.451479
- fold 1: 0.453326
- fold 2: 0.452145
- mean: **0.452317**

Integral confirm residual:
- fold 0: 0.445401
- fold 1: 0.446960
- fold 2: 0.445602
- mean: **0.445988**

These strongly miss the frozen I1/I2 gates.

Coefficient cosine median:

**0.998376**

Thus the learned canonical closure is reproducible across folds but not a faithful local generator.

P13 / DCC35 characteristic ratio:
- mean: **1.200878**
- max: **1.208760**

The mean narrowly exceeds the frozen 1.20 gate; the threshold is not relaxed.

## Runtime result

Despite poor governing-law closure, projected P13 native rollouts are stable:

- fold 0: **0.039591**
- fold 1: **0.039175**
- fold 2: **0.039302**
- mean: **0.039356**

All runs remain finite.

Predicted/target absolute maxima stay approximately:
- 1.0092
- 1.0073
- 1.0082

Thus I5/I6 pass comfortably.

This is important negative evidence: trajectory accuracy alone would have made this run look successful, while explicit governing-law recovery fails.

## Reporting-only physical audit

For PDEBench Nu=0.5, Rho=1.0, the known continuum generator is reporting-only:

`u_t = u - u^2 + 0.5*u_xx`.

With the frozen Taylor coordinate `a2=u_xx/2`, the expected principal coefficients are:
- R_u = +1
- R_u2 = -1
- D_const = +1

Recovered P13 coefficients:

### fold 0
- R_u = -3.3817
- R_u2 = +5.8518
- D_const = 0.4231

### fold 1
- R_u = -2.1920
- R_u2 = +3.6468
- D_const = 0.6393

### fold 2
- R_u = -4.8321
- R_u2 = +8.3973
- D_const = 0.3347

Spurious principal L1 magnitude:
- 7.85
- 4.75
- 10.42

Nonprincipal DCC35 L1 magnitude:
- 4.56
- 4.05
- 4.31

The DCC35 closure therefore uses large compensating reaction and mixed-jet terms instead of recovering the physical reaction-diffusion generator.

## Interpretation

PB2-Q0 does not support freezing the generic strong branch across PDE families.

The result separates two properties:

1. **trajectory closure** — already good (Rel-L2 ~0.039);
2. **governing-law identifiability** — poor (DIC residual ~0.45 and incorrect explicit coefficients).

Because the wrong explicit law is seed/fold-stable, the next step should be a causal identifiability audit, not a threshold relaxation or longer training.

Priority hypotheses:
- saved-time/jet DIC contract may be inconsistent with the exact Reaction-Diffusion generator;
- the single-parameter trajectory manifold may be insufficiently excited, allowing highly correlated DCC35 terms to compensate each other;
- DCC35 may be too redundant for this state manifold even though P13/native rollout is adequate;
- early-time transients may contain substantially more identification information than the sparse centers 10,20,...,90.

The next run must keep the official test sealed and directly compare the reporting-only exact generator, DCC35, and direct-P13 identification across time/excitation regimes.
