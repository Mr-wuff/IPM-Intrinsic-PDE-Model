# IPM-PDEBench-PB1-Q3-FIX1 Run Record

Notebook:
`IPM_PDEBench_PB1_Q3_FIX1_Gain_Aware_Closure_Qualification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`f978589114695475f3555e8acf375bdb4b92f959107ea735de9beab7868ee618`

Protocol SHA256:
`09ce00a186111268c89a5f68f26bbab54590d452e4771b17bb77a1400fc62fc7`

Pinned IPM commit:
`ae9829a3987b8045ce8754cdad6505f62e715301`

Manual uploads:
**none**

## Purpose

This is the required gain-aware rerun after PB1-Q3 exposed that runtime v1.0.1 stored but ignored principal-role gains.

The notebook first verifies:
- non-unit gains alter runtime output;
- applying gains at runtime is numerically equivalent to folding each gain into that role's polynomial coefficients.

It then repeats the four short native-time fits and train-only gain calibration using only the official PDEBench training block.

The official test block is untouched.

## Formal rule

No 500-epoch run is allowed unless one candidate passes all frozen gain-aware secant/rollout/parity gates on both PDEs.
