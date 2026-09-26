# IPM-PDEBench-PB2-Q0-FIX3 Results — Temporal Generator-Validity Gated Integral Qualification

## Integrity

Result ZIP SHA256:

`2dfbc6fadf0e500451776c66553100b8ff0ebfb9a71927609b3ab87ca40a1d36`

Detached checksum matches exactly.

Internal result manifest: **23/23 payload entries match** by byte size and SHA256.

Protocol SHA256:

`fb52b1f2071ef4e56923d92dddd3cfe1805c8963ccfb7a8431647cb319ad915c`

Executed notebook SHA256:

`0795fcea6eeaf5b02135a40cb60efcd572a93379a34afd898d5a52d2f2f183a6`

Frozen source notebook SHA256:

`55a7a95e665316be7dca525ee172f6c378710b3f510f84d3c2dae4c32fddcd80`

Official test accessed: **false**.

## Material protocol deviation

The frozen run required candidate eligibility:

`median standardized coefficient cosine >= 0.995`

The executed notebook changed this condition to:

`relaxed_threshold = 0.99`

with the explicit comment:

`# Relax threshold to 0.99 to allow S4 P13 candidate`

This is a post-registration threshold relaxation.

Therefore the downstream selected-contract qualification result is formally invalid for architecture qualification.

Formal archival status:

**PB2-Q0-FIX3 PROTOCOL-DEVIATED / FORMAL INVALID; DIAGNOSTIC RESULTS RETAINED**

No architecture transition or official-test unlock is authorized.

## Frozen generator-validity gate

The data-only gate itself behaved as intended and selected:

`GENVALID = [2,3,4,5,6,7,8]`

Calibration-block diagnostics:
- center 2: signal fraction 1.000, curvature/signal 0.373
- center 3: 0.582, 0.244
- center 4: 0.415, 0.170
- center 5: 0.325, 0.128
- center 6: 0.264, 0.106
- center 7: 0.217, 0.109
- center 8: 0.179, 0.104

Thus the gate successfully rejects:
- center 1, which is high-signal but excessively curved;
- the long low-signal equilibrium tail.

V1 is validly supported.

## Crucial unselected S2 result

The most important diagnostic result is not the relaxed S4 selection.

### S2 + P13

Three-fold confirm integral residual:
- fold 0: **0.064065**
- fold 1: **0.063909**
- fold 2: **0.064035**
- mean: **~0.06400**

Validation mean is ~0.05744.

Thus the generator-validity gate plus short Simpson-2 integral balance achieves strong trajectory-integral closure.

However coefficient stability is insufficient:

`cosine median = 0.934316`

This fails the frozen 0.995 requirement by a large margin.

### S2 + DCC35

Confirm integral:
- 0.061309
- 0.061104
- 0.061286

Coefficient cosine median:

`0.850273`

Again, residual closure is good but the explicit coefficient vector is non-identifiable.

## S2 physical structure is partially identifiable

Reporting directly from the three S2-P13 coefficient vectors:

Diffusion constant D0:
- 1.05572
- 1.05327
- 1.07627

This component is remarkably stable and close to the reporting-only expected value 1.

But reaction coefficients are unstable:

R_u:
- 0.39436
- 0.08259
- 1.26842

R_u2:
- -0.14292
- +0.45110
- -2.16365

Thus the data identify diffusion much more strongly than the decomposition of the reaction polynomial.

This is the key scientific result of FIX3.

## S4 diagnostic

Because the frozen eligibility threshold was relaxed, S4-P13 was selected even though:

`cosine median = 0.993389 < 0.995`

S4 confirm integral mean:

`0.692570`

Selected / PB2-Q0 baseline:

`1.39682`

Physical coefficient-vector relative error mean:

`47.28`

Runtime:
- FULL1024 mean ~0.10839
- STRIDE4 mean ~0.10839

S4 is therefore neither a good law-closure nor a physically meaningful solution.

It should not be used as the basis for the next architecture decision.

## Updated interpretation

FIX3 shows that the temporal generator-validity gate itself is useful.

For the valid centers 2..8, short Simpson-2 integral equations can be fit very accurately (~0.064 Rel-RMS).

The remaining failure is **coefficient identifiability**, not equation residual.

Within a single Reaction-Diffusion parameter environment:
- diffusion is consistently identified;
- reaction-polynomial coefficients have strong fold-to-fold tradeoffs;
- multiple reaction polynomials generate nearly indistinguishable finite-time balances on the observed state manifold.

Therefore the next experiment should not relax stability thresholds or increase polynomial capacity.

The next causal question is whether **multiple physical parameter environments** provide the structural excitation required to separate reaction and diffusion terms.

A multi-environment support/identifiability audit is justified before introducing any new identification architecture.
