# IPM-A2-Q4 — Parallel Native Execution Qualification

## Objective

Q3-FIX2 is the first formal PASS in the speed-first PDEBench line:

- Advection 40-step Rel-L2: 0.07976
- Burgers 40-step Rel-L2: 0.19280
- batch-1 speedup vs official NeuralOperator FNO: 9.14x / 4.63x
- batch-16 speedup: 10.22x / 4.15x
- effective scalar state: 36 / 38

Q4 does **not** change the learned PDE, role mask, calibrated gain, numerical method, or public-test prediction.

It asks whether the frozen principal normal-form program can be executed as a more efficient GPU-parallel graph.

## Frozen mathematics

Required Q3-FIX2 result SHA256:
`f55c97725c51e82cbe76c981eaa66337b65cb9df98951d0b2566fc6b9a76cedc`

Required Q0 result SHA256:
`6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`

No training or coefficient fitting is allowed.

The selected programs and coefficients are loaded directly from Q3-FIX2.

## Current dependency graph

### Advection T program

[
u
ightarrow f_T(u)
ightarrow v
ightarrow x_d
ightarrow 	ext{periodic interpolation}
ightarrow u^{n+1}.
]

The computation is serial at the operator level, but massively parallel over grid points and batch elements.

### Burgers TDS program

[
u
ightarrow 	ext{transport}
ightarrow 	ilde u
]

then the diffusion and dispersion coefficient branches are independent:

[
	ilde u ightarrow 
u(	ilde u),
qquad
	ilde u ightarrow gamma(	ilde u),
]

followed by one fused Fourier linear flow:

[
hat u
leftarrow
exp[(-
u k^2+gamma(ik)^3)Delta t]hat u.
]

## Execution variants

E0. **Frozen eager**
- exact Q3-FIX2 implementation.

E1. **Tensor-fused eager**
- fixed-shape step module;
- cached grids/wavenumbers;
- T/D/S polynomial evaluation without Python loops;
- D/S coefficient evaluation fused where applicable;
- exact same mathematical step.

E2. **torch.compile**
- compile E1 with `mode="reduce-overhead"`;
- static program, static shape;
- fall back gracefully if unsupported.

E3. **CUDA role streams**
- after transport, launch D and S coefficient/reduction branches on independent CUDA streams;
- synchronize only before the fused spectral step;
- exact same mathematics.

E4. **CUDA Graph single-step replay**
- capture the full static physical step;
- fixed input/output storage;
- replay repeatedly with minimal host launch overhead.

E5. **CUDA Graph horizon replay**
- capture 40 physical steps as one graph;
- optional intermediate-state recording;
- targets digital-twin repeated simulation rather than isolated one-step microbenchmarks.

E6. **Optional Triton fused transport**
- if Triton is available, fuse transport polynomial evaluation, departure-coordinate construction, periodic indexing and linear interpolation into one GPU kernel;
- exact Q3-FIX2 transport formula;
- optional diagnostic only, not required for PASS.

## Why not parallelize everything

Operator dependencies remain physical dependencies. Diffusion/dispersion cannot be applied to the transported state before transport completes without changing the numerical method.

Q4 therefore distinguishes:

1. **mathematical concurrency** — independent role branches;
2. **data parallelism** — batch and spatial points;
3. **kernel fusion** — combine short pointwise/gather kernels;
4. **launch parallelism** — CUDA streams;
5. **submission optimization** — CUDA Graph replay.

The experiment will not claim that serial PDE dependencies disappear.

## Profiling

For E0 and the fastest exact variant, record:
- wall latency;
- CUDA kernel event count;
- CPU self time;
- CUDA self/total time;
- peak VRAM;
- grid-points/s.

Test:
- batch = 1, 16, 64
- native N=256
- optional performance-only N=64,128,512 when available.

## Accuracy equivalence

Every optimized execution path must match E0:

- one-step relative defect <= 2e-5
- 40-step relative defect <= 5e-5
- same finite/non-finite status.

No optimized backend is accepted if it changes the physical result beyond tolerance.

## Official FNO

Reconstruct and re-time the frozen Q0 official NeuralOperator FNO in the same process.

Report:
- batch-1
- batch-16
- batch-64
physical-step latency.

## Gates

P0 parent SHA and program integrity.

P1 all selected optimized variants preserve one-step output within 2e-5.

P2 chosen fastest exact variant preserves 40-step output within 5e-5 on both PDEs.

P3 batch-1 physical-step latency improves >=20% over E0 on both PDEs.

P4 batch-16 physical-step latency improves >=15% over E0 on both PDEs.

P5 40-step horizon wall time improves >=30% over E0 on both PDEs.

P6 fastest exact batch-1 speedup vs official FNO:
- Advection >=10x
- Burgers >=5x.

P7 fastest exact batch-16 speedup vs official FNO:
- Advection >=11x
- Burgers >=5x.

P8 profiler CUDA-kernel event count or host-launch count decreases >=30% for the chosen optimized path.

Decision:
- A2_Q4_PASS: P0-P5 mandatory + at least 2 of P6-P8.
- A2_Q4_CONDITIONAL: exactness passes and at least two of P3-P5 pass.
- A2_Q4_FAIL otherwise.

## Benchmark transition

Q4 is execution-only. Regardless of Q4 outcome, Q3-FIX2 remains the frozen mathematical IPM-v1 candidate unless an exact optimized backend replaces only its execution engine.

After Q4, broad benchmark execution may begin with the fastest exact implementation and the original eager implementation both archived.