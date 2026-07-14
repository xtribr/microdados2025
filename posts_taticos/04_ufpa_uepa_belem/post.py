#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quantos acertos pra UFPA e UEPA (Belém)? — carrossel 2 cards (feed 1080x1350).
MODELO ≠ SISU: nota = média SIMPLES das 5 do ENEM + 10% bônus Região Norte.
Card 1 = SEM bônus (brutal). Card 2 = COM bônus (o 10% viabiliza). Redação assumida = 900.
Cortes reais (listões definitivos 30/01/2026): UFPA Med 871,40 · UEPA Med 872,76 · UFPA Direito 757,82."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64
J = json.loads((D / "dados.json").read_text())
C = J["cursos"]
RED = int(J["red"])


def vir(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def matriz(hp, cen, ry):
    """desenha a matriz dos 3 cursos para o cenário cen ('sem_bonus'|'com_bonus')."""
    txt = hp["txt"]; rrect = hp["rrect"]
    cols = ["MAT", "NAT", "HUM", "LING"]; keys = ["MT", "CN", "CH", "LC"]
    col_x = [W - M - 300 + j * 78 for j in range(4)]
    txt(M + 20, ry - 20, "CURSO (pontuação de corte)", monoB, 12, GRAY)
    for j, c in enumerate(cols):
        cor = CORALd if c == "MAT" else (CYANd if c == "LING" else GRAY)
        txt(col_x[j], ry - 20, c, monoB, 12.5, cor, ha="center")
    rh = 118
    for i, x in enumerate(C):
        yy = ry + i * (rh + 14)
        med = x["curso"] == "Medicina"
        d = x["cenarios"][cen]
        rrect(M, yy, W - 2 * M, rh, 15, "#FFFFFF", z=3)
        rrect(M, yy, 8, rh, 4, CORAL if med else CYANd, z=4)
        txt(M + 30, yy + 40, f"{x['uni']} · {x['curso']}", outfitB, 22, INK, z=5)
        txt(M + 30, yy + 68, x["campus"], mono, 11.5, GRAY, z=5)
        txt(M + 30, yy + 94, f"corte {vir(x['pontuacao'])}", mono, 11.5, CORALd if med else CYANd, z=5)
        for j, k in enumerate(keys):
            ac = d["acertos"][k]
            val = str(ac) if ac is not None else "45+"
            cor = "#C7CBD0" if ac is None else (CORALd if k == "MT" else (CYANd if k == "LC" else INK))
            sz = 24 if ac is None else 30
            txt(col_x[j], yy + rh / 2 + 8, val, outfitB, sz, cor, ha="center", va="center", z=5)
    return ry + len(C) * (rh + 14)


# ---------- card 1: SEM bônus ----------
def card1():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "UFPA & UEPA · BELÉM · SEM O BÔNUS", monoB, 11, GRAY, ha="right", va="center")

    ty = 176
    txt(M, ty, "SEM O BÔNUS DO NORTE,", outfitB, 40, INK)
    txt(M, ty + 52, "O ALVO É QUASE IMPOSSÍVEL", outfitB, 34, CORAL)
    txt(M, ty + 98, "Aqui NÃO é SISU: a nota é a média SIMPLES das 5 do ENEM. Supondo", outfit, 15, GRAY)
    txt(M, ty + 123, "redação 900, os acertos nas objetivas pra bater o corte — sem bônus:", outfit, 15, GRAY)

    end = matriz(hp, "sem_bonus", ty + 196)

    py = end + 16
    hh = 322
    shadow(M, py, W - 2 * M, hh, 16); rrect(M, py, W - 2 * M, hh, 16, "#FCEDE9", z=3); rrect(M, py, 10, hh, 5, CORALd, z=4)
    txt(M + 32, py + 50, "Medicina exigiria gabaritar Natureza, Humanas E Linguagens", outfitB, 17.5, INK, z=5)
    txt(M + 32, py + 80, "(os 45+) e ainda 38 de Matemática. Praticamente inviável.", outfitB, 17.5, INK, z=5)
    ax.plot([M + 32, W - M - 32], [py + 122, py + 122], color="#F3C9BC", lw=1, zorder=5)
    txt(M + 32, py + 170, "Na prática, ninguém entra em Medicina aqui SEM o bônus:", outfitB, 20, CORALd, z=5)
    txt(M + 32, py + 210, "a pontuação de corte (871) já foi construída por quem tem os", outfit, 15.5, INK, z=5)
    txt(M + 32, py + 238, "10% da Região Norte. Sem eles, você compete em desvantagem.", outfit, 15.5, INK, z=5)
    txt(M + 32, py + hh - 30, "vira o card pra ver o que muda COM o bônus →", mono, 12.5, CORALd, z=5)
    txt(M, H - 58, "45+ = nem gabaritando pela mediana · redação 900 assumida", mono, 9.5, GRAY)
    txt(W - M, H - 58, "1/2", monoB, 11, GRAY, ha="right")
    return save(fig, "c1_sem_bonus")


# ---------- card 2: COM bônus ----------
def card2():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "UFPA & UEPA · COM O BÔNUS 10%", monoB, 11, GRAY, ha="right", va="center")

    ty = 176
    txt(M, ty, "COM O BÔNUS DE 10%,", outfitB, 40, INK)
    txt(M, ty + 52, "VIRA REALIDADE", outfitB, 40, "#1F8F3E")
    txt(M, ty + 98, "O mesmo corte, com o bônus da Região Norte (quem fez o EM aqui).", outfit, 15, GRAY)
    txt(M, ty + 123, "Ele multiplica sua média por 1,10. Redação 900:", outfit, 15, GRAY)

    end = matriz(hp, "com_bonus", ty + 196)

    py = end + 10
    hh = H - 150 - py
    shadow(M, py, W - 2 * M, hh, 16); rrect(M, py, W - 2 * M, hh, 16, CARD, z=3); rrect(M, py, 10, hh, 5, "#1F8F3E", z=4)
    txt(M + 32, py + 44, "O bônus derrubou Medicina de 'gabaritar tudo' para 30/38/42/45.", outfitB, 16.5, INK, z=5)
    txt(M + 32, py + 76, "E Direito fica bem acessível: 20 de Mat, 25 de Nat, 30 Hum, 36 Ling.", outfit, 14.5, INK, z=5)
    txt(M + 32, py + 112, "Lembre: como é média simples, a redação vale igual a cada área —", outfit, 14.5, INK, z=5)
    txt(M + 32, py + 138, "um 900 na redação puxa toda a sua média pra cima.", outfit, 14.5, INK, z=5)
    txt(M + 32, py + hh - 26, "Quer a conta do TEU curso e turno? xtrisisu.com", outfitB, 15.5, CYANd, z=5)

    fy = H - 108
    txt(M, fy, "Fontes: listões definitivos 30/01/2026 (CEPS/UFPA e PROSEL/UEPA) · acertos: mediana ENEM 2025 / INEP · bônus ÷1,10 (editais)",
        mono, 8.6, GRAY)
    ay = fy + 30
    txt(M, ay, "Transformamos ", outfitB, 15, INK); xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, H - 58, "@xandaoxtri · xtrisisu.com   2/2", mono, 11, GRAY, ha="right")
    return save(fig, "c2_com_bonus")


if __name__ == "__main__":
    card1(); card2()
