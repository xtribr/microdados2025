#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa + scatter (TRI x %acerto, 180 itens) para o post TRI dos Itens. Padrao XTRI (CLAUDE.md)."""
import os, openpyxl, numpy as np
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
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"; OUT="/sessions/brave-sharp-fermi/mnt/outputs/triitens"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"; AMBER_BG="#FBEFD6"
ACOL={"Linguagens":"#1FAFEF","Ciências Humanas":"#E84B8A","Ciências da Natureza":"#27AE60","Matemática":"#F39C12"}
ANOME={"Linguagens":"Linguagens","Ciências Humanas":"Humanas","Ciências da Natureza":"Natureza","Matemática":"Matemática"}

# dados
wb=openpyxl.load_workbook(f"{BASE}/TRI_ITENS_AZUL_ENEM2025.xlsx",data_only=True)
pts={a:[] for a in ACOL}
for r in list(wb["TRI_itens"].iter_rows(values_only=True))[1:]:
    n,area,ling,co,hab,gab,a,b,c,tri,pac,nresp,anul=r
    if anul or area=="Linguagens" and ling=="Espanhol": continue
    if isinstance(tri,(int,float)) and isinstance(pac,(int,float)): pts[area].append((n,tri,pac))

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
txt(W-M,78,"ENEM 2025 · 180 ITENS CALIBRADOS",mono,11.5,GRAY,ha="right")
txt(M,150,"O RAIO-X COMPLETO DA PROVA",monoB,15,CORALd)
txt(M,212,"TRI dos itens",outfitB,56,INK)
x=M;y=270; txt(x,y,"do ",outfitB,40,GRAY); x+=tw("do ",outfitB,40); txt(x,y,"ENEM 2025",outfitB,40,INK)
txt(M,316,"As 180 questões medidas pela TRI — da mais fácil à mais brutal, área por área.",outfit,18,GRAY)
cx,cy,cw,ch=M,360,W-2*M,150
shadow(cx,cy,cw,ch,22); rrect(cx,cy,cw,ch,22,AMBER_BG,z=2)
txt(cx+34,cy+44,"A MAIS BRUTAL DE TODA A PROVA",mono,13,"#B07A1E")
txt(cx+32,cy+98,"Matemática Q160",outfitB,32,INK)
txt(cx+32+tw("Matemática Q160",outfitB,32)+18,cy+98,"— dificuldade TRI 923,7",outfitB,28,CORALd)
txt(cx+34,cy+128,"apenas 15% de acerto",outfit,16,"#9A7A3A")
assin(M,560); txt(W-M,560,"Fonte: Microdados ENEM 2025 / INEP",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_tri_itens_capa.png",dpi=300,facecolor=BG); plt.close(fig); print("capa ok")

# ---------- SCATTER 1200x740 ----------
W,H=1200,740; M=64; fig,ax,tw,txt,rrect,shadow,logo,assin=base(W,H)
logo(M+22,54); txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,56,"180 ITENS · CADERNO AZUL · INEP",mono,12,GRAY,ha="right")
txt(M,116,"Dificuldade × acerto: as 180 questões do ENEM 2025",outfitB,31,INK)
txt(M,148,"Cada ponto é uma questão. Quanto mais difícil pela TRI, menor o acerto (correlação −0,83).",outfit,15.5,GRAY)
# legenda de areas (topo)
lx=M
for area,col in ACOL.items():
    ax.add_patch(FancyBboxPatch((lx,186-7),14,14,boxstyle="circle,pad=0",fc=col,ec="white",lw=0.5,zorder=4))
    txt(lx+22,186+5,ANOME[area],mono,12,INK); lx+=tw(ANOME[area],mono,12)+56
# area de plot
px0,px1,py0,py1=150,1120,230,604
XMIN,XMAX,YMIN,YMAX=420,940,0,90
def X(v): return px0+(v-XMIN)/(XMAX-XMIN)*(px1-px0)
def Y(v): return py1-(v-YMIN)/(YMAX-YMIN)*(py1-py0)
# grade + eixos
for gx in range(450,941,50):
    ax.add_line(Line2D([X(gx),X(gx)],[py0,py1],color="#E6E7E9",lw=0.8,zorder=1)); txt(X(gx),py1+22,str(gx),mono,10,GRAY,ha="center")
for gy in range(0,91,15):
    ax.add_line(Line2D([px0,px1],[Y(gy),Y(gy)],color="#E6E7E9",lw=0.8,zorder=1)); txt(px0-10,Y(gy),f"{gy}%",mono,10,GRAY,ha="right",va="center")
txt((px0+px1)/2,py1+48,"Dificuldade TRI (b×100+500)",mono,12,INK,ha="center")
ax.text(40,(py0+py1)/2,"% de acerto",fontproperties=mono,fontsize=12,color=INK,ha="center",va="center",rotation=90,zorder=5)
# pontos + regressao
allx=[]; ally=[]
for area,col in ACOL.items():
    for n,tri,pac in pts[area]:
        ax.add_patch(FancyBboxPatch((X(tri)-4,Y(pac)-4),8,8,boxstyle="circle,pad=0",fc=col,ec="white",lw=0.5,alpha=0.9,zorder=4))
        allx.append(tri); ally.append(pac)
m,bb=np.polyfit(allx,ally,1)
ax.add_line(Line2D([X(XMIN),X(XMAX)],[Y(m*XMIN+bb),Y(m*XMAX+bb)],color=INK,lw=2,ls=(0,(6,4)),zorder=5))
# destaques
def annot(tri,pac,lab,col):
    ax.add_patch(FancyBboxPatch((X(tri)-6,Y(pac)-6),12,12,boxstyle="circle,pad=0",fc=col,ec=INK,lw=1.4,zorder=6))
annot(923.7,15,"",CORAL); txt(X(923.7)-12,Y(15)-12,"MT Q160 (mais difícil)",monoB,11,CORALd,ha="right")
annot(440.4,87,"",CYAN); txt(X(440.4)+14,Y(87)+4,"LC Q26 (mais fácil)",monoB,11,CYANd)
assin(M,H-46); txt(W-M,H-47,"Microdados ENEM 2025 / INEP · TRI dos itens (caderno Azul)",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_tri_itens_scatter.png",dpi=300,facecolor=BG); plt.close(fig); print("scatter ok")
print("FIM")
