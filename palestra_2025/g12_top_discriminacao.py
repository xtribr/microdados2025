#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A questão mais discriminativa (maior parâmetro A da TRI) de CADA área — 1ª aplicação (P1), caderno Azul.
Mostra: cor + nº da questão (do Azul), matéria + assunto (lido do PDF oficial), A, B e erro.
Parâmetros A/B/erro vêm do CSV real de itens; assunto/matéria vêm do caderno Azul (PDF INEP).
"""
import csv

import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, W, H)

ITENS = f"{X.BASE}/analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv"
AREA_COL = {"LC": "#1FAFEF", "CH": "#E84855", "CN": "#2EC4B6", "MT": "#3A86FF"}
AREA_NOME = {"LC": "Linguagens", "CH": "Ciências Humanas", "CN": "Ciências da Natureza", "MT": "Matemática"}

# Campeão de discriminação por área: nº da questão (Azul) + matéria/assunto (do PDF oficial).
CHAMP = {
    "LC": {"q": 4,   "lingua": "ING", "materia": "Inglês",     "assunto": "“Snowflake generation”: resiliência e juventude"},
    "CH": {"q": 50,  "lingua": None,  "materia": "Filosofia",  "assunto": "Justiça × direito (Derrida) e desobediência civil"},
    "CN": {"q": 120, "lingua": None,  "materia": "Física",     "assunto": "Cinemática: sensor de movimento (v, tempo, distância)"},
    "MT": {"q": 167, "lingua": None,  "materia": "Matemática", "assunto": "Custo de combustível: GNV × gasolina (proporção)"},
}


def load():
    by = {a: {} for a in CHAMP}
    with open(ITENS, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["cor"] != "AZUL":
                continue
            a = r["area"]
            if a not in CHAMP:
                continue
            try:
                pos = int(float(r["co_posicao"]))
            except (ValueError, KeyError):
                continue
            ch = CHAMP[a]
            if pos == ch["q"] and (ch["lingua"] is None or r.get("lingua_label") == ch["lingua"]):
                by[a] = {"A": float(r["A"]), "B": float(r["B"]),
                         "erro": round(100 - float(r["pct_acerto"])), "hab": r["habilidade"]}
    return by


def vir(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def main():
    d = load()
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    txt(M, 76, "A questão mais ", outfitB, 32, INK)
    txt(M + tw("A questão mais ", outfitB, 32), 76, "discriminativa", outfitB, 32, CORAL)
    txt(M + tw("A questão mais discriminativa", outfitB, 32), 76, " de cada área", outfitB, 32, INK)
    txt(M, 114, "Maior parâmetro A da TRI — o quanto o item separa quem sabe de quem não sabe. "
                "1ª aplicação (P1), caderno Azul.", outfit, 15, GRAY)
    logo(ax, W - M - 4, 84, zoom=0.072)

    top = 168
    rowh = 196
    gap = 18
    for i, a in enumerate(["LC", "CH", "CN", "MT"]):
        ch = CHAMP[a]; p = d[a]; col = AREA_COL[a]
        ry = top + i * rowh
        cardh = rowh - gap
        cy = ry + cardh / 2
        shadow(M, ry, W - 2 * M, cardh, 18)
        rrect(M, ry, W - 2 * M, cardh, 18, CARD, z=2)
        rrect(M, ry, 12, cardh, 6, col, z=3)  # faixa lateral da área

        # badge da área
        bx = M + 34
        rrect(bx, cy - 46, 96, 92, 16, col, z=3)
        txt(bx + 48, cy, a, outfitB, 34, "#FFFFFF", ha="center", va="center", z=4)

        # cor + número
        qx = bx + 138
        txt(qx, cy - 22, "CADERNO AZUL", mono, 11, GRAY, va="center")
        txt(qx, cy + 18, f"Q{ch['q']}", outfitB, 34, INK, va="center")
        txt(qx + tw(f"Q{ch['q']}", outfitB, 34) + 12, cy + 20, f"· {p['hab']}", mono, 13, GRAY, va="center")

        # matéria + assunto
        ax_ = qx + 250
        txt(ax_, cy - 22, ch["materia"].upper() + ("  · só quem escolheu essa língua" if a == "LC" else ""),
            monoB, 12.5, col, va="center")
        txt(ax_, cy + 16, ch["assunto"], outfit, 18.5, INK, va="center")

        # bloco direito: A grande + B/erro
        rx = W - M - 40
        txt(rx, ry + 40, "DISCRIMINAÇÃO (A)", mono, 10.5, GRAY, ha="right", va="center")
        txt(rx, cy + 6, vir(p["A"]), outfitB, 48, col, ha="right", va="center")
        txt(rx, ry + cardh - 30, f"dificuldade B {vir(p['B'])}  ·  erro {p['erro']}%",
            mono, 12.5, GRAY, ha="right", va="center")

    txt(M, H - 66, "Nº da questão referente ao caderno Azul (outras cores renumeram os itens). "
        "A discriminação (A) é a mesma em todas as cores.", mono, 11, GRAY)
    assinatura(hp, ax, M, H - 38, extra=" · assunto do caderno Azul (PDF oficial)")
    return save(fig, "g12_top_discriminacao")


if __name__ == "__main__":
    main()
