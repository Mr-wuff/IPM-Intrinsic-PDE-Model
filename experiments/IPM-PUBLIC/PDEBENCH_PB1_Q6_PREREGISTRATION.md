# IPM-PDEBench-PB1-Q6 — Burgers Causal Bottleneck Audit

## Motivation

PB1-Q5 is formally complete but has a mixed scientific outcome.

Advection closes strongly under the selected native-time S111 contract:
- formal nRMSE `0.072775 ± 0.008730`;
- training loss about `2.2e-4`;
- training-block secant error about `0.00627`;
- learned transport coefficient is approximately the expected unit-amplitude law.

Burgers does not:
- formal nRMSE `0.457651 ± 0.006035`;
- training loss remains `0.392-0.413`;
- refined secant error remains `0.664-0.691`;
- 8-step training-block rollout is much better than the 31-step public behavior;
- frozen Q5 Burgers IDTC has about `1.71-1.75%` non-principal canonical L1 mass, versus about `0.003%` for Advection.

PB1-Q6 is therefore a **causal audit, not another long training run**.

It must determine whether the remaining Burgers failure is primarily caused by:
1. local jet/derivative estimation;
2. non-convex low-rank IDTC parameterization/optimization;
3. principal-normal-form projection;
4. short-horizon native-flow closure / runtime integration.

## Test-data policy

The official first 1,000 PDEBench test trajectories are **not loaded** in PB1-Q6.

All fitting, calibration, route selection, and qualification use only the official 9,000-trajectory training block.

PB1-Q5's official Burgers result is treated as an already-observed final result and is not used numerically inside Q6's fitting objectives.

## Frozen Q5 artifacts

PB1-Q6 embeds the six frozen Q5 IDTC states and compiled programs detached from:

`IPM_PDEBENCH_PB1_Q5_RESULTS.zip`

SHA256:

`71a7c3e42726c5727584f0d9f7ffcfdbae15fb00bece443fa376c38072aae1b3`

The embedded state artifact is hashed inside the Q6 protocol.

## Internal training-block audit split

After skipping the first 1,000 official test trajectories:

- direct-law fit: first 1,024 training trajectories;
- native-flow gain calibration: next 256;
- mechanism validation: next 512;
- confirmatory internal holdout: next 512.

No exact PDE RHS or known Burgers coefficients enter fitting or route selection.

## Counterfactuals

### A. Frozen Q5 IDTC

Measure on train-only validation:
- full IDTC characteristic error;
- compiled principal characteristic error;
- full-to-principal defect;
- canonical non-principal coefficient mass;
- 1/2/4/8/16/31-step rollout drift.

### B. Direct principal canonical fit

Fit the same 16-scalar RTDS principal normal form directly to central secants by normalized ridge regression.

This removes the non-convex low-rank IDTC factorization while preserving the same deployment algebra.

Derivative variants:
- current LocalTaylorJet radius 4 / degree 5;
- LocalTaylorJet radius 6 / degree 7;
- LocalTaylorJet radius 8 / degree 7;
- periodic spectral Taylor jet (diagnostic upper bound).

Each fitted program receives the same train-only four-gain native-flow refinement before rollout qualification.

### C. Direct full 35-term canonical algebra

Fit all 35 monomials of total degree <=3 in the four Taylor-jet coordinates.

Run for:
- current LocalTaylorJet R4/D5;
- spectral Taylor jet.

This is characteristic-only diagnostic evidence; generic RK4 stability is not a formal gate.

Its purpose is to determine whether non-principal differential algebra is required.

### D. Gradient-regime audit

Characteristic errors are stratified by the current local `|u_x|` regime to determine whether the failure concentrates near steep/shock-like regions.

## Frozen hypothesis gates

Let:
- `E_Q5P` = frozen Q5 principal characteristic error;
- `E_DP` = direct R4/D5 principal characteristic error;
- `E_SP` = direct spectral principal characteristic error;
- `E_F35` = direct R4/D5 full-35 characteristic error.

Hypotheses:

- `H_IDTC_FACTORIZATION` if `E_DP / E_Q5P <= 0.70`.
- `H_JET_ESTIMATOR` if `E_SP / E_DP <= 0.75` or the best wider local jet / R4D5 ratio <= `0.80`.
- `H_PRINCIPAL_ALGEBRA` if `E_F35 / E_DP <= 0.75`.
- `H_FLOW_RUNTIME` if the best direct principal characteristic error <= `0.30` but its refined 31-step internal rollout Rel-L2 remains >= `0.40`.

The audit may support more than one hypothesis.

## Transition

No new 500-epoch Advection/Burgers training is permitted in Q6.

The next architecture modification is chosen only after the above counterfactuals are evaluated.

Any method change motivated by PB1-Q5/Q6 must be confirmed on a **new PDE family or unseen physical parameter**, not presented as a fresh independent confirmation on the already-observed beta=1 / nu=0.01 official test set.
