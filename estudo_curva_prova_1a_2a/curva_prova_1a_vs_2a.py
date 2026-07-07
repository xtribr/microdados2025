#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Curva da PROVA: Função de Informação do Teste (TIF) — 1ª aplicação × 2ª aplicação (reaplicação/PPL).
As duas provas são equalizadas para a MESMA escala TRI; comparar onde cada uma 'mede' melhor.
TRI 3PL D=1. Fonte: ITENS_PROVA_2025 (caderno Azul de cada aplicação). Só itens; não usa notas de PPL."""
import csv, json, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D

BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"
ITENS=f"{BASE}/DADOS/ITENS_PROVA_2025.csv"
OUT=f"{BASE}/estudo_curva_prova_1a_2a"
P1={'CN':'1483','CH':'1447','LC':'1459','MT':'1471'}   # 1a aplicacao Azul
P2={'CN':'1569','CH':'1539','LC':'1549','MT':'1559'}   # 2a aplicacao (reaplicacao/PPL) Azul
AREAS=['CN','CH','LC','MT']
ANOME={'CN':'Ciências da Natureza','CH':'Ciências Humanas','LC':'Linguagens','MT':'Matemática'}

def load(provas):
    par={a:[] for a in AREAS}
    with open(ITENS,encoding='latin-1',newline='') as f:
        for r in csv.DictReader(f,delimiter=';'):
            a=r['SG_AREA'].strip(); cp=r['CO_PROVA'].strip()
            if provas.get(a)!=cp: continue
            if str(r['IN_ITEM_ABAN']).strip()=='1': continue
            if a=='LC' and r.get('TP_LINGUA','').strip()=='1': continue   # LC = 40 comuns + 5 inglês
            par[a].append((float(r['NU_PARAM_A'].replace(',','.')),
                           float(r['NU_PARAM_B'].replace(',','.')),
                           float(r['NU_PARAM_C'].replace(',','.'))))
    return par
PAR1=load(P1); PAR2=load(P2)
theta=np.arange(-3.0,4.0001,0.005); nota=100*theta+500
def tif(par):
    I=np.zeros_like(theta)
    for a,b,c in par:
        P=c+(1-c)/(1+np.exp(-a*(theta-b)))
        I+=a*a*((P-c)/(1-c))**2*((1-P)/P)
    return I
TIF1={a:tif(PAR1[a]) for a in AREAS}
TIF2={a:tif(PAR2[a]) for a in AREAS}
def bmean(par): return np.mean([100*b+500 for _,b,_ in par])

C1="#1E6FB8"; C2="#FF4A2D"  # 1a azul, 2a laranja
plt.rcParams.update({'font.size':10})
fig,axes=plt.subplots(2,2,figsize=(13.2,9),dpi=150); fig.patch.set_facecolor('white')
for ax,a in zip(axes.flat,AREAS):
    ax.set_facecolor('white')
    ax.plot(nota,TIF1[a],color=C1,lw=2.6,zorder=4)
    ax.fill_between(nota,TIF1[a],color=C1,alpha=0.06,zorder=1)
    ax.plot(nota,TIF2[a],color=C2,lw=2.6,zorder=4,ls=(0,(5,2)))
    ax.fill_between(nota,TIF2[a],color=C2,alpha=0.06,zorder=1)
    p1=nota[int(np.argmax(TIF1[a]))]; p2=nota[int(np.argmax(TIF2[a]))]
    ax.axvline(p1,color=C1,ls=':',lw=1,zorder=3); ax.axvline(p2,color=C2,ls=':',lw=1,zorder=3)
    ax.set_title(ANOME[a],fontsize=13,weight='bold',color='#1F4E78',pad=8)
    ax.set_xlim(300,860); ax.set_ylim(0,max(TIF1[a].max(),TIF2[a].max())*1.20)
    ax.set_xlabel("Nota TRI (escala ENEM)",fontsize=9.5); ax.set_ylabel("Informação do teste  I(θ)",fontsize=9.5)
    ax.xaxis.set_major_locator(MultipleLocator(100))
    for s in ['top','right']: ax.spines[s].set_visible(False)
    ax.grid(axis='x',color='#EEE',lw=0.7); ax.set_axisbelow(True)
    ax.text(0.025,0.96,f"pico 1ª ≈ {p1:.0f}   ·   pico 2ª ≈ {p2:.0f}\ndificuldade média (TRI):  1ª {bmean(PAR1[a]):.0f}  ·  2ª {bmean(PAR2[a]):.0f}",
            transform=ax.transAxes,va='top',ha='left',fontsize=8.3,color='#444',
            bbox=dict(boxstyle='round,pad=0.35',fc='#F7F7F7',ec='#DDD',lw=0.6))

handles=[Line2D([0],[0],color=C1,lw=2.8,label='1ª aplicação (prova regular)'),
         Line2D([0],[0],color=C2,lw=2.8,ls=(0,(5,2)),label='2ª aplicação (reaplicação/PPL)')]
fig.legend(handles=handles,loc='lower center',ncol=2,frameon=False,fontsize=10.5,bbox_to_anchor=(0.5,0.052))
fig.suptitle("ENEM 2025 — a prova mede igual? Função de Informação: 1ª × 2ª aplicação",fontsize=16.5,weight='bold',color='#1F4E78',y=0.985)
fig.text(0.5,0.945,"As duas provas são equalizadas para a mesma escala TRI. A curva mostra em que faixa cada prova mede com mais precisão.",
         ha='center',fontsize=10,color='#555')
fig.text(0.5,0.030,"Fonte: Microdados ENEM 2025 (INEP) — parâmetros TRI dos itens (caderno Azul). A 2ª aplicação é a prova de reaplicação/PPL (mesma prova para os dois); o INEP não separa PPL de reaplicação.",
         ha='center',fontsize=7.6,color='#888')
fig.text(0.5,0.010,"contato@xtri.online    ·    xtri.online    ·    estudo por Alexandre Emerson Melo de Araújo",
         ha='center',fontsize=9.2,color='#1F4E78',weight='bold')
fig.tight_layout(rect=[0,0.075,1,0.93])
try:
    from PIL import Image
    lg=Image.open(f"{BASE}/logo_xtri_marca_real.png").convert("RGBA")
    w0=360; lg=lg.resize((w0,int(w0*lg.size[1]/lg.size[0])))
    arr=np.asarray(lg).astype(float)/255.0; arr[...,3]*=0.07
    fw,fh=(fig.get_size_inches()*fig.dpi)
    fig.figimage(arr,xo=(fw-arr.shape[1])/2.0,yo=(fh-arr.shape[0])/2.0,zorder=10)
except Exception as e: print("wm:",e)
out=f"{OUT}/CURVA_prova_1a_vs_2a_TIF.png"
fig.savefig(out,facecolor='white'); print("OK ->",out)
for a in AREAS:
    print(f"{a}: 1ª pico {nota[int(np.argmax(TIF1[a]))]:.0f} (Imax {TIF1[a].max():.1f}, b̄ {bmean(PAR1[a]):.0f}) | 2ª pico {nota[int(np.argmax(TIF2[a]))]:.0f} (Imax {TIF2[a].max():.1f}, b̄ {bmean(PAR2[a]):.0f})")
