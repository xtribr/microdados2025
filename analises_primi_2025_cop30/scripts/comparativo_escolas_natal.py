#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comparativo TRI - 54 alunos por escola (Natal/RN) - estilo XTRI."""
import json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
import matplotlib.image as mpimg
import numpy as np

OUT="/sessions/funny-kind-hawking/mnt/outputs"
DRIVE="/sessions/funny-kind-hawking/mnt/microdados_enem_2025"  # pode estar indisponivel p/ shell
for p in ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
    fm.fontManager.addfont(p)
plt.rcParams['font.family']='Liberation Sans'

AZUL="#1CA9E0"; LARANJA="#F15A2B"; INK="#13213A"; MUT="#6B7A90"; BG="#FFFFFF"; GRID="#E4E9F0"; PANEL="#F3F6FA"
res=json.load(open(f"{OUT}/comparacao_escolas.json"))
# reparse m4 lists per school (sorted desc, selected)
def parse(fn):
    v=[]
    for line in open(f"{OUT}/{fn}"):
        line=line.strip()
        if not line: continue
        f=line.split(":",1)[1].split(";")
        try: v.append((float(f[21])+float(f[22])+float(f[23])+float(f[24]))/4)
        except: pass
    return sorted(v, reverse=True)
files={"CCA":"esc_cca.txt","Porto":"esc_porto.txt","CEI":"esc_cei.txt","Marista":"esc_marista.txt"}
m4={k:(parse(v) if k=="CCA" else parse(v)[:54]) for k,v in files.items()}
# ordem por media desc
order=sorted(res.keys(), key=lambda k:res[k]["geral"]["media"], reverse=True)
labels={"CCA":"Ciências\nAplicadas","Porto":"Colégio\nPorto","CEI":"CEI\n(Romualdo)","Marista":"Marista\nde Natal"}
COLS={"CCA":LARANJA,"Porto":AZUL,"CEI":"#3DB8C4","Marista":"#F4A93B"}

fig=plt.figure(figsize=(13.6,9.6),dpi=100); fig.patch.set_facecolor(BG)
def ax_at(l,b,w,h):
    a=fig.add_axes([l,b,w,h]); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_visible(False)
    a.set_xlim(0,1); a.set_ylim(0,1); a.patch.set_alpha(0); return a

# logo + titulo
lp=f"{DRIVE}/logo_xtri_marca_real.png"
if os.path.exists(lp):
    la=fig.add_axes([0.04,0.93,0.05,0.055]); la.axis('off'); la.imshow(mpimg.imread(lp))
top=ax_at(0.095,0.93,0.88,0.06)
top.text(0,0.5,"X",fontsize=22,fontweight='bold',color=AZUL,va='center')
top.text(0.022,0.5,"-TRI",fontsize=22,fontweight='bold',color=LARANJA,va='center')
top.text(1,0.5,"ESTUDO COMPARATIVO · ENEM 2025 · NATAL/RN",fontsize=11,color=MUT,va='center',ha='right',fontweight='bold')
tit=ax_at(0.04,0.85,0.93,0.07)
tit.text(0,0.62,"Comparativo TRI — 54 alunos por escola",fontsize=27,fontweight='bold',color=INK,va='center')
tit.text(0,0.12,"Ciências Aplicadas: todos os 54 concluintes  ·  demais escolas: os 54 melhores (média das 4 notas TRI)",
         fontsize=12.5,color=MUT,va='center')

# Painel A: boxplot distribuicao media por aluno
axA=fig.add_axes([0.065,0.40,0.52,0.40]); axA.set_facecolor(BG)
for s in ['top','right']: axA.spines[s].set_visible(False)
for s in ['left','bottom']: axA.spines[s].set_color(GRID)
data=[m4[k] for k in order]; pos=range(len(order))
bp=axA.boxplot(data,positions=list(pos),widths=0.55,patch_artist=True,
   medianprops=dict(color=INK,lw=2),whiskerprops=dict(color=MUT),capprops=dict(color=MUT),
   flierprops=dict(marker='o',ms=4,mfc='none',mec=MUT))
