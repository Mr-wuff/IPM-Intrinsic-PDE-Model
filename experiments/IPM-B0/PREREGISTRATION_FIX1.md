# IPM-B0-FIX1 — Classical Solver Harness Replication

## Purpose

The initial B0 harness formally passed, but a post-run audit found one invalid baseline implementation:

`AdvSemiLagrangian` used a `[1,1,N]` gather index with a multi-trajectory accuracy batch. `torch.gather` does not broadcast the batch dimension, so the numerical state collapsed to one trajectory and was later broadcast against all references.

FIX1 repairs only this baseline implementation and adds a batch-shape/conservation audit.

IPM-v1 remains frozen and is imported from the repository package. Historical Q0/Q3-FIX2/Q4 result ZIP files are no longer required.

## Inputs

- Official PDEBench Advection beta=1.0 and Burgers nu=0.01 files, downloaded and MD5-verified automatically.
- Frozen `ipm_v1` package from repository `main`.

## Mandatory audit

For constant-velocity semi-Lagrangian, with B=7 random periodic states:
- output shape must equal input shape;
- constant fields must remain constant;
- spatial mean drift after one step <=1e-6.

## Formal replication

Repeat B0 accuracy/timing/Pareto tables with the repository implementations.

The expected scientific status is determined from the corrected results; no target ranking is preregistered.

## Decision

`B0_FIX1_PASS` if:
- package version and frozen program manifest load successfully;
- data MD5s match;
- semi-Lagrangian batch/conservation audit passes;
- all accepted classical configurations are finite;
- CUDA Graph equivalence passes;
- frozen IPM reproduces its Q3-FIX2 mean errors within 2e-4;
- complete accuracy/timing/Pareto tables export.

No model-performance winner is part of the gate.