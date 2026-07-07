#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Graficos para post WordPress (paisagem) — dificuldade por sequencia PPL. Branding XTRI.
Dados reais: Microdados ENEM 2025 / INEP (TRI dos itens da 2a aplicacao)."""
import json, os
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
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/estudo_dificuldade_ppl"
OUT="/sessions/brave-sharp-fermi/mnt/outputs/wp"; os.makedirs(OUT,exist_ok=True)
D=json.load(open(f"{BASE}/ppl_sequencia_data.json"))
BG="#F1F1F2"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
CAT_C={"Fácil":"#56C2F2","Médio":"#C7CBD0","Difícil":"#FB9276","Muito difícil":"#FA5230"}
AREAF={"MT":"Matemática","CN":"Natureza","CH":"Humanas","LC":"Linguagens"}
PAIR={"MT":(3,5),"CN":(29,28),"CH":(25,26),"LC":(17,15)}

def newfig(W,H):
    fig=plt.figure(figsize=(W/100,H/100),dpi=300); ax=fig.add_axes([0,0,1,1])
    ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
    fig.canvas.draw()
    return fig,ax
def mk(fig,ax,W):
    R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
    def tw(s,fp,sz):
        t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw(); w=t.get_window_extent(R).width/PXU; t.remove(); return w
    def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
        return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
    def rrect(x,y,w,h,rad,fc,z=2,ec="none",lw=0):
        ax.add_patch(FancyBboxPatch((x+rad,y+rad),max(w-2*rad,1),max(h-2*rad,1),boxstyle=f"round,pad={rad}",fc=fc,ec=ec,lw=lw,zorder=z,mutation_aspect=1))
    return tw,txt,rrect
def logo(ax,x,y,z=0.085):
    try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=z),(x,y),frameon=False,box_alignment=(0.5,0.5),zorder=6))
    except Exception: pass

# ---------- 1) FEATURED 1200x630 ----------
W,H=1200,630; fig,ax=newfig(W,H); tw,txt,rrect=mk(fig,ax,W); M=64
logo(ax,M+22,58,0.078); txt(M+50,64,"X-TRI",outfitB,15,CYANd)
txt(W-M,58,"ANÁLISE XTRI · TRI",outfitB,14,INK,ha="right")
txt(W-M,82,"ENEM 2025 · 2ª APLICAÇÃO (PPL)",mono,11.5,GRAY,ha="right")
txt(M,210,"Não faça o ENEM",outfitB,66,INK)
x=M; y=288; txt(x,y,"na ordem",outfitB,66,CORAL); x+=tw("na ordem",outfitB,66); txt(x,y,".",outfitB,66,INK)
txt(M,338,"A 2ª aplicação (PPL) prova pela TRI: questões fáceis e quase impossíveis,",outfit,19,GRAY)
txt(M,365,"lado a lado, na mesma região do caderno.",outfit,19,GRAY)
# chips de contraste
def chip(x,y,lab,val,col):
    w=300; rrect(x,y,w,70,16,"#FFFFFF",z=3)
    txt(x+20,y+30,lab,mono,12.5,GRAY); txt(x+20,y+56,val,outfitB,22,col); return w
chip(M,430,"MAT · P03 (difícil)","DIF 95 · ~5% esperado",CORALd)
chip(M+330,430,"MAT · P05 (ao lado)","DIF 14 · ~86% esperado",CYANd)
txt(M+672,475,"mesma\nregião",outfit,16,INK)
txt(M,560,"Dados reais",outfitB,20,CYAN); xx=M+tw("Dados reais",outfitB,20)
txt(xx,560,(" ou "),outfitB,20,INK); xx+=tw(" ou ",outfitB,20); txt(xx,560,"nada",outfitB,20,CORAL); xx+=tw("nada",outfitB,20); txt(xx,560,".",outfitB,20,INK)
txt(W-M,560,"app.rankingenem.com",mono,13,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_ppl_wp_featured.png",dpi=300,facecolor=BG); plt.close(fig); print("featured ok")

# ---------- 2) CONTRASTE 1200x810 ----------
W,H=1200,810; fig,ax=newfig(W,H); tw,txt,rrect=mk(fig,ax,W); M=64
logo(ax,M+22,54,0.072); txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,56,"PPL · 2ª APLICAÇÃO · CADERNO AZUL",mono,12,GRAY,ha="right")
txt(M,120,"Mesma região, dois mundos",outfitB,38,INK)
txt(M,152,"Acerto esperado (aluno mediano, TRI) da questão mais difícil e da fácil vizinha",outfit,16.5,GRAY)
pairs=[("MT",3,5),("CN",29,28),("CH",25,26),("LC",17,15)]
its={ar:{x["pos"]:x for x in D[ar]["items"]} for ar in D}
y0=220; rowh=118; bx0=250; bx1=1010  # escala 0..100%
def xval(v): return bx0+(v/100)*(bx1-bx0)
for i,(ar,hp,ep) in enumerate(pairs):
    yc=y0+i*rowh; h=its[ar][hp]; e=its[ar][ep]
    txt(M,yc+8,AREAF[ar],outfitB,21,INK)
    txt(M,yc+34,("adjacentes" if abs(hp-ep)==1 else f"{abs(hp-ep)} posições"),mono,11.5,GRAY)
    # barra facil (cyan) e dificil (coral)
    for j,(it,col,tag) in enumerate([(e,CYAN,"fácil"),(h,CORAL,"difícil")]):
        by=yc-6+j*40
        ax.add_line(Line2D([bx0,bx1],[by,by],color="#E3E5E7",lw=14,solid_capstyle="round",zorder=2))
        ax.add_line(Line2D([bx0,xval(it["esp"])],[by,by],color=col,lw=14,solid_capstyle="round",zorder=3))
        txt(xval(it["esp"])+14,by+5,f'P{it["pos"]:02d} ({it["hab"]}) · ~{it["esp"]:.0f}%  ·  DIF {it["dif"]:.0f}',outfitB,14,INK,va="center")
# eixo
for g in [0,25,50,75,100]:
    ax.add_line(Line2D([xval(g),xval(g)],[206,y0+4*rowh-30],color="#D8DADD",lw=1,zorder=1))
    txt(xval(g),y0+4*rowh-10,f"{g}%",mono,11,GRAY,ha="center")
txt(M,H-46,"Dados reais",outfitB,17,CYAN); xx=M+tw("Dados reais",outfitB,17)
txt(xx,H-46," ou ",outfitB,17,INK); xx+=tw(" ou ",outfitB,17); txt(xx,H-46,"nada",outfitB,17,CORAL); xx+=tw("nada",outfitB,17); txt(xx,H-46,".",outfitB,17,INK)
txt(W-M,H-47,"Microdados ENEM 2025/INEP · dificuldade pela TRI · PPL sem acerto observado",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_ppl_wp_contraste.png",dpi=300,facecolor=BG); plt.close(fig); print("contraste ok")

# ---------- 3) SKYLINE 1200x920 (4 areas, DIF por posicao) ----------
W,H=1200,920; fig,ax=newfig(W,H); tw,txt,rrect=mk(fig,ax,W); M=64
logo(ax,M+22,54,0.072); txt(M+48,60,"X-TRI",outfitB,14,CYANd)
txt(W-M,56,"PPL · 2ª APLICAÇÃO · CADERNO AZUL",mono,12,GRAY,ha="right")
txt(M,118,"A dificuldade não cresce em ordem",outfitB,34,INK)
txt(M,148,"DIF TRI por posição (P01→P45) em cada área · vermelho = par mais difícil destacado",outfit,15.5,GRAY)
order=["MT","CN","CH","LC"]; py0=182; ph=146
for i,ar in enumerate(order):
    yc=py0+i*ph; items=sorted(D[ar]["items"],key=lambda x:x["pos"])
    txt(M,yc+14,AREAF[ar],outfitB,18,INK)
    bx0=200; bx1=W-M; n=45; bw=(bx1-bx0)/n; base=yc+ph-52; top=yc+8
    for x in items:
        if x.get("aban"): continue
        col=CAT_C[x["cat"]]; hgt=(x["dif"]/100)*(base-top)
        bx=bx0+(x["pos"]-1)*bw
        rrect(bx+1,base-hgt,bw-2,hgt,2,col,z=3)
        hp,ep=PAIR[ar]
        if x["pos"] in (hp,ep):
            ax.add_patch(FancyBboxPatch((bx+1+1,base-hgt+1),bw-4,hgt-2,boxstyle="square,pad=0",fc="none",ec=(CORALd if x["pos"]==hp else CYANd),lw=2,zorder=4))
            txt(bx+bw/2,base-hgt-6,f'P{x["pos"]:02d}',monoB,8.5,(CORALd if x["pos"]==hp else CYANd),ha="center")
    ax.add_line(Line2D([bx0,bx1],[base,base],color="#CFD2D5",lw=1,zorder=2))
    txt(bx0-8,base,"P01",mono,9,GRAY,ha="right",va="center"); txt(bx1,base+16,"P45",mono,9,GRAY,ha="right")
# legenda cores
lx=M; ly=H-92
for cat in ["Fácil","Médio","Difícil","Muito difícil"]:
    rrect(lx,ly-12,16,16,4,CAT_C[cat],z=3); txt(lx+24,ly+2,cat,mono,11.5,INK); lx+=tw(cat,mono,11.5)+56
txt(M,H-52,"Dados reais",outfitB,17,CYAN); xx=M+tw("Dados reais",outfitB,17)
txt(xx,H-52," ou ",outfitB,17,INK); xx+=tw(" ou ",outfitB,17); txt(xx,H-52,"nada",outfitB,17,CORAL); xx+=tw("nada",outfitB,17); txt(xx,H-52,".",outfitB,17,INK)
txt(W-M,H-52,"DIF TRI = 100×(1−P(θ=0)) · Microdados ENEM 2025/INEP",mono,9.5,GRAY,ha="right")
fig.savefig(f"{OUT}/xtri_ppl_wp_skyline.png",dpi=300,facecolor=BG); plt.close(fig); print("skyline ok")
print("FIM")
