# IPM-B1-Q0-FIX1 — Complete Metric Export Qualification

## Motivation

B1-Q0 formally failed only Q0-5 metric export completeness.

The scientific/training qualification was otherwise successful:
- all six architectures construct;
- all 12 model x PDE runs finish 128 updates;
- all 12 reduce normalized training error by >10%;
- official source provenance is verified.

The failure arose because official FNO/TFNO checkpoints reload with a non-parameter top-level `_metadata` entry, causing strict `load_state_dict` to reject the checkpoint during latency evaluation.

Two additional completeness issues are repaired:
1. preregistered batch-64 latency was silently skipped because the public test pool has only 32 trajectories;
2. the grid-contract probe omitted the native N=1024 grid, so fixed-grid DeepONet had no positive native-grid row.

## Scientific freeze

No architecture, optimizer, data split, residual wrapper, update budget, or source commit is changed.

The same six methods are retained:
- ResNet1D
- UNet1D
- official FNO
- official TFNO
- official UNO
- official DeepONet

Same external one-step residual wrapper:
[
hat u_{t+Delta t}=u_t+Delta_	heta(u_t).
]

Same:
- seed 202
- 128 training trajectories
- batch 16
- 128 optimizer updates
- AdamW
- lr 1e-3
- weight decay 1e-5
- deterministic schedule.

## Implementation repairs

### Checkpoint sanitation

Before strict reload, remove only state-dict keys:
- `_metadata`
- keys ending with `._metadata`

No tensor parameter/buffer key may be removed.

After sanitation:
- strict reload must succeed;
- a saved/reloaded model must reproduce pre-save output within Rel-L2 <= 1e-7 on a fixed audit batch.

### Batch-64 timing

For timing only, construct batch 64 by deterministic cyclic repetition of the frozen test input set.

This does not alter accuracy evaluation.

Required latency rows:
[
6	ext{ models}	imes2	ext{ PDEs}	imes3	ext{ batches}=36.
]

Batches:
- 1
- 16
- 64.

### Grid contract

Probe:
- N=128
- N=256
- N=512
- N=1024 native.

DeepONet is expected to support only its native branch grid in the frozen adapter.

No variable-grid quality claim is made.

## Gates

F0 source commits and PDEBench MD5s match.

F1 all six architectures construct and forward at native N=1024.

F2 all 12 short runs complete 128 finite updates.

F3 at least 10/12 runs reduce normalized training MSE >=10%.

F4 FNO and TFNO sanitized strict reload succeeds on both PDEs and output defect <=1e-7.

F5 latency export contains all 36 finite rows with VRAM records.

F6 grid-contract table contains all 24 rows (6 models x 4 grids), including positive native N=1024 DeepONet support.

F7 parameter/checkpoint/training-VRAM/source-provenance exports are complete.

Decision:
- **B1_Q0_FIX1_PASS** if F0-F7 all pass.
- **B1_Q0_FIX1_FAIL** otherwise.

## Transition

Only after FIX1 passes may B1-Q1 begin formal multi-seed neural benchmark training.
