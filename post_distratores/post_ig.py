#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG — mapa de distratores: a alternativa ERRADA que mais engana no ENEM 2025.
Dado real: 180 itens do caderno Azul regular, streaming completo sobre 4,81 mi de presentes.
Feed 1080×1350 + Story 1080×1920.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W = 1080

ESTUDO = D.parent / "estudo_distratores"
resumo = json.loads((ESTUDO / "distratores_resumo.json").read_text())
itens = list(csv.DictReader((ESTUDO / "distratores_itens.csv").open(encoding="utf-8")))
N_ARMADILHA = sum(1 for r in itens if float(r["pct_campeao_da_base"]) > float(r["pct_acerto"]))
PCT_ARMADILHA = round(100 * N_ARMADILHA / len(itens))

NOMES = {"LC": "Linguagens", "CH": "Humanas", "CN": "Natureza", "MT": "Matemática"}
CAMPEOES = [(area, resumo["por_area"][area]["top3"][0]) for area in ("LC", "CH", "CN", "MT")]


def vir(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def make(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400

    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · MICRODADOS · MAPA DE DISTRATORES", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 192 if not story else 246
    txt(M, ty, f"EM {PCT_ARMADILHA}% DAS QUESTÕES DO ENEM 2025,", outfitB, 33, INK)
    txt(M, ty + 44, "A PEGADINHA VENCEU O GABARITO", outfitB, 38, CORAL)
    txt(M, ty + 90, f"Em {N_ARMADILHA} de 180 questões, mais gente marcou UMA alternativa errada", outfit, 16, GRAY)
    txt(M, ty + 116, "específica do que acertou a questão. Mapeei qual é, item por item.", outfit, 16, GRAY)

    # ---- hero: o caso mais extremo ----
    hy = ty + 164
    hh = 190 if not story else 210
    shadow(M, hy, W - 2 * M, hh, 20)
    rrect(M, hy, W - 2 * M, hh, 20, CARD, z=3)
    txt(M + 36, hy + 34, "O CASO MAIS EXTREMO — CIÊNCIAS DA NATUREZA, CICLOS BIOGEOQUÍMICOS", monoB, 11.5, GRAY, z=5)
    txt(M + 36, hy + 84, "45,9%", outfitB, 46, CORAL, z=5)
    bx = M + 36 + tw("45,9%", outfitB, 46) + 26
    txt(bx, hy + 62, "marcaram a alternativa A (errada) —", outfitB, 17, INK, z=5)
    txt(bx, hy + 90, "quase 3× mais do que os 16,5% que acertaram", outfitB, 17, INK, z=5)
    txt(M + 36, hy + hh - 22, "gabarito B · 792 mil presentes na questão · dado oficial INEP, não é estimativa",
        mono, 11, GRAY, z=5)

    # ---- tabela: campeão por área ----
    ty2 = hy + hh + 46
    txt(M, ty2, "A PEGADINHA MAIS EFICAZ DE CADA ÁREA", monoB, 12.5, GRAY, z=3)
    row_h = 124 if not story else 240
    gap = 18 if not story else 25
    ty2 += 34
    for i, (area, c) in enumerate(CAMPEOES):
        ry = ty2 + i * (row_h + gap)
        rrect(M, ry, W - 2 * M, row_h, 16, "#FFFFFF", z=3)
        rrect(M, ry, 8, row_h, 4, CORAL, z=4)
        txt(M + 32, ry + 34, NOMES[area].upper(), outfitB, 18, INK, z=5)
        txt(M + 32, ry + 66, c["habilidade_desc"][:78] + ("…" if len(c["habilidade_desc"]) > 78 else ""),
            outfit, 13.5, GRAY, z=5)
        txt(M + 32, ry + row_h - 20,
            f"gabarito {c['gabarito']} · distrator {c['distrator_campeao']}", mono, 11.5, GRAY, z=5)
        pctx = W - M - 32
        txt(pctx, ry + row_h / 2 - 8, f"{vir(c['pct_campeao_entre_errados'])}%", outfitB, 30, CORALd,
            ha="right", va="center", z=5)
        txt(pctx, ry + row_h / 2 + 26, "de quem errou", mono, 11, GRAY, ha="right", va="center", z=5)

    # ---- rodapé ----
    fy = H - 96
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · caderno Azul regular, 180 itens, itens anulados excluídos · streaming completo (4,81 mi de linhas)",
        mono, 8.7, GRAY)
    ay = fy + 46
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 12, GRAY, ha="right")
    return save(fig, f"xtri_distratores_2025_{tag}")


if __name__ == "__main__":
    make(1350, "feed")
    make(1920, "story")
