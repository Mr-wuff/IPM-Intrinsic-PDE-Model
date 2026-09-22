# IPM-A1-FIX1 Results

## Formal status

**DISCOVERY_FIX1_COMPLETE**

Result ZIP SHA256:
`7f5419ede62c645b321a071eba8f22c3a5e9e6405bd91cc712771f554d6616ee`

The supplied SHA256 file matches exactly.

The executed notebook contains 9 code cells and all 9 are byte-for-byte identical to the released A1-FIX1 notebook.

All F0-F7 integrity checks passed.

## Weak-SINDy repair

The degenerate zero-equation failure from A1 is repaired.

Training-side-only qualification selected non-normalized STLSQ configurations for every PDE.

Selected WeakPDELibrary thresholds:
- Heat: 0.01
- Advection: 0.2
- Burgers: 0.2
- Allen-Cahn: 0.001
- KdV: 0.1

Every selected weak configuration has nonzero active terms on clean qualification data.

## Clean law discovery

Mean clean results:

| Method | Symbolic F1 / IPM order F1 | Coefficient error | exact-Q Rel-RMSE |
|---|---:|---:|---:|
| Strong PySINDy | symbolic 1.000 | 0.000232 | 0.000336 |
| Weak PySINDy | symbolic 0.703 | 0.00977 | 0.0606 |
| IPMRaw | order 0.760 | 0.0531 | 0.0758 |
| IPMAdaptive | order 0.760 | 0.0503 | 0.0814 |

Strong-form sparse discovery is essentially exact in the clean in-library setting.

Weak-SINDy is now valid but its qualification criterion trades some small higher-order terms for robustness/sparsity. For example, clean Burgers and KdV weak models may omit the small diffusion/dispersion term.

## Noise robustness

### 1% observation noise

| Method | Coefficient error | exact-Q Rel-RMSE |
|---|---:|---:|
| IPMAdaptive | **0.0502** | **0.0850** |
| Strong PySINDy | 0.2644 | 0.4425 |
| Weak PySINDy | 0.3185 | 16.1354 |
| IPMRaw | 0.7184 | 1.3083 |

### Unseen 3% noise

| Method | Coefficient error | exact-Q Rel-RMSE |
|---|---:|---:|
| IPMAdaptive | **0.0503** | **0.0988** |
| Strong PySINDy | 0.4045 | 0.9257 |
| IPMRaw | 0.8910 | 1.6681 |
| Weak PySINDy | 1.1335 | 109.973 |

### N=64 + 1% noise

| Method | Coefficient error | exact-Q Rel-RMSE |
|---|---:|---:|
| IPMAdaptive | **0.0491** | **0.0869** |
| Strong PySINDy | 0.1469 | 0.4992 |
| IPMRaw | 0.1749 | 0.4631 |
| Weak PySINDy | 0.4436 | 3.0856 |

The leakage-free IPM coefficient estimate remains essentially invariant:
- clean: 0.05026
- 1% noise: 0.05025
- 3% noise: 0.05030
- N=64 + 1%: 0.04911

The IPMAdaptive differential-order F1 is also constant at 0.760 over all four conditions.

## Paired statistics

Across 25 PDE x seed pairs:

### IPMAdaptive vs Strong PySINDy

Coefficient error, IPMAdaptive - Strong:
- 1% noise: -0.2141, 95% CI [-0.3801,-0.0482]
- 3% noise: -0.3542, 95% CI [-0.5108,-0.1976]
- N=64 + 1%: -0.0978, 95% CI [-0.1917,-0.00385]

Exact-Q error:
- 1% noise: -0.3574, 95% CI [-0.5217,-0.1932]
- 3% noise: -0.8269, 95% CI [-1.0474,-0.6064]
- N=64 + 1%: -0.4123, 95% CI [-0.6238,-0.2008]

Clean data reverses this ordering: Strong PySINDy is decisively better.

## Strong vs weak symbolic support

Weak-SINDy symbolic support is more robust than strong-form support under mild noise/sparsity:

- clean Weak - Strong F1: -0.297, 95% CI [-0.407,-0.186]
- 1% noise: +0.304, 95% CI [+0.176,+0.432]
- 3% noise: +0.100, 95% CI approximately [-0.0003,+0.201]
- N=64 + 1%: +0.264, 95% CI [+0.131,+0.396]

Thus the weak formulation does recover a support-robustness benefit after proper qualification.

## Important interpretation of Weak-SINDy Q error

The very large weak-form pointwise Q errors under noise should not be interpreted as a failure of weak equation discovery itself.

The weak method estimates coefficients without requiring pointwise derivatives, but A1-FIX1 subsequently evaluates the recovered symbolic equation on the noisy field using spectral derivatives. This reintroduces derivative-noise amplification during deployment.

Therefore:
- symbolic support and coefficient error are the primary Weak-SINDy discovery metrics;
- noisy pointwise Q error is a downstream equation-application stress test.

## Information-contract caveat

This is not a matched training-data-budget contest.

PySINDy:
- fits a fixed-coefficient PDE from a small set of formal trajectories;
- receives an explicit polynomial/derivative candidate library and sparsity prior.

IPM:
- uses frozen A0 checkpoints pretrained across coefficient ranges;
- receives no explicit symbolic term library;
- exposes a differentiable local law whose coefficients are audited through the Jacobian.

Fit time must therefore not be read as total learning-cost comparison. IPM training-cost comparisons belong to A0.

## Scientific conclusion

A1 supports a complementary, not replacement, claim:

1. symbolic sparse discovery is superior for exact clean in-library equation recovery;
2. strong-form symbolic discovery degrades sharply when noisy observations are differentiated;
3. qualified Weak-SINDy improves symbolic-support robustness but can discard dynamically weak high-order terms and does not by itself solve pointwise noisy derivative application;
4. IPMAdaptive preserves local-law accuracy, differential-order structure and coefficient estimates across 1-3% noise and reduced spatial resolution;
5. IPM's interpretability is differential/Jacobian based rather than exact symbolic-expression recovery.

A1 is closed. The next stage is external predictive benchmarking on official PDEBench data with official NeuralOperator FNO baselines.
