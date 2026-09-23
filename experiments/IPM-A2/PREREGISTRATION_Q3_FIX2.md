# IPM-A2-Q3-FIX2 — Principal Normal-Form Calibration Compiler

## Motivation

Q3-FIX1 solved the catastrophic long-horizon instability:

- Advection Q3 mean 40-step Rel-L2: ~4.21e14 -> FIX1 0.19574
- Burgers: 0.47204 -> 0.19093

It also passed noise and resolution gates.

Two bottlenecks remain:

1. Advection misses the <=0.12 reliability floor. Its frozen principal transport coefficient is approximately -0.90 instead of the beta=1 reference magnitude, producing smooth phase-speed error accumulation.
2. Burgers compiler latency is 3.434 ms, effectively equal to the official FNO 3.433 ms. Selected FIX1 programs still retain 7-14 nuisance derivative monomials, forcing Local Taylor Jet construction and mixed-derivative evaluation at deployment.

FIX2 tests whether the frozen 35-parameter IDTC can be compiled into a **nuisance-free principal normal form** with only a few training-side calibrated role amplitudes.

No neural network is retrained. No true PDE term or coefficient is supplied.

## Frozen parents

Required:
- Q0 result ZIP SHA256:
  `6671e747ceda73ce8b27208bf8a367c8f4aec1db1cab4c2a4f54f8081ea1fbf0`
- Q2 result ZIP SHA256:
  `23f7af45c0318992b6ae2fd6570a06a04ddd06c258463aaff9e9e3d9f0020b77`
- Q3-FIX1 result ZIP SHA256:
  `fbf93087ce7546f972d72d759b998fecafba48cab5c82a9bcb748cae51aef273`

Q0 is used only to reconstruct and re-time the official NeuralOperator FNO on the current hardware.

Q2 provides the frozen IDTC checkpoints.

Q3-FIX1 is used only for parent integrity/comparison.

## Canonical principal normal form

Expand the frozen IDTC exactly and retain only generic principal families:

[
Q_P =
lambda_R R(u)
+
lambda_1 f_1(u)a_1
+
lambda_2 f_2(u)a_2
+
lambda_3 f_3(u)a_3,
]
where
[
a_1=u_x,quad a_2=u_{xx}/2,quad a_3=u_{xxx}/6.
]

All mixed derivative nuisance monomials are excluded from the deployment program.

This removes the need for Local Taylor Jet construction during deployment.

## New disjoint calibration split

Development chronology must remain explicit.

Q2 model fitting used PDEBench training-pool samples 0..127.

Q3 / Q3-FIX1 used training-pool samples 128..159 for compiler selection.

FIX2 uses a new disjoint calibration block:
- gain-fit: training-pool samples 160..191
- role-validation: training-pool samples 192..223

The official first-10% PDEBench test split remains untouched during selection.

## Role-gain fitting

Generic roles:
- R: reaction/source
- T: first-derivative transport
- D: second-derivative diffusion
- S: third-derivative dispersion

For a candidate role mask, compute role fields from the frozen canonical IDTC on clean gain-fit trajectories and target the central-secant generator proxy:
[
q_{sec}(t)=rac{u(t+Delta t)-u(t-Delta t)}{2Delta t}.
]

Fit only scalar gains by normalized ridge regression:
[
min_lambda |Xlambda-q_{sec}|_2^2+alpha|lambda|_2^2,
]
with fixed normalized ridge (alpha=10^{-6}).

No canonical coefficient inside a role is individually refit.

## Role-mask selection

Enumerate all non-empty subsets of available R/T/D/S roles.

For each mask:
1. fit gains only on gain-fit trajectories;
2. compile a nuisance-free native flow;
3. evaluate 20-step rollout on role-validation trajectories at starts 10/60/120;
4. reject non-finite candidates;
5. choose lowest validation error;
6. if candidates are within 5%, choose the fewer-role program.

No official test trajectory is used for selection.

## Nuisance-free deployment compiler

### Reaction
Local Heun half-step using calibrated (lambda_R R(u)).

### Transport
Semi-Lagrangian periodic transport using
[
v=-lambda_1 f_1(u).
]

### Diffusion
[

u=operatorname{median}_xleft(lambda_2 f_2(u)/2ight).
]

### Dispersion
[
gamma=operatorname{median}_xleft(lambda_3 f_3(u)/6ight).
]

Diffusion and dispersion use one fused periodic spectral exponential step:
[
hat u_kleftarrow
exp[(-
u k^2+gamma(ik)^3)Delta t]hat u_k.
]

There is **no Local Taylor Jet and no nuisance correction at deployment**.

## Formal evaluation

PDEBench:
- Advection beta=1.0
- Burgers nu=0.01

Seeds:
101, 202, 303.

Report:
- selected role mask
- fitted role gains
- gain reproducibility
- 1/5/10/20/40-step rollout
- 1% noise
- resolution /2 and /4
- batch-1 and batch-16 physical-step latency
- grid-points/s
- checkpoint/program size
- current-hardware official FNO latency
- Q3-FIX1 vs FIX2 accuracy/speed delta

## Gates

G0 parent SHA + official PDEBench MD5 integrity.

G1 calibration split is disjoint from Q2 fit, Q3/FIX1 calibration and official test.

G2 all selected programs finite for 40 steps in 3/3 seeds.

G3 mean 40-step Rel-L2:
- Advection <=0.12
- Burgers <=0.25.

G4 current-hardware end-to-end physical-step latency <=0.50x official FNO on both PDEs at batch 16.

G5 batch-1 physical-step latency <=0.75x official FNO on both PDEs.

G6 1% noise degradation <=1.15x native.

G7 resolution /2 <=1.20x and /4 <=1.50x native.

G8 role mask reproducible in at least 2/3 seeds per PDE.

G9 effective calibrated program uses <=39 scalar values:
- 35 frozen IDTC trainable values
- <=4 fitted role gains.

Decision:
- A2_Q3_FIX2_PASS: G0-G4 mandatory + at least 4 of G5-G9.
- A2_Q3_FIX2_CONDITIONAL: finite + speed pass and either PDE accuracy misses by <=25%.
- A2_Q3_FIX2_FAIL otherwise.

## Scope

This remains a development qualification, not the final benchmark.

The comprehensive benchmark against classical PDE solvers, PINNs, neural operators, temporal surrogates, discovery methods and foundation PDE models begins only after one stable compact IPM deployment candidate is frozen.