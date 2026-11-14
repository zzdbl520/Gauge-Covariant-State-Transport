#!/usr/bin/env python3
"""SI Fig. S2 from 100 archived active-only LiH data points (plot-rounded to 8 significant digits).
Source: zzdbl520/electronic-state-identity/data/revision-2026-10-21/analysis/lih_100_locator_plaquettes.csv
When the full CSV is available locally, use --csv to read all original double-precision values.
"""
import argparse,csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
A=np.array([1.5,1.5,1.125,1.125,1.125,1.125,1,1,1,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.375,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,2,1.5,1.5,1,1,1,0.5,0.5,0.5,0.5],float)
C=np.array([3.6847048,3.6275925,2.7904194,2.744409,2.7356745,2.6962257,2.4742852,2.4349399,2.3980834,1.8825581,1.8746899,1.8497389,1.8430577,1.8385246,1.835993,1.8132963,1.8101819,1.8097793,1.8087903,1.7856171,1.7834231,1.246626,1.2428511,1.2345086,1.2265653,1.221491,1.2150067,1.2139304,1.2074036,1.1972749,1.1967144,1.189661,1.1817332,1.2653913,0.95500425,0.94495867,0.93728861,0.92888703,0.92864364,0.92462738,0.91347993,0.91344104,0.91082196,0.91059736,0.89983482,0.89907553,0.89771377,0.89745856,0.88875951,0.88521593,0.64223159,0.63809144,0.63007815,0.62673263,0.6238789,0.62200396,0.61865859,0.61562725,0.61344618,0.61198821,0.61125101,0.61096014,0.60532241,0.60355275,0.60325958,0.60252839,0.60243623,0.60224552,0.59559798,0.59435273,0.59380446,0.59367854,0.58851096,0.5868962,0.32402947,0.31787273,0.31447668,0.31196165,0.30916445,0.30777968,0.3064223,0.30403218,0.30348792,0.30319102,0.29951761,0.29925342,0.29881379,0.29583442,0.29474902,0.29243366,4.8803729,3.6940723,3.6253129,2.4910112,2.4351821,2.399592,1.2630423,1.2294175,1.2070356,1.1937227],float)
P=np.array([True]*90+[False]*10)
assert len(A)==len(C)==len(P)==100 and sum(P)==90

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--csv',type=Path,help='optional exact original CSV');ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);args=ap.parse_args()
    a,c,p,sel=A,C,P,3.6847048
    if args.csv is not None:
        rows=list(csv.DictReader(args.csv.open(encoding='utf-8')))
        assert len(rows)==100
        a=np.array([float(x['area'])*1.e4 for x in rows]);c=np.array([float(x['C'])*1.e4 for x in rows]);p=np.array([x['fidelity_pass_active_only']=='True' for x in rows]);sel=float(next(x['C'] for x in rows if x['selected']=='True'))*1.e4
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.0,'axes.labelsize':9.6,'axes.titlesize':10.8,'legend.fontsize':7.3,'xtick.direction':'in','ytick.direction':'in','pdf.fonttype':42})
    fig,axs=plt.subplots(1,2,figsize=(7.8,3.25),layout='constrained')
    blue='#176488';orange='#BD6530'
    ax=axs[0];ax.set_title('a  Initial grid: 100 rectangles',loc='left',fontweight='bold',pad=11)
    ax.scatter(a[~p],c[~p],s=25,facecolors='none',edgecolors='0.65',label='Above fidelity limits')
    ax.scatter(a[p],c[p],s=25,facecolors='none',edgecolors=blue,label='Within fidelity limits')
    selected_index=np.argmin(abs(c-sel));ax.scatter(a[selected_index],sel,s=115,marker='*',color=orange,zorder=5,label='Largest value meeting all criteria')
    ax.set_xlabel(r'Area ($10^{-4}$ $\AA$ $\times$ a.u. field)');ax.set_ylabel(r'Active-electron $C_{RF}$ ($10^{-4}$)');ax.set_xlim(.03,2.08)
    ax.legend(frameon=False,loc='upper left',fontsize=7.2,handletextpad=.6)
    ax=axs[1];ax.set_title('b  Selection in the full distribution',loc='left',fontweight='bold',pad=11)
    for vals,color,label in [(c,'0.4','All 100'),(c[p],blue,'90 within fidelity limits')]:
        v=np.sort(vals);ax.step(v,np.arange(1,len(v)+1)/len(v),where='post',color=color,lw=1.6,label=label)
    ax.axvline(1,color='0.45',ls=':',lw=1.6,label='Selection threshold')
    ax.axvline(sel,color=orange,ls='--',lw=1.6,label='Selected value')
    ax.set_xlim(.15,5.08);ax.set_ylim(0,1.045)
    ax.set_xlabel(r'Active-electron $C_{RF}$ ($10^{-4}$)');ax.set_ylabel('Cumulative fraction')
    legend=ax.legend(frameon=False,fontsize=7.4,loc='lower left',bbox_to_anchor=(.235,.065),borderaxespad=0,handlelength=2.1,handletextpad=.65,labelspacing=.45)
    fig.canvas.draw()
    bb=legend.get_window_extent(fig.canvas.get_renderer()).transformed(ax.transData.inverted())
    assert bb.x0>1.1 and bb.x1<sel-.12,(bb.x0,bb.x1,sel)
    for ax in axs:
        ax.tick_params(which='major',direction='in',length=5,width=1.1)
        ax.tick_params(which='minor',direction='in',length=3,width=.9)
        for spine in ax.spines.values():spine.set_linewidth(1)
    args.out.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.out/'FigureS2_LiH.pdf',bbox_inches='tight')
    fig.savefig(args.out/'FigureS2_LiH_600dpi.png',dpi=600,bbox_inches='tight')
    print('Legend in data units:',(bb.x0,bb.x1),'selected x:',sel)
if __name__=='__main__':main()