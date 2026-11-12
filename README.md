# LiH wavefunctions and gauge-covariant closed-loop transport

Companion LiH research data for *Gauge-Covariant Closed-Loop Transport of Multireference State Manifolds* (Journal of Chemical Theory and Computation, manuscript ct-2026-02017u).

## Archived data

- `wavefunctions/baseline/`: 64 original SA-CASSCF MO/CI checkpoints, byte-identical to the verified 2026-10-13 production archive.
- `wavefunctions/refined/`: 90 additional local-refinement MO/CI checkpoints.
- `wavefunctions/histories/forward/` and `wavefunctions/histories/reverse/`: 155 checkpoints per optimization history, including the independently recomputed closing checkpoint.
- `analysis/loop_factor_016.json`: reference analysis for the final 154-edge closed loop.
- `analysis/histories_factor_016.json`: reference analyses of the forward and reverse histories.
- `code/lih_engine.py` and `code/refine_lih.py`: archived analysis and calculation implementation.
- `provenance_manifest.csv` and `history_provenance_manifest.csv`: source records and SHA256 hashes.
- `reproduction_report.json`: direct-loop replay report.
- `history_replay_report.json`: forward/reverse replay report.
- `SHA256SUMS.txt` and `SHA256SUMS_RELEASE.txt`: integrity manifests.

## Computational scope

LiH singlet A1 SA4-CASSCF(2e,5o)/aug-cc-pVTZ. The nuclear separation and external electric field are varied around a closed path. The final nonuniform loop has 154 edges and 154 distinct coordinate nodes (155 vertex entries, including closure). State-overlap and transport quantities are reconstructed from archived molecular-orbital and configuration-interaction coefficients using the archived implementation; no new CASSCF optimizations are needed for these replays.

## Reproduction status

**PASS — direct loop, forward history, and reverse history.**

The direct loop was replayed from 64 baseline plus 90 refined checkpoints. Its stored and replayed values agree to the reported numerical precision:

| Quantity | Direct 154-edge result |
| --- | ---: |
| C | 0.0003191653837014273 |
| D_mu | 0.0006300611946496533 |
| eta (minimum singular value) | 0.9997918305550153 |
| leakage | 0.00040458883948302216 |
| assignment margin | 0.37613122170923985 |
| delta_mu (a.u.) | 0.01509458016614645 |

The independent forward and reverse optimization histories were also replayed from their archived checkpoint chains (155 files each), with provenance and closure checks. Both history qualifications pass. See `history_replay_report.json` for the comparisons against the archived reference results.

These are repeat executions of the original analysis implementation on archived wavefunctions, **not** an independent reimplementation of the algorithm. The original coarse-grid `REVIEW_REQUIRED` decision is preserved: numerical convergence does not override its assignment-margin failure. The refined 154-edge loop passes the stated qualification checks.

## Integrity and reuse

After cloning the repository, verify the full release with:

```bash
sha256sum -c SHA256SUMS_RELEASE.txt
```

The historical `SHA256SUMS.txt` is retained for the original direct-only staging; use `SHA256SUMS_RELEASE.txt` for the full published release. The two checksum manifests are updated when this README changes.

This repository currently documents the **LiH** portion of the manuscript, not the complete wavefunction archive for every molecular example. Consult the manuscript and supporting information for physical definitions, scope, and limitations.

## Citation and licensing

Please cite the associated manuscript and this repository. Add the final journal DOI and bibliographic details when available. No explicit reuse license is asserted here until the authors select one.
