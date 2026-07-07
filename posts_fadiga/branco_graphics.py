#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa + curva do branco por posição — post fadiga/em branco. Padrao XTRI. Dado real recalculado."""
import os, csv
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
FD="/sessions/brave-sharp-fermi/mnt/.claude/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB=F("Outfit-Bold"); outfit=F("Outfit-Regular"); mono=F("JetBrainsMono-Regular"); monoB=F("JetBrainsMono-Bold")
LOGO="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/logo_xtri_marca_real.png"
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"; OUT="/sessions/brave-sharp-fermi/mnt/outputs/branco"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"; AMBER_BG="#FBEFD6"
ACOL={"LC":"#1FAFEF","CH":"#E84B8A","CN":"#27AE60","MT":"#F39C12"}
ANOME={"LC":"Linguagens","CH":"Ciências Humanas","CN":"Ciências da Natureza","MT":"Matemática"}
AMED={"LC":"0,39%","CH":"0,76%","CN":"0,20%","MT":"0,28%"}
# dados
D={a:{} for a in ACOL}
for r in csv.DictReader(open(f"{BASE}/posts_fadiga/fadiga_branco_por_posicao.csv")):
    try: D[r["area"]][int(r["pos"])]=float(r["pct"])
    except: pass

# ---------- CAPA 1200x630 ----------
W,H=1200,630; M=64
fig=plt.figure(figsize=(W/100,H/100),dpi=300); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0)); fig.canvas.draw()
R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
def tw(s,fp,sz):
    t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw(); w=t.get_window_extent(R).width/PXU; t.remove(); return w
def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
    return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
def rrect(x,y,w,h,rad,fc,z=2):
    ax.add_patch(FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",fc=fc,ec="none",zorder=z,mutation_aspect=1))
def shadow(x,y,w,h,rad):
    for i in range(1,7): rrect(x-i,y+2+1.6*i,w+2*i,h+i,rad+1.1*i,"#000000",z=1.5)
try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=0.072),(M+22,54),frameon=False,box_alignment=(0.5,0.5),zorder=6))
except Exception: pass
txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,52,"X-TRI · ANÁLISE DE DADOS",outfitB,14,INK,ha="right")
txt(W-M,78,"ENEM 2025 · QUEM TRAVA NO FIM",mono,11.5,GRAY,ha="right")
txt(M,196,"A prova ",outfitB,54,INK); txt(M+tw("A prova ",outfitB,54),196,"cansa",outfitB,54,CORAL); txt(M+tw("A prova cansa",outfitB,54),196,".",outfitB,54,INK)
txt(M,250,"Questões em branco no ENEM quase dobram do começo ao fim da prova.",outfit,18,GRAY)
cx,cy,cw,ch=M,330,W-2*M,168
shadow(cx,cy,cw,ch,22); rrect(cx,cy,cw,ch,22,CARD,z=2)
txt(cx+34,cy+46,"CIÊNCIAS HUMANAS · A MAIS LONGA DE LEITURA",mono,13,GRAY)
txt(cx+32,cy+106,"~0,5% → ~1,0%",outfitB,42,CORALd); txt(cx+32+tw("~0,5% → ~1,0%",outfitB,42)+18,cy+106,"(×1,9)",outfitB,30,INK)
txt(cx+34,cy+140,"o branco quase dobra até o fim — não é falta de saber, é energia",outfit,16,GRAY)
txt(M,560,"Dados reais",outfitB,17,CYAN); xx=M+tw("Dados reais",outfitB,17)
txt(xx,560," ou ",outfitB,17,INK); xx+=tw(" ou ",outfitB,17); txt(xx,560,"nada",outfitB,17,CORAL); xx+=tw("nada",outfitB,17); txt(xx,560,".",outfitB,17,INK)
txt(W-M,560,"Fonte: Microdados ENEM 2025 / INEP",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_branco_capa.png",dpi=300,facecolor=BG); plt.close(fig); print("capa ok")

# ---------- CURVA 1200x720 ----------
fig,ax=plt.subplots(figsize=(12,7.2),dpi=100); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
xs=list(range(1,46))
for ar in ["CH","LC","MT","CN"]:
    ys=[D[ar].get(i,0) for i in xs]
    ax.plot(xs,ys,color=ACOL[ar],lw=2.4,zorder=4,label=f"{ANOME[ar]}  (média {AMED[ar]})")
ax.set_xlim(1,45); ax.set_ylim(0,1.25)
ax.set_xlabel("Posição da questão na prova (1ª → 45ª)",fontproperties=outfit,fontsize=13,color=INK)
ax.set_ylabel("% de respostas em branco",fontproperties=outfit,fontsize=13,color=INK)
for s in ["top","right"]: ax.spines[s].set_visible(False)
for s in ["left","bottom"]: ax.spines[s].set_color("#CFD2D5")
ax.tick_params(colors=GRAY); ax.grid(axis="y",color="#E6E7E9",lw=0.8); ax.set_axisbelow(True)
import matplotlib.ticker as mt
ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v,p:f"{v:.1f}%".replace(".",",")))
for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(10)
leg=ax.legend(loc="upper left",frameon=True,prop=outfit,framealpha=0.95,edgecolor="#E0E0E0")
for t in leg.get_texts(): t.set_fontsize(11.5); t.set_color(INK)
fig.text(0.075,0.935,"O branco sobe ao longo da prova",fontproperties=outfitB,fontsize=21,color=INK)
fig.text(0.075,0.888,"Taxa de questões em branco por posição (4,8 mi de participantes). Humanas, a mais longa, é a que mais sobe.",fontproperties=outfit,fontsize=12.5,color=GRAY)
fig.subplots_adjust(left=0.085,right=0.97,top=0.82,bottom=0.135)
fig.text(0.075,0.035,"Dados reais ou nada.",fontproperties=outfitB,fontsize=14,color=CYAN)
fig.text(0.97,0.037,"Fonte: Microdados ENEM 2025 / INEP · TX_RESPOSTAS por posição",fontproperties=mono,fontsize=9.5,color=GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_branco_curva.png",facecolor=BG); plt.close(fig); print("curva ok")
print("FIM")
