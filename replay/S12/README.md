# LiH S12: basis comparisons and area-law reproducibility

This directory contains the **verified** Section S12 numerical evidence. The
historical 1,936-checkpoint LiH archive is at
[`wavefunctions/`](wavefunctions/), with SHA-256 checksums and an unpacking
script. It includes all source checkpoints required for the 64-vertex
three-basis comparison.

## Reproducible calculations

1. `python replay/S12/replay_historical_area_law.py` from the repository
   root, or `python replay_historical_area_law.py` from this directory,
   reconstructs six reported area-law coefficients from five archived numerical
   records in `historical/`. All six values match SI S12.
2. `replay_s12_cross_basis.py` computes the full four-electron overlaps at
   **64 matched vertices × three bases = 192 checkpoint inputs**, with PySCF
   2.13.1 and NumPy, after unpacking the NPZ archive. It reproduces the
   energy-gap table, cross-basis state singular values and leakage, active-
   orbital singular values, core overlaps and active-orbital spatial extent.

Results:
[`s12_common_grid_audit.json`](s12_common_grid_audit.json).
Verified run:
https://github.com/zzdbl520/Gauge-Covariant-State-Transport/actions/runs/43467979855 .

| Basis pair | Minimum state singular value | Maximum leakage |
| --- | ---: | ---: |
| aug-cc-pVDZ / cc-pVTZ | 0.3219063494 | 0.4270069775 |
| aug-cc-pVDZ / aug-cc-pVTZ | 0.9780704286 | 0.0211952771 |
| cc-pVTZ / aug-cc-pVTZ | 0.3102168143 | 0.4384681678 |

All pairs fail the specified cross-basis fidelity acceptance, while the
accepted within-basis LiH loops remain qualified. These are postprocessings
of archived wavefunctions, **not new CASSCF optimizations**.

The original files came from the public
[`electronic-state-identity` October 2026 revision](https://github.com/zzdbl520/electronic-state-identity/tree/main/data/revision-2026-10-21).
