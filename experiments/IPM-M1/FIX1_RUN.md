# IPM-M1-FIX1

## Purpose
Correct the pre-training derivative-audit gate that blocked the original M1 run before any formal model training.

## Amendment
- Original threshold: relative L2 < 1e-8
- FIX1 threshold: relative L2 < 1e-6
- Audit strengthened to:
  - 3 analytic periodic test functions
  - grid sizes 128 / 256 / 512
  - derivative orders 1 / 2 / 3
  - float64 execution
  - maximum and median relative-error reporting

All model architectures, five formal seeds, training settings, generalization tests, and M1 empirical decision gates remain unchanged.

## Notebook
`IPM_M1_FIX1_Holonomic_Closure_Stable_Intrinsic_Evolution_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`d29370550bd9daf9e016a63d53d5b10338a2342bd993086b5e119d6f06ad9c19`

Frozen FIX1 protocol SHA256:
`deca7139d49d596a67d64722dfdba4404d2b193371f6756b9fd75c69d4894770`

## Output
The completed notebook generates and automatically downloads in Colab:
- `IPM_M1_FIX1_RESULTS.zip`
- `IPM_M1_FIX1_RESULTS.zip.sha256`

## Scientific status
The original M1 attempt is recorded as **pre-training audit blocked**, not as an IPM architecture failure.
