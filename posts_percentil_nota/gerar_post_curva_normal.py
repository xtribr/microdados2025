#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG — a curva normal traduzida para a escala do ENEM (500 = média,
100 pontos = 1 desvio-padrão na população de referência da escala), com faixas
de % (34,1/13,6/2,1/0,1) e o aviso empírico de 2025 (percentis reais por área).
Sem glifos σ/μ (ausentes na Outfit): usar "DP" e "média".
"""
import sys
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent
sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN,
                       DIF_FACIL, DIF_MEDIO, DIF_DIFICIL, DIF_MDIFICIL)

X.OUTDIR = str(D)


def build(W, H, nome):
    fig, ax, hp = new_slide(W, H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 72
    story = H > 1500
    y = 250 if story else 118

    logo(ax, W - M + 6, (200 if story else 106), zoom=0.085)
    txt(M, y, "A ESCALA DO ENEM FOI DESENHADA NUMA CURVA NORMAL", monoB, 15, CORALd)
    y += 84 if story else 76
    txt(M, y, "ONDE SUA NOTA CAI", outfitB, 62, INK)
    y += 72
    txt(M, y, "NA CURVA DO ENEM", outfitB, 62, CORAL)
    y += 64 if story else 58
    txt(M, y, "500 = média da referência · cada 100 pontos = 1 desvio-padrão (DP).", outfit, 21.5, GRAY)

    # ---------- curva normal ----------
    top = y + (130 if story else 66)
    ch_h = 680 if story else 470          # altura da região da curva
    base = top + ch_h                     # linha do eixo
    x0, x1 = M + 10, W - M - 10
    sig_min, sig_max = -3.6, 3.6

    def sx(s):
        return x0 + (s - sig_min) / (sig_max - sig_min) * (x1 - x0)

    def dens(s):
        return np.exp(-0.5 * s * s)

    escala = (ch_h - 60) / dens(0)

    bandas = [(-3.6, -3, DIF_MDIFICIL, "0,1%"), (-3, -2, DIF_DIFICIL, "2,1%"),
              (-2, -1, DIF_MEDIO, "13,6%"), (-1, 0, DIF_FACIL, "34,1%"),
              (0, 1, DIF_FACIL, "34,1%"), (1, 2, DIF_MEDIO, "13,6%"),
              (2, 3, DIF_DIFICIL, "2,1%"), (3, 3.6, DIF_MDIFICIL, "0,1%")]
    for a_, b_, cor, lab in bandas:
        ss = np.linspace(a_, b_, 60)
        xs = [sx(s) for s in ss]
        ys = [base - dens(s) * escala for s in ss]
        ax.fill(list(xs) + [sx(b_), sx(a_)], list(ys) + [base, base],
                color=cor, alpha=0.85, zorder=2, lw=0)
        mid = (max(a_, -3.3) + min(b_, 3.3)) / 2
        if abs(mid) < 1:
            txt(sx(mid), base - dens(mid) * escala * 0.45, lab, outfitB, 20, "#FFFFFF", ha="center", z=5)
        elif abs(mid) < 2:
            txt(sx(mid), base - dens(mid) * escala * 0.32, lab, outfitB, 16, INK, ha="center", z=5)
        else:
            txt(sx((a_ + b_) / 2), base - 90 - (18 if abs(mid) > 3 else 0), lab, outfitB, 13.5,
                CORALd if abs(mid) > 3 else INK, ha="center", z=5)
    ss = np.linspace(sig_min, sig_max, 240)
    ax.plot([sx(s) for s in ss], [base - dens(s) * escala for s in ss],
            color=INK, lw=2.4, zorder=4)
    ax.plot([x0 - 6, x1 + 6], [base, base], color="#B9BDC1", lw=1.6, zorder=4)

    # eixo em NOTAS + em DP
    for s, nota in [(-3, "200"), (-2, "300"), (-1, "400"), (0, "500"),
                    (1, "600"), (2, "700"), (3, "800")]:
        ax.plot([sx(s), sx(s)], [base, base + 8], color="#B9BDC1", lw=1.4, zorder=4)
        txt(sx(s), base + 34, nota, outfitB, 20, CORAL if s in (1, 2) else INK, ha="center", z=5)
        dp = "média" if s == 0 else f"{s:+d} DP"
        txt(sx(s), base + 62, dp, mono, 12.5, GRAY, ha="center", z=5)

    # marcações 600 e 700 (as notas que o aluno persegue)
    for s, nota, pct in [(1, "600", "só 16% passam daqui"), (2, "700", "só 2,3% passam")]:
        xx = sx(s)
        ax.plot([xx, xx], [base - dens(s) * escala, base - ch_h + (30 if s == 1 else 90)],
                color=CORALd, lw=1.6, ls=(0, (4, 3)), zorder=5)
        txt(xx + 12, base - ch_h + (52 if s == 1 else 112), nota, outfitB, 24, CORALd, z=6)
        txt(xx + 12, base - ch_h + (80 if s == 1 else 140), pct, outfit, 15.5, INK, z=6)

    # ---------- aviso empírico ----------
    ay = base + (110 if story else 96)
    ah = 168 if story else 150
    rrect(M, ay, W - 2 * M, ah, 16, "#FCEDE9", z=2)
    rrect(M, ay, 10, ah, 5, CORAL, z=3)
    txt(M + 34, ay + 40, "MAS A PROVA REAL NÃO É SIMÉTRICA ASSIM", monoB, 13.5, CORALd, z=5)
    txt(M + 34, ay + (84 if story else 78), "Em 2025, chegar a 700 foi: top 0,4% em Linguagens · top 1,1% em", outfit, 20, INK, z=5)
    txt(M + 34, ay + (122 if story else 112), "Humanas e Natureza · top 10,4% em Matemática (a escala estica até 980).", outfit, 20, INK, z=5)

    # ---------- rodapé ----------
    fy = H - (220 if story else 106)
    txt(M, fy, "Curva = desenho da escala (referência ENEM 2009). Percentis reais: Microdados ENEM 2025 / INEP.",
        mono, 12, GRAY)
    fy = H - (160 if story else 52)
    xx = M
    for s, c in [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
        txt(xx, fy, s, outfitB, 17, c)
        xx += tw(s, outfitB, 17)
    txt(W - M, fy, "@xandaoxtri", monoB, 15, GRAY, ha="right")
    save(fig, nome)


build(1080, 1350, "post_curva_normal_feed")
build(1080, 1920, "post_curva_normal_story")
