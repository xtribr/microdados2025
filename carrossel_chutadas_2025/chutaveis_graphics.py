#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa + grafico 'campeas do chute por area' para o post WP. Padrao XTRI (CLAUDE.md)."""
import os
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
OUT="/sessions/brave-sharp-fermi/mnt/outputs/chutaveis"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"; AMBER_BG="#FBEFD6"
def base(W,H):
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
    def logo(x,y,z=0.072):
        try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=z),(x,y),frameon=False,box_alignment=(0.5,0.5),zorder=6))
        except Exception: pass
    def assin(x,y,sz=17):
        txt(x,y,"Dados reais",outfitB,sz,CYAN); xx=x+tw("Dados reais",outfitB,sz)
        txt(xx,y," ou ",outfitB,sz,INK); xx+=tw(" ou ",outfitB,sz); txt(xx,y,"nada",outfitB,sz,CORAL); xx+=tw("nada",outfitB,sz); txt(xx,y,".",outfitB,sz,INK)
    return fig,ax,tw,txt,rrect,shadow,logo,assin

# ---------- CAPA 1200x630 ----------
W,H=1200,630; M=64; fig,ax,tw,txt,rrect,shadow,logo,assin=base(W,H)
logo(M+22,54); txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,52,"X-TRI · ANÁLISE DE DADOS",outfitB,14,INK,ha="right")
txt(W-M,78,"ENEM 2025 · TRI",mono,11.5,GRAY,ha="right")
txt(M,196,"As questões mais",outfitB,54,INK)
x=M; y=262; txt(x,y,"chutáveis",outfitB,54,CORAL); x+=tw("chutáveis",outfitB,54); txt(x,y," do ENEM 2025",outfitB,54,INK)
txt(M,308,"Pelo parâmetro c da TRI: a chance de acertar sem dominar o conteúdo.",outfit,18.5,GRAY)
# card campea
cx,cy,cw,ch=M,360,W-2*M,150
shadow(cx,cy,cw,ch,22); rrect(cx,cy,cw,ch,22,AMBER_BG,z=2)
txt(cx+34,cy+44,"A CAMPEÃ DO BRASIL",mono,13,"#B07A1E")
txt(cx+32,cy+98,"Física (Q95)",outfitB,34,INK)
txt(cx+32+tw("Física (Q95)",outfitB,34)+18,cy+98,"— 40% no chute",outfitB,34,CORALd)
txt(cx+34,cy+128,"o dobro do chute aleatório (20%)",outfit,16,"#9A7A3A")
assin(M,560)
txt(W-M,560,"Fonte: Microdados ENEM 2025 / INEP",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_chutaveis_capa.png",dpi=300,facecolor=BG); plt.close(fig); print("capa ok")

# ---------- CAMPEAS POR AREA 1200x640 ----------
W,H=1200,640; M=64; fig,ax,tw,txt,rrect,shadow,logo,assin=base(W,H)
logo(M+22,54); txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,56,"ENEM 2025 · CADERNO AZUL · INEP",mono,12,GRAY,ha="right")
txt(M,118,"As campeãs do chute, por área",outfitB,34,INK)
txt(M,150,"Maior parâmetro c (acerto sem dominar o conteúdo) em cada área, vs. o chute aleatório de 20%.",outfit,15.5,GRAY)
rows=[("CIÊNCIAS DA NATUREZA","Q95 · Transferência de calor (Física)",40),
      ("CIÊNCIAS HUMANAS","Q90 · Imperialismo científico (História)",31),
      ("MATEMÁTICA","Q139 · Comprimento de circunferência",31),
      ("LINGUAGENS","Q37 · Intertextualidade",28)]
bx0,bx1=360,1080; SC=50.0  # escala 0..50%
def xv(v): return bx0+(v/SC)*(bx1-bx0)
y0=220; rh=92
# linha de referencia 20%
ax.add_line(Line2D([xv(20),xv(20)],[200,y0+4*rh-26],color=CYANd,lw=1.6,ls=(0,(5,4)),zorder=3))
txt(xv(20),192,"chute aleatório 20%",mono,12,CYANd,ha="center")
for i,(area,q,c) in enumerate(rows):
    yc=y0+i*rh
    txt(M,yc-2,area,outfitB,15.5,INK); txt(M,yc+22,q,outfit,12.5,GRAY)
    ax.add_line(Line2D([bx0,bx1],[yc+6,yc+6],color="#E3E5E7",lw=15,solid_capstyle="round",zorder=2))
    col=CORALd if c==40 else CORAL
    ax.add_line(Line2D([bx0,xv(c)],[yc+6,yc+6],color=col,lw=15,solid_capstyle="round",zorder=3.5))
    txt(xv(c)+16,yc+6,f"{c}%",outfitB,22,INK,va="center")
    if c==40: txt(xv(c)+72,yc+6,"campeã nacional",mono,12,CORALd,va="center")
# eixo
for g in [0,10,20,30,40,50]:
    txt(xv(g),y0+4*rh-6,f"{g}%",mono,11,GRAY,ha="center")
assin(M,H-44)
txt(W-M,H-45,'"No chute" = parâmetro c (TRI) · análise XTRI',mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_chutaveis_campeas.png",dpi=300,facecolor=BG); plt.close(fig); print("campeas ok")
print("FIM")
