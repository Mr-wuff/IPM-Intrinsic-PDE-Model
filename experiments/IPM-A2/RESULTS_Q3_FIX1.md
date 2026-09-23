# IPM-A2-Q3-FIX1 Results — Canonical Differential-Algebra Compiler

Formal decision: **A2_Q3_FIX1_FAIL**

Result ZIP SHA256:
`fbf93087ce7546f972d72d759b998fecafba48cab5c82a9bcb748cae51aef273`

The supplied SHA256 matches exactly. The executed notebook has 12 code cells and all 12 code cells are byte-for-byte identical to the frozen Q3-FIX1 notebook.

Passed gates: F0, F1, F2, F3, F6, F7, F8.
Failed gates: F4 physical reliability and F5 end-to-end speed.

## Stability repair

Q3 Advection mean 40-step Rel-L2 was ~4.21e14. Q3-FIX1 reduces this to 0.19574 +/- 0.01574.

Burgers improves from 0.47204 to 0.19093 +/- 0.00274.

All three seeds remain finite through 40 steps.

Mean horizon errors:

Advection: h1 0.01041, h5 0.03140, h10 0.05654, h20 0.10483, h40 0.19574.

Burgers: h1 0.03708, h5 0.07720, h10 0.11345, h20 0.15696, h40 0.19093.

The catastrophic instability is gone; remaining error accumulates smoothly.

## Robustness

Advection:
- native 0.19574
- 1% noise 0.19309
- N/2 0.20094
- N/4 0.24905

Burgers:
- native 0.19093
- 1% noise 0.19108
- N/2 0.18455
- N/4 0.19107

Noise and resolution gates pass.

## Accuracy limitation

Formal floors:
- Advection <=0.12
- Burgers <=0.35

Burgers passes. Advection does not.

The frozen algebra's dominant Advection transport coefficient remains about -0.89 to -0.91 rather than the beta=1 reference magnitude. The smooth horizon curve is consistent with accumulated phase-speed bias rather than numerical explosion.

## Speed

Advection:
- compiler 3.134 ms
- official frozen FNO 7.983 ms
- 2.55x faster

Burgers:
- compiler 3.434 ms
- official frozen FNO 3.433 ms
- approximately equal speed

Therefore the >=2x gate fails on Burgers.

## Deployment complexity bottleneck

The selected compiled programs still retain nuisance monomials.

Advection nuisance counts: 14 / 4 / 4.
Burgers nuisance counts: 7 / 14 / 14.

These nuisance terms require Local Taylor Jet construction during every deployment step and repeated derivative-product evaluation.

The principal normal-form families depend only on u after compilation:
- reaction R(u)
- transport f1(u) ux
- diffusion f2(u) uxx
- dispersion f3(u) uxxx

Removing the nuisance runtime path is therefore the most direct speed repair.

## Principal-law evidence

Burgers transport coefficients remain:
- seed101: -1.00946 u*ux
- seed202: -0.98822 u*ux
- seed303: -1.00782 u*ux

Thus FIX1 preserves the nonlinear transport structure learned by the 35-parameter IDTC.

Advection transport remains approximately -0.89 to -0.91 ux.

## Scientific conclusion

Q3-FIX1 is a failed formal gate but a successful mechanism repair:

1. canonical differential-role compilation solves the long-horizon stability failure;
2. the frozen 35-parameter IDTC contains a stable deployable principal PDE structure;
3. Burgers reaches ~0.19 40-step error;
4. Advection is now limited mainly by phase/coefficient calibration;
5. nuisance monomials are the leading deployment-cost liability.

Next: principal-normal-form deployment with nuisance-free runtime and training-side-only calibration of a few generic role amplitudes.