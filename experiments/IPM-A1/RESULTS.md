# IPM-A1 Results — Independent Audit

## Artifact integrity

Result ZIP SHA256:
`480226f61e50c44d63768469397f7e8b0521f17b01cfb660ed9dcb3bb7da792e`

The checksum matches the supplied `.sha256` file.

The internal report returns:
`DISCOVERY_BENCHMARK_COMPLETE`

All D0–D7 execution/integrity checks are true.

## Scientific audit status

**A1_PARTIAL_VALID / FIX1_REQUIRED**

The run contains strong valid evidence, but two evaluation issues must be repaired before the full equation-discovery table is used in the paper.

### Valid evidence: official strong-form PySINDy

Clean strong-form PySINDy recovers the exact governing support in every PDE and every seed.

Mean clean results:
- support F1 = 1.000
- normalized coefficient error = 2.32e-4
- held-out exact-Q Rel-RMSE = 3.36e-4

Examples:
- Heat: (0.0200 u_{xx})
- Advection: (-0.6500 u_x)
- Burgers: (0.0200 u_{xx}-0.8000 uu_x)
- Allen-Cahn: (0.7500u-0.7500u^3+0.00650u_{xx})
- KdV: (-0.00200u_{xxx}-0.6000uu_x)

This is an important positive control: the candidate library and official strong-form implementation can exactly identify the governing equations from clean data.

### Noise stress result

Mean held-out exact-Q Rel-RMSE:

| Condition | IPMAdaptive | IPMRaw | Strong PySINDy |
|---|---:|---:|---:|
| clean | 0.0814 | 0.0758 | 0.000336 |
| 1% noise | 0.0850 | 1.3083 | 0.4952 |
| 3% noise | 0.0988 | 1.6681 | 1.2229 |
| N=64 + 1% noise | 0.0869 | 0.4631 | 0.6130 |

Paired across 25 PDE×seed cases:
- 1% noise, IPMAdaptive − Strong PySINDy Q error: −0.4102, 95% CI [−0.6350, −0.1853]
- 3% noise: −1.1241, 95% CI [−1.6056, −0.6426]
- sparse64 + 1% noise: −0.5261, 95% CI [−0.8121, −0.2402]

Thus the adaptive observation lift produces a strong and reproducible noise-robustness signal.

### Strong-form support collapse under noise

Strong PySINDy support F1:
- clean: 1.000
- 1% noise: 0.199
- 3% noise: 0.199
- N=64 + 1% noise: 0.200

The noisy equations become dense because derivative estimation amplifies observation noise.

This result is valid for the frozen A1 strong-form configuration, but a stronger training-side hyperparameter qualification should be added before making a broad statement about PySINDy robustness.

## Issue 1 — WeakPDELibrary baseline is not qualified

The weak-form smoke test already returned:
- active terms = 0

All 100 formal WeakPDELibrary runs then returned:
[
Q=0,
]
with:
- support F1 = 0
- coefficient error = 1
- Q error = 1

This is a **degenerate baseline configuration**, not evidence that Weak SINDy itself fails.

The A1 optimizer used:
- threshold = 0.05
- alpha = 1e-6
- normalize_columns = True

PySINDy's own diffusion-PDE test uses WeakPDELibrary with STLSQ and `normalize_columns=False`. The official STLSQ default is also `normalize_columns=False`.

A1-FIX1 must qualify weak-form hyperparameters on training-side data only and require a nonzero clean qualification before formal evaluation.

## Issue 2 — noisy IPM coefficient extraction leaks clean state

The A1 function `ipm_audit()` computes the local-law Jacobian from the corrupted/lifted observation, but Burgers/KdV/Allen-Cahn coefficient regression uses:

`u = clean[:,0,:]`

For noisy conditions, the coefficient estimator therefore receives clean state information that would not be available from the observation.

This does not affect:
- IPM Q error;
- IPM differential-order support;
- the clean coefficient result.

It **does affect noisy/sparse IPM coefficient-error claims**.

A1-FIX1 must use the observed/lifted base coordinate:
[
u_{obs}=a_0
]
for coefficient recovery.

## Metric-contract caution

PySINDy support F1 is **explicit symbolic term support**.

IPM support F1 in A1 is **differential-order support**.

They should not be placed in one column and interpreted as identical quantities in the paper.

A1-FIX1 will export them separately.

## Conclusion

A1 already establishes three robust observations:

1. official strong-form PySINDy is essentially exact on clean data when the true equation lies in its candidate library;
2. raw high-order jet differentiation and strong-form sparse discovery are both highly vulnerable to measurement noise;
3. IPMAdaptive preserves held-out local-law accuracy under 1–3% noise and spatial sparsity.

Before paper use, repair the weak baseline and noisy IPM coefficient audit without retraining IPM.
