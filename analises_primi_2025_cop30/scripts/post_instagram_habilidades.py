#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post Instagram 1080x1350 - habilidades mais dificeis ENEM 2025 - estilo XTRI/Apple."""
import json, textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D
import numpy as np

OUT="/sessions/funny-kind-hawking/mnt/microdados_enem_2025/analises_primi_2025_cop30/outputs"

# fonte tipo Helvetica
for p in ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
    fm.fontManager.addfont(p)
plt.rcParams['font.family']='Liberation Sans'

# cores XTRI
AZUL="#1CA9E0"; LARANJA="#F15A2B"
COL={'LC':AZUL,'MT':LARANJA,'CH':"#F4A93B",'CN':"#3DB8C4"}
LAB={'LC':'Linguagens','MT':'Matemática','CH':'Ciências Humanas','CN':'Ciências da Natureza'}
INK="#13213A"; MUT="#6B7A90"; BG="#FFFFFF"; PANEL="#F3F6FA"; GRID="#E4E9F0"

aud=json.load(open(f"{OUT}/auditoria_dificuldade_habilidades_2025.json"))
rows=aud['habilidades']
pts=[(r['area'],r['p_ponderado']*100,r['B_medio']) for r in rows if r['B_medio'] is not None]
hard={}
for a in COL:
    ar=sorted([r for r in rows if r['area']==a],key=lambda r:r['p_ponderado'])
    hard[a]=ar[0]

W,H=1080,1350
fig=plt.figure(figsize=(W/100,H/100),dpi=100)
fig.patch.set_facecolor(BG)

def ax_at(l,b,w,h):
    a=fig.add_axes([l,b,w,h]); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_visible(False)
    a.set_xlim(0,1); a.set_ylim(0,1); a.patch.set_alpha(0); return a

# ---------- topo: faixa de marca ----------
import os
from matplotlib.patches import Polygon
top=ax_at(0,0.945,1,0.055)
_B="/sessions/funny-kind-hawking/mnt/microdados_enem_2025/"
_cands=[_B+"logo_xtri_marca_real.png",_B+"logo_xtri_marca.png",_B+"logo_xtri.png"]
logo_path=next((p for p in _cands if os.path.exists(p)),None)
if logo_path:
    import matplotlib.image as mpimg
    lg=fig.add_axes([0.055,0.949,0.055,0.045]); lg.axis('off')
    lg.imshow(mpimg.imread(logo_path));
else:
    # recriacao do X: arcos arredondados, azul (esquerda) + laranja (direita)
    lg=fig.add_axes([0.055,0.949,0.05,0.045]); lg.axis('off')
    lg.set_xlim(0,1); lg.set_ylim(0,1); lg.set_aspect('equal')
    C=(0.5,0.5); LW=13
    lg.add_line(Line2D([C[0],0.1],[C[1],0.93],lw=LW,color=AZUL,solid_capstyle='round',zorder=2))
    lg.add_line(Line2D([C[0],0.1],[C[1],0.07],lw=LW,color=AZUL,solid_capstyle='round',zorder=2))
    lg.add_line(Line2D([C[0],0.9],[C[1],0.93],lw=LW,color=LARANJA,solid_capstyle='round',zorder=2))
    lg.add_line(Line2D([C[0],0.9],[C[1],0.07],lw=LW,color=LARANJA,solid_capstyle='round',zorder=2))
    lg.add_patch(Polygon([[0.6,0.6],[0.78,0.5],[0.6,0.4]],closed=True,fc=LARANJA,ec='none',zorder=3,
                 joinstyle='round'))
# wordmark X-TRI (X azul, TRI laranja)
top.text(0.118,0.5,"X",fontsize=26,fontweight='bold',color=AZUL,va='center',ha='left')
top.text(0.146,0.5,"-TRI",fontsize=26,fontweight='bold',color=LARANJA,va='center',ha='left')
top.text(0.965,0.5,"ANÁLISE · MICRODADOS ENEM 2025",fontsize=11.5,color=MUT,va='center',ha='right',fontweight='bold')

# ---------- titulo ----------
tit=ax_at(0.055,0.83,0.89,0.10)
tit.text(0,0.74,"As habilidades mais difíceis",fontsize=33,fontweight='bold',color=INK,va='center')
tit.text(0,0.30,"do ENEM 2025",fontsize=33,fontweight='bold',color=LARANJA,va='center')
sub=ax_at(0.055,0.788,0.89,0.045)
sub.text(0,0.5,"% de acerto real dos participantes cruzado com a dificuldade na escala TRI (parâmetro B).",
         fontsize=13.5,color=MUT,va='center')

# ---------- grafico scatter ----------
gx=fig.add_axes([0.105,0.475,0.84,0.275]); gx.set_facecolor(BG)
for s in ['top','right']: gx.spines[s].set_visible(False)
for s in ['left','bottom']: gx.spines[s].set_color(GRID)
gx.tick_params(colors=MUT,labelsize=11,length=0)
gx.grid(True,color=GRID,lw=1)
gx.set_axisbelow(True)
for a in COL:
    xs=[b for (ar,p,b) in pts if ar==a]; ys=[p for (ar,p,b) in pts if ar==a]
    gx.scatter(xs,ys,s=70,color=COL[a],alpha=0.82,edgecolor='white',linewidth=0.8,zorder=3,label=LAB[a])
