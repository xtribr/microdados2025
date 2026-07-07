#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post IG — O EFEITO EDCLEY NO ENEM 2025: as 3 questões anuladas por vazamento.
Curvas reais das TRÊS questões (consenso dos fortes × faixa de nota na área da questão).
Feed 1080×1350 + Story 1080×1920. Dados: anulados_curvas.csv (Regular P1, ~3,18 mi respostas/item).
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W = 1080

# as 3 vazadas: co_item -> (rótulo, cor, alternativa-consenso)
ITENS = {
    "141774": ("Natureza · q1", "#FA5230", "E"),
    "141557": ("Natureza · q2", "#1FAFEF", "C"),
    "31350":  ("Matemática",    "#2EC4B6", "B"),
}
curvas = {ci: [] for ci in ITENS}
with (D.parent / "palestra_2025/anulados_curvas.csv").open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        ci = r["co_item"]
        if ci in ITENS and r["alt"] == ITENS[ci][2]:
            curvas[ci].append((float(r["banda_meio"]), float(r["pct"])))
for ci in curvas:
    curvas[ci].sort()
pisos = [c[1][1] for c in curvas.values()]
topos = [c[-1][1] for c in curvas.values()]


def vir0(x):
    return f"{x:.0f}%"


def make(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    story = H > 1400

    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · MICRODADOS", monoB, 13, GRAY, ha="right", va="center")
    ty = 186 if not story else 240
    txt(M, ty, "O EFEITO EDCLEY", outfitB, 54, CORAL)
    txt(M, ty + 56, "NO ENEM 2025", outfitB, 54, INK)
    txt(M, ty + 100, "3 questões anuladas por vazamento", outfitB, 24, GRAY)
    txt(M, ty + 148, "O INEP anulou 2 questões de Natureza e 1 de Matemática por “previamente", outfit, 17, GRAY)
    txt(M, ty + 176, "exposto” — e apagou o gabarito. Quem viu antes levou vantagem? Fui ver o rastro.", outfit, 17, GRAY)

    # ---- gráfico: as 3 curvas ----
    gy0 = ty + 232
    gh = 400 if not story else 500
    gx0, gx1 = M + 56, W - M - 150     # folga à direita p/ rótulos das linhas
    base = gy0 + gh

    def xx(nota):
        return gx0 + (nota - 325) / (825 - 325) * (gx1 - gx0)

    def yy(pct):
        return base - pct / 100 * gh

    for v in (0, 25, 50, 75, 100):
        ax.plot([gx0, W - M], [yy(v), yy(v)], color="#E2E3E5", lw=1, zorder=1)
        txt(gx0 - 12, yy(v), f"{v}%", mono, 11, GRAY, ha="right", va="center", z=3)
    ax.plot([gx0, W - M], [yy(20), yy(20)], color="#8C9298", lw=1.6, linestyle=(0, (4, 4)), zorder=2)
    txt(gx0 + 8, yy(20) + 20, "chute puro (20%)", mono, 11.5, GRAY, z=3)

    # curvas + rótulo no fim de cada linha (dodge simples)
    ends = []
    for ci, (rotulo, cor, alt) in ITENS.items():
        pts = curvas[ci]
        xs = [xx(n) for n, _ in pts]
        ys = [yy(p) for _, p in pts]
        ax.plot(xs, ys, color=cor, lw=4.2, zorder=4, solid_capstyle="round")
        ax.scatter(xs, ys, s=34, color=cor, zorder=5)
        ends.append([ys[-1], rotulo, cor, pts[-1][1]])
    ends.sort()
    for i in range(1, len(ends)):
        if ends[i][0] - ends[i - 1][0] < 44:
            ends[i][0] = ends[i - 1][0] + 44
    for ye, rotulo, cor, pct in ends:
        txt(gx1 + 14, ye - 6, vir0(pct), outfitB, 20, cor, z=6)
        txt(gx1 + 14, ye + 14, rotulo, mono, 10.5, GRAY, z=6)

    # callout do piso (zona vazia do alto-esquerdo; todas as curvas ficam < 40% até ~610)
    txt(gx0 + 40, yy(46), f"piso dos mais fracos: {vir0(min(pisos))} a {vir0(max(pisos))}",
        outfitB, 19, INK, z=6)
    txt(gx0 + 40, yy(40.5), "colado no chute — nas 3 questões", mono, 12, GRAY, z=6)

    for n in (400, 500, 600, 700, 800):
        txt(xx(n), base + 26, str(n), mono, 11.5, GRAY, ha="center", z=3)
    txt((gx0 + gx1) / 2, base + 54, "nota TRI do aluno na área da questão", outfit, 14.5, INK, ha="center", z=3)
    txt(M, gy0 - 16, "% QUE MARCOU A RESPOSTA-CONSENSO — AS 3 QUESTÕES VAZADAS", monoB, 12, INK, z=3)

    # ---- leitura ----
    ry = base + 84
    rh = 150
    rrect(M, ry, W - 2 * M, rh, 18, "#FCEDE9", z=3)
    rrect(M, ry, 10, rh, 5, CORAL, z=4)
    txt(M + 34, ry + 40, "Vazamento em massa deixa rastro: gente fraca acertando demais.", outfit, 18, INK, z=5)
    txt(M + 34, ry + 74, "Nas 3 curvas o rastro não existe — piso no chão, formato de item saudável.", outfit, 18, INK, z=5)
    txt(M + 34, ry + 116, "A anulação foi preventiva. E o custo foi de todos: 3 questões a menos.", outfitB, 18, CORALd, z=5)

    # ---- rodapé (nota + assinatura com respiro) ----
    fy = H - 116
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · Regular P1 · ~3,18 mi respostas por questão · motivo: 'Previamente exposto'",
        mono, 10, GRAY)
    txt(M, fy + 18, "gabarito apagado pelo INEP (X); 'resposta-consenso' = alternativa modal dos alunos de nota alta",
        mono, 10, GRAY)
    ay = H - 44
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx2 = M + tw("Transformamos ", outfitB, 15)
    txt(xx2, ay, "dados", outfitB, 15, CYAN); xx2 += tw("dados", outfitB, 15)
    txt(xx2, ay, " em ", outfitB, 15, INK); xx2 += tw(" em ", outfitB, 15)
    txt(xx2, ay, "aprovações", outfitB, 15, CORAL); xx2 += tw("aprovações", outfitB, 15)
    txt(xx2, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 12, GRAY, ha="right")
    return save(fig, f"xtri_anulados_{tag}")


if __name__ == "__main__":
    make(1350, "feed")
    make(1920, "story")
