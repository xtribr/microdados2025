#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E1 — Funcao de Informacao do Teste x rede de ensino (ENEM 2025).
TRI: I(theta) e SE(theta) por area (params 3PL caderno Azul regular, D=1).
Perfil: densidade da nota por rede (RESULTADOS, mesma linha) sobreposta a regua de precisao.
Trava: so RESULTADOS+ITENS; nada de PARTICIPANTES."""
import csv, json, math
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

SP   = "/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/eea62195-d399-4434-8338-95d5d92b8bac/scratchpad"
ITENS= "/Volumes/Kingston 1/microdados_enem_2025/DADOS/ITENS_PROVA_2025.csv"
PROVAS={'CN':'1483','CH':'1447','LC':'1459','MT':'1471'}
AREAS=['CN','CH','LC','MT']
ANOME={'CN':'Ciências da Natureza','CH':'Ciências Humanas','LC':'Linguagens','MT':'Matemática'}

# ---- 1) parametros dos itens (Azul regular; dropar anulados; LC = 40 comuns + 5 ingles) ----
def fnum(s): return float(str(s).strip().replace(',','.'))
params={a:[] for a in AREAS}
with open(ITENS, encoding='latin-1', newline='') as f:
    for r in csv.DictReader(f, delimiter=';'):
        if r.get('TX_COR','').strip().upper()!='AZUL': continue
        a=r['SG_AREA'].strip()
        if PROVAS.get(a)!=r['CO_PROVA'].strip(): continue
        if str(r['IN_ITEM_ABAN']).strip()=='1': continue
        if a=='LC':
            ling=r.get('TP_LINGUA','').strip()
            if ling=='1':  # espanhol -> fora (usamos ingles, lingua majoritaria)
                continue
        params[a].append((fnum(r['NU_PARAM_A']), fnum(r['NU_PARAM_B']), fnum(r['NU_PARAM_C'])))
for a in AREAS: print(a, 'itens no teste:', len(params[a]))

# ---- 2) funcao de informacao I(theta) (3PL, D=1) ----
theta=np.arange(-3.0,4.0001,0.005)
def info(area):
    I=np.zeros_like(theta)
    for a,b,c in params[area]:
        P=c+(1-c)/(1+np.exp(-a*(theta-b)))
        I+=a*a*((P-c)/(1-c))**2*((1-P)/P)
    return I
INFO={a:info(a) for a in AREAS}
nota=100*theta+500
def se_points_at(area, nota_val):
    th=(nota_val-500)/100.0
    Ii=np.interp(th, theta, INFO[area])
    return 100.0/math.sqrt(Ii) if Ii>0 else float('nan')

# ---- 3) densidade da nota por rede ----
H=json.load(open(f"{SP}/hist_nota_rede.json"))
binw=H['binw']; nb=H['nb']
centers=(np.arange(nb)+0.5)*binw
REDES=[('2','Estadual','#5B9BD5'),('1','Federal','#ED7D31'),('4','Privada','#4CAF50')]
def density(area, rede):
    c=np.array(H['hist'][area][rede], dtype=float); tot=c.sum()
    return c/(tot*binw) if tot>0 else c

# ---- 4) figura principal 2x2 ----
plt.rcParams.update({'font.size':10,'axes.edgecolor':'#cccccc'})
fig,axes=plt.subplots(2,2,figsize=(13.2,9.0),dpi=150)
fig.patch.set_facecolor('white')
hero={}
for ax,area in zip(axes.flat, AREAS):
    ax.set_facecolor('white')
    # densidade por rede (eixo direito)
    ax2=ax.twinx()
    for code,name,col in REDES:
        d=density(area,code)
        ax2.fill_between(centers, d, color=col, alpha=0.16, zorder=1)
        ax2.plot(centers, d, color=col, lw=1.6, label=name, zorder=2)
    ax2.set_ylim(0, max(density(area,'2').max(),density(area,'4').max())*1.5)
    ax2.set_yticks([])
    # curva de informacao (eixo esquerdo)
    ax.plot(nota, INFO[area], color='#2C3E50', lw=2.6, zorder=5)
    ax.fill_between(nota, INFO[area], color='#2C3E50', alpha=0.05, zorder=0)
    pico=nota[int(np.argmax(INFO[area]))]
    ax.axvline(pico, color='#2C3E50', ls=':', lw=1.2, zorder=4)
    ax.set_zorder(ax2.get_zorder()+1); ax.patch.set_visible(False)
    # medianas estadual e privada
    med_e=H['medianas'][area]['2']; med_p=H['medianas'][area]['4']
    for med,col in [(med_e,'#5B9BD5'),(med_p,'#4CAF50')]:
        ax.axvline(med, color=col, ls='--', lw=1.6, zorder=6)
    # hero: SE em pontos nas medianas
    se_e=se_points_at(area,med_e); se_p=se_points_at(area,med_p)
    hero[area]=dict(pico=round(float(pico)), med_e=med_e, med_p=med_p, se_e=round(se_e,1), se_p=round(se_p,1))
    ax.set_xlim(300,850)
    ax.set_ylim(0, INFO[area].max()*1.18)
    ax.set_title(f"{ANOME[area]}", fontsize=13, weight='bold', color='#1F4E78', pad=22)
    ax.annotate(f"pico de precisão ≈ {round(float(pico))}", xy=(pico,INFO[area].max()),
                xytext=(0,6), textcoords='offset points', ha='center', fontsize=8.5, color='#2C3E50')
    ax.text(0.015,0.97,f"estadual {med_e:.0f} → erro ±{se_e:.0f} pts\nprivada {med_p:.0f} → erro ±{se_p:.0f} pts",
            transform=ax.transAxes, va='top', ha='left', fontsize=8.4, color='#444',
            bbox=dict(boxstyle='round,pad=0.35', fc='#F7F7F7', ec='#DDD', lw=0.6))
    ax.set_ylabel("Informação do teste  I(θ)", fontsize=9.5, color='#2C3E50')
    ax.set_xlabel("Nota TRI (escala ENEM)", fontsize=9.5)
    ax.xaxis.set_major_locator(MultipleLocator(100))
    for s in ['top']: ax.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
    ax.grid(axis='x', color='#EEE', lw=0.7); ax.set_axisbelow(True)

# legenda unica (redes) + curva
from matplotlib.lines import Line2D
handles=[Line2D([0],[0],color='#2C3E50',lw=2.6,label='Informação do teste I(θ) — onde a prova "enxerga" com nitidez')]
handles+=[Line2D([0],[0],color=c,lw=6,alpha=0.5,label=f"densidade de alunos — {n}") for _,n,c in REDES]
fig.legend(handles=handles, loc='lower center', ncol=2, frameon=False, fontsize=9.5, bbox_to_anchor=(0.5,0.035))
fig.suptitle("ENEM 2025 — a prova mede melhor quem? Função de Informação × rede de ensino",
             fontsize=16.5, weight='bold', color='#1F4E78', y=0.99)
fig.text(0.5,0.945,"O pico de informação (medida mais precisa) cai onde se concentram privada e federal; a maioria da rede estadual fica na cauda, onde o erro de medida é maior.",
         ha='center', fontsize=10, color='#555')
fig.text(0.5,0.006,"Fonte: Microdados ENEM 2025 (INEP) · caderno Azul regular · subset com escola declarada (36,1%; municipal omitida) · X-TRI",
         ha='center', fontsize=7.6, color='#999')
fig.tight_layout(rect=[0,0.085,1,0.93])
out=f"{SP}/E1_informacao_x_rede.png"
fig.savefig(out, facecolor='white'); print("OK ->", out)
print("HERO:", json.dumps(hero, ensure_ascii=False))
