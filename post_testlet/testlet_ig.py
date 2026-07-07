#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post Instagram — TESTLET de Linguagens (ENEM 2025, 1ª aplicação):
"Um texto, cinco questões — como os alunos se saíram?"
Feed 1080×1350 + Story 1080×1920. Dados: taxa de erro por item sobre TODOS os
3.368.961 participantes de LC do P1 regular (Microdados INEP; itens são os mesmos
em todas as cores — numeração exibida = caderno azul).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd,
                       DIF_DIFICIL, DIF_MDIFICIL)

X.OUTDIR = str(Path(__file__).resolve().parent)
W = 1080

# erro % (100 - pct_acerto) sobre 3.368.961 participantes (P1 regular, todas as cores)
DATA = [
    ("Q06", "achar o gênero", "(bilhete)",        100 - 50.65, DIF_DIFICIL),
    ("Q07", "por que é",      "uma crônica",      100 - 46.48, DIF_DIFICIL),
    ("Q08", "manuscrito",     "× digital",        100 - 31.66, DIF_MDIFICIL),
    ("Q09", "a conclusão",    "da autora",        100 - 31.48, DIF_MDIFICIL),
    ("Q10", "a síntese da",   "opinião dela",     100 - 34.11, DIF_MDIFICIL),
]
MEDIA = sum(d[3] for d in DATA) / 5          # 61,1
RESTO = 52.2                                  # LC Q11-45 (média por item, mesma base)


def make(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400
    dy = 190 if story else 0     # deslocamento do miolo na story

    # ---- topo ----
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · 1ª APLICAÇÃO", monoB, 13, GRAY, ha="right", va="center")
    ty = 200 if not story else 260
    txt(M, ty, "Um texto, cinco questões.", outfitB, 46, INK)
    txt(M, ty + 56, "Como os alunos se saíram?", outfitB, 46, CORAL)
    txt(M, ty + 106, "Na prova de Linguagens, as questões 06 a 10 (caderno azul)", outfit, 17.5, GRAY)
    txt(M, ty + 134, "saem TODAS da mesma crônica — “De próprio punho”.", outfit, 17.5, GRAY)

    # ---- gráfico ----
    base_y = (800 if not story else 1000) + dy * 0
    if story:
        base_y = 1010
    scale = 4.7 if not story else 5.6
    bw, gap = 118, 26
    x0 = 322
    # linha de referência (resto da prova) — atrás das barras
    ly = base_y - RESTO * scale
    ax.plot([M, x0 + 5 * bw + 4 * gap - gap + bw * 0], [ly, ly], color=CYANd, lw=2.2,
            linestyle=(0, (5, 4)), zorder=2)
    ax.plot([x0, W - M], [ly, ly], color=CYANd, lw=2.2, linestyle=(0, (5, 4)), zorder=2)
    txt(M, ly - 34, "média do resto", monoB, 12.5, CYANd, va="center", z=6)
    txt(M, ly - 12, "da prova: 52%", monoB, 12.5, CYANd, va="center", z=6)
    for i, (q, p1, p2, erro, cor) in enumerate(DATA):
        bx = x0 + i * (bw + gap)
        bh = erro * scale
        rrect(bx, base_y - bh, bw, bh, 10, cor, z=3)
        cxb = bx + bw / 2
        txt(cxb, base_y - bh - 16, f"{erro:.0f}%", outfitB, 30, INK, ha="center", z=5)
        txt(cxb, base_y + 30, q, monoB, 15, INK, ha="center", z=5)
        txt(cxb, base_y + 56, p1, mono, 11.5, GRAY, ha="center", z=5)
        txt(cxb, base_y + 74, p2, mono, 11.5, GRAY, ha="center", z=5)

    # legenda de dificuldade (canto do gráfico, acima das barras baixas)
    lgy = base_y - 69 * scale - 16
    rrect(M, lgy - 12, 18, 18, 5, DIF_DIFICIL, z=4)
    txt(M + 26, lgy + 2, "difícil", mono, 12, GRAY, va="center", z=5)
    rrect(M, lgy + 16, 18, 18, 5, DIF_MDIFICIL, z=4)
    txt(M + 26, lgy + 30, "muito difícil", mono, 12, GRAY, va="center", z=5)
    txt(M, lgy - 34, "TAXA DE ERRO (TRI)", monoB, 11.5, GRAY, z=5)

    # ---- hero ----
    hy = base_y + 112
    hh = 150
    shadow(M, hy, W - 2 * M, hh, 20)
    rrect(M, hy, W - 2 * M, hh, 20, CARD, z=3)
    big = f"{MEDIA:.0f}%"
    txt(M + 36, hy + 100, big, outfitB, 66, CORAL, z=5)
    bx2 = M + 36 + tw(big, outfitB, 66) + 26
    txt(bx2, hy + 62, "de erro médio nas 5 questões", outfitB, 22, INK, z=5)
    txt(bx2, hy + 94, "do texto único", outfitB, 22, INK, z=5)
    txt(bx2, hy + 124, "9 pontos acima do resto da prova (52%)", mono, 13, CYANd, z=5)

    # ---- leitura ----
    ry = hy + hh + 28
    rh = 118
    rrect(M, ry, W - 2 * M, rh, 18, "#FCEDE9", z=3)
    rrect(M, ry, 10, rh, 5, CORAL, z=4)
    txt(M + 34, ry + 46, "Reconhecer o gênero do texto, tudo bem (Q06–Q07).", outfit, 19, INK, z=5)
    txt(M + 34, ry + 84, "Interpretar o que a autora defende? 2 em cada 3 erraram.", outfitB, 19, CORALd, z=5)

    # ---- rodapé ----
    fy = H - 96
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · 1ª aplicação regular · 3.368.961 participantes em Linguagens",
        mono, 10, GRAY)
    txt(M, fy + 18, "taxa de erro por questão · itens iguais em todas as cores · numeração do caderno azul",
        mono, 10, GRAY)
    ay = fy + 46
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 12, GRAY, ha="right")

    from xtri_deck import save
    return save(fig, f"xtri_testlet_{tag}")


if __name__ == "__main__":
    make(1350, "feed")
    make(1920, "story")
