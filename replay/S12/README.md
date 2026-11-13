# LiH Section S12 — archived area-law replay

**Scope:** We have restored the historical numerical records from the previous public repository,
[`zzdbl520/electronic-state-identity`](https://github.com/zzdbl520/electronic-state-identity),
revision `data/revision-2026-10-21/`. The copied CSV/JSON records in `historical/` are preserved
for replay and should not be interpreted as fresh CASSCF calculations.

## Independently replayed from numerical records

Run from this directory, using only Python 3 standard-library modules:

```bash
python replay_historical_area_law.py
```

The script recomputes, rather than copying SI values into its outputs, six S12 quantities:

| Source record | Quantity | Replay result |
| --- | --- | ---: |
| 100 locator rectangles | Active-only area slope | 2.4381877205 |
| Same 100 rectangles, complete overlap | Area slope | 2.4330041559 |
| Four aug-cc-pVDZ local loops (8 segments/side) | Area slope | 2.4486701653 |
| Four aug-cc-pVTZ local loops (8 segments/side) | Area slope | 2.1209884895 |
| Smallest aug-cc-pVDZ local loop | C/A | 2.4456740705 |
| Smallest aug-cc-pVTZ local loop | C/A | 2.1186230352 |

The script also verifies that none of the original 100 *complete-overlap* rectangles meets
the fidelity acceptance criterion. This is a reconstruction of **reported regressions
from archived numerical source records**. It does not independently recompute the
underlying wavefunction overlaps.

The older `check_s12_reported_arithmetic.py` is retained as a separate, weaker check
of SI-table arithmetic; it is not a substitute for the record-based replay above.

## Cross-basis wavefunction replay — next validation step

The old public archive already includes **1,936 checkpoint NPZ files**, among them
337 aug-cc-pVDZ, 194 cc-pVTZ, and 736 augmented-triple-zeta production
files (plus 644 refinement and 25 initial-grid records). Counts include
optimizer candidates and duplicate baselines, not independent geometries.
The approximately 37.8 MB compressed wavefunction archive is under
[the old repository's `wavefunctions/` folder](https://github.com/zzdbl520/electronic-state-identity/tree/main/data/revision-2026-10-21/wavefunctions),
with `MANIFEST.json`, provenance records and SHA256 checksums.

To restore it *without rerunning CASSCF*, clone the old repository and run:

```bash
git clone https://github.com/zzdbl520/electronic-state-identity.git
cd electronic-state-identity
python scripts/unpack_wavefunctions.py
```

The old repository's
[`code/run_lih_revision.py`](https://github.com/zzdbl520/electronic-state-identity/blob/main/data/revision-2026-10-21/code/run_lih_revision.py)
and
[`systems/lih/workflow/LiH_S4_cross_basis_audit.py`](https://github.com/zzdbl520/electronic-state-identity/blob/main/systems/lih/workflow/LiH_S4_cross_basis_audit.py)
provide the historical calculation/analysis context. The **S4 script uses an earlier
active-only overlap construction and is not, by itself, a validation of the
current complete-four-electron cross-basis S12 table**.

**Not yet independently recalculated here:** the S12 cross-basis state singular
values, orbital-character measures, and all common-vertex gaps from the recovered
NPZ files. These require selecting the corresponding 64 checkpoint files per
basis and running the complete-overlap analysis. The original binary archive is
not duplicated in this directory; its provenance and checksum records remain
available in the old repository.

The cross-basis fidelity failure does not invalidate the accepted **within-basis**
LiH path-transport results.


## Completed common-grid molecular replay (14 November 2026)

The recovered historical NPZ checkpoints have now been independently
reanalyzed using `replay_s12_cross_basis.py` and PySCF 2.13.1. This is a
postprocessing calculation of complete-four-electron state overlap matrices
using **192 archived NPZ checkpoint inputs** on 64 common vertices in each
of three bases; no new CASSCF was run.

The machine-readable result is [`s12_common_grid_audit.json`](s12_common_grid_audit.json).
Its cross-basis minimum state singular values A/D, A/T, D/T are
0.3219063494, 0.9780704286, 0.3102168143 respectively; all agree
with SI Section S12. The energy gaps, leakage, active-orbital
singular values, core overlaps and corner mean squared orbital extents
also agree with the reported SI tables. The validated GitHub Actions
run is [here](https://github.com/zzdbl520/Gauge-Covariant-State-Transport/actions/runs/43467979855).
Earlier scope notes above refer to the original area-law-only stage
and are superseded for the common-grid calculations by this section.
