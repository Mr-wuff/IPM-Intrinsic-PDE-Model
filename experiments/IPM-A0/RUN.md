# IPM-A0 Run Record

Notebook: `IPM_A0_Controlled_Paper_Benchmark_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`0b1857719445ffadf6a8fd173ea806e1c68f19bd6d9d5f4dd8c587636f9fc4fe`

Frozen protocol SHA256:
`39dc7a1f7192d1bcaa2c7a10032cb5916c2b1a2415889df0d9687d28da2245cc`

Frozen controlled-benchmark source SHA256:
`fbadc59fa25574d88ed713d725e948d0fb19b8720b9c331ed4c69affa52efd89`

Static AST validation: PASS.

Additional model-forward smoke validation:
- IPM LocalCharacteristic: PASS, 10,081 parameters
- FieldMLP: PASS, 9,793 parameters
- ResNet1D_RHS: PASS, 14,137 parameters
- FNO1D_RHS: PASS, 26,017 parameters
- UNet1D_RHS: PASS, 15,601 parameters
- ConvDeepONet1D_RHS: PASS, 13,345 parameters

All tested models return finite [B,1,N] RHS tensors at N=128.

Expected outputs:
- `IPM_A0_RESULTS.zip`
- `IPM_A0_RESULTS.zip.sha256`
