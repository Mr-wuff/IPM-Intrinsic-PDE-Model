# Formal Experiment Protocol

Every IPM experiment must be preregistered in the repository before long training.

## Required header
- Experiment ID
- scientific question
- null hypothesis
- proposed mechanism
- baselines
- fixed compute budget
- datasets/PDEs
- primary metrics
- failure criteria
- success gate

## Fairness rules
- capacity-matched and compute-aware comparisons;
- identical train/validation/test splits;
- identical reference trajectories;
- identical rollout horizons;
- no baseline-specific handicaps;
- hyperparameter tuning budget disclosed for every method.

## Diagnostics before formal training
1. tensor/shape/unit tests;
2. derivative accuracy test;
3. manifold/consistency test;
4. numerical integrator sanity test;
5. overfit-tiny-batch test;
6. gradient-scale/conditioning audit;
7. stability smoke rollout;
8. baseline convergence check.

## Artifact bundle
Each run exports:
- config.json
- environment.txt
- seed_manifest.json
- train_metrics.csv
- eval_metrics.csv
- gates.json
- failure_analysis.md
- figures/
- tables/
- checkpoints/
- RESULT_MANIFEST.json

## Paper rule
A result can enter the paper only if it is reproducible from a frozen commit and passes the experiment's preregistered validity checks.
