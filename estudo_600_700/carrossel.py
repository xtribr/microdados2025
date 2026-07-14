#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel IG — As questões que separam o 600 do 700 (ENEM 2025). Marca XTRI.
Capa + conceito (U-invertido) + 4 questões divisoras com print + fecho."""
import sys
from pathlib import Path
from PIL import Image
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)
D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64
VERDE = "#1E8449"; ROXO = "#6C3483"

# faixas do U-invertido (gap 700-600 por dificuldade TRI)
BANDS = [("Fácil\n(<560)", 11.2, "#9AA0A6"), ("560–640", 30.7, "#7FB3E0"),
         ("640–700", 31.4, CORAL), ("700–760", 16.3, "#7FB3E0"), ("Muito dif.\n(760+)", 6.3, "#9AA0A6")]
# questões divisoras: area, nome, cor, Q, hab, difTRI, a6, a7, assunto, crop
QST = [
    ("Linguagens", CYANd, 32, 29, 650, 14, 91, "gênero crônica (leitura)", "q032_LC.png"),
    ("C. Humanas", CORAL, 59, 26, 638, 25, 86, "energia × Amazônia", "q059_CH.png"),
    ("C. Natureza", VERDE, 127, 8, 612, 37, 98, "cinética química (enzima)", "q127_CN.png"),
    ("Matemática", ROXO, 157, 19, 624, 43, 84, "razão e proporção", "q157_MT.png"),
]


def foot(hp, idx, nota="Fonte: Microdados ENEM 2025 / INEP · caderno Azul, 1ª aplicação · acerto por faixa de nota TRI."):
    txt = hp["txt"]
    txt(M, H - 62, nota, mono, 9, GRAY)
    txt(W - M, H - 62, idx, monoB, 11, GRAY, ha="right")


def thumb(ax, crop, x0, y0, cw, chmax, accent):
    im = Image.open(D / "crops" / crop).convert("RGB")
    iw, ih = im.size; sc = cw / iw; dh = ih * sc
    if dh > chmax:
        im = im.crop((0, 0, iw, int(chmax / sc))); ch = chmax
    else:
        ch = dh
    ax.imshow(mpimg.pil_to_array(im), extent=(x0, x0 + cw, y0 + ch, y0), zorder=3, aspect="auto")
    ax.add_patch(Rectangle((x0, y0), cw, ch, fill=False, ec="#DADBDD", lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x0, y0), 7, ch, fc=accent, ec="none", zorder=5))
    return ch


# ---------- Card 1: capa ----------
def capa():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · TRI", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 232; S = 58
    txt(M, ty, "AS QUESTÕES QUE", outfitB, S, INK)
    txt(M, ty + 74, "SEPARAM O", outfitB, S, INK)
    txt(M + 6 + hp["tw"]("SEPARAM O ", outfitB, S), ty + 74, "600", outfitB, S, CYANd)
    txt(M, ty + 148, "DO", outfitB, S, INK)
    txt(M + 6 + hp["tw"]("DO ", outfitB, S), ty + 148, "700", outfitB, S, CORAL)
    txt(M, ty + 208, "No microdado do INEP, achamos exatamente quais", outfit, 21, GRAY)
    txt(M, ty + 238, "questões decidem se você fica no 600 ou chega no 700.", outfit, 21, GRAY)
    # destaque teaser
    py = ty + 300; hh = 244
    shadow(M, py, W - 2 * M, hh, 20); rrect(M, py, W - 2 * M, hh, 20, CARD, z=6); rrect(M, py, 11, hh, 5, CYANd, z=7)
    txt(M + 40, py + 52, "Spoiler: a Q32 de Linguagens", outfitB, 25, INK, z=8)
    nb = py + 150
    txt(M + 40, nb, "14%", outfitB, 60, GRAY, z=8)
    txt(M + 40 + hp["tw"]("14%  ", outfitB, 60), nb, "→", outfitB, 38, GRAY, z=8)
    txt(M + 40 + hp["tw"]("14%  →  ", outfitB, 60), nb, "91%", outfitB, 60, CORAL, z=8)
    txt(M + 40, py + 196, "acerto de quem tirou 600  →  de quem tirou 700", mono, 14, GRAY, z=8)
    txt(M, H - 150, "Deslize: as 4 áreas, com o print de cada questão.", outfit, 17, INK)
    foot(hp, "1/7")
    return save(fig, "c1_capa")


# ---------- Card 2: conceito (U-invertido) ----------
def conceito():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "O CONCEITO", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 170
    txt(M, ty, "NÃO SÃO AS MAIS DIFÍCEIS", outfitB, 40, INK)
    txt(M, ty + 46, "é a faixa do meio que decide", outfit, 24, CORALd)
    txt(M, ty + 92, "Gap de acerto entre quem tirou 700 e quem tirou 600, por", outfit, 16, GRAY)
    txt(M, ty + 116, "dificuldade da questão (média das 4 áreas):", outfit, 16, GRAY)
    # barras
    bx0 = M + 40; bw = (W - 2 * M - 80) / len(BANDS); base = 900; scale = 7.0
    for i, (lab, g, col) in enumerate(BANDS):
        x = bx0 + i * bw; bh = g * scale
        rrect(x + 14, base - bh, bw - 28, bh, 10, col, z=4)
        txt(x + bw / 2, base - bh - 16, f"{g:.0f}", outfitB, 26, col if col != "#9AA0A6" else GRAY, ha="center", z=5)
        for k, ln in enumerate(lab.split("\n")):
            txt(x + bw / 2, base + 30 + k * 22, ln, mono, 12.5, GRAY, ha="center", z=5)
    txt(bx0, base + 96, "pontos percentuais de diferença", mono, 12, GRAY)
    # explicação
    py = base + 150
    rrect(M, py, W - 2 * M, 220, 18, "#FEF3F0", z=2)
    txt(M + 36, py + 56, "Nas fáceis, quase todo mundo acerta. Nas impossíveis,", outfit, 19, INK, z=5)
    txt(M + 36, py + 88, "quase todo mundo erra. A diferença entre 600 e 700 se", outfit, 19, INK, z=5)
    txt(M + 36, py + 120, "decide nas questões de dificuldade MÉDIA-ALTA — as que", outfit, 19, INK, z=5)
    txt(M + 36, py + 152, "o 700 acerta e o 600 ainda erra.", outfitB, 19, CORALd, z=5)
    foot(hp, "2/7", "Fonte: Microdados ENEM 2025 / INEP · caderno Azul · gap = acerto(nota 690–710) − acerto(nota 590–610).")
    return save(fig, "c2_conceito")


# ---------- Cards 3-6: questão por área ----------
def card_questao(i, area, cor, q, hab, dif, a6, a7, assunto, crop, idx):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, f"DIVISORA · {area.upper()}", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 168
    txt(M, ty, area.upper(), outfitB, 40, cor)
    txt(M, ty + 42, f"A questão que separa 600 de 700", outfitB, 25, INK)
    txt(M, ty + 76, f"Q{q} · habilidade {hab} · dificuldade TRI {dif} · {assunto}", mono, 13, GRAY)
    # print
    gy = ty + 108
    ch = thumb(ax, crop, M, gy, W - 2 * M, 560, cor)
    # stat card
    py = gy + ch + 22
    hh = H - 96 - py
    rrect(M, py, W - 2 * M, hh, 18, CARD, z=6); rrect(M, py, 11, hh, 5, cor, z=7)
    cy = py + hh / 2
    txt(M + 40, cy - 6, f"{a6}%", outfitB, 74, GRAY, va="center", z=8)
    aw = hp["tw"](f"{a6}% ", outfitB, 74)
    txt(M + 40 + aw, cy - 6, "→", outfitB, 46, GRAY, va="center", z=8)
    txt(M + 40 + aw + hp["tw"]("→ ", outfitB, 46), cy - 6, f"{a7}%", outfitB, 74, cor, va="center", z=8)
    rx = M + 40 + aw + hp["tw"]("→ ", outfitB, 46) + hp["tw"](f"{a7}%  ", outfitB, 74)
    txt(rx, cy - 22, "acertaram", outfit, 17, INK, va="center", z=8)
    txt(rx, cy + 4, "quem tirou 600", mono, 13, GRAY, va="center", z=8)
    txt(rx, cy + 26, "quem tirou 700", monoB, 13, cor, va="center", z=8)
    foot(hp, idx)
    return save(fig, f"c{i}_{area.split()[-1].lower()}")


# ---------- Card 7: fecho ----------
def fecho():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "O BIZU", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 244
    txt(M, ty, "ONDE SUA NOTA", outfitB, 54, INK)
    txt(M, ty + 74, "É DECIDIDA", outfitB, 54, CORAL)
    txt(M, ty + 146, "Não adianta só brigar com as impossíveis: nelas, o 700", outfit, 20, GRAY)
    txt(M, ty + 176, "também erra. Sua nota sobe quando você domina a FAIXA", outfit, 20, GRAY)
    txt(M, ty + 206, "DO MEIO — as questões que a maioria dos 600 ainda erra.", outfit, 20, GRAY)
    py = ty + 266; hh = 250
    shadow(M, py, W - 2 * M, hh, 20); rrect(M, py, W - 2 * M, hh, 20, CARD, z=6); rrect(M, py, 11, hh, 5, CORAL, z=7)
    txt(M + 40, py + 60, "Na prática", outfitB, 24, INK, z=8)
    txt(M + 40, py + 104, "Revise as habilidades de dificuldade média-alta", outfit, 19, INK, z=8)
    txt(M + 40, py + 136, "(TRI ~560–700). É onde o 600 vira 700.", outfit, 19, INK, z=8)
    txt(M + 40, py + 190, "Simule sua nota real por acertos:", outfit, 17, GRAY, z=8)
    txt(M + 40, py + 218, "xtri.online", monoB, 19, CYANd, z=8)
    # assinatura de marca
    txt(M, H - 150, "Salva pra revisar na reta final e marca quem tá no 600 tentando o 700.", outfit, 16, INK)
    foot(hp, "7/7")
    return save(fig, "c7_fecho")


if __name__ == "__main__":
    capa(); conceito()
    for i, (area, cor, q, hab, dif, a6, a7, assunto, crop) in enumerate(QST, start=3):
        card_questao(i, area, cor, q, hab, dif, a6, a7, assunto, crop, f"{i}/7")
    fecho()
