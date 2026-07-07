#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa + gráfico do paradoxo (15 acertos→notas diferentes) — post 'como funciona a nota'. Padrao XTRI.
Dado real: amostra_xtri_2025_MT.csv (Regular P1)."""
import os, csv, numpy as np
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
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"; OUT="/sessions/brave-sharp-fermi/mnt/outputs/nota"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"; AMBER_BG="#FBEFD6"

# ---- dados do paradoxo ----
acc={}
with open(f"{BASE}/analises_primi_2025_cop30/outputs/amostra_xtri_2025_MT.csv") as f:
    for r in csv.DictReader(f):
        if r["area"]=="MT" and r["aplicacao"]=="Regular P1":
            try: acc.setdefault(int(r["acertos"]),[]).append(float(r["nota"]))
            except: pass
ks=[k for k in sorted(acc) if len(acc[k])>=30]
mn=[np.min(acc[k]) for k in ks]; mx=[np.max(acc[k]) for k in ks]
p10=[np.percentile(acc[k],10) for k in ks]; p90=[np.percentile(acc[k],90) for k in ks]; med=[np.median(acc[k]) for k in ks]

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
txt(W-M,78,"TRI DO ENEM · COMO A NOTA FUNCIONA",mono,11.5,GRAY,ha="right")
txt(M,196,"Acerto ",outfitB,54,INK); txt(M+tw("Acerto ",outfitB,54),196,"não",outfitB,54,CORAL); txt(M+tw("Acerto não",outfitB,54),196," é nota.",outfitB,54,INK)
txt(M,250,"Como funciona a nota do ENEM: o que pesa é a discriminação, não a dificuldade.",outfit,18,GRAY)
cx,cy,cw,ch=M,330,W-2*M,168
shadow(cx,cy,cw,ch,22); rrect(cx,cy,cw,ch,22,CARD,z=2)
txt(cx+34,cy+46,"MATEMÁTICA · MESMO Nº DE ACERTOS",mono,13,GRAY)
txt(cx+32,cy+106,"15 acertos",outfitB,40,INK); txt(cx+32+tw("15 acertos",outfitB,40)+16,cy+106,"→ 353 a 635",outfitB,40,CORALd)
txt(cx+34,cy+140,"282 pontos de diferença com o mesmo número de acertos",outfit,16,GRAY)
txt(M,560,"Dados reais",outfitB,17,CYAN); xx=M+tw("Dados reais",outfitB,17)
txt(xx,560," ou ",outfitB,17,INK); xx+=tw(" ou ",outfitB,17); txt(xx,560,"nada",outfitB,17,CORAL); xx+=tw("nada",outfitB,17); txt(xx,560,".",outfitB,17,INK)
txt(W-M,560,"Fonte: Microdados ENEM 2025 / INEP",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_nota_capa.png",dpi=300,facecolor=BG); plt.close(fig); print("capa ok")

# ---------- PARADOXO 1200x720 ----------
fig,ax=plt.subplots(figsize=(12,7.2),dpi=100); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.fill_between(ks,mn,mx,color=CORAL,alpha=0.10,zorder=1,label="faixa mín–máx")
ax.plot(ks,p10,color=CORALd,lw=1.4,ls=(0,(2,2)),zorder=3); ax.plot(ks,p90,color=CORALd,lw=1.4,ls=(0,(2,2)),zorder=3,label="p10–p90")
ax.plot(ks,med,color=CORALd,lw=3.2,zorder=4,label="mediana")
# destaque 15 acertos
i15=ks.index(15)
ax.plot([15,15],[mn[i15],mx[i15]],color="#7a1d10",lw=5,zorder=5,solid_capstyle="round")
ax.annotate("15 acertos → 353 a 635\n282 pts de diferença",xy=(15,mx[i15]),xytext=(9.5,720),
            fontproperties=outfitB,fontsize=13,color=CORALd,ha="left",va="bottom",
            arrowprops=dict(arrowstyle="->",color=CORALd,lw=1.6))
ax.set_xlim(2,42); ax.set_ylim(300,1000)
ax.set_xlabel("Nº de acertos (Matemática)",fontproperties=outfit,fontsize=13,color=INK)
ax.set_ylabel("Nota TRI oficial",fontproperties=outfit,fontsize=13,color=INK)
fig.text(0.075,0.935,"Mesmo número de acertos, notas diferentes",fontproperties=outfitB,fontsize=21,color=INK)
fig.text(0.075,0.888,"Em Matemática (amostra Regular P1): a nota depende do padrão das respostas, não da contagem.",fontproperties=outfit,fontsize=12.5,color=GRAY)
for s in ["top","right"]: ax.spines[s].set_visible(False)
for s in ["left","bottom"]: ax.spines[s].set_color("#CFD2D5")
ax.tick_params(colors=GRAY); ax.grid(axis="y",color="#E6E7E9",lw=0.8); ax.set_axisbelow(True)
for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(10)
leg=ax.legend(loc="lower right",frameon=False,prop=mono);
for t in leg.get_texts(): t.set_fontsize(11); t.set_color(INK)
fig.subplots_adjust(left=0.085,right=0.97,top=0.82,bottom=0.135)
fig.text(0.085,0.035,"Dados reais ou nada.",fontproperties=outfitB,fontsize=14,color=CYAN)
fig.text(0.97,0.037,"Fonte: Microdados ENEM 2025 / INEP · amostra Regular P1 (MT) · reconstrução TRI",
         fontproperties=mono,fontsize=9.5,color=GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_nota_paradoxo.png",facecolor=BG); plt.close(fig); print("paradoxo ok")
print("FIM")
