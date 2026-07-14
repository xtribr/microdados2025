#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa WP destaque/social 1200x630 -- 'O ENEM fica mais dificil a cada ano?'
Segue o padrao das capas anteriores (titulo+subtitulo a esquerda, lista de
cards a direita: capa_wp_sequencia_dificuldade_1200x630.png etc.)."""
import json
import sys
sys.path.insert(0, "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026")
from xtri_style import *

OUT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"

with open(f"{OUT}/dados_previsao_2026.json", encoding="utf-8") as f:
    D = json.load(f)

AREAS = ["LC", "CH", "CN", "MT"]
NOME = {"LC": "Linguagens", "CH": "Ciências Humanas", "CN": "Ciências da Natureza", "MT": "Matemática"}
COR = {"LC": CYAN, "CH": CORAL, "CN": INK, "MT": GRAY}

faixas = {}
for area in AREAS:
    difs = [p[1] * 100 + 500 for p in D["serie_completa"][area]]
    faixas[area] = (min(difs), max(difs))

w, h = 1200, 630
fig, ax, hp = new_canvas(w, h)
txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]

add_logo(ax, 44, 46, zoom=0.075)
txt(w - 44, 50, "MICRODADOS ENEM 2010–2025", mono, 12, GRAY, ha="right")

# ---- coluna esquerda: titulo + subtitulo ----
txt(64, 150, "O ENEM fica mais", outfitB, 40, INK)
txt(64, 200, "difícil a cada ano?", outfitB, 40, CORAL)

txt(64, 250, "16 anos de dados reais", outfit, 17, GRAY)
txt(64, 278, "respondem — e não é", outfit, 17, GRAY)
txt(64, 306, "o que você imagina.", outfit, 17, GRAY)

rrect(64, 355, 300, 2, 1, "#D8DADC")
txt(64, 392, "R² < 0,07", monoB, 15, INK)
txt(64, 416, "nas 4 áreas — sem", mono, 12.5, GRAY)
txt(64, 434, "tendência linear real", mono, 12.5, GRAY)

# ---- coluna direita: cards por area (faixa historica) ----
cx, cy, cw = 632, 120, 508
row_h = 84
gap = 14
rrect(cx, cy, cw, 12, 6, "#E9EAEB", z=0)  # sombra sutil (placeholder visual leve)
txt(cx, cy - 14, "FAIXA HISTÓRICA DE DIFICULDADE (2010–2025)", mono, 11.5, GRAY)

y = cy + 24
for area in AREAS:
    col = COR[area]
    rrect(cx, y, cw, row_h, 16, "#FFFFFF", z=2)
    rrect(cx, y, 5, row_h, 2.5, col, z=3)
    # chip
    chip_w, chip_h = 52, 34
    chip_x, chip_y = cx + 26, y + row_h / 2 - chip_h / 2
    rrect(chip_x, chip_y, chip_w, chip_h, 9, col, z=4)
    txt(chip_x + chip_w / 2, chip_y + chip_h / 2 + 1, area, outfitB, 14.5, "#FFFFFF", ha="center", va="center", z=5)
    # label
    lx = chip_x + chip_w + 18
    txt(lx, y + row_h / 2 - 12, NOME[area], outfitB, 15, INK, va="center")
    sublabel = "faixa histórica real"
    txt(lx, y + row_h / 2 + 13, sublabel, mono, 10.5, GRAY, va="center")
    # valor (medido com tw() p/ garantir folga horizontal ate o rotulo)
    lo, hi = faixas[area]
    val = f"{lo:.0f}–{hi:.0f}"
    vx = cx + cw - 22
    val_sz = 22
    val_w = tw(val, outfitB, val_sz)
    label_end = lx + max(tw(NOME[area], outfitB, 15), tw(sublabel, mono, 10.5))
    gap_disponivel = (vx - val_w) - label_end
    assert gap_disponivel > 40, f"{area}: gap insuficiente entre rotulo e valor ({gap_disponivel:.0f}px)"
    txt(vx, y + row_h / 2 + 8, val, outfitB, val_sz, col, ha="right", va="center")
    y += row_h + gap

# ---- rodape ----
fy = 585
assinatura(hp, 64, fy)
txt(w - 44, fy, "Fonte: Microdados ENEM / INEP · app.rankingenem.com", mono, 9.6, GRAY, ha="right")

save(fig, f"{OUT}/capa_wp_previsao_2026_1200x630.png")
