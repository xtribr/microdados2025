#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACERTA ESSA? #01 — quiz IG (2 cards, feed 1080x1350). Pergunta + resposta.
Dado real: ENEM 2025, Q111 CN (biodigestão), distribuição A-E de 792.190 presentes."""
import sys
from pathlib import Path
import matplotlib.image as mpimg

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64
LETRAS = [("A", 45.9, False), ("B", 16.5, True), ("C", 23.5, False), ("D", 6.8, False), ("E", 7.4, False)]


def footer(hp, txt, n, tag):
    t = hp["txt"]
    t(M, H - 58, "Fonte: Microdados ENEM 2025 / INEP · Q111 CN · 792.190 presentes", mono, 9.5, GRAY)
    t(W - M, H - 58, tag, monoB, 11, GRAY, ha="right")


# ---------- card 1: a pergunta ----------
def card1():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ACERTA ESSA? · #01 · NATUREZA", monoB, 12, GRAY, ha="right", va="center")

    ty = 178
    txt(M, ty, "SÓ 16% DO BRASIL", outfitB, 44, INK)
    txt(M, ty + 54, "ACERTOU ESSA. E VOCÊ?", outfitB, 44, CORAL)

    # print da questão
    img = mpimg.imread(str(D / "q111.png"))
    ih, iw = img.shape[0], img.shape[1]
    card_w = W - 2 * M
    y0 = ty + 96
    card_h = H - y0 - 210
    scale = min(card_w / iw, card_h / ih)
    dw, dh = iw * scale, ih * scale
    x0 = M + (card_w - dw) / 2
    ax.imshow(img, extent=(x0, x0 + dw, y0 + dh, y0), zorder=3)
    ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
        (x0, y0), dw, dh, fill=False, ec="#D9D9D9", lw=1.2, zorder=4))

    # CTA band
    by = y0 + dh + 22
    hh = H - 96 - by
    shadow(M, by, W - 2 * M, hh, 18); rrect(M, by, W - 2 * M, hh, 18, CORAL, z=3)
    txt(W / 2, by + 46, "COMENTA A LETRA QUE VOCÊ MARCARIA", outfitB, 21, "#FFFFFF", ha="center", z=5)
    txt(W / 2, by + 80, "sem pesquisar! a resposta está no próximo card →", mono, 13, "#FFE3DB", ha="center", z=5)

    footer(hp, txt, 1, "1/2")
    return save(fig, "c1_pergunta")


# ---------- card 2: a resposta ----------
def card2():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ACERTA ESSA? · #01 · RESPOSTA", monoB, 12, GRAY, ha="right", va="center")

    ty = 178
    txt(M, ty, "A RESPOSTA É", outfitB, 40, INK)
    txt(M, ty + 50, "A LETRA B", outfitB, 40, CYANd)
    txt(M, ty + 96, "eutrofização dos corpos d'água — e só 16,5% acertaram.", outfit, 16.5, GRAY)

    # barras A-E
    gy0 = ty + 150
    gh = 420
    base = gy0 + gh
    n = len(LETRAS)
    gw = (W - 2 * M) / n
    bw = gw * 0.58
    maxv = max(v for _, v, _ in LETRAS)
    scale = gh / (maxv * 1.2)
    for letra, pct, gab in LETRAS:
        i = "ABCDE".index(letra)
        gx = M + i * gw + (gw - bw) / 2
        h = pct * scale
        campea = letra == "A"
        cor = CYANd if gab else (CORAL if campea else "#C7CBD0")
        rrect(gx, base - h, bw, h, 9, cor, z=3)
        txt(gx + bw / 2, base - h - 16, f"{pct}%".replace(".", ","), outfitB, 20,
            CYANd if gab else (CORALd if campea else "#6B7076"), ha="center", z=5)
        txt(gx + bw / 2, base + 30, letra, outfitB, 22, INK, ha="center", z=5)
        rot = "certa" if gab else ("pegadinha" if campea else "")
        if rot:
            txt(gx + bw / 2, base + 58, rot, mono, 11, GRAY, ha="center", z=5)

    # painel explicação
    py = base + 96
    hh = H - 96 - py
    shadow(M, py, W - 2 * M, hh, 18); rrect(M, py, W - 2 * M, hh, 18, CARD, z=3); rrect(M, py, 10, hh, 5, CORALd, z=4)
    txt(M + 34, py + 48, "46% caiu na A — quase 3× mais que o gabarito.", outfitB, 19, INK, z=5)
    txt(M + 34, py + 84, "A pegadinha: confundir bioacumulação de toxinas (A)", outfit, 15.5, INK, z=5)
    txt(M + 34, py + 112, "com eutrofização por excesso de nutrientes (B). Soam", outfit, 15.5, INK, z=5)
    txt(M + 34, py + 140, "parecido — mas são processos diferentes.", outfit, 15.5, INK, z=5)
    ax.plot([M + 34, W - M - 34], [py + 186, py + 186], color="#E6E7E9", lw=1, zorder=5)
    txt(M + 34, py + 232, "BIZU:", monoB, 14, CORALd, z=5)
    txt(M + 34 + tw("BIZU:  ", monoB, 14), py + 232, "leia o PROCESSO que a alternativa", outfitB, 18, INK, z=5)
    txt(M + 34, py + 264, "descreve — não se ela só 'soa' ambiental.", outfitB, 18, INK, z=5)
    txt(M + 34, py + 312, "É assim que o distrator pega quem estudou 'por cima'.", outfit, 14.5, GRAY, z=5)
    txt(M + 34, py + hh - 26, "acertou? manda pra quem errou. série ACERTA ESSA toda semana.", mono, 12, GRAY, z=5)

    footer(hp, txt, 2, "2/2")
    return save(fig, "c2_resposta")


if __name__ == "__main__":
    card1(); card2()
