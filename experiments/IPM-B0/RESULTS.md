# IPM-B0 Initial Results — Classical PDE Solver Harness

Formal preregistered harness decision: **B0_HARNESS_PASS**

Result ZIP SHA256:
`0894771ed6600029ef2771f81076f0046acd51a5ec37c9a7eb96fec8228d2566`

All six formal harness gates passed, and frozen IPM-v1 reproduced the parent Q3-FIX2 40-step errors to machine precision.

## Main valid observations

### Advection beta=1
- Fourier exact phase: Rel-L2 0.001366, 40-step CUDA-Graph time 0.40694 ms (batch 1)
- Upwind m4: 0.057151, 0.99944 ms
- IPM-v1: 0.079760, 1.60781 ms
- Lax-Wendroff m4: 0.009518, 2.36611 ms

For this simple known periodic PDE, IPM-v1 is **not** on the initial error–latency Pareto frontier. The equation-specific Fourier solver strongly dominates, as expected when the exact PDE is known.

### Burgers nu=0.01
- known-PDE SL + spectral diffusion m1: Rel-L2 0.145636, 2.47841 ms
- IPM-v1: 0.192795, 5.23826 ms
- Rusanov + Strang m1: 0.117879, 5.67790 ms
- pseudo-spectral RK4 + Strang m1: 0.107889, 7.35860 ms

Again, on this simple known-equation task, classical solvers provide a stronger quality–speed frontier than IPM-v1. This is an important limiting result and remains part of the benchmark record.

## Post-run baseline bug found

The constant-velocity `AdvSemiLagrangian` implementation used an index tensor of shape `[1,1,N]` directly in `torch.gather` while accuracy evaluation used a multi-trajectory batch.

`torch.gather` does not broadcast the index batch dimension. Therefore the first semi-Lagrangian step collapsed the accuracy batch to one trajectory, and subsequent comparison broadcast it against all reference trajectories.

This explains the anomalous initial B0 row:
- SemiLagrangian Rel-L2 1.397638
- mean drift 0.877073

That row is invalid for paper use.

The reusable repository implementation now explicitly expands the periodic index grid to the input batch. A B0-FIX1 replication is required before the Advection semi-lagrangian row is used.

## Scientific interpretation

B0 does not ask whether IPM should beat an exact solver that already knows the correct PDE. It quantifies the deployment trade-off after IPM has learned and compiled its own local law.

The initial result shows that for simple known PDEs, strong classical solvers can dominate IPM. Future benchmark stages must therefore determine where the learned/compiled architecture becomes useful: unknown governing laws, parameterized regimes, harder systems, repeated deployment, and amortized cost.

The formal harness PASS is retained; the paper-level B0 table remains pending B0-FIX1 because of the semi-lagrangian batch bug.