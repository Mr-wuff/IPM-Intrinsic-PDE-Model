# IPM-M4-FIX1 Run Record

Notebook:
`IPM_M4_FIX1_Resolution_Covariant_Spectral_Bandwidth_Jet_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`95ae51065c6b04515d7993de19f2721e32d59d5ed69e762d978da68f66dd5b09`

Frozen protocol SHA256:
`4d35b6ca83740f9721ad366e57bfd0b91b171442420979546cce5861f96fda37`

Frozen IPM core SHA256:
`f2538811881a1ff5b393f4febce1f8b6f71b69cac0fad00b0f0e2bb83d126c5c`

Frozen observation-lift SHA256:
`1e239004d0df92be787cc0a0a6a76a43d9102ba98b6ca6832c83c4cb8707d77d`

## Parent result
M4 returned `CONDITIONAL_M4`.

Important findings:
- fixed ScaleJet strongly improved 1–5% noise robustness;
- fixed ScaleJet introduced clean/extreme-sparsity bias;
- M4 hidden-clean-Q evaluation incorrectly fed raw jets to ScaleJet models;
- the fixed cutoff (0.5k_{Nyquist}) is discretization dependent;
- fused FFT jet was ~25% faster but missed the preregistered 0.60 latency ratio.

## FIX1 change
No IPM-core modification.

The only scientific change is the observation lift:
- estimate a robust spectral noise floor;
- infer the trusted physical signal bandwidth (k_E);
- define (k_c=min(2k_E,0.9k_N));
- construct all jet orders with one fused real FFT and batched inverse FFT.

## Structural smoke test
Executed before release:
- raw rFFT vs repeated FFT jet relative error: ~9.4e-8 to 1.33e-7 across N=64/128/256/512;
- analytic field estimated (k_E=6) at all four resolutions;
- estimated (k_capprox12) at all four resolutions;
- adaptive clean-jet relative error vs raw: ~0.00242;
- G2/G3 pre-training audits PASS.

## Output
The notebook automatically downloads:
- `IPM_M4_FIX1_RESULTS.zip`
- `IPM_M4_FIX1_RESULTS.zip.sha256`
