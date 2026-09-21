# IPM-M1 — Holonomic Closure and Stable Intrinsic Evolution

## Formal notebook

`IPM_M1_Holonomic_Closure_Stable_Intrinsic_Evolution_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`7757f607365c23dcafd4ea40634f8e424a3d44eb31bace562e8303117e554c9c`

Frozen protocol SHA256:

`d29c54ee2b398ae5abd3c94271d2e2c807e7b3013dd8775b3104128d9e7a8120`

## Purpose

M1 repairs the principal M0 failure mode by changing the recurrent numerical state from a freely integrated finite jet to a master field with exact stage-wise jet reconstruction.

At every integration stage:

[
u \rightarrow J^k u \rightarrow Q_\theta(J^k u,\lambda) \rightarrow u_t
]

and only (u) is integrated.

The experiment also introduces intrinsic differential normalization and an order-factorized IPM generator.

## Model ladder

1. FieldState
2. RawJetGenerator
3. NormalizedJetGenerator
4. HolonomicIPM-NoOrderStructure
5. HolonomicIPM

## Formal PDE suite

- Heat
- Linear advection
- Viscous Burgers
- Allen–Cahn
- KdV

## Integrity

The notebook embeds the preregistered protocol payload and verifies its SHA256 at runtime. A changed protocol is marked invalid for formal evidence.

## Result export

At completion the notebook creates:

- `IPM_M1_RESULTS.zip`
- `IPM_M1_RESULTS.zip.sha256`

Google Colab automatically triggers browser downloads for both files. Local WSL/Jupyter runs print local absolute paths and clickable links when supported.

## Decision

The notebook returns one of:

- `PASS_M1`
- `CONDITIONAL_M1`
- `FAIL_M1`

IPM-A0 remains blocked until M-stage qualification is supported by the frozen gates.
