# PDEBench PB1-Q0 Frozen Run

Notebook:
`IPM_PDEBench_PB1_Q0_Official_Pretrained_Artifact_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`b46b31c9832a55e2daae757871d72dde3b329ef19a523a652736ef2f99e4fc0c`

Protocol SHA256:
`76e6aeee9398ca9d180f968292bd0360347100f669df4b66a2b01af1cb372bd0`

Pinned IPM commit used by the notebook:
`bda83a980fbdc9504f24840a5b559f6ed99eaeca`

Pinned PDEBench commit:
`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Manual uploads required: **none**

Baseline training: **none**

Purpose:
- resolve official DaRUS V2 Advection/Burgers pretrained FNO/U-Net/PINN artifacts;
- verify published checksums;
- safely inventory/extract packages;
- strictly restore official FNO/U-Net checkpoints;
- resolve PINN legacy checkpoint compatibility;
- verify IPM-v1.0.1 CUDA Burgers runtime without creating an NVRTC soname alias;
- verify detached result-manifest bookkeeping.
