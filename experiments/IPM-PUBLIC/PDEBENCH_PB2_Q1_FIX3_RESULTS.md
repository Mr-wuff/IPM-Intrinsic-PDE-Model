# IPM-PDEBench-PB2-Q1-FIX3 Results — Semigroup Compiler-in-Loop Coefficient Identification

## Integrity

Result ZIP SHA256:

`09292008c5420d888db31e90f90a27d0a7c263767e8ae4238a80bc7f7a3952b6`

Detached SHA file matches exactly.

Internal result manifest: **30/30 tracked payload entries match** by byte size and SHA256.

Protocol SHA256:

`36a915e8d28085e710d86b265fc164bfae11d243b78460f5f3d46e20c5da95c3`

Frozen source notebook SHA256:

`83c49c00b57b83e8f85ec97a36902826dd6e86ac26f1d1aa525d953fc13ef8a1`

Executed notebook SHA256:

`158c1b39ebddcc466af5b840ebd2f26fda276c80bb09ab2ec627bb9c6778d0aa`

The executed notebook has no runtime-error outputs.

A direct source comparison found only one execution-layer change in the download helper:
- ensure the parent directory exists;
- guard tmp.replace if the partial file is absent;
- guard MD5 evaluation if the destination file is absent.

No data split, support, compiler, optimizer, gate, coefficient mapping, or official-test logic changed. This is treated as protocol-preserving I/O repair.

## Formal result

All internal gates pass:

- C1 optimization integrity: **PASS**
- C2 screen finite-time closure: **PASS**
- C3 confirm finite-time closure: **PASS**
- C4 coefficient stability: **PASS**
- C5 physical coefficient fidelity: **PASS**
- C6 causal gain over saved-time S2 identification: **PASS**

The protocol therefore correctly unlocked the first 1,000 official trajectories.

All official gates then pass:

- O1 finite: **PASS**
- O2 external finite-time closure: **PASS**
- O3 no degradation cliff: **PASS**

Primary route:

**PB2_REACTION_DIFFUSION_INDEPENDENTLY_CONFIRMED**

Reaction-Diffusion new-family identification is independently confirmed across the held-out diffusion axis.

No 500-epoch training is authorized or needed.

## Internal finite-time closure

Overall:
- screen increment Rel-L2 mean: **0.0150567**
- confirm increment Rel-L2 mean: **0.0154995**

Confirm by held-out environment:

### Nu1 / Rho2
- compiler-in-loop mean: **0.0218108**
- S2-initializer through the same compiler: **0.460525**
- ratio: **0.04752**

### Nu1 / Rho5
- compiler-in-loop mean: **0.0148536**
- S2-initializer: **0.247320**
- ratio: **0.06023**

### Nu1 / Rho10
- compiler-in-loop mean: **0.0098341**
- S2-initializer: **0.181721**
- ratio: **0.05429**

Thus compiler-in-loop identification reduces finite-time confirm error by roughly 94–95% versus the saved-time S2 coefficient initialization.

## Recovered coefficients

Expected held-out continuum coefficients:
- R_u = rho
- R_u2 = -rho
- D0 = 2.

Three-fold means:

### Nu1 / Rho2
- R_u = **1.98753**
- R_u2 = **-1.96858**
- D0 = **1.99713**
- physical coefficient relative L2 mean = **0.01030**
- D0 / true = **0.99856**

### Nu1 / Rho5
- R_u = **5.04183**
- R_u2 = **-5.04945**
- D0 = **1.99605**
- physical coefficient relative L2 mean = **0.00883**
- D0 / true = **0.99802**

### Nu1 / Rho10
- R_u = **10.05501**
- R_u2 = **-10.06880**
- D0 = **1.99688**
- physical coefficient relative L2 mean = **0.00617**
- D0 / true = **0.99844**

Overall reporting-only physical coefficient relative L2 mean:

**0.00843**

The previous saved-time S2 initializers had D0 means of only approximately:
- 0.717
- 0.737
- 0.737

The finite-time compiler-in-loop objective therefore restores the physically correct diffusion coefficient almost exactly.

## Coefficient stability

Median three-fold coefficient cosine:
- Nu1/Rho2: **0.999953**
- Nu1/Rho5: **~1.000000**
- Nu1/Rho10: **~1.000000**

Thus the recovered law is both physically correct and fold-stable.

## Official-block confirmation

No refitting was performed after unlock.

Official increment Rel-L2:

### Nu1 / Rho2
- mean: **0.0232586**
- max fold: approximately **0.02344**

### Nu1 / Rho5
- mean: **0.0159103**
- max fold: approximately **0.01592**

### Nu1 / Rho10
- mean: **0.0104594**
- max fold: approximately **0.01046**

Overall official increment Rel-L2:

**0.0165428**

Official/internal-confirm degradation ratios:
- Nu1/Rho2: **1.0664**
- Nu1/Rho5: **1.0711**
- Nu1/Rho10: **1.0636**

These are far below the frozen 1.50 degradation gate.

## Scientific conclusion

PB2 is now complete.

The full Reaction-Diffusion causal chain is:

1. a canonical physical support can be recovered on the Nu=0.5 rho-sweep;
2. saved-time S2/TR1 identification systematically attenuates stiff diffusion on Nu=1;
3. the true finite-time reaction-diffusion semigroup reproduces the held-out trajectories with the true coefficients;
4. fitting the same frozen physical support directly through that finite-time compiler recovers the held-out coefficients to ~0.84% mean relative error;
5. the still-sealed official block confirms the frozen programs without refitting.

Therefore IPM must explicitly distinguish:

- **infinitesimal PDE algebra**, and
- **physics-role-aware finite-time observation/compiler semantics**.

For smooth Reaction-Diffusion, the qualified native execution/identification contract is:

`Generator-Validity -> canonical support -> semigroup compiler-in-loop coefficient identification -> native finite-time flow`

Reaction-Diffusion mechanism tuning should now stop.

Next authorized stage:

**PB3_NEW_PDE_OR_2D_QUALIFICATION**
