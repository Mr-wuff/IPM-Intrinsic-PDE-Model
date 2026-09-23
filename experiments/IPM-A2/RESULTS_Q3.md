# IPM-A2-Q3 Results — Intrinsic Principal-Flow Compiler

## Integrity

Frozen decision: **A2_Q3_FAIL**

Result ZIP SHA256:
`81b7f82937e6039512de903b212651040e0eacd30862758389c2186ef41a081f`

The supplied `.sha256` matches exactly.

The executed notebook contains 11 code cells and is byte-for-byte identical to the frozen Q3 notebook.

All parent/data/compiler-equivalence integrity checks passed.

## Gate outcome

Passed:
- Q3-0 parent/data integrity
- Q3-1 calibration-only degree selection
- Q3-2 finite 40-step output
- Q3-4 end-to-end speed
- Q3-6 resolution robustness under the selected stable D1 flow
- Q3-7 degree reproducibility

Failed:
- Q3-3 physical reliability
- Q3-5 noise robustness

All six seed/task cases selected D1.

## Formal rollout

Advection beta=1:
- seed 101: 8.94e14
- seed 202: 3.61e14
- seed 303: 8.75e12
- mean: 4.21e14

Burgers nu=0.01:
- seed 101: 0.472352
- seed 202: 0.471577
- seed 303: 0.472204
- mean: 0.472044

Advection remains accurate for the first few steps:
- step 1: ~0.014-0.016
- step 5: ~0.061-0.071
then blows up between horizons 5 and 10.

Burgers remains finite and monotonic but plateaus at insufficient accuracy.

## Speed

Mean end-to-end macro-step latency:

Advection:
- IPFC: 1.516 ms
- official frozen FNO: 7.983 ms
- speedup: 5.27x

Burgers:
- IPFC: 1.567 ms
- official frozen FNO: 3.433 ms
- speedup: 2.19x

Thus the speed target is reproducibly met.

## Mechanism diagnosis

The Q3 compiler handles only first- and second-derivative principal contributions specially:
- first derivative -> semi-Lagrangian transport
- second derivative -> exponential diffusion

All remaining learned terms are placed into an explicit residual source.

This is insufficient for the frozen Q2 IDTC algebra.

### Advection

Q2 linear algebra contains approximately:
- c1 on a1 = -0.89 to -0.91
- c3 on a3 = about -5.3e-5 to -6.0e-5

Because
[
a_3=u_{xxx}/6,
]
the physical third-derivative coefficient is about
[
gammaapprox-9	imes10^{-6}	ext{ to }-1.0	imes10^{-5}.
]

At N=256, L=1, dt=0.01, the Nyquist stiffness scale is
[
Delta t |gamma| k_{max}^3 approx 46-52.
]

The Q3 explicit residual correction is therefore catastrophically unstable even though the learned a3 coefficient is numerically tiny.

This exactly matches the resolution evidence:
- native N=256: catastrophic growth
- N/2: stable ~0.29-0.33
- N/4: stable ~0.28-0.31

### Burgers

Q2 learned the dominant nonlinear transport coefficient accurately:
[
2A_{a_0,a_1}approx -1.
]

However D2/D3 Q3 calibration becomes non-finite under the incomplete principal-flow compiler, so calibration selects D1 for every seed.

D1 removes the learned u*u_x interaction. The compiled Burgers flow therefore has near-zero transport velocity and behaves mostly as diffusion:
- velocity RMS ~0.001-0.004
- diffusion median ~0.0032

This explains why Q3 is stable but inaccurate at ~0.472.

## Scientific conclusion

Q3 does not falsify the learned 35-parameter IDTC law.

It falsifies the **incomplete compiler** that treats higher-order derivative contributions as explicit source terms and selects polynomial degree as one indivisible block.

The next compiler must:

1. preserve the nonlinear first-derivative transport structure learned by IDTC;
2. compile all linear derivative orders into a stability-compatible symbol flow, including dispersive odd-order terms;
3. separate algebraic degree from derivative order;
4. use calibration-only selection without access to the true PDE formula;
5. keep the end-to-end speed advantage.

The correct next test is a full-symbol / quasilinear normal-form compiler, not another larger neural model.
