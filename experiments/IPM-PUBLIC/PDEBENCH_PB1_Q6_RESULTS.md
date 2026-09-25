# IPM-PDEBench-PB1-Q6 Results — Burgers Causal Bottleneck Audit

## Integrity

Result ZIP SHA256:

`9c7d02d68273ec74b945f1dd5a61f517824f8d13c4eb0b0ba2c6902c47efde07`

Detached manifest: **18/18 payload entries match** by byte size and SHA256.

Protocol SHA256:

`cadbf36032905413e566fe83e4fe182c1655ff815fc4c61195e16251a4c10ab3`

Executed notebook code cells are byte-for-byte identical to the frozen Q6 notebook.

The official first 1,000 PDEBench test trajectories were not loaded.

## Frozen causal gate

- Q5 principal characteristic error: **0.700983**
- direct R4/D5 principal: **0.138474**
- direct R6/D7 principal: **0.141328**
- direct R8/D7 principal: **0.165166**
- spectral principal: **0.180801**
- direct R4/D5 full-35: **0.146736**

Frozen hypotheses:

- `H_IDTC_FACTORIZATION = true`
- `H_JET_ESTIMATOR = false`
- `H_PRINCIPAL_ALGEBRA = false`
- `H_FLOW_RUNTIME = false`

Primary route:

`IDTC_FACTORIZATION_OR_OPTIMIZATION`

No new 500-epoch run was authorized.

## Main causal result

Replacing the frozen Q5 low-rank nonlinear IDTC parameterization with a direct 16-coefficient principal canonical fit, while retaining the same local Taylor jet and the same RTDS deployment algebra, reduces confirm characteristic error from:

`0.700983 -> 0.138474`

an **80.25% reduction**.

This is the cleanest causal evidence so far that the Burgers failure is dominated by the IDTC factorization/optimization path rather than by the jet estimator, principal normal form, or native runtime.

## Jet estimator counterfactual

Relative to R4/D5 direct principal:
- R6/D7 ratio: **1.021**
- R8/D7 ratio: **1.193**
- spectral ratio: **1.306**

Thus neither a wider local Taylor stencil nor periodic spectral derivatives improve characteristic identification.

The current R4/D5 local jet is retained for the next mechanism stage.

## Principal algebra counterfactual

Direct full-35 canonical algebra gives confirm characteristic error:

`0.146736`

versus:

`0.138474`

for the direct principal-16 algebra.

Ratio:

`1.060`

Therefore the additional non-principal canonical terms are not required to explain the Q5 Burgers failure.

The Q5 non-principal terms are interpreted as compensation produced by the low-rank/non-convex identification path rather than evidence that deployment must expand beyond RTDS.

## Gradient-regime audit

Direct R4 principal characteristic error remains controlled across all gradient regimes:
- lower 50% |u_x|: **0.3076**
- 50-90%: **0.1756**
- 90-99%: **0.1412**
- top 1%: **0.1298**

The direct fit does not deteriorate in the steepest-gradient regime.

This further weakens the hypothesis that the local jet estimator is the dominant Burgers bottleneck.

## Internal rollout

After the same train-only native-flow four-gain closure, 31-step confirm Rel-L2:

- direct R8/D7: **0.176041**
- direct R4/D5: **0.186719**
- direct R6/D7: **0.188173**
- direct spectral: **0.194439**
- frozen Q5 seed 202: **0.238224**

The formal primary route remains based on characteristic identification, where R4/D5 is best. The small R8 rollout advantage is not sufficient to overturn the frozen jet-estimator gate.

## Learned differential law

For direct R4/D5 principal identification:
- transport coefficient for `u * a1`: about **-1.0236**
- after native-flow gain closure: about **-1.0737**

This recovers the correct order and sign of Burgers nonlinear transport from trajectories without using exact PDE RHS or known PDE coefficients in fitting.

The diffusion amplitude remains more attenuated than the ideal reporting-only law, so the next stage must test whether a direct canonical *integral* identification core can recover the full law without the low-rank IDTC optimization path.

## Scientific conclusion

PB1-Q6 isolates the current Burgers bottleneck to the **IDTC low-rank/non-convex parameterization or its optimization**, not to:
- the R4/D5 local jet,
- the RTDS principal normal form,
- or the native compiled runtime.

The next architecture experiment should therefore replace the low-rank nonlinear IDTC factorization with a direct canonical differential core whose coefficients enter the trajectory integral equations linearly.

This preserves the IPM first-principles structure while turning local law identification into a convex/linear problem.

Archival status:

**PB1-Q6 PASS — CAUSAL BOTTLENECK ISOLATED**
