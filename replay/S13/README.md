# LiH operator-specific transport: Section S13 replay

This directory contains a **postprocessing-only** numerical replay for the LiH example in *When State Tracking Is Not Enough: Path-Dependent Transport in Multireference Calculations* (JCTC manuscript ct-2026-02017u). It does not repeat CASSCF optimization or wavefunction-overlap evaluation.

## Reproduced from already public matrices

The input `lih_public_inputs.json` is an extraction of the two route matrices and the transported axial-dipole **difference** matrix from [`analysis/loop_factor_016.json`](../../analysis/loop_factor_016.json). Run with Python 3 and NumPy:

```bash
cd replay/S13
python reconstruct_s13.py
```

The independent matrix postprocessing reproduces the following values (rounded):

| Quantity | Value | Status |
| --- | ---: | --- |
| Route nonclosure, `||K_a-K_b||_F / (2 sqrt(m))`, `m=4` | 0.000319165383701 | Verified |
| Axial-dipole difference, Frobenius norm (a.u.) | 0.015094580166146 | Verified |
| Axial-dipole difference, spectral norm (a.u.) | 0.009729790320533 | Verified |
| Maximum difference for adiabatic-diagonal mixtures (a.u.) | 0.000928172130189 | Verified |
| Eigenphase pair 2--3 contribution to squared axial-dipole difference | 37.66433289% | Verified |
| Sum of six dipole eigenphase-pair contributions | 100.0000000013% | Verified |

The checked outputs are in `s13_replay.json` and `s13_replay.pair_weights.csv`. These are **numerical re-analyses of archived route/dipole matrices**, not independent regenerations of the underlying CASSCF wavefunctions.

## Extended operator check (not yet recorded as verified here)

The already public endpoint checkpoint
[`wavefunctions/baseline/R_5.950000000000_F_0.011500000000.npz`](../../wavefunctions/baseline/R_5.950000000000_F_0.011500000000.npz)
contains `state_energies_Eh` and `dipole_au`. It can be used to recalculate the transported endpoint dipole and Hamiltonian operator differences:

```bash
python reconstruct_s13.py \
  --loop-json ../../analysis/loop_factor_016.json \
  --endpoint-npz ../../wavefunctions/baseline/R_5.950000000000_F_0.011500000000.npz \
  --out s13_replay_with_endpoint.json
```

The Hamiltonian eigenphase-pair percentage reported in the SI (**7.34%**) is **not independently certified by the six-check replay** in this directory. To claim this additional check as completed, execute the command above and save the resulting output.

Different route-transported representations of the same endpoint operator should not be interpreted as distinct physical endpoint operators or as real-time dynamical differences.
