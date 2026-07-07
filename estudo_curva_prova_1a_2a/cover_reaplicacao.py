#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa WordPress 1200x630 — 'Reaplicação do ENEM é mais difícil?'. Padrao XTRI (CLAUDE.md)."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
FD="/sessions/brave-sharp-fermi/mnt/.claude/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB=F("Outfit-Bold"); outfit=F("Outfit-Regular"); mono=F("JetBrainsMono-Regular"); monoB=F("JetBrainsMono-Bold")
LOGO="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/logo_xtri_marca_real.png"
OUT="/sessions/brave-sharp-fermi/mnt/outputs/reaplic"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
BLUE="#1E6FB8"; RED="#FF4A2D"
W,H=1200,630; M=64
fig=plt.figure(figsize=(W/100,H/100),dpi=300); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0)); fig.canvas.draw()
R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
def tw(s,fp,sz):
    t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw(); w=t.get_window_extent(R).width/PXU; t.remove(); return w
def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
    return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
def rrect(x,y,w,h,rad,fc,z=2,ec="none",lw=0):
    ax.add_patch(FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",fc=fc,ec=ec,lw=lw,zorder=z,mutation_aspect=1))
def shadow(x,y,w,h,rad):
    for i in range(1,7): rrect(x-i,y+2+1.6*i,w+2*i,h+i,rad+1.1*i,"#000000",z=1.5)
try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=0.072),(M+22,54),frameon=False,box_alignment=(0.5,0.5),zorder=6))
except Exception: pass
txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,52,"X-TRI · ANÁLISE DE DADOS",outfitB,14,INK,ha="right")
txt(W-M,78,"ENEM 2025 · TRI",mono,11.5,GRAY,ha="right")
# headline
txt(M,196,"Reaplicação do ENEM",outfitB,52,INK)
x=M;y=258; txt(x,y,"é ",outfitB,52,INK); x+=tw("é ",outfitB,52); txt(x,y,"mais difícil",outfitB,52,CORAL); x+=tw("mais difícil",outfitB,52); txt(x,y,"?",outfitB,52,INK)
txt(M,302,"A função de informação da TRI compara a 2ª aplicação com a regular, área por área.",outfit,17.5,GRAY)
# card veredito (esq) + mini-curvas (dir)
cx,cy,cw,ch=M,348,690,176
shadow(cx,cy,cw,ch,22); rrect(cx,cy,cw,ch,22,CARD,z=2)
txt(cx+30,cy+42,"O VEREDITO",mono,13,CORALd)
txt(cx+30,cy+82,"Não é mais fácil nem mais difícil —",outfitB,23,INK)
txt(cx+30,cy+112,"varia por área.",outfitB,23,INK)
txt(cx+30,cy+148,"MT 2ª mais difícil · LC regular mede melhor · CN 2ª mais precisa",mono,12.5,GRAY)
# mini curvas
ix0,ix1,iy0,iy1=792,1120,360,500
xs=np.linspace(0,1,200)
def bell(mu,sg,h): return h*np.exp(-((xs-mu)**2)/(2*sg*sg))
for ys,col,ls in [(bell(0.42,0.13,1.0),BLUE,"solid"),(bell(0.60,0.11,0.78),RED,(0,(5,2)))]:
    px=ix0+xs*(ix1-ix0); py=iy1-ys*(iy1-iy0)
    ax.add_line(Line2D(px,py,color=col,lw=3,ls=ls,zorder=4))
ax.add_line(Line2D([ix0,ix1],[iy1,iy1],color="#D8DADD",lw=1.4,zorder=3))
txt((ix0+ix1)/2,iy0-8,"informação da prova I(θ)",mono,11,GRAY,ha="center")
txt(ix0,iy1+22,"1ª",monoB,12,BLUE); txt(ix0+44,iy1+22,"2ª aplicação",monoB,12,RED)
# rodape
txt(M,560,"Dados reais",outfitB,17,CYAN); xx=M+tw("Dados reais",outfitB,17)
txt(xx,560," ou ",outfitB,17,INK); xx+=tw(" ou ",outfitB,17); txt(xx,560,"nada",outfitB,17,CORAL); xx+=tw("nada",outfitB,17); txt(xx,560,".",outfitB,17,INK)
txt(W-M,561,"Fonte: INEP · estudo de Alexandre E. M. de Araújo",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_reaplicacao_capa.png",dpi=300,facecolor=BG); print("capa ok")
