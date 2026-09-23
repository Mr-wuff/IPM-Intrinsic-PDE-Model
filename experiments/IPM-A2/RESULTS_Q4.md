# IPM-A2-Q4 Results — Parallel Native Execution

## Integrity

Formal decision: **A2_Q4_PASS**

Result ZIP SHA256:
`e9073c703c72c2d44896bf437d6db02a1a00815c14771161de072fa5e83d729e`

Executed notebook SHA256:
`6afc9eb518e920a878034e59aa48d4b39424576a074169e9d1fc18a2b5bc69d6`

Frozen notebook SHA256:
`fbc208a2fcc7e66b4eb90575e4a855b2ab68adabb3ee59022ea0d97effc3fa16`

The result ZIP SHA matches the supplied SHA file.

### Runtime repair

Only code cells 9 and 11 differ from the frozen notebook.

The executed notebook adds:
- `torch.compiler.cudagraph_mark_step_begin()`
- output `.clone()`

around repeated `torch.compile` model invocations during rollout/equivalence and callable 40-step benchmarking.

This repairs PyTorch CUDA Graph output-lifetime overwrite errors. It does not alter the frozen Q3-FIX2 PDE program, role mask, gains, numerical flow, data, or test contract.

## Gates

Passed:
- P0 parent/data integrity
- P1 one-step exactness
- P2 40-step exactness
- P3 batch-1 improvement
- P4 batch-16 improvement
- P5 40-step improvement
- P6 batch-1 FNO speedup
- P7 batch-16 FNO speedup

Failed:
- P8 profiler CUDA-event reduction

Overall: **PASS**

## Numerical equivalence

E1 fused eager, E3 streams and E4 CUDA Graph reproduce E0 exactly in the saved audit.

E2 torch.compile defects are tiny:
- one-step: about 5.5e-8 to 7.9e-8
- 40-step: about 1.5e-7 to 4.6e-7

All are far below the preregistered tolerances.

## Single-step latency

Mean batch-1:

Advection:
- E0 eager: 0.49405 ms
- E1 fused: 0.48685 ms
- E3 streams: 0.38553 ms
- E2 compile: 0.17961 ms
- **E4 CUDA Graph: 0.08273 ms**

Burgers:
- E0: 1.17477 ms
- E1: 1.15442 ms
- E3: 1.37189 ms
- E2: 0.17955 ms
- **E4: 0.23594 ms**

Mean batch-16:

Advection:
- E0: 0.33752 ms
- E4: **0.09010 ms**

Burgers:
- E0: 0.94656 ms
- E4: **0.23585 ms**

Mean batch-64:

Advection:
- E0: 0.33759 ms
- E4: **0.07605 ms**

Burgers:
- E0: 0.88180 ms
- E4: **0.19507 ms**

## Improvement over frozen eager

Batch-1:
- Advection: **83.3% lower latency**
- Burgers: **79.9% lower latency**

Batch-16:
- Advection: **73.3% lower latency**
- Burgers: **75.1% lower latency**

The main gain is graph replay / launch-overhead removal, not CUDA-stream role concurrency.

## Official FNO comparison in the same run

Batch-1:
- Advection IPM E4 0.08273 ms vs FNO 4.03786 ms: **48.81x**
- Burgers IPM E4 0.23594 ms vs FNO 4.12999 ms: **17.50x**

Batch-16:
- Advection 0.09010 ms vs 4.07575 ms: **45.23x**
- Burgers 0.23585 ms vs 4.17700 ms: **17.71x**

These are end-to-end physical-step timings for the frozen Q3-FIX2 mathematics.

## 40-step horizon

Fastest exact path: **E5 horizon CUDA Graph**.

Mean batch-1 speedup over E0 40-step loop:
- Advection: ~7.02x
- Burgers: ~4.79x

Mean batch-16:
- Advection: ~3.54x
- Burgers: ~4.84x

Thus whole-horizon graph capture is particularly valuable for repeated simulation workloads.

## What did not help

### Raw tensor fusion
E1 provides only modest gains.

### CUDA role streams
E3 is inconsistent and usually slower on Burgers.

The D/S branches are too small for stream-overlap benefits to dominate scheduling/synchronization overhead.

### torch.compile
E2 is excellent for batch-1 single-step execution but unstable as the best choice across batch/horizon settings. It is not the frozen deployment backend.

## Profiler result

The preregistered P8 uses CUDA-event-count reduction and fails:
- Advection CUDA events: 520 -> 460 (~11.5% reduction)
- Burgers: 1260 -> 1080 (~14.3%)

However total profiler events decrease much more:
- Advection: 1863 -> 503 (~73.0%)
- Burgers: 5243 -> 1123 (~78.6%)

Self CPU time decreases:
- Advection: ~59.4%
- Burgers: ~66.7%

Self CUDA time decreases:
- Advection: ~52.1%
- Burgers: ~52.5%

Therefore the dominant measured benefit is reduced host/framework submission and replay overhead, even though the narrow P8 CUDA-event threshold is not met.

## Frozen deployment choice

**IPM-v1 mathematical core remains Q3-FIX2.**

Deployment runtime:
- isolated/repeated step: E4 CUDA Graph
- fixed long horizon: E5 horizon CUDA Graph
- eager reference: E0 archived for exactness and portability

Q4 changes only execution, not the scientific model.

## Benchmark transition

The core architecture modification stage is closed.

Next phase: comprehensive benchmark against classical numerical PDE solvers, PINNs, physics-informed neural operators, neural operators, temporal surrogates, discovery/mechanistic models and PDE foundation models.

Numerical PDE solvers are evaluated first because they are the strongest direct competitor to IPM's speed-first physical-simulation claim.