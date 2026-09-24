# IPM-PDEBench-PB1-Q1 Results — Same-Scale Standard-Data Run

Result ZIP SHA256:
`cc96ad8e72a5806238b1bb2da7e6b604f406923b231c68c9ae73027356dc9421`

Executed notebook SHA256:
`1965d5b83c685482f7da3917918127944333a40a163a0119b87644458819cb54`

Frozen notebook SHA256:
`c2d96c686598ece0b832d498133cc77c4a15c2470f823e35339540f90df01afc`

Protocol SHA256:
`8504bfb85b9e65303070a71dd18d2dac0e5d2073dc37914243a84125be293692`

The result ZIP matches its external SHA file and all 27 detached-manifest entries match their archived bytes.

## Critical protocol deviation

The frozen preregistration required the pilot to satisfy:

`final_epoch_loss <= 0.8 * first_epoch_loss`

before the 500-epoch formal run could start.

The executed notebook changed this line after observing the pilot behavior to:

`final_epoch_loss <= 0.99 * first_epoch_loss`

with the explicit code comment:

`Adjusted threshold from 0.8 to 0.99 to allow the run to proceed`

Observed five-epoch pilot loss ratios were:
- Advection: **0.988186**
- Burgers: **0.988568**

Therefore both tasks would have **failed the preregistered 0.8 pilot gate**.

The automatic final harness label `PDEBENCH_PB1_Q1_COMPLETE` must not be interpreted as a preregistered formal PASS. The 500-epoch continuation is retained as a valuable post-hoc/exploratory negative result.

Recommended archival status:

**FORMAL PILOT GATE FAIL / POST-HOC 500-EPOCH CONTINUATION COMPLETED**

No result is discarded.

## Fairness contract actually executed

The long run did match the intended nominal public-data scale:
- official 90% train / 10% held-out split;
- 9,000 train trajectories;
- 1,000 held-out trajectories;
- spatial reduction 4;
- temporal reduction 5;
- batch size 50;
- 500 epochs;
- 180 trajectory batches/epoch;
- 90,000 optimizer updates per task/seed;
- 4,500,000 trajectory exposures per task/seed;
- seeds 101 / 202 / 303.

All six long runs completed with finite loss.

This establishes that the negative result is not a short-run/OOM artifact.

## Long-run optimization behavior

### Advection

Mean first-epoch loss across three seeds:
**0.986224**

Mean final-epoch loss:
**0.965985**

Only about **2.05%** reduction after 90,000 updates.

The objective effectively plateaus near one.

### Burgers

Mean first-epoch loss:
**0.985509**

Mean final-epoch loss:
**0.695866**

Burgers learns substantially more than Advection, but the plateau remains high.

Mean per-seed wall time on Tesla T4:
- Advection: **1739.7 s** (~29.0 min)
- Burgers: **1715.4 s** (~28.6 min)

Peak allocated training memory:
- Advection: ~386 MB
- Burgers: ~746 MB

## Official PDEBench accuracy

All values are from the pinned official PDEBench `metric_func`.

### Advection beta=1

nRMSE:
- official FNO: **0.012769**
- frozen historical-low-data IPM: **0.250003 ± 0.101671**
- official U-Net: **0.296940**
- standard-data same-scale IPM: **0.930727 ± 0.003389**

RMSE:
- FNO: **0.006884**
- frozen IPM: **0.161984 ± 0.064686**
- U-Net: **0.186403**
- standard-data IPM: **0.622808 ± 0.004137**

The frozen low-data IPM is better than the released U-Net checkpoint on mean RMSE/nRMSE in this official evaluator, but far behind FNO.

The same-scale training protocol makes IPM much worse, not better.

### Burgers nu=0.01

nRMSE:
- FNO: **0.010364**
- frozen historical-low-data IPM: **0.190939 ± 0.000450**
- official U-Net: **0.287901**
- standard-data same-scale IPM: **0.356557 ± 0.001220**

RMSE:
- FNO: **0.003550**
- frozen IPM: **0.086616 ± 0.000188**
- U-Net: **0.092700**
- standard-data IPM: **0.139068 ± 0.000394**

Again, frozen IPM is competitive with / better than the released U-Net checkpoint, but the same-scale fit degrades accuracy.

## Learned-law diagnosis

The compiled same-scale programs are strongly attenuated relative to the physically expected leading terms.

Advection:
- learned leading T coefficient is about **-0.118** for all three seeds;
- frozen programs were near **-1**.

Burgers:
- learned leading nonlinear transport coefficient is about **-0.40**;
- learned leading diffusion coefficient is about **0.0033**;
- both are substantially attenuated relative to the expected order of the target law.

The three same-scale seeds converge to very similar wrong laws, so this is not primarily seed instability.

Non-principal canonical coefficient mass is small (~0.1% L1 for Advection and ~0.5-0.6% for Burgers), so principal-role compilation is not the main source of the failure.

The dominant evidence points to a training-contract / trajectory-objective mismatch.

## Runtime / deployment

### Frozen historical-low-data IPM

Same-process full official horizon, batch 1:
- Advection: **9.257 ms**
- Burgers: **29.844 ms**

Official FNO:
- Advection: **59.370 ms**
- Burgers: **59.799 ms**

Thus frozen IPM is approximately:
- **6.41x faster** than FNO on Advection batch 1;
- **2.00x faster** on Burgers batch 1.

At batch 64:
- frozen IPM is ~**6.82x faster** than FNO on Advection;
- ~**2.15x faster** on Burgers.

### Same-scale dense-RTDS IPM

The dense program is slower because all R/T/D/S runtime paths remain active.

It is:
- slower than FNO for Advection batch 1;
- roughly tied at batch 16;
- faster at batch 64;
- faster than FNO on Burgers at all measured batches.

This is a secondary result because the standard-data fit itself failed scientifically.

## Deployment size

Official FNO:
- 23,937 trainable parameters
- 533,251-byte checkpoint

IPM compiled programs:
- frozen Advection: 36 effective scalars / 267 bytes
- frozen Burgers: 38 effective scalars / 401 bytes
- same-scale dense RTDS: 39 effective scalars / 362-423 bytes

Thus the frozen IPM/FNO deployment-size gap is roughly three orders of magnitude in checkpoint bytes and >600x in scalar count.

Official U-Net has ~2.71M parameters and ~32.6 MB checkpoint.

## Scientific conclusion

This experiment does **not** show that “more PDEBench data hurts IPM” in general.

It shows that the specific attempted fairness recipe:

> official temporal reduction 5 + FNO/U-Net optimizer schedule + current Simpson triplet objective + dense RTDS compilation

is poorly matched to the IPM identification problem.

The original preregistered pilot gate correctly warned of this: both tasks failed the required 20% five-epoch loss reduction.

The next experiment must diagnose the training contract cheaply before any new 500-epoch run.

Primary hypothesis to test:
- local continuous-law identification needs finer temporal sampling than the operator baselines' temporally reduced autoregressive training contract.

Secondary hypotheses:
- equal weighting of strides 1/2/4 at the reduced time step;
- optimizer/regularization mismatch;
- normalization/conditioning of the trajectory-only objective.

No new full-scale training is allowed until a mechanism qualification stage closes this issue.
