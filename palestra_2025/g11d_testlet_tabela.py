#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tabela do testlet LC (Q6-10, Azul P1): parâmetros TRI lado a lado — estilo do deck
(cabeçalho verde). Colunas: Questão | Hab | A (discrim.) | B (dific.) | C (acaso) |
Dif. TRI | Erro | Veredito. "Aliar A e B": veredito combina dificuldade + discriminação.
Números reais do CSV de itens (nada inventado).
"""
import csv

import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, DIF_DIFICIL, DIF_MDIFICIL, W, H)

ITENS = f"{X.BASE}/analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv"
GREEN = "#2EA84F"
GREEN_BG = "#EAF6EE"


def disc_tag(a):
    if a >= 3.0:
        return "navalha"
    if a >= 1.70:
        return "afiado"
    if a >= 1.35:
        return "ok"
    return "fraco"


def load():
    out = {}
    with open(ITENS, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["area"] == "LC" and r["cor"] == "AZUL":
                try:
                    pos = int(float(r["pos_area"]))
                except (ValueError, KeyError):
                    continue
                if 6 <= pos <= 10 and pos not in out:
                    A = float(r["A"]); B = float(r["B"]); C = float(r["C"])
                    cat = r["categoria"]
                    out[pos] = {
                        "pos": pos, "hab": r["habilidade"], "A": A, "B": B, "C": C,
                        "difTRI": round(B * 100 + 500), "erro": round(100 - float(r["pct_acerto"]), 1),
                        "cat": cat, "veredito": f"{cat.lower()} · {disc_tag(A)}",
                    }
    return [out[p] for p in sorted(out)]


def vir(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def main():
    data = load()
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 70
    txt(M, 78, "Testlet Q6–Q10: ", outfitB, 32, INK)
    txt(M + tw("Testlet Q6–Q10: ", outfitB, 32), 78, "os parâmetros TRI lado a lado", outfitB, 32, CORAL)
    txt(M, 116, "A = discrimina (separa quem sabe) · B = dificuldade · C = acerto ao acaso · "
                "Dif. TRI = B×100+500. Crônica “De próprio punho”.", outfit, 15, GRAY)
    logo(ax, W - M - 8, 84, zoom=0.075)

    tx = M
    tw_all = W - 2 * M
    top = 208
    head_h = 60
    rowh = 74
    heads = ["Questão", "Hab.", "A · discrim.", "B · dificul.", "C · acaso", "Dif. TRI", "Erro", "Veredito  (A + B)"]
    cwp = [0.08, 0.08, 0.13, 0.13, 0.10, 0.10, 0.10, 0.28]

    # sombra + corpo BRANCO (evita a sombra preta vazar nas linhas ímpares) + cabeçalho verde
    shadow(tx, top, tw_all, head_h + len(data) * rowh, 12)
    rrect(tx, top, tw_all, head_h + len(data) * rowh, 12, CARD, z=1.8)
    rrect(tx, top, tw_all, head_h, 10, GREEN, z=3)
    rrect(tx, top + head_h - 12, tw_all, 12, 0, GREEN, z=3)
    cx = tx
    for j, hd in enumerate(heads):
        colw = tw_all * cwp[j]
        ha = "left" if j == 7 else "center"
        xh = cx + 18 if j == 7 else cx + colw / 2
        txt(xh, top + head_h * 0.60, hd, monoB, 15, "#FFFFFF", ha=ha, va="center")
        cx += colw

    for i, r in enumerate(data):
        yy = top + head_h + i * rowh
        catcol = DIF_DIFICIL if r["cat"] == "Difícil" else DIF_MDIFICIL
        if i % 2 == 0:
            rrect(tx, yy, tw_all, rowh, 0, GREEN_BG, z=2)
        rrect(tx, yy, 8, rowh, 0, catcol, z=3)  # borda esquerda = categoria
        vals = [
            (f"Q{r['pos']:02d}", monoB, INK),
            (r["hab"], mono, GRAY),
            (vir(r["A"]), monoB, INK),
            (vir(r["B"]), monoB, INK),
            (vir(r["C"]), mono, GRAY),
            (str(r["difTRI"]), mono, INK),
            (f"{vir(r['erro'], 1)}%", mono, CORALd),
            (r["veredito"], mono, INK),
        ]
        cx = tx
        for j, (v, fp, col) in enumerate(vals):
            colw = tw_all * cwp[j]
            if j == 7:
                vc = CORALd if "navalha" in v else INK
                txt(cx + 18, yy + rowh * 0.58, v, fp, 15.5, vc, ha="left", va="center")
            else:
                sz = 21 if j in (2, 3) else 17
                txt(cx + colw / 2, yy + rowh * 0.58, v, fp, sz, col, ha="center", va="center")
            cx += colw

    # faixa de leitura
    by = top + head_h + len(data) * rowh + 36
    bh = 120
    rrect(tx, by, tw_all, bh, 16, "#FCEDE9", z=2)
    rrect(tx, by, 12, bh, 6, CORAL, z=3)
    txt(tx + 40, by + 34, "COMO LER JUNTOS", monoB, 13, CORALd)
    txt(tx + 40, by + 66, "Os 5 têm discriminação muito alta (Baker: A > 1,70).  “afiado” = discrimina muito bem · "
        "“navalha” = A altíssimo (> 3).", outfit, 16, INK)
    txt(tx + 40, by + 98, "Difícil + afiado = dificuldade que informa: o erro alto é sinal, não ruído.",
        outfitB, 16, CORALd)

    assinatura(hp, ax, M, H - 40, extra=" · caderno Azul P1 · parâmetros TRI 3PL")
    return save(fig, "g11d_testlet_tabela")


if __name__ == "__main__":
    main()
