#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG (feed 1080x1350 + story 1080x1920) — "o mesmo 700 não vale o mesmo".
Percentis empíricos por área, ENEM 2025 P1 regular (presentes, nota válida):
dados_apoio/cdf_notas_enem2025_p1_regular.csv (gerado nesta sessão do RESULTADOS).
700: LC top 0,4% (~4/1000) · CH 1,1% (11) · CN 1,1% (11) · MT 10,4% (104).
"""
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

X.OUTDIR = str(D)

AREAS = [("Linguagens", "~4", "top 0,4%", False),
         ("Humanas", "11", "top 1,1%", False),
         ("Natureza", "11", "top 1,1%", False),
         ("Matemática", "104", "top 10,4%", True)]
# mini-tabela: nota -> top % por área (LC, CH, CN, MT)
TAB = [("600", "16,5%", "16,1%", "10,2%", "26,5%"),
       ("650", "3,4%", "5,1%", "3,5%", "17,5%"),
       ("750", "<0,1%", "0,1%", "0,2%", "5,5%")]


def build(W, H, nome):
    fig, ax, hp = new_slide(W, H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 72
    story = H > 1500
    y = 250 if story else 120

    logo(ax, W - M + 6, 200 if story else 108, zoom=0.085)
    txt(M, y, "MICRODADOS ENEM 2025 · 3,4 MILHÕES DE CANDIDATOS", monoB, 15, CORALd)
    y += 88 if story else 78
    txt(M, y, "O MESMO 700", outfitB, 64, INK)
    y += 74
    txt(M, y, "NÃO VALE O MESMO", outfitB, 64, CORAL)
    y += 68 if story else 62
    txt(M, y, "A nota compara você com quem fez a MESMA área —", outfit, 22.5, GRAY)
    y += 36
    txt(M, y, "e cada área tem uma régua diferente.", outfit, 22.5, GRAY)

    # ---- pergunta + cards ----
    y += (120 if story else 72)
    txt(M, y, "DE CADA 1.000 CANDIDATOS, QUANTOS CHEGAM A 700?", monoB, 16.5, INK)
    y += 40 if story else 34
    gap = 26
    cw = (W - 2 * M - 3 * gap) / 4
    ch = 280 if story else 218
    for i, (nome_a, num, top, destaque) in enumerate(AREAS):
        x = M + i * (cw + gap)
        shadow(x, y, cw, ch, 16)
        rrect(x, y, cw, ch, 16, CORAL if destaque else CARD, z=2)
        cor_num = "#FFFFFF" if destaque else INK
        cor_lab = "#FFE1D9" if destaque else GRAY
        txt(x + cw / 2, y + (60 if story else 52), nome_a.upper(), monoB, 13.5, cor_lab, ha="center", z=5)
        txt(x + cw / 2, y + (162 if story else 130), num, outfitB, 56, cor_num, ha="center", z=5)
        txt(x + cw / 2, y + (226 if story else 180), top, mono, 14.5, cor_lab, ha="center", z=5)
    y += ch + (80 if story else 42)

    # ---- leitura ----
    lh = 152 if story else 128
    rrect(M, y, W - 2 * M, lh, 16, "#FCEDE9", z=2)
    rrect(M, y, 10, lh, 5, CORAL, z=3)
    txt(M + 34, y + (56 if story else 44), "700 em Linguagens te coloca entre 4 em mil.", outfitB, 22, INK, z=5)
    txt(M + 34, y + (104 if story else 90), "Em Matemática, 104 chegam lá — porque a escala estica até 980.", outfit, 20, INK, z=5)
    y += lh + (86 if story else 44)

    # ---- mini-tabela ----
    txt(M, y, "E NAS OUTRAS NOTAS? (% que chega lá, por área)", monoB, 15, INK)
    y += 32 if story else 26
    rowh = 84 if story else 56
    tw_all = W - 2 * M
    cols = [0.16, 0.21, 0.21, 0.21, 0.21]
    heads = ["nota", "Linguagens", "Humanas", "Natureza", "Matemática"]
    shadow(M, y, tw_all, rowh * 4, 14)
    rrect(M, y, tw_all, rowh * 4, 14, CARD, z=2)
    cx = M
    for j, hd in enumerate(heads):
        txt(cx + tw_all * cols[j] / 2, y + rowh * 0.64, hd, monoB, 14,
            GRAY if j else INK, ha="center", z=5)
        cx += tw_all * cols[j]
    for i, linha in enumerate(TAB):
        yy = y + (i + 1) * rowh
        if i % 2 == 0:
            rrect(M, yy, tw_all, rowh, 0, "#F7F7F8", z=2.5)
        cx = M
        for j, v in enumerate(linha):
            eh_mt = (j == 4)
            txt(cx + tw_all * cols[j] / 2, yy + rowh * 0.64, v,
                outfitB, 19 if j else 20, CORALd if eh_mt else (INK if j == 0 else GRAY),
                ha="center", z=5)
            cx += tw_all * cols[j]
    y += rowh * 4

    # ---- rodapé (na story, acima da zona de UI do Instagram) ----
    fy = H - (220 if story else 108)
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP — 1ª aplicação regular, presentes com nota válida.",
        mono, 12, GRAY)
    fy = H - (160 if story else 52)
    xx = M
    for s, c in [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
        txt(xx, fy, s, outfitB, 17, c)
        xx += tw(s, outfitB, 17)
    txt(W - M, fy, "@xandaoxtri", monoB, 15, GRAY, ha="right")
    save(fig, nome)


build(1080, 1350, "post_percentil_700_feed")
build(1080, 1920, "post_percentil_700_story")
