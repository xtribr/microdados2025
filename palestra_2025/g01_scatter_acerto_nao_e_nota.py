#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráfico assinatura do deck: "Acerto não é nota".
Scatter Número de Acertos × NU_NOTA_TRI, colorido por acert_dif (proporção de itens
DIFÍCEIS que o candidato acertou) — mesmo encoding do deck 2024. Um por área.
Amostra Regular P1 (~100 mil/área); contagem de acertos máximos é nacional (real).
"""
import csv
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, style_axes, save,
                       outfitB, outfit, mono, monoB, INK, GRAY, CARD, W, H)

AREAS = {
    "LC": ("Linguagens e Códigos", 45, "#FF9F1C"),
    "CH": ("Ciências Humanas", 45, "#E84855"),
    "CN": ("Ciências da Natureza", 45, "#2EC4B6"),
    "MT": ("Matemática", 43, "#3A86FF"),
}
IV = {"LC": 45, "CH": 45, "CN": 42, "MT": 43}
# contagem nacional real no topo (de acertos_para_nota_2025_full.csv)
NACIONAL_TOPO = {
    "LC": (45, 85, 794.5), "CH": (45, 15, 856.4),
    "CN": (42, 83, 858.7), "MT": (43, 573, 980.3),
}


def load(area):
    xs, ys, ad = [], [], []
    path = f"{X.BASE}/analises_primi_2025_cop30/outputs/amostra_xtri_2025_{area}.csv"
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["area"] != area or r["aplicacao"] != "Regular P1":
                continue
            try:
                a = int(r["acertos"]); nota = float(r["nota"])
            except (ValueError, KeyError):
                continue
            if a < 1 or nota <= 0:  # tira o caso degenerado (0 acertos / nota-piso)
                continue
            try:
                dif = float(r["acert_dif"])
            except (ValueError, KeyError):
                dif = np.nan
            xs.append(a); ys.append(nota); ad.append(dif)
    return np.array(xs), np.array(ys), np.array(ad)


def make(area):
    nome, _, _ = AREAS[area]
    iv = IV[area]
    xs, ys, ad = load(area)
    # jitter horizontal pequeno pra separar os pontos por coluna de acertos
    rng = np.random.RandomState(42)
    xj = xs + rng.uniform(-0.32, 0.32, size=len(xs))

    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 70
    # card branco
    cx, cy, cw, ch = M, 150, W - 2 * M, H - 150 - 96
    shadow(cx, cy, cw, ch, 26)
    rrect(cx, cy, cw, ch, 26, CARD, z=2)

    # título + subtítulo
    txt(M, 78, f"ENEM 2025 — {nome}: ", outfitB, 34, INK)
    xx = M + tw(f"ENEM 2025 — {nome}: ", outfitB, 34)
    txt(xx, 78, "acerto não é nota", outfitB, 34, X.CORAL)
    n_topo = NACIONAL_TOPO[area]
    txt(M, 116, f"Mesmo nº de acertos → notas diferentes. Cor = proporção de itens DIFÍCEIS "
                f"que o candidato acertou.  |  {n_topo[1]} candidatos fizeram {n_topo[0]} acertos "
                f"(nota máxima {str(n_topo[2]).replace('.', ',')}).",
        outfit, 15, GRAY)
    logo(ax, W - M - 8, 84, zoom=0.075)

    # eixo do scatter dentro do card
    pad_l, pad_r, pad_t, pad_b = 90, 150, 40, 70
    l = (cx + pad_l) / W
    b = 1 - (cy + ch - pad_b) / H
    w = (cw - pad_l - pad_r) / W
    h = (ch - pad_t - pad_b) / H
    axc = fig.add_axes([l, b, w, h])
    axc.set_facecolor(CARD)

    sc = axc.scatter(xj, ys, c=ad, cmap="rainbow_r", vmin=0, vmax=1,
                     s=7, alpha=0.35, linewidths=0, rasterized=True)
    axc.set_xlim(0, iv + 1)
    ymin = max(280, np.floor(ys.min() / 50) * 50)
    ymax = np.ceil(ys.max() / 50) * 50
    axc.set_ylim(ymin, ymax)
    style_axes(axc, f"Número de Acertos ({area}, de {iv})", "Nota TRI oficial (NU_NOTA_TRI)")

    # colorbar (acert_dif)
    cbar = fig.colorbar(ScalarMappable(norm=Normalize(0, 1), cmap="rainbow_r"),
                        ax=axc, fraction=0.035, pad=0.02)
    cbar.set_label("acerto de difíceis", fontproperties=outfit, fontsize=12, color=INK)
    cbar.ax.tick_params(labelsize=10, colors=GRAY)
    for t in cbar.ax.get_yticklabels():
        t.set_fontproperties(mono)

    assinatura(hp, ax, M, H - 44, extra=f" · amostra Regular P1 (~100 mil, {area})")
    return save(fig, f"g01_scatter_{area}")


if __name__ == "__main__":
    for a in ["LC", "CH", "CN", "MT"]:
        make(a)
    print("FIM scatters base")
