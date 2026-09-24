# IPM-PDEBench-PB1-Q5 Results — Formal Standard-Data Native-Closure 3-Seed Run

## Integrity

Result ZIP SHA256:

`71a7c3e42726c5727584f0d9f7ffcfdbae15fb00bece443fa376c38072aae1b3`

Detached result manifest: **28/28 entries match** by byte size and SHA256.

Frozen protocol SHA256:

`3b2b70632f66f08fb97ac77d9ad3e9499459f7ea2a60bfa2da5d18ccaf634f1a`

Runtime semantic audit:
- runtime parity Rel-L2: `0.0`
- gain gradient norm: `0.1773872226`
- gain gradients finite/non-zero: `true`
- all six formal runs present: `true`
- official test accessed only after all six compiled programs were frozen: `true`
- seed selection: `false`
- maximum independent RMSE/nRMSE audit relative difference: `2.22e-7`

## Formal public metrics

| PDE | RMSE mean ± std | nRMSE mean ± std |
|---|---:|---:|
| Advection beta=1 | **0.043089 ± 0.005784** | **0.072775 ± 0.008730** |
| Burgers nu=0.01 | **0.134618 ± 0.000312** | **0.457651 ± 0.006035** |

Official PB1-Q1 reference:
- Advection FNO nRMSE `0.012769`; U-Net `0.296940`
- Burgers FNO nRMSE `0.010364`; U-Net `0.287901`

## Interpretation

The formal outcome is mixed and must not be summarized as a universal PB1-Q5 accuracy pass.

### Advection

The native-time S111 contract closes successfully at full standard-data scale.

Compared with the earlier PB1-Q1 same-scale IPM:
- nRMSE: `0.930727 -> 0.072775` (**92.18% reduction**)
- RMSE: `0.622808 -> 0.043089` (**93.08% reduction**)

Compared with the historical low-data frozen IPM:
- nRMSE: `0.250003 -> 0.072775` (**70.89% reduction**)

The formal Q5 IPM is substantially better than the released U-Net checkpoint on Advection, but remains behind the official FNO checkpoint.

The three Advection seeds recover almost the same transport law:
- principal transport constant coefficient about `-1.0037`
- final transport gain about `0.996-0.999`

Training loss falls from about `0.79` at epoch 1 to about `2.2e-4`, and training-block secant error is about `0.00627`.

### Burgers

The same contract does **not** close the full long-horizon Burgers problem.

Compared with PB1-Q1 same-scale IPM:
- nRMSE: `0.356557 -> 0.457651` (**28.35% worse**)

Compared with historical low-data frozen IPM:
- nRMSE: `0.190939 -> 0.457651` (**139.68% worse**)

Compared with the released U-Net:
- nRMSE ratio: `1.590`

The result is highly seed-stable, so this is not a single-seed accident.

Training-block diagnostics already reveal the difference from Advection:
- final integral-flow loss remains `0.392-0.413`
- refined secant error remains `0.664-0.691`
- 8-step training-block rollout remains much better (`0.212-0.247`) than the final 31-step public behavior

The frozen Burgers IDTC canonical expansion also contains about **1.71-1.75% non-principal L1 mass**, compared with only about **0.003%** for Advection. Dominant Burgers non-principal terms include `u * u_x^2` and `u_x^2`.

This means the remaining Burgers failure must be causally separated into:
1. local jet/derivative estimation;
2. non-convex IDTC factorization/optimization;
3. principal-normal-form projection;
4. short-horizon gain closure versus long-horizon flow;
5. native runtime integration.

No additional 500-epoch Advection/Burgers run is authorized until that causal audit is complete.

## Runtime

The dense RTDS Q5 program records roughly `40-58 ms` for the 31-step horizon on Tesla T4 depending on task/seed/batch. These numbers remain secondary until all baselines are timed in the same process/hardware/software contract.

## Archival status

**PB1-Q5 FORMAL COMPLETE / MIXED SCIENTIFIC OUTCOME**

- Advection branch: formal standard-data closure established.
- Burgers branch: long-horizon identification/closure remains unresolved.
- Next stage: low-cost PB1-Q6 causal bottleneck audit using the frozen Q5 artifacts and training block only.
