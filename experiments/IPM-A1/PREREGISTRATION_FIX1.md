# IPM-A1-FIX1 — Weak-SINDy Qualification and Leakage-Free Coefficient Audit

## Motivation

A1 completed operationally, but independent audit identified two paper-level fairness problems.

1. The WeakPDELibrary smoke test already produced zero active terms and all 100 formal weak runs returned the zero equation. This is a degenerate configuration, not a valid estimate of Weak-SINDy capability.
2. In noisy IPM coefficient recovery, the Jacobian was evaluated on corrupted/lifted observations but Burgers/KdV/Allen-Cahn coefficient regression used the clean base field. This leaks clean state information into noisy coefficient estimates.

No IPM model is retrained.

## External baseline

Pin official:
- `pysindy==2.1.0`
- `PDELibrary`
- `WeakPDELibrary`
- `STLSQ`
- `SpectralDerivative`

## Training-side PySINDy qualification

Hyperparameters are selected on dedicated qualification trajectories only.

Qualification PDE coefficients are fixed at the center of the A0 training ranges.

Qualification conditions:
- clean N=128
- 1% noise N=128

Formal unseen conditions remain:
- 3% noise N=128
- N=64 + 1% noise

### Candidate STLSQ configurations

Strong-form:
- normalize_columns = True with thresholds {0.02, 0.05, 0.1, 0.2, 0.5}
- normalize_columns = False with thresholds {1e-4, 3e-4, 1e-3, 3e-3, 1e-2}
- alpha = 1e-5
- unbias = True

Weak-form:
- normalize_columns = False
- thresholds {1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.2}
- alpha = 1e-5
- unbias = True

Weak `normalize_columns=False` follows the official PySINDy default and its diffusion-PDE test configuration.

### Selection criterion

No true equation coefficients or support are used for hyperparameter selection.

For each PDE and baseline:
1. fit each candidate on dedicated qualification-train trajectories;
2. evaluate trajectory-only Simpson integral residual on independent qualification-validation trajectories;
3. do this for clean and 1% noisy observations;
4. score = mean(clean residual, noisy residual) + 0.01 × active_term_count / library_size;
5. reject any weak candidate that gives zero active terms on its clean qualification fit.

The lowest-score configuration is frozen per PDE/baseline before formal test seeds are evaluated.

## Leakage-free IPM coefficient audit

For noisy/sparse cases define the observed state used in coefficient regression as

[
u_{obs}=a_0,
]

the base coordinate of the same raw/adaptive jet supplied to the IPM law.

Thus:
- Burgers/KdV transport coefficient is regressed against (u_{obs});
- Allen-Cahn reaction coefficient uses (1-3u_{obs}^2);
- no clean state is used for noisy coefficient recovery.

Clean exact-Q remains the evaluation target for robustness, which is legitimate because it measures corruption-induced prediction error.

## Metric separation

Do not combine different support notions.

PySINDy exports:
- symbolic term precision/recall/F1;
- false-positive term count.

IPM exports:
- differential-order precision/recall/F1;
- Jacobian coefficient error.

Both export:
- coefficient error;
- held-out exact-Q relative RMSE;
- runtime.

## Formal conditions

- clean N=128
- 1% noise N=128
- unseen 3% noise N=128
- unseen N=64 + 1% noise

Five seeds:
11, 29, 47, 71, 97.

## Integrity

F0 — A0 ZIP checksum matches.  
F1 — all 50 frozen IPM checkpoints present.  
F2 — PySINDy version/classes match official 2.1.0 package.  
F3 — each weak baseline passes nonzero clean qualification.  
F4 — selected PySINDy hyperparameters depend only on qualification data.  
F5 — IPM noisy coefficient estimator uses observed/lifted base state only.  
F6 — no IPM retraining.  
F7 — all successful formal results finite and all raw tables/equations exported.

Decision:
- DISCOVERY_FIX1_COMPLETE
- DISCOVERY_FIX1_INCOMPLETE

No winner-dependent gate is used.
