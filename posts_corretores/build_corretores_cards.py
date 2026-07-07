#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Card A6 'azar de corretor' — PADRAO VISUAL XTRI. Gera SEMPRE feed + story.
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
LOGO="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/logo_xtri_marca_real.png"

BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"
CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
CHIP_BG="#FBE3DC"; CHIP_TX="#E8431F"; ROW_HL="#FCEDE8"
BADGE_CY_BG="#DCF0FB"; BADGE_CO_BG="#FBDDD3"
TRACK="#E3E5E7"; BARFILL="#C5CACF"; CTA_BG="#1B1B1E"; CTA_SUB="#9AA0A6"
M=72; W=1080
ROWS=[("C1","Norma culta",20.7),("C2","Compreensão do tema",21.5),
      ("C3","Argumentação",22.0),("C4","Coesão",24.2),("C5","Proposta interv.",26.3)]

# layouts por formato (so as coordenadas verticais mudam)
LAY={
 "feed":  dict(H=1350, logoy=82, logoz=0.115, wmy=140, k1=100,k2=128,
   h1=250,h2=326,hsz=62, suby=388, heroy=430,heroh=172, hnum=92,hpct=50,
   hlab=52,hval=96,hsub=130,hnumy=128, mety=648, rowsy=662,rowsh=432,rtop=54,rbot=58,
   taky=1134, fhandle=1192,fdados=1232,fcap=1266, ctay=1182,ctah=104),
 "story": dict(H=1920, logoy=168, logoz=0.135, wmy=236, k1=188,k2=222,
   h1=372,h2=470,hsz=64, suby=566, heroy=650,heroh=214, hnum=104,hpct=56,
   hlab=58,hval=116,hsub=154,hnumy=150, mety=918, rowsy=956,rowsh=600,rtop=68,rbot=72,
   taky=1592, fhandle=1666,fdados=1712,fcap=1748, ctay=1652,ctah=116),
}

