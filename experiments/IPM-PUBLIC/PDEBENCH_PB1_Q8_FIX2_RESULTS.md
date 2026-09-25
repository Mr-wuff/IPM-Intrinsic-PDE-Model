# IPM-PDEBench-PB1-Q8-FIX2 Results — Conservative Native-Flow Qualification

## Integrity

Result ZIP SHA256:

`755295046e76ce473bb544a8c3e19f0aaca4b93acd021fd52eb26b81d6465594`

Detached manifest: **10/10 payload entries match** by byte size and SHA256.

Protocol SHA256:

`29be51cb498648070e67bb967395eb3ed3435fdbf6e09645e789761f6ade2501`

Executed notebook SHA256:

`384db8acfe446cc1e719d6631db46989b84f59e232999bfe51b6ff32f6c82a32`

The executed notebook reports:
- Tesla T4
- N=256
- dx = 0.00390625
- raw saved-data dt = 0.00999999
- official test remains sealed.

No identification change and no official-test access occurred.

## Formal outcome

All FV1 and FV2 runs became non-finite.

Therefore the frozen C1-C7 gates all report FAIL and:

**PB1-Q8-FIX2 FORMAL FAIL**

Runtime transition is not authorized from this run.

However, the run also exposes a protocol-level numerical-stability defect in the candidate runtime specification, so this result is not valid evidence against conservative weak-form compilation itself.

## Legacy controls reproduce Q8-FIX1

Exact-law legacy IPMStep:
- one coarse step: **0.336870**
- five saved-time substeps: **0.272472**

Three frozen learned laws, legacy five-substep mean:
- **0.263593**

These agree with the prior attribution run.

## Conservative candidates

For the exact law and all three frozen learned laws:

- FV1 Rusanov, 1 substep: non-finite
- FV1 Rusanov, 5 substeps: non-finite
- FV2-MC Rusanov, 1 substep: non-finite
- FV2-MC Rusanov, 5 substeps: non-finite

Because even the first-order monotone Rusanov control diverges, the shared failure points to the explicit time-step contract rather than specifically to MUSCL reconstruction.

## Root cause: frozen FV time step violates CFL stability

The run records:

- `dx = 1/256 = 0.00390625`
- saved-data `dt_raw ≈ 0.01`
- one official interval = `5*dt_raw ≈ 0.05`

The preregistered five-substep conservative candidate therefore used:

`dt_FV ≈ 0.01`.

For a Burgers-type flux, the transport wave speed is:

`a = |F'(u)| ≈ |u| = O(1)`.

The resulting nominal Courant number is therefore already approximately:

`dt_FV/dx ≈ 2.56`

before multiplying by the actual maximum wave amplitude.

This is far outside the explicit Rusanov/MUSCL CFL regime.

The pinned PDEBench Burgers generator itself uses adaptive time stepping with:

`CFL = 0.25`

for the multi-solution Burgers datasets.

Thus Q8-FIX2 fixed the number of substeps to a value that is incompatible with the numerical stability contract of the newly introduced explicit conservative executor.

## Scientific status

The correct interpretation is:

- the low-viscosity runtime bottleneck remains established by Q8-FIX1;
- Q8-FIX2 does **not** falsify conservative flux compilation;
- Q8-FIX2 does falsify the preregistered fixed-five-substep FV execution contract;
- the next repair must make the conservative runtime CFL-aware without changing the identified law or the frozen performance gates.

No official test trajectory may be opened.

## Next repair

Use the same:
- exact conservation-form compiler;
- Rusanov flux;
- FV1 diagnostic;
- FV2-MC formal candidate;
- frozen exact law;
- three frozen DIC-DCC35 laws;
- frozen C1-C7 accuracy/conservation thresholds.

Replace only the invalid fixed substep count with deterministic adaptive subcycling:

`dt <= CFL * dx / max(|F'(u)|)`

using the **PDEBench generator's pinned CFL=0.25**.

The adaptive policy is a numerical stability requirement, not a searched hyperparameter.
