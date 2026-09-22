# IPM-M3 Run

Notebook:
`IPM_M3_Trajectory_Only_Integral_Flow_Identification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`b62003ae0569e9290c5fdb1550e6db1d06a76903c05a7707241e300b04a162a4`

Frozen protocol SHA256:
`bca4800c196ce02812118814d43a7fa2c366803aee5f07eafc6c958a93c1f5bc`

Frozen IPM core SHA256:
`d481d376f61ab0b0d34485996b688c13560e6c5ade950fa4332776ddad36e451`

Frozen IntegralFlow objective SHA256:
`3ecb5d10f9b5056f9b3c25bb8a525d2b76bf7c52f3f6f597cffd83d2aee3cc87`

## Purpose

Test whether the frozen first-principles IPM core can identify its local characteristic from solution trajectories alone, without exact instantaneous RHS labels.

## Methods

- OracleRHS: exact-RHS upper bound.
- SecantDerivative: trajectory central-difference derivative labels.
- IntegralFlowIPM: trajectory-only integral flow matching.

All three methods share exactly the same local J3 characteristic architecture.

## Formal note

N=512 remains a diagnostic axis only in M3 because M2-FIX1 localized the unresolved extreme-resolution degradation to that regime. The formal grid gate uses N=64/128/256.

## Output

The notebook creates:
- `IPM_M3_RESULTS.zip`
- `IPM_M3_RESULTS.zip.sha256`

and triggers automatic download in Colab.
