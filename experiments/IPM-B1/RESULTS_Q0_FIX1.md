# IPM-B1-Q0-FIX1 Results — Complete Metric Export Qualification

Formal decision: **B1_Q0_FIX1_PASS**

Result ZIP SHA256:
`c3bab71860aefb863162d82d5c928d334d29ebd66b86adb90b005d7e187d92e7`

Executed notebook SHA256:
`ff2380d06f5ab31199365b7ac3c21c0b0fdaf034c74fbc40cc33af9083437f71`

Frozen notebook SHA256:
`e2ce0e4ce3331d62a7f19d7b227c97f0c0ddaa053f3093fe7d21aaf5bef11710`

All 10 code cells in the executed notebook are byte-for-byte identical to the frozen notebook. Result-manifest verification also passed for all 24 archived files.

## Gates

All eight FIX1 gates pass:
- F0 source/data integrity
- F1 native construction/forward
- F2 all 12 short runs finite
- F3 short optimization signal
- F4 FNO/TFNO strict reload equivalence
- F5 complete 36-row latency export
- F6 complete 24-row grid-contract export
- F7 cost/provenance export completeness

## Checkpoint repair

Every one of the 12 model x PDE checkpoints reloads strictly after removal of non-parameter serialization metadata only.

For all 12:
- missing keys = []
- unexpected keys = []
- reload output Rel-L2 defect = **0.0**

This closes the Q0 FNO/TFNO `_metadata` serialization defect without weakening strict checkpoint validation.

## Optimization qualification

All 12 runs complete all 128 optimizer updates.

Loss-reduction range:
- minimum: **0.833487**
- maximum: **0.990386**

Thus all 12 pass the preregistered >=10% short-optimization criterion.

### Advection beta=1 one-step diagnostic

After 128 updates:
- FNO official: **0.022288**
- UNO official: **0.022321**
- TFNO official: **0.024020**
- UNet1D: **0.039452**
- ResNet1D: **0.095552**
- DeepONet official: **0.133122**

### Burgers nu=0.01 one-step diagnostic

- FNO official: **0.042363**
- UNO official: **0.044417**
- TFNO official: **0.051280**
- UNet1D: **0.070856**
- ResNet1D: **0.072013**
- DeepONet official: **0.072682**

These remain qualification diagnostics, not final rankings.

## Parameter / checkpoint cost

Trainable parameters:
- TFNO official: 22,485
- FNO official: 49,953
- UNO official: 56,321
- ResNet1D: 61,921
- DeepONet official: 82,369
- UNet1D: 265,617

Checkpoint bytes:
- TFNO: 147,719
- ResNet: 257,231
- DeepONet: 338,809
- FNO: 364,139
- UNO: 405,389
- UNet: 1,074,871

## Complete native-grid latency diagnostic (Tesla T4, N=1024)

Mean batch-1 latency across the two PDE runs:
- DeepONet official: **0.652 ms**
- ResNet1D: **1.345 ms**
- UNet1D: **1.690 ms**
- FNO official: **5.296 ms**
- TFNO official: **8.113 ms**
- UNO official: **8.842 ms**

Batch-16 mean:
- DeepONet: **0.627 ms**
- ResNet1D: **1.233 ms**
- UNet1D: **2.123 ms**
- FNO: **5.214 ms**
- UNO: **7.899 ms**
- TFNO: **8.296 ms**

Batch-64 mean:
- DeepONet: **0.647 ms**
- UNet1D: **4.227 ms**
- ResNet1D: **4.744 ms**
- FNO: **6.084 ms**
- TFNO: **8.774 ms**
- UNO: **11.083 ms**

These are eager one-step adapter diagnostics only. The paper-level Q1 benchmark will use the shared N=256 B0 grid, full 40-step rollout, and both eager and whole-horizon CUDA-Graph execution.

## Grid contract

At N=128/256/512/1024:
- ResNet1D: supported on all four
- UNet1D: supported on all four
- FNO: supported on all four
- TFNO: supported on all four
- UNO: supported on all four

DeepONet:
- N=128/256/512: unsupported by the frozen branch-input contract
- N=1024 native grid: supported

This correctly characterizes the current official DeepONet adapter as fixed branch-grid rather than generally unsupported.

## Scientific conclusion

B1-Q0-FIX1 closes the adapter qualification stage.

The six-model suite is technically valid for formal benchmarking. The NeuralOperator family shows the strongest short-budget one-step accuracy, while DeepONet is the fastest eager one-step adapter on this native-grid Q0 diagnostic. Neither statement is a final paper ranking.

Next: **B1-Q1**, a three-seed matched-update formal benchmark on the same N=256 PDEBench grid used by B0/IPM, with 40-step autoregressive rollout, latency/VRAM/training-cost accounting, and same-process frozen IPM-v1 comparison.
