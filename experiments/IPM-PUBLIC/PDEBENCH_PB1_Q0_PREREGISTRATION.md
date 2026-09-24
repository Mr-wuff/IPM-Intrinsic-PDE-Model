# IPM-PDEBench-PB1-Q0 — Official Pretrained Artifact Qualification

## Purpose

PB0 established that frozen IPM-v1 can be evaluated under the pinned official PDEBench contract.

PB1 will compare IPM against **official PDEBench pretrained baselines** rather than retraining the baselines ourselves.

PB1-Q0 is a zero-training artifact qualification stage. It downloads, verifies, inventories, and attempts strict checkpoint loading for the current official PDEBench pretrained Advection/Burgers artifacts.

No baseline is trained in this experiment.

## Official sources

PDEBench code:
- repository: `pdebench/PDEBench`
- pinned commit: `4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Official pretrained-model dataset:
- DaRUS persistent identifier: `doi:10.18419/DARUS-2987`
- current published version: V2
- V2 notes state that it contains weights trained using the latest Advection and Burgers data.

The notebook resolves file IDs, filenames, checksums, sizes, and direct download URLs from the official Dataverse API at runtime.

## Candidate artifacts

Discover the V2 package artifacts for:

Advection:
- FNO
- U-Net
- PINN

Burgers:
- FNO
- U-Net
- PINN

Expected naming families include:
- `advection_FNO-1.tar`
- `advection_Unet-1.tar`
- `advection_PINN-1.tar`
- `burgers_FNO-1.tar`
- corresponding Burgers U-Net/PINN packages if present in the official V2 release.

The API response, not hard-coded file IDs, is authoritative.

## Artifact qualification

For each selected package:

1. download from the official DaRUS Data Access API;
2. verify the checksum published in the Dataverse metadata;
3. list every archive member with size;
4. record SHA256 for the downloaded archive;
5. safely extract into a model-specific directory;
6. find checkpoint/model/config/result files;
7. inspect PyTorch checkpoint top-level keys when applicable;
8. reject path traversal / unsafe archive members.

No artifact content is modified.

## FNO / U-Net load qualification

Construct the official PDEBench model architecture from the pinned official code/config and attempt a strict state-dict restore from the discovered checkpoint.

A successful FNO/U-Net artifact must:
- load without missing/unexpected tensor keys after only documented checkpoint-wrapper extraction (e.g. `checkpoint["model_state_dict"]`);
- run a finite forward smoke test on the official N=256 / initial_step=10 input contract.

No state-dict key surgery is allowed.

## PINN qualification

PINN artifacts may use the DeepXDE checkpoint structure rather than the FNO/U-Net PyTorch checkpoint structure.

Q0 inventories the exact PINN archive content and attempts the official pinned PDEBench/DeepXDE restoration path.

If the current environment cannot restore an official PINN artifact because of legacy framework-version serialization, the artifact remains official/valid; the result is recorded as an environment-compatibility limitation and PB1 may use the published official PINN metric table as the primary PINN reference.

No retraining is permitted.

## IPM v1.0.1 runtime-compatibility audit

PB0 encountered an environment-specific CUDA NVRTC soname problem in `torch.exp(complex)`.

The repository runtime is now patched mathematically equivalently:

[
e^{-Delta t
u k^2-iDelta tgamma k^3}
=
e^{-Delta t
u k^2}
left[
cos(Delta tgamma k^3)-isin(Delta tgamma k^3)
ight].
]

Frozen program coefficients and architecture are unchanged.

Q0 must verify:
- `ipm_v1.__version__ == 1.0.1`;
- no NVRTC soname alias/symlink workaround is used;
- a Burgers finite forward smoke test succeeds on CUDA;
- where cached official PDEBench data is available, seed-202 PB0 RMSE/nRMSE reproduction is reported; this reproduction is diagnostic rather than required to download the pretrained artifacts.

## Package-manifest repair

The result manifest must exclude its own file from the internal hash table, avoiding PB0's self-referential manifest mismatch.

## Gates

PB1Q0-0 pinned PDEBench and IPM source provenance verified.

PB1Q0-1 official DaRUS V2 metadata resolves the candidate Advection/Burgers pretrained packages.

PB1Q0-2 all downloaded candidate archives match their official published checksums.

PB1Q0-3 all archives pass safe inventory/extraction and produce a complete file inventory.

PB1Q0-4 official FNO artifacts for both tasks strictly restore and produce finite smoke outputs.

PB1Q0-5 official U-Net artifacts for both tasks strictly restore and produce finite smoke outputs.

PB1Q0-6 PINN artifact status is fully resolved: either successful official restoration/finite smoke or an explicit reproducible legacy-environment compatibility report with archive integrity proven.

PB1Q0-7 IPM v1.0.1 Burgers CUDA smoke succeeds without any NVRTC library alias.

PB1Q0-8 result ZIP SHA and detached internal manifest audit pass, with no self-hash entry.

Decision:
- **PDEBENCH_PB1_Q0_PASS** if PB1Q0-0..PB1Q0-8 pass.
- **PDEBENCH_PB1_Q0_CONDITIONAL** if only PB1Q0-6 is an official PINN legacy-environment incompatibility while all artifact-integrity and FNO/U-Net gates pass.
- **PDEBENCH_PB1_Q0_FAIL** otherwise.

## Transition

If Q0 passes/conditional, PB1-FULL evaluates:
- frozen IPM-v1.0.1;
- official pretrained FNO;
- official pretrained U-Net;
- official pretrained PINN when executable;

through the same pinned official PDEBench test data and `metric_func`.

No baseline retraining is performed.
