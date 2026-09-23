# IPM-B0 — Classical PDE Solver Speed–Quality Frontier

## Purpose

A2-Q4 freezes IPM-v1 and its exact CUDA-Graph runtime.

B0 begins the paper benchmark phase.

The first comparison is deliberately against **classical numerical PDE solvers**, because these are the strongest direct competitors to a speed-first PDE simulation engine.

No IPM model, coefficient, role mask or calibration is changed in B0.

## Frozen parents

- Q0 official NeuralOperator FNO:
  `6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`
- Q3-FIX2 frozen IPM-v1 mathematics:
  `f55c97725c51e82cbe76c981eaa66337b65cb9df98951d0b2566fc6b9a76cedc`
- Q4 frozen parallel runtime:
  `e9073c703c72c2d44896bf437d6db02a1a00815c14771161de072fa5e83d729e`

## Information-contract distinction

Classical solvers receive the **true PDE equation and coefficient**:
- Advection: beta=1
- Burgers: nu=0.01

IPM does not receive the true symbolic equation at deployment; it uses the frozen learned/compiled principal program.

Therefore B0 does not call this a matched-information contest.

The paper reports it as a practical deployment question:

> Given that a classical solver knows the PDE and IPM has learned/compiled its own PDE program, which method occupies the best error–latency frontier?

## PDEBench tasks

- 1D periodic Advection beta=1.0
- 1D periodic Burgers nu=0.01

Same official first-10% test split and the same N=256 spatially downsampled qualification grid used by IPM-v1.

Formal horizon:
- start = state 9
- predict states 10..49
- 40 physical steps

## Frozen IPM baseline

Three Q3-FIX2 seed programs.

Runtime:
- step: Q4 E4 CUDA Graph
- horizon: Q4-style 40-step CUDA Graph

## Classical Advection baselines

### A0 Fourier exact phase
For the known periodic constant-coefficient equation
[
u_t+eta u_x=0,
]
advance exactly in the resolved Fourier space:
[
hat u_k(t+Delta t)=e^{-ieta kDelta t}hat u_k(t).
]

This is an intentionally strong equation-specific baseline.

### A1 Semi-Lagrangian
Known constant velocity beta, periodic linear interpolation.

### A2 First-order upwind
Substeps m in {1,2,4,8,16}; unstable-CFL configurations are marked invalid.

### A3 Lax–Wendroff
Substeps m in {1,2,4,8,16}; CFL <=1 required.

## Classical Burgers baselines

PDE:
[
u_t + (u^2/2)_x = 
u u_{xx},qquad 
u=0.01.
]

### B0 Known-PDE semi-Lagrangian + spectral diffusion
Use velocity u for semi-Lagrangian transport and exact periodic spectral diffusion.

### B1 Rusanov finite volume + Strang spectral diffusion
Convective Rusanov step with SSP-RK3, exact half-step spectral diffusion.

### B2 MUSCL–Rusanov + Strang spectral diffusion
Minmod-limited MUSCL interface reconstruction, Rusanov flux, SSP-RK3, exact spectral diffusion.

### B3 Dealiased pseudo-spectral nonlinear RK4 + Strang diffusion
2/3-rule filtered spectral derivative for the nonlinear flux and exact spectral diffusion.

For B0/B1/B2/B3 use substeps m in {1,2,4,8}. Non-finite configurations are rejected.

WENO5 is reserved for B0-FULL after this harness qualifies; its implementation will be cross-checked independently before inclusion.

## Timing fairness

For every fixed-shape solver/configuration report:

1. ordinary eager 40-step horizon time;
2. CUDA-Graph 40-step horizon time when capturable;
3. batch 1;
4. batch 16;
5. grid-points/second;
6. peak VRAM.

The primary timing is the fastest exact native implementation available to that method.

No method is penalized for being compilable or graph-capturable.

## Quality metrics

- 40-step Rel-L2
- RMSE
- horizon Rel-L2 at 1/5/10/20/40
- finite/non-finite status
- spatial-mean conservation drift
- Fourier low/mid/high band error

## Pareto protocol

A numerical configuration is Pareto-nondominated if no other configuration has both:
- lower/equal 40-step Rel-L2
- lower/equal horizon wall time
with at least one strict inequality.

Create separate Pareto fronts for:
- batch 1
- batch 16
- each PDE

IPM is plotted as a frozen point, not tuned against each solver.

## Qualification gates

B0-0 parent hashes and PDEBench MD5s match.

B0-1 Fourier-exact Advection is finite and 40-step Rel-L2 <=0.03.

B0-2 at least three classical configurations are finite for each PDE.

B0-3 CUDA-Graph and eager outputs for every accepted solver differ by <=2e-6.

B0-4 metric/timing/VRAM/Pareto tables export.

B0-5 frozen IPM output remains finite and reproduces the parent 40-step error within 2e-4.

Decision:
- B0_HARNESS_PASS if B0-0..B0-5 all pass.
- B0_HARNESS_FAIL otherwise.

## Next benchmark stages

After B0:
- B1 neural surrogate + neural operator suite
- B2 PINN + physics-informed operator suite
- B3 discovery/mechanistic + PDE foundation suite
- B4 unified Pareto and amortized-cost analysis

The final benchmark will include the broad model families already frozen in `docs/PAPER_BENCHMARK_PLAN.md`.