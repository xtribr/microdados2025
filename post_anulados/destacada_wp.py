#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Imagem destacada WordPress (1200×630) — post 'Questões anuladas do ENEM 2025: a autópsia das 6'."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1200, 630

CHIPS = [
    ("CN", "vazada", "coral"), ("CN", "convergência", "cyan"),
    ("CN", "vazada", "coral"), ("MT", "convergência", "cyan"),
    ("MT", "vazada", "coral"), ("CH", "Bis < 0,01", "cyan"),
]
AREA_COL = {"CH": "#E84855", "CN": "#2EC4B6", "MT": "#3A86FF"}


def main():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 56
    logo(ax, M + 108, 66, zoom=0.056)
    txt(W - M, 70, "MICRODADOS ENEM 2025", monoB, 12, GRAY, ha="right", va="center")

    # coluna esquerda — título
    ty = 200
    txt(M, ty, "Questões anuladas", outfitB, 46, INK)
    txt(M, ty + 54, "do ENEM 2025:", outfitB, 46, INK)
    txt(M, ty + 112, "a autópsia das 6", outfitB, 46, CORAL)
    txt(M, ty + 164, "3 vazadas + 3 reprovadas pela estatística.", outfit, 17, GRAY)
    txt(M, ty + 192, "O que cada uma deixou nos dados, item a item.", outfit, 17, GRAY)

    # coluna direita — 6 chips (2 col × 3 lin)
    cx0 = 660
    cw, ch = 236, 118
    gap = 12
    cy0 = 130
    for i, (area, motivo, tipo) in enumerate(CHIPS):
        r, c = divmod(i, 2)
        x = cx0 + c * (cw + gap)
        y = cy0 + r * (ch + gap)
        shadow(x, y, cw, ch, 14)
        rrect(x, y, cw, ch, 14, CARD, z=2)
        rrect(x, y, 8, ch, 4, CORAL if tipo == "coral" else CYANd, z=3)
        rrect(x + 22, y + ch / 2 - 21, 50, 42, 10, AREA_COL[area], z=3)
        txt(x + 47, y + ch / 2 + 1, area, outfitB, 16, "#FFFFFF", ha="center", va="center", z=5)
        selo = "POR VAZAMENTO" if tipo == "coral" else "PELA TRI"
        txt(x + 88, y + 42, selo, monoB, 10.5, CORALd if tipo == "coral" else CYANd, z=5)
        txt(x + 88, y + 72, motivo, outfitB, 16, INK, z=5)

    # rodapé
    ay = H - 40
    txt(M, ay, "Transformamos ", outfitB, 14, INK)
    xx = M + tw("Transformamos ", outfitB, 14)
    txt(xx, ay, "dados", outfitB, 14, CYAN); xx += tw("dados", outfitB, 14)
    txt(xx, ay, " em ", outfitB, 14, INK); xx += tw(" em ", outfitB, 14)
    txt(xx, ay, "aprovações", outfitB, 14, CORAL); xx += tw("aprovações", outfitB, 14)
    txt(xx, ay, ".", outfitB, 14, INK)
    txt(W - M, ay, "Fonte: Microdados ENEM 2025 / INEP · app.rankingenem.com", mono, 10.5, GRAY, ha="right")
    return save(fig, "destacada_wp_anuladas_1200x630")


if __name__ == "__main__":
    main()
