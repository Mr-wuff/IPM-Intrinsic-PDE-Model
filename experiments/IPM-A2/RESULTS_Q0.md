# IPM-A2-Q0 Results — PDEBench + Official NeuralOperator FNO Qualification

## Integrity

Decision: **A2_Q0_PASS**

Result ZIP SHA256:
`6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`

The supplied SHA256 matches exactly.

Environment:
- Python 3.13.15
- PyTorch 2.11.0+cu128
- neuraloperator 2.0.0
- CUDA / Tesla T4

Official PDEBench MD5 validation passed for:
- Advection beta=1.0
- Burgers nu=0.01

The public files contain:
- tensor shape: (10000, 201, 1024)
- x-coordinate: 1024
- t-coordinate: 202

The executed notebook applies one implementation-only correction:
`t-coordinate[:T]`
so the time coordinate matches the 201 stored tensor states. No hypothesis, training or model change was made.

## Qualification gates

All Q0-0 through Q0-6 passed:
- official dataset MD5
- HDF5 schema
- official NeuralOperator FNO import
- IPM public-batch smoke
- pilot loss reduction
- finite public rollout
- metrics/efficiency export

Q0 is therefore an engineering/data-interface qualification success.

## Public rollout result

40-step public rollout Rel-L2:

| Task | NeuralOperator FNO | IPMAdaptive | IPMRaw |
|---|---:|---:|---:|
| Advection beta=1 | 0.06495 | 0.11239 | 0.82478 |
| Burgers nu=0.01 | 0.12561 | 0.93001 | 4.27718 |

This is not yet a competitive public-benchmark result for IPM.

IPMAdaptive / FNO error ratio:
- Advection: 1.73x
- Burgers: 7.40x

IPMRaw / FNO:
- Advection: 12.70x
- Burgers: 34.05x

## Training diagnostic

Final pilot training loss after 600 updates:

Advection:
- FNO: 6.20e-4
- IPMRaw: 3.92e-3
- IPMAdaptive: 6.97e-3

Burgers:
- FNO: 3.89e-4
- IPMRaw: 1.74e-1
- IPMAdaptive: 3.12e-1

The Burgers failure is already visible in teacher-forced training. Therefore the primary problem is generator identification/training, not merely autoregressive rollout accumulation.

## Noise and resolution

IPMAdaptive retains the robustness pattern from controlled experiments.

Advection:
- native 0.11239
- 1% noise 0.11259
- N/2 0.11237
- N/4 0.11254

Burgers:
- native 0.93001
- 1% noise 0.92993
- N/2 1.02045
- N/4 1.24299

Thus Adaptive observation lift remains nearly noise invariant and strongly resolution covariant on Advection; Burgers retains noise robustness but loses accuracy and degrades at the coarsest resolution.

IPMRaw improves dramatically when Advection is spatially downsampled, a strong indication that unresolved/high-frequency raw jet coordinates harm its learned law.

## Efficiency

Parameters:
- FNO: 50,529
- IPM: 9,889

IPM uses 19.57% of FNO parameters (80.43% fewer).

Training wall time:
- IPMRaw is ~1.84-2.21x faster than FNO
- IPMAdaptive is ~1.29-1.36x faster

Forward latency:
- IPMRaw is ~4.33-4.45x faster
- IPMAdaptive is ~2.11-2.62x faster

This confirms the efficiency advantage, but Q0 does not yet support an accuracy-efficiency Pareto claim on public data because Burgers accuracy is insufficient.

## Scientific diagnosis

The Q0 architecture is not failing because of model size, data loading, official FNO mismatch or numerical non-finiteness.

The key failure is that the current trajectory-only scalar integral law
[
u(t+2h)-u(t) approx rac{h}{3}[Q_t+4Q_{t+h}+Q_{t+2h}]
]
does not sufficiently identify the nonlinear local characteristic on public Burgers data at the pilot budget.

The next experiment therefore keeps the IPM architecture fixed and strengthens the **intrinsic jet evolution law**, rather than adding conventional neural-network components.

A2-FULL is blocked pending A2-Q1.
