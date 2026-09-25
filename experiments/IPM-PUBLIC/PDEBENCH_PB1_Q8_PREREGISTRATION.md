# IPM-PDEBench-PB1-Q8 — Unseen-Viscosity Independent Confirmation

## Purpose

PB1-Q7-FIX1 formally qualified the architecture transition:

`IDTC-35 -> DIC-DCC35`

That qualification used only the Burgers nu=0.01 official training block. The nu=0.01 official test set has already been observed historically and is therefore not eligible as fresh confirmation.

PB1-Q8 is the first **independent confirmatory benchmark** for the new architecture.

It uses two Burgers viscosities that were not used in Q2-Q7 architecture selection:

- `nu = 0.001` — lower-viscosity / sharper regime
- `nu = 0.1` — higher-viscosity / smoother regime

These bracket the development parameter `nu=0.01` by one decade on each side.

## Frozen official assets

Pinned PDEBench commit:

`4ff3e3a4aa1561721b5571fa3a048a0a463e0568`

Official pinned download list:

### nu=0.001
- file: `1D_Burgers_Sols_Nu0.001.hdf5`
- URL: `https://darus.uni-stuttgart.de/api/access/datafile/268190`
- MD5: `44cb784d5a07aa2b1c864cabdcf625f9`

### nu=0.1
- file: `1D_Burgers_Sols_Nu0.1.hdf5`
- URL: `https://darus.uni-stuttgart.de/api/access/datafile/268185`
- MD5: `660ba1008d3843bf4e28d2895eb607ce`

Official Burgers model contract:
- spatial reduction: 4
- temporal reduction: 5
- initial step: 10

## Architecture freeze

No architecture component may be changed in Q8.

Identification:
- LocalTaylorJet radius=4, degree=5, order=3
- complete total-degree<=3 DCC-35 canonical basis
- differential-integral consistency with equal dimensionless integral/differential weights
- ridge alpha=1e-8
- no SGD for law identification

Compilation:
- exact P13 principal projection
- runtime `u^3 a1/u^3 a2/u^3 a3` slots fixed to zero
- same four-gain native-flow refinement as Q7-FIX1

No known Burgers coefficient enters fitting, projection, gain refinement, route selection, or gates.

## Split policy per unseen viscosity

The first 1,000 trajectories are sealed as the official test block and may not be loaded until all internal gates pass and all three fold programs are frozen.

Training block:
- fit fold A: 0:1024 after the test block
- fit fold B: 1024:2048
- fit fold C: 2048:3072
- gain calibration: 3072:3328
- validation: 3328:3840
- confirmatory internal holdout: 3840:4352

Thus each viscosity produces three independently identified DIC-DCC35 laws.

## Internal qualification gates

These gates are evaluated before any official test trajectory is loaded.

For **each unseen viscosity**:

### I1 — characteristic confirmation
DIC-DCC35 internal confirm characteristic:
- three-fold mean <= 0.22
- max fold <= 0.25

### I2 — integral confirmation
DIC-DCC35 internal confirm Simpson-integral residual:
- three-fold mean <= 0.14
- max fold <= 0.16

### I3 — long-horizon internal closure
Projected/refined 31-step internal confirm Rel-L2:
- mean <= 0.25
- max fold <= 0.28

### I4 — objective replication
DIC-DCC35 characteristic mean / integral-only DCC35 characteristic mean <= 0.95.

### I5 — coefficient stability
Median pairwise DIC-DCC35 coefficient cosine >= 0.95.

### I6 — basis consistency
All P13 runtime quartic derivative slots are exactly zero.

Only if I1-I6 pass for **both** viscosities may the official test blocks be opened.

## Independent official-test confirmation

After all six programs are frozen, load the first 1,000 official trajectories for both unseen viscosities exactly once.

Evaluate:
- pinned official PDEBench `metric_func`
- full 31-step future-horizon Rel-L2
- per-fold and three-fold mean/std
- all outputs finite

For **each viscosity**:

### E1 — finite official horizon
All 31 future steps finite for all three folds.

### E2 — official full-horizon relative error
Official-test 31-step Rel-L2:
- three-fold mean <= 0.30
- max fold <= 0.35

### E3 — official PDEBench nRMSE
- three-fold mean <= 0.35
- max fold <= 0.40

No threshold may be changed after observing either official test block.

## Reporting-only physics audit

After all gates are frozen, report:
- learned `u*a1` coefficient versus -1
- learned `a2` coefficient versus `2*nu` in Taylor coordinates

These known coefficients are never used for fitting or qualification.

## Decision

**PB1-Q8 PASS** only if:
- I1-I6 pass for both unseen viscosities; and
- E1-E3 pass for both unseen viscosities.

If Q8 passes, DIC-DCC35 is independently confirmed across a 100x Burgers viscosity span from `0.001` to `0.1`, with `0.01` used only during architecture development.

The next stage is a new PDE family (Reaction-Diffusion), not further Burgers tuning.

No 500-epoch training is authorized in Q8.
