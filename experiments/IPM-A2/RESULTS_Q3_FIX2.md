# IPM-A2-Q3-FIX2 Results — Principal Normal-Form Calibration Compiler

## Integrity

Formal decision: **A2_Q3_FIX2_PASS**

Result ZIP SHA256:
`f55c97725c51e82cbe76c981eaa66337b65cb9df98951d0b2566fc6b9a76cedc`

The supplied SHA256 matches exactly.

The executed notebook has 12 code cells. One implementation-only runtime repair changes
`program.coeffs[r].tolist()`
to
`list(program.coeffs[r])`
because the optimized frozen coefficient representation is a tuple. No hypothesis, selected program, coefficient, data split, or evaluation rule is changed.

## Gates

Passed:
- G0 parent/data integrity
- G1 disjoint calibration
- G2 finite 40-step rollout, 3/3 seeds
- G3 physical reliability
- G4 batch-16 speed
- G5 batch-1 speed
- G6 noise robustness
- G8 role-mask reproducibility
- G9 effective scalar budget

Failed:
- G7 resolution /4 transfer, due to Advection.

## Frozen selected programs

All three Advection seeds select:
[
T
]
only.

Transport gains:
- seed101: 1.076665
- seed202: 1.083100
- seed303: 1.071138

All three Burgers seeds select:
[
T+D+S.
]

Burgers gains:
- T: 0.97669 / 0.99699 / 0.98443
- D: 1.09369 / 1.05973 / 1.07577
- S: 0.75883 / 0.75674 / 0.89568

Thus role-mask selection is perfectly reproducible across the three formal seeds.

## Accuracy

Mean 40-step Rel-L2:
- Advection beta=1: **0.07976**
- Burgers nu=0.01: **0.19280**

Per-seed Advection:
- 0.07756
- 0.04966
- 0.11206

Per-seed Burgers:
- 0.19276
- 0.19354
- 0.19209

Compared with Q3-FIX1:
- Advection: 0.19574 -> 0.07976 (**59.3% lower error**)
- Burgers: 0.19093 -> 0.19280 (essentially unchanged, +0.98%)

The remaining rollout is finite and smoothly accumulating.

## Horizon

Advection mean:
- h1 0.00356
- h5 0.01167
- h10 0.02170
- h20 0.04142
- h40 0.07976

Burgers mean:
- h1 0.03695
- h5 0.07838
- h10 0.11538
- h20 0.15919
- h40 0.19280

## Robustness

Advection:
- native 0.07976
- 1% noise 0.07976
- /2 0.09123 (1.144x)
- /4 0.18340 (2.299x) — fails frozen /4 transfer gate

Burgers:
- native 0.19280
- 1% noise 0.19293
- /2 0.18618
- /4 0.19216

The principal normal form is essentially invariant to the 1% observation-noise perturbation. Burgers is also strongly resolution-stable. Advection loses relative accuracy at the coarsest /4 resolution.

## Current-hardware end-to-end speed

Official NeuralOperator FNO is re-timed in the same run.

### Batch 1

Advection:
- IPM: 0.511 ms
- FNO: 4.552 ms
- **9.14x speedup**

Burgers:
- IPM: 0.921 ms
- FNO: 4.225 ms
- **4.63x speedup**

### Batch 16

Advection:
- IPM: 0.330 ms
- FNO: 3.364 ms
- **10.22x speedup**

Burgers:
- IPM: 0.864 ms
- FNO: 3.587 ms
- **4.15x speedup**

Batch-16 IPM throughput:
- Advection: ~12.45 million grid-points/s
- Burgers: ~4.74 million grid-points/s

## Compactness

Effective scalar state:
- Advection: 36 scalars = frozen 35 IDTC trainable values + 1 calibrated gain
- Burgers: 38 scalars = frozen 35 + 3 calibrated gains

Compiled JSON programs are only ~0.43-0.57 KiB.

## Architecture interpretation

The development path is now:

[
u
ightarrow J^3u
ightarrow 	ext{35-parameter IDTC}
ightarrow 	ext{canonical differential algebra}
ightarrow 	ext{principal normal form}
ightarrow 	ext{native PDE program}.
]

At deployment, the Q3-FIX2 program no longer evaluates the IDTC or constructs a Local Taylor Jet.

Advection executes only a learned nonlinear transport polynomial plus periodic semi-Lagrangian transport.

Burgers executes learned transport plus calibrated diffusion/dispersion normal forms and one fused spectral linear step.

This is the first formal PASS in the speed-first public PDEBench line.

## Remaining limitation

Advection /4 resolution transfer fails (2.299x native error). This must remain visible in the paper and later benchmark.

The next experiment is execution-only: preserve the frozen Q3-FIX2 mathematics and investigate GPU-parallel/fused execution, CUDA Graph replay and kernel-launch reduction before broad benchmarking.
