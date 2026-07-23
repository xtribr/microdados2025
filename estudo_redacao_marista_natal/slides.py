#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Slides 16:9 + PDF — Redação ENEM: Marista de Natal x a REDE MARISTA (70 colégios), 2024->2025.
Mesmos parâmetros do estudo Salesiano RN (redações válidas, C1-C5, evolução). Marca XTRI."""
import json
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, style_axes, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)
D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1920, 1080
M = 96
NAT = CORAL      # Marista Natal
REDE = CYANd     # rede Marista
BR = "#9AA0A6"   # Brasil
dd = json.loads((D / "dados_maristas.json").read_text())
n25, n24 = dd["2025"]["natal"], dd["2024"]["natal"]
r25, r24 = dd["2025"]["rede"], dd["2024"]["rede"]
BRC = {"2024": {"comp": [126.2, 152.5, 124.5, 136.0, 119.8], "red": 659.0},
       "2025": {"comp": [120.6, 137.0, 119.6, 127.3, 114.2], "red": 618.7}}
COMPS = ["C1", "C2", "C3", "C4", "C5"]
CNOME = ["norma culta", "compreensão\nda proposta", "argumentação", "coesão", "proposta de\nintervenção"]


def vir(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def head(hp, ax, tag, titulo, sub):
    txt = hp["txt"]
    logo(ax, M + 150, 96, zoom=0.085)
    txt(W - M, 100, tag, monoB, 15, GRAY, ha="right", va="center")
    txt(M, 205, titulo, outfitB, 44, INK)
    txt(M, 252, sub, outfit, 21, GRAY)


def foot(hp, idx, extra=""):
    txt = hp["txt"]; tw = hp["tw"]
    y = H - 52
    txt(M, y - 28, f"Fonte: Microdados ENEM 2024 e 2025 / INEP · redações válidas (status \"Sem problemas\"){extra}", mono, 12, GRAY)
    xx = M
    for s, c in [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
        txt(xx, y + 4, s, outfitB, 15, c); xx += tw(s, outfitB, 15)
    txt(W - M, y + 4, f"@xandaoxtri · xtri.online   {idx}", monoB, 13, GRAY, ha="right")


def legenda(hp, ax, x, y):
    txt = hp["txt"]; tw = hp["tw"]
    from matplotlib.patches import Circle
    for cor, lab in [(NAT, "Marista de Natal"), (REDE, "rede Marista (70 colégios)"), (BR, "Brasil")]:
        ax.add_patch(Circle((x + 10, y - 7), 10, fc=cor, ec="none", zorder=6))
        txt(x + 30, y, lab, outfit, 17, INK, z=6)
        x += 30 + tw(lab, outfit, 17) + 46


# ---------- S1 capa ----------
def s1():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 150, 110, zoom=0.10)
    txt(W - M, 112, "ESTUDO XTRI · MICRODADOS INEP", monoB, 16, GRAY, ha="right", va="center")
    ty = 330
    txt(M, ty, "REDAÇÃO ENEM", outfitB, 88, INK)
    txt(M, ty + 96, "MARISTA DE NATAL × A REDE", outfitB, 88, CORAL)
    txt(M, ty + 170, "A redação do Colégio Marista de Natal comparada com os 70 colégios Maristas do Brasil", outfit, 30, INK)
    txt(M, ty + 216, "Notas por competência (C1–C5) e evolução 2024 → 2025", outfit, 24, GRAY)
    py, ph = ty + 290, 190
    shadow(M, py, W - 2 * M, ph, 22); rrect(M, py, W - 2 * M, ph, 22, CARD, z=6); rrect(M, py, 12, ph, 6, CORAL, z=7)
    txt(M + 48, py + 62, "Em 2025, o Marista de Natal é a REDAÇÃO Nº 1 da rede Marista no Brasil:", outfit, 24, INK, z=8)
    txt(M + 48, py + 100, f"{vir(n25['red'])} — subiu de 5º (2024) para 1º lugar entre os 70 colégios.", outfitB, 24, CORALd, z=8)
    txt(M + 48, py + 148, f"Natal: {vir(n25['red'])} (n={n25['n']})  ·  rede: {vir(r25['red'])} ({r25['escolas']} colégios, {r25['n']} redações)  ·  Brasil: 618,7", mono, 17, GRAY, z=8)
    foot(hp, "1/7")
    return save(fig, "s1_capa")


# ---------- S2 panorama ----------
def s2():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    head(hp, ax, "PANORAMA 2025", "Redação 2025 — Natal, a rede e o país",
         "Nota média de redação (válidas) no ENEM 2025.")
    cards = [
        (NAT, "MARISTA DE NATAL", "Natal/RN", vir(n25["red"]), f"{n25['n']} redações válidas",
         f"{n25['p900']} alunos com 900+  ({vir(100*n25['p900']/n25['n'],0)}% da turma)", "1º da rede Marista"),
        (REDE, "REDE MARISTA", "70 colégios · Brasil", vir(r25["red"]), f"{r25['n']} redações válidas",
         f"{r25['p900']} alunos com 900+  ({vir(100*r25['p900']/r25['n'],0)}%)", "referência da comparação"),
    ]
    cw = (W - 2 * M - 60) / 2
    for k, (cor, nome, cidade, red, l1, l2, l3) in enumerate(cards):
        x = M + k * (cw + 60); y = 330; ch = 460
        shadow(x, y, cw, ch, 22); rrect(x, y, cw, ch, 22, CARD, z=6); rrect(x, y, 12, ch, 6, cor, z=7)
        txt(x + 46, y + 66, nome, outfitB, 27, INK, z=8)
        txt(x + 46, y + 100, cidade, mono, 15, GRAY, z=8)
        txt(x + 46, y + 226, red, outfitB, 96, cor, z=8)
        txt(x + 46 + tw(red, outfitB, 96) + 18, y + 226, "de 1000", outfit, 22, GRAY, z=8)
        txt(x + 46, y + 286, l1, outfit, 19, INK, z=8)
        txt(x + 46, y + 330, l2, outfitB, 21, INK, z=8)
        txt(x + 46, y + 396, l3, mono, 15, GRAY, z=8)
    txt(M, 860, "Natal está 93 pontos acima da média da própria rede Marista — e 249 acima do Brasil (618,7).", outfit, 21, INK)
    txt(M, 894, "Quase metade da turma (44%) entregou redação de 900 ou mais.", outfit, 21, INK)
    foot(hp, "2/7")
    return save(fig, "s2_panorama")


# ---------- S3 competências ----------
def s3():
    fig, ax, hp = new_slide()
    txt = hp["txt"]
    head(hp, ax, "COMPETÊNCIAS 2025", "As 5 competências — Natal × rede × Brasil",
         "Média em cada competência (0 a 200), redações válidas de 2025.")
    legenda(hp, ax, M, 320)
    axc = fig.add_axes([M / W, 0.16, (W - 2 * M) / W, 0.52])
    import numpy as np
    xs = np.arange(5); bw = 0.26
    nat = [n25[f"c{i}"] for i in range(1, 6)]
    red = [r25[f"c{i}"] for i in range(1, 6)]
    br = BRC["2025"]["comp"]
    axc.bar(xs - bw, nat, bw, color=NAT, zorder=3)
    axc.bar(xs, red, bw, color=REDE, zorder=3)
    axc.bar(xs + bw, br, bw, color=BR, zorder=3)
    for i in range(5):
        axc.text(xs[i] - bw, nat[i] + 4, vir(nat[i], 0), ha="center", fontproperties=monoB, fontsize=13, color=CORALd)
        axc.text(xs[i], red[i] + 4, vir(red[i], 0), ha="center", fontproperties=monoB, fontsize=13, color=REDE)
        axc.text(xs[i] + bw, br[i] + 4, vir(br[i], 0), ha="center", fontproperties=mono, fontsize=12, color="#6B7076")
    axc.set_xticks(xs)
    axc.set_xticklabels([f"{c}\n{n}" for c, n in zip(COMPS, CNOME)], fontproperties=outfit, fontsize=14, color=INK)
    axc.set_ylim(0, 208); axc.set_yticks([0, 50, 100, 150, 200])
    style_axes(axc, "", "nota média (0–200)")
    foot(hp, "3/7", " · C5 de Natal: 190,2 — a mais alta da rede")
    return save(fig, "s3_competencias")


# ---------- S4 ranking da rede ----------
def s4():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; rrect = hp["rrect"]
    head(hp, ax, "RANKING DA REDE", "O top 10 da redação Marista no Brasil — 2025",
         "Nota média de redação (válidas) entre os 70 colégios Maristas (10 redações ou mais).")
    y = 320; rowh = 54
    twid = W - 2 * M
    cx = [M + 20, M + 110, M + twid * 0.55, M + twid * 0.70, M + twid * 0.80, M + twid - 20]
    rrect(M, y, twid, rowh - 8, 10, INK, z=2)
    for lab, xp, ha in [("#", cx[0], "left"), ("Colégio", cx[1], "left"), ("Cidade/UF", cx[2], "center"),
                        ("Redações", cx[3], "center"), ("900+", cx[4], "center"), ("Média", cx[5], "right")]:
        txt(xp, y + 30, lab, monoB, 15, "#FFFFFF", ha=ha)
    y += rowh
    p9 = {t["nome"]: None for t in dd["2025"]["top10"]}
    for k, t in enumerate(dd["2025"]["top10"]):
        hot = t["e_natal"]
        rrect(M, y, twid, rowh - 8, 9, "#FFF0EC" if hot else (CARD if k % 2 == 0 else "#F7F7F8"), z=2)
        if hot: rrect(M, y, 9, rowh - 8, 4, CORAL, z=3)
        txt(cx[0], y + 30, f"{t['pos']}º", outfitB if hot else mono, 17 if hot else 15, CORALd if hot else INK)
        txt(cx[1], y + 30, t["nome"][:44], outfitB if hot else outfit, 17 if hot else 16, INK)
        txt(cx[2], y + 30, f"{t['cid']}/{t['uf']}", mono, 13, GRAY, ha="center")
        txt(cx[3], y + 30, str(t["n"]), mono, 14, GRAY, ha="center")
        txt(cx[4], y + 30, f"{vir(100*n25['p900']/n25['n'],0)}%" if hot else "·", monoB if hot else mono, 13, CORALd if hot else GRAY, ha="center")
        txt(cx[5], y + 30, vir(t["red"]), outfitB, 19 if hot else 17, CORALd if hot else INK, ha="right")
        y += rowh
    foot(hp, "4/7", f" · Natal lidera com {vir(n25['red'] - dd['2025']['top10'][1]['red'])} pontos sobre o 2º colocado")
    return save(fig, "s4_ranking")


# ---------- S5 evolução total ----------
def s5():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; rrect = hp["rrect"]
    head(hp, ax, "EVOLUÇÃO 2024 → 2025", "O ano em que a rede caiu 33 pontos — e Natal virou o nº 1",
         "Redação média 2024 x 2025: Natal, rede Marista e Brasil.")
    series = [("Natal", NAT, n24["red"], n25["red"]), ("Rede Marista", REDE, r24["red"], r25["red"]),
              ("Brasil", BR, BRC["2024"]["red"], BRC["2025"]["red"])]
    axc = fig.add_axes([M / W, 0.17, 0.50, 0.50])
    import numpy as np
    xs = np.arange(3); bw = 0.33
    v24 = [s[2] for s in series]; v25 = [s[3] for s in series]
    axc.bar(xs - bw / 2, v24, bw, color=[s[1] for s in series], alpha=0.45, zorder=3)
    axc.bar(xs + bw / 2, v25, bw, color=[s[1] for s in series], zorder=3)
    for i in range(3):
        axc.text(xs[i] - bw / 2, v24[i] + 12, vir(v24[i], 0), ha="center", fontproperties=mono, fontsize=13, color="#6B7076")
        axc.text(xs[i] + bw / 2, v25[i] + 12, vir(v25[i], 0), ha="center", fontproperties=monoB, fontsize=14, color=INK)
    axc.set_xticks(xs); axc.set_xticklabels([s[0] for s in series], fontproperties=outfit, fontsize=16, color=INK)
    axc.set_ylim(0, 980); axc.set_yticks([0, 200, 400, 600, 800])
    style_axes(axc, "barra clara = 2024 · barra cheia = 2025", "redação média")
    dx = M + (W - 2 * M) * 0.58; dy = 380
    txt(dx, dy - 46, "Variação 2024 → 2025", outfitB, 24, INK)
    for nome, cor, a, b in series:
        dl = b - a
        rrect(dx, dy, W - M - dx, 100, 16, CARD, z=5); rrect(dx, dy, 10, 100, 5, cor, z=6)
        txt(dx + 36, dy + 62, nome, outfit, 22, INK, z=7)
        txt(W - M - 36, dy + 66, f"−{vir(abs(dl))}", outfitB, 38, CORALd if abs(dl) < 10 else ("#6B7076" if cor == BR else INK), ha="right", z=7)
        dy += 122
    txt(dx, dy + 22, "Natal: −7,5 · rede: −33,1 · Brasil: −40,3.", outfitB, 21, CORALd)
    txt(dx, dy + 56, "Segurando a nota, Natal saltou de 5º para 1º da rede.", outfit, 19, INK)
    foot(hp, "5/7")
    return save(fig, "s5_evolucao")


# ---------- S6 evolução por competência ----------
def s6():
    fig, ax, hp = new_slide()
    txt = hp["txt"]
    head(hp, ax, "EVOLUÇÃO POR COMPETÊNCIA", "Onde Natal ganhou da rede (2024 → 2025)",
         "Variação da média em cada competência. Linha cinza = variação do Brasil.")
    legenda(hp, ax, M, 320)
    axc = fig.add_axes([M / W, 0.16, (W - 2 * M) / W, 0.50])
    import numpy as np
    xs = np.arange(5); bw = 0.32
    d_nat = [n25[f"c{i}"] - n24[f"c{i}"] for i in range(1, 6)]
    d_red = [r25[f"c{i}"] - r24[f"c{i}"] for i in range(1, 6)]
    d_br = [BRC["2025"]["comp"][i] - BRC["2024"]["comp"][i] for i in range(5)]
    axc.axhline(0, color="#CFD2D5", lw=1.4, zorder=2)
    axc.bar(xs - bw / 2, d_nat, bw, color=NAT, zorder=3)
    axc.bar(xs + bw / 2, d_red, bw, color=REDE, zorder=3)
    axc.plot(xs, d_br, "o--", color=BR, lw=2.2, ms=9, zorder=4)
    for i in range(5):
        va, off = ("bottom", 0.6) if d_nat[i] >= 0 else ("top", -0.6)
        axc.text(xs[i] - bw / 2, d_nat[i] + off, f"{'+' if d_nat[i]>=0 else '−'}{vir(abs(d_nat[i]))}", ha="center", va=va, fontproperties=monoB, fontsize=13, color=CORALd)
        va, off = ("bottom", 0.6) if d_red[i] >= 0 else ("top", -0.6)
        axc.text(xs[i] + bw / 2, d_red[i] + off, f"{'+' if d_red[i]>=0 else '−'}{vir(abs(d_red[i]))}", ha="center", va=va, fontproperties=monoB, fontsize=13, color=REDE)
    axc.set_xticks(xs)
    axc.set_xticklabels([f"{c}\n{n}" for c, n in zip(COMPS, CNOME)], fontproperties=outfit, fontsize=14, color=INK)
    axc.set_ylim(-19, 9)
    style_axes(axc, "", "variação 2024 → 2025 (pontos)")
    foot(hp, "6/7", " · destaque: C5 de Natal (+5,9, chegando a 190,2) · C2 caiu em todo lugar")
    return save(fig, "s6_evolucao_comp")


# ---------- S7 síntese ----------
def s7():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    head(hp, ax, "SÍNTESE", "O que os dados dizem",
         "Três leituras objetivas a partir dos microdados oficiais.")
    blocos = [
        (CORAL, "1 · Natal virou a referência nacional da rede",
         ["Num ano em que a rede Marista caiu 33,1 pontos e o Brasil 40,3, Natal cedeu só 7,5 —",
          "e saltou de 5º para 1º lugar entre os 70 colégios Maristas do país."]),
        (CYANd, "2 · A C5 é a marca da casa",
         ["Proposta de intervenção em 190,2 (de 200), a mais alta da rede — e foi a competência",
          "que mais SUBIU (+5,9). 44% da turma entregou redação de 900 ou mais."]),
        (INK, "3 · O alvo de 2026 é o mesmo do país: C2 e C1",
         ["A C2 (compreensão da proposta) caiu 13,8 — movimento nacional (Brasil −15,5).",
          "E a C1 (norma culta, 154,5) segue como teto: é onde mora o próximo ganho."]),
    ]
    y = 330
    for cor, tit, linhas in blocos:
        ch = 150
        shadow(M, y, W - 2 * M, ch, 18); rrect(M, y, W - 2 * M, ch, 18, CARD, z=6); rrect(M, y, 11, ch, 5, cor, z=7)
        txt(M + 44, y + 52, tit, outfitB, 25, INK, z=8)
        for k, ln in enumerate(linhas):
            txt(M + 44, y + 90 + k * 30, ln, outfit, 19, "#3A3A3D", z=8)
        y += ch + 26
    foot(hp, "7/7", " · análise XTRI · xtri.online")
    return save(fig, "s7_sintese")


if __name__ == "__main__":
    pngs = [s1(), s2(), s3(), s4(), s5(), s6(), s7()]
    imgs = [Image.open(p).convert("RGB") for p in pngs]
    pdf = D / "Redacao_Marista_Natal_x_Rede_Marista.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=110)
    print("PDF:", pdf)
