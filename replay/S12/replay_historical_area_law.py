#!/usr/bin/env python3
"""Replay LiH S12 area-law regressions from archived, numerical source records.

This verifies reported regression coefficients and C/A ratios, not original
CASSCF convergence, cross-basis MO/CI overlaps, or orbital-character results.
No external dependencies beyond the Python 3 standard library.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "historical"

def csv_records(name):
    with (DATA / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def linear_fit(records, x="area", y="C"):
    values = [(float(row[x]), float(row[y])) for row in records]
    n = len(values)
    if n < 2:
        raise ValueError("At least two points are necessary")
    xm = sum(a for a, _ in values) / n
    ym = sum(b for _, b in values) / n
    denom = sum((a - xm) ** 2 for a, _ in values)
    slope = sum((a - xm) * (b - ym) for a, b in values) / denom
    return {"n": n, "slope": slope, "intercept": ym - slope * xm}

def loop_records(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return json.load(f)

def assert_close(label, found, expected, tol=1e-6):
    if abs(found - expected) > tol:
        raise AssertionError(f"{label}: found {found:.12g}, expected {expected:.12g}")
    print(f"PASS  {label:44s} {found:.10f}")

def main():
    raw = csv_records("lih_100_locator_plaquettes.csv")
    complete = csv_records("lih_100_complete_overlap_rectangles.csv")
    assert len(raw) == len(complete) == 100
    fit_raw = linear_fit(raw)
    fit_complete = linear_fit(complete)
    assert_close("100 rectangles, active-only slope", fit_raw["slope"], 2.4381877)
    assert_close("100 rectangles, complete-overlap slope", fit_complete["slope"], 2.4330042)
    assert not any(row["fidelity_pass"].strip().lower() == "true" for row in complete), (
        "The historical complete-overlap rectangles were reported as failing fidelity"
    )

    pvdz = [
        {"area": str(row["area"]), "C": str(row["C"])}
        for row in loop_records("augccpvdz_loop_results.json")
        if float(row["scale"]) < 1.0 and int(row["segments_per_side"]) == 8
    ]
    pvdz.sort(key=lambda row: float(row["area"]), reverse=True)
    apvtz = [{"area": row["area"], "C": row["C8"]}
             for row in csv_records("lih_augccpvtz_nested.csv")]
    apvtz.sort(key=lambda row: float(row["area"]), reverse=True)
    assert len(pvdz) == len(apvtz) == 4
    for a, b in zip(pvdz, apvtz):
        assert abs(float(a["area"]) - float(b["area"])) < 1e-13

    fit_a = linear_fit(pvdz)
    fit_t = linear_fit(apvtz)
    assert_close("aug-cc-pVDZ, four local loops slope", fit_a["slope"], 2.4486702)
    assert_close("aug-cc-pVTZ, four local loops slope", fit_t["slope"], 2.1209885)
    ratio_a = float(pvdz[-1]["C"]) / float(pvdz[-1]["area"])
    ratio_t = float(apvtz[-1]["C"]) / float(apvtz[-1]["area"])
    assert_close("aug-cc-pVDZ, smallest loop C/A", ratio_a, 2.4456741)
    assert_close("aug-cc-pVTZ, smallest loop C/A", ratio_t, 2.1186230)
    print(f"PASS  100 complete-overlap rectangles all fail fidelity")
    print(f"Basis difference, relative to aug-cc-pVDZ: {100*(ratio_a-ratio_t)/ratio_a:.5f}%")
    print(f"Curvature norms from 2*sqrt(4)*C/A: {4*ratio_a:.7f} and {4*ratio_t:.7f}")
    print("\nSix area-law checks PASS. Cross-basis matrix and orbital diagnostics NOT tested.")

if __name__ == "__main__":
    main()
