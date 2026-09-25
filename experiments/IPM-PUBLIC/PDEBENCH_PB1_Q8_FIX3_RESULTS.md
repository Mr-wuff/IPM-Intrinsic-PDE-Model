# IPM-PDEBench-PB1-Q8-FIX3 Results — Weak Conservative Flux-Core Qualification

## Integrity

Result ZIP SHA256:

`fc4eae5329af69c322bbbcdaca3def0a5ac196b1eb9a6ac35f0e7cc5b8b63e64`

Detached checksum matches exactly.

Internal result manifest: **15/15 payload entries match** by byte size and SHA256.

Embedded protocol SHA256:

`f431c9a19e8306dbe334fa2a3a61904e2be52e88ec15e6c0cdd2ae427235310e`

Frozen notebook SHA256 recorded in GitHub:

`9dde5ebb1e7e45586fc641189f9151b4bf7d657496c371aa0703bf944a62d51f`

Executed notebook SHA256:

`5b5efbc0b50565cebd9769d295252ce657fcc9afc385c8852bba8f89aacc4fed`

The executed notebook contains 8 code cells and no runtime error output.

Official test accessed: **false**.

## Material execution deviation

The frozen Q8-FIX3 notebook required:

`if not CONSERVATION_ACTIVE: raise RuntimeError(...)`

because WCFC fitting was permitted only after the preregistered conservation detector passed.

The executed notebook changed this to:

`print("Conservation detector did not activate; bypassing constraint for now.")`

and commented out the RuntimeError.

The detector in fact failed.

Therefore the downstream WCFC fitting/runtime outputs are useful **diagnostics only** and do not constitute a valid preregistered WCFC qualification.

Formal archival status:

**PB1-Q8-FIX3 PROTOCOL-DEVIATED / FORMAL INVALID; DIAGNOSTIC RESULTS RETAINED**

No weak-conservative architecture transition is authorized.

## Frozen detector result

Normalized spatial-mean drift on the N=256 reduced observations:

- fit fold 0: **0.011910**
- fit fold 1: **0.010126**
- fit fold 2: **0.013138**
- validation: **0.007634**

Frozen W0 threshold:

`<= 0.001`

Thus W0 fails strongly.

## Diagnostic WCFC fit

Despite the bypass, the three five-scalar laws are highly stable:

median standardized coefficient cosine:

**0.999955**

Typical recovered coefficients:

- `f2 ≈ 0.507`
- `kappa ≈ 0.000310 to 0.000316`
- nuisance quartic flux term `f4 ≈ -0.026`

Reporting-only exact values for the pinned Burgers generator are:
- `f2 = 0.5`
- `kappa = epsilon/pi ≈ 0.00031831`
- `f4 = 0`

Thus the leading flux and diffusion amplitudes are close, but the weak fit introduces a systematic quartic compensation term.

Confirm weak joint residual:

**~0.21777**

versus the preregistered threshold `0.10`.

## Diagnostic runtime

On the new internal holdout with the frozen FV2-MC-CFL executor:

- exact law: **0.008892**
- frozen strong DIC laws mean: **0.081777**
- diagnostic WCFC laws mean: **0.124432**

WCFC / exact:

**13.99**

WCFC / frozen strong DIC:

**1.522**

WCFC therefore does not repair the learned/oracle gap in this execution.

WCFC is nevertheless strictly conservative at runtime:
- max normalized mean drift: **5.18e-5**
- all trajectories finite
- max Courant: **0.25**

## Root-cause audit of W0

The pinned PDEBench multi-solution Burgers generator is a periodic finite-volume scheme.

It:
- stores values at finite-volume cell centers;
- uses periodic ghost cells;
- advances each cell by a difference of interface fluxes;
- uses adaptive CFL=0.25.

Therefore the full N=1024 discrete solution is globally conservative up to numerical precision.

However, Q8-FIX3 applied the official benchmark spatial reduction as:

`tensor[..., ::4]`

before measuring mean conservation and constructing weak spatial moments.

The official PDEBench forward-loader itself performs spatial reduction by the same stride/decimation operation, not by conservative block averaging.

A stride-4 decimation of moving shock cell averages is not itself a conservative coarse-grid restriction. The mean of one out of every four moving cell values can drift even when the mean over all 1024 fine cells is conserved exactly.

Thus W0 may primarily be measuring the **observation/restriction operator**, rather than the conservation property of the underlying PDE trajectory.

The systematic quartic WCFC term is also consistent with a weak-law fit compensating for aliasing introduced by non-conservative decimation.

## Next experiment

Before changing WCFC algebra or abandoning weak identification, isolate the observation operator.

Compare on the same train-only rows:

1. **FULL1024** — native finite-volume cell averages.
2. **STRIDE4-256** — official benchmark decimation.
3. **AVG4-256** — conservative restriction obtained by averaging each four adjacent fine cells.

For each representation:
- conservation drift;
- identical WCFC-5 weak fit;
- weak residual;
- coefficient stability;
- learned coefficients;
- FV2-MC-CFL rollout after compiling the same weak law.

No architecture transition or official-test unlock is permitted in this attribution run.
