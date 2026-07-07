#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infográfico: alunos que acertaram 12 questões, cada um com seu θ (TRI).
Base: recorte da planilha X-TRI (score=12). Mesmos 12 acertos, θ/nota diferentes —
porque a TRI olha QUAIS itens foram acertados, não o total. Dados reais do print (X-TRI).
"""
import matplotlib
matplotlib.use("Agg")
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

import xtri_deck as X
from xtri_deck import new_slide, logo, save, outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H

# Alunos reais com score=12 no recorte da planilha X-TRI (ordenados por nota).
ALUNOS = [
    {"theta": -0.89, "nota": 511.59, "tag": None},
    {"theta": -0.67, "nota": 534.24, "tag": "B"},
    {"theta": -0.33, "nota": 567.92, "tag": "A"},
    {"theta": -0.27, "nota": 573.31, "tag": None},
    {"theta":  0.05, "nota": 605.37, "tag": None},
]
SHIRTS = ["#1FAFEF", "#2FB9C4", "#F4B740", "#FB8155", "#FA5230"]  # frio→quente por nota
SKIN = "#E3AE7E"
PANTS = "#3A4A5A"


def vir(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def person(ax, hp, xc, floor_y, shirt, sign_lines, tag):
    rrect = hp["rrect"]; txt = hp["txt"]
    hip = floor_y - 92
    sh = hip - 100          # ombro
    head_c = sh - 32
    head_r = 28
    z = 5
    # pernas
    ax.plot([xc - 20, xc - 8], [floor_y, hip], color=PANTS, lw=14, solid_capstyle="round", zorder=z)
    ax.plot([xc + 20, xc + 8], [floor_y, hip], color=PANTS, lw=14, solid_capstyle="round", zorder=z)
    # tronco
    rrect(xc - 30, sh, 60, hip - sh, 18, shirt, z=z + 1)
    # cabeça
    ax.add_patch(Circle((xc, head_c), head_r, fc=SKIN, ec="none", zorder=z + 2))
    # placa (acima da cabeça)
    sign_w, sign_h = 258, 132
    sign_by = head_c - head_r - 30      # base da placa (menor y = mais alto)
    sign_ty = sign_by - sign_h
    # braços seguram um bastão central até a placa
    ax.plot([xc, xc], [sh + 22, sign_by], color="#B8895A", lw=7, solid_capstyle="round", zorder=z + 1)
    ax.plot([xc - 26, xc], [sh + 8, sh + 20], color=shirt, lw=13, solid_capstyle="round", zorder=z + 3)
    ax.plot([xc + 26, xc], [sh + 8, sh + 20], color=shirt, lw=13, solid_capstyle="round", zorder=z + 3)
    # placa
    hp["shadow"](xc - sign_w / 2, sign_ty, sign_w, sign_h, 16)
    rrect(xc - sign_w / 2, sign_ty, sign_w, sign_h, 16, CARD, z=z + 4, ec=shirt, lw=3)
    txt(xc, sign_ty + 40, sign_lines[0], outfitB, 27, INK, ha="center", va="center", z=z + 5)
    ax.plot([xc - sign_w / 2 + 26, xc + sign_w / 2 - 26], [sign_ty + 62, sign_ty + 62],
            color="#E6E7E9", lw=1.4, zorder=z + 5)
    txt(xc, sign_ty + 84, sign_lines[1], monoB, 21, shirt, ha="center", va="center", z=z + 5)
    txt(xc, sign_ty + 112, sign_lines[2], mono, 15, GRAY, ha="center", va="center", z=z + 5)
    # etiqueta de aluno (piso)
    if tag:
        rrect(xc - 52, floor_y + 20, 104, 40, 12, INK, z=z + 2)
        txt(xc, floor_y + 40, f"ALUNO {tag}", monoB, 14, "#FFFFFF", ha="center", va="center", z=z + 3)


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 70

    # título
    txt(M, 84, "Mesmos 12 acertos, ", outfitB, 40, INK)
    txt(M + tw("Mesmos 12 acertos, ", outfitB, 40), 84, "thetas diferentes", outfitB, 40, CORAL)
    txt(M, 128, "Cinco alunos acertaram exatamente 12 questões — mas a TRI deu a cada um um theta (proficiência) "
                "diferente, conforme QUAIS itens acertaram.", outfit, 17, GRAY)

    # callout do delta
    notas = [a["nota"] for a in ALUNOS]
    dlt = max(notas) - min(notas)
    cw = 560
    rrect(W - M - cw, 150, cw, 74, 16, "#FCEDE9", z=3)
    rrect(W - M - cw, 150, 10, 74, 5, CORAL, z=4)
    txt(W - M - cw + 34, 180, f"Nota de {vir(min(notas))} a {vir(max(notas))}", outfitB, 20, CORALd, va="center")
    txt(W - M - cw + 34, 208, f"Δ {vir(dlt, 1)} pontos com o MESMO nº de acertos", mono, 13.5, INK, va="center")

    # eixo de nota (referência das barras)
    floor_y = 858
    ky = 2.55
    n0 = 490

    def yn(n):
        return floor_y - (n - n0) * ky

    for n in (500, 550, 600):
        ax.plot([M + 8, W - M], [yn(n), yn(n)], color="#E2E3E5", lw=1.1, zorder=1)
        txt(M - 4, yn(n), f"{n}", mono, 12, GRAY, ha="right", va="center", z=2)
    txt(M - 4, yn(620), "nota", mono, 12, GRAY, ha="right", va="center", z=2)

    # piso
    ax.plot([M, W - M], [floor_y, floor_y], color="#C9CBCE", lw=2, zorder=2)

    xs = [323, 669, 1015, 1361, 1707]
    for i, a in enumerate(ALUNOS):
        xc = xs[i]; shirt = SHIRTS[i]
        # barra de nota atrás
        bh = floor_y - yn(a["nota"])
        ax.add_patch(FancyBboxPatch((xc - 48, yn(a["nota"])), 96, bh, boxstyle="round,pad=0",
                                    fc=shirt, ec="none", alpha=0.16, zorder=1))
        person(ax, hp, xc, floor_y, shirt,
               ["12 acertos", f"θ = {vir(a['theta'])}", f"nota {vir(a['nota'])}"], a["tag"])

    # rodapé
    txt(M, H - 92, "A TRI não conta acertos — pesa QUAIS itens. Acertar itens mais discriminativos eleva o theta; "
        "acertar só os fáceis (ou chutar) mantém o theta baixo, mesmo com o mesmo total.", outfit, 15, INK)
    # fonte X-TRI (estilo do print)
    rrect(M, H - 60, 190, 40, 10, "#FFD400", z=4)
    txt(M + 95, H - 40, "FONTE: X-TRI", monoB, 15, INK, ha="center", va="center", z=5)
    txt(W - M, H - 40, "Recorte da planilha X-TRI (simulado) · θ e nota por padrão de respostas",
        mono, 11.5, GRAY, ha="right", va="center")
    logo(ax, W - M - 4, H - 108, zoom=0.06)
    return save(fig, "infografico_12acertos")


if __name__ == "__main__":
    main()
