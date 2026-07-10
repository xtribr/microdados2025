#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa destaque WordPress 1200x630 — 'Nota maxima do ENEM 2025 decidida
por uma questao anulada'. PADRAO VISUAL XTRI."""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FD = "/Volumes/Kingston/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/173c3dab-6f51-4ed6-920d-43825f73e36c/a32ba23c-1f19-4aa1-8eaf-390193971d87/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB = F("Outfit-Bold"); outfit = F("Outfit-Regular")
mono = F("JetBrainsMono-Regular"); monoB = F("JetBrainsMono-Bold")
BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE, "..", "..", "..", "logo_xtri_marca_real.png")

BG = "#F1F1F2"; CARD = "#FFFFFF"; INK = "#1D1D20"; GRAY = "#8C9298"
CORAL = "#FA5230"; CORALd = "#E8431F"; CYANd = "#1597D8"; TRACK = "#E3E5E7"
W, H, M = 1200, 630, 64

fig = plt.figure(figsize=(W / 100, H / 100), dpi=300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))
fig.canvas.draw(); R = fig.canvas.get_renderer()
PXU = fig.get_size_inches()[0] * fig.dpi / W

def tw(s, fp, sz):
    t = ax.text(0, 0, s, fontproperties=fp, fontsize=sz); fig.canvas.draw()
    w = t.get_window_extent(R).width / PXU; t.remove(); return w

def txt(x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
    return ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

def rrect(x, y, w, h, rad, fc, z=2, alpha=1):
    ax.add_patch(FancyBboxPatch((x + rad, y + rad), w - 2 * rad, h - 2 * rad,
        boxstyle=f"round,pad={rad}", fc=fc, ec="none", zorder=z, alpha=alpha, mutation_aspect=1))

def shadow(x, y, w, h, rad):
    for i in range(1, 9):
        rrect(x - 1.0 * i, y + 2.4 + 1.7 * i, w + 2.0 * i, h + 1.0 * i, rad + 1.2 * i,
              "#000000", z=1.5, alpha=0.012)

# header
try:
    ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=0.095),
        (M + 26, 66), frameon=False, box_alignment=(0.5, 0.5), zorder=6))
except Exception:
    pass
txt(M, 112, "X-TRI", outfitB, 14, CYANd)

# headline (coluna esquerda)
txt(M, 208, "Nota máxima do", outfitB, 40, INK)
txt(M, 262, "ENEM 2025:", outfitB, 40, INK)
txt(M, 322, "decidida por uma", outfitB, 33, GRAY)
txt(M, 378, "QUESTÃO", outfitB, 44, CORAL)
txt(M, 434, "ANULADA.", outfitB, 44, CORAL)
txt(M, 492, "Gêmeos de prova nos microdados:", outfit, 16.5, GRAY)
txt(M, 520, "mesmo desempenho válido, 12,6 pontos de diferença.", outfit, 16.5, GRAY)

# card direito com o duelo
cx0, cy0, cw, ch = 636, 118, 500, 424
shadow(cx0, cy0, cw, ch, 24); rrect(cx0, cy0, cw, ch, 24, CARD, z=2)
ccx = cx0 + cw / 2
txt(ccx, cy0 + 44, "QUEM ACERTOU TUDO QUE VALIA", mono, 11.5, GRAY, ha="center")
txt(ccx, cy0 + 84, "MARCOU A NA ANULADA", monoB, 11.5, CORALd, ha="center")
txt(ccx, cy0 + 158, "980,3", outfitB, 58, CORAL, ha="center")
ax.add_line(Line2D([cx0 + 70, cx0 + cw - 70], [cy0 + 196, cy0 + 196], color=TRACK, lw=1.5, zorder=3))
txt(ccx, cy0 + 238, "MARCOU OUTRA LETRA", monoB, 11.5, GRAY, ha="center")
txt(ccx, cy0 + 312, "967,7", outfitB, 58, INK, ha="center")
bw, bh = 190, 44
rrect(ccx - bw / 2, cy0 + ch - 70, bw, bh, 14, CORAL, z=4)
txt(ccx, cy0 + ch - 70 + bh / 2 + 1, "+12,6 pontos", monoB, 14.5, "#FFFFFF", ha="center", va="center", z=5)

# footer
x = M
for s, c in [("Transformamos ", INK), ("dados", "#1FAFEF"), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
    txt(x, 574, s, outfitB, 17, c); x += tw(s, outfitB, 17)
txt(M, 604, "Fonte: Microdados ENEM 2025 / INEP · análise em R", mono, 9.5, GRAY)
txt(W - M, 604, "xtri.online", monoB, 11, GRAY, ha="right")

out = os.path.join(BASE, "capa_wp_nota_maxima_1200x630.png")
fig.savefig(out, dpi=300, facecolor=BG); plt.close(fig)
print("salvo", out)
