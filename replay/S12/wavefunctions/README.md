# Archived LiH wavefunctions — 21 October 2026 revision

These 10 compressed archive parts and their manifests were copied unchanged from
[the original `electronic-state-identity` release](https://github.com/zzdbl520/electronic-state-identity/tree/main/data/revision-2026-10-21/wavefunctions).
GitHub Actions verified all 10 parts against their recorded SHA-256 checksums.

The archive contains **1,936 NPZ checkpoints**, including candidates and
duplicate baselines (not 1,936 distinct geometries):

- aug-cc-pVDZ revision: 337 files
- cc-pVTZ revision: 194 files
- aug-cc-pVTZ production: 736 files
- aug-cc-pVTZ local refinement: 644 files
- initial-grid replay: 25 files

## Reconstruct the wavefunctions

From the directory containing this README:

```bash
python3 unpack_wavefunctions.py --destination ./restored
```

The script verifies each part, the reconstructed archive, and each extracted
NPZ file against `MANIFEST.json` and `SOURCE_PROVENANCE.json`.
It does not rerun CASSCF or overwrite local files whose hashes disagree.

The cross-basis S12 tables still require a separate comparison using the
corresponding checkpoint files and complete-four-electron overlap method.
Restoring the original wavefunctions is an archiving step, **not** a claim that
all cross-basis numerical diagnostics have already been independently replayed.
