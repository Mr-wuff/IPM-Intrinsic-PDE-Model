# IPM-PDEBench-PB2-Q0-FIX1 — Reaction-Diffusion Strong-Branch Identifiability Audit

## Motivation

PB2-Q0 failed the frozen governing-law gates on a new PDE family while still achieving stable full-horizon rollout:

- DCC35 characteristic confirm mean ~0.452
- DCC35 integral confirm mean ~0.446
- coefficient cosine median ~0.998
- P13 native full-horizon Rel-L2 mean ~0.039
- official test remained sealed

Reporting-only physical coefficients were strongly incorrect even though rollout remained good.

Therefore PB2-Q0-FIX1 is an attribution experiment. It asks whether the failure is caused by:

1. an incompatible strong DIC observation contract;
2. insufficient temporal excitation / late-time sampling;
3. overcomplete DCC35 canonical redundancy on the Reaction-Diffusion state manifold;
4. native runtime mismatch.

No official test access and no architecture transition are allowed.

## Dataset

PDEBench 1D Reaction-Diffusion:
- Nu=0.5
- Rho=1.0
- `ReacDiff_Nu0.5_Rho1.0.hdf5`
- URL `https://darus.uni-stuttgart.de/api/access/datafile/133177`
- MD5 `69a429239778d529cd419ed5888ea835`

Official rows 0:1000 remain sealed.

All diagnostic rows are relative to the training portion after the official block.

Three diagnostic fit folds:
- 0:512
- 512:1024
- 1024:1536

Validation:
- 3072:3328

Confirm:
- 3584:3840

Runtime confirm:
- first 64 trajectories of confirm.

## Frozen jet

Local Taylor jet:
- radius 4
- degree 5
- order 3
- FULL1024 identification observation

## Time-center contracts

### C0 — CURRENT_SPARSE
`[10,20,30,40,50,60,70,80,90]`

This reproduces the PB2-Q0 temporal sampling contract.

### C1 — EARLY_ENRICHED
`[1,2,3,4,5,6,8,10,12,15,20,30]`

### C2 — UNIFORM_DENSE
all centers `1,3,5,...,99`

No center set is selected using the known PDE coefficients.

## Canonical spaces

### S0 — DCC35
Complete total-degree<=3 polynomial basis in `(u,a1,a2,a3)`.

### S1 — P13
Frozen principal RTDS subspace:
- reaction polynomial degree<=3;
- transport/diffusion/dispersion derivative-linear terms with u degree<=2.

Both use the same DIC objective:
- centered differential equation;
- Simpson-2 integral equation;
- each family normalized by its own target RMS;
- equal dimensionless weighting;
- normalized ridge alpha=1e-8.

## Diagnostics

For every center-set / canonical-space pair and each of three folds:

- validation characteristic Rel-RMS;
- validation integral Rel-RMS;
- confirm characteristic Rel-RMS;
- confirm integral Rel-RMS;
- normalized Gram condition number;
- standardized coefficient cosine stability.

No candidate is promoted in this attribution run.

## Reporting-only exact-generator audit

After the data-only diagnostic matrix is computed, evaluate the known continuum generator:

`u_t = u - u^2 + 0.5*u_xx`

or, in frozen Taylor coordinates:

`Q = u - u^2 + 1*a2`.

Evaluate:
- characteristic residual per saved-time center 1..99;
- Simpson-2 integral residual per center;
- residual summaries for C0/C1/C2;
- exact-law native rollout on internal confirm.

The known law is not used to fit any candidate.

## Attribution hypotheses

### H1 — strong DIC contract compatibility
Supported if exact-law C2 characteristic and integral residual means are both <=0.12.

If either exceeds 0.20:
route contribution = `STRONG_TEMPORAL_OR_JET_CONTRACT_MISMATCH`.

### H2 — temporal excitation limitation
Supported if:
- EARLY_ENRICHED or UNIFORM_DENSE reduces P13 confirm characteristic residual by >=30% relative to CURRENT_SPARSE;
and
- normalized Gram condition number improves by >=3x.

### H3 — DCC35 redundancy
Supported if, on the same best center set:
- P13 confirm characteristic residual / DCC35 confirm characteristic residual <=0.80;
or
- P13 condition number is >=10x lower while its confirm residual is no worse than 1.05x DCC35.

### H4 — native runtime compatibility
Reporting-only exact-law runtime full-horizon Rel-L2 <=0.03 and remains finite.

### H5 — effective-closure diagnosis
Supported if:
- current learned P13 runtime remains <=0.06,
- but its governing-law residual remains >=0.25,
- while exact-law runtime is materially better.

This identifies trajectory closure without correct law identification.

## Routing

Priority:

1. If H1 fails:
   `STRONG_TEMPORAL_OR_JET_CONTRACT_MISMATCH`

2. Else if H2 and H3:
   `EXCITATION_PLUS_CANONICAL_REDUNDANCY`

3. Else if H2:
   `TEMPORAL_EXCITATION_LIMITED`

4. Else if H3:
   `DCC35_REDUNDANCY_LIMITED`

5. Else:
   `STRONG_IDENTIFIABILITY_UNRESOLVED`

H4/H5 are supporting diagnostics and do not override the primary route.

No official-test access, architecture freeze, or 500-epoch training is authorized.
