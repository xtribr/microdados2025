#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Instagram feed 1080x1350 + story 1080x1920 -- 'O ENEM fica mais dificil a cada ano?'
Mesmo layout base do padrao (titulo caixa-alta + subtitulo + faixa-plot + card RESPOSTA + rodape),
tudo em coordenadas de pixel (ax overlay), sem eixo matplotlib separado."""
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

all_lo = min(v[0] for v in faixas.values())
all_hi = max(v[1] for v in faixas.values())
dom_lo, dom_hi = all_lo - 8, all_hi + 8


def build(w, h, chart_top, row_gap, filename, card_h):
    fig, ax, hp = new_canvas(w, h)
    txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]

    add_logo(ax, 64, 66, zoom=0.095)
    txt(w - 64, 70, "ENEM 2010–2025 · MICRODADOS · TRI OFICIAL", mono, 12.5, GRAY, ha="right")

    txt(64, 168, "O ENEM FICA MAIS", outfitB, 42, INK)
    txt(64, 222, "DIFÍCIL A CADA ANO?", outfitB, 42, CORAL)
    txt(64, 272, "16 anos de dados reais respondem.", outfit, 18, GRAY)
    txt(64, 300, "E a resposta não é a que você imagina.", outfit, 18, GRAY)

    label_x = 64
    bar_x0, bar_x1 = 330, w - 240
    value_x = w - 64

    def scale(v):
        return bar_x0 + (v - dom_lo) / (dom_hi - dom_lo) * (bar_x1 - bar_x0)

    legend_y = 344
    assert chart_top - 27 - legend_y > 28, "legenda colide com o R² da 1ª linha"
    txt((bar_x0 + bar_x1) / 2, legend_y, "faixa histórica de Dificuldade TRI  ·  círculo = nota real 2025",
        mono, 11.5, GRAY, ha="center")

    ry = chart_top
    for area in AREAS:
        col = COR[area]
        lo, hi = faixas[area]
        x_lo, x_hi = scale(lo), scale(hi)
        lab_w = tw(NOME[area], outfitB, 17)
        assert label_x + lab_w + 24 < x_lo, f"{area}: rótulo colide com a barra ({lab_w:.0f}px)"
        val_txt = f"{lo:.0f}–{hi:.0f}"
        val_w = tw(val_txt, outfitB, 21)
        assert x_hi + 24 < value_x - val_w, f"{area}: barra colide com o valor"

        ax.plot([x_lo, x_hi], [ry, ry], color=col, lw=13, solid_capstyle="round", zorder=3, alpha=0.85)
        ax.scatter([scale(v2025[area])], [ry], s=130, facecolor="white", edgecolor=col, lw=2.8, zorder=4)
        txt(label_x, ry, NOME[area], outfitB, 17, INK, va="center")
        txt(value_x, ry, val_txt, outfitB, 21, col, ha="right", va="center")
        txt((x_lo + x_hi) / 2, ry - 27, f"R² = {r2[area]:.3f}", mono, 10, GRAY, ha="center", va="center")
        ry += row_gap

    # ---- card RESPOSTA ----
    card_y = ry + 30
    cw = w - 128
    rrect(64, card_y, cw, card_h, 20, "#FFFFFF", z=2)
    pad = 34
    txt(64 + pad, card_y + pad + 14, "RESPOSTA", mono, 13, GRAY)
    txt(64 + pad, card_y + pad + 70, "OSCILA,", outfitB, 44, CORAL)
    txt(64 + pad, card_y + pad + 118, "NÃO SOBE", outfitB, 44, INK)

    ty = card_y + pad + 168
    linhas = [
        "Em 16 anos completos (2010–2025), a dificuldade média sobe e desce",
        "dentro de uma faixa estável — sem tendência linear real (R² < 0,07).",
    ]
    for ln in linhas:
        txt(64 + pad, ty, ln, outfit, 16, GRAY)
        ty += 27

    # ---- rodape ----
    fy = card_y + card_h + 64
    txt(64, fy, "Fonte: Microdados ENEM 2010-2025 / INEP · análise XTRI.",
        mono, 10, GRAY)
    ay = fy + 54
    assinatura(hp, 64, ay)
    txt(w - 64, ay, "@xandaoxtri", mono, 13, GRAY, ha="right")

    assert ay + 40 < h, f"assinatura ({ay}) ultrapassa a altura do canvas ({h})"
    save(fig, f"{OUT}/{filename}")


# ---- feed 1080x1350 ----
build(w=1080, h=1350, chart_top=414, row_gap=98, filename="xtri_previsao_2026_feed.png", card_h=340)

# ---- story 1080x1920 (mais respiro vertical + margem de seguranca no rodape) ----
build(w=1080, h=1920, chart_top=414, row_gap=210, filename="xtri_previsao_2026_story.png", card_h=340)
