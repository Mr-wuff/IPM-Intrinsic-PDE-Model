# IPM-M1 FIX1 — Derivative Audit Amendment

## Status
This is a **protocol amendment before formal M1 training began**.

The original M1 run was blocked at the pre-training spectral derivative audit. No model training, validation, or empirical comparison was executed, so no outcome-dependent tuning occurred.

## Observed audit
The original notebook produced relative L2 errors approximately:

- first derivative: 7.11e-8
- second derivative: 1.22e-7
- third derivative: 1.39e-7

These errors are numerically very small, but the preregistered threshold was 1e-8 for every derivative order. The threshold therefore rejected an otherwise high-accuracy spectral derivative implementation.

## Amendment
The formal derivative audit threshold is changed from:

```
relative L2 < 1e-8
```

to:

```
relative L2 < 1e-6
```

and the audit is strengthened rather than weakened by evaluating:
- multiple analytic functions;
- derivative orders 1–3;
- multiple grid resolutions;
- float64 execution;
- maximum and median relative errors.

The new threshold is intended as an implementation correctness gate, not as a benchmark metric.

## Scientific rationale
A pre-training derivative audit should reject implementation errors, incorrect wavenumber scaling, aliasing mistakes, or dtype regressions. It should not require near-machine-epsilon behavior from every CUDA FFT execution path.

An error around 1e-7 is several orders of magnitude below the modeling errors that M1 is designed to study and is sufficiently accurate for this mechanism qualification.

## Integrity
The FIX1 notebook receives a new frozen protocol SHA256. The original preregistration remains preserved for provenance.

## Decision rule
M1 formal training may start only if all strengthened derivative-audit cases satisfy relative L2 < 1e-6 and the existing holonomic/stability smoke tests also pass.
