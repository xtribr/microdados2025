#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa LinkedIn 1200x1200 — 'Uma questao anulada decidiu as maiores notas
de Matematica'. PADRAO VISUAL XTRI. Numeros reais (scripts R 06-08)."""
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
CORAL = "#FA5230"; CORALd = "#E8431F"; CYAN = "#1FAFEF"; CYANd = "#1597D8"
TRACK = "#E3E5E7"
W, H, M = 1200, 1200, 76

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
    ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=0.12),
        (M + 32, 88), frameon=False, box_alignment=(0.5, 0.5), zorder=6))
except Exception:
    pass
txt(M, 148, "X-TRI", outfitB, 17, CYANd)
txt(W - M, 104, "PSICOMETRIA · ENEM 2025", outfitB, 17, INK, ha="right")
txt(W - M, 134, "Microdados / INEP · aplicação regular", mono, 13, GRAY, ha="right")

# chamada
txt(M, 266, "Uma questão ANULADA", outfitB, 56, CORAL)
txt(M, 344, "decidiu as maiores notas", outfitB, 56, INK)
txt(M, 422, "de Matemática.", outfitB, 56, INK)
sub1 = "Gêmeos de prova: "
txt(M, 492, sub1, outfitB, 21, INK)
txt(M + tw(sub1, outfitB, 21), 492, "desempenho válido idêntico, 12,6 pontos de diferença.",
    outfit, 21, GRAY)

# hero
hy, hh = 560, 400
shadow(M, hy, W - 2 * M, hh, 28); rrect(M, hy, W - 2 * M, hh, 28, CARD, z=2)
txt(W / 2, hy + 52, "OS 601 CANDIDATOS QUE ACERTARAM TUDO QUE VALIA NOTA", mono, 13, GRAY, ha="center")
cx = W / 2
ax.add_line(Line2D([cx, cx], [hy + 84, hy + hh - 96], color=TRACK, lw=1.5, zorder=3))
lx = M + (W - 2 * M) / 4; rx = W - M - (W - 2 * M) / 4
txt(lx, hy + 116, "MARCOU A NA ANULADA", monoB, 13.5, CORALd, ha="center")
txt(lx, hy + 232, "980,3", outfitB, 78, CORAL, ha="center")
txt(lx, hy + 282, "86 candidatos", mono, 13.5, GRAY, ha="center")
txt(rx, hy + 116, "MARCOU OUTRA LETRA", monoB, 13.5, GRAY, ha="center")
txt(rx, hy + 232, "967,7", outfitB, 78, INK, ha="center")
txt(rx, hy + 282, "515 candidatos", mono, 13.5, GRAY, ha="center")
cw, ch = 236, 52
rrect(cx - cw / 2, hy + hh - 84, cw, ch, 16, CORAL, z=4)
txt(cx, hy + hh - 84 + ch / 2 + 1, "+12,6 pontos", monoB, 17, "#FFFFFF", ha="center", va="center", z=5)

# footer
x = M
for s, c in [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
    txt(x, 1064, s, outfitB, 24, c); x += tw(s, outfitB, 24)
txt(W - M, 1064, "@xandaoxtri", outfitB, 24, GRAY, ha="right")
txt(M, 1136, "Fonte: Microdados ENEM 2025 / INEP · análise em R (data.table + ggplot2) · 644 comparações de gêmeos, zero exceções",
    mono, 11, GRAY)

out = os.path.join(BASE, "capa_linkedin_1200x1200.png")
fig.savefig(out, dpi=300, facecolor=BG); plt.close(fig)
print("salvo", out)
