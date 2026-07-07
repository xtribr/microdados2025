#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tabela de referência Acerto → Nota (por área), estilo do deck (3 painéis, cabeçalho verde).
Colunas: Acerto | Freq (n) | Mín | Med | Máx  — nota TRI oficial por nº de acertos.
Dado: acertos_para_nota_2025_full.csv (população Regular P1 completa).
"""
import csv
from collections import defaultdict

import xtri_deck as X
from xtri_deck import new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB, INK, GRAY, W, H

NOMES = {"LC": "Linguagens e Códigos", "CH": "Ciências Humanas",
         "CN": "Ciências da Natureza", "MT": "Matemática"}
GREEN = "#2EA84F"
GREEN_BG = "#EAF6EE"


def load():
    rows = defaultdict(list)
    with open(f"{X.BASE}/posts_acertos_nota/acertos_para_nota_2025_full.csv") as f:
        for r in csv.DictReader(f):
            rows[r["area"]].append(r)
    for a in rows:
        rows[a].sort(key=lambda x: int(x["acertos"]))
    return rows


def fmt_n(v):
    return f"{int(v):,}".replace(",", ".")


def fmt_nota(v):
    return f"{float(v):.1f}".replace(".", ",")


def make(area, rows):
    fig, ax, hp = new_slide()
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 70
    txt(M, 78, f"{NOMES[area]} — ", outfitB, 32, INK)
    txt(M + hp["tw"](f"{NOMES[area]} — ", outfitB, 32), 78, "quantos acertos valem quanto",
        outfitB, 32, X.CORAL)
    txt(M, 116, "Nota TRI oficial por número de acertos (Regular P1): frequência, mínima, mediana e máxima.",
        outfit, 15, GRAY)
    logo(ax, W - M - 8, 84, zoom=0.075)

    n = len(rows)
    per = -(-n // 3)  # ceil
    panels = [rows[i * per:(i + 1) * per] for i in range(3)]

    top = 165
    bottom = H - 96
    gap = 34
    pw = (W - 2 * M - 2 * gap) / 3
    # colunas: Acerto | Freq | Mín | Med | Máx  (proporções)
    cw = [0.16, 0.30, 0.18, 0.18, 0.18]
    heads = ["Acerto", "Freq", "Mín", "Med", "Máx"]
    rowh = min(46, (bottom - top) / (per + 1))

    for pi, panel in enumerate(panels):
        if not panel:
            continue
        px = M + pi * (pw + gap)
        # cabeçalho verde
        rrect(px, top, pw, rowh, 8, GREEN, z=3)
        cx = px
        for j, hd in enumerate(heads):
            colw = pw * cw[j]
            txt(cx + colw / 2, top + rowh * 0.62, hd, monoB, 14.5, "#FFFFFF", ha="center")
            cx += colw
        # linhas
        for i, r in enumerate(panel):
            yy = top + (i + 1) * rowh
            if i % 2 == 0:
                rrect(px, yy, pw, rowh, 0, GREEN_BG, z=2)
            vals = [r["acertos"], fmt_n(r["n"]), fmt_nota(r["min"]),
                    fmt_nota(r["mediana"]), fmt_nota(r["max"])]
            cx = px
            for j, v in enumerate(vals):
                colw = pw * cw[j]
                fp = monoB if j == 0 else mono
                col = INK if j != 3 else X.CORALd  # mediana destacada
                txt(cx + colw / 2, yy + rowh * 0.62, v, fp, 13, col, ha="center")
                cx += colw

    assinatura(hp, ax, M, H - 44, extra=f" · Regular P1 ({area}), população completa")
    return save(fig, f"g07_tabela_acerto_nota_{area}")


if __name__ == "__main__":
    rows = load()
    for a in ["LC", "CH", "CN", "MT"]:
        make(a, rows[a])
    print("FIM tabelas")
