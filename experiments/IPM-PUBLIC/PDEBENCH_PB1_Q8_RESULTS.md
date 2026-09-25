# IPM-PDEBench-PB1-Q8 Results — Unseen-Viscosity Independent Confirmation

## Integrity

Result ZIP SHA256:

`4cdadd4de4538808739f05e854ba29d49d813d289aba6de0730f00bd19b092d0`

Detached manifest: **17/17 payload entries match** by byte size and SHA256.

Embedded protocol SHA256:

`08a8d4054d83bcc3673ea91e003f31567bfe31855fb5160d0b3475bffe07ab80`

Executed notebook SHA256:

`5ecad41cdd7c64676fd141c929b35d8b0082bf97f64f25dd1d1fd38905688f2c`

The executed notebook contains the frozen Q8 protocol hash and produced no official-test metric files beyond empty placeholders because the internal unlock gate failed.

## Formal outcome

**PB1-Q8 FAIL**

- internal qualification: **FAIL**
- official test accessed: **FALSE**
- external confirmation: **NOT RUN**
- architecture changed in Q8: **FALSE**
- 500-epoch training authorized: **FALSE**

The official first 1,000 test trajectories for both unseen viscosities remain unobserved.

## Parameter-wise outcome

### Burgers epsilon=0.1

All internal gates pass strongly.

Three-fold internal confirm means:
- DIC-DCC35 characteristic: **0.008554**
- Simpson-integral residual: **0.006789**
- refined 31-step rollout: **0.015170**
- DIC / integral-only characteristic ratio: **0.845976**
- coefficient cosine median: **~1.000000**

This is a strong out-of-development-parameter success in a smoother diffusion-dominated regime.

### Burgers epsilon=0.001

The lower-viscosity regime fails I1/I2/I3 while passing I4/I5/I6.

Three-fold internal confirm:
- DIC-DCC35 characteristic mean: **0.468684**
- characteristic max: **0.470330**
- Simpson-integral mean: **0.405274**
- Simpson-integral max: **0.408726**
- refined 31-step rollout mean: **0.298258**
- rollout max: **0.300546**
- DIC / integral-only characteristic ratio: **0.874346**
- coefficient cosine median: **0.999587**

Thus the failure is highly systematic and not a fold-instability effect.

## Critical post-run physics audit

PDEBench's pinned Burgers generator uses the diffusion coefficient:

`epsilon / pi`

in physical coordinates.

Because the IPM Taylor coordinate is:

`a2 = u_xx / 2`

the reporting-only exact canonical coefficient is:

`2*epsilon/pi`

not `2*epsilon`.

This corrects the interpretation used in earlier Q7/Q7-FIX1 reporting.

### epsilon=0.1

Reporting-only exact:
- transport `u*a1`: **-1**
- diffusion `a2`: **0.06366198**

Three Q8 DCC fits recover:
- transport: about **-0.99787**
- diffusion: about **0.0636664**

Mean raw coefficient errors are approximately:
- transport amplitude: **0.21%**
- diffusion: **0.0069%**

The recovered local differential law is essentially exact.

### epsilon=0.001

Reporting-only exact:
- transport `u*a1`: **-1**
- diffusion `a2`: **0.000636620**

Three Q8 DCC fits recover:
- transport mean: about **-0.966806**
- diffusion mean: about **0.000647121**

Mean raw coefficient errors are approximately:
- transport amplitude: **3.32%**
- diffusion: **1.65%**

Therefore the low-viscosity Q8 failure is **not primarily a PDE-law coefficient identification failure**.

## Gain-closure signal

At epsilon=0.001, the four-gain native-flow refinement moves the already-near-correct physical law away from its reporting-only coefficients:
- effective transport mean becomes about **-0.806**
- effective diffusion mean becomes about **0.001876**, roughly **2.95x** the exact Taylor-coordinate diffusion coefficient

Yet refined 31-step rollout improves only from roughly `0.33` to `0.298`.

By contrast, at epsilon=0.1 the gains remain approximately one and preserve the identified physical coefficients.

This strongly suggests that the gain stage is compensating for a low-viscosity discretization/runtime mismatch rather than correcting a wrong learned law.

## Scientific interpretation

The Q8 split is now:

- smooth/high-viscosity regime: law identification and native execution both close;
- low-viscosity/sharp-gradient regime: DCC identifies the correct PDE coefficients, but the strong-form jet observations and/or the current native discretization do not reproduce the same law accurately enough at the reduced N=256 benchmark grid.

The next experiment must therefore isolate:
1. spatial-resolution error;
2. local-jet derivative error;
3. native-flow temporal/discretization error;
4. gain compensation.

No change to DIC-DCC35 law identification is authorized by Q8 itself.

The next stage is a train-only low-viscosity discretization attribution study. Official epsilon=0.001 and epsilon=0.1 test sets remain sealed.
