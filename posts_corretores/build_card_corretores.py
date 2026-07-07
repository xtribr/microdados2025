#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Card A6 — 'Sua redacao caiu num corretor mais duro?' (movimento DUPLA PAUTA).
Todos os numeros sao reais (Microdados ENEM 2025 / INEP), calculados de RESULTADOS_2025.csv."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
import numpy as np

FD = "/sessions/brave-sharp-fermi/mnt/.claude/skills/canvas-design/canvas-fonts"
def F(name):
    fp = fm.FontProperties(fname=f"{FD}/{name}.ttf")
    return fp
serif   = F("InstrumentSerif-Regular")
serif_i = F("InstrumentSerif-Italic")
gloock  = F("Gloock-Regular")
outfit  = F("Outfit-Regular")
outfitB = F("Outfit-Bold")
mono    = F("JetBrainsMono-Regular")
monoB   = F("JetBrainsMono-Bold")

# ---- PALETA DE MARCA XTRI ----
PAPER = "#F4F2EC"   # papel morno, sem branco puro, sem fundo preto
INK   = "#22303A"   # tinta ardosia (nao preto puro)
INK2  = "#5A6B73"   # texto secundario
CORAL = "#EF5130"   # corretor 1 / acento principal
BLUE  = "#1FA8E8"   # corretor 2
BLUEd = "#1387C2"
HAIR  = "#D8D2C6"   # filetes
SOFT  = "#ECE7DD"   # preenchimento suave

W, H = 1080, 1350
fig = plt.figure(figsize=(W/100, H/100), dpi=300)
ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
ax.add_patch(Rectangle((0,0), W, H, color=PAPER, zorder=0))

# textura sutil de pauta (linhas finissimas, baixa opacidade)
for y in range(120, 1300, 7):
    ax.add_line(Line2D([0,W],[y,y], color=INK, lw=0.4, alpha=0.022, zorder=0.2))

LM, RM = 92, 988
def txt(x,y,s,fp,size,color=INK,ha="left",va="baseline",alpha=1,ls=0,zorder=5):
    t = ax.text(x,y,s,fontproperties=fp,fontsize=size,color=color,ha=ha,va=va,alpha=alpha,zorder=zorder)
    if ls: t.set_fontproperties(fp)
    return t
def hair(y,x0=LM,x1=RM,color=HAIR,lw=1.4,alpha=1):
    ax.add_line(Line2D([x0,x1],[y,y],color=color,lw=lw,alpha=alpha,zorder=4))

# ===== KICKER =====
txt(LM, 64, "X·TRI   —   ENEM 2025 EM DADOS", monoB, 15.5, INK, ls=1)
txt(RM, 64, "EST. A6 · REDAÇÃO · DUPLA CORREÇÃO", mono, 13.5, INK2, ha="right")
hair(86)

# ===== HEADLINE (voz do aluno) =====
txt(LM, 168, "Sua redação caiu", serif_i, 67, INK)
txt(LM, 230, "num corretor mais duro?", serif_i, 67, CORAL)
# subhead
txt(LM, 276, "Cada redação do ENEM é corrigida por dois avaliadores, de forma independente.", outfit, 19.5, INK2)
txt(LM, 303, "O quanto eles discordam — e o que acontece quando discordam de verdade.", outfit, 19.5, INK2)

# ===== HERO =====
# divisor pauta-dupla acima do heroi
ax.add_line(Line2D([LM, RM],[336,336], color=CORAL, lw=2.6, zorder=4))
ax.add_line(Line2D([LM, RM],[343,343], color=BLUE, lw=2.6, zorder=4))
# numero heroi: "67,5" grande + "%" menor elevado (compacto e elegante)
txt(84, 472, "67,5", gloock, 128, CORAL)
txt(398, 404, "%", gloock, 58, CORAL)
# sublinhado pauta-dupla sob o numero
ax.add_line(Line2D([92, 432],[500,500], color=CORAL, lw=2.6, zorder=4))
ax.add_line(Line2D([92, 432],[507,507], color=BLUE,  lw=2.6, zorder=4))
# caption a direita (bloco proprio, sem colisao com o numero)
cx = 476
txt(cx, 400, "das redações tiveram os", outfit, 21, INK)
txt(cx, 428, "dois corretores a no máximo", outfit, 21, INK)
txt(cx, 458, "80 pontos de diferença", outfitB, 23, CORAL)
txt(cx, 485, "(numa escala de 0 a 1000)", outfit, 16, INK2)

