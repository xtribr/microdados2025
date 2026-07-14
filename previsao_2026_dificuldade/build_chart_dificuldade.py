#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grafico principal: Dificuldade TRI por area, 2010-2025 (16 anos completos -- 2018
recuperado direto do INEP oficial), sem tendencia linear significativa (R2 baixo em
todas), com faixa historica real e faixa esperada 2026.
"""
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


def plot_panel(axc, area, show_xticks=True):
    pts = D["serie_completa"][area]
    anos = [p[0] for p in pts]
    difs = [p[1] * 100 + 500 for p in pts]
    prev = D["previsao_2026"][area]

    hist_min, hist_max = min(difs), max(difs)
    col = COR[area]

    # faixa historica (banda horizontal)
    axc.axhspan(hist_min, hist_max, color=col, alpha=0.08, zorder=1)

    # linha real, quebrando no buraco de 2018
    segs = []
    cur = []
    for a, d in zip(anos, difs):
        if cur and a - cur[-1][0] > 1:
            segs.append(cur)
            cur = []
        cur.append((a, d))
    if cur:
        segs.append(cur)
    for seg in segs:
        xs = [p[0] for p in seg]; ys = [p[1] for p in seg]
        axc.plot(xs, ys, "-o", color=col, lw=1.8, ms=4.5, zorder=3, mec="white", mew=0.6)

    # faixa esperada 2026 (min-max historico, nao um ponto unico)
    axc.plot([2026, 2026], [hist_min, hist_max], color=col, lw=3, alpha=0.35, zorder=2, solid_capstyle="round")
    axc.scatter([2026], [(hist_min + hist_max) / 2], s=46, facecolor="white", edgecolor=col, lw=2, zorder=4)

    axc.set_xlim(2009, 2027.3)
    axc.set_xticks([2010, 2013, 2016, 2019, 2022, 2025])
    if not show_xticks:
        axc.tick_params(labelbottom=False)
    ymarg = (hist_max - hist_min) * 0.22
    axc.set_ylim(hist_min - ymarg, hist_max + ymarg * 2.3)

    style_axes(axc, ylabel="Dificuldade TRI")
    axc.set_title(f"{NOME[area]} ({area})", fontproperties=outfitB, fontsize=13.5, color=INK, pad=10, loc="left")
    axc.text(0.02, 0.95, f"R² = {prev['r2']:.3f}  ·  faixa hist. {hist_min:.0f}–{hist_max:.0f}",
             transform=axc.transAxes, fontproperties=mono, fontsize=8.3, color=GRAY, va="top")
    axc.text(2026, hist_max + ymarg * 1.75, "faixa\nesperada", fontproperties=mono, fontsize=7.6,
              color=col, ha="center", va="top", linespacing=1.15)


def build(w, h, title_lines, footer_extra, filename, chart_box):
    fig, ax, hp = new_canvas(w, h)
    txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]

    add_logo(ax, 44, 46, zoom=0.075)
    txt(w - 44, 50, "@xandaoxtri", mono, 12, GRAY, ha="right")

    y = 118
    for i, (line, sz, col) in enumerate(title_lines):
        txt(60, y, line, outfitB, sz, col)
        y += sz + 10

    cx, cy, cw, ch = chart_box
    rrect(cx, cy, cw, ch, 16, CARD, z=1)
    pad = 30
    gapx = 46
    gapy = 100
    pw = (cw - 2 * pad - gapx) / 2
    ph = (ch - 2 * pad - gapy) / 2
    for i, area in enumerate(AREAS):
        row, col_i = divmod(i, 2)
        x0 = cx + pad + col_i * (pw + gapx)
        y0 = cy + pad + row * (ph + gapy)
        l = x0 / w; b = 1 - (y0 + ph) / h; ww = pw / w; hh = ph / h
        axc = fig.add_axes([l, b, ww, hh])
        plot_panel(axc, area, show_xticks=(row == 1))

    fy = cy + ch + 64
    txt(60, fy, "Fonte: Microdados ENEM 2010-2025 / INEP · análise XTRI.",
        mono, 9.6, GRAY)
    txt(60, fy + 18, "R² próximo de zero nas 4 áreas: sem tendência linear real no período —",
        mono, 9.6, GRAY)
    txt(60, fy + 36, footer_extra, mono, 9.6, GRAY)

    ay = fy + 36 + 54
    assinatura(hp, 60, ay)
    txt(w - 44, ay, "Fonte: Microdados ENEM / INEP", mono, 9.6, GRAY, ha="right")

    save(fig, f"{OUT}/{filename}")


# ---- WP inline (1200 largura) ----
build(
    w=1200, h=1610,
    title_lines=[
        ("O ENEM fica mais difícil a cada ano?", 30, INK),
        ("16 anos de dados reais respondem — e a resposta não é a que você imagina.", 15.5, GRAY),
    ],
    footer_extra="a faixa esperada em 2026 é a faixa histórica real de cada área, não um número extrapolado.",
    filename="wp_inline_dificuldade_2026.png",
    chart_box=(60, 176, 1080, 1160),
)
