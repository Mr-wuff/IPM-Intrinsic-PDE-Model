# IPM-PDEBench-PB1-Q4 Results — Native-Flow Gain Closure Qualification

## Integrity

Uploaded result ZIP SHA256:

`77d9fdea708cf3368885a10dba409be51350d40c206ceba753f5fbb2e431d685`

External SHA256 file matches exactly.

The detached result manifest contains 18 payload entries. All 18 match archived byte size and SHA256.

Executed notebook audit:
- all 8 code cells are byte-for-byte identical to the frozen PB1-Q4 notebook;
- no gate, data split, objective, or runtime code was modified during execution.

Embedded protocol SHA256:

`0e59ed3d12ba99ebbca512b8ed01114093e842bc81ef24fe7ff22f1147b1f58b`

## Runtime semantics

The differentiable native-flow implementation is exactly aligned with repository IPMStep for the audit input:

- runtime parity Rel-L2: **0.0**
- gain gradient norm: **0.1756164**
- gain gradients finite: **true**
- gain gradient non-zero: **true**

Therefore the compiler-in-the-loop gain optimization is scientifically valid.

## Main results

| PDE | candidate | Q3 secant-gain rollout8 | Q4 refined rollout8 | ratio | secant preservation ratio |
|---|---|---:|---:|---:|---:|
| Advection beta=1 | T1_S111_NATIVE_LOCAL | 0.527312 | **0.482625** | **0.915254** | 1.002744 |
| Advection beta=1 | T1_S124_NATIVE | 0.550621 | 0.547166 | 0.993724 | 1.018584 |
| Burgers nu=0.01 | T1_S111_NATIVE_LOCAL | 0.191893 | **0.181067** | **0.943584** | 1.022792 |
| Burgers nu=0.01 | T1_S124_NATIVE | 0.169935 | 0.162764 | 0.957802 | 1.019083 |

S111 reduces the remaining Advection validation rollout error by about 8.47% while changing secant error by only +0.27%.

## Formal gate

### T1_S111_NATIVE_LOCAL

Passes every preregistered gate:
- finite training and rollout;
- runtime parity <= 2e-6;
- refined rollout <= 0.50 on both PDEs;
- per-task refined/baseline rollout <= 1.10;
- secant preservation <= 1.15;
- max absolute gain <= 6;
- geometric-mean refined/baseline rollout ratio = **0.929311 <= 0.99**.

Geometric-mean refined rollout error:

**0.295614**

Result:

`candidate_pass=true`

### T1_S124_NATIVE

Fails only the frozen Advection absolute-rollout gate:
- Advection refined rollout = **0.547166 > 0.50**

Result:

`candidate_pass=false`

## Formal decision

`FORMAL_500_EPOCH_RUN_AUTHORIZED=true`

Selected contract:

`T1_S111_NATIVE_LOCAL`

The selected formal pipeline is:

`native-time IDTC identification -> principal RTDS projection -> train-only secant gain calibration -> exact native-flow four-gain refinement -> frozen native IPM runtime`

## Scientific conclusion

PB1-Q4 closes the remaining PB1-Q3-FIX1 gap without expanding the algebra.

The evidence supports that the four-role principal normal form is sufficient for the current Advection/Burgers qualification line when its role amplitudes are closed against the actual discrete native flow.

The next stage is the preregistered PB1-Q5 formal 500-epoch, 3-seed, standard-data run. No further candidate tuning is permitted before the official test evaluation.
