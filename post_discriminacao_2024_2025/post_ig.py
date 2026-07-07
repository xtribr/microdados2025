#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG — qual área do ENEM 2025 mais separa quem sabe de quem chuta?
Parâmetro A oficial da TRI (3PL), banco Regular / caderno Azul, itens não anulados.
Sem comparação com 2024 (dado oficial não disponível para aquele ano — ver estudo completo).
Feed 1080×1350 + Story 1080×1920.
"""
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

AR = json.loads((D.parent / "estudo_discriminacao_idade/discriminacao_areas.json").read_text())
NOMES = {"LC": "Linguagens", "CH": "Humanas", "CN": "Natureza", "MT": "Matemática"}
DADOS = sorted(
    [(sigla, NOMES[sigla], AR[sigla]["A_media"]) for sigla in ("LC", "CH", "CN", "MT")],
    key=lambda d: -d[2],
)
VENCEDORA = DADOS[0]
LANTERNA = DADOS[-1]


def vir(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def make(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400

    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · MICRODADOS · TRI OFICIAL", monoB, 12.5, GRAY, ha="right", va="center")
    ty = 192 if not story else 246
    txt(M, ty, "QUAL ÁREA DO ENEM 2025 MAIS", outfitB, 38, INK)
    txt(M, ty + 46, "SEPARA QUEM SABE DE QUEM CHUTA?", outfitB, 34, CORAL)
    txt(M, ty + 92, "A resposta pode te surpreender.", outfit, 16.5, GRAY)
    txt(M, ty + 118, "Parâmetro A oficial da TRI por área — dado real do INEP, não é estimativa.", outfit, 16.5, GRAY)

    # ---- gráfico — 1 barra por área, bem maior ----
    gy0 = ty + 198
    gh = 450 if not story else 930
    base = gy0 + gh
    n = len(DADOS)
    group_w = (W - 2 * M) / n
    bw = group_w * 0.56

    maxr = max(d[2] for d in DADOS)
    scale = gh / (maxr * 1.18)

    txt(M, gy0 - 16, "linha tracejada = limiar oficial de discriminação \"muito alta\" (A ≥ 1,70)",
        mono, 10.5, GRAY, va="bottom", z=3)

    for v in (1.0, 2.0):
        yv = base - v * scale
        ax.plot([M, W - M], [yv, yv], color="#E9EAEB", lw=1, zorder=1)
        txt(M - 10, yv, vir(v, 1), mono, 10.5, GRAY, ha="right", va="center", z=3)

    th = 1.70
    yth = base - th * scale
    ax.plot([M, W - M], [yth, yth], color="#C7CBD0", lw=1.4, zorder=2, linestyle=(0, (5, 4)))

    RANKS = ["1º", "2º", "3º", "4º"]
    for i, (sigla, nome, a_media) in enumerate(DADOS):
        gx = M + i * group_w + (group_w - bw) / 2
        hgt = a_media * scale
        cor = CORAL if sigla == VENCEDORA[0] else "#C7CBD0"
        rrect(gx, base - hgt, bw, hgt, 10, cor, z=3)
        txt(gx + bw / 2, base - hgt - 16, vir(a_media), outfitB, 21,
            CORALd if sigla == VENCEDORA[0] else "#6B7076", ha="center", z=5)
        txt(gx + bw / 2, base + 30, nome, outfitB, 15.5, INK, ha="center", z=5)
        txt(gx + bw / 2, base + 54, RANKS[i], mono, 12, GRAY, ha="center", z=5)

    # ---- resposta (as 4 áreas, não só os extremos) ----
    hy = base + 92
    hh = 222 if not story else 244
    shadow(M, hy, W - 2 * M, hh, 20)
    rrect(M, hy, W - 2 * M, hh, 20, CARD, z=3)
    txt(M + 36, hy + 34, "RESPOSTA", monoB, 12, GRAY, z=5)
    txt(M + 36, hy + 80, VENCEDORA[1].upper(), outfitB, 40, CORAL, z=5)
    bx = M + 36 + tw(VENCEDORA[1].upper(), outfitB, 40) + 26
    seg = DADOS[1]
    txt(bx, hy + 60, f"A média = {vir(VENCEDORA[2])} — só {vir(VENCEDORA[2] - seg[2])} à frente de", outfitB, 15, INK, z=5)
    txt(bx, hy + 86, f"{seg[1]} ({vir(seg[2])}), a 2ª colocada.", outfitB, 15, INK, z=5)
    terc = DADOS[2]
    txt(M + 36, hy + 128,
        f"{terc[1]} fica no meio ({vir(terc[2])}) — sólida, sem se destacar.", outfit, 14.5, GRAY, z=5)
    txt(M + 36, hy + hh - 26,
        f"a queda real é só na {LANTERNA[1]}: A = {vir(LANTERNA[2])}, {vir(terc[2] - LANTERNA[2])} abaixo de {terc[1]}",
        mono, 11.5, GRAY, z=5)

    # ---- rodapé ----
    fy = H - 96
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · parâmetro A do modelo 3PL (TRI) · banco Regular, caderno Azul, itens não anulados",
        mono, 9.5, GRAY)
    ay = fy + 50
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 12, GRAY, ha="right")
    return save(fig, f"xtri_discriminacao_2025_{tag}")


if __name__ == "__main__":
    make(1350, "feed")
    make(1920, "story")
