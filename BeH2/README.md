# BeH2: history-dependent CASSCF state manifolds

Companion BeH2 data for *Gauge-Covariant Closed-Loop Transport of Multireference State Manifolds* (JCTC manuscript ct-2026-02017u).

## Scope and provenance

This directory is separate from the existing LiH release at the repository root. The six-point BeH2 analysis uses A1-symmetry SA3- and SA4-CASSCF(6e,6o)/cc-pVTZ solutions at lambda = 2.52170, 2.52175, 2.52180, 2.52185, 2.52190, and 2.52195 bohr, with two continuation histories per state-averaging protocol. Original PySCF orbital-gradient convergence tolerance: 3e-6. The archived wavefunction files must be obtained from the original gu03 calculation directory, not regenerated from the analysis tables.

Original HPC source directory (not a public URL):
`/mnt/BeH2/BeH2_B0/BeH2_B3R/BeH2_B3R_work/`

Expected original checkpoint layout:
`solutions/A1/SA3/unique_up/`,
`solutions/A1/SA3/upper_down/`,
`solutions/A1/SA4/upper_up/`,
`solutions/A1/SA4/upper_down/`.

## Verified numerical reference

At lambda = 2.52195 bohr, PySCF 2.13.1 `fci.addons.overlap` gives:
- SA3 unique_up vs upper_down: minimum singular value 0.9178266379157551; mean leakage 0.05473436113970365.
- SA4 upper_up vs upper_down: minimum singular value approximately 1; mean leakage approximately 0.
- SA3 unique_up vs SA4 upper_up: minimum singular value 0.898052075; mean leakage 0.082880230.
- SA3 upper_down vs SA4 upper_down: minimum singular value 0.976538063; mean leakage 0.030405492.

The SA3 history energy separation at this point is approximately 5.619197663 mEh. The 2.52180 -> 2.52185 bohr SA3 upper_down edge exhibits a localized fidelity loss. This is a **fidelity failure**, not a qualified geometric holonomy.

## Reproduction

Requires Python 3.11, NumPy and PySCF 2.13.1. With the full checkpoint archive restored and the analysis script present, run from the original work directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python -u BeH2_original_PySCF_fidelity_v5_complete.py \
  --root "$PWD/solutions/A1" --out "$PWD/BeH2_v5_full" \
  --start 2.52170 --count 6
```

Outputs include `summary.csv`, `sa4_subsets.csv`, and `report.json`. Same-geometry comparisons use the stored AO overlap; intergeometry comparisons require AO cross-overlap integrals. The SA4 subset (0,1,3) is important in mixed-model comparisons; do not automatically substitute the lowest three SA4 roots.

## Release completeness

**Staging status — NOT YET a complete reproducibility release.** This initial documentation does not certify that the original NPZ checkpoints, original calculation/analysis scripts, full output JSON, or SHA256 manifest have been uploaded. Do not describe the archive as fully reproducible until those files are present, independently verified, and checksummed. Existing root-level LiH data and checksum manifests must remain unchanged.

## Interpretation and limitations

The history-dependent SA3 stationary solutions are distinct at the original convergence tolerance. The near-unity SA4 history fidelity and the nonzero SA3/SA4 cross-model leakage are separate observations. Fidelity loss at a mixed-model or nuclear edge prevents interpreting that edge's nonclosure as a controlled geometric holonomy. Earlier custom determinant-minor overlap results were inconsistent with PySCF and are superseded by the native PySCF audit.

Please cite the associated manuscript and repository. No license is implied unless explicitly supplied by the authors.
