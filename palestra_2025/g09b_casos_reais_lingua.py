#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Casos REAIS: aluno de inglês × aluno de espanhol com o MESMO desempenho.
Comparação casada por (nº total de acertos LC, nº de acertos no bloco de língua = 3/5).
Valores = mediana de alunos reais com esse exato desempenho (representativo, não inventado).
Fecha com o paradoxo da seleção. Dado: lingua_casos.json + lingua_curve.json.
"""
import json

import xtri_deck as X
from xtri_deck import new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H

CAS = json.load(open(f"{X.BASE}/palestra_2025/lingua_casos.json", encoding="utf-8"))
CUR = json.load(open(f"{X.BASE}/palestra_2025/lingua_curve.json", encoding="utf-8"))
ING = "#E8431F"
ESP = "#1597D8"


def caso(ac, ling=3):
    for p in CAS:
        if p["acertos_total"] == ac and p["acertos_lingua"] == ling:
            return p
    return None


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 70
    txt(M, 78, "Caso real: mesmo desempenho, ", outfitB, 32, INK)
    txt(M + tw("Caso real: mesmo desempenho, ", outfitB, 32), 78, "o de espanhol tira mais",
        outfitB, 32, ESP)
    txt(M, 116, "Alunos reais com o MESMO nº de acertos em Linguagens e o mesmo desempenho no bloco de "
                "língua (3 de 5). A única diferença é o idioma escolhido.", outfit, 15, GRAY)
    logo(ax, W - M - 8, 84, zoom=0.075)

    niveis = [25, 30, 35]
    cy = 165
    ch = 520
    cw = W - 2 * M
    shadow(M, cy, cw, ch, 24)
    rrect(M, cy, cw, ch, 24, CARD, z=2)
    # cabeçalhos de coluna
    colx_ac = M + 130
    colx_ing = M + 480
    colx_esp = M + 830
    colx_dif = M + cw - 230
    txt(colx_ac, cy + 56, "DESEMPENHO", mono, 13, GRAY, ha="center")
    txt(colx_ing, cy + 56, "ALUNO — INGLÊS", monoB, 13, ING, ha="center")
    txt(colx_esp, cy + 56, "ALUNO — ESPANHOL", monoB, 13, ESP, ha="center")
    txt(colx_dif, cy + 56, "DIFERENÇA", mono, 13, GRAY, ha="center")

    rowh = 140
    y0 = cy + 100
    for i, ac in enumerate(niveis):
        p = caso(ac)
        yy = y0 + i * rowh
        # desempenho
        txt(colx_ac, yy + 52, f"{ac} acertos", outfitB, 26, INK, ha="center")
        txt(colx_ac, yy + 84, "(3/5 no bloco de língua)", mono, 11.5, GRAY, ha="center")
        # inglês
        txt(colx_ing, yy + 60, f"{str(p['ingles_nota']).replace('.', ',')}", outfitB, 40, ING, ha="center")
        # espanhol
        txt(colx_esp, yy + 60, f"{str(p['espanhol_nota']).replace('.', ',')}", outfitB, 40, ESP, ha="center")
        # diferença
        dif = p["dif"]
        rrect(colx_dif - 105, yy + 22, 210, 60, 16, "#EAF4FB", z=3)
        txt(colx_dif, yy + 62, f"+{str(dif).replace('.', ',')}", outfitB, 30, ESP, ha="center")
        txt(colx_dif, yy + 92, "pontos pro espanhol", mono, 11, GRAY, ha="center")
        if i < len(niveis) - 1:
            ax.plot([M + 34, M + cw - 34], [yy + rowh - 18, yy + rowh - 18], color="#EDEEEF", lw=1.2, zorder=3)

    # paradoxo da seleção
    py = cy + ch + 44
    ph = 180
    rrect(M, py, cw, ph, 20, "#FCEDE9", z=2)
    txt(M + 34, py + 44, "MAS A MÉDIA GERAL DO INGLÊS É MAIOR — POR QUÊ?", monoB, 14, CORALd)
    ig = CUR["media_geral"]["Inglês"]; es = CUR["media_geral"]["Espanhol"]
    sh_i = str(CUR["share"]["Inglês"]).replace(".", ",")
    sh_e = str(CUR["share"]["Espanhol"]).replace(".", ",")
    txt(M + 34, py + 88, f"Inglês média {str(ig).replace('.', ',')}  ×  Espanhol média {str(es).replace('.', ',')}.  "
        f"O espanhol rende mais por acerto, mas o inglês é escolhido por quem chega com mais acertos",
        outfit, 16, INK)
    txt(M + 34, py + 122, f"({sh_i}% fazem inglês, {sh_e}% espanhol). A vantagem do inglês é SELEÇÃO de quem faz — não vantagem da prova.",
        outfit, 16, INK)

    assinatura(hp, ax, M, H - 44, extra=" · Regular P1 · mediana de alunos reais por desempenho")
    return save(fig, "g09b_casos_reais_lingua")


if __name__ == "__main__":
    main()
