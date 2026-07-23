#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Slides 16:9 + PDF — Redação ENEM: Salesiano São José (Natal) x Dom Bosco (Parnamirim), 2024->2025.
Competências C1-C5, evolução e leitura. Marca XTRI. Dados: dados.json (microdados INEP)."""
import json
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, style_axes, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, BG)
D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1920, 1080
M = 96
DB = CORAL      # Dom Bosco
SJ = CYANd      # São José
BR = "#9AA0A6"  # Brasil
dd = json.loads((D / "dados.json").read_text())
db, sj, br = dd["escolas"]["dom_bosco"], dd["escolas"]["sao_jose"], dd["brasil"]
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
    for cor, lab in [(DB, "Dom Bosco (Parnamirim)"), (SJ, "São José (Natal)"), (BR, "Brasil")]:
        ax.add_patch(Circle((x + 10, y - 7), 10, fc=cor, ec="none", zorder=6))
        txt(x + 30, y, lab, outfit, 17, INK, z=6)
        x += 30 + tw(lab, outfit, 17) + 46


# ---------- S1 capa ----------
def s1():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 150, 110, zoom=0.10)
    txt(W - M, 112, "ESTUDO XTRI · MICRODADOS INEP", monoB, 16, GRAY, ha="right", va="center")
    ty = 330
    txt(M, ty, "REDAÇÃO ENEM", outfitB, 88, INK)
    txt(M, ty + 96, "REDE SALESIANA · RN", outfitB, 88, CORAL)
    txt(M, ty + 170, "Salesiano São José (Natal)  ×  Salesiano Dom Bosco (Parnamirim)", outfit, 30, INK)
    txt(M, ty + 216, "Notas por competência (C1–C5) e evolução 2024 → 2025", outfit, 24, GRAY)
    # cartão-resumo
    py, ph = ty + 290, 190
    shadow(M, py, W - 2 * M, ph, 22); rrect(M, py, W - 2 * M, ph, 22, CARD, z=6); rrect(M, py, 12, ph, 6, CORAL, z=7)
    txt(M + 48, py + 62, "Em 2025, as duas unidades ficaram com redação média acima de 820 —", outfit, 24, INK, z=8)
    txt(M + 48, py + 100, "mais de 200 pontos acima do Brasil (618,7).", outfitB, 24, CORALd, z=8)
    txt(M + 48, py + 148, f"Dom Bosco: {vir(db['2025']['red'])} (n={db['2025']['n']})   ·   São José: {vir(sj['2025']['red'])} (n={sj['2025']['n']})", mono, 17, GRAY, z=8)
    foot(hp, "1/6")
    return save(fig, "s1_capa")


# ---------- S2 panorama 2025 ----------
def s2():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    head(hp, ax, "PANORAMA 2025", "Redação 2025 — onde as duas unidades estão",
         "Nota média de redação (válidas) e alunos na faixa 900+, ENEM 2025.")
    cards = [
        (DB, "SALESIANO DOM BOSCO", "Parnamirim/RN", db["2025"], db["2024"]),
        (SJ, "SALESIANO SÃO JOSÉ", "Natal/RN", sj["2025"], sj["2024"]),
    ]
    cw = (W - 2 * M - 60) / 2
    for k, (cor, nome, cidade, d25, d24) in enumerate(cards):
        x = M + k * (cw + 60); y = 330; ch = 460
        shadow(x, y, cw, ch, 22); rrect(x, y, cw, ch, 22, CARD, z=6); rrect(x, y, 12, ch, 6, cor, z=7)
        txt(x + 46, y + 66, nome, outfitB, 27, INK, z=8)
        txt(x + 46, y + 100, cidade, mono, 15, GRAY, z=8)
        txt(x + 46, y + 226, vir(d25["red"]), outfitB, 96, cor, z=8)
        txt(x + 46 + tw(vir(d25["red"]), outfitB, 96) + 18, y + 226, "de 1000", outfit, 22, GRAY, z=8)
        txt(x + 46, y + 286, f"{d25['n']} redações válidas · máxima {d25['max']}", outfit, 19, INK, z=8)
        p9 = 100 * d25["p900"] / d25["n"]
        txt(x + 46, y + 330, f"{d25['p900']} alunos com 900+  ({vir(p9, 0)}% da turma)", outfitB, 21, INK, z=8)
        txt(x + 46, y + 396, f"Brasil 2025: 618,7 · vantagem de {vir(d25['red'] - br['2025']['red'], 0)} pts", mono, 15, GRAY, z=8)
    txt(M, 860, "Leitura: em um ano de correção mais rigorosa no país inteiro, as duas unidades salesianas do RN", outfit, 21, INK)
    txt(M, 894, "seguem em outro patamar — a média de cada uma supera o Brasil em mais de 200 pontos.", outfit, 21, INK)
    foot(hp, "2/6")
    return save(fig, "s2_panorama")


# ---------- S3 competências 2025 ----------
def s3():
    fig, ax, hp = new_slide()
    txt = hp["txt"]
    head(hp, ax, "COMPETÊNCIAS 2025", "As 5 competências em 2025 — unidade por unidade",
         "Média em cada competência (0 a 200). Ao lado de cada grupo, a referência do Brasil.")
    legenda(hp, ax, M, 320)
    axc = fig.add_axes([M / W, 0.16, (W - 2 * M) / W, 0.52])
    import numpy as np
    xs = np.arange(5); bw = 0.26
    axc.bar(xs - bw, db["2025"]["comp"], bw, color=DB, zorder=3)
    axc.bar(xs, sj["2025"]["comp"], bw, color=SJ, zorder=3)
    axc.bar(xs + bw, br["2025"]["comp"], bw, color=BR, zorder=3)
    for i in range(5):
        axc.text(xs[i] - bw, db["2025"]["comp"][i] + 4, vir(db["2025"]["comp"][i], 0), ha="center", fontproperties=monoB, fontsize=13, color=CORALd)
        axc.text(xs[i], sj["2025"]["comp"][i] + 4, vir(sj["2025"]["comp"][i], 0), ha="center", fontproperties=monoB, fontsize=13, color=SJ)
        axc.text(xs[i] + bw, br["2025"]["comp"][i] + 4, vir(br["2025"]["comp"][i], 0), ha="center", fontproperties=mono, fontsize=12, color="#6B7076")
    axc.set_xticks(xs)
    axc.set_xticklabels([f"{c}\n{n}" for c, n in zip(COMPS, CNOME)], fontproperties=outfit, fontsize=14, color=INK)
    axc.set_ylim(0, 205); axc.set_yticks([0, 50, 100, 150, 200])
    style_axes(axc, "", "nota média (0–200)")
    foot(hp, "3/6", " · C1 norma culta · C2 compreensão · C3 argumentação · C4 coesão · C5 intervenção")
    return save(fig, "s3_competencias")


# ---------- S4 evolução total ----------
def s4():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    head(hp, ax, "EVOLUÇÃO 2024 → 2025", "O ano em que o Brasil caiu 40 pontos — e o Dom Bosco não",
         "Redação média 2024 x 2025. A correção nacional endureceu; veja quem segurou a nota.")
    series = [("Dom Bosco", DB, db), ("São José", SJ, sj), ("Brasil", BR, {"2024": br["2024"], "2025": br["2025"]})]
    axc = fig.add_axes([M / W, 0.17, 0.50, 0.50])
    import numpy as np
    xs = np.arange(3); bw = 0.33
    v24 = [s[2]["2024"]["red"] for s in series]; v25 = [s[2]["2025"]["red"] for s in series]
    axc.bar(xs - bw / 2, v24, bw, color=[s[1] for s in series], alpha=0.45, zorder=3)
    axc.bar(xs + bw / 2, v25, bw, color=[s[1] for s in series], zorder=3)
    for i in range(3):
        axc.text(xs[i] - bw / 2, v24[i] + 12, vir(v24[i], 0), ha="center", fontproperties=mono, fontsize=13, color="#6B7076")
        axc.text(xs[i] + bw / 2, v25[i] + 12, vir(v25[i], 0), ha="center", fontproperties=monoB, fontsize=14, color=INK)
    axc.set_xticks(xs); axc.set_xticklabels([s[0] for s in series], fontproperties=outfit, fontsize=16, color=INK)
    axc.set_ylim(0, 980); axc.set_yticks([0, 200, 400, 600, 800])
    style_axes(axc, "barra clara = 2024 · barra cheia = 2025", "redação média")
    # deltas à direita
    dx = M + (W - 2 * M) * 0.58; dy = 380
    deltas = [("Dom Bosco", DB, db["2025"]["red"] - db["2024"]["red"]),
              ("São José", SJ, sj["2025"]["red"] - sj["2024"]["red"]),
              ("Brasil", BR, br["2025"]["red"] - br["2024"]["red"])]
    txt(dx, dy - 46, "Variação 2024 → 2025", outfitB, 24, INK)
    for nome, cor, dl in deltas:
        rrect(dx, dy, W - M - dx, 110, 16, CARD, z=5)
        rrect(dx, dy, 10, 110, 5, cor, z=6)
        txt(dx + 36, dy + 68, nome, outfit, 22, INK, z=7)
        sinal = "+" if dl > 0 else "−"
        txt(W - M - 36, dy + 72, f"{sinal}{vir(abs(dl))}", outfitB, 40, (CORALd if abs(dl) < 10 else INK) if cor != BR else "#6B7076", ha="right", z=7)
        dy += 132
    txt(dx, dy + 26, "Dom Bosco: −2,2 num ano de −40,3 no país.", outfitB, 21, CORALd)
    txt(dx, dy + 60, "Em termos relativos, a unidade GANHOU terreno.", outfit, 19, INK)
    foot(hp, "4/6")
    return save(fig, "s4_evolucao")


# ---------- S5 evolução por competência ----------
def s5():
    fig, ax, hp = new_slide()
    txt = hp["txt"]
    head(hp, ax, "EVOLUÇÃO POR COMPETÊNCIA", "Onde cada unidade ganhou e perdeu (2024 → 2025)",
         "Variação da média em cada competência. Linha cinza = quanto o Brasil variou.")
    legenda(hp, ax, M, 320)
    axc = fig.add_axes([M / W, 0.16, (W - 2 * M) / W, 0.50])
    import numpy as np
    xs = np.arange(5); bw = 0.32
    d_db = [db["2025"]["comp"][i] - db["2024"]["comp"][i] for i in range(5)]
    d_sj = [sj["2025"]["comp"][i] - sj["2024"]["comp"][i] for i in range(5)]
    d_br = [br["2025"]["comp"][i] - br["2024"]["comp"][i] for i in range(5)]
    axc.axhline(0, color="#CFD2D5", lw=1.4, zorder=2)
    axc.bar(xs - bw / 2, d_db, bw, color=DB, zorder=3)
    axc.bar(xs + bw / 2, d_sj, bw, color=SJ, zorder=3)
    axc.plot(xs, d_br, "o--", color=BR, lw=2.2, ms=9, zorder=4)
    for i in range(5):
        va, off = ("bottom", 0.7) if d_db[i] >= 0 else ("top", -0.7)
        axc.text(xs[i] - bw / 2, d_db[i] + off, f"{'+' if d_db[i]>=0 else '−'}{vir(abs(d_db[i]))}", ha="center", va=va, fontproperties=monoB, fontsize=13, color=CORALd)
        va, off = ("bottom", 0.7) if d_sj[i] >= 0 else ("top", -0.7)
        axc.text(xs[i] + bw / 2, d_sj[i] + off, f"{'+' if d_sj[i]>=0 else '−'}{vir(abs(d_sj[i]))}", ha="center", va=va, fontproperties=monoB, fontsize=13, color=SJ)
    axc.set_xticks(xs)
    axc.set_xticklabels([f"{c}\n{n}" for c, n in zip(COMPS, CNOME)], fontproperties=outfit, fontsize=14, color=INK)
    axc.set_ylim(-24, 12)
    style_axes(axc, "", "variação 2024 → 2025 (pontos)")
    foot(hp, "5/6", " · destaque: C5 do Dom Bosco (+5,5) · queda comum em C2 (Brasil −15,5)")
    return save(fig, "s5_evolucao_comp")


# ---------- S6 síntese ----------
def s6():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    head(hp, ax, "SÍNTESE", "O que os dados dizem — e onde atacar em 2026",
         "Três leituras objetivas a partir dos microdados oficiais.")
    blocos = [
        (CORAL, "1 · Dom Bosco resistiu à correção dura",
         ["O país caiu 40,3 pontos; o Dom Bosco, só 2,2 — e a C5 (proposta de",
          "intervenção) ainda SUBIU 5,5. Em termos relativos, o melhor ano da unidade."]),
        (CYANd, "2 · São José: a queda veio quase toda da C2",
         ["Dos 39,7 pontos perdidos, 18,9 saíram da C2 (compreensão da proposta) —",
          "a mesma competência que derrubou o Brasil. Recuperá-la é o caminho mais curto."]),
        (INK, "3 · O teto comum das duas é a C1",
         ["Norma culta é a competência mais baixa das duas unidades (~148 de 200).",
          "É onde mora o próximo salto — inclusive para os alunos que já estão em 900+."]),
    ]
    y = 330
    for cor, tit, linhas in blocos:
        ch = 150
        shadow(M, y, W - 2 * M, ch, 18); rrect(M, y, W - 2 * M, ch, 18, CARD, z=6); rrect(M, y, 11, ch, 5, cor, z=7)
        txt(M + 44, y + 52, tit, outfitB, 25, INK, z=8)
        for k, ln in enumerate(linhas):
            txt(M + 44, y + 90 + k * 30, ln, outfit, 19, "#3A3A3D", z=8)
        y += ch + 26
    foot(hp, "6/6", " · análise XTRI · xtri.online")
    return save(fig, "s6_sintese")


if __name__ == "__main__":
    pngs = [s1(), s2(), s3(), s4(), s5(), s6()]
    imgs = [Image.open(p).convert("RGB") for p in pngs]
    pdf = D / "Redacao_Salesiano_RN_SaoJose_x_DomBosco.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=110)
    print("PDF:", pdf)
