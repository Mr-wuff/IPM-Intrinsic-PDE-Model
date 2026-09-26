# IPM-PDEBench-PB1-Q9 Results — Independent Weak-Conservative Branch Confirmation

## Integrity

Result ZIP SHA256:

`8683e569e9b7330bacb94e3b82f0af43535dd42c698e51902247df5700d12a68`

Detached checksum matches exactly.

Internal result manifest: **17/17 payload entries match** by byte size and SHA256.

Protocol SHA256:

`0844281983f5c23274521281bbe10dfeb9af47b4c91800ddde1d257e50d4f058`

Executed notebook SHA256:

`2f08dc0fa791016f5b3015fdc899aac151cb548cf4de39be539e804e152e0377`

Frozen notebook SHA256 from the run record:

`f5f4b3c34e93210dea041d2c3995b7709a14d2a30d135db546a782a28cc38382`

The executed notebook contains 8 code cells and no runtime errors. The embedded frozen protocol hash matches exactly. The full-file notebook hash differs from the frozen source because execution outputs are embedded; exact source-byte identity is not claimed here.

## Formal outcome

**PB1-Q9 PASS**

- internal qualification: PASS for epsilon=0.002 and epsilon=0.004
- official test unlock: correctly triggered only after both internal tasks passed
- official test accessed: TRUE
- external confirmation: PASS for both viscosities
- weak-conservative branch frozen: TRUE
- Burgers mechanism development complete: TRUE
- next stage authorized: PB2 new PDE family
- 500-epoch training authorized: FALSE

## Internal qualification

### epsilon=0.002
- confirm weak integral mean: **0.000480**
- confirm weak integral max: **0.000480**
- coefficient cosine median: **~1.000000**
- 31-step internal rollout mean: **0.004848**
- 31-step internal rollout max: **0.004852**
- max normalized mean drift: **7.1e-5**
- max Courant: **0.25**

### epsilon=0.004
- confirm weak integral mean: **0.000291**
- confirm weak integral max: **0.000291**
- coefficient cosine median: **0.999999**
- 31-step internal rollout mean: **0.002044**
- 31-step internal rollout max: **0.002045**
- max normalized mean drift: **7.0e-5**
- max Courant: **0.25**

All frozen internal gates I1-I4 pass for both viscosities.

## Sealed official-test confirmation

The first 1,000 official trajectories for each viscosity were opened only after all internal gates passed for both tasks.

### epsilon=0.002
Three-fold official test:
- future Rel-L2 mean: **0.005357**
- future Rel-L2 max: **0.005361**
- PDEBench nRMSE mean: **0.005708**
- PDEBench nRMSE max: **0.005718**
- RMSE mean: **0.002375**
- max normalized predicted-domain mean drift: **8.5e-5**
- all rollouts finite
- max Courant: **0.25**

### epsilon=0.004
Three-fold official test:
- future Rel-L2 mean: **0.002277**
- future Rel-L2 max: **0.002278**
- PDEBench nRMSE mean: **0.002183**
- PDEBench nRMSE max: **0.002184**
- RMSE mean: **0.000927**
- max normalized predicted-domain mean drift: **8.3e-5**
- all rollouts finite
- max Courant: **0.25**

All frozen external gates E1-E4 pass for both viscosities.

## Reporting-only governing-law audit

No exact coefficient was used for fitting or gate decisions.

### epsilon=0.002
Three-fold mean:
- f2 ≈ **0.4999907** vs exact 0.5
- f2 relative error ≈ **1.86e-5**
- kappa ≈ **0.00065221**
- exact epsilon/pi ≈ **0.00063662**
- kappa relative error ≈ **2.45%**
- f1, f3 and f4 remain near zero

### epsilon=0.004
Three-fold mean:
- f2 ≈ **0.5000305** vs exact 0.5
- f2 relative error ≈ **6.10e-5**
- kappa ≈ **0.00128141**
- exact epsilon/pi ≈ **0.00127324**
- kappa relative error ≈ **0.64%**
- f1, f3 and f4 remain near zero

The previously observed epsilon=0.001 diffusion positive bias decreases strongly as viscosity increases, while the quadratic Burgers flux coefficient remains essentially exact.

## Frozen branch

The following scalar periodic shock/conservation branch is now independently qualified:

`FULL finite-volume observation -> Fourier K=4 weak moments -> Simpson-4 integral-only WCFC-5 -> exact conservative compiler -> FV2-MC-Rusanov adaptive CFL=0.25`

The branch is supported on:
- development epsilon=0.001;
- independent epsilon=0.002;
- independent epsilon=0.004;
with sealed official confirmation on the latter two.

## Scientific conclusion

PB1 Burgers mechanism development is complete.

The evidence now supports a structure-dependent IPM architecture:
- smooth/classical strong regime -> holonomic jet + DIC-DCC35;
- shock/conservation weak regime -> low-mode finite-time weak integral WCFC;
- both compile to explicit physical programs and structure-consistent native executors.

Further Burgers mechanism tuning is not justified. The next experiment must move to a genuinely different PDE family.
