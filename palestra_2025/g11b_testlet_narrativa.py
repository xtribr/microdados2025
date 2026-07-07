#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Card narrativo do TESTLET de Linguagens (Azul P1): Q6–Q10 saem da MESMA crônica
("De próprio punho"). Mostra o que cada questão pede + a taxa de erro, em escada,
para responder "como a turma absorveu o formato": rasa passa, profunda trava.
Números (erro, dificuldade, habilidade) vêm do CSV real de itens; enunciados
resumidos vêm do caderno Azul P1 (PDF oficial INEP), citado no rodapé.
"""
import csv

import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, DIF_DIFICIL, DIF_MDIFICIL, W, H)

ITENS = f"{X.BASE}/analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv"

# Enunciado resumido + gabarito por posição — do caderno Azul P1 (verificado no PDF).
DESC = {
    6:  {"gab": "E", "pede": "Reconhecer o gênero bilhete dentro da crônica.", "faixa": "reconhecer"},
    7:  {"gab": "C", "pede": "Identificar o que faz o texto ser uma crônica.", "faixa": "reconhecer"},
    8:  {"gab": "D", "pede": "Contrastar a escrita manuscrita e a digital.", "faixa": "interpretar"},
    9:  {"gab": "C", "pede": "Inferir a conclusão da autora sobre a escrita.", "faixa": "interpretar"},
    10: {"gab": "E", "pede": "Achar o recurso que sintetiza a opinião dela.", "faixa": "interpretar"},
}


def load_testlet():
    rows = {}
    with open(ITENS, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["area"] == "LC" and r["cor"] == "AZUL":
                try:
                    pos = int(float(r["pos_area"]))
                except (ValueError, KeyError):
                    continue
                if 6 <= pos <= 10 and pos not in rows:
                    rows[pos] = {
                        "pos": pos,
                        "hab": r["habilidade"],
                        "erro": round(100 - float(r["pct_acerto"]), 1),
                        "cat": r["categoria"],
                    }
    return [rows[p] for p in sorted(rows)]


def wrap(tw, s, fp, sz, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, fp, sz) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    data = load_testlet()

    M = 50
    # ---- título ----
    txt(M, 74, "Um texto, cinco perguntas: ", outfitB, 33, INK)
    txt(M + tw("Um texto, cinco perguntas: ", outfitB, 33), 74, "onde a turma travou", outfitB, 33, CORAL)
    txt(M, 116, "Azul (P1): as Q6–Q10 saem todas da crônica “De próprio punho”. "
                "O erro sobe conforme a pergunta exige leitura mais profunda.", outfit, 16, GRAY)
    logo(ax, W - M - 4, 86, zoom=0.075)

    # ---- escada de cards ----
    n = len(data)
    gap = 24
    cw = (W - 2 * M - (n - 1) * gap) / n
    ch = 340
    y0 = 306
    rise = 34
    pad = 24
    for i, d in enumerate(data):
        xc = M + i * (cw + gap)
        yc = y0 - i * rise
        dcol = DIF_DIFICIL if d["cat"] == "Difícil" else DIF_MDIFICIL
        htxt = INK if d["cat"] == "Difícil" else "#FFFFFF"
        info = DESC[d["pos"]]
        # sombra + corpo branco + cabeçalho colorido
        shadow(xc, yc, cw, ch, 16)
        rrect(xc, yc, cw, ch, 16, CARD, z=2)
        rrect(xc, yc, cw, 58, 16, dcol, z=3)
        rrect(xc, yc + 40, cw, 26, 0, CARD, z=3)  # cobre a barra de baixo do header p/ ficar reto
        # header
        txt(xc + pad, yc + 40, f"Q{d['pos']:02d}", outfitB, 27, htxt, z=6)
        txt(xc + cw - pad, yc + 38, f"Habilidade {d['hab']}", mono, 12.5, htxt, ha="right", z=6)
        # rótulo dificuldade
        txt(xc + pad, yc + 92, d["cat"].upper(), monoB, 12, dcol, z=5)
        # o que pede
        txt(xc + pad, yc + 122, "O QUE PEDE", mono, 10.5, GRAY, z=5)
        lines = wrap(tw, info["pede"], outfit, 16, cw - 2 * pad)
        for li, ln in enumerate(lines[:3]):
            txt(xc + pad, yc + 148 + li * 25, ln, outfit, 16, INK, z=5)
        # número de erro (embaixo, sempre escuro p/ contraste)
        txt(xc + pad, yc + ch - 58, f"{str(d['erro']).replace('.', ',')}%", outfitB, 44, INK, z=5)
        txt(xc + pad, yc + ch - 32, "de erro", mono, 12, GRAY, z=5)
        txt(xc + cw - pad, yc + ch - 32, f"gab. {info['gab']}", mono, 11, GRAY, ha="right", z=5)

    # ---- faixa de síntese ----
    by = 690
    bh = 214
    shadow(M, by, W - 2 * M, bh, 20)
    rrect(M, by, W - 2 * M, bh, 20, "#FCEDE9", z=2)
    rrect(M, by, 12, bh, 6, CORAL, z=3)
    q7 = next(d["erro"] for d in data if d["pos"] == 7)
    q8 = next(d["erro"] for d in data if d["pos"] == 8)
    salto = round(q8 - q7, 1)
    txt(M + 44, by + 46, "O QUE O TESTLET REVELA", monoB, 13, CORALd, z=5)
    txt(M + 44, by + 92, "Reconhecer gênero e tipo (Q6–Q7): erro entre 49% e 54% — perto do resto da prova.",
        outfit, 19, INK, z=5)
    txt(M + 44, by + 130, "Interpretar a tese e a síntese da autora (Q8–Q10): erro pula para 66%–69%.",
        outfit, 19, INK, z=5)
    txt(M + 44, by + 176, f"Mesmo texto — o que subiu o erro foi a profundidade da leitura "
        f"(+{str(salto).replace('.', ',')} pontos ao sair do reconhecimento para a interpretação).",
        outfitB, 19, CORALd, z=5)

    assinatura(hp, ax, M, H - 40, extra=" · caderno Azul P1 · enunciados do PDF oficial")
    return save(fig, "g11b_testlet_narrativa")


if __name__ == "__main__":
    main()
