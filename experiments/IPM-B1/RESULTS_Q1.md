# IPM-B1-Q1 Results — Matched-Update Neural Benchmark

Result ZIP SHA256:
`60596dc5b20ec6e2013d454fb10bf80c1bd78f808f8a2616943f8e2fadeb42e0`

Formal harness decision:
`B1_Q1_COMPLETE`

All 36 neural training runs completed all 1536 optimizer updates.

## Training fairness

Within each PDE and seed, all six neural baselines used:
- the same 128 training trajectories;
- the same deterministic sampled trajectory/time schedule;
- batch size 16;
- 1536 optimizer updates;
- identical normalized one-step MSE objective;
- identical residual one-step wrapper;
- identical AdamW learning rate / weight decay / gradient clipping.

Therefore the six neural baselines are matched in data exposure and optimizer-step budget.

This does **not** mean neural-vs-IPM is data-budget matched: IPM-v1 was frozen from its earlier discovery/calibration pipeline and was not retrained under B1-Q1.

## Training result

All 36 runs reached terminal status `complete`.

Representative final diagnostic means at update 1536:

Advection one-step / 8-step:
- ResNet1D: 0.00677 / 0.04620
- UNet1D: 0.00706 / 0.05934
- FNO: 0.02146 / 0.01800
- TFNO: 0.02047 / 0.02214
- UNO: 0.02121 / 0.01918
- DeepONet: 0.13382 / 0.33037

Burgers:
- ResNet1D: 0.01210 / 0.06050
- UNet1D: 0.02739 / 0.11228
- FNO: 0.01294 / 0.04839
- TFNO: 0.01840 / 0.07318
- UNO: 0.01956 / 0.06332
- DeepONet: 0.07327 / 0.26047

These are diagnostic-node results only.

## Critical formal-evaluation defect

All 36 neural formal rollout evaluations failed with:

`RuntimeError: indices should be either on cpu or on the same device as the indexed tensor (cpu)`

The defect occurs in the formal evaluation path, not training.

As a result:
- all neural `rollout_rel_l2` values in `neural_accuracy.csv` are NaN;
- the generated neural-vs-IPM error-latency Pareto table is invalid;
- the paired neural-vs-IPM accuracy table is invalid;
- B1-Q1 must **not** be cited as a formal neural accuracy comparison.

The completion gate was too weak because it required evaluation to be attempted, not successfully completed. The `B1_Q1_COMPLETE` label therefore means infrastructure/training record completeness only, not scientifically valid formal accuracy completion.

## Valid outputs retained

Valid evidence:
- 36/36 completed training runs;
- training time / peak VRAM / parameter / checkpoint cost;
- intermediate one-step and 8-step diagnostics;
- eager/CUDA-Graph runtime measurements;
- frozen IPM reproduction.

Invalid for paper:
- final 40-step neural rollout accuracy;
- final neural spectral metrics;
- neural-vs-IPM Pareto based on those NaN errors.

## Benchmark strategy change

The project will not spend further compute reproducing large collections of baselines locally as the primary paper evidence.

The next benchmark phase prioritizes official public benchmark harnesses and published/pretrained baselines:
1. PDEBench official protocol/evaluator and official pretrained FNO/U-Net/PINN;
2. Representative PDE Benchmarks / CNO on compatible tasks;
3. PDEArena after a validated 2-D/multifield IPM extension;
4. The Well after multidimensional/multifield support is frozen.

Internal B-series runs remain diagnostic/control experiments, not the primary public benchmark claim.
