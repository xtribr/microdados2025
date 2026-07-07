#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa WordPress (1200x630) — 'Microdados 2025 ENEM: do zero ao 960'. Padrao XTRI (CLAUDE.md)."""
import os
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
OUT="/sessions/brave-sharp-fermi/mnt/outputs/wp"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
CY_BG="#E7F4FB"; CO_BG="#FBE3DC"
W,H=1200,630; M=64
fig=plt.figure(figsize=(W/100,H/100),dpi=300); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
fig.canvas.draw(); R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
def tw(s,fp,sz):
    t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw(); w=t.get_window_extent(R).width/PXU; t.remove(); return w
def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
    return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
def rrect(x,y,w,h,rad,fc,z=2):
    ax.add_patch(FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",fc=fc,ec="none",zorder=z,mutation_aspect=1))
def shadow(x,y,w,h,rad):
    for i in range(1,7): rrect(x-i,y+2+1.6*i,w+2*i,h+i,rad+1.1*i,"#000000",z=1.5)
# logo + kicker
try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=0.072),(M+22,54),frameon=False,box_alignment=(0.5,0.5),zorder=6))
except Exception: pass
txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,52,"X-TRI · ANÁLISE DE DADOS",outfitB,14,INK,ha="right")
txt(W-M,78,"MICRODADOS 2025 · ENEM",mono,11.5,GRAY,ha="right")
# headline: Do zero ao 960
y=178; x=M
for seg,col in [("Do ",INK),("zero",CORAL),(" ao ",INK),("960",CYAN),(".",INK)]:
    txt(x,y,seg,outfitB,60,col); x+=tw(seg,outfitB,60)
# hook (2 linhas, palavras-chave em destaque)
hy=232
def line(y,parts):
    x=M
    for s,fp,col in parts: txt(x,y,s,fp,19,col); x+=tw(s,fp,19)
line(hy,[("Na redação do ENEM, o que é ",outfit,GRAY),("“repertório”",outfitB,INK),(" para um corretor",outfit,GRAY)])
line(hy+28,[("pode virar ",outfit,GRAY),("“cópia”",outfitB,INK),(" para outro — e a nota vai de 0 a 960.",outfit,GRAY)])
# card heroi
cx,cy,cw,ch=M,300,W-2*M,182
shadow(cx,cy,cw,ch,24); rrect(cx,cy,cw,ch,24,CARD,z=2)
txt(cx+36,cy+46,"UM AVALIADOR PONTUOU, O OUTRO ANULOU (NOTA 0)",mono,12.5,GRAY)
txt(cx+34,cy+110,"67.346",outfitB,56,CORAL)
txt(cx+34+tw("67.346",outfitB,56)+14,cy+110,"redações",outfit,24,INK)
txt(cx+36,cy+150,"ENEM 2025 · recorte dos 300 casos mais extremos.",outfit,16.5,INK)
# chips contraste (direita do card)
chx=cx+cw-372
rrect(chx,cy+34,360,56,14,CY_BG,z=3); txt(chx+18,cy+58,"UM CORRETOR",mono,12,CYANd); txt(chx+360-18,cy+74,"600+ pontos",outfitB,21,CYANd,ha="right")
rrect(chx,cy+100,360,56,14,CO_BG,z=3); txt(chx+18,cy+124,"O OUTRO CORRETOR",mono,12,CORALd); txt(chx+360-18,cy+140,"0 · anulou",outfitB,21,CORALd,ha="right")
# rodape
fy=H-44
txt(M,fy,"Dados reais",outfitB,17,CYAN); xx=M+tw("Dados reais",outfitB,17)
txt(xx,fy," ou ",outfitB,17,INK); xx+=tw(" ou ",outfitB,17); txt(xx,fy,"nada",outfitB,17,CORAL); xx+=tw("nada",outfitB,17); txt(xx,fy,".",outfitB,17,INK)
txt(W-M,fy-1,"Fonte: Microdados ENEM 2025 / INEP · app.rankingenem.com",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_wp_capa_zero_ao_960.png",dpi=300,facecolor=BG); print("capa ok")
