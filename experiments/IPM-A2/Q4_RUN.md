# IPM-A2-Q4 Frozen Run

Notebook:
`IPM_A2_Q4_Parallel_Native_Execution_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`fbc208a2fcc7e66b4eb90575e4a855b2ab68adabb3ee59022ea0d97effc3fa16`

Protocol SHA256:
`366cb38d84aba05d6ab24b89dd03e8c4d55808a2a3c75b87188bcca59e15eb5c`

Required parents:
- Q0: `6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`
- Q3-FIX2: `f55c97725c51e82cbe76c981eaa66337b65cb9df98951d0b2566fc6b9a76cedc`

Execution variants:
- E0 frozen eager
- E1 tensor-fused static
- E2 torch.compile reduce-overhead
- E3 CUDA-stream D/S lanes
- E4 single-step CUDA Graph
- E5 40-step CUDA Graph

No training, refitting, role-mask changes or PDE coefficient changes are permitted.

Static Python AST validation: PASS.
