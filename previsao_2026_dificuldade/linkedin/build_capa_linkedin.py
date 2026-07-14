#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa LinkedIn 1280x720 -- 'O ENEM fica mais dificil a cada ano?'
Tudo desenhado em coordenadas de pixel do overlay (ax), sem eixo matplotlib
separado -- evita qualquer estouro de texto em coordenada de dado."""
import json
import sys
sys.path.insert(0, "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026")
from xtri_style import *

OUT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"

with open(f"{OUT}/dados_previsao_2026.json", encoding="utf-8") as f:
    D = json.load(f)

AREAS = ["MT", "CN", "CH", "LC"]
NOME = {"LC": "Linguagens", "CH": "Ciências Humanas", "CN": "Ciências da Natureza", "MT": "Matemática"}
COR = {"LC": CYAN, "CH": CORAL, "CN": INK, "MT": GRAY}

faixas, r2, v2025 = {}, {}, {}
for area in AREAS:
    difs = [p[1] * 100 + 500 for p in D["serie_completa"][area]]
    faixas[area] = (min(difs), max(difs))
    r2[area] = D["previsao_2026"][area]["r2"]
    v2025[area] = D["serie_completa"][area][-1][1] * 100 + 500

w, h = 1280, 720
fig, ax, hp = new_canvas(w, h)
txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]

add_logo(ax, 56, 58, zoom=0.085)
txt(w - 56, 62, "ENEM 2010–2025 · MICRODADOS · TRI OFICIAL", mono, 12.5, GRAY, ha="right")

txt(56, 145, "O ENEM FICA MAIS DIFÍCIL", outfitB, 35, INK)
txt(56, 192, "A CADA ANO?", outfitB, 35, CORAL)
txt(56, 228, "16 anos de dados oficiais — e a resposta não é a que você imagina.", outfit, 16, GRAY)

# ---- zona de conteudo: range-plot horizontal, tudo em pixel (ax) ----
label_x = 56          # rotulo da area, alinhado a esquerda
bar_x0, bar_x1 = 330, 940   # coluna da barra de faixa
value_x = w - 56       # valor, alinhado a direita

all_lo = min(v[0] for v in faixas.values())
all_hi = max(v[1] for v in faixas.values())
dom_lo, dom_hi = all_lo - 8, all_hi + 8


def scale(v):
    return bar_x0 + (v - dom_lo) / (dom_hi - dom_lo) * (bar_x1 - bar_x0)


rows_y = [300, 385, 470, 555]
txt((bar_x0 + bar_x1) / 2, rows_y[0] - 42, "faixa histórica de Dificuldade TRI (2010–2025)  ·  círculo = nota real 2025",
    mono, 11, GRAY, ha="center")

for area, ry in zip(AREAS, rows_y):
    col = COR[area]
    lo, hi = faixas[area]
    x_lo, x_hi = scale(lo), scale(hi)

    # verificacao de folga antes de desenhar (rotulo x barra x valor)
    lab_w = tw(NOME[area], outfitB, 15.5)
    assert label_x + lab_w + 24 < x_lo, f"{area}: rótulo colide com a barra"
    val_txt = f"{lo:.0f}–{hi:.0f}"
    val_w = tw(val_txt, outfitB, 20)
    assert x_hi + 24 < value_x - val_w, f"{area}: barra colide com o valor"

    ax.plot([x_lo, x_hi], [ry, ry], color=col, lw=11, solid_capstyle="round", zorder=3, alpha=0.85)
    ax.scatter([scale(v2025[area])], [ry], s=110, facecolor="white", edgecolor=col, lw=2.6, zorder=4)
    txt(label_x, ry, NOME[area], outfitB, 15.5, INK, va="center")
    txt(value_x, ry, val_txt, outfitB, 20, col, ha="right", va="center")
    txt((x_lo + x_hi) / 2, ry - 24, f"R² = {r2[area]:.3f}", mono, 9.5, GRAY, ha="center", va="center")

# ---- rodape ----
fy = 668
assinatura(hp, 56, fy)
txt(w - 56, fy, "Prof. Alexandre Emerson · @xandaoxtri", mono, 12.5, GRAY, ha="right")

save(fig, f"{OUT}/capa_linkedin_previsao_2026_1280x720.png")
