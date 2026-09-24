# IPM-PDEBench-PB1-Q3-FIX1 Results — Gain-Aware Principal Closure Qualification

## Integrity

Uploaded result archive SHA256:

`64447e0003e1680feb5e5bb08e21a11643c96ca2fe4414876a2a45520b018ca6`

The detached manifest contains 17 payload entries. All 17 match the archived files by byte size and SHA256.

Frozen protocol SHA256:

`09ce00a186111268c89a5f68f26bbab54590d452e4771b17bb77a1400fc62fc7`

## Runtime semantic repair is validated

The gain-aware runtime audit passes:

- non-unit gain effect Rel-L2: `0.6299120`
- gain-aware vs gain-folded coefficient defect: `7.6044e-08`
- frozen tolerance: `2e-6`

Therefore the PB1-Q3 runtime-gain omission is resolved in IPM v1.0.2, and Q3-FIX1 rollout results are scientifically usable.

## Main results

| PDE | Candidate | unit secant | calibrated secant | secant ratio | unit rollout8 | calibrated rollout8 | rollout ratio |
|---|---|---:|---:|---:|---:|---:|---:|
| Advection beta=1 | T1_S111_NATIVE_LOCAL | 0.573332 | 0.254764 | 0.444357 | 0.943679 | 0.527312 | 0.558784 |
| Advection beta=1 | T1_S124_NATIVE | 0.603135 | 0.271182 | 0.449621 | 0.972623 | 0.550621 | 0.566120 |
| Burgers nu=0.01 | T1_S111_NATIVE_LOCAL | 0.529360 | 0.351860 | 0.664688 | 0.277156 | 0.191893 | 0.692366 |
| Burgers nu=0.01 | T1_S124_NATIVE | 0.609728 | 0.214434 | 0.351688 | 0.286332 | 0.169935 | 0.593488 |

The train-only gain calibration therefore transfers into the real compiled native flow, not only the central-secant proxy.

The characteristic amplitude ratios also move close to one after calibration:
- Advection S111: 0.569950 -> 0.925654
- Advection S124: 0.495844 -> 0.919196
- Burgers S111: 0.653550 -> 0.988684
- Burgers S124: 0.458163 -> 0.993295

## Frozen gate outcome

Both candidates pass:
- finite training/rollout;
- calibrated secant ratio <= 0.70 on both PDEs;
- calibrated rollout ratio <= 0.70 on both PDEs;
- gain-aware/gain-folded runtime parity <= 2e-6.

Both fail only the frozen absolute rollout condition because Advection remains slightly above 0.50:

- S111: `0.527312`
- S124: `0.550621`

Burgers already passes comfortably:
- S111: `0.191893`
- S124: `0.169935`

Therefore:

`FORMAL_500_EPOCH_RUN_AUTHORIZED=false`

The 0.50 gate is not relaxed post hoc.

## Scientific conclusion

PB1-Q3-FIX1 changes the diagnosis substantially:

1. native-time IDTC identification has a real learning signal;
2. principal-role gain calibration is real and causally changes compiled rollout;
3. the repaired runtime executes gains correctly;
4. the remaining bottleneck is a small compiled-flow closure mismatch dominated by Advection, not a general failure of IPM identification.

The next experiment must target this one remaining closure mismatch before any full-scale training.
