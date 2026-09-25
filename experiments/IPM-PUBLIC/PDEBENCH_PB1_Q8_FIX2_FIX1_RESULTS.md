# IPM-PDEBench-PB1-Q8-FIX2-FIX1 Results — CFL-Aware Conservative Native-Flow Qualification

## Integrity

Result ZIP SHA256:

`9ab5d847dfcf77178d5fa36c5347adf03e630f4fa7bc29697329dc70b69e0088`

Detached manifest: **12/12 payload entries match** by byte size and SHA256.

Protocol SHA256:

`26d4766873a8a87a74e31c263ca4e09e45d106cd38323e033f5a08bfed3ce724`

Executed notebook SHA256:

`036144509d1c149ce0fb146f3be4790e44bd3924f7b6544ac668bd5cbc7a0fb3`

No notebook error output was present. Official test access remained **false**.

## Formal outcome

Frozen gates:

- C0 CFL contract: **PASS**
- C1 exact-law conservative closure: **PASS**
- C2 conservative improvement: **PASS**
- C3 learned-law runtime closure: **PASS**
- C4 runtime/law separation: **FAIL**
- C5 learned improvement over legacy: **PASS**
- C6 exact-law conservation: **PASS**
- C7 finite execution: **PASS**

Formal status:

**PB1-Q8-FIX2-FIX1 FAIL — 7/8 GATES PASS**

The C4 threshold is not relaxed post hoc, so the runtime transition is not yet formally authorized.

## Exact-law result

Legacy semi-Lagrangian, five saved-time substeps:

`Rel-L2 = 0.272472`

CFL-aware FV1 Rusanov:

`0.034645`

CFL-aware FV2-MC Rusanov:

`0.00963831`

Thus FV2-MC-CFL reduces the exact-law error by **96.46%** relative to the frozen legacy-five-substep executor.

Ratio:

`0.00963831 / 0.272472 = 0.03537`.

This is strong evidence that the low-viscosity execution failure identified in Q8/Q8-FIX1 was primarily a numerical-semantics problem of the semi-Lagrangian transport executor.

## CFL contract

For FV2-MC-CFL:
- maximum observed Courant: **0.25**
- maximum substeps in any official interval: **117**
- all expected interval records complete
- all runs finite

Mean adaptive substeps per official interval:
- exact law: **93.35**
- learned fold 0: **92.13**
- learned fold 1: **97.90**
- learned fold 2: **105.52**

The previous Q8-FIX2 non-finite failure is therefore confirmed to have been a fixed-step CFL violation.

## Conservation

Exact-law FV2-MC-CFL maximum relative periodic-domain mean drift:

`6.75e-5`

which passes the frozen `1e-4` gate.

## Learned-law result

Frozen strong-form DIC-DCC35 -> P13 laws:

### Legacy-five-substep
- fold 0: 0.268792
- fold 1: 0.262492
- fold 2: 0.259496
- mean: **0.263593**

### FV2-MC-CFL
- fold 0: 0.104348
- fold 1: 0.095697
- fold 2: 0.065106
- mean: **0.088384**
- max: **0.104348**

Thus the conservative runtime improves the same frozen learned laws by **66.47%** on average.

The learned programs comfortably pass the absolute C3 closure gate.

## Why C4 fails

C4 requires:

`learned_FV2_mean / exact_FV2 <= 1.20`

Observed:

`0.088384 / 0.009638 = 9.17`.

The failure occurs because the exact-law conservative executor is now extremely accurate, exposing remaining law contamination that the legacy executor previously masked.

The frozen learned P13 programs contain nonzero source/reaction polynomials of order `1e-2`.

Their FV2-CFL periodic-domain mean drift is:
- fold 0: **0.04669**
- fold 1: **0.10278**
- fold 2: **0.12152**

whereas the exact law is only `6.75e-5`.

This is direct evidence that the remaining learned/oracle gap is dominated by residual non-conservative structure in the strong-form DCC->P13 projection, not by the newly repaired conservative executor.

## Latency

Batch 64, Tesla T4, 31 official steps:

- legacy SL5 median: **~300 ms**
- FV1-CFL median: **~10.4 s**
- FV2-MC-CFL median: **~13.15 s**

The conservative reference executor is therefore not yet performance-competitive. These timings are diagnostic only.

The high cost is explained by approximately 2,900 conservative CFL substeps over the 31-step horizon.

Kernel fusion / compiled adaptive stepping is a later optimization problem and must not be attempted before the physical law/runtime contract is frozen.

## Scientific conclusion

The conservative weak-flow runtime is strongly supported:

- exact PDE law -> almost benchmark-level trajectory reproduction;
- strong conservation;
- deterministic CFL stability;
- large improvement for every frozen learned law.

The only formal failure is now **law/runtime separation**: a high-quality conservative executor makes the residual strong-form law pollution visible.

The next experiment must therefore modify the **identification representation for a detected conservation-law regime**, not the conservative FV runtime.

A trajectory-only weak formulation can avoid shock-singular pointwise derivatives completely.

For a scalar conservation-diffusion law,

`u_t + dF(u)/dx = kappa*u_xx`,

periodic weak moments satisfy:

`<phi,u_t> = <phi_x,F(u)> + kappa<phi_xx,u>`.

This uses only observed field values and known test functions; no spatial derivative of the observed shock profile is required.

The next stage should fit the flux and diffusion coefficients directly from these weak differential/integral equations, then execute them with the now-validated FV2-MC-CFL backend.