gx.set_xlim(-0.6,3.1); gx.set_ylim(5,85)
gx.set_xlabel("Dificuldade TRI (B)  →",fontsize=12,color=INK,labelpad=6)
gx.set_ylabel("% de acerto",fontsize=12,color=INK,labelpad=4)
gx.yaxis.set_major_formatter(lambda v,_:f"{int(v)}%")
gx.set_title("Cada ponto é uma habilidade  ·  quanto mais à direita e mais embaixo, mais difícil",
             fontsize=11.5,color=MUT,loc='left',pad=10)
# marca a mais dificil de cada area (circulo aberto) e rotula a campea geral (CN H26)
for a in COL:
    h=hard[a]; x=h['B_medio']; y=h['p_ponderado']*100
    gx.scatter([x],[y],s=160,facecolor='none',edgecolor=COL[a],linewidth=2.2,zorder=4)
hcn=hard['CN']; xc=hcn['B_medio']; yc=hcn['p_ponderado']*100
gx.annotate(f"Mais difícil de todas\nCN · H26  ·  {yc:.1f}% de acerto",(xc,yc),
            textcoords='offset points',xytext=(-30,72),ha='center',
            fontsize=11,fontweight='bold',color=INK,
            bbox=dict(boxstyle='round,pad=0.4',fc='white',ec=COL['CN'],lw=1.6),
            arrowprops=dict(arrowstyle='-',color=COL['CN'],lw=1.6))
# legenda
leg=gx.legend(loc='upper right',frameon=False,fontsize=10.5,handletextpad=0.3,labelspacing=0.3,ncol=2,columnspacing=1.2)
for t in leg.get_texts(): t.set_color(INK)

# ---------- 2x2 cards (mais dificil por area) ----------
order=['CN','MT','CH','LC']
short={'CN':"Avaliar implicações sociais, ambientais e econômicas de recursos energéticos ou minerais.",
       'MT':"Identificar a relação de dependência entre grandezas.",
       'CH':"Analisar a atuação de movimentos sociais em disputas pelo poder.",
       'LC':"Reconhecer a produção cultural em língua estrangeira como expressão da diversidade."}
cw,ch=0.435,0.135; gapx=0.02; gapy=0.018; x0=0.055; y0=0.10
pos=[(x0,y0+ch+gapy),(x0+cw+gapx,y0+ch+gapy),(x0,y0),(x0+cw+gapx,y0)]
for (a,(cx,cy)) in zip(order,pos):
    h=hard[a]; c=COL[a]
    cax=ax_at(cx,cy,cw,ch)
    cax.add_patch(FancyBboxPatch((0.02,0.06),0.96,0.88,boxstyle="round,pad=0.02,rounding_size=0.06",
                 fc=PANEL,ec=GRID,lw=1,transform=cax.transAxes,mutation_aspect=cw/ch))
    cax.add_patch(FancyBboxPatch((0.02,0.06),0.035,0.88,boxstyle="round,pad=0,rounding_size=0.02",
                 fc=c,ec=c,transform=cax.transAxes))
    cax.text(0.10,0.80,LAB[a].upper(),fontsize=10.5,color=c,fontweight='bold',va='center')
    cax.text(0.10,0.55,f"H{h['hab']}",fontsize=23,color=INK,fontweight='bold',va='center')
    cax.text(0.30,0.575,f"{h['p_ponderado']*100:.1f}%",fontsize=20,color=INK,fontweight='bold',va='center')
    cax.text(0.30,0.40,"de acerto",fontsize=9.5,color=MUT,va='center')
    cax.text(0.66,0.575,f"B {h['B_medio']:+.2f}",fontsize=15,color=c,fontweight='bold',va='center')
    cax.text(0.66,0.40,"dificuldade",fontsize=9.5,color=MUT,va='center')
    wrapped="\n".join(textwrap.wrap(short[a],42))
    cax.text(0.10,0.20,wrapped,fontsize=9.5,color=MUT,va='center',linespacing=1.25)

# ---------- rodape ----------
foot=ax_at(0,0.0,1,0.075)
foot.plot([0.055,0.945],[0.92,0.92],color=GRID,lw=1)
foot.text(0.055,0.60,"Fonte: Microdados ENEM 2025 / INEP  ·  ENEM Regular (1ª aplicação nacional)",
          fontsize=10.5,color=MUT,va='center')
foot.text(0.055,0.34,"~3,2–3,4 milhões de presentes por área  ·  180 itens  ·  questões anuladas excluídas",
          fontsize=10.5,color=MUT,va='center')
foot.text(0.945,0.46,"Dados reais ou nada.",fontsize=12,color=LARANJA,fontweight='bold',va='center',ha='right')

fig.savefig(f"{OUT}/post_ig_habilidades_dificeis_2025.png",dpi=100,facecolor=BG)
print("OK 1080x1350")
