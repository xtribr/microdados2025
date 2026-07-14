#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grafico estatistico em plotnine (gramatica ggplot2) -- regressao OLS + IC 95%
por area, 2010-2025 (2018 excluido). Pedido explicito do usuario: "graficos
precisos em ggplot2" para o estudo preditivo. R (e portanto ggplot2 literal e
o pacote ggdist) nao esta disponivel neste ambiente (sem root/apt/conda) --
plotnine e o equivalente Python da mesma gramatica de graficos, usado aqui
para o grafico analitico/metodologico (geom_point + geom_smooth(lm) + IC 95%
real, nao um unico ponto "falso-preciso" -- o mesmo espirito de
geom_dotsinterval/stat_dotsinterval do ggdist que o usuario mostrou).
"""
import json
import pandas as pd
from matplotlib import font_manager as fm
from plotnine import (
    ggplot, aes, geom_point, geom_smooth, facet_wrap, labs, theme_minimal,
    theme, element_text, element_rect, element_line, element_blank,
    scale_color_manual, scale_x_continuous, coord_cartesian, geom_text
)

OUT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"
FD = "/sessions/kind-gracious-heisenberg/mnt/.claude/skills/canvas-design/canvas-fonts"

# Outfit-Regular/Bold-Fixed.ttf: mesma fonte, com o gap acento<->letra corrigido
# na glyf table (ver fix_accent_font.py) -- necessario p/ "Ciências", "Matemática"
# etc. nos strip_text dos facets, que usam peso bold.
for fname in ["Outfit-Regular-Fixed.ttf", "Outfit-Bold-Fixed.ttf"]:
    fm.fontManager.addfont(f"{OUT}/{fname}")
fm.fontManager.addfont(f"{FD}/JetBrainsMono-Regular.ttf")
FAM_TEXT = fm.FontProperties(fname=f"{OUT}/Outfit-Regular-Fixed.ttf").get_name()
FAM_MONO = fm.FontProperties(fname=f"{FD}/JetBrainsMono-Regular.ttf").get_name()

INK, GRAY, CORAL, CYAN, BG = "#1D1D20", "#8C9298", "#FA5230", "#1FAFEF", "#F1F1F2"
COR = {"LC": CYAN, "CH": CORAL, "CN": INK, "MT": "#8C9298"}
NOME = {"LC": "Linguagens", "CH": "Ciências Humanas", "CN": "Ciências da Natureza", "MT": "Matemática"}

with open(f"{OUT}/dados_previsao_2026.json", encoding="utf-8") as f:
    D = json.load(f)

rows = []
r2_rows = []
for area in ["LC", "CH", "CN", "MT"]:
    for ano, b in D["serie_completa"][area]:
        rows.append({"area": NOME[area], "ano": ano, "dificuldade": b * 100 + 500})
    prev = D["previsao_2026"][area]
    r2_rows.append({"area": NOME[area], "ano": 2011.3,
                     "dificuldade": max(v * 100 + 500 for _, v in D["serie_completa"][area]) + 3,
                     "lbl": f"R² = {prev['r2']:.3f}  (n={prev['n']}, 2010-2025 completo)"})

df = pd.DataFrame(rows)
df["area"] = pd.Categorical(df["area"], categories=[NOME[a] for a in ["LC", "CH", "CN", "MT"]], ordered=True)
r2_df = pd.DataFrame(r2_rows)
r2_df["area"] = pd.Categorical(r2_df["area"], categories=[NOME[a] for a in ["LC", "CH", "CN", "MT"]], ordered=True)
palette = {NOME[a]: COR[a] for a in COR}

p = (
    ggplot(df, aes("ano", "dificuldade", color="area"))
    + geom_smooth(method="lm", se=True, level=0.95, fill="#C7CBD0", color=None, alpha=0.35, size=0)
    + geom_smooth(method="lm", se=False, size=1.1, linetype="dashed", alpha=0.9)
    + geom_point(size=2.6, alpha=0.95)
    + geom_text(r2_df, aes(label="lbl"), family=FAM_MONO, size=7.3, color=GRAY, ha="left", show_legend=False)
    + facet_wrap("~area", scales="free_y", ncol=2)
    + scale_color_manual(values=palette, guide=None)
    + scale_x_continuous(breaks=[2010, 2013, 2016, 2019, 2022, 2025])
    + labs(x="Ano", y="Dificuldade TRI (b×100+500)")
    + theme_minimal(base_family=FAM_TEXT)
    + theme(
        figure_size=(10.2, 6.6),
        plot_background=element_rect(fill=BG, color=None),
        panel_background=element_rect(fill="#FFFFFF", color=None),
        panel_grid_major=element_line(color="#E6E7E9", size=0.6),
        panel_grid_minor=element_blank(),
        strip_background=element_rect(fill=BG, color=None),
        strip_text=element_text(color=INK, family=FAM_TEXT, weight="bold", size=12, ha="left"),
        axis_text=element_text(color=GRAY, family=FAM_MONO, size=8),
        axis_title=element_text(color=INK, family=FAM_TEXT, size=10),
        plot_margin=0.015,
    )
)

p.save(f"{OUT}/plotnine_regressao_dificuldade.png", dpi=170, verbose=False)
print("salvo plotnine_regressao_dificuldade.png")
