# IPM-M1 — Holonomic Closure and Stable Intrinsic Evolution

## Motivation

IPM-M0 established that intrinsic prolongation can enforce derivative-state evolution by construction, but the full jet-state rollout was unstable, especially for nonlinear and high-order PDEs. M1 therefore tests a revised formulation where the only numerically integrated state is the master field (u).

## Core hypothesis

A stable IPM should treat the jet as **intrinsic geometry reconstructed from the master field**, not as independently drifting memory.

At every numerical integrator stage:

[
u ightarrow J^k u ightarrow Q_	heta(J^k u,lambda) ightarrow u_t,
]

and only (u) is integrated. The jet is then reconstructed exactly from the updated field.

## Null hypothesis

Reconstructing the jet holonomically and normalizing derivative order provides no reproducible advantage over a raw derivative-feature generator with the same master-field integration.

## Models

1. **FieldState** — (u ightarrow Q_	heta).
2. **RawJetGenerator** — raw concatenated (J^k u ightarrow Q_	heta), master-field integration.
3. **NormalizedJetGenerator** — dimensionless derivative-order normalization, master-field integration.
4. **HolonomicIPM** — order-factorized intrinsic jet encoder + dimensionless normalization + stage-wise exact jet reconstruction.
5. **HolonomicIPM-NoOrderStructure** — same master-field reconstruction and normalization but without order-factorized fusion, isolating the architectural contribution.

The primary comparison is:
- RawJetGenerator vs NormalizedJetGenerator: conditioning effect.
- NormalizedJetGenerator vs HolonomicIPM-NoOrderStructure: implementation control.
- HolonomicIPM-NoOrderStructure vs HolonomicIPM: intrinsic order-structured architecture effect.

## PDE suite

Formal M1:
- Heat
- Linear advection
- Viscous Burgers
- Allen–Cahn
- KdV

## Pre-training qualification

Formal training is blocked unless:
1. spectral derivative audit passes for orders 1–3;
2. holonomic reconstruction defect is below tolerance;
3. one-step RK stage reconstruction remains finite for all PDE families;
4. derivative normalization yields bounded channel-scale ratios on the training distribution;
5. exact experiment/config hash matches the frozen manifest.

## Evaluation

- field relative L2;
- derivative/jet relative L2;
- generator (u_t) error;
- long-rollout stability;
- dt transfer;
- grid transfer;
- coefficient OOD;
- IC OOD;
- noise robustness;
- spectral high-frequency error;
- gradient error;
- latency and memory;
- five formal seeds.

## Frozen gates

G0 — protocol hash verified.  
G1 — derivative audit passes.  
G2 — holonomic reconstruction defect < 5e-6 at N=128 and N=256.  
G3 — HolonomicIPM stable on all 5 PDEs across all 5 seeds for the base rollout.  
G4 — mean final field error of HolonomicIPM <= 0.90 × RawJetGenerator OR <= 1.05 × best baseline with >=25% lower high-order jet error.  
G5 — Burgers + KdV mean field error <= 0.70 × the M0 IPM reference failure level and no catastrophic outlier.  
G6 — dt transfer degradation no worse than 1.20 × best jet-based baseline.  
G7 — grid transfer degradation no worse than 1.20 × best jet-based baseline.  
G8 — coefficient OOD error <= 1.15 × best learned baseline.  
G9 — at least 4/5 seeds reproduce the direction of the primary HolonomicIPM vs RawJetGenerator result.

Decision:
- PASS_M1: G0–G3 and G9 mandatory, plus at least 4 of G4–G8.
- CONDITIONAL_M1: all structural gates pass but empirical evidence is mixed.
- FAIL_M1: structural stability/closure fails or advantages are not reproducible.

## Integrity policy

The notebook embeds a frozen protocol payload and SHA256. If the runtime payload differs, the run is marked `PROTOCOL_MODIFIED` and cannot be used as formal paper evidence.

## Output policy

After result packaging:
- Colab: automatically trigger browser download of ZIP + SHA256.
- Local Jupyter/WSL: print the absolute local file paths and render clickable links when available.
