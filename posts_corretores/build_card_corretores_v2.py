#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Card A6 no PADRAO VISUAL XTRI (replica do template do usuario).
Numeros reais: Microdados ENEM 2025 / INEP (RESULTADOS_2025.csv)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FD="/sessions/brave-sharp-fermi/mnt/.claude/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB=F("Outfit-Bold"); outfit=F("Outfit-Regular")
mono=F("JetBrainsMono-Regular"); monoB=F("JetBrainsMono-Bold")

# ---- PALETA (do template XTRI) ----
BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"; GRAYv="#A8ADB3"
CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
CHIP_BG="#FBE3DC"; CHIP_TX="#E8431F"; ROW_HL="#FCEDE8"
BADGE_CY_BG="#DCF0FB"; BADGE_CO_BG="#FBDDD3"
TRACK="#E3E5E7"; BARFILL="#C5CACF"; CTA_BG="#1B1B1E"; CTA_SUB="#9AA0A6"

W,H=1080,1350
fig=plt.figure(figsize=(W/100,H/100),dpi=300)
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
fig.canvas.draw(); R=fig.canvas.get_renderer()
PXU=fig.get_size_inches()[0]*fig.dpi/W   # px por unidade de dado

def tw(s,fp,size):
    t=ax.text(0,0,s,fontproperties=fp,fontsize=size); fig.canvas.draw()
    w=t.get_window_extent(R).width/PXU; t.remove(); return w
def txt(x,y,s,fp,size,color=INK,ha="left",va="baseline",z=5,alpha=1):
    return ax.text(x,y,s,fontproperties=fp,fontsize=size,color=color,ha=ha,va=va,zorder=z,alpha=alpha)
def rrect(x,y,w,h,rad,fc,ec="none",lw=0,z=2,alpha=1):
    p=FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",
                     fc=fc,ec=ec,lw=lw,zorder=z,alpha=alpha,mutation_aspect=1); ax.add_patch(p); return p
def shadow(x,y,w,h,rad):
    for i in range(1,9):
        rrect(x-1.0*i, y+2.4+1.7*i, w+2.0*i, h+1.0*i, rad+1.2*i, "#000000", z=1.5, alpha=0.012)

M=72  # margem lateral

# ===== LOGO (topo-esq) =====
try:
    lg=mpimg.imread("/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/logo_xtri_marca_real.png")
    ab=AnnotationBbox(OffsetImage(lg,zoom=0.115),(M+30,82),frameon=False,box_alignment=(0.5,0.5),zorder=6)
    ax.add_artist(ab)
except Exception as e:
    pass
txt(M,140,"X-TRI",outfitB,16,CYANd)

# ===== KICKER (topo-dir) =====
txt(W-M,100,"REDAÇÃO · ENEM",outfitB,16.5,INK,ha="right")
txt(W-M,128,"ENEM 2025",mono,13.5,GRAY,ha="right")

# ===== HEADLINE =====
txt(M,250,"O “azar de corretor”",outfitB,62,INK)
x=M; y=326
x+=0; txt(x,y,"tem ",outfitB,62,INK); x+=tw("tem ",outfitB,62)
txt(x,y,"limite",outfitB,62,CORAL); x+=tw("limite",outfitB,62)
txt(x,y,".",outfitB,62,INK)

# ===== SUBHEAD =====
ys=388
a="Dois corretores independentes"; b=" avaliam cada redação — e concordam muito."
txt(M,ys,a,outfitB,20.5,INK); txt(M+tw(a,outfitB,20.5),ys,b,outfit,20.5,GRAY)

# ===== HERO CARD =====
hx,hy,hw,hh=M,430,W-2*M,172
shadow(hx,hy,hw,hh,28); rrect(hx,hy,hw,hh,28,CARD,z=2)
txt(hx+40,hy+52,"DIFERENÇA ENTRE OS DOIS",mono,14.5,GRAY)
txt(hx+40,hy+96,"no máximo 80 pontos",outfitB,29,INK)
txt(hx+40,hy+130,"(escala de 0 a 1000)",outfit,16.5,GRAY)
# numero heroi (dir)
hn="67,5"; sz=92
xpct=hx+hw-40
wpe=tw("%",outfitB,50); wnum=tw(hn,outfitB,sz)
txt(xpct, hy+128, "%", outfitB, 50, CORAL, ha="right")
txt(xpct-wpe-6, hy+128, hn, outfitB, sz, CORAL, ha="right")

