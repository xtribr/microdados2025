#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa da newsletter do LinkedIn (1280×720) — qual área do ENEM 2025 mais discrimina (TRI)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import new_slide, logo, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1280, 720

AR = json.loads((D.parent.parent / "estudo_discriminacao_idade/discriminacao_areas.json").read_text())
NOMES = {"LC": "Linguagens", "CH": "Humanas", "CN": "Natureza", "MT": "Matemática"}
DADOS = sorted(
    [(sigla, NOMES[sigla], AR[sigla]["A_media"]) for sigla in ("LC", "CH", "CN", "MT")],
    key=lambda d: -d[2],
)
VENCEDORA = DADOS[0][0]


def vir(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def make():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 56

    logo(ax, M + 100, 66, zoom=0.052)
    txt(W - M, 70, "ENEM 2025 · TRI OFICIAL", monoB, 11.5, GRAY, ha="right", va="center")

    ty = 128
    txt(M, ty, "QUAL ÁREA DO ENEM 2025 MAIS", outfitB, 32, INK)
    txt(M, ty + 40, "SEPARA QUEM SABE DE QUEM CHUTA?", outfitB, 29, CORAL)
    txt(M, ty + 76, "Parâmetro A oficial da TRI (3PL) por área · Microdados INEP 2025", outfit, 14, GRAY)

    # mini gráfico
    gy0 = ty + 112
    gh = 300
    base = gy0 + gh
    n = len(DADOS)
    area_w = (W - 2 * M) / n
    bw = area_w * 0.5
    maxr = max(d[2] for d in DADOS)
    scale = gh / (maxr * 1.18)

    for i, (sigla, nome, a_media) in enumerate(DADOS):
        gx = M + i * area_w + (area_w - bw) / 2
        hgt = a_media * scale
        cor = CORAL if sigla == VENCEDORA else "#C7CBD0"
        rrect(gx, base - hgt, bw, hgt, 8, cor, z=3)
        txt(gx + bw / 2, base - hgt - 12, vir(a_media), outfitB, 16,
            CORALd if sigla == VENCEDORA else "#6B7076", ha="center", z=5)
        txt(gx + bw / 2, base + 22, nome, outfitB, 12.5, INK, ha="center", z=5)

    ay = H - 46
    txt(M, ay, "Transformamos ", outfitB, 13, INK)
    xx = M + tw("Transformamos ", outfitB, 13)
    txt(xx, ay, "dados", outfitB, 13, CYAN); xx += tw("dados", outfitB, 13)
    txt(xx, ay, " em ", outfitB, 13, INK); xx += tw(" em ", outfitB, 13)
    txt(xx, ay, "aprovações", outfitB, 13, CORAL); xx += tw("aprovações", outfitB, 13)
    txt(xx, ay, ".", outfitB, 13, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 11, GRAY, ha="right")
    return save(fig, "capa_linkedin_discriminacao_2025")


if __name__ == "__main__":
    make()
