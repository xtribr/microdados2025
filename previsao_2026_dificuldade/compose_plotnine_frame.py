#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compoe o grafico plotnine (regressao OLS + IC95%) dentro da moldura de
marca XTRI (logo, titulo, rodape com fonte + assinatura), via colagem PIL
(evita ambiguidade de orientacao do imshow/extent em eixo invertido)."""
import sys
from PIL import Image
sys.path.insert(0, "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026")
from xtri_style import *

OUT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"

chart_img = Image.open(f"{OUT}/plotnine_regressao_dificuldade.png")
cw_native, ch_native = chart_img.size

w = 1200
img_w = 1080
scale = img_w / cw_native
img_h = int(ch_native * scale)
img_x = (w - img_w) // 2
img_y = 186

fy = img_y + img_h + 64
ay = fy + 36 + 54
h = ay + 70

fig, ax, hp = new_canvas(w, h)
txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]

add_logo(ax, 44, 46, zoom=0.075)
txt(w - 44, 50, "METODOLOGIA · ANÁLISE ESTATÍSTICA", mono, 12, GRAY, ha="right")

txt(60, 118, "A mesma pergunta, pela regressão estatística completa", outfitB, 26, INK)
txt(60, 148, "OLS + intervalo de confiança de 95% por área — gerado em plotnine (gramática ggplot2).",
    outfit, 14.5, GRAY)

rrect(img_x - 4, img_y - 4, img_w + 8, img_h + 8, 14, "#FFFFFF", z=1)

txt(60, fy, "Fonte: Microdados ENEM 2010-2025 / INEP · análise XTRI.",
    mono, 9.6, GRAY)
txt(60, fy + 18, "Faixa cinza = IC 95% da regressão linear. Quanto mais larga, menos confiável é o ajuste —",
    mono, 9.6, GRAY)
txt(60, fy + 36, "e ela é larga nas 4 áreas: não há tendência linear real a se apoiar.", mono, 9.6, GRAY)

assinatura(hp, 60, ay)
txt(w - 44, ay, "Fonte: Microdados ENEM / INEP", mono, 9.6, GRAY, ha="right")

save(fig, f"{OUT}/_frame_plotnine.png")

frame = Image.open(f"{OUT}/_frame_plotnine.png").convert("RGB")
chart_resized = chart_img.convert("RGB").resize((img_w, img_h), Image.LANCZOS)
frame.paste(chart_resized, (img_x, img_y))
frame.save(f"{OUT}/wp_metodologia_regressao_2026.png")
print("salvo: wp_metodologia_regressao_2026.png", frame.size)
