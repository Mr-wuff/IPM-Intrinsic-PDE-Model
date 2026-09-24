# IPM-PDEBench-PB1-Q0 Results — Official Pretrained Artifact Qualification

Harness decision: **PDEBENCH_PB1_Q0_PASS**

Result ZIP SHA256:
`3f669495390623c42010bfda58996daafccb809dd3f5927b13d90c7652301f81`

Executed notebook SHA256:
`065583d8302b330571396288015696fb84e4177ea02909bd8a95e233fb5c5863`

Frozen notebook SHA256:
`b46b31c9832a55e2daae757871d72dde3b329ef19a523a652736ef2f99e4fc0c`

The 11 executed code cells are byte-for-byte identical to the frozen notebook.

Protocol SHA256:
`76e6aeee9398ca9d180f968292bd0360347100f669df4b66a2b01af1cb372bd0`

## Valid results

All six official DaRUS V2 archive packages were resolved and downloaded:
- advection FNO / U-Net / PINN
- Burgers FNO / U-Net / PINN

All six published MD5 checksums match exactly.

The detached result manifest also passes for all 12 hashed result files; the manifest correctly excludes itself, closing PB0's self-referential hash defect.

IPM-v1.0.1 source audit passes:
- runtime version 1.0.1;
- real decay + cosine/sine spectral multiplier detected;
- no notebook-created NVRTC soname alias;
- Burgers CUDA smoke finite.

## FNO / U-Net package restore

Strict state-dict restoration succeeded with no missing/unexpected keys and finite N=256 smoke output for both package families.

However, a post-run audit found that the Q0 helper selected the first/largest checkpoint found inside each multi-parameter TAR, rather than the exact paper target parameter.

The recorded smoke checkpoints were:
- Advection FNO: beta=4.0
- Advection U-Net: beta=4.0
- Burgers FNO: nu=1.0
- Burgers U-Net: nu=0.1

Therefore these rows prove **official archive/model-class compatibility**, not exact beta=1.0 / nu=0.01 target-checkpoint qualification.

PB1-FULL/Q1 must select exact filenames explicitly:
- `1D_Advection_Sols_beta1.0_FNO.pt`
- `1D_Advection_Sols_beta1.0_Unet-PF-20.pt`
- `1D_Burgers_Sols_Nu0.01_FNO.pt`
- `1D_Burgers_Sols_Nu0.01_Unet-PF-20.pt`

## PINN audit correction

The Q0 notebook labeled PINN restoration as `legacy_environment_incompatible`, but the actual reported failure was only:

`ModuleNotFoundError: No module named 'deepxde'`

Thus Q0 did **not** establish a true legacy serialization incompatibility. The archive integrity and checkpoint presence are valid; executable PINN restoration remains unresolved.

The next stage must either:
- install a compatible DeepXDE and load the exact beta=1.0 / nu=0.01 checkpoint; or
- use PDEBench's published protocol-native PINN metrics and clearly mark the protocol difference.

## Scientific decision

The artifact layer is sufficiently qualified to proceed, but Q0 is not itself a target-parameter accuracy benchmark.

Post-audit status:

**ARTIFACT_QUALIFICATION_PASS / TARGET_CHECKPOINT_EVALUATION_PENDING**

No Q0 smoke-output accuracy claim is paper-eligible.

## Fair-data transition

The next public experiment adopts two separate IPM entries:

1. **IPM-v1 frozen / historical-low-data** — PB0 result, no PDEBench-specific fitting.
2. **IPM-v1 standard-data** — same frozen architecture trained from scratch using the official PDEBench FNO/U-Net training split and nominal training scale.

For the standard-data track, the fair nominal budget is:
- same 90% official training split;
- same spatial reduction = 4;
- same temporal reduction = 5;
- same 500 epochs;
- same batch size = 50;
- therefore the same number of trajectory-batch optimizer updates as the official FNO/U-Net recipe.

The per-update loss geometry necessarily differs by architecture and is reported explicitly rather than treated as identical compute.