for i,k in enumerate(order):
    bp['boxes'][i].set(facecolor=COLS[k],alpha=0.35,edgecolor=COLS[k],lw=1.6)
    # jitter pontos
    xs=np.random.RandomState(7).normal(i,0.06,len(m4[k]))
    axA.scatter(xs,m4[k],s=12,color=COLS[k],alpha=0.55,zorder=3,edgecolor='none')
    axA.text(i,res[k]["geral"]["media"],f"  {res[k]['geral']['media']:.0f}",fontsize=9.5,color=INK,fontweight='bold',va='center')
axA.set_xticks(list(pos)); axA.set_xticklabels([labels[k] for k in order],fontsize=10.5,color=INK)
axA.tick_params(colors=MUT,labelsize=9,length=0); axA.grid(axis='y',color=GRID,lw=1); axA.set_axisbelow(True)
axA.set_ylabel("Média das 4 notas TRI (por aluno)",fontsize=11,color=INK)
axA.set_title("Distribuição dos 54 alunos por escola",fontsize=12.5,color=INK,loc='left',pad=8,fontweight='bold')

# Painel B: barras por area
axB=fig.add_axes([0.64,0.40,0.33,0.40]); axB.set_facecolor(BG)
for s in ['top','right']: axB.spines[s].set_visible(False)
for s in ['left','bottom']: axB.spines[s].set_color(GRID)
areas=["CN","CH","LC","MT"]; x=np.arange(len(areas)); w=0.2
for i,k in enumerate(order):
    vals=[res[k][a]["media"] for a in areas]
    axB.bar(x+(i-1.5)*w,vals,w,color=COLS[k],label=labels[k].replace("\n"," "),alpha=0.9)
axB.set_xticks(x); axB.set_xticklabels(["Natureza","Humanas","Linguagens","Matem."],fontsize=9.5,color=INK)
axB.tick_params(colors=MUT,labelsize=8,length=0); axB.grid(axis='y',color=GRID,lw=1); axB.set_axisbelow(True)
axB.set_ylim(600,860); axB.set_ylabel("Média TRI por área",fontsize=11,color=INK)
axB.set_title("Média por área",fontsize=12.5,color=INK,loc='left',pad=8,fontweight='bold')
axB.legend(fontsize=8.5,frameon=False,loc='upper left',ncol=2,columnspacing=1)

# Painel C: tabela resumo
axC=ax_at(0.065,0.07,0.905,0.28)
axC.add_patch(FancyBboxPatch((0,0.0),1,1,boxstyle="round,pad=0.01,rounding_size=0.02",fc=PANEL,ec=GRID,lw=1,transform=axC.transAxes))
hdr=["Escola","Pool c/ 4 notas","Amostra","Média geral","Mediana","Desvio","Melhor aluno"]
colx=[0.02,0.34,0.47,0.57,0.69,0.80,0.90]
for j,h in enumerate(hdr):
    axC.text(colx[j],0.86,h,fontsize=10.5,color=MUT,fontweight='bold',va='center')
axC.plot([0.02,0.98],[0.78,0.78],color=GRID,lw=1)
rowy=[0.62,0.46,0.30,0.14]
for i,k in enumerate(order):
    v=res[k]; c=COLS[k]
    pool = v['n_total_4notas']
    amostra = "todos os 54" if k=="CCA" else "54 melhores"
    cells=[v['name'].replace(" (Romualdo)",""),str(pool),amostra,f"{v['geral']['media']:.1f}",
           f"{v['geral']['mediana']:.1f}",f"{v['geral']['dp']:.1f}",f"{v['geral']['max']:.1f}"]
    axC.text(0.02,rowy[i],f"●",fontsize=11,color=c,va='center')
    for j,txt in enumerate(cells):
        off = 0.022 if j==0 else 0
        axC.text(colx[j]+off,rowy[i],txt,fontsize=10.5,color=INK,va='center',
                 fontweight='bold' if j in (0,3) else 'normal')

foot=ax_at(0.04,0.005,0.93,0.05)
foot.text(0,0.5,"Fonte: Microdados ENEM 2025/INEP · presentes nos 2 dias com as 4 notas objetivas · ranqueado pela média das 4 notas TRI · Análise XTRI · Dados reais.",
          fontsize=9.5,color=MUT,va='center')
fig.savefig(f"{OUT}/comparativo_escolas_natal_2025.png",dpi=100,facecolor=BG)
print("OK")
