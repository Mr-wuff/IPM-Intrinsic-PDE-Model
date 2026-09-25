# IPM-PDEBench-PB1-Q8-FIX3-FIX1 Frozen Run Record

Experiment:

`IPM-PDEBENCH-PB1-Q8-FIX3-FIX1`

Notebook:

`IPM_PDEBench_PB1_Q8_FIX3_FIX1_Conservative_Observation_Operator_Attribution_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:

`22570793e39a92d3dcfae1acea5ca98ed528375009056e7b35e41e9047b67d75`

Protocol SHA256:

`9e2624b4a5cbd8597779f451b5a427dc6ec43d4cbf938343da16513c72369656`

Pinned repository commit used by the notebook:

`82aeb32c23d45949c9639d7f965da79e06721253`

Policy:
- official first 1,000 epsilon=0.001 trajectories remain sealed;
- Q8-FIX3 mechanism rows are intentionally reused because this is an observation-operator attribution run, not independent confirmation;
- FULL1024, STRIDE4-256 and conservative AVG4-256 use the identical WCFC-5 identification contract;
- known Burgers coefficients are reporting-only;
- no architecture transition is authorized from this run;
- no 500-epoch training.
