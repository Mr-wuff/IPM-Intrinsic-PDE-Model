# IPM-A2-Q4 Frozen Run

Notebook:
`IPM_A2_Q4_Full_Symbol_Quasilinear_Flow_Compiler_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`f943663d23f2f69e2593e7952d5b36b742b156731a1f24a24f1923a5bb9ba86b`

Frozen protocol SHA256:
`17c9135066e7b238c36c43e6ad702569ffc91fe785265e57d82befbd2b0d59b9`

Required parent artifacts:
- Q2 ZIP SHA256: `23f7af45c0318992b6ae2fd6570a06a04ddd06c258463aaff9e9e3d9f0020b77`
- Q3 ZIP SHA256: `81b7f82937e6039512de903b212651040e0eacd30862758389c2186ef41a081f`

No neural retraining occurs in Q4.

The experiment compiles the frozen Q2 IDTC into a derivative-zero quasilinear normal form and evaluates a stable full-symbol flow. D1/D2/D3 and source OFF/ON are selected exclusively on the disjoint PDEBench training-pool calibration block.

Static Python AST validation: PASS.
