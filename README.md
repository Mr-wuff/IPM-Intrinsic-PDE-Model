# Intrinsic PDE Model (IPM)

Research repository for **Intrinsic PDE Model (IPM)** and the paper:

> **Make PDE integrated into model native**

## Frozen scope

This repository studies **IPM only**. CIDM, CIDM-SIM, CIDM-JET, digital-twin integration, and other downstream systems are outside the current research scope and will not be used in the IPM paper experiments.

The current project starts from a clean research definition. Earlier prototype/half-finished IPM experiments are treated as invalid historical attempts and are not evidence for the architecture.

## Research thesis

IPM investigates whether a neural model can make PDE structure **intrinsic to its state transition mechanism**, rather than using the PDE only as:

- an external residual loss,
- an input token or symbolic condition,
- a post-hoc constraint,
- or an implicitly learned state-to-state mapping.

The central object is a geometrically valid differential state (jet state) together with an intrinsic evolution operator and consistency/prolongation structure.

## Paper questions

1. What mathematical state representation makes PDE dynamics intrinsic to the model?
2. Can IPM learn continuous infinitesimal evolution rather than a fixed-step map?
3. Does intrinsic differential structure improve data efficiency, long-horizon stability, and transfer?
4. Can one architecture generalize across coefficients, initial/boundary conditions, grids, time steps, geometries, and PDE families?
5. Which gains come from intrinsic structure itself, rather than parameter count, derivative features, or solver choice?

## Repository policy

Every formal experiment will include:

- frozen hypothesis and gate before training;
- exact environment and random seeds;
- matched-capacity baselines;
- automatic metrics, figures, tables, and report generation;
- checkpoints and manifests;
- failure analysis;
- reproducible result bundle;
- experiment-specific branch/commit history.

See `docs/RESEARCH_ROADMAP.md` for the full development plan.
