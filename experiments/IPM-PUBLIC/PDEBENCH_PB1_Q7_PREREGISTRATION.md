# IPM-PDEBench-PB1-Q7 — Direct Canonical Integral Core Qualification

## Motivation

PB1-Q6 causally isolated the Burgers failure to the low-rank/non-convex IDTC factorization or optimization:

- frozen Q5 principal characteristic error: `0.700983`
- direct R4/D5 principal fit: `0.138474`
- `H_IDTC_FACTORIZATION = true`
- `H_JET_ESTIMATOR = false`
- `H_PRINCIPAL_ALGEBRA = false`
- `H_FLOW_RUNTIME = false`

The next architecture experiment replaces the 35-scalar low-rank IDTC with a **Direct Canonical Core (DCC-35)**.

DCC-35 uses the 35 monomials of total degree <= 3 in the four Taylor-jet coordinates directly as coefficients.

This retains the same scalar order as IDTC while:
- spanning the complete third-degree canonical polynomial space;
- eliminating low-rank quadratic/cubic tensor factorization;
- making trajectory integral identification linear in the unknown coefficients;
- permitting a deterministic normal-equation solve rather than long non-convex SGD.

## First-principles identification law

No exact PDE RHS or known PDE coefficients are used.

For a Simpson triplet `t-dt, t, t+dt`:

`u(t+dt)-u(t-dt) ≈ (dt/3)[Q(j(t-dt)) + 4 Q(j(t)) + Q(j(t+dt))]`

If `Q(j)=Phi(j)c`, then each trajectory triplet is linear in `c`.

DCC therefore identifies the local differential law directly from trajectory integrals.

## Data policy

PDEBench Burgers nu=0.01.

The official first 1,000 test trajectories are never loaded.

Three disjoint fit folds are used:
- fold A: first 1,024 training trajectories
- fold B: next 1,024
- fold C: next 1,024

Shared training-only blocks after the three folds:
- gain calibration: 256 trajectories
- validation: 512 trajectories
- confirmatory internal holdout: 512 trajectories

All route selection occurs before any future official or unseen-parameter evaluation.

## Jet

Frozen from Q6:

`LocalTaylorJet(radius=4, degree=5, order=3)`

No jet search is allowed in Q7.

## Candidates

1. **DCC-35** — all 35 canonical monomials of total degree <=3.
2. **DCC-P16** — principal RTDS 16-term ablation.
3. **Q6 direct-secant P16** — recomputed train-only reference, not a candidate architecture.

Both DCC candidates are trained from trajectory Simpson integral equations only.

## Solver

Column-normalized ridge normal equations.

Frozen ridge coefficient:

`alpha = 1e-8`

No gradient descent is used to identify canonical coefficients.

After identification, the same train-only four-gain native-flow refinement used in Q6 is applied only to the compiled RTDS program.

## Evaluation

On validation and internal confirmatory blocks:
- trajectory Simpson-integral residual;
- central-secant characteristic Rel-RMS (diagnostic only; not an identification target);
- canonical coefficient stability across three fit folds;
- DCC-35 non-principal coefficient mass;
- DCC-35 -> RTDS projection defect;
- raw and refined 1/2/4/8/16/31-step native rollout;
- gain stability;
- known Burgers coefficient comparison only as a post-hoc reporting diagnostic.

## Frozen gates

Let the three-fold means be computed on the internal confirmatory block.

### Q7-1 direct-canonical identification
DCC-35 characteristic Rel-RMS mean <= 0.20 and max fold <= 0.24.

### Q7-2 trajectory-integral closure
DCC-35 refined 31-step internal rollout Rel-L2 mean <= 0.22 and max fold <= 0.26.

### Q7-3 factorization repair
DCC-35 characteristic error / frozen Q5 principal characteristic error <= 0.35.

### Q7-4 full-space viability
DCC-35 characteristic error / DCC-P16 characteristic error <= 1.15.

This gate is important: the generic full 35-term core must remain competitive with the equation-family-specific principal ablation.

### Q7-5 coefficient stability
Across the three DCC-35 folds, the median pairwise cosine similarity of the normalized 35-coefficient vectors must be >= 0.95.

### Q7-6 no hidden need for expanded deployment algebra
After DCC-35 is projected to RTDS, its refined 31-step rollout may be at most 15% worse than directly fitted DCC-P16.

If Q7-1..Q7-6 all pass, the architecture transition is authorized:

`IDTC-35 low-rank nonlinear factorization -> DCC-35 direct canonical integral core`

No 500-epoch run is authorized by Q7 itself.

## Transition

If Q7 passes, the next confirmatory stage must use an unseen physical parameter or new PDE family before any claim of general improvement.

The already-observed Burgers nu=0.01 official test set must not be reused as a fresh confirmatory benchmark for the architecture change.
