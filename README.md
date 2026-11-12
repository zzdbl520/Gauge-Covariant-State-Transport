# LiH wavefunctions and gauge-covariant closed-loop transport

Companion research data for *Gauge-Covariant Closed-Loop Transport of Multireference State Manifolds* (JCTC manuscript ct-2026-02017u).

## Contents

- `wavefunctions/baseline/`: 64 frozen original SA-CASSCF MO/CI checkpoints, verified byte-identical to the 2026-10-13 production archive.
- `wavefunctions/refined/`: 90 additional local-refinement checkpoints.
- `code/`: exact archived computation implementation.
- `analysis/loop_factor_016.json`: 154-edge reference analysis.
- `provenance_manifest.csv`: ordered vertices and original paths plus SHA256.
- `reproduction_report.json`: independent execution of the original analysis implementation against archived MO/CI checkpoints.
- `SHA256SUMS.txt`: checksums for this staged release.

## Scientific protocol

LiH SA4-CASSCF(2,5)/aug-cc-pVTZ; nuclear distance and electric field vary along a closed 154-edge loop. The replay reconstructs four-electron state overlaps from saved MO and CI coefficients using the original code, without rerunning CASSCF.

## Status and limitations

The **direct 154-edge loop** has been replayed successfully. The forward/reverse history wavefunctions are **not included in this initial staging** and their end-to-end replay has **not yet been certified**. Do not describe this staging as the complete final research deposit. The original coarse baseline may fail the assignment-margin qualification despite numerical convergence; the refined loop passes.

## Verification

From the release directory, run `sha256sum -c SHA256SUMS.txt`. A complete public replay entrypoint and the forward/reverse history checkpoints must be added before final publication.

## Software and citation

The computation was performed using PySCF and NumPy/SciPy. Check the manuscript and software versions before public release. Add the final article DOI, citation, authors, and an explicitly chosen license before making the repository public.
