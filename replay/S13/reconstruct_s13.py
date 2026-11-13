#!/usr/bin/env python3
"""Independent, zero-new-QC LiH S13 matrix replay from the PUBLIC LiH release.

Input in this bundle: a faithful numerical extraction of route_R_then_F,
route_F_then_R, W, and delta_dipole_in_start_frame (z component) from
analysis/loop_factor_016.json in the official GitHub repository.

For a fuller replay, pass --loop-json to use the complete archived JSON and
--endpoint-npz to use the original endpoint CASSCF checkpoint (containing
state_energies_Eh and dipole_au). No PySCF or new electronic-structure work
is required; NumPy alone suffices.

No physical observables are claimed to change at the same endpoint. The
computed values compare representations transported by two path maps.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np

EXPECTED = {
    "C": 0.0003191653837014273,
    "mu_frobenius_au": 0.01509458016614645,
    "mu_spectral_au": 0.0097297903,
    "mu_diagonal_au": 0.0009281721,
    "mu_mode_23_percent": 37.66433,
    "hamiltonian_frobenius_Eh": 2.7995280e-4,
    "hamiltonian_spectral_Eh": 1.7908249e-4,
    "hamiltonian_mode_23_percent": 7.33536,
}

def load_public_archive(path: Path):
    j = json.loads(path.read_text(encoding="utf-8"))
    if "route_R_then_F" in j:
        a = np.asarray(j["route_R_then_F"], dtype=complex)
        b = np.asarray(j["route_F_then_R"], dtype=complex)
        x = j["delta_dipole_in_start_frame"]
        dm = (np.asarray(x["real"], float) + 1j*np.asarray(x["imag"], float))[2]
    else:
        a = np.asarray(j["K_R_then_F"], dtype=complex)
        b = np.asarray(j["K_F_then_R"], dtype=complex)
        dm = np.asarray(j["Delta_mu_z"], dtype=complex)
    return a, b, dm, j

def eigpairs(a, b, difference):
    """Pair weights can be reconstructed solely from delta-O; O is not needed.

    If delta-O=a O a†−b O b† and V=a†b, then in V's eigenbasis
    D'=U†a†(delta-O)aU has off-diagonal pair weights 2|D'jk|².
    """
    v=a.conj().T @ b
    phases, u = np.linalg.eig(v)
    order=np.argsort(np.angle(phases))
    theta=np.angle(phases[order]);u=u[:,order]
    transformed=u.conj().T @ a.conj().T @ difference @ a @ u
    denominator=np.linalg.norm(difference,"fro")**2
    pairs=[]
    for i in range(len(theta)):
        for k in range(i+1,len(theta)):
            pct=100.0*2.0*abs(transformed[i,k])**2/denominator
            pairs.append({"pair":f"{i+1}--{k+1}","percent":float(pct)})
    return theta, pairs, float(np.max(abs(np.diag(transformed))))

def analyze_difference(a,b,d):
    hermitian_error=float(np.linalg.norm(d-d.conj().T))
    if hermitian_error>1.e-10:
        raise ValueError(f"Non-Hermitian matrix: {hermitian_error:.3e}")
    phases,pairs,diag_error=eigpairs(a,b,d)
    return {"frobenius":float(np.linalg.norm(d,"fro")),
            "spectral":float(np.linalg.norm(d,2)),
            "anchor_diagonal_max":float(np.max(abs(np.diag(d)))),
            "trace":float(np.trace(d).real),
            "pair_phase_rad":[float(x) for x in phases],
            "pair_weights_percent":{p['pair']:p['percent'] for p in pairs},
            "pair_weights_sum_percent":sum(p['percent'] for p in pairs),
            "V_eigenbasis_diagonal_error":diag_error}

def check(name,actual,expected,atol):
    diff=abs(actual-expected)
    if diff>atol:
        raise AssertionError(f"{name}: {actual:.12g} vs {expected:.12g} (diff {diff:.2g})")
    return {"check":name,"observed":float(actual),"reference":float(expected),"absolute_error":float(diff),"pass":True}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--loop-json",type=Path,default=Path(__file__).with_name("lih_public_inputs.json"))
    ap.add_argument("--endpoint-npz",type=Path,help="Original endpoint wavefunctions/baseline/R_5.950000000000_F_0.011500000000.npz")
    ap.add_argument("--out",type=Path,default=Path(__file__).with_name("s13_replay.json"))
    args=ap.parse_args()
    a,b,d,j=load_public_archive(args.loop_json)
    n=a.shape[0]
    if a.shape!=(n,n) or b.shape!=(n,n) or d.shape!=(n,n):
        raise ValueError("Route / operator shape mismatch")
    v=a.conj().T@b
    nonclosure=float(np.linalg.norm(a-b,"fro")/(2*np.sqrt(n)))
    out={"source":str(args.loop_json),"m":n,
         "transport_orthogonality_error_max":float(max(np.linalg.norm(a.conj().T@a-np.eye(n)),np.linalg.norm(b.conj().T@b-np.eye(n)))),
         "nonclosure_C_correct_normalization_2sqrtm":nonclosure,
         "dipole_z":analyze_difference(a,b,d),"checks":[],
         "endpoint_operator_replay":"not supplied"}
    mu=out["dipole_z"]
    out["checks"] += [check("C",nonclosure,EXPECTED["C"],2.e-12),
      check("dipole_Frobenius",mu["frobenius"],EXPECTED["mu_frobenius_au"],2.e-11),
      check("dipole_spectral",mu["spectral"],EXPECTED["mu_spectral_au"],2.e-10),
      check("dipole_diagonal",mu["anchor_diagonal_max"],EXPECTED["mu_diagonal_au"],2.e-10),
      check("dipole_mode_23",mu["pair_weights_percent"]["2--3"],EXPECTED["mu_mode_23_percent"],1.e-5),
      check("dipole_weights_sum",mu["pair_weights_sum_percent"],100,2.e-7)]
    if args.endpoint_npz is not None:
        with np.load(args.endpoint_npz,allow_pickle=False) as z:
            energy=np.asarray(z["state_energies_Eh"],float)
            dipoles=np.asarray(z["dipole_au"])
        if len(energy)!=n or dipoles.shape[-2:]!=(n,n):
            raise ValueError(f"Endpoint mismatch: E={energy.shape}, mu={dipoles.shape}")
        mu_end=np.asarray(dipoles[2],complex)
        dd=a@mu_end@a.conj().T-b@mu_end@b.conj().T
        match=float(np.linalg.norm(dd-d,"fro"))
        out["endpoint_operator_replay"]={"endpoint_npz":str(args.endpoint_npz),
                                         "dipole_delta_archive_difference":match}
        out["checks"].append(check("archive_dipole_from_endpoint",match,0.0,5.e-8))
        h=np.diag(energy)
        dh=a@h@a.conj().T-b@h@b.conj().T
        out["hamiltonian_Eh"]=analyze_difference(a,b,dh)
        hh=out["hamiltonian_Eh"]
        out["checks"] += [
          check("hamiltonian_frobenius",hh["frobenius"],EXPECTED["hamiltonian_frobenius_Eh"],3.e-9),
          check("hamiltonian_spectral",hh["spectral"],EXPECTED["hamiltonian_spectral_Eh"],3.e-9),
          check("hamiltonian_mode_23",hh["pair_weights_percent"]["2--3"],EXPECTED["hamiltonian_mode_23_percent"],0.02)]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    path=args.out.with_suffix(".pair_weights.csv")
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["mode_pair","dipole_z_percent","Hamiltonian_percent_if_endpoint_supplied"])
        for k,val in mu["pair_weights_percent"].items():
            h_val=out.get("hamiltonian_Eh",{}).get("pair_weights_percent",{}).get(k,"")
            w.writerow([k,f"{val:.12f}",h_val])
    print(f"PUBLIC LiH S13: {len(out['checks'])} checks PASS; C={nonclosure:.12g}; ",
          f"mu spectral={mu['spectral']:.12g}; diagonal={mu['anchor_diagonal_max']:.12g};",
          f"mode(2,3)={mu['pair_weights_percent']['2--3']:.8f}%")
    if args.endpoint_npz is None:
        print("Hamiltonian contribution and endpoint dipole re-evaluation: require --endpoint-npz (available in public repository).")
    else:
        print("Hamiltonian and endpoint dipole replay checks PASS")
    print(f"Saved {args.out} and {path}")
if __name__=="__main__":main()