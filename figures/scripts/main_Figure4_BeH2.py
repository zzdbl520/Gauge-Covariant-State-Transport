#!/usr/bin/env python3
"""Reproducible two-panel BeH2 figure for JCTC R2.

Panel (a): original 21 SA3 points from
  zz dbl520/electronic-state-identity (2026-10-21),
  data/revision-2026-10-21/records/BeH2/source_data/B3R/B3R_branch_map.csv
  Columns: lambda_bohr; protocol=SA3; delta_e_absolute.
Panel (b): Table S5 of final SI, maximum edge leakage for rank-matched
  SA3/SA4 subspaces on six-point comparison grid.

Not a new CASSCF calculation. No synthetic/approximated data used.

Run: python plot_BeH2_JCTC_R2.py
Produces PNG 600 dpi, PDF, and SVG in the same directory.
"""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LogLocator, LogFormatterMathtext

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'BeH2_B3R_SA3_21points.csv'
LEAK = np.array([0.083069, 0.083788, 0.106221], dtype=float)
LABELS = ['Constrained\nCAS(6e,6o)', 'Unconstrained\nCAS(6e,6o)', 'Valence\nCAS(4e,6o)']
COLORS = ['#c0662f', '#24688f', '#657b66']

with SOURCE.open(newline='', encoding='utf-8') as fp:
    rr = list(csv.DictReader(fp))
xy = sorted([(float(row['lambda_bohr']), float(row['delta_e_absolute'])) for row in rr])
lam = np.array([x for x, _ in xy]); E = np.array([y for _, y in xy])
assert len(xy) == 21
assert abs(lam[0] - 2.5212) < 1e-10 and abs(lam[-1] - 2.5222) < 1e-10
assert np.allclose(np.diff(lam), 5e-5, atol=1e-10)
assert np.isclose(E[np.where(np.isclose(lam, 2.52195, atol=1e-10))[0][0]], 0.005619197662738884, atol=5e-12)

plt.rcParams.update({
 'font.family':'DejaVu Sans', 'mathtext.fontset':'dejavusans',
 'font.size':11, 'axes.titlesize':14.5, 'axes.titleweight':'bold',
 'axes.labelsize':12, 'xtick.labelsize':10.5, 'ytick.labelsize':10.5,
 'pdf.fonttype':42, 'ps.fonttype':42,
 'axes.linewidth':1.1, 'savefig.facecolor':'white',
})

fig, (a,b)=plt.subplots(1,2,figsize=(11.6,4.6),gridspec_kw={'width_ratios':[1,1]})
fig.subplots_adjust(left=.075,right=.98,bottom=.19,top=.85,wspace=.24)

# (a): Historical SA3 scan (not an interpolated/idealized step curve)
a.plot(lam, E, '-o', lw=1.75, markersize=4.4, color='#19678b', zorder=3)
a.set_yscale('log'); a.set_xlim(2.52115,2.52225); a.set_ylim(1e-8,1e-2)
a.set_xticks(np.arange(2.5212,2.52221,0.0002))
a.set_xticklabels([f'{v:.4f}' for v in np.arange(2.5212,2.52221,.0002)])
a.yaxis.set_major_locator(LogLocator(base=10)); a.yaxis.set_major_formatter(LogFormatterMathtext(base=10))
a.set_xlabel(r'$\lambda$ (Bohr)'); a.set_ylabel(r'$|\Delta\bar{E}|$ ($E_h$)')
a.set_title('a  SA3 scans in opposite directions',loc='left',pad=14)
a.text(.035,.11,r'21 points; $\Delta\lambda=5\times10^{-5}$ Bohr',transform=a.transAxes,fontsize=9.8)

# (b): Table S5 numerical values; the three labels refer to orbital constraints
x=np.arange(3)
for i,val in enumerate(LEAK):
    b.bar(i,val,width=.64,color=COLORS[i],zorder=2)
    b.text(i,val+.0022,f'{val:.5f}',ha='center',va='bottom',fontsize=10.3)
b.axhline(.01,ls='--',lw=1.6,color='#545454',zorder=4,
          label='Acceptance threshold: 0.01')
b.set_xticks(x, LABELS); b.set_ylim(0,.128);b.set_xlim(-.46,2.46)
b.yaxis.set_major_locator(MultipleLocator(.02))
b.set_ylabel('Maximum edge leakage')
b.set_title('b  SA3/SA4 subspace fidelity',loc='left',pad=14)
b.legend(loc='upper left',frameon=False,fontsize=9.7,handlelength=2.2)

for ax in (a,b):
    ax.tick_params(which='both',direction='in',width=1.0,top=False,right=False)
    ax.tick_params(which='major',length=5)
    ax.spines['top'].set_visible(True);ax.spines['right'].set_visible(True)

for ext in ('png','pdf','svg'):
    fig.savefig(ROOT / f'BeH2_Figure4_JCTC_R2.{ext}', dpi=600 if ext=='png' else 300,
                facecolor='white', bbox_inches='tight',pad_inches=.14)
plt.close(fig)
print(f'Loaded {len(lam)} original SA3 points; at lambda=2.52195, DeltaE={E[np.argmin(abs(lam-2.52195))]:.14g} Eh')
print('Saved 600-dpi PNG and vector PDF/SVG')