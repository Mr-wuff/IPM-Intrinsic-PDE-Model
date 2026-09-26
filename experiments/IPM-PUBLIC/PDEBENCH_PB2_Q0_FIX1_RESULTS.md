# IPM-PDEBench-PB2-Q0-FIX1 Results — Reaction-Diffusion Strong-Branch Identifiability Audit

## Integrity

Result ZIP SHA256:

`ce22dad5d2824123b0989b1a5e274c6995c1df9f4c20e7d949eeed3821906902`

Detached checksum matches exactly.

Internal result manifest: **28/28 payload entries match** by byte size and SHA256.

Protocol SHA256:

`281a6b7905b61c48c95de4ca2f745329de85fba092cea2a809635a3a01c8dd58`

Executed notebook SHA256:

`1de00b9300ae92d2640353f8590e5947b6d9010770790745e3771383e183fc63`

Frozen notebook SHA256 recorded in the run record:

`2bd2fae2769765cf59416c8e05ccebf8c1b0b25062b344ec3e160c208662ab2e`

Embedded exact PB2-Q0 baseline-program SHA256:

`dda496e9d9e37546e8fdd801e3487a5e376cfdb54999890539810bba9c8c790d`

The executed notebook contains 7 code cells and no runtime errors. The embedded protocol hash matches the frozen run record.

Official test accessed: **false**.

## Frozen attribution report

The frozen report returned:

- H1 strong-DIC compatibility: false
- H1 mismatch: true
- H2 temporal-excitation repair: false
- H3 DCC35 redundancy repair: false
- H4 exact-law native-runtime compatibility: false
- H5 effective-closure diagnosis: false
- primary route: `STRONG_TEMPORAL_OR_JET_CONTRACT_MISMATCH`

No architecture transition, test unlock or long training is authorized.

## Data-driven identifiability matrix

### Current sparse centers

DCC35:
- confirm characteristic mean: **0.43284**
- confirm integral mean: **0.42779**
- median normalized Gram condition number: **8.38e5**

Direct P13:
- confirm characteristic mean: **0.50078**
- confirm integral mean: **0.49582**
- median condition number: **6.65e5**

DCC35 therefore fits the observed finite-time closure better than P13, but both remain far from a clean local-generator identification.

### Early-enriched centers

DCC35 characteristic mean: **0.69688**

P13 characteristic mean: **0.74668**

P13 median condition number improves to **5.80e4**, approximately **11.46x** better than current sparse P13, but the residual becomes about **49% worse**.

Thus improved conditioning alone does not restore the governing law.

### Uniform-dense centers

DCC35 characteristic mean: **0.72442**

P13 characteristic mean: **0.77775**

Again the additional temporal centers worsen closure.

## Canonical-space attribution

On the best alternate center set, P13 / DCC35 characteristic ratio is approximately:

**1.0715**

DCC35 / P13 condition-number ratio is only:

**1.91**

Therefore the preregistered DCC35-redundancy hypothesis does not explain the failure.

DCC35 is not simply failing because it has too many canonical terms.

## Runtime attribution

Reporting-only continuum oracle program:

`R(u)=u-u^2, D=1, T=S=0`

under the current P13 `IPMStep` executor gives full-horizon internal Rel-L2:

**0.21672**

The previously learned PB2-Q0 effective-closure programs give:

**0.03936** mean.

Therefore the frozen H4/H5 hypotheses fail.

The learned programs are reproducing the benchmark trajectory better than the nominal continuum law executed by the current coarse-grid runtime.

This is strong evidence that PB2-Q0 learned an **effective discrete/coarse closure**, not the continuum governing generator.

## Critical caveat: the preregistered oracle relative-residual summary degenerates near equilibrium

The attribution report lists enormous uniform-dense oracle relative residuals (~1e11).

Inspection of `oracle_per_center_profile.csv` shows why:

- by approximately saved center 28 (t≈0.28), the temporal target RMS becomes numerically zero for the audited trajectories;
- the relative residual denominator is therefore clamped to 1e-12;
- tiny absolute derivative/jet errors are divided by an essentially zero physical evolution signal.

Thus the huge 1e11 value is a **metric degeneracy**, not a physically meaningful residual magnitude.

The primary route remains directionally useful — the strong observation/jet/runtime contract is mismatched to this dataset — but the 1e11 oracle value must not be interpreted literally.

## Informative early-time evidence

Before equilibration, the exact continuum generator is much more compatible:

- center 2: characteristic 0.143, integral 0.0318
- center 3: characteristic 0.0878, integral 0.0528
- center 4: characteristic 0.0911, integral 0.0801
- center 5: characteristic 0.1188, integral 0.1135
- center 6: characteristic 0.1559, integral 0.1488

For centers 2–6, signal-weighted aggregate:
- characteristic residual ≈ **0.130**
- integral residual ≈ **0.056**

After this short transient, the Reaction-Diffusion trajectories rapidly approach a low-dynamics manifold and pointwise derivative/relative-residual identifiability degrades.

## Source audit of PDEBench generator

The pinned PDEBench source confirms:
- periodic finite-volume grid, nx=1024, L=1;
- rho=1, nu=0.5;
- exact logistic reaction substep;
- second-order finite-volume diffusion flux;
- dt_save=0.01;
- CFL=0.25.

The continuum target equation `u_t=u-u^2+0.5*u_xx` is therefore correct as a reporting equation.

However, the saved trajectories come from a specific discrete splitting scheme, and the final benchmark runtime is evaluated after spatial stride reduction. A continuum spectral/characteristic P13 executor is not guaranteed to reproduce that coarse observation exactly.

## Updated interpretation

PB2-Q0-FIX1 narrows the problem to **observability + discrete/jet semantics**, rather than simple temporal-center scarcity or DCC35 redundancy.

Three effects now require separation:

1. temporal signal collapses rapidly after the early transient;
2. high-order local derivatives amplify float32 quantization/noise as the spatial field becomes nearly uniform;
3. the benchmark generator and the P13 runtime use different discrete execution semantics, so an effective learned closure can outperform the nominal continuum oracle on the coarse observed trajectory.

The next attribution must explicitly compare:
- current LocalTaylor jet;
- float64 LocalTaylor evaluation;
- generator-matched finite-difference diffusion operator;
- signal-weighted rather than per-center relative oracle metrics;
- data-only temporal observability selection.

No official test may be opened.
