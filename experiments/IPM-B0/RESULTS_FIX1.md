# IPM-B0-FIX1 Results — Repository-native Classical Solver Replication

Formal decision: **B0_FIX1_PASS**

Result ZIP SHA256:
`dbeb2df1487718d51dd2f5180a440fa2f693b53f9c1e298281f3c0bb2c56918c`

Executed notebook SHA256:
`633c44bc5b596b6657b82d334b7355b36e2873e9ce77400fa230c50f2cd6e5d8`

Frozen notebook SHA256:
`f2cf082daa011c58c86c00e44ebf5c85b8b22e7bf29015296d8834d74043362f`

The executed notebook has 13 code cells and all 13 code cells are byte-for-byte identical to the frozen B0-FIX1 notebook. Notebook byte differences are execution outputs / metadata only.

## Gates

All six gates pass:
- F0 package/data integrity
- F1 Semi-Lagrangian batch/conservation audit
- F2 all classical configurations finite
- F3 CUDA-Graph equivalence
- F4 IPM freeze reproduction
- F5 complete exports

## Repository-native workflow validation

The notebook installs `ipm_v1==1.0.0` from pinned repository commit:

`d51449027f66dac3accd59f1b224a86a4be86eaa`

No historical Q0/Q3-FIX2/Q4 result ZIP is required.

Frozen IPM reproduction:
- Advection: 0.07976008454958598 vs frozen 0.07976008454958593
- Burgers: 0.1927954206864039 vs frozen 0.19279542068640387

Absolute differences are ~1e-17.

This validates the new repository-native workflow.

## Semi-Lagrangian bug repair

The mandatory audit passes:
- output shape preserved for B=7
- maximum spatial-mean drift: 7.8231e-08
- constant-field error: 0.0

Corrected Advection Semi-Lagrangian 40-step Rel-L2:
[
0.017443
]
instead of the invalid initial B0 value ~1.398.

## Advection beta=1

40-step accuracy:
- Fourier exact: **0.001366**
- Lax-Wendroff m4: **0.009518**
- Semi-Lagrangian: **0.017443**
- Upwind m4: **0.057151**
- IPM-v1: **0.079760**

Batch-1 fastest exact 40-step wall time:
- Fourier exact: **0.3891 ms**
- Upwind m4: **0.9771 ms**
- Semi-Lagrangian: **1.0798 ms**
- IPM-v1: **1.5957 ms**
- Lax-Wendroff m4: **2.3517 ms**

For this known linear periodic PDE, IPM-v1 is not Pareto-nondominated.

Relative to Fourier exact, IPM-v1 has about 58.4x the error and 4.10x the wall time.

Relative to corrected Semi-Lagrangian, IPM-v1 has about 4.57x the error and 1.48x the wall time.

## Burgers nu=0.01

Best / representative 40-step accuracy:
- pseudo-spectral RK4 + Strang m8: **0.107576**
- MUSCL-Rusanov m8: **0.108186**
- Rusanov m8: **0.117531**
- SL + spectral diffusion m4: **0.117966**
- SL + spectral diffusion m1: **0.145636**
- IPM-v1: **0.192795**

Batch-1 40-step wall time:
- SL + spectral diffusion m1: **2.4820 ms**
- IPM-v1: **4.5698 ms**
- Rusanov m1: **6.5295 ms**
- pseudo-spectral RK4 + Strang m1: **7.0846 ms**

The fastest known-PDE SL + spectral-diffusion solver dominates IPM-v1 on this task:
- ~1.32x lower error
- ~1.84x lower wall time

## Scientific interpretation

B0-FIX1 establishes a clear boundary for the paper:

**When the governing equation is already known and admits a highly specialized solver, frozen IPM-v1 is not expected to dominate that solver.**

IPM's relevant question is therefore not "can it replace an exact/specialized solver for a known simple PDE?" but whether a learned-and-compiled PDE-native model provides a stronger amortized quality-speed-cost trade-off when the governing law must be inferred from data, varies across regimes, or is deployed repeatedly across tasks.

This negative boundary result remains part of the final paper benchmark.

## Next phase

Proceed to B1 neural surrogate / neural operator benchmarking while keeping IPM-v1 frozen and repository-native.
