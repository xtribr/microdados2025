#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cards 'sequencia de dificuldade' — PPL/2a aplicacao, padrao XTRI, feed+story.
DIF/acerto = MODELO 3PL (a,b,c reais). PPL nao tem taxa de acerto observada."""
import sys, os, json
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
OUT="/sessions/brave-sharp-fermi/mnt/outputs/ppl_seq"; os.makedirs(OUT,exist_ok=True)
DATA=json.load(open(f"{BASE}/ppl_sequencia_data.json"))

BG="#F1F1F2"; INK="#1D1D20"; GRAY="#8C9298"; CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
CAT_BG={"Fácil":"#E7F4FB","Médio":"#E9EAEC","Difícil":"#FBE0D7","Muito difícil":"#FA5230"}
CAT_TX={"Fácil":INK,"Médio":INK,"Difícil":CORALd,"Muito difícil":"#FFFFFF"}
CAT_SUB={"Fácil":CYANd,"Médio":GRAY,"Difícil":CORALd,"Muito difícil":"#FFE3DC"}
AREAF={"MT":"Matemática","CN":"Ciências da Natureza","CH":"Ciências Humanas","LC":"Linguagens e Códigos"}
PAIR={"MT":(3,5),"CN":(29,28),"CH":(25,26),"LC":(17,15)}  # (hard pos, easy pos)
W=1080; M=66

def make(ar, fmt):
    d=DATA[ar]; items={x["pos"]:x for x in d["items"]}
    H=1350 if fmt=="feed" else 1920
    fig=plt.figure(figsize=(W/100,H/100),dpi=300)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
    fig.canvas.draw(); R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
    def tw(s,fp,sz):
        t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw(); w=t.get_window_extent(R).width/PXU; t.remove(); return w
    def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
        return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
    def rrect(x,y,w,h,rad,fc,z=2,ec="none",lw=0):
        ax.add_patch(FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",fc=fc,ec=ec,lw=lw,zorder=z,mutation_aspect=1))
    # logo + kicker
    try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=0.10),(M+26,74),frameon=False,box_alignment=(0.5,0.5),zorder=6))
    except Exception: pass
    txt(M,126,"X-TRI",outfitB,15,CYANd)
    txt(W-M,98,"DIFICULDADE POR QUESTÃO",outfitB,15,INK,ha="right")
    txt(W-M,124,"PPL · 2ª APLICAÇÃO",mono,13,CORALd,ha="right")
    # titulo + subt + stats
    txt(M,196,f"{AREAF[ar]}: sequência de dificuldade",outfitB,31,INK)
    txt(M,228,"Caderno Azul · 2ª aplicação (PPL) · dificuldade pela TRI, sem taxa de acerto observada",outfit,15,GRAY)
    hardp,easyp=PAIR[ar]; h=items[hardp]; e=items[easyp]
    txt(M,262,f"2ª aplicação · {d['n_valid']} válidas · {d['n_aban']} anuladas · A média {d['media_a']:.2f} · DIF média {d['media_dif']:.0f}",mono,13,INK)
    # barra de distribuicao
    by=284; bw=W-2*M; tot=sum(d["dist"].values()); x=M
    for cat in ["Fácil","Médio","Difícil","Muito difícil"]:
        seg=bw*d["dist"][cat]/tot
        rrect(x,by,seg-3,18,5,CAT_BG[cat],z=3)
        x+=seg
    # grade 9x5
    bottom=262 if fmt=="feed" else 322; gy0=330; gh=H-330-bottom; rows=5; cols=9
    cw=(W-2*M)/cols; chh=gh/rows; gap=5
    for pos in range(1,46):
        it=items.get(pos)
        col=(pos-1)%cols; row=(pos-1)//cols
        cx=M+col*cw; cy=gy0+row*chh
        if it is None or it.get("aban"):
            rrect(cx,cy,cw-gap,chh-gap,10,"#E2E3E5",z=2)
            txt(cx+(cw-gap)/2,cy+chh/2-6,f"P{pos:02d}",monoB,10,GRAY,ha="center")
            txt(cx+(cw-gap)/2,cy+chh/2+14,"ANUL.",mono,8.5,GRAY,ha="center"); continue
        cat=it["cat"]; rrect(cx,cy,cw-gap,chh-gap,10,CAT_BG[cat],z=2)
        # destaque do par
        if pos==hardp: rrect(cx,cy,cw-gap,chh-gap,10,"#00000000",z=4,ec=CORALd,lw=3)
        if pos==easyp: rrect(cx,cy,cw-gap,chh-gap,10,"#00000000",z=4,ec=CYANd,lw=3)
        tc=CAT_TX[cat]; sc=CAT_SUB[cat]
        txt(cx+12,cy+22,f"P{pos:02d}",monoB,11,tc)
        txt(cx+cw-gap-12,cy+22,it["hab"],mono,10,sc,ha="right")
        txt(cx+(cw-gap)/2,cy+chh*0.52,f'{it["esp"]:.0f}%',outfitB,23,tc,ha="center",va="center")
        txt(cx+(cw-gap)/2,cy+chh-24,f'DIF {it["dif"]:.0f} · {it["tier"]}',mono,9,sc,ha="center",va="center")
    # legenda categorias
    ly=gy0+gh+26; lx=M
    for cat in ["Fácil","Médio","Difícil","Muito difícil"]:
        rrect(lx,ly-12,16,16,4,CAT_BG[cat],z=3); txt(lx+24,ly+2,cat,mono,11.5,INK); lx+=tw(cat,mono,11.5)+54
    txt(W-M,ly+2,"contorno vermelho = mais difícil · azul = a fácil vizinha",mono,10.5,GRAY,ha="right")
    # callout do contraste
    coy=ly+42
    txt(M,coy,f'P{hardp:02d} ({h["hab"]}) DIF {h["dif"]:.0f} ≈ {h["esp"]:.0f}% esperado',outfitB,16,CORALd)
    txt(M,coy+26,f'colada na P{easyp:02d} ({e["hab"]}) DIF {e["dif"]:.0f} ≈ {e["esp"]:.0f}% — não faça na ordem.',outfit,16,INK)
    # rodape
    fy=H-60
    txt(M,fy-22,"DIF TRI = 100×(1−P(θ=0)) pelos a,b,c oficiais · acerto = esperado do aluno mediano · PPL sem acerto observado.",mono,10.5,GRAY)
    txt(M,fy+8,"@xandaoxtri",outfitB,22,INK)
    xx=M+tw("@xandaoxtri",outfitB,22)+24
    for t,cc in [("Dados reais",CYAN),(" ou ",INK),("nada",CORAL),(".",INK)]: txt(xx,fy+8,t,outfitB,19,cc); xx+=tw(t,outfitB,19)
    txt(W-M,fy+8,"Microdados ENEM 2025 / INEP",mono,11,GRAY,ha="right")
    p=f"{OUT}/ppl_seq_{ar}_{fmt}.png"; fig.savefig(p,dpi=300,facecolor=BG); plt.close(fig); print("ok",os.path.basename(p))

mode=sys.argv[1] if len(sys.argv)>1 else "all"
if mode=="one": make("MT","feed")
else:
    for ar in ["MT","CN","CH","LC"]:
        for fmt in ("feed","story"): make(ar,fmt)
print("FIM")
