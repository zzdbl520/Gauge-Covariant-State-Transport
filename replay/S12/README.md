# LiH Section S12: reported-value arithmetic check

This directory includes only a **reported-table arithmetic check** for the LiH basis and area-law comparisons. It takes previously reported numerical coefficients as inputs, rather than recomputing cross-basis electronic-state overlaps.

Run from a Python 3 installation:

```bash
python check_s12_reported_arithmetic.py
```

The check confirms the 0.21260% overlap-definition difference, 13.3726% / 15.4370% matched-loop basis differences, and `2 sqrt(m)=4` curvature normalization for `m=4`.

**Not yet validated by this directory:** molecular cross-basis overlap singular values, the 192 wavefunction checkpoints across three basis sets, or the historical grid/area-law regression inputs. This script is not a replacement for the original S12 audit and makes no claim of independently reproducing the SI S12 molecular tables.
