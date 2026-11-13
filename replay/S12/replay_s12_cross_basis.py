#!/usr/bin/env python3
"""LiH S12 replay from THREE previously optimized basis-set checkpoint sets.

Status: implementation provided, NOT executed on the original 192 files here.
Full replay requires 64 checkpoint NPZ files each for aug-cc-pVDZ (A), cc-pVTZ
(D), and aug-cc-pVTZ (T). No new SCF or CASSCF optimizations are performed.

Run --selftest for an algebraic test without PySCF. Full runs require PySCF
2.13.1, NumPy and the original wavefunctions, then write diagnostics as JSON.
The 100-rectangle complete-overlap area regression is NOT recomputed here;
that needs the historical coarse-grid loop and its saved route records.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np

BASIS = {"A":"aug-cc-pvdz", "D":"cc-pvtz", "T":"aug-cc-pvtz"}
SI_GAPS={
    "A":[0.000293183,0.0301322,0.0707053,0.249452,0.265564],
    "D":[0.00671983,0.0360389,0.109953,0.272357,0.284461],
    "T":[0.000188919,0.0284726,0.0713181,0.245451,0.261602],
}
SI_CROSS={
    "A/D":[0.321906,0.427007,0.323888,0.99999768],
    "A/T":[0.978070,0.0211953,0.978469,0.99999847],
    "D/T":[0.310217,0.438468,0.312023,0.99999927],
}

def complete_state_overlap(x: np.ndarray, ci_a: np.ndarray, ci_b: np.ndarray):
    """CAS(2e,5o), one inactive doubly occupied core, spin-paired alpha/beta.

    x = C_A[:,:6]† S_AB C_B[:,:6] in [core, active(5)] order.
    Determinant overlap d_ac=x_00*x_ac-x_a0*x_0c.
    Includes BOTH alpha and beta sectors and the optimized core orbital.
    """
    if x.shape !=(6,6) or ci_a.shape!=(4,5,5) or ci_b.shape!=(4,5,5):
        raise ValueError(f"Bad shapes: MO={x.shape}; CI-A={ci_a.shape}; CI-B={ci_b.shape}")
    d=x[0,0]*x[1:,1:]-np.outer(x[1:,0],x[0,1:])
    state=np.einsum('iab,jcd,ac,bd->ij',ci_a.conj(),ci_b,d,d,optimize=True)
    return state

def algebraic_selftest():
    rng=np.random.default_rng(413)
    z=rng.normal(size=(25,4))+1j*rng.normal(size=(25,4))
    q,_=np.linalg.qr(z)
    ci=q.T.reshape(4,5,5)
    M=complete_state_overlap(np.eye(6),ci,ci)
    assert np.linalg.norm(M-np.eye(4))<1.e-12
    v=rng.normal(size=(5,5))
    x=np.eye(6);x[1:,1:]=v
    M1=complete_state_overlap(x,ci,ci)
    # Fermionic four-electron state overlap is covariant under swapping inputs.
    M2=complete_state_overlap(x.T,ci,ci)
    assert np.linalg.norm(M1-M2.conj().T)<1.e-11
    print('S12 complete four-electron overlap algebraic selftest PASS (synthetic inputs; NOT molecular replay).')

def checkpoint(directory:Path, r:float, field:float):
    filename=f'R_{r:.12f}_F_{field:.12f}.npz'
    exact=directory/filename
    if exact.is_file():return exact
    found=list(directory.rglob(filename))
    if len(found)!=1: raise FileNotFoundError(f'{filename}: expected 1 match under {directory}, found {len(found)}')
    return found[0]

def load(path):
    with np.load(path,allow_pickle=False) as d:
        meta=json.loads(str(d['metadata_json'].item()))
        ci=np.stack([d[f'ci_root_{i}'] for i in range(4)])
        mo=d['mo_coeff'].copy()
        energies=np.asarray(d['state_energies_Eh'],float)
        probe=np.asarray(d['five_root_probe_energies_Eh'],float)
    if int(meta.get('ncore',-1))!=1 or int(meta.get('ncas',-1))!=5:
        raise ValueError(f'{path}: wrong core/active-space dimensions')
    return {'metadata':meta,'ci':ci,'mo':mo,'energies':energies,'probe':probe}

def molecular(r,basis):
    from pyscf import gto
    return gto.M(atom=[('Li',(0,0,-r/2)),('H',(0,0,r/2))],unit='Angstrom',
                 basis=basis,charge=0,spin=0,symmetry='C2v',verbose=0)

def reference_vertices():
    # Same 64-point closed rectangular boundary used in the archived baseline.
    r0,r1,f0,f1=5.8,5.95,0.0105,0.0115
    n=16
    sides=[[(r0+(r1-r0)*k/n,f0) for k in range(n)],
           [(r1,f0+(f1-f0)*k/n) for k in range(n)],
           [(r1-(r1-r0)*k/n,f1) for k in range(n)],
           [(r0,f1-(f1-f0)*k/n) for k in range(n)]]
    return [(round(r,12),round(f,12)) for side in sides for r,f in side]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest',action='store_true')
    ap.add_argument('--A',type=Path,help='Directory containing aug-cc-pVDZ checkpoint NPZ files')
    ap.add_argument('--D',type=Path,help='Directory containing cc-pVTZ checkpoint NPZ files')
    ap.add_argument('--T',type=Path,help='Directory containing aug-cc-pVTZ checkpoint NPZ files')
    ap.add_argument('--output',type=Path,default=Path('s12_replayed_from_checkpoints.json'))
    args=ap.parse_args()
    if args.selftest:
        algebraic_selftest();return
    if not (args.A and args.D and args.T):
        ap.error('For molecular audit supply --A, --D, --T; or use --selftest')
    try:
        from pyscf import gto  # noqa: F401
    except ImportError as e:
        raise SystemExit('Full cross-basis molecular replay requires PySCF (not installed here).') from e
    roots={'A':args.A,'D':args.D,'T':args.T}
    vertices=reference_vertices();gap_stats={};r2_stats={};data={};molcache={}
    for label,dirname in roots.items():
        records=[];gaps=[];r2=[]
        for idx,(r,f) in enumerate(vertices):
            path=checkpoint(dirname,r,f);s=load(path)
            meta=s['metadata']
            if abs(float(meta['R_angstrom'])-r)>1.e-9 or abs(float(meta['field_z_au'])-f)>1.e-10:
                raise ValueError(f'{path}: coordinate differs from requested common grid')
            if str(meta['basis']).lower()!=BASIS[label]:
                raise ValueError(f'{path}: unexpected basis {meta["basis"]}')
            if r not in molcache:molcache[r]={}
            if label not in molcache[r]:molcache[r][label]=molecular(r,BASIS[label])
            mol=molcache[r][label]
            if s['mo'].shape[0]!=mol.nao_nr():
                raise ValueError(f'{path}: molecular-orbital AO dimension mismatch')
            energy=s['energies'];probe=s['probe']
            gaps.append([energy[3]-energy[2],probe[4]-energy[3],energy[3]-energy[0]])
            if idx in (0,16,32,48):
                with mol.with_common_orig((0.,0.,0.)):
                    integral=mol.intor_symmetric('int1e_r2')
                c=s['mo'][:,1:6]
                r2.append(float(np.trace(c.conj().T@integral@c).real/5))
            records.append(s)
        gg=np.asarray(gaps)
        gap_stats[label]=dict(zip(['min_D34_Eh','max_D34_Eh','min_external_Eh','min_width_Eh','max_width_Eh'],
                         map(float,[gg[:,0].min(),gg[:,0].max(),gg[:,1].min(),gg[:,2].min(),gg[:,2].max()])))
        r2_stats[label]={'min_corner_active_r2_bohr2':min(r2),'max_corner_active_r2_bohr2':max(r2)}
        data[label]=records
    cross={}
    for first,second in [('A','D'),('A','T'),('D','T')]:
        singular=[];leak=[];active=[];core=[]
        for i,(r,f) in enumerate(vertices):
            mol1=molcache[r][first];mol2=molcache[r][second]
            ma=data[first][i];mb=data[second][i]
            sab=gto.intor_cross('int1e_ovlp',mol1,mol2)
            x=ma['mo'][:,:6].conj().T@sab@mb['mo'][:,:6]
            M=complete_state_overlap(x,ma['ci'],mb['ci'])
            sig=np.linalg.svd(M,compute_uv=False)
            singular.append(float(sig.min()))
            leak.append(float(1-np.mean(sig**2)))
            active.append(float(np.linalg.svd(x[1:,1:],compute_uv=False).min()))
            core.append(float(abs(x[0,0])))
        cross[f'{first}/{second}']={
          'minimum_state_sigma':min(singular),'maximum_state_leakage':max(leak),
          'minimum_active_sigma':min(active),'minimum_core_overlap':min(core)}
    result={'status':'CALCULATED_FROM_ORIGINAL_CHECKPOINTS','vertices':len(vertices),
            'wavefunctions':3*len(vertices),'gap_stats':gap_stats,
            'cross_basis_stats':cross,'active_r2_bohr2':r2_stats,
            'note':'Area-law regression requires the historical local/global loop data; not reconstructed here.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    print('Historical SI comparison values are embedded as SI_GAPS and SI_CROSS for separate assessment; this script does not tune outputs to them.')
if __name__=='__main__':main()