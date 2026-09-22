# IPM-M4 Run

Notebook:
`IPM_M4_Sparse_Noisy_Trajectory_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`e184db87322ee3e406d0318bb6380abc7e9f21ae795aa35dc1e0259a9f347ff4`

Frozen protocol SHA256:
`afc92e109afbc90f7d8deb6b174234229c90bac577e9847bb48b14dd5d2edd08`

Frozen IPM core SHA256:
`f7947e36fdcc29dc13682bfc9ceecf6cbe15f2dd79123f63842be284372947a3`

Frozen observation-lift SHA256:
`329cea4321ce6b04708b68142edb264802a666b7617d225194419ab8131f7c5a`

## Purpose

Qualify the frozen IPM mathematical core under sparse/noisy trajectory observations without adding a learned denoiser or modifying the characteristic architecture.

## Training observation distribution

- spatial points: 32 / 64 / 128
- temporal factors: 1 / 2 / 4
- relative Gaussian noise: 0 / 0.5% / 1% / 2%

## Held-out conditions

- spatial points: 48 / 96
- temporal factor: 3
- relative noise: 3%
- extreme diagnostics: 5% noise and 24 points

## Methods

- CleanIntegralFlow
- RawJetIntegralFlow
- ScaleJetIntegralFlow
- ScaleJetSecant

## Observation-lift interpretation

The scale-space Fourier filter is a fixed non-learned observation interface. It is not part of the frozen IPM core or the paper's architecture novelty claim.

## Efficiency diagnostics

The notebook records:
- repeated-FFT jet latency;
- fused one-forward-FFT jet latency;
- Q-only latency;
- full jet + Q RHS latency;
- grid-size scaling through N=512.

## Artifact behavior

At completion the notebook creates and automatically downloads:
- `IPM_M4_RESULTS.zip`
- `IPM_M4_RESULTS.zip.sha256`

## Serialization fix

The protocol is embedded as canonical JSON and parsed with `json.loads`, preventing the JSON `true` / Python `True` error observed in M3-FIX1.
