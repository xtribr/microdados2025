#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel-resumo do estudo CEI: N, médias TRI por área × Brasil, redação, incoerência e alertas."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H)

D = Path(__file__).resolve().parent
R = json.loads((D / "cei_resumo.json").read_text())
X.OUTDIR = str(D / "graficos")

ROM = "CEI Romualdo"
RF = "CEI Roberto Freire"
AREAS = [("LC", "Linguagens"), ("CH", "Humanas"), ("CN", "Natureza"), ("MT", "Matemática")]


def vir(x, d=1):
    return f"{float(x):.{d}f}".replace(".", ",")


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    txt(M, 76, "CEI Romualdo ", outfitB, 32, CORAL)
    x2 = M + tw("CEI Romualdo ", outfitB, 32)
    txt(x2, 76, "× ", outfitB, 32, INK)
    txt(x2 + tw("× ", outfitB, 32), 76, "CEI Roberto Freire", outfitB, 32, CYAN)
    txt(M, 114, f"Raio-X ENEM 2025 — {R['n_alunos'][ROM]} + {R['n_alunos'][RF]} concluintes com escola declarada, "
                "corrigidos item a item (175 itens válidos).", outfit, 15, GRAY)
    logo(ax, W - M - 4, 84, zoom=0.072)

    # ---- tabela de médias ----
    ty = 170
    rowh = 64
    tw_all = W - 2 * M
    cols = [0.26, 0.22, 0.26, 0.26]
    heads = ["Área", ROM, RF, "Brasil (Regular P1)"]
    hcols = [INK, CORAL, CYANd, GRAY]
    shadow(M, ty, tw_all, rowh * 6, 14)
    rrect(M, ty, tw_all, rowh * 6, 14, CARD, z=2)
    cx = M
    for j, hd in enumerate(heads):
        txt(cx + tw_all * cols[j] / 2, ty + rowh * 0.62, hd, monoB, 14, hcols[j], ha="center")
        cx += tw_all * cols[j]
    ax.plot([M + 24, W - M - 24], [ty + rowh - 6, ty + rowh - 6], color="#E3E4E6", lw=1.4, zorder=4)
    for i, (a, nome) in enumerate(AREAS + [("RED", "Redação")]):
        yy = ty + (i + 1) * rowh
        if i % 2 == 0:
            rrect(M, yy, tw_all, rowh, 0, "#F7F7F8", z=2.5)
        if a == "RED":
            vals = [R["redacao"][ROM], R["redacao"][RF], None]
        else:
            vals = [R["medias"][ROM][a], R["medias"][RF][a], R["nacional_regular_p1"][a]]
        cx = M
        txt(cx + tw_all * cols[0] / 2, yy + rowh * 0.62, nome, outfit, 17, INK, ha="center", z=5)
        cx += tw_all * cols[0]
        for j, v in enumerate(vals):
            col = [CORALd, CYANd, GRAY][j]
            s = vir(v) if v is not None else "—"
            txt(cx + tw_all * cols[j + 1] / 2, yy + rowh * 0.62, s, outfitB if j < 2 else mono,
                21 if j < 2 else 16, col, ha="center", z=5)
            cx += tw_all * cols[j + 1]

    # ---- incoerência ----
    by = ty + rowh * 6 + 36
    bw = (tw_all - 30) / 2
    bh = 150
    for k, (nome, col, cold) in enumerate([(ROM, CORAL, CORALd), (RF, CYAN, CYANd)]):
        bx = M + k * (bw + 30)
        shadow(bx, by, bw, bh, 16)
        rrect(bx, by, bw, bh, 16, CARD, z=2)
        rrect(bx, by, 10, bh, 5, col, z=3)
        inc = R["incoer"][nome]
        txt(bx + 34, by + 38, f"ÍNDICE DE CHUTE (INCOERÊNCIA) — {nome.upper()}", monoB, 12, cold, z=5)
        txt(bx + 34, by + 88, vir(inc["media"], 2), outfitB, 40, INK, z=5)
        txt(bx + 34 + tw(vir(inc["media"], 2), outfitB, 40) + 14, by + 88, "média por aluno", mono, 12, GRAY, z=5)
        txt(bx + 34, by + 122, f"mediana {vir(inc['mediana'],0)} · máx {inc['max']} · só {vir(inc['zero_pct'])}% com zero",
            mono, 12.5, GRAY, z=5)

    # ---- leitura ----
    ly = by + bh + 30
    lh = 158
    rrect(M, ly, tw_all, lh, 16, "#FCEDE9", z=2)
    rrect(M, ly, 12, lh, 6, CORAL, z=3)
    txt(M + 40, ly + 36, "COMO LER", monoB, 13, CORALd, z=5)
    txt(M + 40, ly + 68, "Turmas ~100 pontos acima do Brasil em cada área — e a distância MAIOR aparece nos itens de "
        "discriminação muito alta (A > 1,70).", outfit, 16.5, INK, z=5)
    txt(M + 40, ly + 100, "Na turma forte, a 'incoerência' quase nunca é chute em difícil: é DESLIZE em item fácil "
        "(~4–5 por aluno nas 4 provas).", outfit, 16.5, INK, z=5)
    txt(M + 40, ly + 136, "Alerta: erro ACIMA do Brasil em CH-H10 (ambas), CN-H6 (ambas) e LC-H28 (Roberto Freire) — prioridade 2026.",
        outfitB, 16.5, CORALd, z=5)

    assinatura(hp, ax, M, H - 40, extra=" · Censo Escolar 2025 (nomes) · alunos anônimos")
    return save(fig, "cei_painel_resumo")


if __name__ == "__main__":
    main()
