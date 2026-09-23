# IPM-A2-Q3-FIX2 Frozen Run

Notebook:
`IPM_A2_Q3_FIX2_Principal_Normal_Form_Calibration_Compiler_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`61ff9a11670b2028102c524b29e134d1b5c6d1432b51b0654a189838940ea0db`

Protocol SHA256:
`22381bf60de083cc332790da6675cf74b838f51fc2bfed4a7e5430601c3d8dea`

Required parents:
- Q0: `6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`
- Q2: `23f7af45c0318992b6ae2fd6570a06a04ddd06c258463aaff9e9e3d9f0020b77`
- Q3-FIX1: `fbf93087ce7546f972d72d759b998fecafba48cab5c82a9bcb748cae51aef273`

Static Python syntax validation: PASS.

No neural retraining. Frozen Q2 IDTC checkpoints are compiled into a nuisance-free principal normal form with at most four calibration gains using disjoint PDEBench training-pool blocks.

Headline deployment metric: current-hardware end-to-end physical-step latency against the frozen official NeuralOperator FNO reconstructed from Q0.