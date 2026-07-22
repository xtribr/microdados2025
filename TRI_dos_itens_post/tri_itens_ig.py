#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Versões INSTAGRAM (feed 1080×1350 + story 1080×1920) das artes do post "TRI dos itens".
As artes originais (tri_itens_graphics.py) eram WordPress 1200×630/1200×740 e usavam
caminhos de sandbox + a assinatura APOSENTADA. Aqui: padrão XTRI atual (CLAUDE.md).
Dado real: TRI_ITENS_AZUL_ENEM2025.xlsx (caderno Azul, 175 itens válidos).
"""
import sys
from pathlib import Path

import numpy as np
import openpyxl
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
BASE = D.parent
W = 1080
AMBER_BG = "#FBEFD6"
AMBER_INK = "#B07A1E"
CYAN_BG = "#E3F4FD"

ACOL = {"Linguagens": "#1FAFEF", "Ciências Humanas": "#E84B8A",
        "Ciências da Natureza": "#27AE60", "Matemática": "#F39C12"}
ANOME = {"Linguagens": "Linguagens", "Ciências Humanas": "Humanas",
         "Ciências da Natureza": "Natureza", "Matemática": "Matemática"}

# ---------- dados reais ----------
wb = openpyxl.load_workbook(BASE / "TRI_ITENS_AZUL_ENEM2025.xlsx", data_only=True)
pts = {a: [] for a in ACOL}
for r in list(wb["TRI_itens"].iter_rows(values_only=True))[1:]:
    n, area, ling, co, hab, gab, a, b, c, tri, pac, nresp, anul = r
    if anul:                                    # anulados fora (CN 3 · MT 2)
        continue
    if area == "Linguagens" and ling == "Espanhol":   # LC = Inglês nas 1-5
        continue
    if isinstance(tri, (int, float)) and isinstance(pac, (int, float)):
        pts[area].append((n, tri, pac))

ALLP = [(n, t, p, ar) for ar, v in pts.items() for (n, t, p) in v]
NITENS = len(ALLP)
CORR = float(np.corrcoef([p[1] for p in ALLP], [p[2] for p in ALLP])[0, 1])
HARD = max(ALLP, key=lambda p: p[1])      # (160, 923.7, 15, Matemática)
EASY = min(ALLP, key=lambda p: p[1])      # (26, 440.4, 87, Linguagens)
STATS = {ar: (float(np.mean([p[1] for p in v])), min(p[1] for p in v), max(p[1] for p in v))
         for ar, v in pts.items()}


def br(v, dec=1):
    return f"{v:.{dec}f}".replace(".", ",")


def rodape(hp, H, M, nota):
    """Banda própria do rodapé: >=60px do conteúdo, >=50px entre nota e assinatura."""
    txt = hp["txt"]; tw = hp["tw"]
    fy = H - 150
    txt(M, fy, nota, mono, 10, GRAY)
    txt(M, fy + 18, f"TRI dos itens · caderno Azul · {NITENS} itens válidos (anulados excluídos)",
        mono, 10, GRAY)
    ay = fy + 86
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · xtri.online", mono, 12, GRAY, ha="right")


def topo(ax, hp, M, ty, l1, l2, sub1, sub2, eyebrow):
    txt = hp["txt"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · 180 ITENS", monoB, 13, GRAY, ha="right", va="center")
    txt(M, ty, eyebrow, monoB, 13, CORALd)
    txt(M, ty + 52, l1, outfitB, 44, INK)
    txt(M, ty + 106, l2, outfitB, 44, CORAL)
    txt(M, ty + 154, sub1, outfit, 17.5, GRAY)
    txt(M, ty + 182, sub2, outfit, 17.5, GRAY)


# ============================ CAPA ============================
def capa(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400
    ty = 168 if not story else 236

    topo(ax, hp, M, ty, "TRI dos itens", "da mais fácil à mais brutal",
         f"As {NITENS} questões que valeram nota, medidas item a item",
         "pela TRI do próprio INEP. Área por área.", "O RAIO-X COMPLETO DA PROVA")

    # ---- faixas min–max de dificuldade por área ----
    by = (ty + 250) if not story else (ty + 300)
    bx0, bx1 = 208, W - M
    XMIN, XMAX = 420, 980

    def PX(v):
        return bx0 + (v - XMIN) / (XMAX - XMIN) * (bx1 - bx0)

    txt(M, by - 26, "faixa de dificuldade TRI de cada área (mín → máx)", mono, 11.5, GRAY)
    rowh = 62
    for i, (ar, col) in enumerate(ACOL.items()):
        mean, mn, mx = STATS[ar]
        yy = by + i * rowh
        txt(M, yy + 15, ANOME[ar], outfitB, 15, INK)
        rrect(PX(mn), yy + 6, PX(mx) - PX(mn), 18, 9, col, z=3)
        # média = marca branca
        ax.add_patch(FancyBboxPatch((PX(mean) - 2.5, yy + 4), 5, 22, boxstyle="square,pad=0",
                                    fc="#FFFFFF", ec=INK, lw=1.0, zorder=5))
        txt(PX(mx) + 10, yy + 16, br(mx), mono, 11, GRAY, va="center")
    sy = by + 4 * rowh + 2
    for gx in (450, 550, 650, 750, 850, 950):  # escala ate 980, ticks ate 950
        ax.add_line(Line2D([PX(gx), PX(gx)], [by - 8, sy - 6], color="#E0E1E3", lw=0.8, zorder=1))
        txt(PX(gx), sy + 12, str(gx), mono, 10, GRAY, ha="center")
    txt(M, sy + 12, "escala TRI", mono, 10, GRAY)
    txt(bx0, sy + 40, "traço branco = dificuldade média da área", mono, 10.5, GRAY)

    # ---- card: a mais brutal ----
    cy = sy + 68
    ch = 172
    shadow(M, cy, W - 2 * M, ch, 20)
    rrect(M, cy, W - 2 * M, ch, 20, AMBER_BG, z=3)
    txt(M + 32, cy + 40, "A MAIS BRUTAL DE TODA A PROVA", mono, 12.5, AMBER_INK, z=5)
    txt(M + 32, cy + 92, f"Matemática Q{HARD[0]}", outfitB, 31, INK, z=5)
    txt(M + 32 + tw(f"Matemática Q{HARD[0]}", outfitB, 31) + 16, cy + 92,
        f"dificuldade TRI {br(HARD[1])}", outfitB, 24, CORALd, z=5)
    txt(M + 32, cy + 132, f"só {br(HARD[2], 0)}% acertaram", outfit, 17, AMBER_INK, z=5)

    # ---- card: a mais fácil ----
    c2 = cy + ch + 26
    shadow(M, c2, W - 2 * M, ch, 20)
    rrect(M, c2, W - 2 * M, ch, 20, CYAN_BG, z=3)
    txt(M + 32, c2 + 40, "A MAIS FÁCIL DE TODA A PROVA", mono, 12.5, CYANd, z=5)
    txt(M + 32, c2 + 92, f"Linguagens Q{EASY[0]}", outfitB, 31, INK, z=5)
    txt(M + 32 + tw(f"Linguagens Q{EASY[0]}", outfitB, 31) + 16, c2 + 92,
        f"dificuldade TRI {br(EASY[1])}", outfitB, 24, CYANd, z=5)
    txt(M + 32, c2 + 132, f"{br(EASY[2], 0)}% acertaram", outfit, 17, CYANd, z=5)

    rodape(hp, H, M, "Fonte: Microdados ENEM 2025 / INEP · dificuldade TRI = b×100+500")
    return save(fig, f"xtri_tri_itens_capa_{tag}")


# ============================ SCATTER ============================
def scatter(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 64
    story = H > 1400
    ty = 168 if not story else 236

    topo(ax, hp, M, ty, "Dificuldade × acerto:", f"as {NITENS} questões",
         f"Cada ponto é uma questão. Quanto mais difícil pela TRI,",
         f"menor o acerto — correlação {br(CORR, 2)}.", "O RAIO-X COMPLETO DA PROVA")

    # ---- legenda das áreas (2 col × 2 linhas) ----
    ly = (ty + 232) if not story else (ty + 286)
    for i, (ar, col) in enumerate(ACOL.items()):
        cx = M + (i % 2) * 300
        cyy = ly + (i // 2) * 30
        ax.add_patch(FancyBboxPatch((cx, cyy - 6), 13, 13, boxstyle="circle,pad=0",
                                    fc=col, ec="white", lw=0.6, zorder=4))
        txt(cx + 24, cyy + 5, ANOME[ar], mono, 12.5, INK)

    # ---- área de plot ----
    px0, px1 = 148, W - M
    py0 = ly + 84
    py1 = py0 + (630 if not story else 900)
    XMIN, XMAX, YMIN, YMAX = 420, 980, 0, 90

    def PX(v):
        return px0 + (v - XMIN) / (XMAX - XMIN) * (px1 - px0)

    def PY(v):
        return py1 - (v - YMIN) / (YMAX - YMIN) * (py1 - py0)

    for gx in range(450, 951, 100):
        ax.add_line(Line2D([PX(gx), PX(gx)], [py0, py1], color="#E6E7E9", lw=0.8, zorder=1))
        txt(PX(gx), py1 + 24, str(gx), mono, 10.5, GRAY, ha="center")
    for gy in range(0, 91, 15):
        ax.add_line(Line2D([px0, px1], [PY(gy), PY(gy)], color="#E6E7E9", lw=0.8, zorder=1))
        txt(px0 - 12, PY(gy), f"{gy}%", mono, 10.5, GRAY, ha="right", va="center")
    txt((px0 + px1) / 2, py1 + 52, "Dificuldade TRI (b×100+500)", mono, 12, INK, ha="center")
    ax.text(76, (py0 + py1) / 2, "% de acerto", fontproperties=mono, fontsize=12, color=INK,
            ha="center", va="center", rotation=90, zorder=5)

    # ---- pontos ----
    for ar, col in ACOL.items():
        for n, tri, pac in pts[ar]:
            ax.add_patch(FancyBboxPatch((PX(tri) - 4.5, PY(pac) - 4.5), 9, 9,
                                        boxstyle="circle,pad=0", fc=col, ec="white",
                                        lw=0.5, alpha=0.9, zorder=4))
    # ---- reta de tendência (clipada à área do plot) ----
    # sem clipe a reta prevê acerto negativo (-19,7% em TRI=980) e vaza para cima do rodapé.
    m, bb = np.polyfit([p[1] for p in ALLP], [p[2] for p in ALLP], 1)
    xs = sorted([(YMIN - bb) / m, (YMAX - bb) / m])          # onde a reta cruza 0% e 90%
    lx0 = max(XMIN, xs[0])
    lx1 = min(XMAX, xs[1])
    ax.add_line(Line2D([PX(lx0), PX(lx1)], [PY(m * lx0 + bb), PY(m * lx1 + bb)],
                       color=INK, lw=2, ls=(0, (6, 4)), zorder=5))

    def marca(tri, pac, col):
        ax.add_patch(FancyBboxPatch((PX(tri) - 7, PY(pac) - 7), 14, 14, boxstyle="circle,pad=0",
                                    fc=col, ec=INK, lw=1.6, zorder=6))

    marca(HARD[1], HARD[2], CORAL)
    txt(PX(HARD[1]) - 14, PY(HARD[2]) + 4, f"MT Q{HARD[0]} · mais difícil", monoB, 11.5,
        CORALd, ha="right")
    marca(EASY[1], EASY[2], CYAN)
    txt(PX(EASY[1]) + 16, PY(EASY[2]) + 4, f"LC Q{EASY[0]} · mais fácil", monoB, 11.5, CYANd)

    rodape(hp, H, M, "Fonte: Microdados ENEM 2025 / INEP · dificuldade TRI = b×100+500")
    return save(fig, f"xtri_tri_itens_scatter_{tag}")


if __name__ == "__main__":
    capa(1350, "feed")
    capa(1920, "story")
    scatter(1350, "feed")
    scatter(1920, "story")
