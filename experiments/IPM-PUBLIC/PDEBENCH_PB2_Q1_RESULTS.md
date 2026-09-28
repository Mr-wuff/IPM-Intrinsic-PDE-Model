# IPM-PDEBench-PB2-Q1 Results — Held-Out Diffusion-Axis Independent Confirmation

## Integrity

Result ZIP SHA256:

`9f0a0efa16d76ad2886a2d2899db9ff5542dd856f6a3a8e2c2ec3e3a8a498cab`

Detached checksum matches exactly.

Internal manifest: **22/22 tracked payload entries match** by byte size and SHA256.

Protocol SHA256:

`3eb38ff9666e54caa1c5838dcc338aa1f3490e2ad4ba572df0e0816b8e4166a1`

Frozen source notebook SHA256:

`513e7eee7caf26257012e50764057c618c5f5f9dc9c31aa83d726cfc2ddf5e61`

Executed notebook SHA256:

`48eb68f11d2bf4555238898ecd24dc5158dd0194c3ed19bf04897b67a0bc61b4`

The executed notebook contains 8 code cells and no runtime errors.

A direct source comparison against the frozen notebook found one execution-layer change only: the download helper retries a complete download after an MD5 mismatch. No data split, model, support, gate, center rule, or scientific calculation was changed. This is treated as a protocol-preserving I/O repair.

Official test accessed: **false**.

## Formal outcome

No held-out environment passed the frozen environment screen.

Therefore:

- I1: **FAIL**
- I2: **FAIL**
- I3: **FAIL**
- I4: **FAIL**
- I5: **FAIL**

The latter gates are false because the preregistered logic evaluates them only after I1 provides at least two qualified environments.

Internal pass: **false**.

Official block unlock: **false**.

External gates E1-E3 were not evaluated and remain false placeholders.

PB2-Q1 PASS: **false**.

Reaction-Diffusion new-family identification is **not yet independently confirmed across the diffusion axis**.

## Data integrity / shape

All three held-out HDF5 files were MD5 verified and loaded as:

- Nu1/Rho2: (10000, 101, 1024)
- Nu1/Rho5: (10000, 101, 1024)
- Nu1/Rho10: (10000, 101, 1024)

Domain length reported by the packaged coordinate arrays: 1.0.

Saved-time spacing: approximately 0.01.

Thus the failure is not caused by an obvious grid-shape change in the packaged held-out data.

## Data-only valid pools and temporal budgets

### Nu1/Rho2
Valid pool: centers 2..22, 21 centers.

Frozen-support D-optimal B=8:
`[2,3,4,5,19,20,21,22]`

### Nu1/Rho5
Valid pool: centers 2..42, 41 centers.

Budget:
`[2,3,4,5,39,40,41,42]`

### Nu1/Rho10
Valid pool: centers 2..27, 26 centers.

Budget:
`[2,3,4,5,24,25,26,27]`

## Environment screen

Three-fold S2 screen residuals:

### Nu1/Rho2
- 0.736253
- 0.736420
- 0.735221

Mean: **0.735965**

### Nu1/Rho5
- 0.662238
- 0.662162
- 0.662273

Mean: **0.662224**

### Nu1/Rho10
- 0.489635
- 0.489575
- 0.489656

Mean: **0.489622**

All are far above the frozen qualification limits:
- mean <=0.12
- max fold <=0.15.

Therefore no environment qualifies.

## Diagnostic frozen-support coefficients

These coefficients are diagnostic only because the environments did not qualify.

Frozen support:
`[R_u,R_u2,D0]`

Expected reporting-only coefficients for Nu=1:
- R_u = rho
- R_u2 = -rho
- D0 = 2.

### Nu1/Rho2
Learned:
- R_u ≈ 4.94–5.99
- R_u2 ≈ -7.16 to -9.08
- D0 ≈ 0.640–0.660

The reaction decomposition is also badly distorted.

### Nu1/Rho5
Learned:
- R_u ≈ 5.36–5.40
- R_u2 ≈ -5.51 to -5.57
- D0 ≈ 0.672–0.705

Reaction coefficients are close to the expected 5/-5, while diffusion is strongly attenuated.

### Nu1/Rho10
Learned:
- R_u ≈ 10.36–10.41
- R_u2 ≈ -10.49 to -10.55
- D0 ≈ 0.672–0.705

Reaction coefficients are again close to the expected 10/-10, while diffusion remains strongly attenuated.

Fold coefficient cosine stability is extremely high:
- Nu1/Rho2 median ≈ 0.99975
- Nu1/Rho5 median ≈ 0.99999
- Nu1/Rho10 median ≈ 0.999998.

Thus the failure is not fold instability.

## Scientific interpretation

Q1 does **not** falsify the FIX6 support result.

Instead, the failure is strongly diffusion-axis specific:

1. the reaction terms transfer increasingly well as rho increases;
2. the fitted diffusion coefficient remains around 0.67–0.70 instead of the continuum Taylor-coordinate expectation 2;
3. S2 screen residual improves as reaction dominates diffusion, from ~0.736 at rho2 to ~0.490 at rho10, but never approaches qualification.

This pattern points to a mismatch between the stronger-diffusion saved-time trajectory and the current finite-time S2 observation contract.

The exact cause is not yet isolated.

Two confounds require a dedicated audit before modifying the support:
- Q1 changed the D-optimal budgeting matrix from the FIX6 full-P13 design to the frozen three-term support design;
- stronger diffusion may create a saved-time stiffness / high-frequency quadrature error that the 0.02-wide S2 window cannot represent accurately.

The next experiment should therefore keep official blocks sealed and compare:
- exact FIX6 full-P13 D-optimal budgeting versus the Q1 frozen-support D-optimal budget;
- all-valid-center fitting;
- S2 versus a one-save-step trapezoidal integral contract;
- spectral-band localization of the residual.

No support search is justified.
