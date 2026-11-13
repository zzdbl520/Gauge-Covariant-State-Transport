#!/usr/bin/env python3
"""Check arithmetic using S12 coefficients already reported in the SI.

Not a molecular overlap replay; no CASSCF or cross-basis wavefunctions are
read by this program.
"""
a=2.4381877; b=2.4330042
c=2.4456741; d=2.1186230
print(f"Active-only vs complete-overlap global slope difference: {100*(a-b)/a:.7f}% (SI: 0.21260%)")
print(f"Local basis difference relative to aug-cc-pVDZ:  {100*(c-d)/c:.7f}% (SI: 13.3726%)")
print(f"Local basis difference relative to aug-cc-pVTZ: {100*(c-d)/d:.7f}% (SI: 15.4370%)")
print(f"Finite-loop curvature estimates, 2 sqrt(m) = 4:  {4*c:.7f}, {4*d:.7f} (SI: 9.7826963, 8.4744921)")
assert abs(100*(a-b)/a-0.21260)<5.e-5
assert abs(100*(c-d)/c-13.3726)<5.e-4
assert abs(100*(c-d)/d-15.4370)<5.e-4
print("S12 reported-table arithmetic PASS. This does not validate raw cross-basis overlaps.")
