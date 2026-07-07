#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos de redação para o deck 2025 (tema: a C2). Dado real: redacao_2024_2025.json
(médias nacionais entre redações VÁLIDAS, 2024 vs 2025).
  g02a_c2_hero      — spotlight da C2 (2024 vs 2025, maior queda das 5)
  g02b_comp_5       — as 5 competências 2024 vs 2025, C2 destacada
  g02c_status_2025  — status das redações 2025 (válidas + motivos de problema)
  g02d_faixas_2025  — distribuição das notas de redação 2025 (faixas de 100)
"""
import json
import numpy as np

import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, style_axes, save,
                       outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd,
                       CYAN, CYANd, W, H)

D = json.load(open(f"{X.BASE}/palestra_2025/redacao_2024_2025.json", encoding="utf-8"))
COMP_NOME = {
    "C1": "Norma culta", "C2": "Compreensão do tema", "C3": "Seleção de argumentos",
    "C4": "Coesão / coerência", "C5": "Proposta de intervenção",
}


def header(ax, hp, M, titulo_pre, titulo_hi, sub):
    txt = hp["txt"]; tw = hp["tw"]
    txt(M, 78, titulo_pre, outfitB, 34, INK)
    txt(M + tw(titulo_pre, outfitB, 34), 78, titulo_hi, outfitB, 34, CORAL)
    txt(M, 116, sub, outfit, 15, GRAY)
    logo(ax, W - M - 8, 84, zoom=0.075)


def card(hp, M):
    cx, cy, cw, ch = M, 150, W - 2 * M, H - 150 - 96
    hp["shadow"](cx, cy, cw, ch, 26)
    hp["rrect"](cx, cy, cw, ch, 26, CARD, z=2)
    return cx, cy, cw, ch


# ---------------- g02a: C2 HERO ----------------
def c2_hero():
    c2 = D["delta_comp"]["C2"]
    a, b, dlt = c2["2024"], c2["2025"], c2["delta"]
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 70
    header(ax, hp, M, "Redação 2025: ", "a C2 foi a que mais caiu",
           "Compreensão da proposta e desenvolvimento do tema — a competência historicamente "
           "mais alta e estável, agora recuou o dobro das demais.")
    cx, cy, cw, ch = card(hp, M)

    # duas colunas: barras 2024 vs 2025 (esq) + número-herói da queda (dir)
    # painel esquerdo: 2 barras verticais
    bx0 = cx + 120
    base_y = cy + ch - 150
    top_y = cy + 120
    scale = (base_y - top_y) / 200.0  # 0-200
    barw = 150
    gap = 120
    for i, (lab, val, col) in enumerate([("2024", a, GRAY), ("2025", b, CORALd)]):
        x = bx0 + i * (barw + gap)
        hbar = val * scale
        rrect(x, base_y - hbar, barw, hbar, 16, col, z=4)
        txt(x + barw / 2, base_y - hbar - 22, f"{str(val).replace('.', ',')}", outfitB, 34, col, ha="center")
        txt(x + barw / 2, base_y + 40, lab, monoB, 20, INK, ha="center")
    # eixo base
    ax.plot([bx0 - 30, bx0 + 2 * barw + gap + 30], [base_y, base_y], color="#CFD2D5", lw=2, zorder=3)
    txt(bx0 - 30, top_y - 10, "Nota média da C2 (0–200)", mono, 13, GRAY)

    # seta de queda entre as barras
    x1 = bx0 + barw / 2
    x2 = bx0 + barw + gap + barw / 2
    y1 = base_y - a * scale - 70
    y2 = base_y - b * scale - 70
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=CORAL, lw=3), zorder=6)

    # painel direito: número-herói
    px = cx + cw - 620
    py = cy + 150
    pw, phh = 540, ch - 300
    rrect(px, py, pw, phh, 22, "#FCEDE9", z=3)
    txt(px + pw / 2, py + 130, f"{dlt:+.1f}".replace(".", ",").replace("+", "−" if dlt < 0 else "+"),
        outfitB, 96, CORALd, ha="center")
    # (dlt é negativo; formata como −15,6)
    txt(px + pw / 2, py + 200, "pontos na C2", outfitB, 30, INK, ha="center")
    txt(px + pw / 2, py + 270, "de 2024 para 2025", outfit, 20, GRAY, ha="center")
    # comparativo com as outras
    outras = [abs(D["delta_comp"][k]["delta"]) for k in ["C1", "C3", "C4", "C5"]]
    media_outras = sum(outras) / len(outras)
    mult = f"{abs(dlt) / media_outras:.1f}".replace(".", ",")
    txt(px + pw / 2, py + 350, f"{mult}× a queda média", outfitB, 26, CORAL, ha="center")
    txt(px + pw / 2, py + 388, "das outras 4 competências", outfit, 17, GRAY, ha="center")

    assinatura(hp, ax, M, H - 44, extra=f" · válidas: {D['2024']['n_validas']:,} (2024) / {D['2025']['n_validas']:,} (2025)".replace(",", "."))
    return save(fig, "g02a_c2_hero")


# ---------------- g02b: 5 COMPETÊNCIAS ----------------
def comp_5():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 70
    header(ax, hp, M, "Redação — ", "as 5 competências caíram, a C2 despencou",
           "Média nacional por competência (redações válidas), 2024 → 2025. Escala 0–200 por competência.")
    cx, cy, cw, ch = card(hp, M)

    comps = ["C1", "C2", "C3", "C4", "C5"]
    base_y = cy + ch - 170
    top_y = cy + 90
    scale = (base_y - top_y) / 200.0
    n = len(comps)
    slot = (cw - 240) / n
    barw = 62
    x0 = cx + 150
    for i, c in enumerate(comps):
        d = D["delta_comp"][c]
        a, b, dlt = d["2024"], d["2025"], d["delta"]
        cxx = x0 + i * slot
        is_c2 = c == "C2"
        col24 = "#B9BDC2" if not is_c2 else "#8C9298"
        col25 = CORALd if is_c2 else "#F6A58C"
        # barra 2024
        h24 = a * scale
        rrect(cxx, base_y - h24, barw, h24, 10, col24, z=4)
        txt(cxx + barw / 2, base_y - h24 - 14, f"{a:.0f}", mono, 14, GRAY, ha="center")
        # barra 2025
        h25 = b * scale
        rrect(cxx + barw + 12, base_y - h25, barw, h25, 10, col25, z=4)
        txt(cxx + barw + 12 + barw / 2, base_y - h25 - 14, f"{b:.0f}", monoB, 14,
            CORALd if is_c2 else GRAY, ha="center")
        # rótulo competência
        lab_col = CORALd if is_c2 else INK
        txt(cxx + barw + 6, base_y + 40, c, outfitB, 22, lab_col, ha="center")
        txt(cxx + barw + 6, base_y + 66, COMP_NOME[c], outfit, 12.5, GRAY, ha="center")
        # delta
        dbox_w = 108
        dbx = cxx + barw + 6 - dbox_w / 2
        dby = base_y + 84
        rrect(dbx, dby, dbox_w, 32, 10, "#FCEDE9" if is_c2 else "#EDEEEF", z=4)
        txt(cxx + barw + 6, dby + 22, f"{dlt:+.1f}".replace(".", ",").replace("+", "−" if dlt < 0 else "+"),
            monoB, 15, CORALd if is_c2 else GRAY, ha="center")

    ax.plot([x0 - 30, cx + cw - 90], [base_y, base_y], color="#CFD2D5", lw=2, zorder=3)
    # legenda
    lx = cx + cw - 360
    ly = cy + 70
    rrect(lx, ly, 24, 24, 6, "#8C9298", z=5); txt(lx + 34, ly + 18, "2024", mono, 15, INK)
    rrect(lx + 130, ly, 24, 24, 6, CORALd, z=5); txt(lx + 164, ly + 18, "2025", mono, 15, INK)

    assinatura(hp, ax, M, H - 44)
    return save(fig, "g02b_comp_5")


# ---------------- g02c: STATUS 2025 ----------------
def status_2025():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 70
    st = D["2025"]["status_count"]
    total = D["2025"]["n_com_status"]
    validas = st.get("Sem problemas", 0)
    header(ax, hp, M, "Redação 2025: ", f"{100*validas/total:.1f}".replace(".", ",") + "% sem problemas",
           f"De {total:,} redações com status, {validas:,} foram válidas. Os demais motivos abaixo.".replace(",", "."))
    cx, cy, cw, ch = card(hp, M)

    # barra grande de válidas em cima
    bx = cx + 80
    bw = cw - 160
    by = cy + 90
    rrect(bx, by, bw, 70, 16, "#E7E8EA", z=3)
    rrect(bx, by, bw * validas / total, 70, 16, "#2EA84F", z=4)
    txt(bx + 24, by + 45, f"VÁLIDAS (sem problemas)  {validas:,}  ({100*validas/total:.1f}%)".replace(",", "."),
        monoB, 17, "#FFFFFF")

    # motivos de problema (barras horizontais)
    motivos = [(k, v) for k, v in st.items() if k != "Sem problemas"]
    motivos.sort(key=lambda x: -x[1])
    my0 = by + 130
    rowh = (ch - (my0 - cy) - 40) / len(motivos)
    maxv = max(v for _, v in motivos)
    bar_x = cx + 430
    barmax = cw - 760  # deixa coluna à direita p/ o rótulo caber dentro do card
    for i, (k, v) in enumerate(motivos):
        yy = my0 + i * rowh
        txt(bx, yy + rowh * 0.5, k, outfit, 17, INK, va="center")
        blen = barmax * v / maxv
        rrect(bar_x, yy + rowh * 0.5 - 15, blen, 30, 10, CORAL, z=4)
        pct = f"{100*v/total:.2f}".replace(".", ",")
        txt(bar_x + blen + 14, yy + rowh * 0.5, f"{v:,}".replace(",", ".") + f"  ({pct}%)",
            monoB, 15, INK, va="center")

    assinatura(hp, ax, M, H - 44)
    return save(fig, "g02c_status_2025")


# ---------------- g02d: FAIXAS DE NOTA 2025 ----------------
def faixas_2025():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 70
    bands = D["2025"]["redacao_bands_validas"]
    total = D["2025"]["n_validas"]
    # agrupa 1000 dentro de 900-999? não: mantém 1000 separado como "1000"
    order = ["0", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1000"]
    labels = {"0": "0–99", "100": "100–199", "200": "200–299", "300": "300–399",
              "400": "400–499", "500": "500–599", "600": "600–699", "700": "700–799",
              "800": "800–899", "900": "900–999", "1000": "1000"}
    mil = int(bands.get("1000", 0))
    header(ax, hp, M, "Redação 2025: ", "onde estão as notas",
           f"Distribuição das {total:,} redações válidas por faixa de 100 pontos. "
           f"Apenas {mil} pessoas tiraram 1000.".replace(",", "."))
    cx, cy, cw, ch = card(hp, M)

    base_y = cy + ch - 120
    top_y = cy + 90
    n = len(order)
    slot = (cw - 200) / n
    barw = slot * 0.62
    x0 = cx + 110
    maxpct = max(int(bands.get(k, 0)) / total for k in order) * 100
    scale = (base_y - top_y) / maxpct
    for i, k in enumerate(order):
        v = int(bands.get(k, 0))
        pct = 100 * v / total
        xx = x0 + i * slot
        hh = pct * scale
        # cor por faixa de dificuldade (600+ = destaque)
        if k in ("0", "100", "200", "300"):
            col = "#C7CBD0"
        elif k in ("400", "500"):
            col = "#9FD8F5"
        elif k in ("600", "700"):
            col = CYAN
        else:
            col = CORAL
        if hh >= 4:
            rrect(xx, base_y - hh, barw, hh, min(8, hh / 2), col, z=4)
        else:  # faixa quase vazia: traço fino, sem artefato de arredondamento
            ax.add_patch(__import__("matplotlib").patches.Rectangle(
                (xx, base_y - 4), barw, 4, fc=col, ec="none", zorder=4))
        txt(xx + barw / 2, base_y - max(hh, 6) - 14, f"{pct:.1f}%".replace(".", ","),
            monoB, 13, INK, ha="center")
        txt(xx + barw / 2, base_y + 34, labels[k], mono, 12, GRAY, ha="center", va="center")
    ax.plot([x0 - 30, cx + cw - 70], [base_y, base_y], color="#CFD2D5", lw=2, zorder=3)
    txt(x0 - 30, top_y - 6, "% das redações válidas", mono, 13, GRAY)

    assinatura(hp, ax, M, H - 44)
    return save(fig, "g02d_faixas_2025")


if __name__ == "__main__":
    c2_hero()
    comp_5()
    status_2025()
    faixas_2025()
    print("FIM redação")
