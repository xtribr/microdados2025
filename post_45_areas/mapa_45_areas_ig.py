#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG — mapa (tile grid) do Brasil: quem GABARITOU cada área (todos os itens válidos)
na 1ª aplicação regular, por estado. Feed 1080×1350 + Story 1080×1920.
Mesma arte do post_45_lc, agora para Matemática, Humanas e Natureza.
Dado: gabaritos_areas_uf.json (varredura completa de RESULTADOS_2025.csv).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
DADOS = json.loads((D / "gabaritos_areas_uf.json").read_text())
W = 1080

# tile grid do Brasil (col, row) — idêntico ao post de LC
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

# Config por área. n_anul = itens anulados (excluídos do total de válidas).
AREAS = {
    "MT": dict(tag="45mt", nome="Matemática", validas=43, n_anul=2, teto="980,3",
               milhoes="3,18 milhões"),
    "CH": dict(tag="45ch", nome="Humanas", validas=45, n_anul=0, teto="856,4",
               milhoes="3,37 milhões"),
    "CN": dict(tag="45cn", nome="Natureza", validas=42, n_anul=3, teto="858,7",
               milhoes="3,18 milhões"),
}


def make(area, H, tag):
    cfg = AREAS[area]
    por_uf = DADOS[area]["por_uf"]
    total = DADOS[area]["total"]
    presentes = DADOS[area]["presentes"]
    n_ufs = sum(1 for u in GRID if por_uf.get(u, 0) > 0)
    maxn = max(por_uf.values())
    nv = cfg["validas"]

    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400

    # ---- topo ----
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · 1ª APLICAÇÃO", monoB, 13, GRAY, ha="right", va="center")
    ty = 186 if not story else 250
    txt(M, ty, f"{nv} de {nv} em {cfg['nome']}:", outfitB, 44, INK)
    txt(M, ty + 54, "onde estão os gabaritos?", outfitB, 44, CORAL)
    txt(M, ty + 102, f"{cfg['milhoes']} fizeram a prova. Acertar TODAS as {nv}",
        outfit, 17.5, GRAY)
    txt(M, ty + 130, f"questões? Só {total} pessoas no país inteiro.", outfit, 17.5, GRAY)

    # ---- mapa (tile grid) ----
    ts = 74 if story else 60
    gp = 9
    cols, rows = 8, 9
    gw = cols * ts + (cols - 1) * gp
    gx = (W - gw) / 2
    gy = (ty + 170) if not story else (ty + 200)
    for uf, (cx, cy) in GRID.items():
        n = por_uf.get(uf, 0)
        x = gx + cx * (ts + gp)
        y = gy + cy * (ts + gp)
        if n > 0:
            col = CORALd if n == maxn else CORAL
            rrect(x, y, ts, ts, 12, col, z=3)
            txt(x + ts / 2, y + 17, uf, outfitB, 13, "#FFFFFF", ha="center", va="center", z=5)
            fs = 20 if n < 10 else (18.5 if n < 100 else 16.5)
            txt(x + ts / 2, y + ts - 21, str(n), outfitB, fs, "#FFFFFF",
                ha="center", va="center", z=5)
        else:
            rrect(x, y, ts, ts, 12, "#E2E3E5", z=3)
            txt(x + ts / 2, y + ts / 2, uf, outfit, 13.5, "#A9ADB1", ha="center", va="center", z=5)

    # legenda do mapa
    lgx = M
    lgy = gy + 8 * (ts + gp) + 8
    rrect(lgx, lgy, 18, 18, 5, CORAL, z=4)
    txt(lgx + 26, lgy + 10, "tem gabarito (nº = alunos)", mono, 12, GRAY, va="center", z=5)
    rrect(lgx, lgy + 28, 18, 18, 5, "#E2E3E5", z=4)
    txt(lgx + 26, lgy + 38, f"nenhum aluno com {nv}/{nv}", mono, 12, GRAY, va="center", z=5)

    # ---- hero ----
    hy = gy + rows * (ts + gp) + 22
    hh = 128
    shadow(M, hy, W - 2 * M, hh, 18)
    rrect(M, hy, W - 2 * M, hh, 18, CARD, z=3)
    big = str(total)
    txt(M + 36, hy + 88, big, outfitB, 62, CORAL, z=5)
    bx = M + 36 + tw(big, outfitB, 62) + 24
    razao = round(presentes / total / 1000)
    txt(bx, hy + 54, f"gabaritos em {n_ufs} estados", outfitB, 22, INK, z=5)
    txt(bx, hy + 86, f"1 a cada ~{razao} mil candidatos", outfit, 17, INK, z=5)
    txt(bx, hy + 112, f"nota máxima de {cfg['nome']} do país: {cfg['teto']} pontos",
        mono, 11.5, GRAY, z=5)

    # ---- rodapé (banda própria: >=60px do hero, >=50px entre nota de fonte e assinatura) ----
    fy = H - 150
    txt(M, fy, f"Fonte: Microdados ENEM 2025 / INEP · 1ª aplicação regular · correção item a "
               f"item das {nv} questões válidas", mono, 10, GRAY)
    nota2 = (f"UF = estado onde fez a prova · {cfg['n_anul']} "
             f"{'item anulado excluído' if cfg['n_anul'] == 1 else 'itens anulados excluídos'} "
             f"do total") if cfg["n_anul"] else \
            "UF = estado onde fez a prova · nenhum item anulado nesta área"
    txt(M, fy + 18, nota2, mono, 10, GRAY)
    ay = fy + 86
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · xtri.online", mono, 12, GRAY, ha="right")
    return save(fig, f"xtri_{cfg['tag']}_mapa_{tag}")


if __name__ == "__main__":
    for a in ("MT", "CH", "CN"):
        make(a, 1350, "feed")
        make(a, 1920, "story")