def render(fmt):
    L=LAY[fmt]; H=L["H"]
    fig=plt.figure(figsize=(W/100,H/100),dpi=300)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
    fig.canvas.draw(); R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
    def tw(s,fp,sz):
        t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw()
        w=t.get_window_extent(R).width/PXU; t.remove(); return w
    def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
        return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
    def rrect(x,y,w,h,rad,fc,z=2,alpha=1):
        ax.add_patch(FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",
                     fc=fc,ec="none",zorder=z,alpha=alpha,mutation_aspect=1))
    def shadow(x,y,w,h,rad):
        for i in range(1,9): rrect(x-1.0*i,y+2.4+1.7*i,w+2.0*i,h+1.0*i,rad+1.2*i,"#000000",z=1.5,alpha=0.012)

    # LOGO + wordmark
    try:
        ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=L["logoz"]),
            (M+30,L["logoy"]),frameon=False,box_alignment=(0.5,0.5),zorder=6))
    except Exception: pass
    txt(M,L["wmy"],"X-TRI",outfitB,16,CYANd)
    # KICKER
    txt(W-M,L["k1"],"REDAÇÃO · ENEM",outfitB,16.5,INK,ha="right")
    txt(W-M,L["k2"],"ENEM 2025",mono,13.5,GRAY,ha="right")
    # HEADLINE
    txt(M,L["h1"],"O “azar de corretor”",outfitB,L["hsz"],INK)
    x=M; y=L["h2"]; txt(x,y,"tem ",outfitB,L["hsz"],INK); x+=tw("tem ",outfitB,L["hsz"])
    txt(x,y,"limite",outfitB,L["hsz"],CORAL); x+=tw("limite",outfitB,L["hsz"]); txt(x,y,".",outfitB,L["hsz"],INK)
    # SUBHEAD
    a="Dois corretores independentes"; b=" avaliam cada redação — e concordam muito."
    txt(M,L["suby"],a,outfitB,20.5,INK); txt(M+tw(a,outfitB,20.5),L["suby"],b,outfit,20.5,GRAY)
    # HERO CARD
    hx,hy,hw,hh=M,L["heroy"],W-2*M,L["heroh"]
    shadow(hx,hy,hw,hh,28); rrect(hx,hy,hw,hh,28,CARD,z=2)
    txt(hx+40,hy+L["hlab"],"DIFERENÇA ENTRE OS DOIS",mono,14.5,GRAY)
    txt(hx+40,hy+L["hval"],"no máximo 80 pontos",outfitB,29,INK)
    txt(hx+40,hy+L["hsub"],"(escala de 0 a 1000)",outfit,16.5,GRAY)
    xpct=hx+hw-40
    txt(xpct,hy+L["hnumy"],"%",outfitB,L["hpct"],CORAL,ha="right")
    txt(xpct-tw("%",outfitB,L["hpct"])-6,hy+L["hnumy"],"67,5",outfitB,L["hnum"],CORAL,ha="right")
    # METRIC LABEL
    txt(M,L["mety"],"DIVERGÊNCIA MÉDIA ENTRE OS DOIS CORRETORES · POR COMPETÊNCIA (CADA UMA 0–200)",mono,12.5,GRAY)
    # ROWS CARD
    rx,ry,rw,rh=M,L["rowsy"],W-2*M,L["rowsh"]
    shadow(rx,ry,rw,rh,28); rrect(rx,ry,rw,rh,28,CARD,z=2)
    maxv=26.3; bx0,bx1=430,812
    top=ry+L["rtop"]; bot=ry+rh-L["rbot"]; step=(bot-top)/4.0
    for i,(code,name,val) in enumerate(ROWS):
        yc=top+i*step; hl=(code=="C5")
        if hl: rrect(rx+24,yc-34,rw-48,68,18,ROW_HL,z=2.4)
        rrect(rx+30,yc-19,52,38,12, BADGE_CO_BG if hl else BADGE_CY_BG, z=3)
        txt(rx+56,yc+1,code,monoB,15.5, CORALd if hl else CYANd, ha="center",va="center",z=4)
        txt(rx+102,yc+1,name,outfitB,20.5,INK,va="center",z=4)
        ax.add_line(Line2D([bx0,bx1],[yc+1,yc+1],color=TRACK,lw=9,solid_capstyle="round",zorder=3))
        xe=bx0+(val/maxv)*(bx1-bx0)
        ax.add_line(Line2D([bx0,xe],[yc+1,yc+1],color=(CORAL if hl else BARFILL),lw=9,solid_capstyle="round",zorder=3.5))
        cw,ch=116,40; cxx=rx+rw-46-cw
        rrect(cxx,yc-ch/2,cw,ch,13, CORAL if hl else CHIP_BG, z=3.2)
        txt(cxx+cw/2,yc+1,f"{val:.1f}".replace(".",","),monoB,17, "#FFFFFF" if hl else CHIP_TX, ha="center",va="center",z=4)
    # TAKEAWAY
    ty=L["taky"]; t1="Passou de 80 pontos de diferença? Entra um "; t2="3º corretor"; t3=" — 1 em cada 3 redações."
    txt(M,ty,t1,outfit,17.5,INK); xx=M+tw(t1,outfit,17.5)
    txt(xx,ty,t2,outfitB,17.5,CORALd); xx+=tw(t2,outfitB,17.5); txt(xx,ty,t3,outfit,17.5,INK)
    # FOOTER
    txt(M,L["fhandle"],"@xandaoxtri",outfitB,30,INK)
    fy=L["fdados"]; s1="Dados reais"; s2=" ou "; s3="nada"; s4="."
    txt(M,fy,s1,outfitB,25,CYAN); xx=M+tw(s1,outfitB,25)
    txt(xx,fy,s2,outfitB,25,INK); xx+=tw(s2,outfitB,25)
    txt(xx,fy,s3,outfitB,25,CORAL); xx+=tw(s3,outfitB,25); txt(xx,fy,s4,outfitB,25,INK)
    txt(M,L["fcap"],"diferença por competência · ENEM 2025 / INEP",mono,12.5,GRAY)
    cax,cay,caw,cah=556,L["ctay"],W-M-556,L["ctah"]
    rrect(cax,cay,caw,cah,24,CTA_BG,z=3)
    txt(cax+32,cay+42,"VEJA O ESTUDO COMPLETO",mono,12.5,CTA_SUB)
    txt(cax+32,cay+78,"app.rankingenem.com/redacao →",monoB,15.5,"#FFFFFF")

    out=f"/sessions/brave-sharp-fermi/mnt/outputs/card_corretores_A6_{fmt}.png"
    fig.savefig(out,dpi=300,facecolor=BG); plt.close(fig); print("salvo",out)

for f in ("feed","story"): render(f)
