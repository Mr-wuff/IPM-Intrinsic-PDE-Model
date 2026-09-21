# IPM-M1-FIX1 Results

## Integrity
- Result ZIP SHA256 verified against the returned .sha256 file.
- Frozen protocol integrity: PASS.
- Strengthened derivative audit: PASS.
- Holonomic reconstruction audit: PASS.

## Corrected scientific decision
**CONDITIONAL_M1**

The notebook's automatic verdict is also CONDITIONAL_M1, but two automatic gates (G4 and G9) are not admissible as formal evidence because RawJetGenerator diverged to Inf on all PDEs. Comparisons of finite error against Inf trivially pass.

The corrected interpretation therefore separates RawJetGenerator as a catastrophic-failure control and evaluates the finite models directly.

## Base rollout

| Model | Mean final field Rel-L2 | Mean final jet Rel-L2 | Stability |
|---|---:|---:|---:|
| FieldState | 0.00943 | 0.106 | 1.0 |
| RawJetGenerator | Inf | Inf | 0.0 |
| NormalizedJetGenerator | 0.74206 | 203.84 | 1.0 |
| HolonomicIPM-NoOrderStructure | 0.47843 | 188.96 | 1.0 |
| HolonomicIPM | 0.05612 | 17.45 | 1.0 |

HolonomicIPM reduces mean field error by about:
- 92.4% relative to NormalizedJetGenerator;
- 88.3% relative to HolonomicIPM-NoOrderStructure.

It wins against both finite jet baselines in all 5 formal seeds.

However, FieldState remains substantially better:
- FieldState mean field error: 0.00943
- HolonomicIPM mean field error: 0.05612
- ratio: ~5.95x

## PDE-wise HolonomicIPM field error
- Advection: 0.10370
- Allen-Cahn: 0.01492
- Burgers: 0.01337
- Heat: 0.11776
- KdV: 0.03086

The M0 catastrophic Burgers/KdV failure is strongly repaired. The remaining weakness is concentrated in Heat and Advection and in high-frequency derivative fidelity.

## High-frequency / jet failure
HolonomicIPM remains affected by high-frequency contamination:
- Heat final jet error ~47.1
- Advection final jet error ~34.0
- KdV final jet error ~5.16

Field values can stay finite and moderately accurate while derivatives become very inaccurate.

## Generalization
HolonomicIPM:
- dt transfer degradation: poor;
- grid transfer: poor, especially at N=256 and N=512;
- coefficient OOD: 0.0906 vs best baseline 0.0359;
- IC OOD: much closer to FieldState than other jet models, but still worse.

Grid behavior is especially diagnostic:
- N=64 field error ~0.0596
- N=128 ~0.1083
- N=256 ~0.2598
- N=512 ~0.3424

This suggests that the current spatial convolutional generator introduces a grid-index receptive field and therefore conflicts with the intended local, resolution-independent PDE generator.

## Conditioning audit
The current characteristic-scale normalization does not fully equalize derivative orders. Normalized RMS values increase with derivative order, with the third derivative still much larger than lower orders.

## Main architectural diagnosis
M1 successfully repaired independent jet-state drift, but its convolutional generator is not yet the right intrinsic PDE core.

For a finite-order local PDE,
[
u_t = F(j^k u,\lambda),
]
the generator should be pointwise in jet space. A spatial Conv1D trunk mixes neighboring grid points in index space, making the learned local law depend on resolution and creating a hidden grid-scale prior.

## Next step
**IPM-M1-FIX2: Pointwise Jet Generator + Resolution-Invariant Differential Normalization + Generator Sobolev Fidelity**

Goals:
1. replace the spatial convolutional IPM core with a pointwise jet-space generator;
2. normalize every derivative order directly by its own RMS scale and expose those scales as context;
3. use the same generator Sobolev supervision for all finite baselines to control high-frequency error fairly;
4. treat RawJet catastrophic divergence as a failure control, never as a denominator for winner gates;
5. require grid and dt transfer improvements before A0.
