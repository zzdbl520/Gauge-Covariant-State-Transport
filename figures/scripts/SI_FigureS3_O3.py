#!/usr/bin/env python3
"""Replot JCTC SI Figure S3 from the archived O3 Gate4B numerical data.

Only presentation changes: simplified/explicit major ticks, larger tick labels,
inward ticks and removal of the in-plot shaded-range explanation. The shaded
range is explained by the manuscript's existing Figure S3 caption.

Source: zzdbl520/electronic-state-identity, revision 2026-10-21,
records/O3/source_data/gate4B/O3_gate4B_scaling.csv
"""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter, LogLocator

HERE = Path(__file__).resolve().parent
with (HERE/'O3_gate4B_scaling_original.csv').open(newline='') as fp:
    rows = list(csv.DictReader(fp))

def get(direction):
    rr = sorted((r for r in rows if r['direction'] == direction), key=lambda r: float(r['h']))
    return {k: np.array([float(r[k]) for r in rr]) for k in
            ('h', 'C_minus', 'C_plus', 'eta_edge_min', 'lambda_nuclear_max')}

stretch = get('delta_r')
bend = get('theta')
assert len(stretch['h']) == len(bend['h']) == 4

BLUE = '#176488'
ORANGE = '#bd6530'
GREY = '#dfdfdf'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'pdf.fonttype': 42, 'ps.fonttype': 42,
    'font.size': 13.5, 'axes.labelsize': 16, 'axes.titlesize': 17,
    'legend.fontsize': 12.5, 'axes.linewidth': 1.45,
    'xtick.labelsize': 15.0, 'ytick.labelsize': 15.0,
    'xtick.direction': 'in', 'ytick.direction': 'in',
})
fig, axs = plt.subplots(2, 2, figsize=(10.8, 7.9))
fig.subplots_adjust(left=.105, right=.985, bottom=.095, top=.945, wspace=.31, hspace=.40)

for ax in axs.flat:
    ax.tick_params(which='major', direction='in', length=8, width=1.5, pad=7, top=True, right=True)
    ax.tick_params(which='minor', direction='in', length=3.2, width=.8, top=True, right=True)
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_linewidth(1.45)

def short_log_x(ax, values, labels):
    ax.set_xscale('log')
    ax.xaxis.set_major_locator(FixedLocator(values))
    ax.xaxis.set_major_formatter(FixedFormatter(labels))
    ax.xaxis.set_minor_locator(LogLocator(base=10., subs=np.arange(2,10)*.1))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(values[0]*.80, values[-1]*1.25)

def y_ticks(ax, vals, labels, ylim=None):
    ax.yaxis.set_major_locator(FixedLocator(vals))
    ax.yaxis.set_major_formatter(FixedFormatter(labels))
    if ylim is not None:
        ax.set_ylim(*ylim)

# (a) Antisymmetric stretch: x in milliangstroms; y in units of 1e-5.
ax=axs[0,0]
x=stretch['h']*1000
for k,marker,color,label in [('C_minus','s',BLUE,'Negative'),('C_plus','o',ORANGE,'Positive')]:
    ax.plot(x, stretch[k]*1e5, marker=marker, color=color, lw=2.1, ms=7.5, label=label)
short_log_x(ax,[1.25,2.5,5,10],['1.25','2.5','5','10'])
y_ticks(ax,[1,2,3,4,5],['1','2','3','4','5'],(.80,5.75))
ax.set_xlabel(r'Absolute step ($10^{-3}$ Å)', labelpad=8)
ax.set_ylabel(r'$\mathcal{C}_{qp}$ ($10^{-5}$)', labelpad=8)
ax.set_title('a  Antisymmetric stretch',loc='left',weight='bold',pad=12)
ax.legend(loc='upper left',frameon=False,borderaxespad=.55)

# (b) Equal-bond bend: x in 0.01 degrees; y on log scale.
ax=axs[0,1]
x=bend['h']*100
cvals=np.r_[bend['C_minus'],bend['C_plus']]
ax.axhspan(float(cvals.min()),float(cvals.max()),facecolor=GREY,alpha=.55,zorder=0)
for k,marker,color,label in [('C_minus','s',BLUE,'Negative'),('C_plus','o',ORANGE,'Positive')]:
    ax.plot(x,bend[k],marker=marker,color=color,lw=2.1,ms=7.5,label=label,zorder=3)
short_log_x(ax,[2.5,5,10,20],['2.5','5','10','20'])
ax.set_yscale('log')
y_ticks(ax,[1e-9,1e-8],[r'$10^{-9}$',r'$10^{-8}$'],(6e-10,7e-8))
ax.set_xlabel(r'Absolute step ($10^{-2}$ degree)',labelpad=8)
ax.set_ylabel(r'$\mathcal{C}_{qp}$',labelpad=8)
ax.set_title('b  Equal-bond bend',loc='left',weight='bold',pad=12)
ax.legend(loc='lower right',frameon=True,facecolor='white',edgecolor='none',framealpha=.95,borderpad=.30,labelspacing=.30)

# (c), (d) normalized steps: tick fractions eliminate awkward log tick clutter.
for j,(title,field) in enumerate([('c  Nuclear-edge leakage','lambda_nuclear_max'),
                                 ('d  Worst singular value','eta_edge_min')]):
    ax=axs[1,j]
    for src,col,lab in [(stretch,BLUE,'Stretch'),(bend,ORANGE,'Bend')]:
        xx=src['h']/src['h'].max()
        ax.plot(xx,src[field],'-o',color=col,lw=2.1,ms=7.3,label=lab,zorder=4)
    short_log_x(ax,[.125,.25,.5,1.0],[r'$1/8$',r'$1/4$',r'$1/2$','1'])
    ax.set_xlabel('Step / largest step',labelpad=8)
    ax.set_title(title,loc='left',weight='bold',pad=12)
    ax.legend(loc='lower right' if j==0 else 'lower left',frameon=False)
    if j==0:
        ax.set_yscale('log')
        y_ticks(ax,[1e-4,1e-3,1e-2],[r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$'],(1.5e-5,1.4e-2))
        ax.set_ylabel('Nuclear-edge leakage',labelpad=8)
        ax.axhline(0.01,color='.42',ls=':',lw=1.6,zorder=1)
    else:
        y_ticks(ax,[.996,.997,.998,.999],[f'{t:.3f}' for t in [.996,.997,.998,.999]],(.9954,.99978))
        ax.set_ylabel(r'$\eta_{\min}$',labelpad=8)

for ext in ('pdf','svg','png'):
    fig.savefig(HERE/f'FigureS3_O3.{ext}',dpi=600,facecolor='white')
plt.close(fig)
print('Wrote vector PDF/SVG and 600 dpi PNG from 8 O3 source records')