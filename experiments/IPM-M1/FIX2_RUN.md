# IPM-M1-FIX2 Run

Notebook:
`IPM_M1_FIX2_Pointwise_Intrinsic_Generator_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`48d1803f45bcb912e1b713e30fdf7c2cafc76e146d6233ec40a384ac9fe39b83`

Frozen protocol SHA256:
`9144cd394df0dec2eb6ea7f12f0c3bff7d4a751ef38d8786c099e8f7654ca8cc`

## Parent result
M1-FIX1 returned a corrected scientific status of **CONDITIONAL_M1**:
- structural and holonomic repair succeeded;
- order-structured HolonomicIPM strongly beat finite jet baselines;
- FieldState remained substantially stronger;
- dt/grid/parameter generalization remained insufficient;
- RawJet divergence was excluded from winner denominators.

## FIX2 core change
The proposed IPM generator is pointwise in jet space rather than spatially convolutional.

The experiment also adds:
- exact per-order RMS normalization;
- common generator Sobolev fidelity;
- common spectral de-aliasing;
- common short-rollout fine-tuning;
- strict finite-baseline winner gates;
- automatic ZIP + SHA256 download.

## Advancement
IPM-A0 remains blocked unless this experiment returns `PASS_M1_FIX2`.
