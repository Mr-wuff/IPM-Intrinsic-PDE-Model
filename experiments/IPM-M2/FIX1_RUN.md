# IPM-M2-FIX1 Run

Notebook:
`IPM_M2_FIX1_Overcomplete_Jet_Law_Discovery_RTX5080_WSL_Colab.ipynb`

Notebook SHA256:
`66c485da80c15f9245d0ec4fdd908de5e002401756a2d0c40c4af0ac5386e38a`

Frozen protocol SHA256:
`f0747d9ea789ce5746c53b83d80fe47272718cb524b46789025369667a9dbd80`

Frozen Cartan core SHA256:
`08d7cca4d82367a22af07c87917e9c2dcfc079feb6c686c9ace5c4aa913366bb`

## Parent M2 result
M2 returned FAIL_M2.

Validated:
- analytic Cartan identity;
- learned D_x Q consistency;
- PDE-law Jacobian attribution on 4/5 families.

Failed:
- the temporal-curvature audit as originally defined;
- explicit Cartan-T2 flow, especially KdV;
- dt/grid transfer of Cartan-T2;
- seed reproducibility.

## Theoretical correction
The IPM architecture is defined by the learned characteristic and its Cartan/evolutionary lift. A truncated explicit Taylor time integrator is not part of the defining model.

## FIX1 question
Every PDE receives the same overcomplete J3 local state. The model is not told the true derivative order. We test whether the learned law Jacobian identifies and suppresses the correct derivative orders.

## Output
The notebook automatically exports and downloads:
- IPM_M2_FIX1_RESULTS.zip
- IPM_M2_FIX1_RESULTS.zip.sha256
