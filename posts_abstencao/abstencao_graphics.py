#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa + gráfico dia1×dia2 — post abstenção ENEM 2025. Padrao XTRI (CLAUDE.md). Dados: TP_PRESENCA / INEP."""
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
OUT="/sessions/brave-sharp-fermi/mnt/outputs/abst"; os.makedirs(OUT,exist_ok=True)
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
AMBER="#F39C12"; AMBER_BG="#FBEFD6"; PINK="#E84B8A"; PINK_BG="#FBE3EE"
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
txt(W-M,78,"ENEM 2025 · QUEM NÃO FOI",mono,11.5,GRAY,ha="right")
txt(M,194,"Abstenção no ENEM 2025:",outfitB,46,INK)
x=M;y=252; txt(x,y,"faltar é ",outfitB,46,INK); x+=tw("faltar é ",outfitB,46); txt(x,y,"regra",outfitB,46,CORAL); x+=tw("regra",outfitB,46); txt(x,y,".",outfitB,46,INK)
txt(M,298,"Quase 1 em cada 3 inscritos não fez a prova — e a desistência cresce no 2º dia.",outfit,18,GRAY)
cx,cy,cw,ch=M,350,W-2*M,162
shadow(cx,cy,cw,ch,22); rrect(cx,cy,cw,ch,22,CARD,z=2)
txt(cx+34,cy+46,"FALTARAM NO 2º DIA",mono,13,GRAY)
txt(cx+32,cy+108,"1,5 milhão",outfitB,52,CORAL)
txt(cx+34,cy+142,"de 4,8 mi de inscritos · +200 mil foram no sábado e desistiram no domingo",outfit,15.5,GRAY)
assin(M,560); txt(W-M,560,"Fonte: Microdados ENEM 2025 / INEP (TP_PRESENCA)",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_abstencao_capa.png",dpi=300,facecolor=BG); plt.close(fig); print("capa ok")

# ---------- DIA1 x DIA2 1200x600 ----------
W,H=1200,600; M=64; fig,ax,tw,txt,rrect,shadow,logo,assin=base(W,H)
logo(M+22,54); txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,56,"ENEM 2025 · ABSTENÇÃO · INEP",mono,12,GRAY,ha="right")
txt(M,118,"Faltou mais no domingo",outfitB,34,INK)
txt(M,150,"Abstenção por dia de prova (% dos 4,8 mi de inscritos). A desistência sobe +4,2 pontos no 2º dia.",outfit,15.5,GRAY)
rows=[("DIA 1","Humanas · Linguagens · Redação",28.0,AMBER,AMBER_BG),
      ("DIA 2","Natureza · Matemática",32.2,PINK,PINK_BG)]
bx0,bx1=300,1010; SC=40.0
def xv(v): return bx0+(v/SC)*(bx1-bx0)
y0=230; rh=120
for i,(dia,sub,v,col,bg) in enumerate(rows):
    yc=y0+i*rh
    txt(M,yc-2,dia,outfitB,24,INK); txt(M,yc+26,sub,outfit,12.5,GRAY)
    ax.add_line(Line2D([bx0,bx1],[yc+4,yc+4],color="#E3E5E7",lw=18,solid_capstyle="round",zorder=2))
    ax.add_line(Line2D([bx0,xv(v)],[yc+4,yc+4],color=col,lw=18,solid_capstyle="round",zorder=3.5))
    txt(xv(v)+18,yc+4,f"{v:.1f}%".replace(".",","),outfitB,26,INK,va="center")
# +4,2 callout
txt(xv(28.0)+2, y0+rh-30, "↑ +4,2 pontos do sábado para o domingo", mono,12.5, CORALd)
for g in [0,10,20,30,40]:
    txt(xv(g),y0+rh+58,f"{g}%",mono,11,GRAY,ha="center")
# nota lateral
rrect(M,y0+rh+86,W-2*M,0.1,1,BG,z=1)
txt(M,y0+rh+92,"Cerca de 200 mil pessoas foram no 1º dia e desistiram do 2º · ~1 em cada 3 inscritos não fez a prova.",outfit,14.5,INK)
assin(M,H-44); txt(W-M,H-45,"Microdados ENEM 2025 / INEP · presença (TP_PRESENCA)",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_abstencao_dia1_dia2.png",dpi=300,facecolor=BG); plt.close(fig); print("grafico ok")
print("FIM")
