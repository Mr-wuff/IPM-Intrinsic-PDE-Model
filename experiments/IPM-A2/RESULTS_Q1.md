# IPM-A2-Q1 Results — Holonomic Prolonged Integral Flow

## Integrity

Decision from frozen protocol: **A2_Q1_FAIL**

Result ZIP SHA256:
`48ffafc3e0f9c2a6e6b77541496cd19095e0b815bc93d90e8dcc943faa946fb0`

The supplied SHA256 matches exactly.

The executed notebook contains 9 code cells and all 9 are byte-for-byte identical to the frozen Q1 notebook.

Parent Q0 SHA and official PDEBench MD5 checks passed. All 18 formal P0/P1/P2 runs are finite and all models have exactly 9,889 trainable parameters.

## Automatic gates

Passed:
- Q1-0 parent Q0 integrity
- Q1-1 official PDEBench MD5
- Q1-2 identical parameter counts
- Q1-3 finite three-seed evaluation
- Q1-5 Burgers rollout improvement
- Q1-7 noise robustness
- Q1-8 resolution robustness
- Q1-9 latency safety

Failed:
- Q1-4 Burgers order-0 integral-residual improvement
- Q1-6 Advection safety

Selected by the frozen rule: P2.

## Three-seed mean results

### Advection beta=1

| Variant | r0 integral | r1 | r2 | secant-Q | 40-step rollout |
|---|---:|---:|---:|---:|---:|
| P0 | **0.0641** | **0.2052** | **0.7888** | **0.0947** | **0.0593** |
| P1 | 0.0720 | 0.2117 | 0.7952 | 0.1047 | 0.1038 |
| P2 | 0.0789 | 0.2175 | 0.7976 | 0.1118 | 0.1406 |

Equal-weight prolongation is harmful on the essentially first-order transport law.

### Burgers nu=0.01

| Variant | r0 integral | r1 | r2 | secant-Q | 40-step rollout |
|---|---:|---:|---:|---:|---:|
| P0 | **0.6961** | 0.7847 | 0.9889 | **0.7119** | 0.5139 |
| P1 | 0.8321 | **0.7695** | 0.8825 | 0.8412 | 0.3815 |
| P2 | 0.7722 | 0.7759 | **0.8701** | 0.7828 | **0.3324** |

P2 reduces the Burgers 40-step rollout error by **35.3%** relative to matched P0-1200, but makes the order-0 held-out integral residual **10.9% worse**.

Paired P2-P0 Burgers rollout difference over the three formal seeds:
- mean = -0.1815
- 95% t interval = [-0.3033,-0.0597]

P2 also improves the Burgers order-2 residual:
- mean difference = -0.1189
- 95% t interval = [-0.2058,-0.0319]

This indicates a real long-horizon regularization effect, not improved instantaneous characteristic identification.

## Q0 frozen diagnostics

For Q0 IPMAdaptive:
- Advection rollout is unchanged by RK4 substeps 1/2/4/8 (~0.1123).
- Burgers rollout is unchanged by substeps 1/2/4/8 (~0.930).

Therefore the Adaptive public-data failure is not primarily a numerical-integrator step-size problem.

The generator/trajectory-law diagnostics are already poor on Burgers:
- integral r0 = 0.742
- secant-Q relative error = 0.761

The principal failure is characteristic identification.

## Jet conditioning

Raw high-order jet magnitude is extremely resolution sensitive. Example Advection order-3 RMS:
- full resolution: 17,535
- /2: 8,869
- /4: 3,815

Adaptive lift reduces this to:
- 2,544
- 2,543
- 2,051

This independently reinforces the decision to retain Raw only as an ablation and use a robust jet lift on the formal path.

## Training-duration effect

Q0 used 600 updates. Q1 P0 uses the same order-0 objective for 1,200 updates.

The longer P0 training itself substantially improves rollout:
- Advection: Q0 Adaptive ~0.1124 -> Q1 P0 mean 0.0593
- Burgers: Q0 Adaptive ~0.9300 -> Q1 P0 mean 0.5139

Thus Q0 was partly optimization-limited. This must be separated from any claimed prolongation effect.

## Efficiency

All variants have 9,889 parameters.

Mean generator-forward latency remains ~1.5-1.9 ms on the T4, but this is **not an end-to-end simulation-step comparison** against FNO. Current IPM uses four generator evaluations per RK4 physical step, whereas the FNO native contract predicts the next field in one forward pass.

No paper claim that IPM is end-to-end faster than FNO is supported yet.

## Scientific interpretation

Q1 falsifies the hypothesis that equal-weight high-order prolongation universally improves the learned characteristic.

What is supported:
1. holonomic prolongation can regularize nonlinear Burgers long-horizon evolution;
2. the same equal-weight constraint conflicts with simple transport dynamics;
3. the dominant public-data Burgers bottleneck remains local-law identification;
4. numerical RK4 substepping is not the main bottleneck;
5. speed evidence must use end-to-end physical-step timing, not generator timing.

A2-FULL remains blocked.

The next qualification should target the user's core IPM objective directly: a PDE-native, ultra-small, ultra-fast local differential computation core rather than adding conventional neural components.
