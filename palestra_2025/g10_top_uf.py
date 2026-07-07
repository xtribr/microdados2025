#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leaderboard: a maior nota TRI por estado (média das 4 objetivas) + a escola do aluno.
Dado: top_uf_2025.json (aluno anônimo; nome da escola do Censo Escolar 2025 / INEP).
"""
import json
import re

import xtri_deck as X
from xtri_deck import new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H

D = json.load(open(f"{X.BASE}/palestra_2025/top_uf_2025.json", encoding="utf-8"))
REDE_COL = {"Privada": "#FA5230", "Federal": "#1FAFEF", "Estadual": "#2EC4B6", "Municipal": "#8C9298"}


def clean_nome(s):
    s = s.title()
    s = re.sub(r"\s+(Ltda|Efm|Ei Ef Em|- Ensino Medio.*|- Cin.*|- Matutino.*|Ensino Medio|Integral|Matutino|Vespertino)$", "", s).strip()
    s = s.replace("Col ", "Colégio ").replace("Esc ", "Escola ").replace("Colegio", "Colégio")
    s = re.sub(r"\s+(De|Da|Do|E|Ii|Iii)$", "", s).strip()  # tira conectores/numeração pendurada
    s = re.sub(r"\s{2,}", " ", s).strip(" -")
    return s


def make_leaderboard():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    txt(M, 74, "A maior nota do ENEM 2025 ", outfitB, 32, INK)
    txt(M + tw("A maior nota do ENEM 2025 ", outfitB, 32), 74, "em cada estado", outfitB, 32, CORAL)
    txt(M, 112, "Média das 4 provas objetivas (TRI). Ao lado, a escola do aluno — quase sempre a rede privada.",
        outfit, 15, GRAY)
    logo(ax, W - M - 8, 80, zoom=0.07)

    ufs = sorted(D["best_school"], key=lambda u: -D["best_school"][u]["media4"])
    maxm = D["best_school"][ufs[0]]["media4"]

    cols = [ufs[:14], ufs[14:]]
    colw = (W - 2 * M - 40) / 2
    top = 150
    rowh = (H - 96 - top) / 14
    for ci, colufs in enumerate(cols):
        cx = M + ci * (colw + 40)
        for i, uf in enumerate(colufs):
            r = D["best_school"][uf]
            rank = ufs.index(uf) + 1
            yy = top + i * rowh
            if i % 2 == 0:
                rrect(cx, yy, colw, rowh - 6, 10, "#FFFFFF", z=2)
            # rank + UF badge
            col = REDE_COL.get(r["dep"], GRAY)
            txt(cx + 18, yy + rowh * 0.42, f"{rank}º", monoB, 15, GRAY, va="center")
            rrect(cx + 52, yy + rowh * 0.5 - 17, 52, 34, 8, col, z=3)
            txt(cx + 78, yy + rowh * 0.5, uf, outfitB, 17, "#FFFFFF", ha="center", va="center")
            # média
            txt(cx + 124, yy + rowh * 0.42, f"{str(r['media4']).replace('.', ',')}", outfitB, 21, INK, va="center")
            # escola + cidade
            nome = clean_nome(r.get("escola_nome", "?"))
            if len(nome) > 40:
                nome = nome[:39] + "…"
            txt(cx + 210, yy + rowh * 0.34, nome, outfit, 13.5, INK, va="center")
            txt(cx + 210, yy + rowh * 0.66, f"{r.get('escola_municipio','')} · {r['dep']}", mono, 10.5, GRAY, va="center")

    # legenda de rede
    lx = M
    ly = H - 66
    for i, (rede, c) in enumerate([("Privada", REDE_COL["Privada"]), ("Federal", REDE_COL["Federal"])]):
        rrect(lx + i * 150, ly - 12, 20, 20, 5, c, z=5)
        txt(lx + i * 150 + 28, ly, rede, mono, 12, INK, va="center")
    assinatura(hp, ax, M + 340, H - 44, extra=" · escola: Censo Escolar 2025")
    return save(fig, "g10a_top_uf_leaderboard")


if __name__ == "__main__":
    make_leaderboard()
