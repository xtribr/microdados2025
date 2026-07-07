#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Card-inventário: as 6 questões anuladas do ENEM 2025 — motivo oficial + o que o dado mostrou."""
import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H)

ROWS = [
    ("CH", "2ª aplic.", "Bis < 0,01", "TRI",
     "Gabarito D não lidera em NENHUM grupo — os fortes marcam E (51%). Correlação ~zero."),
    ("CN", "Regular P1", "Problema de convergência", "TRI",
     "Curva do gabarito em U: cai a 18% no meio da escala e só dispara no topo (69%)."),
    ("MT", "Regular P1", "Problema de convergência", "TRI",
     "Os fortes convergem em D (73%); o gabarito oficial A CAI com a nota (15% → 8%)."),
    ("CN", "Regular P1", "Previamente exposto", "VAZAMENTO",
     "Comportamento saudável; piso dos fracos 27%, no nível do acaso — sem vantagem em massa."),
    ("CN", "Regular P1", "Previamente exposto", "VAZAMENTO",
     "Item difícil e sadio: fortes 83%, piso 9% — ABAIXO do acaso. Anulação preventiva."),
    ("MT", "Regular P1", "Previamente exposto", "VAZAMENTO",
     "Saudável; piso 23%, no nível do acaso. O gabarito foi apagado (X) pelo INEP."),
]
TIPO_COL = {"TRI": CYANd, "VAZAMENTO": CORALd}
AREA_COL = {"CH": "#E84855", "CN": "#2EC4B6", "MT": "#3A86FF"}


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    txt(M, 76, "As 6 questões que ", outfitB, 32, INK)
    txt(M + tw("As 6 questões que ", outfitB, 32), 76, "morreram", outfitB, 32, CORAL)
    txt(M + tw("As 6 questões que morreram", outfitB, 32), 76, " no ENEM 2025", outfitB, 32, INK)
    txt(M, 114, "Motivo oficial (TX_MOTIVO_ABAN dos microdados) + o que a autópsia das marcações mostrou. "
                "Item anulado não entra na nota de ninguém.", outfit, 15, GRAY)
    logo(ax, W - M - 4, 84, zoom=0.072)

    top = 168
    rowh = 118
    for i, (area, aplic, motivo, tipo, veredito) in enumerate(ROWS):
        ry = top + i * rowh
        ch = rowh - 14
        shadow(M, ry, W - 2 * M, ch, 14)
        rrect(M, ry, W - 2 * M, ch, 14, CARD, z=2)
        rrect(M, ry, 10, ch, 5, TIPO_COL[tipo], z=3)
        # badge área
        rrect(M + 28, ry + ch / 2 - 26, 64, 52, 12, AREA_COL[area], z=3)
        txt(M + 60, ry + ch / 2 + 1, area, outfitB, 20, "#FFFFFF", ha="center", va="center", z=5)
        # aplicação + motivo
        txt(M + 118, ry + 34, aplic.upper(), mono, 11, GRAY, z=5)
        txt(M + 118, ry + 66, motivo, outfitB, 19, INK, z=5)
        # selo do tipo
        selo = "ANULADA PELA TRI" if tipo == "TRI" else "ANULADA POR VAZAMENTO"
        sw = tw(selo, monoB, 11.5) + 28
        rrect(M + 118, ry + 76, sw, 26, 8, "#EAF4FB" if tipo == "TRI" else "#FCEDE9", z=3)
        txt(M + 132, ry + 93, selo, monoB, 11.5, TIPO_COL[tipo], z=5)
        # veredito
        vx = M + 520
        txt(vx, ry + 34, "O QUE O DADO MOSTROU", mono, 10.5, GRAY, z=5)
        txt(vx, ry + 66, veredito, outfit, 16.5, INK, z=5)

    txt(M, H - 66, "Autópsia: % de marcação de cada alternativa por faixa de nota (Regular P1: ~3,18 mi respostas/item; CH: 2ª aplicação, n=309).",
        mono, 10.5, GRAY)
    assinatura(hp, ax, M, H - 40, extra=" · motivos oficiais do ITENS_PROVA")
    return save(fig, "g15_inventario_anulados")


if __name__ == "__main__":
    main()
