# LiH wavefunction archive (historical revision, 21 October 2026)

These **10 byte-identical compressed parts** were copied from the public
[original JCTC electronic-state-identity archive](https://github.com/zzdbl520/electronic-state-identity/tree/main/data/revision-2026-10-21/wavefunctions).
They contain **1,936 NPZ checkpoints** in total:

| Source batch | NPZ count |
| --- | ---: |
| aug-cc-pVDZ revision | 337 |
| cc-pVTZ revision | 194 |
| aug-cc-pVTZ production | 736 |
| aug-cc-pVTZ local refinement | 644 |
| initial-grid replay | 25 |

Counts include optimization candidates and duplicate baselines, not unique
molecular geometries. These are historical wavefunctions, **not new
electronic-structure calculations**.

`MANIFEST.json` records the ten part sizes/SHA-256 hashes and the complete
archive digest. The accompanying `SOURCE_PROVENANCE.json` records each
original NPZ member's SHA-256.

To restore and verify the archive from this directory:

```bash
python3 unpack_wavefunctions.py --destination ./restored
```

The script checks the hash of each part, the concatenated archive, and **all
1,936 extracted NPZ files**, and refuses to overwrite a modified existing file.
No new CASSCF calculations are performed.

This archive supplies the historical checkpoint inputs needed for further
cross-basis S12 checks. The record-based **area-law** slopes have been replayed
separately under `../replay_historical_area_law.py`. Uploading the original
wavefunctions does not itself establish that all S12 cross-basis singular
values and orbital-character measures have been recomputed.
