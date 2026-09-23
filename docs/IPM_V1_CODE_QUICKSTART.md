# IPM-v1 reusable core

Install directly from GitHub:

```bash
pip install "git+https://github.com/Mr-wuff/IPM-Intrinsic-PDE-Model.git@main"
```

Then:

```python
import torch
from ipm_v1 import load_program, IPMStep, HorizonCUDAGraph

program = load_program("advection_beta1", seed=202)
step = IPMStep(program, n=256, length=1.0, dt=1e-3).cuda().eval()

u = torch.randn(16, 1, 256, device="cuda")
y = step(u)

graph = HorizonCUDAGraph(step, u, steps=40)
graph.reset(u)
y40 = graph.replay()
```

The package contains the exact frozen Q3-FIX2 program coefficients for seeds 101/202/303. Historical Q0/Q3-FIX2/Q4 result ZIP files are **not required** for future IPM experiments.

Architecture/research utilities exposed by the package:
- `LocalTaylorJet`
- `IDTC`
- `canonical_terms`
- `principal_role_coeffs`
- `cartan_dx`
- `evolutionary_field_components`
- `simpson_integral_loss`

Reusable numerical baselines live in `ipm_v1.benchmarks`.

Important: the constant-velocity semi-Lagrangian baseline includes the post-B0 batch-index correction.