#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa da newsletter LinkedIn (1280×720) — O ENEM inclui o aluno com necessidades especiais?"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import new_slide, logo, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1280, 720
VERDEd = "#1F8F3E"
F = json.loads((D.parent / "dados_inclusao.json").read_text())["funil_nacional"]


def make():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 60

    logo(ax, M + 100, 62, zoom=0.05)
    txt(W - M, 66, "CENSO ESCOLAR 2025 × ENEM 2025 · INEP/MEC", monoB, 11, GRAY, ha="right", va="center")

    ty = 150
    txt(M, ty, "O ENEM INCLUI O ALUNO COM", outfitB, 37, INK)
    txt(M, ty + 46, "NECESSIDADES ESPECIAIS?", outfitB, 37, CORAL)
    txt(M, ty + 92, "O que os microdados oficiais mostram — e o que eles deixam de mostrar.", outfit, 15.5, GRAY)

    # dois blocos-stat lado a lado
    by = ty + 130
    bw = (W - 2 * M - 28) / 2
    bh = 168
    # esquerda: matrícula (verde)
    rrect(M, by, bw, bh, 16, "#EAF7EE", z=3); rrect(M, by, 8, bh, 4, VERDEd, z=4)
    txt(M + 28, by + 40, "NA MATRÍCULA (CENSO)", monoB, 11, GRAY, z=5)
    txt(M + 28, by + 96, "294.089", outfitB, 46, VERDEd, z=5)
    txt(M + 28, by + 130, "na Educação Especial do EM · 99,4% em classe comum", mono, 11, INK, z=5)
    # direita: prova (coral)
    rx = M + bw + 28
    rrect(rx, by, bw, bh, 16, "#FCEDE9", z=3); rrect(rx, by, 8, bh, 4, CORALd, z=4)
    txt(rx + 28, by + 40, "NA PROVA (ENEM)", monoB, 11, GRAY, z=5)
    txt(rx + 28, by + 96, "22.500", outfitB, 46, CORALd, z=5)
    txt(rx + 28, by + 130, "com prova adaptada · a condição não é registrada", mono, 11, INK, z=5)

    # faixa de fecho
    fy2 = by + bh + 34
    txt(M, fy2, "O sistema inclui no acesso — mas é cego aos próprios dados.", outfitB, 19, INK)
    txt(M, fy2 + 30, "O primeiro passo da inclusão é ser contado.", outfit, 16, GRAY)

    # assinatura
    ay = H - 52
    txt(M, ay, "Transformamos ", outfitB, 14, INK); xx = M + tw("Transformamos ", outfitB, 14)
    txt(xx, ay, "dados", outfitB, 14, CYAN); xx += tw("dados", outfitB, 14)
    txt(xx, ay, " em ", outfitB, 14, INK); xx += tw(" em ", outfitB, 14)
    txt(xx, ay, "aprovações", outfitB, 14, CORAL); xx += tw("aprovações", outfitB, 14)
    txt(xx, ay, ".", outfitB, 14, INK)
    txt(W - M, ay, "Prof. Alexandre Emerson · @xandaoxtri", mono, 11.5, GRAY, ha="right")
    return save(fig, "capa_linkedin_inclusao")


if __name__ == "__main__":
    make()
