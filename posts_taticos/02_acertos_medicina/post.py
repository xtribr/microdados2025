#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quantos acertos pra Medicina? — carrossel 2 cards (feed 1080x1350).
Card 1: notas de corte REAIS (SISU 2026 = ENEM 2025), ampla concorrência.
Card 2: tradução em acertos por área (modelo com assunções rotuladas).
Fontes: SISU 2026 pesos+cortes (projeto MIRT) · acertos→nota mediana ENEM 2025 / INEP."""
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
J = json.loads((D / "sisu_medicina.json").read_text())
RED = int(J["red_assumida"])
U = {x["sigla"] + "|" + x["city"]: x for x in J["universidades"]}
# escolhe 6 concorridas (uma linha por universidade principal)
def pick(sig, city):
    return next(x for x in J["universidades"] if x["sigla"] == sig and x["city"] == city)
TAB = [pick("UFMG", "Belo Horizonte"), pick("UFC", "Fortaleza"), pick("UFPE", "Recife"),
       pick("UFPB", "João Pessoa"), pick("UFMA", "São Luís"), pick("UFRN", "Natal")]
ANCHOR = pick("UFRN", "Natal")


def vir(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def footer(hp, n, tag):
    t = hp["txt"]
    t(M, H - 58, "Fontes: SISU 2026 (notas do ENEM 2025), cortes e pesos oficiais · acertos→nota: Microdados ENEM 2025 / INEP",
      mono, 9, GRAY)
    t(W - M, H - 58, tag, monoB, 11, GRAY, ha="right")


# ---------- card 1: cortes reais ----------
def card1():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "MEDICINA · SISU 2026 · AMPLA CONCORRÊNCIA", monoB, 11, GRAY, ha="right", va="center")

    ty = 182
    txt(M, ty, "A NOTA DE CORTE REAL", outfitB, 44, INK)
    txt(M, ty + 54, "DE MEDICINA", outfitB, 44, CORAL)
    txt(M, ty + 100, "Cortes oficiais do SISU 2026 (feito com as notas do ENEM 2025),", outfit, 16, GRAY)
    txt(M, ty + 126, "ampla concorrência, nas federais mais concorridas:", outfit, 16, GRAY)

    ry = ty + 176
    rh = 96
    for i, x in enumerate(TAB):
        yy = ry + i * (rh + 12)
        cor = CORAL if x["sigla"] == "UFRN" else "#C7CBD0"
        rrect(M, yy, W - 2 * M, rh, 15, "#FFFFFF", z=3)
        rrect(M, yy, 8, rh, 4, cor, z=4)
        txt(M + 32, yy + 40, f"{x['sigla']} · Medicina", outfitB, 21, INK, z=5)
        txt(M + 32, yy + 68, f"{x['city']}/{x['uf']}", mono, 12, GRAY, z=5)
        txt(W - M - 30, yy + rh / 2 + 8, vir(x["corte"]), outfitB, 34, CORALd if x["sigla"] == "UFRN" else INK,
            ha="right", va="center", z=5)

    py = ry + len(TAB) * (rh + 12) + 8
    hh = H - 150 - py
    rrect(M, py, W - 2 * M, hh, 16, "#EAF4FB", z=3); rrect(M, py, 10, hh, 5, CYANd, z=4)
    txt(M + 32, py + 44, "O corte é a MÉDIA PONDERADA das 5 notas — cada curso", outfit, 15.5, INK, z=5)
    txt(M + 32, py + 72, "usa pesos diferentes. E a UECE nem entra aqui: Medicina", outfit, 15.5, INK, z=5)
    txt(M + 32, py + 100, "na UECE é por vestibular próprio, não pelo SISU.", outfit, 15.5, INK, z=5)
    txt(M + 32, py + hh - 24, "nos próximos cards: quantos ACERTOS isso significa →", mono, 12, CYANd, z=5)
    footer(hp, 1, "1/3")
    return save(fig, "c1_cortes")


# ---------- card 2: traduzindo em acertos ----------
def card2():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "MEDICINA · TRADUZINDO EM ACERTOS", monoB, 11, GRAY, ha="right", va="center")

    ty = 182
    txt(M, ty, "QUANTOS ACERTOS", outfitB, 44, INK)
    txt(M, ty + 54, "PRA MEDICINA?", outfitB, 44, CORAL)
    txt(M, ty + 100, f"Ex.: UFRN (corte {vir(ANCHOR['corte'])}). Num desempenho equilibrado e", outfit, 16, GRAY)
    txt(M, ty + 126, f"redação {RED}, você precisa acertar (de 45 questões) — pela mediana:", outfit, 16, GRAY)

    areas = [("MATEMÁTICA", "MT", CORAL), ("C. NATUREZA", "CN", "#8C9298"),
             ("C. HUMANAS", "CH", "#8C9298"), ("LINGUAGENS", "LC", CYANd)]
    ry = ty + 176
    rh = 92
    for i, (nome, key, cor) in enumerate(areas):
        yy = ry + i * (rh + 12)
        ac = ANCHOR["acertos"][key]
        rrect(M, yy, W - 2 * M, rh, 15, "#FFFFFF", z=3); rrect(M, yy, 8, rh, 4, cor, z=4)
        txt(M + 32, yy + 40, nome, outfitB, 22, INK, z=5)
        rot = "onde você tem MAIS folga" if key == "MT" else ("o GARGALO: quase a prova toda" if key == "LC" else "")
        if rot:
            txt(M + 32, yy + 68, rot, mono, 12, cor, z=5)
        if ac is not None:
            txt(W - M - 30, yy + rh / 2 + 8, str(ac), outfitB, 40, INK, ha="right", va="center", z=5)
            txt(W - M - 30 - tw(str(ac), outfitB, 40) - 14, yy + rh / 2 + 8, "acertos", mono, 12, GRAY, ha="right", va="center", z=5)
        else:
            txt(W - M - 30, yy + rh / 2, "45", outfitB, 30, GRAY, ha="right", va="center", z=5)
            txt(W - M - 30, yy + rh / 2 + 28, "e nem isso basta", mono, 10.5, CORALd, ha="right", va="center", z=5)

    py = ry + len(areas) * (rh + 12) + 8
    hh = H - 150 - py
    shadow(M, py, W - 2 * M, hh, 16); rrect(M, py, W - 2 * M, hh, 16, CARD, z=3); rrect(M, py, 10, hh, 5, CORALd, z=4)
    txt(M + 32, py + 48, "Linguagens é o gargalo de Medicina — e Matemática, a folga.", outfitB, 18, INK, z=5)
    txt(M + 32, py + 84, "E o peso importa: a UFRN pesa Natureza 3× e Matemática 1×.", outfit, 15, INK, z=5)
    txt(M + 32, py + 112, "Lá, cada acerto de Bio/Química vale muito mais que um de Mat.", outfit, 15, INK, z=5)
    ax.plot([M + 32, W - M - 32], [py + 156, py + 156], color="#E6E7E9", lw=1, zorder=5)
    txt(M + 32, py + 204, "A conta muda por curso e universidade.", outfitB, 19, CORALd, z=5)
    txt(M + 32, py + 236, "Quer a SUA? Simula teu desempenho e curso", outfit, 15.5, INK, z=5)
    txt(M + 32, py + 264, "no xtrisisu.com — o simulador do XTRI.", outfit, 15.5, INK, z=5)
    txt(M + 32, py + hh - 24, f"estimativa: redação {RED}, desempenho equilibrado; a nota de cada acerto varia por item", mono, 10.5, GRAY, z=5)
    footer(hp, 2, "2/3")
    return save(fig, "c2_acertos")


# ---------- card 3: matriz de acertos por UF ----------
def card3():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "MEDICINA · ACERTOS POR UNIVERSIDADE", monoB, 11, GRAY, ha="right", va="center")

    ty = 182
    txt(M, ty, "OS ACERTOS DE CADA", outfitB, 42, INK)
    txt(M, ty + 58, "UNIVERSIDADE", outfitB, 42, CORAL)
    txt(M, ty + 108, "Simulado pelo ENEM 2025: acertos (de 45) por área pra bater o", outfit, 15.5, GRAY)
    txt(M, ty + 134, "corte de ampla concorrência — redação 900, desempenho equilibrado.", outfit, 15.5, GRAY)

    # cabeçalho de colunas
    cols = ["MAT", "NAT", "HUM", "LING"]
    keys = ["MT", "CN", "CH", "LC"]
    x_uf = M + 20
    col_x = [W - M - 300 + j * 78 for j in range(4)]
    hy = ty + 168
    txt(x_uf, hy, "UNIVERSIDADE (corte)", monoB, 12, GRAY)
    for j, c in enumerate(cols):
        cor = CORALd if c == "MAT" else (CYANd if c == "LING" else GRAY)
        txt(col_x[j], hy, c, monoB, 12.5, cor, ha="center")

    ry = hy + 20
    rh = 96
    for i, x in enumerate(TAB):
        yy = ry + i * (rh + 10)
        destaque = x["sigla"] == "UFRN"
        rrect(M, yy, W - 2 * M, rh, 14, "#FFFFFF", z=3)
        rrect(M, yy, 8, rh, 4, CORAL if destaque else "#C7CBD0", z=4)
        txt(M + 30, yy + 40, x["sigla"], outfitB, 22, INK, z=5)
        txt(M + 30, yy + 66, f"{x['city']}/{x['uf']} · corte {vir(x['corte'])}", mono, 11, GRAY, z=5)
        for j, k in enumerate(keys):
            ac = x["acertos"][k]
            val = str(ac) if ac is not None else "45+"
            cor = CORALd if k == "MT" else (CYANd if k == "LC" else INK)
            txt(col_x[j], yy + rh / 2 + 8, val, outfitB, 26, cor, ha="center", va="center", z=5)

    py = ry + len(TAB) * (rh + 10) + 6
    hh = H - 150 - py
    rrect(M, py, W - 2 * M, hh, 16, "#EAF4FB", z=3); rrect(M, py, 10, hh, 5, CYANd, z=4)
    txt(M + 32, py + 44, "Repare: MAT quase não muda (31→33) — mas em LING é sempre", outfit, 15, INK, z=5)
    txt(M + 32, py + 72, "44–45, e nas mais concorridas nem gabaritar garante (45+).", outfit, 15, INK, z=5)
    txt(M + 32, py + 108, "Quer o corte e o peso do TEU curso? xtrisisu.com", outfitB, 17, CYANd, z=5)
    txt(M + 32, py + hh - 24, "cortes/pesos: SISU 2026 (ENEM 2025) · UECE fora: Medicina por vestibular próprio", mono, 10.5, GRAY, z=5)
    footer(hp, 3, "3/3")
    return save(fig, "c3_por_uf")


if __name__ == "__main__":
    card1(); card2(); card3()
