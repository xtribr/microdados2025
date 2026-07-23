#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dossiê A4 (8 págs) — Colégio Marista Nossa Senhora de Nazaré (Belém/PA).
TRI por área, histórico 2024->2025, redação C1-C5, rankings, raio-X item a item (COP30) e metodologia.
Marca XTRI. Dados: dossie_dados.json (microdados INEP 2024/2025, aplicação COP30/BAM)."""
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib.image as mpimg

sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
from xtri_deck import outfitB, outfit, mono, monoB, LOGO
INK = "#1D1D20"; GRAY = "#8C9298"; BG = "#F1F1F2"; CARD = "#FFFFFF"
CORAL = "#FA5230"; CORALd = "#E8431F"; CYAN = "#1FAFEF"; CYANd = "#1597D8"
VERDE = "#1E8449"; LINE = "#E2E3E6"; COOP = "#B9BEC4"; BRc = "#6B7076"

D = Path(__file__).resolve().parent
dd = json.loads((D / "dossie_dados.json").read_text())
AR = ["LC", "CH", "CN", "MT"]
ARN = {"LC": "Linguagens", "CH": "Humanas", "CN": "Natureza", "MT": "Matemática"}


def vir(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


W, H = 595, 842; M = 46
PAGES = "8"


def page(pdf, draw, tag):
    fig = plt.figure(figsize=(W / 72, H / 72), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))

    def tw(s, fp, sz):
        t = ax.text(0, 0, s, fontproperties=fp, fontsize=sz); fig.canvas.draw()
        wd = t.get_window_extent(fig.canvas.get_renderer()).width / (fig.dpi / 72); t.remove(); return wd

    def txt(x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
        return ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

    def rrect(x, y, ww, hh, rad, fc, z=2, ec="none", lw=0):
        ax.add_patch(FancyBboxPatch((x + rad, y + rad), ww - 2 * rad, hh - 2 * rad, boxstyle=f"round,pad={rad}", fc=fc, ec=ec, lw=lw, zorder=z))

    def line(x1, y, x2, c=LINE, lw=1.0):
        ax.plot([x1, x2], [y, y], color=c, lw=lw, zorder=3, solid_capstyle="round")

    def logo_(x, y, zoom=0.045):
        try:
            ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=zoom), (x, y), frameon=False, box_alignment=(0, 0.5), zorder=8))
        except Exception:
            pass

    def sig(y):
        xx = M
        for s, c in [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
            txt(xx, y, s, outfitB, 9.5, c); xx += tw(s, outfitB, 9.5)
        txt(W - M, y, "@xandaoxtri · xtri.online", mono, 7.5, GRAY, ha="right")

    hp = dict(ax=ax, fig=fig, txt=txt, tw=tw, rrect=rrect, line=line, sig=sig)
    logo_(M, 64, 0.045); txt(W - M, 66, tag, mono, 7.5, GRAY, ha="right", va="center"); line(M, 92, W - M)
    draw(hp)
    fig.savefig(str(D / f"_dp_{draw.__name__}.png"), dpi=150, facecolor=BG)
    pdf.savefig(fig, facecolor=BG); plt.close(fig)


def footer(hp, nota, pg):
    hp["line"](M, H - 96, W - M)
    hp["txt"](M, H - 74, nota, mono, 7.5, GRAY)
    hp["sig"](H - 46)
    hp["txt"](W - M, H - 28, f"{pg} / {PAGES}", mono, 7.5, GRAY, ha="right")


FONTE = "Fonte: Microdados ENEM 2024 e 2025 / INEP · aplicação COP30/BAM em 2025 · notas TRI em escala equalizada."


# ---------- p1 capa ----------
def p1_capa(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 148, "Dossiê ENEM", outfitB, 30, INK)
    txt(M, 186, "Colégio Marista Nossa Senhora de Nazaré", outfitB, 19, CORALd)
    txt(M, 208, "Belém/PA · rede privada · aplicação COP30/BAM em 2025", outfit, 11.5, GRAY)
    # hero
    rrect(M, 236, W - 2 * M, 112, 12, CARD, z=2); rrect(M, 236, 7, 112, 3.5, CORAL, z=3)
    txt(M + 26, 268, "MÉDIA GERAL 2025 (5 NOTAS)", mono, 8.5, GRAY)
    txt(M + 26, 322, vir(dd["tri2025"]["M5"]), outfitB, 42, CORAL)
    txt(M + 26 + 136, 322, "pontos", outfit, 12, GRAY)
    txt(W - M - 26, 286, "REDAÇÃO 830,6", outfitB, 14, CYANd, ha="right")
    txt(W - M - 26, 308, f"{dd['tri2025']['concluintes']} concluintes · {dd['red2025']['n']} redações válidas", mono, 8, GRAY, ha="right")
    txt(W - M - 26, 328, "evolução de +3,5 na média vs 2024", mono, 8, GRAY, ha="right")
    # mini-cards
    cw = (W - 2 * M - 2 * 14) / 3; y0 = 372
    minis = [("7º", "de 163", "em Belém"), ("10º", "de 850", "no Pará"), ("+34,7", "em Natureza", "maior salto 24 a 25")]
    for i, (a, b, c) in enumerate(minis):
        x = M + i * (cw + 14)
        rrect(x, y0, cw, 86, 10, CARD, z=2)
        txt(x + cw / 2, y0 + 40, a, outfitB, 26, INK, ha="center")
        txt(x + cw / 2, y0 + 57, b, mono, 8.5, GRAY, ha="center")
        txt(x + cw / 2, y0 + 74, c, outfit, 9.5, INK, ha="center")
    txt(M, 500, "O que este dossiê contém", outfitB, 13, INK)
    itens = ["Notas TRI 2025 por área — escola × coorte COP30 × Brasil",
             "Histórico 2024 → 2025 (áreas, média e ranking)",
             "Redação por competência (C1–C5) e sua evolução",
             "Posição nos rankings de Belém e do Pará",
             "Raio-X TRI item a item: dificuldade, discriminação e habilidades",
             "Metodologia e contexto da aplicação COP30"]
    yy = 526
    for it in itens:
        rrect(M, yy - 7, 6, 6, 2, CYANd, z=3)
        txt(M + 16, yy, it, outfit, 10.5, "#3A3A3D"); yy += 22
    footer(hp, FONTE, "1")


# ---------- p2 TRI 2025 ----------
def p2_tri(hp):
    txt = hp["txt"]
    txt(M, 132, "Notas TRI 2025 — em outro patamar", outfitB, 17, INK)
    txt(M, 152, "Média da escola em cada área, contra a coorte COP30 (mesma prova) e o Brasil (P1 regular).", outfit, 10.5, GRAY)
    axc = hp["fig"].add_axes([M / W, 0.36, (W - 2 * M) / W, 0.36])
    import numpy as np
    xs = np.arange(4); bw = 0.27
    esc = [dd["tri2025"][a] for a in AR]; co = [dd["coorte_cop30"][a] for a in AR]; br = [dd["br2025_p1"][a] for a in AR]
    axc.bar(xs - bw, esc, bw, color=CORAL, zorder=3, label="Marista Nazaré")
    axc.bar(xs, co, bw, color=COOP, zorder=3, label="coorte COP30")
    axc.bar(xs + bw, br, bw, color=BRc, zorder=3, label="Brasil P1")
    for i in range(4):
        axc.text(xs[i] - bw, esc[i] + 8, vir(esc[i], 0), ha="center", fontproperties=monoB, fontsize=7.5, color=CORALd)
        axc.text(xs[i], co[i] + 8, vir(co[i], 0), ha="center", fontproperties=mono, fontsize=6.5, color="#6B7076")
        axc.text(xs[i] + bw, br[i] + 8, vir(br[i], 0), ha="center", fontproperties=mono, fontsize=6.5, color="#4A4E52")
    axc.set_xticks(xs); axc.set_xticklabels([ARN[a] for a in AR], fontproperties=outfit, fontsize=9, color=INK)
    axc.set_ylim(0, 740); axc.set_yticks([0, 200, 400, 600])
    for lab in axc.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(7); lab.set_color(GRAY)
    for s in ["top", "right", "left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_color("#CFD2D5"); axc.tick_params(length=0)
    axc.grid(axis="y", color="#ECEDEF", lw=0.7); axc.set_axisbelow(True)
    axc.legend(prop=outfit, fontsize=7.5, loc="upper left", frameon=False, ncol=3, bbox_to_anchor=(0, 1.12))
    y = 610
    txt(M, y, "Leitura", outfitB, 12, INK); y += 18
    for ln in [f"• A escola supera a coorte COP30 em TODAS as áreas — a maior folga é em Matemática ({vir(dd['tri2025']['MT'],0)} × {vir(dd['coorte_cop30']['MT'],0)}, +186).",
               "• Contra o Brasil da prova regular, a vantagem vai de 64 (LC) a 149 pontos (MT) — a escala TRI é equalizada",
               "  entre aplicações, então a comparação é legítima.",
               "• Matemática é o carro-chefe (669,7); Natureza, após o salto de 2025, deixou de ser o ponto fraco."]:
        txt(M, y, ln, outfit, 9.5, "#3A3A3D"); y += 16
    footer(hp, FONTE, "2")


# ---------- p3 histórico TRI ----------
def p3_hist(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 132, "Histórico 2024 → 2025 — o salto de Natureza", outfitB, 17, INK)
    txt(M, 152, "Prova regular em 2024; aplicação COP30 em 2025. Notas TRI comparáveis (escala equalizada).", outfit, 10.5, GRAY)
    axc = hp["fig"].add_axes([M / W, 0.40, (W - 2 * M) / W, 0.32])
    import numpy as np
    xs = np.arange(5); bw = 0.34
    lab5 = AR + ["M5"]
    v24 = [dd["tri2024"][a] for a in AR] + [dd["tri2024"]["M5"]]
    v25 = [dd["tri2025"][a] for a in AR] + [dd["tri2025"]["M5"]]
    axc.bar(xs - bw / 2, v24, bw, color="#F5B5A5", zorder=3, label="2024")
    axc.bar(xs + bw / 2, v25, bw, color=CORAL, zorder=3, label="2025")
    for i in range(5):
        axc.text(xs[i] - bw / 2, v24[i] + 8, vir(v24[i], 0), ha="center", fontproperties=mono, fontsize=6.5, color="#8C6A5E")
        axc.text(xs[i] + bw / 2, v25[i] + 8, vir(v25[i], 0), ha="center", fontproperties=monoB, fontsize=7, color=CORALd)
    axc.set_xticks(xs)
    axc.set_xticklabels([ARN[a] for a in AR] + ["Média 5"], fontproperties=outfit, fontsize=9, color=INK)
    axc.set_ylim(0, 760); axc.set_yticks([0, 200, 400, 600])
    for lab in axc.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(7); lab.set_color(GRAY)
    for s in ["top", "right", "left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_color("#CFD2D5"); axc.tick_params(length=0)
    axc.grid(axis="y", color="#ECEDEF", lw=0.7); axc.set_axisbelow(True)
    axc.legend(prop=outfit, fontsize=7.5, loc="upper left", frameon=False, ncol=2, bbox_to_anchor=(0, 1.12))
    # tabela deltas
    y = 548
    txt(M, y, "Variação da escola × variação do Brasil", outfitB, 12, INK); y += 14
    cols = ["", "LC", "CH", "CN", "MT"]
    dE = [dd["tri2025"][a] - dd["tri2024"][a] for a in AR]
    dB = [dd["br2025_p1"][a] - dd["br2024"][a] for a in AR]
    cx = [M + 8, M + 170, M + 260, M + 350, M + 440]
    rrect(M, y, W - 2 * M, 26, 5, INK, z=2)
    for j, c in enumerate(cols):
        txt(cx[j], y + 17, c if c else "Δ 2024 → 2025", monoB, 8, "#FFFFFF", ha="left" if j == 0 else "center")
    y += 26
    for nome, vals, hot in [("Marista Nazaré", dE, True), ("Brasil", dB, False)]:
        rrect(M, y, W - 2 * M, 26, 5, CARD if hot else "#F7F7F8", z=2)
        txt(cx[0], y + 17, nome, outfitB if hot else outfit, 9, INK)
        for j, v in enumerate(vals, 1):
            s = f"+{vir(v)}" if v >= 0 else f"−{vir(abs(v))}"
            cor = (VERDE if v > 5 else (CORALd if v < -5 else INK)) if hot else "#6B7076"
            txt(cx[j], y + 17, s, outfitB if hot else mono, 9 if hot else 8, cor, ha="center")
        y += 26
    y += 22
    for ln in ["• Natureza: +34,7 na escola contra +6,7 no Brasil — um ganho real de 28 pontos sobre o país, o maior avanço do ciclo.",
               "• Linguagens acompanhou (+14,5 × +8,9). Humanas e Matemática ficaram estáveis em nível já alto.",
               "• A média das 5 notas subiu (+3,5) mesmo num ano de prova nova (COP30) — e o ranking se manteve: 7º de Belém nos 2 anos."]:
        txt(M, y, ln, outfit, 9.5, "#3A3A3D"); y += 16
    footer(hp, FONTE, "3")


# ---------- p4 redação 2025 ----------
def p4_red(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 132, "Redação 2025 — 830,6, com C5 de elite", outfitB, 17, INK)
    txt(M, 152, "Competências C1–C5 (0 a 200) contra a coorte COP30 (mesma prova e mesmo tema).", outfit, 10.5, GRAY)
    axc = hp["fig"].add_axes([M / W, 0.40, (W - 2 * M) / W, 0.32])
    import numpy as np
    xs = np.arange(5); bw = 0.36
    esc = dd["red2025"]["comp"]; co = dd["red_coorte_comp"]
    axc.bar(xs - bw / 2, esc, bw, color=CYANd, zorder=3, label="Marista Nazaré")
    axc.bar(xs + bw / 2, co, bw, color=COOP, zorder=3, label="coorte COP30")
    for i in range(5):
        axc.text(xs[i] - bw / 2, esc[i] + 3, vir(esc[i], 0), ha="center", fontproperties=monoB, fontsize=7.5, color=CYANd)
        axc.text(xs[i] + bw / 2, co[i] + 3, vir(co[i], 0), ha="center", fontproperties=mono, fontsize=6.5, color="#6B7076")
    axc.set_xticks(xs)
    axc.set_xticklabels(["C1\nnorma culta", "C2\ncompreensão", "C3\nargumentação", "C4\ncoesão", "C5\nintervenção"], fontproperties=outfit, fontsize=8, color=INK)
    axc.set_ylim(0, 205); axc.set_yticks([0, 50, 100, 150, 200])
    for lab in axc.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(7); lab.set_color(GRAY)
    for s in ["top", "right", "left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_color("#CFD2D5"); axc.tick_params(length=0)
    axc.grid(axis="y", color="#ECEDEF", lw=0.7); axc.set_axisbelow(True)
    axc.legend(prop=outfit, fontsize=7.5, loc="upper left", frameon=False, ncol=2, bbox_to_anchor=(0, 1.12))
    y = 548
    rrect(M, y, W - 2 * M, 74, 10, "#E8F6FE", z=2)
    txt(M + 22, y + 26, "Destaque: C5 (proposta de intervenção)", outfitB, 11.5, CYANd)
    txt(M + 22, y + 46, "59% da turma tirou nota MÁXIMA (200) na C5 — na coorte COP30, só 13%. Média 181,2 × 111,4.", outfit, 9.5, INK)
    txt(M + 22, y + 62, "É a marca registrada da escola na redação.", outfit, 9.5, INK)
    y += 96
    for ln in ["• Todas as competências ficam 29 a 70 pontos acima da coorte; a maior distância é justamente a C5 (+69,8).",
               "• O teto a atacar é a C1 (norma culta, 147,7) — padrão que se repete nas escolas fortes do país.",
               f"• Média geral: {vir(dd['red2025']['media'])} contra {vir(dd['coorte_cop30']['red'])} da coorte (+221)."]:
        txt(M, y, ln, outfit, 9.5, "#3A3A3D"); y += 16
    footer(hp, "Fonte: Microdados ENEM 2025 / INEP · coorte COP30: mesma prova e mesmo tema de redação da escola.", "4")


# ---------- p5 redação histórico ----------
def p5_red_hist(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 132, "Redação 2024 → 2025 — leitura honesta da queda", outfitB, 17, INK)
    txt(M, 152, "A média caiu 40,1 pontos — praticamente o mesmo que o Brasil inteiro (−40,3), num ano de correção mais dura.", outfit, 10.5, GRAY)
    # totais
    y = 186
    cards = [("Marista Nazaré", dd["red2024"]["media"], dd["red2025"]["media"], CORAL),
             ("Brasil (válidas)", dd["br_red"]["2024"], dd["br_red"]["2025"], "#9AA0A6")]
    cw = (W - 2 * M - 16) / 2
    for k, (nome, a24, a25, cor) in enumerate(cards):
        x = M + k * (cw + 16)
        rrect(x, y, cw, 96, 10, CARD, z=2); rrect(x, y, 6, 96, 3, cor, z=3)
        txt(x + 20, y + 26, nome, outfitB, 11.5, INK)
        txt(x + 20, y + 62, f"{vir(a24)} → {vir(a25)}", outfitB, 20, INK)
        d = a25 - a24
        txt(x + 20, y + 84, f"variação: −{vir(abs(d))}", monoB, 9.5, CORALd if k == 0 else "#6B7076")
    # deltas C1-C5
    y = 316
    txt(M, y, "Variação por competência (escola)", outfitB, 12, INK); y += 10
    axc = hp["fig"].add_axes([M / W, 0.40, (W - 2 * M) / W, 0.17])
    import numpy as np
    xs = np.arange(5)
    dc = [dd["red2025"]["comp"][i] - dd["red2024"]["comp"][i] for i in range(5)]
    cores = [CORALd if v < -8 else ("#F5B5A5" if v < 0 else VERDE) for v in dc]
    axc.axhline(0, color="#CFD2D5", lw=1.2, zorder=2)
    axc.bar(xs, dc, 0.5, color=cores, zorder=3)
    for i, v in enumerate(dc):
        axc.text(xs[i], v - 1.6 if v < 0 else v + 0.6, f"−{vir(abs(v))}" if v < 0 else f"+{vir(v)}",
                 ha="center", va="top" if v < 0 else "bottom", fontproperties=monoB, fontsize=7.5, color=INK)
    axc.set_xticks(xs); axc.set_xticklabels(["C1", "C2", "C3", "C4", "C5"], fontproperties=outfit, fontsize=9, color=INK)
    axc.set_ylim(-20, 5); axc.set_yticks([])
    for s in ["top", "right", "left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_visible(False); axc.tick_params(length=0)
    y = 542
    for ln in ["• A queda concentra-se na C2 (−16,1) — exatamente a competência que derrubou o Brasil (−15,5 no país).",
               "• C5 quase não cedeu (−2,4) e segue 70 pontos acima da coorte: o diferencial da escola resistiu.",
               "• Em 2024, 62 de 135 alunos (46%) fizeram 900+ na redação; em 2025, com a régua nacional mais dura,",
               "  a média de 830,6 ainda deixa a escola 221 pontos acima da própria coorte.",
               "• Conclusão: a queda é do ciclo de correção nacional, não um problema da unidade. O alvo de 2026 é C2 e C1."]:
        txt(M, y, ln, outfit, 9.5, "#3A3A3D"); y += 16
    footer(hp, FONTE, "5")


# ---------- p6 rankings ----------
def p6_rank(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 132, "Posição nos rankings — Belém e Pará", outfitB, 17, INK)
    txt(M, 152, "Colocação por média das 5 notas (escolas com 10 alunos ou mais), ENEM 2025.", outfit, 10.5, GRAY)
    y = 184; rowh = 30
    cols = ["Recorte", "Média 5", "LC", "CH", "CN", "MT", "Redação"]
    twid = W - 2 * M
    cx = [M + 8, M + twid * 0.44, M + twid * 0.55, M + twid * 0.64, M + twid * 0.73, M + twid * 0.82, M + twid * 0.92]
    rrect(M, y, twid, rowh, 5, INK, z=2)
    for j, c in enumerate(cols):
        txt(cx[j], y + rowh / 2 + 1, c, monoB, 8, "#FFFFFF", va="center", ha="left" if j == 0 else "center")
    y += rowh
    ra = dd["rank2025"]
    linhas = [
        (f"Belém ({ra['belem'][1]} escolas)", ra["belem"][0], ra["por_area_belem"]),
        (f"Belém — privadas ({ra['belem_priv'][1]})", ra["belem_priv"][0], None),
        (f"Pará ({ra['pa'][1]} escolas)", ra["pa"][0], ra["por_area_pa"]),
        (f"Pará — privadas ({ra['pa_priv'][1]})", ra["pa_priv"][0], None),
    ]
    for k, (nome, m5, pa) in enumerate(linhas):
        rrect(M, y, twid, rowh, 5, CARD if k % 2 == 0 else "#F7F7F8", z=2)
        txt(cx[0], y + rowh / 2 + 1, nome, outfit, 9, INK, va="center")
        txt(cx[1], y + rowh / 2 + 1, f"{m5}º", outfitB, 10.5, CORALd, va="center", ha="center")
        if pa:
            for j, a in enumerate(["LC", "CH", "CN", "MT", "RED"], 2):
                txt(cx[j], y + rowh / 2 + 1, f"{pa[a]}º", outfit, 9, INK, va="center", ha="center")
        else:
            for j in range(2, 7):
                txt(cx[j], y + rowh / 2 + 1, "·", mono, 9, GRAY, va="center", ha="center")
        y += rowh
    # evolução de posição
    y += 26
    rrect(M, y, W - 2 * M, 84, 10, CARD, z=2); rrect(M, y, 6, 84, 3, CORAL, z=3)
    txt(M + 22, y + 26, "Evolução da posição em Belém", outfitB, 11.5, INK)
    txt(M + 22, y + 50, f"2024: 7º de {dd['rank2024_belem'][1]}   →   2025: 7º de {ra['belem'][1]}", outfitB, 13, INK)
    txt(M + 22, y + 70, "Estável no top 10 da capital nos dois anos — com melhora absoluta da média (657,7 → 661,2).", outfit, 9.5, "#3A3A3D")
    y += 112
    for ln in ["• Em Matemática, a escola é 6ª de Belém e 9ª do Pará inteiro — a melhor colocação entre as áreas.",
               "• Na redação, o 8º lugar de Belém reflete a força local: a capital concentra escolas de redação altíssima.",
               "• Entre as privadas do Pará, é top 10 em tudo, com 9º na média geral."]:
        txt(M, y, ln, outfit, 9.5, "#3A3A3D"); y += 16
    footer(hp, "Fonte: Microdados ENEM 2025 / INEP · ranking por média dos presentes nos 2 dias com 5 notas · N mínimo 10.", "6")


# ---------- p7 raio-X TRI ----------
def p7_tri_itens(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 132, "Raio-X TRI item a item (prova COP30)", outfitB, 17, INK)
    txt(M, 152, "Acerto da escola × coorte COP30 por categoria de dificuldade, discriminação e habilidades.", outfit, 10.5, GRAY)
    # categorias
    y = 182
    txt(M, y, "Acerto por dificuldade do item (média das 4 áreas)", outfitB, 11.5, INK); y += 12
    import numpy as np
    cats = ["Fácil", "Médio", "Difícil", "Muito difícil"]
    esc = [np.mean([p[0] for p in dd["categorias"][c]]) for c in cats]
    co = [np.mean([p[1] for p in dd["categorias"][c]]) for c in cats]
    axc = hp["fig"].add_axes([M / W, 0.615, (W - 2 * M) / W, 0.135])
    xs = np.arange(4); bw = 0.36
    axc.bar(xs - bw / 2, esc, bw, color=CORAL, zorder=3)
    axc.bar(xs + bw / 2, co, bw, color=COOP, zorder=3)
    for i in range(4):
        axc.text(xs[i] - bw / 2, esc[i] + 1.5, f"{vir(esc[i],0)}%", ha="center", fontproperties=monoB, fontsize=7, color=CORALd)
        axc.text(xs[i] + bw / 2, co[i] + 1.5, f"{vir(co[i],0)}%", ha="center", fontproperties=mono, fontsize=6.5, color="#6B7076")
    axc.set_xticks(xs); axc.set_xticklabels(cats, fontproperties=outfit, fontsize=8.5, color=INK)
    axc.set_ylim(0, 95); axc.set_yticks([])
    for s in ["top", "right", "left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_color("#CFD2D5"); axc.tick_params(length=0)
    # discriminação
    y = 420
    txt(M, y, "Nos itens que mais separam (discriminação A de 1,70 para cima)", outfitB, 11.5, INK); y += 20
    for a in AR:
        e, c = dd["disc_muito_alta"][a]
        wmax = W - 2 * M - 150
        rrect(M + 110, y - 9, wmax * c / 100, 9, 3, COOP, z=2)
        rrect(M + 110, y + 2, wmax * e / 100, 9, 3, CORAL, z=2)
        txt(M, y + 2, ARN[a], outfit, 9, INK)
        txt(M + 116 + wmax * e / 100, y + 9, f"{vir(e,0)}% × {vir(c,0)}%", mono, 7.5, GRAY)
        y += 30
    txt(M, y + 4, "É exatamente nos itens de alta discriminação — os que 'ordenam' os candidatos — que a distância é maior.", outfit, 9, "#3A3A3D")
    # habilidades
    y += 34
    cw = (W - 2 * M - 16) / 2
    rrect(M, y, cw, 118, 10, "#FEF3F0", z=2)
    txt(M + 18, y + 22, "Alertas (erra mais que a coorte)", outfitB, 10.5, CORALd)
    yy = y + 44
    for hab, e, c in dd["hab_alertas"]:
        txt(M + 18, yy, f"{hab}: {vir(e,0)}% × {vir(c,0)}% da coorte", outfit, 9.5, INK); yy += 18
    txt(M + 18, yy + 4, "Apenas 2 habilidades acima da coorte —", outfit, 8.5, GRAY)
    txt(M + 18, yy + 18, "pauta cirúrgica para 2026.", outfit, 8.5, GRAY)
    x2 = M + cw + 16
    rrect(x2, y, cw, 118, 10, "#E9F7EF", z=2)
    txt(x2 + 18, y + 22, "Forças (erra muito menos)", outfitB, 10.5, VERDE)
    yy = y + 44
    for hab, e, c in dd["hab_forcas"][:4]:
        txt(x2 + 18, yy, f"{hab}: {vir(e,0)}% × {vir(c,0)}%", outfit, 9.5, INK); yy += 18
    footer(hp, "Fonte: Microdados ENEM 2025 / INEP · parâmetros da própria prova COP30 (mapa validado, zero divergências).", "7")


# ---------- p8 metodologia ----------
def p8_metodo(hp):
    txt = hp["txt"]; rrect = hp["rrect"]
    txt(M, 136, "Metodologia e contexto COP30", outfitB, 17, INK)
    y = 168
    itens = [
        ("Escola e população", "CO_ESCOLA 15038424 (Censo Escolar). 2025: 142 concluintes com escola declarada; 114–117 notas por área; 117 redações válidas. 2024: 135 presentes com as 5 notas. Língua: 136 inglês, 6 espanhol."),
        ("Aplicação COP30/BAM", "Em 2025, Belém, Ananindeua e Marituba fizeram prova própria (COP30), sem itens em comum com a Regular. Em RESULTADOS os códigos são 1583–1634; os parâmetros TRI desses mesmos itens estão em ITENS_PROVA sob os códigos 1502–1532. O mapa entre os dois foi revalidado: cruzamento do gabarito com todos os ~66 mil alunos BAM = zero divergências."),
        ("Comparações", "Nota TRI compara com qualquer aplicação (escala equalizada) → usamos coorte COP30 E Brasil P1. Análise item a item (habilidade, dificuldade, discriminação) compara SÓ com a coorte COP30 — mesma prova. Redação: mesmo tema apenas na coorte; evolução 2024 a 2025 usa redações válidas (status 'Sem problemas')."),
        ("Histórico", "Microdados completos disponíveis: 2024 (regular) e 2025 (COP30). Anos anteriores não integram este dossiê por indisponibilidade de microdado por escola no disco."),
        ("Critérios de ranking", "Média das 5 notas dos presentes nos 2 dias, escolas com 10 alunos ou mais. Belém 2025: 163 escolas; Pará: 850."),
        ("Integridade", "Nenhum valor estimado. Todos os números vêm dos Microdados ENEM 2024/2025 (INEP) e do Censo Escolar 2025. Dados por aluno jamais são publicados — apenas agregados da escola."),
    ]
    for t, c in itens:
        rrect(M, y, 7, 7, 2, CYAN, z=3)
        txt(M + 18, y + 7, t, outfitB, 11, INK)
        yy = y + 22
        words = c.split(); ln = ""; lines = []
        for w in words:
            if hp["tw"]((ln + " " + w).strip(), outfit, 9.5) > (W - 2 * M - 18):
                lines.append(ln); ln = w
            else:
                ln = (ln + " " + w).strip()
        lines.append(ln)
        for L in lines:
            txt(M + 18, yy, L, outfit, 9.5, "#3A3A3D"); yy += 14.5
        y = yy + 10
    footer(hp, "Dossiê XTRI · Prof. Alexandre Emerson · dados abertos do INEP.", "8")


with PdfPages(str(D / "Dossie_Marista_Belem_ENEM.pdf")) as pdf:
    for fn, tag in [(p1_capa, "DOSSIÊ · ENEM 2024–2025"), (p2_tri, "NOTAS TRI 2025"),
                    (p3_hist, "HISTÓRICO 2024 → 2025"), (p4_red, "REDAÇÃO · COMPETÊNCIAS"),
                    (p5_red_hist, "REDAÇÃO · EVOLUÇÃO"), (p6_rank, "RANKINGS"),
                    (p7_tri_itens, "RAIO-X TRI"), (p8_metodo, "METODOLOGIA")]:
        page(pdf, fn, tag)
print("ok: Dossie_Marista_Belem_ENEM.pdf (8 págs)")