# ===== TRES CHIPS =====
chips = [("20,4%","deram nota idêntica","(1 em cada 5)"),
         ("1 em 3","vai a um 3º corretor","quando a diferença passa de 80"),
         ("5,4%","vai à banca (4º)","os casos mais divergentes")]
cw = (RM-LM)/3
for i,(big,l1,l2) in enumerate(chips):
    x0 = LM + i*cw
    if i>0: ax.add_line(Line2D([x0,x0],[600,664],color=HAIR,lw=1.2,zorder=4))
    txt(x0+ (18 if i else 0), 624, big, gloock, 33, BLUEd if i==1 else INK)
    txt(x0+ (18 if i else 0), 646, l1, outfitB, 15.5, INK)
    txt(x0+ (18 if i else 0), 664, l2, outfit, 13.5, INK2)
hair(690)

# ===== SECAO BARRAS POR COMPETENCIA =====
txt(LM, 726, "A DISTÂNCIA MÉDIA ENTRE OS DOIS CORRETORES, POR COMPETÊNCIA", monoB, 14.5, INK, ls=1)
txt(LM, 748, "diferença média |Corretor 1 − Corretor 2|, em pontos · cada competência vale 0 a 200", outfit, 15, INK2)

comps = [("C1","Norma culta", 20.7),
         ("C2","Compreensão do tema", 21.5),
         ("C3","Argumentação", 22.0),
         ("C4","Coesão e conectivos", 24.2),
         ("C5","Proposta de intervenção", 26.3)]
bx0, bx1 = 360, 900           # trilha da barra
SC = 80.0                      # escala 0..80 (limite da competencia p/ 3a correcao = 80)
def xval(v): return bx0 + (v/SC)*(bx1-bx0)
row_y = [800, 852, 904, 956, 1008]
# linha de limite 80
ax.add_line(Line2D([bx1,bx1],[784,1028], color=INK2, lw=1.3, ls=(0,(5,4)), alpha=0.6, zorder=3))
txt(bx1, 776, "80 pts → 3º corretor", mono, 12.5, INK2, ha="right")
for (code,name,val),y in zip(comps,row_y):
    # rotulo
    txt(LM, y+1, code, monoB, 17, CORAL if val==26.3 else INK)
    txt(LM+44, y+1, name, outfit, 18.5, INK, va="center")
    # trilha base
    ax.add_line(Line2D([bx0,bx1],[y+14,y+14], color=SOFT, lw=7, alpha=1, zorder=2.5,
                       solid_capstyle="round"))
    # barra (divergencia)
    xe = xval(val)
    ax.add_line(Line2D([bx0,xe],[y+14,y+14], color=CORAL, lw=7, zorder=3, solid_capstyle="round"))
    ax.add_patch(Circle((xe, y+14), 6.5, color=BLUE, zorder=4, ec=PAPER, lw=1.5))
    txt(xe+16, y+14, f"{val:.1f}".replace(".",",")+" pts", outfitB, 16.5, INK, va="center")
# nota de leitura das pontas
txt(LM+44, 1052, "Proposta de intervenção é onde os corretores mais divergem; norma culta, onde mais concordam.",
    serif_i, 16, INK2)

hair(1082)
# ===== TAKEAWAY =====
txt(LM, 1118, "O “azar de corretor” tem limite.", outfitB, 25, INK)
txt(LM, 1149, "Na média, os dois ficam a só ~85 pontos um do outro (escala 0–1000). Passou de 80,", outfit, 17.5, INK2)
txt(LM, 1174, "entra um 3º corretor. A nota é a média de quem corrige — não a sorte de um.", outfit, 17.5, INK2)

# ===== FOOTER =====
hair(1208, lw=1.2)
txt(LM, 1240, "Fonte: Microdados ENEM 2025 / INEP · 3,46 mi de redações.", mono, 12.5, INK2)
txt(LM, 1260, "Dupla correção independente · análise XTRI · sem dado estimado.", mono, 12.5, INK2)
# marca
try:
    logo = mpimg.imread("/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/logo_xtri_marca_real.png")
    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    im = OffsetImage(logo, zoom=0.075)
    ab = AnnotationBbox(im, (RM, 1250), frameon=False, box_alignment=(1,0.5), zorder=6)
    ax.add_artist(ab)
except Exception as e:
    txt(RM, 1244, "X·TRI", gloock, 30, CORAL, ha="right")

out = "/sessions/brave-sharp-fermi/mnt/outputs/card_corretores_A6.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
print("salvo", out)
