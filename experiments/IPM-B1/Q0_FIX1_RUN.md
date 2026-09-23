# IPM-B1-Q0-FIX1 Frozen Run

Notebook:
`IPM_B1_Q0_FIX1_Complete_Metric_Export_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`e2ce0e4ce3331d62a7f19d7b227c97f0c0ddaa053f3093fe7d21aaf5bef11710`

Frozen Protocol SHA256:
`72627d0fd7eac33f2690c654f9a34d1efb8beb3b2e61a810bd0dba889e572065`

Pinned IPM repository commit:
`609e63d5e4cc50b09af84ef6d135be2432272b3d`

No parent result ZIP uploads are required.

The run repeats the same short 128-update B1-Q0 qualification and repairs only:
- NeuralOperator state-dict `_metadata` sanitation before strict reload;
- complete batch 1/16/64 latency export;
- native N=1024 grid-contract audit.

Expected output:
- `IPM_B1_Q0_FIX1_RESULTS.zip`
- `IPM_B1_Q0_FIX1_RESULTS.zip.sha256`
