# IPM-M3-FIX1 Run

Notebook:
`IPM_M3_FIX1_Compute_Observation_Matched_Identification_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`c2192cb8943a9e7af4b7d952d49ec69cf0201bab5b0e0484f816303706b64f72`

Frozen protocol SHA256:
`dc469f14e1cba4691d90de188f85d7f55412b46e7c804f5ee3125989512a256d`

Matched sampler SHA256:
`c93863c7df1583de6e8945e9c40bd16fed4210c7e74e40a97972bc371330c9ba`

## Fairness controls
- identical initial state_dict per PDE/seed across methods;
- identical trajectory triplet per optimizer step;
- identical stride schedule;
- identical batch size;
- 64 optimizer steps per epoch;
- 24 epochs;
- 1536 updates per run;
- identical optimizer and LR schedule;
- final checkpoint only, no objective-specific early stopping.

## Parent result
M3 formally passed all preregistered gates and established trajectory-only IPM identifiability. FIX1 is required only to validate direct method-superiority claims under matched compute and observation budgets.
