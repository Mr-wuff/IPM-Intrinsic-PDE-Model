# IPM-B1-Q0 Results — Neural Surrogate / Operator Adapter Qualification

Formal preregistered decision: **B1_Q0_FAIL**

Result ZIP SHA256:
`7d5fd2d04a96a7b1d41c452c4dbb135dfe2cc26f1086ef8b1f9d397c3797d4cb`

Executed notebook SHA256:
`672b43f4e05335df379c46c908bd925b3de5b00170e9d8c9dceadb100167306b`

Frozen notebook SHA256:
`db74b28d96224e80f7cc1de4196c24ee0612eda8d0b8d0120bea99ea1b52b9e7`

The executed notebook has 10 code cells; all 10 are byte-for-byte identical to the frozen notebook. Differences are execution outputs/metadata only.

## Gate outcome

Passed:
- Q0-0 source/data integrity
- Q0-1 all six architectures construct
- Q0-2 all forward contracts
- Q0-3 all 12 short optimization runs finite
- Q0-4 short optimization signal
- Q0-6 official-source provenance

Failed:
- Q0-5 metric export completeness

Therefore the formal decision remains **FAIL**.

## Why Q0-5 failed

Training itself was successful. The failure is isolated to latency-checkpoint reload for official FNO and TFNO.

Reload error:
`Unexpected key(s) in state_dict: "_metadata"`

The NeuralOperator state dict serialized an auxiliary `_metadata` entry. The repository adapter's strict reload path did not strip that non-parameter key, so FNO/TFNO latency rows were exported as NaN.

This is an evaluation/serialization adapter defect, not a model-training failure.

A second audit issue is that the preregistered latency batch 64 was skipped because the test pool contains only 32 trajectories and the timing loop required `batch <= n_test`. FIX1 will create batch-64 timing inputs by deterministic repetition of frozen test states rather than silently omitting the row.

A third reporting issue is that the grid probe tested N=128/256/512 while the native PDEBench grid in this run is N=1024. DeepONet is fixed to the branch-input grid, so all three off-grid probes correctly failed but its native-grid support was not explicitly demonstrated. FIX1 adds N=1024.

## Optimization qualification succeeded

All 12 model x PDE runs completed all 128 updates and all 12 reduced the normalized training MSE by more than the preregistered 10% threshold.

Loss reduction range:
- minimum: ~83.35%
- maximum: ~99.04%

This strongly qualifies the optimization path itself.

## Short-run one-step accuracy

These numbers are **qualification diagnostics only**, not final model rankings.

### Advection beta=1

Test one-step Rel-L2 after 128 updates:
- FNO official: **0.022288**
- UNO official: **0.022321**
- TFNO official: **0.024020**
- UNet1D: **0.039453**
- ResNet1D: **0.095552**
- DeepONet official: **0.133122**

### Burgers nu=0.01

- FNO official: **0.042363**
- UNO official: **0.044417**
- TFNO official: **0.051280**
- UNet1D: **0.070856**
- ResNet1D: **0.072013**
- DeepONet official: **0.072682**

The three NeuralOperator spectral/U-shaped models show the strongest short-budget one-step signal on both PDEs.

## Compactness / training cost

Trainable parameters:
- TFNO official: **22,485**
- FNO official: **49,953**
- UNO official: **56,321**
- ResNet1D: **61,921**
- DeepONet official: **82,369**
- UNet1D: **265,617**

Checkpoint bytes:
- TFNO: **147,719**
- ResNet: **257,231**
- DeepONet: **338,809**
- FNO: **364,139**
- UNO: **405,389**
- U-Net: **1,074,871**

On the Tesla T4 qualification run, all 12 training jobs completed in ~0.61–3.11 s for 128 updates and peak training VRAM remained below 88 MB.

## Available latency signal

FNO/TFNO latency is invalid/missing because of the reload defect and must not be ranked from Q0.

Valid batch-1 examples:
- DeepONet: ~0.64–0.67 ms
- ResNet1D: ~1.23–1.33 ms
- UNet1D: ~1.76–1.88 ms
- UNO: ~7.42–9.47 ms

Again, these are Q0 adapter diagnostics, not final paper latency.

## Grid-contract probe

Variable-grid forward support was demonstrated at N=128/256/512 for:
- ResNet1D
- UNet1D
- FNO
- TFNO
- UNO

DeepONet's branch input is fixed-grid by construction in the current official adapter. Q0 failed to include the native N=1024 probe, so FIX1 will explicitly verify native support and retain off-grid unsupported status.

## Scientific conclusion

Q0 is a **formal FAIL caused by metric-export plumbing**, but the expensive part of the qualification is positive:

1. all six architectures construct;
2. all 12 training runs are finite;
3. all 12 show strong optimization signal;
4. official source provenance is correct;
5. the only formal blocker is incomplete latency export caused by the FNO/TFNO state-dict metadata entry.

No architecture should be removed.

Next: B1-Q0-FIX1 reruns the cheap 128-update preflight with corrected checkpoint sanitation, complete batch-1/16/64 latency, and native-grid contract verification. Formal B1-Q1 training begins only after FIX1 passes.
