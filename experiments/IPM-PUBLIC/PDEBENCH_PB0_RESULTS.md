# IPM-PDEBench-PB0 Results — Official Evaluator Qualification

Formal decision: **PDEBENCH_PB0_PASS**

Result ZIP SHA256:
`4a2d77f9d954d9ff01a70f0b744f4df455a15efb7a9ba74febeca216c5a8b831`

Executed notebook SHA256:
`ecd95e295b6fcdf45919d3920995bc559544c985348b2552ca190d4f60ff2b80`

Frozen notebook SHA256:
`a52773de403bd209b191458000f779dc128e3edee4c0ab8e9732fb4f8f005c9a`

Protocol SHA256:
`befeeb9edb32b45e2674850a8e259bbf8682b668713074be566c8ca93d641496`

Pinned sources:
- IPM: `973a06a5e05ce75f3348475a28917650da2fbeae`
- PDEBench: `4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Entry label:
`IPM-v1 frozen / historical-low-data`

## Formal gates

All seven preregistered gates passed:

- PB0-0 pinned source provenance
- PB0-1 official data MD5
- PB0-2 official reduction contract
- PB0-3 full official horizon finite
- PB0-4 official PDEBench metrics finite
- PB0-5 independent RMSE/nRMSE audit
- PB0-6 complete public tables

## Official PDEBench metrics

All headline metrics below are produced by the pinned official PDEBench `metric_func`.

### Advection beta=1.0 — three frozen IPM seeds

Mean ± sample std:
- RMSE: **0.161984 ± 0.064686**
- nRMSE: **0.250003 ± 0.101671**
- conserved-variable error: **0.056312**
- max error: **1.533718**
- boundary RMSE: **0.131442**
- Fourier low: **0.043404**
- Fourier mid: **0.028970**
- Fourier high: **0.000906**

Seed-level RMSE / nRMSE:
- seed 101: 0.154902 / 0.237018
- seed 202: 0.101130 / 0.155448
- seed 303: 0.229919 / 0.357543

The Advection frozen programs therefore show substantial between-seed variation under the official temporally coarsened PDEBench contract.

### Burgers nu=0.01 — three frozen IPM seeds

Mean ± sample std:
- RMSE: **0.086616 ± 0.000188**
- nRMSE: **0.190939 ± 0.000450**
- conserved-variable error: **0.071268**
- max error: **0.871307**
- boundary RMSE: **0.048614**
- Fourier low: **0.044318**
- Fourier mid: **0.008869**
- Fourier high: **0.000170**

Seed-level RMSE / nRMSE:
- seed 101: 0.086597 / 0.190820
- seed 202: 0.086812 / 0.191437
- seed 303: 0.086437 / 0.190560

Burgers is exceptionally seed-stable under this contract.

## Metric audit

The independently implemented RMSE/nRMSE audit agrees with the official evaluator at floating-point scale.

Maximum observed relative differences:
- RMSE: about **1.72e-7**
- nRMSE: about **1.56e-7**

This is strong evidence that the official PDEBench metric function was invoked with the intended tensor/time contract.

## Secondary runtime

The official reduced-time future horizon contains 31 autoregressive steps.

Seed-202 eager full-horizon wall time on Tesla T4:

Advection:
- batch 1: **10.412 ms**
- batch 16: **10.198 ms**
- batch 64: **11.073 ms**

Burgers:
- batch 1: **29.274 ms**
- batch 16: **30.714 ms**
- batch 64: **30.262 ms**

Peak allocated inference memory recorded by this local measurement is about 0.78 / 0.96 / 1.52 MB for batch 1 / 16 / 64.

These runtime numbers are **secondary** and must not be compared to published baseline timing unless hardware/software/backend contracts are matched.

## User-applied notebook repairs

The executed notebook differs from the frozen notebook in two implementation-only changes:

1. an environment workaround cell was inserted before the formal code because the Colab runtime failed to locate `libnvrtc-builtins.so.13.0` during the Burgers complex spectral exponential path;
2. `import zipfile` was added to the final packaging cell after the original notebook raised a packaging-only `NameError`.

No benchmark dataset split, PDEBench configuration, frozen IPM coefficient, time step, model equation, seed, metric, or gate definition was changed.

### Important environment caveat

The successful workaround aliased an available CUDA 12.9 NVRTC builtins library under a CUDA 13.0 soname.

This produced finite, audited benchmark outputs in this run, but it is an ABI-dependent environment workaround and is **not** adopted as the canonical IPM runtime fix.

Future public notebooks should avoid relying on this alias. The preferred remedy is a mathematically equivalent real-valued construction of the spectral exponential or a fully compatible pinned CUDA/NVRTC environment, with explicit numerical-equivalence qualification.

## Result-package audit caveat

The ZIP-level SHA256 matches the supplied SHA file.

Five substantive archived files match the recorded size/hash entries:
- protocol
- official metric table
- summary table
- runtime table
- qualification report

The manifest's self-entry does not match the final manifest bytes because the notebook hashed `RESULT_MANIFEST.json` before overwriting that same file with the completed manifest. This is a self-referential packaging bookkeeping defect, not a scientific-data defect.

Future notebooks must exclude the manifest itself from its internal file-hash table (or write a detached manifest after all other files are frozen).

## Scientific interpretation

PB0 proves that frozen IPM-v1 can be inserted into the official PDEBench data/evaluation contract with no benchmark-specific fitting and remain finite over the full official reduced-time horizon.

It does **not** yet establish a direct current ranking against PDEBench FNO/U-Net/PINN, because PB0 evaluates only IPM.

The next public stage must use the official PDEBench pretrained artifacts directly, rather than retraining those baselines locally.
