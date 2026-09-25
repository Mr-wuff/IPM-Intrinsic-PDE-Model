# IPM-PDEBench-PB1-Q7-FIX1 — Differential-Integral Consistent Canonical Core Qualification

## Motivation

PB1-Q7 formally failed only Q7-1:
- DCC35 confirm characteristic mean `0.218421 > 0.20`
- the other five frozen gates passed.

Q7 also exposed a structural basis mismatch:
- DCC35 spans all monomials of total degree <=3 in the four Taylor-jet coordinates;
- the legacy P16 list contains three total-degree-4 terms: `u^3 a1`, `u^3 a2`, `u^3 a3`.

Q7-FIX1 removes that mismatch and directly targets the observed full-space identifiability gap.

## Architecture

The candidate remains **DCC-35**:
- 35 direct canonical coefficients;
- complete total-degree <=3 polynomial space;
- no low-rank tensor factorization;
- no neural optimizer.

The mathematically consistent principal ablation is now **P13**:
- reaction: `1,u,u^2,u^3` (4 terms);
- transport/diffusion/dispersion: `a_r, u a_r, u^2 a_r` for r=1,2,3 (9 terms);
- total = 13 terms.

Runtime coefficient slots for `u^3 a1`, `u^3 a2`, and `u^3 a3` are fixed to zero.

## Identification contract

No exact PDE RHS and no known PDE coefficient is used.

For each raw-time trajectory triplet, construct two equations from the same observed states.

### Integral equation

`Delta u ≈ (dt/3)[Q_- + 4 Q_0 + Q_+]`

### Differential equation

`(u_+ - u_-)/(2dt) ≈ Q_0`

With `Q = Phi c`, both are linear in the same canonical coefficient vector `c`.

The two equation families are normalized by their own target RMS and stacked with equal dimensionless weight:

`L_DIC = L_integral_normalized + L_differential_normalized`

No tunable mixture weight is searched.

## Data

Official PDEBench Burgers nu=0.01.

The first 1,000 official test trajectories are never loaded.

Use the same three disjoint Q7 fit folds:
- A: training trajectories 0:1024
- B: 1024:2048
- C: 2048:3072

Training-only blocks:
- gain calibration: 3072:3328
- validation: 3328:3840
- confirm: 3840:4352

Jet is frozen:
`LocalTaylorJet(radius=4, degree=5, order=3)`

## Candidates

1. **DIC-DCC35** — 35-term full canonical core with joint differential-integral solve.
2. **DIC-P13** — exact principal subspace ablation with the same joint solve.
3. **INT-DCC35** — Q7 integral-only full-space control, recomputed.
4. **SEC-DCC35** — secant-only full-space diagnostic reference.

All solves use column-normalized ridge normal equations with alpha=`1e-8`.

## Evaluation

On validation and untouched internal confirm blocks:
- Simpson integral Rel-RMS;
- central characteristic Rel-RMS;
- coefficient cosine stability across fit folds;
- DCC35 non-principal coefficient mass;
- DCC35 -> P13 projection defect;
- normalized normal-system condition number;
- raw/refined native rollout at 1/2/4/8/16/31 steps;
- final four-gain stability.

Known Burgers coefficients remain reporting-only.

## Frozen gates

### F1 — characteristic closure
DIC-DCC35 confirm characteristic:
- mean <= 0.20
- max fold <= 0.22

### F2 — integral preservation
DIC-DCC35 confirm integral Rel-RMS:
- mean <= 0.11
- max fold <= 0.13

### F3 — long-horizon closure
Projected/refined DIC-DCC35 confirm 31-step rollout:
- mean <= 0.22
- max fold <= 0.25

### F4 — objective repair
DIC-DCC35 characteristic mean / INT-DCC35 characteristic mean <= 0.95.

### F5 — generic-space viability
DIC-DCC35 characteristic mean / DIC-P13 characteristic mean <= 1.15.

### F6 — coefficient stability
Median pairwise cosine of the three DIC-DCC35 coefficient vectors >= 0.95.

### F7 — projection viability
Projected/refined DIC-DCC35 31-step rollout mean / DIC-P13 31-step rollout mean <= 1.15.

### F8 — basis consistency
No total-degree-4 term may appear in DCC35 or P13 fitting. Runtime slots corresponding to `u^3 a1`, `u^3 a2`, `u^3 a3` must be exactly zero.

## Decision

If F1-F8 all pass:

**DCC-35 with differential-integral consistent identification is architecture-qualified.**

This authorizes the architecture transition:

`IDTC-35 -> DIC-DCC35`

It does **not** authorize reusing the already-observed Burgers nu=0.01 official test set as fresh confirmation.

The next confirmatory benchmark must use an unseen physical parameter or a new PDE family.

No 500-epoch training is authorized in Q7-FIX1.
