#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa WordPress 1200x630 — post 'Curva normal do ENEM' (mini-curva + números)."""
import sys
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent
sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CORAL, CORALd, CYAN, DIF_FACIL, DIF_MEDIO, DIF_DIFICIL, DIF_MDIFICIL)

X.OUTDIR = str(D)
W, H = 1200, 630

fig, ax, hp = new_slide(W, H)
txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
M = 70

rrect(0, 0, 18, H, 0, CORAL, z=1)
txt(M, 88, "MICRODADOS ENEM 2025 · INEP", monoB, 14, CORALd)
txt(M, 160, "A curva normal", outfitB, 46, INK)
txt(M, 218, "do ENEM", outfitB, 46, CORAL)
txt(M, 268, "500 = média · 100 pontos = 1 desvio.", outfit, 19, GRAY)
txt(M, 300, "E os percentis REAIS de 2025, por área.", outfit, 19, GRAY)
txt(M, 400, "700 em Linguagens: top 0,4%", outfitB, 25, INK)
txt(M, 448, "700 em Matemática: top 10,4%", outfitB, 25, CORALd)
txt(M, 500, "3,4 milhões de candidatos, contados um a um.", mono, 13.5, GRAY)
txt(M, 568, "Prof. Alexandre Emerson · XTRI", mono, 12.5, GRAY)

# mini-curva à direita
x0, x1 = 660, W - 60
base = 480
esc = 300

def sx(s):
    return x0 + (s + 3.4) / 6.8 * (x1 - x0)

bandas = [(-3.4, -3, DIF_MDIFICIL), (-3, -2, DIF_DIFICIL), (-2, -1, DIF_MEDIO),
          (-1, 1, DIF_FACIL), (1, 2, DIF_MEDIO), (2, 3, DIF_DIFICIL), (3, 3.4, DIF_MDIFICIL)]
for a_, b_, cor in bandas:
    ss = np.linspace(a_, b_, 50)
    xs = [sx(s) for s in ss]
    ys = [base - np.exp(-0.5 * s * s) * esc for s in ss]
    ax.fill(list(xs) + [sx(b_), sx(a_)], list(ys) + [base, base], color=cor, alpha=0.9, zorder=2, lw=0)
ss = np.linspace(-3.4, 3.4, 200)
ax.plot([sx(s) for s in ss], [base - np.exp(-0.5 * s * s) * esc for s in ss], color=INK, lw=2.2, zorder=4)
ax.plot([x0 - 4, x1 + 4], [base, base], color="#B9BDC1", lw=1.4, zorder=4)
for s, lab in [(-2, "300"), (0, "500"), (2, "700")]:
    txt(sx(s), base + 30, lab, outfitB, 16, CORAL if s == 2 else INK, ha="center", z=5)
xx = sx(2)
ax.plot([xx, xx], [base - np.exp(-2) * esc, base - esc - 24], color=CORALd, lw=1.5, ls=(0, (4, 3)), zorder=5)
txt(xx + 10, base - esc - 4, "700", outfitB, 19, CORALd, z=6)

logo(ax, W - 66, 86, zoom=0.07)
save(fig, "capa_wp_curva_normal_1200x630")
