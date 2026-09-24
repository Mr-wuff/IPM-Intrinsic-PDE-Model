# IPM-PDEBench-PB1-Q2 — Temporal Identification Contract Qualification

## Motivation

PB1-Q1 attempted a same-data/same-scale IPM fit under the official PDEBench temporally reduced operator-learning contract.

The frozen preregistered pilot gate required a five-epoch loss ratio <=0.8. The observed ratios were ~0.988 for both tasks, so the original gate failed. A post-hoc threshold relaxation allowed the long run to proceed; the 500-epoch results then confirmed severe underfitting / law attenuation.

No new 500-epoch fit is allowed until the mechanism is diagnosed.

Primary hypothesis:

> IPM continuous local-law identification requires finer temporal sampling than the operator baselines' `reduced_resolution_t=5` autoregressive contract.

This is a training-contract question, not an IPM architecture change.

## Data

Official PDEBench Advection beta=1 and Burgers nu=0.01.

Spatial reduction is fixed at 4 for every variant.

Training trajectories:
- official training split only;
- first 1000 official training trajectories for optimization;
- next 256 official training trajectories for validation;
- official held-out test split is not accessed for model selection.

Batch size:
- 50 trajectories.

Seed:
- 202.

Epochs:
- 20.

Thus every variant uses exactly 400 optimizer updates.

## Equal sampled-observation geometry

Every update samples three Simpson triplets per trajectory.

To keep the number of sampled frames per update matched, single-stride variants repeat the same stride family three times but draw independent start locations.

Variants:

1. **T5_S124_CONTROL**
   - temporal reduction 5;
   - strides (1,2,4);
   - reproduces the failed PB1-Q1 training contract.

2. **T5_S111_LOCAL**
   - temporal reduction 5;
   - strides (1,1,1);
   - isolates whether long multi-stride windows are the main problem while preserving three triplets/update.

3. **T1_S5_10_20_PHYSICAL_MATCH**
   - native temporal resolution 1;
   - strides (5,10,20);
   - same physical time separations as T5_S124;
   - controls for loader/layout effects versus physical interval effects.

4. **T1_S124_NATIVE**
   - native temporal resolution 1;
   - strides (1,2,4);
   - architecture-native local-time identification.

5. **T1_S111_NATIVE_LOCAL**
   - native temporal resolution 1;
   - strides (1,1,1);
   - most local trajectory-only identification while retaining the same three-triplet sample count.

No exact RHS is supplied to training.

## Optimizer

All variants keep the PB1-Q1 optimizer:
- Adam
- lr 1e-3
- weight decay 1e-4
- no scheduler effect within 20 epochs because scheduler_step=100.

This isolates temporal sampling before testing optimizer changes.

## Training-only validation

Variant selection must not use the official test split.

For the next 256 official training trajectories, report:

1. deterministic held-out normalized Simpson residual;
2. common physical 8-step rollout error at the official PDEBench evaluation step `dt_official = 5 * dt_raw`;
3. full IDTC vs compiled dense-RTDS characteristic discrepancy;
4. principal role contribution fractions;
5. leading coefficient diagnostics.

The common 8-step rollout always uses the compiled continuous law at `dt_official`, regardless of training temporal resolution.

## Known-law coefficient diagnostics

These are diagnostics only and are not supplied to optimization.

For Advection beta=1:
- expected dominant T constant coefficient is order -1.

For Burgers nu=0.01:
- expected dominant nonlinear transport coefficient is order -1;
- expected leading diffusion coefficient is order 1e-2.

The diagnostic records direction and magnitude error but does not alter the fit.

## Hypothesis tests

### H-TEMPORAL

Supported if at least one T1 native-local variant reduces the common validation 8-step Rel-L2 by >=40% relative to T5_S124_CONTROL on both tasks.

### H-LONGSTRIDE

Supported if S111 materially outperforms S124 at fixed temporal resolution.

### H-LOADER

Refuted if T1_S5_10_20_PHYSICAL_MATCH behaves similarly to T5_S124_CONTROL. This would show that the physical time interval, not merely loader representation, drives the failure.

### H-COMPILER

Compilation is not the primary problem if dense-RTDS Q differs from the full trained IDTC Q by <=5% relative RMS on validation jets.

## Gate for a new full-scale run

A new 500-epoch standard-data run is authorized only if one predeclared variant satisfies all of:

- finite optimization;
- final 20-epoch loss <=0.8 * first-epoch loss OR held-out integral residual <=0.8 * control;
- common physical 8-step validation rollout Rel-L2 <=0.6 * control on both PDEs;
- compiled/full characteristic discrepancy <=0.05 on both PDEs;
- no role/component produces non-finite rollout.

If no variant passes, do not launch another 500-epoch run. The next stage must investigate objective conditioning / optimizer design.

## Fairness interpretation

This qualification separates two public-benchmark fairness tracks:

### Protocol-matched track
Same processed `reduced_resolution_t=5` data as official FNO/U-Net.

### Data-budget-matched architecture-native track
Same raw training trajectories, same batch/epoch/update scale and same sampled triplet count per update, but temporal locations are selected at the resolution required by local continuous-law identification.

If the native track is adopted later, the paper must label it explicitly rather than claiming identical preprocessing.
