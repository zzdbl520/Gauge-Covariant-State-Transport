# LiH S13: reproducible endpoint-operator analysis

The [`reconstruct_s13.py`](reconstruct_s13.py) script uses the archived
two LiH transport matrices, endpoint dipole and state energies, with NumPy.
No new CASSCF calculation is required.

## Replay

From this directory:

```bash
python reconstruct_s13.py \
  --loop-json ../../analysis/loop_factor_016.json \
  --endpoint-npz ../../wavefunctions/baseline/R_5.950000000000_F_0.011500000000.npz \
  --out s13_full_audit.json
```

Validated outputs are
[`s13_full_audit.json`](s13_full_audit.json) and
[`s13_full_audit.pair_weights.csv`](s13_full_audit.pair_weights.csv),
with all **10 numerical checks passed**. Verification:
https://github.com/zzdbl520/Gauge-Covariant-State-Transport/actions/runs/43467979855 .

| Quantity | Recomputed |
| --- | ---: |
| Normalized transport nonclosure | 0.000319165383701 |
| Axial dipole difference spectral norm (a.u.) | 0.009729790320533 |
| Adiabatic-diagonal mixture bound (a.u.) | 0.000928172130189 |
| Dipole mode-pair 2–3 weight | 37.6643328932% |
| Hamiltonian mode-pair 2–3 weight | 7.3353589013% |
| Hamiltonian difference Frobenius norm (Eh) | 0.000279952802834 |
| Hamiltonian difference spectral norm (Eh) | 0.000179082493589 |

The analyses compare **transported representations of a single endpoint
operator**; they do not establish different physical operators or
nonadiabatic dynamics.
