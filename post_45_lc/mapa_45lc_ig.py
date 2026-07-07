#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG — mapa (tile grid) do Brasil: quem GABARITOU Linguagens (45/45) na 1ª aplicação,
por estado. Feed 1080×1350 + Story 1080×1920. Dado: gabaritos_lc_uf.json (varredura completa).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
DADOS = json.loads((D / "gabaritos_lc_uf.json").read_text())
POR_UF = DADOS["por_uf"]
TOTAL = DADOS["total"]
W = 1080

# tile grid do Brasil (col, row)
GRID = {
    "RR": (2, 0), "AP": (4, 0),
    "AM": (1, 1), "PA": (3, 1), "MA": (4, 1), "PI": (5, 1), "CE": (6, 1), "RN": (7, 1),
    "AC": (0, 2), "RO": (2, 2), "TO": (4, 2), "BA": (5, 2), "PE": (6, 2), "PB": (7, 2),
    "MT": (3, 3), "GO": (4, 3), "DF": (5, 3), "SE": (6, 3), "AL": (7, 3),
    "MS": (3, 4), "MG": (4, 4), "ES": (5, 4),
    "SP": (3, 5), "RJ": (4, 5),
    "PR": (3, 6),
    "SC": (3, 7),
    "RS": (3, 8),
}
N_UFS = sum(1 for u in GRID if POR_UF.get(u, 0) > 0)
MAXN = max(POR_UF.values())


def make(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400

    # ---- topo ----
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · 1ª APLICAÇÃO", monoB, 13, GRAY, ha="right", va="center")
    ty = 196 if not story else 250
    txt(M, ty, "45 de 45 em Linguagens:", outfitB, 44, INK)
    txt(M, ty + 54, "onde estão os gabaritos?", outfitB, 44, CORAL)
    txt(M, ty + 102, "3,37 milhões fizeram a prova. Acertar TODAS as 45", outfit, 17.5, GRAY)
    txt(M, ty + 130, f"questões? Só {TOTAL} pessoas no país inteiro.", outfit, 17.5, GRAY)

    # ---- mapa (tile grid) ----
    ts = 74 if story else 66      # tamanho do tile
    gp = 9                        # gap
    cols = 8
    rows = 9
    gw = cols * ts + (cols - 1) * gp
    gx = (W - gw) / 2
    gy = (ty + 178) if not story else (ty + 200)
    for uf, (cx, cy) in GRID.items():
        n = POR_UF.get(uf, 0)
        x = gx + cx * (ts + gp)
        y = gy + cy * (ts + gp)
        if n > 0:
            col = CORALd if n == MAXN else CORAL
            rrect(x, y, ts, ts, 12, col, z=3)
            txt(x + ts / 2, y + 17, uf, outfitB, 13, "#FFFFFF", ha="center", va="center", z=5)
            txt(x + ts / 2, y + ts - 21, str(n), outfitB, 20 if n < 10 else 18.5, "#FFFFFF",
                ha="center", va="center", z=5)
        else:
            rrect(x, y, ts, ts, 12, "#E2E3E5", z=3)
            txt(x + ts / 2, y + ts / 2, uf, outfit, 13.5, "#A9ADB1", ha="center", va="center", z=5)

    # legenda do mapa (canto inferior esquerdo da área do grid)
    lgx = M
    lgy = gy + 8 * (ts + gp) + 8
    rrect(lgx, lgy, 18, 18, 5, CORAL, z=4)
    txt(lgx + 26, lgy + 10, "tem gabarito (nº = alunos)", mono, 12, GRAY, va="center", z=5)
    rrect(lgx, lgy + 28, 18, 18, 5, "#E2E3E5", z=4)
    txt(lgx + 26, lgy + 38, "nenhum aluno com 45/45", mono, 12, GRAY, va="center", z=5)

    # ---- hero ----
    hy = gy + rows * (ts + gp) + 22
    hh = 128
    shadow(M, hy, W - 2 * M, hh, 18)
    rrect(M, hy, W - 2 * M, hh, 18, CARD, z=3)
    big = str(TOTAL)
    txt(M + 36, hy + 88, big, outfitB, 62, CORAL, z=5)
    bx = M + 36 + tw(big, outfitB, 62) + 24
    razao = round(3368961 / TOTAL / 1000)
    txt(bx, hy + 54, f"gabaritos em {N_UFS} estados", outfitB, 22, INK, z=5)
    txt(bx, hy + 86, f"1 a cada ~{razao} mil candidatos", outfit, 17, INK, z=5)
    txt(bx, hy + 112, "quem gabarita leva nota máxima de Linguagens do país", mono, 11.5, GRAY, z=5)

    # ---- rodapé ----
    fy = H - 96
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · 1ª aplicação regular · correção item a item das 45 questões",
        mono, 10, GRAY)
    txt(M, fy + 18, "UF = estado onde fez a prova · anulados excluídos do total de itens",
        mono, 10, GRAY)
    ay = fy + 46
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 12, GRAY, ha="right")
    return save(fig, f"xtri_45lc_mapa_{tag}")


if __name__ == "__main__":
    make(1350, "feed")
    make(1920, "story")
