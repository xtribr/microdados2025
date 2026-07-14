#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Propaganda XTRI (estilo 'stift') — público ESCOLA. Contraste: parado embaixo vs subir a
escada até a META + alvo. Voz XTRI (dados -> próximo nível). Gera feed 1080x1350 e story 1080x1920."""
import sys
from pathlib import Path
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
import xtri_deck as X
from xtri_deck import new_slide, logo, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd
D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W = 1080
M = 70
BG = "#EFEFF4"; GRID = "#E3E3EC"; CORALhl = "#FA5230"


def draw(name, H, TOP, GND, steps, sw, sh, x0, fs, alvo_r):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))
    for gx in range(0, W + 1, 54): ax.plot([gx, gx], [0, H], color=GRID, lw=0.8, zorder=0.5)
    for gy in range(0, H + 1, 54): ax.plot([0, W], [gy, gy], color=GRID, lw=0.8, zorder=0.5)
    for (sx, sy) in [(120, 250), (980, 300), (60, 640), (1010, 780), (150, GND + 60), (930, GND + 70), (540, 210)]:
        txt(sx, sy, "+", monoB, 20, "#CFCFDA", ha="center", va="center", z=1)

    # topo
    logo(ax, W / 2 + 66, 96, zoom=0.085)
    txt(W / 2, 150, "xtri.online", monoB, 15, GRAY, ha="center", va="center")

    # headline (2 colunas) — público ESCOLA
    def hl(x, y, s, fp, sz, tcol, bg, pad=13):
        w = tw(s, fp, sz)
        rrect(x - pad, y - sz * 1.02, w + 2 * pad, sz * 1.34, 9, bg, z=4)
        txt(x, y, s, fp, sz, tcol, z=5)
        return w + 2 * pad
    lx = M; ly = 236; LS = 44
    txt(lx, ly, "Ler os", outfit, 27, GRAY)
    txt(lx, ly + LS, "DADOS DA PROVA,", outfitB, 33, INK)
    txt(lx, ly + 2 * LS, "questão por questão,", outfit, 27, GRAY)
    rx = W / 2 + 26
    txt(rx, ly, "é o que leva", outfit, 27, GRAY)
    txt(rx, ly + LS, "sua ", outfit, 30, INK)
    hl(rx + tw("sua ", outfit, 30) + 10, ly + LS, "ESCOLA", outfitB, 30, "#FFFFFF", CYANd)
    hl(rx, ly + 2 * LS, "AO PRÓXIMO NÍVEL", outfitB, 30, "#FFFFFF", CORALhl)

    # chão
    ax.plot([M - 6, W - M + 6], [GND, GND], color="#C9C9D4", lw=2.5, zorder=2, solid_capstyle="round")

    def pilar(cx, w, top):
        shadow(cx - w / 2, top, w, GND - top, 16)
        rrect(cx - w / 2, top, w, GND - top, 16, CARD, z=5, ec="#1D1D20", lw=3)

    def bandeira(cx, top, cor, label):
        pt = top - 96
        ax.plot([cx, cx], [top, pt], color=INK, lw=4, zorder=6, solid_capstyle="round")
        ax.add_patch(Polygon([(cx, pt), (cx + 96, pt + 20), (cx, pt + 44)], closed=True, fc=cor, ec=INK, lw=3, zorder=7, joinstyle="round"))
        txt(cx + 32, pt + 27, label, outfitB, 17, "#FFFFFF", ha="center", va="center", z=8)

    def figura(fx, feet, s, pose, cor):
        hr = 20 * s; hy = feet - 120 * s; trunk = hy + hr + 52 * s
        ax.plot([fx, fx], [hy + hr, trunk], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
        ax.add_patch(Circle((fx, hy), hr, fc="#FFFFFF", ec=cor, lw=5 * s, zorder=12))
        if pose == "subindo":
            ax.plot([fx, fx - 26 * s], [trunk, feet], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
            ax.plot([fx, fx + 24 * s], [trunk, feet - 34 * s], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
            ax.plot([fx, fx + 30 * s], [hy + hr + 16 * s, hy + hr - 6 * s], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
            ax.plot([fx, fx - 22 * s], [hy + hr + 16 * s, hy + hr + 40 * s], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
        else:
            ax.plot([fx, fx - 18 * s], [trunk, feet], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
            ax.plot([fx, fx + 18 * s], [trunk, feet], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
            ax.plot([fx, fx - 26 * s], [hy + hr + 18 * s, hy + hr + 46 * s], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")
            ax.plot([fx, fx + 26 * s], [hy + hr + 18 * s, hy + hr + 46 * s], color=cor, lw=6 * s, zorder=11, solid_capstyle="round")

    def alvo(cx, cy, r):
        for rr, c in [(r, CORAL), (r * 0.68, "#FFFFFF"), (r * 0.42, CORAL), (r * 0.16, "#FFFFFF")]:
            ax.add_patch(Circle((cx, cy), rr, fc=c, ec=INK, lw=2, zorder=9))
        ax.add_patch(Circle((cx, cy), r * 0.06, fc=INK, ec="none", zorder=10))

    # LADO ESQUERDO
    pilar(210, 140, TOP); bandeira(210, TOP, CORAL, "META")
    figura(98, GND, 1.05 * fs, "parado", GRAY)
    ax.add_patch(FancyBboxPatch((122, GND - 96), 72, 40, boxstyle="round,pad=3", fc="#FFFFFF", ec=GRAY, lw=2, zorder=13))
    txt(158, GND - 72, "DIA 21", monoB, 12, GRAY, ha="center", va="center", z=14)
    txt(210, GND + 38, "sem dados, a meta fica longe", outfit, 15, GRAY, ha="center")

    # LADO DIREITO
    for i in range(steps):
        bx = x0 + i * sw; by = GND - (i + 1) * sh
        rrect(bx, by, sw + 2, GND - by, 6, "#FFFFFF", z=5, ec="#1D1D20", lw=2)
        txt(bx + sw / 2 + 1, by + sh / 2, f"DIA {i+1}", monoB, 10, GRAY, ha="center", va="center", z=6)
    pcx = x0 + steps * sw + 66
    pilar(pcx, 128, TOP); bandeira(pcx, TOP, CORAL, "META")
    alvo(pcx, TOP + 88, alvo_r)
    figura(x0 + (steps - 2) * sw + 22, GND - (steps - 1) * sh, fs, "subindo", INK)
    txt((x0 + pcx) / 2, GND + 38, "com a XTRI, um passo de cada vez", outfit, 15, CORALd, ha="center")

    # CTA
    bw = 360; bh = 74; bxx = (W - bw) / 2; by = H - 174
    shadow(bxx, by, bw, bh, bh / 2); rrect(bxx, by, bw, bh, bh / 2, "#FFFFFF", z=8)
    ax.add_patch(Circle((bxx + 52, by + bh / 2), 17, fc=INK, ec="none", zorder=9))
    txt(bxx + 52, by + bh / 2, "i", outfitB, 20, "#FFFFFF", ha="center", va="center", z=10)
    txt(bxx + 90, by + bh / 2, "Leia a legenda", outfitB, 24, INK, ha="left", va="center", z=9)

    # assinatura
    sy = H - 50
    parts = [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]
    total = sum(tw(s, outfitB, 16) for s, _ in parts); xx = W / 2 - total / 2
    for s, c in parts:
        txt(xx, sy, s, outfitB, 16, c, z=16); xx += tw(s, outfitB, 16)
    return save(fig, name)


if __name__ == "__main__":
    draw("promo_xtri_escola_feed", 1350, 560, 1070, 8, 44, 54, 502, 1.0, 50)
    draw("promo_xtri_escola_story", 1920, 640, 1340, 8, 48, 76, 470, 1.3, 64)