# ===== ROWS =====
txt(M,648,"DIVERGÊNCIA MÉDIA ENTRE OS DOIS CORRETORES · POR COMPETÊNCIA (CADA UMA 0–200)",mono,12.5,GRAY)
rx,ry,rw,rh=M,662,W-2*M,432
shadow(rx,ry,rw,rh,28); rrect(rx,ry,rw,rh,28,CARD,z=2)
rows=[("C1","Norma culta",20.7),("C2","Compreensão do tema",21.5),
      ("C3","Argumentação",22.0),("C4","Coesão",24.2),("C5","Proposta interv.",26.3)]
maxv=26.3
bx0,bx1=430,812
top=ry+54; bot=ry+rh-58; step=(bot-top)/4.0
for i,(code,name,val) in enumerate(rows):
    yc=top+i*step
    hl=(code=="C5")
    if hl: rrect(rx+24,yc-34,rw-48,68,18,ROW_HL,z=2.4)
    # badge
    rrect(rx+30,yc-19,52,38,12, BADGE_CO_BG if hl else BADGE_CY_BG, z=3)
    txt(rx+56,yc+1,code,monoB,15.5, CORALd if hl else CYANd, ha="center",va="center",z=4)
    # nome
    txt(rx+102,yc+1,name,outfitB,20.5,INK,va="center",z=4)
    # barra
    ax.add_line(Line2D([bx0,bx1],[yc+1,yc+1],color=TRACK,lw=9,solid_capstyle="round",zorder=3))
    xe=bx0+(val/maxv)*(bx1-bx0)
    ax.add_line(Line2D([bx0,xe],[yc+1,yc+1],color=(CORAL if hl else BARFILL),lw=9,solid_capstyle="round",zorder=3.5))
    # chip valor (recuado da borda do card)
    cw,ch=116,40; cxx=rx+rw-46-cw
    rrect(cxx,yc-ch/2,cw,ch,13, CORAL if hl else CHIP_BG, z=3.2)
    txt(cxx+cw/2,yc+1,f"{val:.1f}".replace(".",","),monoB,17, "#FFFFFF" if hl else CHIP_TX, ha="center",va="center",z=4)

# ===== TAKEAWAY =====
ty=1134
t1="Passou de 80 pontos de diferença? Entra um "; t2="3º corretor"; t3=" — 1 em cada 3 redações."
txt(M,ty,t1,outfit,17.5,INK); xx=M+tw(t1,outfit,17.5)
txt(xx,ty,t2,outfitB,17.5,CORALd); xx+=tw(t2,outfitB,17.5)
txt(xx,ty,t3,outfit,17.5,INK)

# ===== FOOTER =====
txt(M,1192,"@xandaoxtri",outfitB,30,INK)
fy=1232
s1="Dados reais"; s2=" ou "; s3="nada"; s4="."
txt(M,fy,s1,outfitB,25,CYAN); xx=M+tw(s1,outfitB,25)
txt(xx,fy,s2,outfitB,25,INK); xx+=tw(s2,outfitB,25)
txt(xx,fy,s3,outfitB,25,CORAL); xx+=tw(s3,outfitB,25)
txt(xx,fy,s4,outfitB,25,INK)
txt(M,1266,"diferença por competência · ENEM 2025 / INEP",mono,12.5,GRAY)

# CTA botao
cax,cay,caw,cah=556,1182,W-M-556,104
rrect(cax,cay,caw,cah,24,CTA_BG,z=3)
txt(cax+32,cay+42,"VEJA O ESTUDO COMPLETO",mono,12.5,CTA_SUB)
txt(cax+32,cay+78,"app.rankingenem.com/redacao →",monoB,15.5,"#FFFFFF")

out="/sessions/brave-sharp-fermi/mnt/outputs/card_corretores_A6.png"
fig.savefig(out,dpi=300,facecolor=BG); print("salvo",out)
