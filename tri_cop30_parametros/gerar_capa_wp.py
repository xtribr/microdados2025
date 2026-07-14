#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa WordPress 1200x630 — post 'Parâmetros TRI da COP30'."""
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import new_slide, logo, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN

X.OUTDIR = str(D)
W, H = 1200, 630

fig, ax, hp = new_slide(W, H)
txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
M = 70

rrect(0, 0, 18, H, 0, CORAL, z=1)
txt(M, 92, "MICRODADOS ENEM 2025 · INEP", monoB, 14, CORALd)
txt(M, 168, "Os parâmetros TRI da", outfitB, 44, INK)
txt(M, 228, "COP30 são públicos", outfitB, 44, CORAL)
txt(M, 282, "A comunidade procurava nos códigos errados.", outfit, 20, GRAY)

# cards de número
cards = [("186", "itens com a, b, c"), ("1583→1502", "a ponte entre os arquivos"), ("0", "divergências na prova")]
cw = (W - 2 * M - 2 * 28) / 3
y0, ch = 330, 170
for i, (num, lab) in enumerate(cards):
    x = M + i * (cw + 28)
    shadow(x, y0, cw, ch, 14)
    rrect(x, y0, cw, ch, 14, CARD, z=2)
    rrect(x, y0, cw, 8, 4, CORAL if i != 1 else CYAN, z=3)
    txt(x + cw / 2, y0 + 92, num, outfitB, 34 if i == 1 else 42, INK, ha="center", z=5)
    txt(x + cw / 2, y0 + 136, lab, mono, 12.5, GRAY, ha="center", z=5)

txt(M, 578, "Onde encontrar e como verificar em 5 minutos", outfitB, 19, INK)
txt(W - M, 578, "Prof. Alexandre Emerson · XTRI", mono, 12, GRAY, ha="right")
logo(ax, W - M + 10, 92, zoom=0.075)
save(fig, "capa_wp_parametros_tri_cop30_1200x630")
