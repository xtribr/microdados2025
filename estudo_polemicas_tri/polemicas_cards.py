#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cards 'As 10 mais polemicas por TRI' — padrao XTRI, feed+story, com print real da questao.
Dificuldade TRI = b*100+500. Numeros reais: Microdados ENEM 2025 / INEP."""
import sys, os, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

FD="/sessions/brave-sharp-fermi/mnt/.claude/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB=F("Outfit-Bold"); outfit=F("Outfit-Regular"); mono=F("JetBrainsMono-Regular"); monoB=F("JetBrainsMono-Bold")
LOGO="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/logo_xtri_marca_real.png"
CROPS="/sessions/brave-sharp-fermi/mnt/outputs/crops"
OUT="/sessions/brave-sharp-fermi/mnt/outputs/cards"; os.makedirs(OUT,exist_ok=True)

BG="#F1F1F2"; CARD="#FFFFFF"; INK="#1D1D20"; GRAY="#8C9298"
CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"
CHIP="#F4F5F6"; CTA_BG="#1B1B1E"; CTA_SUB="#9AA0A6"
M=72; W=1080
AREA={"CN":"Ciências da Natureza","MT":"Matemática","LC":"Linguagens","CH":"Ciências Humanas"}

ITEMS=[
 dict(n=1,tema="Matemática básica",area="MT",q=146,crop="04_matbasica_Q146",a="1,25",dif="585",c="21%",ac="53%",ipt="83,6",
   reason="Uma subtração de decimais (10,00−9,58), mas discrimina pouco (a=1,25) e o acerto veio acima do previsto."),
 dict(n=2,tema="Interpretação de textos",area="LC",q=35,crop="08_interpretacao_Q35",a="1,26",dif="631",c="28%",ac="47%",ipt="79,9",
   reason="Discriminação baixa (a=1,26) somada a chute alto: 28% podem acertar sem dominar o texto."),
 dict(n=3,tema="Física",area="CN",q=122,crop="03_fisica_Q122",a="2,30",dif="665",c="32%",ac="29%",ipt="76,9",
   reason="Boa discriminação, mas c=32%: quase 1 em 3 acerta no chute, e desvia do previsto."),
 dict(n=4,tema="Química",area="CN",q=100,crop="02_quimica_Q100",a="1,13",dif="478",c="21%",ac="60%",ipt="76,7",
   reason="Item fácil (60% de acerto), porém discrimina pouco (a=1,13): separa mal quem sabe."),
 dict(n=5,tema="Biologia",area="CN",q=96,crop="01_biologia_Q96",a="1,40",dif="506",c="18%",ac="67%",ipt="76,4",
   reason="O maior desajuste do grupo: o modelo previa ~58% de acerto; na prova saíram 67%."),
 dict(n=6,tema="Literatura",area="LC",q=16,crop="06_literatura_Q16",a="1,64",dif="596",c="19%",ac="47%",ipt="73,2",
   reason="Soneto simbolista: discriminação mediana e desajuste entre o previsto e o observado."),
 dict(n=7,tema="Geografia",area="CH",q=63,crop="10_geografia_Q63",a="1,86",dif="615",c="26%",ac="45%",ipt="72,6",
   reason="Puxada pelo chute alto (c=26%) num item de dificuldade mediana."),
 dict(n=8,tema="Artes",area="LC",q=15,crop="07_artes_Q15",a="2,04",dif="574",c="21%",ac="48%",ipt="68,0",
   reason="Boa discriminação, mas entra pelo conjunto: chute e desajuste elevam o índice."),
 dict(n=9,tema="Geometria",area="MT",q=139,crop="05_geometria_Q139",a="1,01",dif="791",c="31%",ac="37%",ipt="67,2",
   reason="O pior item estrutural: a=1,01 (quase não separa), difícil (TRI 791) e chute de 31%."),
 dict(n=10,tema="História",area="CH",q=53,crop="09_historia_Q53",a="2,13",dif="601",c="19%",ac="32%",ipt="59,4",
   reason="Boa discriminação; entra pelo chute moderado e leve desajuste (o menor IPT dos dez)."),
 # --- BONUS: PPL / 2a aplicacao (so TRI, sem taxa de acerto) ---
 dict(n=11,ppl=True,tema="Biologia (evolução)",area="CN",q=98,crop="PPL01_biologia_Q98",a="1,13",dif="632",c="28%",
   reason="Reaplicação (PPL): discrimina pouco (a=1,13) e tem chute alto (28%) — mede pouco e dá para eliminar alternativas."),
 dict(n=12,ppl=True,tema="Geografia (socioambiental)",area="CH",q=79,crop="PPL02_ch_Q79",a="0,66",dif="501",c="23%",
   reason="Reaplicação (PPL): discriminação baixíssima (a=0,66) — a resposta está quase explícita no texto e mal separa quem sabe."),
]
# layout: so coordenadas verticais mudam entre feed e story
LAY={"feed": dict(H=1350, imy=300, imh=506, statY=856, footY=1150),
     "story":dict(H=1920, imy=372, imh=836, statY=1306, footY=1648)}

def make(it, fmt):
    L=LAY[fmt]; H=L["H"]
    fig=plt.figure(figsize=(W/100,H/100),dpi=300)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
    fig.canvas.draw(); R=fig.canvas.get_renderer(); PXU=fig.get_size_inches()[0]*fig.dpi/W
    def tw(s,fp,sz):
        t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw(); w=t.get_window_extent(R).width/PXU; t.remove(); return w
    def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
        return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
    def rrect(x,y,w,h,rad,fc,z=2):
        ax.add_patch(FancyBboxPatch((x+rad,y+rad),w-2*rad,h-2*rad,boxstyle=f"round,pad={rad}",fc=fc,ec="none",zorder=z,mutation_aspect=1))
    def shadow(x,y,w,h,rad):
        for i in range(1,8): rrect(x-i,y+2+1.7*i,w+2*i,h+i,rad+1.1*i,"#000000",z=1.5)
    # logo + kicker
    try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=0.115),(M+30,82),frameon=False,box_alignment=(0.5,0.5),zorder=6))
    except Exception: pass
    txt(M,140,"X-TRI",outfitB,16,CYANd)
    ppl=it.get("ppl",False)
    txt(W-M,100,"MAIS POLÊMICAS · TRI",outfitB,16,INK,ha="right")
    txt(W-M,128,("REAPLICAÇÃO · PPL (P2)" if ppl else f'ENEM 2025 · Nº {it["n"]}/10'),mono,13.5,(CORALd if ppl else GRAY),ha="right")
    # cabecalho: area / tema / questao
    txt(M,200,AREA[it["area"]].upper(),mono,14,GRAY)
    txt(M,252,it["tema"],outfitB,44,INK)
    txt(M,288,f'Questão {it["q"]} · Caderno Azul · '+("2ª aplicação (PPL/P2)" if ppl else "1ª aplicação (P1)"),outfit,17.5,GRAY)
    # card com o print
    ix,iy,iw,ih=M,L["imy"],W-2*M,L["imh"]
    shadow(ix,iy,iw,ih,24); rrect(ix,iy,iw,ih,24,CARD,z=2)
    # ---- faixa IPT (esq) + chips (dir) ----
    sY=L["statY"]
    if ppl:
        txt(M,sY,"TRI DA QUESTÃO · 2ª APLICAÇÃO",mono,12.5,GRAY)
        txt(M,sY+48,"PPL",outfitB,40,CORAL)
        txt(M+tw("PPL",outfitB,40)+12,sY+48,"reaplicação",outfit,19,GRAY)
        txt(M,sY+86,"sem taxa de acerto observada",mono,12.5,CORALd)
        chips=[("DISCRIM. (a)",it["a"]),("DIFIC. TRI",it["dif"]),("CHUTE (c)",it["c"]),("ACERTO REAL","n/d")]
    else:
        txt(M,sY,"ÍNDICE DE POLÊMICA · TRI",mono,12.5,GRAY)
        txt(M,sY+50,it["ipt"],outfitB,44,CORAL)
        txt(M+tw(it["ipt"],outfitB,44)+10,sY+50,"/100",outfit,19,GRAY)
        txt(M,sY+86,f'posição nº {it["n"]} de 10',mono,12.5,GRAY)
        chips=[("DISCRIM. (a)",it["a"]),("DIFIC. TRI",it["dif"]),("CHUTE (c)",it["c"]),("ACERTO REAL",it["ac"])]
    cw,ch,gx,gy=226,58,16,14; bx=W-M-2*cw-gx; topY=sY-12
    for i,(lab,val) in enumerate(chips):
        cx=bx+(i%2)*(cw+gx); cy=topY+(i//2)*(ch+gy)
        rrect(cx,cy,cw,ch,14,CHIP,z=3)
        txt(cx+18,cy+24,lab,mono,12.5,GRAY)
        txt(cx+cw-18,cy+41,val,outfitB,25,INK,ha="right")
    txt(W-M,topY+2*ch+gy+22,"Dificuldade TRI = b × 100 + 500",mono,11.5,GRAY,ha="right")
    # ---- por que pegou ----
    rY=sY+190
    txt(M,rY,("POR QUE CHAMA ATENÇÃO" if ppl else "POR QUE PEGOU"),mono,12.5,CORALd)
    for k,line in enumerate(textwrap.wrap(it["reason"],width=66)[:2]):
        txt(M,rY+30+k*28,line,outfit,17,INK)
    # ---- rodape (CTA em cima, legenda curta abaixo do botao) ----
    fy=L["footY"]
    cax,cay,caw,cah=596,fy-30,W-M-596,88
    rrect(cax,cay,caw,cah,22,CTA_BG,z=3)
    txt(cax+28,cay+38,"ESTUDO COMPLETO",mono,12,CTA_SUB)
    txt(cax+28,cay+70,"app.rankingenem.com/polemicas →",monoB,14,"#FFFFFF")
    txt(M,fy,"@xandaoxtri",outfitB,28,INK)
    yy=fy+38; seg=[("Dados reais",CYAN),(" ou ",INK),("nada",CORAL),(".",INK)]; xx=M
    for t,cc in seg: txt(xx,yy,t,outfitB,23,cc); xx+=tw(t,outfitB,23)
    txt(M,fy+90,"Fonte: Microdados ENEM 2025 / INEP",mono,12.5,GRAY)
    base=f"{OUT}/_base_{it['crop']}_{fmt}.png"; fig.savefig(base,dpi=300,facecolor=BG); plt.close(fig)
    # ---- PIL: cola o print dentro do card (contain) ----
    canvas=Image.open(base).convert("RGB"); sc=canvas.size[0]/W
    q=Image.open(f"{CROPS}/{it['crop']}.png").convert("RGB")
    pad=int(22*sc); BX=int((ix)*sc)+pad; BY=int((iy)*sc)+pad; BW=int(iw*sc)-2*pad; BH=int(ih*sc)-2*pad
    r=min(BW/q.size[0],BH/q.size[1]); nw,nh=int(q.size[0]*r),int(q.size[1]*r)
    q=q.resize((nw,nh),Image.LANCZOS)
    canvas.paste(q,(BX+(BW-nw)//2, BY+(BH-nh)//2))
    fout=f"{OUT}/polemica_{it['n']:02d}_{it['crop']}_{fmt}.png"; canvas.save(fout); print("ok",os.path.basename(fout))
    return fout

mode=sys.argv[1] if len(sys.argv)>1 else "all"
if mode=="one": make(ITEMS[0],"feed"); make(ITEMS[0],"story")
else:
    for it in ITEMS:
        for fmt in ("feed","story"): make(it,fmt)
print("FIM")
