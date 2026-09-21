# IPM-M0 Results

## Decision

**FAIL_M0**

The experiment does not qualify the current Intrinsic Prolongation implementation for progression to IPM-A0.

## Structural results

- Intrinsic prolongation identity max absolute defect: **0.0**
- One-step holonomic relative defect: **3.70e-4**
- The architecture therefore successfully enforced higher jet tendencies from the base generator by construction.

## Empirical results

Mean base-rollout metrics:

| Model | Final field Rel-L2 | Final jet Rel-L2 | Mean consistency defect |
|---|---:|---:|---:|
| FieldState | 0.00936 | 0.11715 | 0 |
| DerivativeFeature | 0.44556 | 263.78877 | 0 |
| FreeJet | 0.01559 | 0.15421 | 0.60314 |
| SoftJetConsistency | 0.01629 | 0.16230 | 0.17820 |
| IPM | 0.74966 | 462.77906 | 2.72e-4 |

IPM preserved jet consistency extremely well but failed to translate that structural validity into stable and accurate physical rollout.

## Seed reproducibility

IPM did not outperform SoftJetConsistency in final mean jet error for any of the five formal seeds.

A severe seed-dependent instability occurred, most notably for Burgers and KdV.

## Generalization failures

- large dt-transfer degradation;
- grid transfer became non-finite at high resolution in multiple seeds;
- coefficient OOD substantially worse than the best learned baseline;
- high-order / nonlinear PDEs were the dominant failure modes.

## Important audit note

The executed notebook used a derivative-validation threshold of **1e-2**, while the originally generated frozen notebook used **5e-4**.

The observed third-derivative relative error was **5.152e-3**.

Therefore the derivative-validation gate would not pass under the original stricter threshold. This does not change the overall M0 decision, which is already FAIL, but future experiments will include configuration hashing and run-integrity checks so gate definitions cannot be silently changed.

## Main technical diagnosis

The failure should not be treated as a simple hyperparameter problem.

The current formulation exposes three deeper issues:

1. **Finite-order jet closure**  
   If (Q_\theta) depends on (J^k u), then repeated total derivatives (D_x^rQ_\theta) can involve derivatives beyond order (k). A naive finite (J^k) state is therefore not generally dynamically closed.

2. **High-order conditioning / stiffness**  
   Derivative magnitudes and high-frequency errors grow rapidly with derivative order. Directly integrating all jet coordinates strongly amplifies small generator errors.

3. **Rollout manifold implementation**  
   Although prolongation makes the vector field locally consistent, numerically evolving all jet coordinates directly is fragile. A more robust formulation should consider a master field plus holonomic reconstruction / retraction, or a mathematically closed intrinsic state.

## Next experiment

**IPM-M1: Holonomic Closure and Stable Intrinsic Evolution**

M1 will test:
- master-state + intrinsic jet reconstruction;
- explicit holonomic retraction after integration stages;
- derivative-order normalization;
- low/high-frequency conditioning diagnostics;
- closure-aware generator formulations;
- integrator sensitivity;
- separate smooth and high-order PDE qualification.

IPM-A0 remains blocked until M-stage qualification passes.
