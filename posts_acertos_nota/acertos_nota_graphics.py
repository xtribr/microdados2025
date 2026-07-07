#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A9 — "Quantos acertos pra sua nota dos sonhos?" (por área)
Gera capa + 4 cards de área, cada um em feed (1080x1350) e story (1080x1920).
Padrao visual XTRI: fundo #F1F1F2, Outfit/JetBrains Mono, logo, assinatura.
Dado real: acertos_para_nota_2025_full.csv (gerado por compute_acertos_nota_full.py,
streaming completo de RESULTADOS_2025.csv — Regular P1, ~3,16M candidatos/área).
Metas "dos sonhos" por área (pedido do usuário, XTRI): LC 700 · CH 800 · CN 800 · MT 900.
Acertos=0 é excluído do traçado: é um caso degenerado (nota-piso ~0 por convenção do
INEP para padrão de resposta totalmente errado), fora do escopo de "quantos acertos".
"""
import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import font_manager as fm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import FancyBboxPatch

BASE = "/Volumes/Kingston 1/microdados_enem_2025"
FD = "/Volumes/Kingston/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/173c3dab-6f51-4ed6-920d-43825f73e36c/a32ba23c-1f19-4aa1-8eaf-390193971d87/skills/canvas-design/canvas-fonts"
LOGO = f"{BASE}/logo_xtri_marca_real.png"
OUT = f"{BASE}/posts_acertos_nota"
os.makedirs(OUT, exist_ok=True)


def F(n):
    return fm.FontProperties(fname=f"{FD}/{n}.ttf")


outfitB = F("Outfit-Bold")
outfit = F("Outfit-Regular")
mono = F("JetBrainsMono-Regular")
monoB = F("JetBrainsMono-Bold")

BG = "#F1F1F2"
CARD = "#FFFFFF"
INK = "#1D1D20"
GRAY = "#8C9298"
CORAL = "#FA5230"
CORALd = "#E8431F"
CYAN = "#1FAFEF"
CYANd = "#1597D8"

AREAS = [
    ("LC", "Linguagens", "linguagens e códigos"),
    ("CH", "Ciências Humanas", "ciências humanas"),
    ("CN", "Ciências da Natureza", "ciências da natureza"),
    ("MT", "Matemática", "matemática"),
]
DREAM_TARGET = {"LC": 700, "CH": 800, "CN": 800, "MT": 900}
# metas por área (a última é a "nota dos sonhos" / dream target, destacada em coral)
MILESTONES = {"LC": [600, 700], "CH": [600, 700, 800], "CN": [600, 700, 800], "MT": [700, 800, 900]}


def load_table():
    rows = defaultdict(list)
    with open(f"{OUT}/acertos_para_nota_2025_full.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            acertos = int(r["acertos"])
            if acertos < 1:
                continue  # exclui o caso degenerado de 0 acertos (nota-piso ~0)
            rows[r["area"]].append(
                {
                    "acertos": acertos,
                    "itens_validos": int(r["itens_validos"]),
                    "n": int(r["n"]),
                    "min": float(r["min"]),
                    "p10": float(r["p10"]),
                    "mediana": float(r["mediana"]),
                    "p90": float(r["p90"]),
                    "max": float(r["max"]),
                }
            )
    for a in rows:
        rows[a].sort(key=lambda r: r["acertos"])
    return rows


def milestone_hit(rs, thresh):
    return next((r for r in rs if r["mediana"] >= thresh), None)


def most_common(rs):
    return max(rs, key=lambda r: r["n"])


# ---------- canvas helpers (padrão XTRI) ----------
def new_canvas(W, H):
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    PXU = fig.get_size_inches()[0] * fig.dpi / W

    def tw(s, fp, sz):
        t = ax.text(0, 0, s, fontproperties=fp, fontsize=sz)
        fig.canvas.draw()
        w = t.get_window_extent(R).width / PXU
        t.remove()
        return w

    def txt(x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
        return ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

    def rrect(x, y, w, h, rad, fc, z=2, ec="none", lw=0):
        ax.add_patch(
            FancyBboxPatch(
                (x + rad, y + rad), w - 2 * rad, h - 2 * rad, boxstyle=f"round,pad={rad}",
                fc=fc, ec=ec, lw=lw, zorder=z, mutation_aspect=1,
            )
        )

    def shadow(x, y, w, h, rad):
        for i in range(1, 7):
            rrect(x - i, y + 2 + 1.6 * i, w + 2 * i, h + i, rad + 1.1 * i, "#000000", z=1.5)

    return fig, ax, tw, txt, rrect, shadow


def header(ax, txt, tw, W, M, kicker):
    try:
        ax.add_artist(
            AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=0.072), (M + 22, 54),
                           frameon=False, box_alignment=(0.5, 0.5), zorder=6)
        )
    except Exception:
        pass
    txt(M + 48, 60, "X-TRI", outfitB, 14, CYANd)
    txt(W - M, 52, "X-TRI · ANÁLISE DE DADOS", outfitB, 14, INK, ha="right")
    txt(W - M, 78, kicker, mono, 11.5, GRAY, ha="right")


def footer(ax, txt, tw, W, H, M, fonte_extra=""):
    txt(M, H - 70, "Dados reais", outfitB, 17, CYAN)
    xx = M + tw("Dados reais", outfitB, 17)
    txt(xx, H - 70, " ou ", outfitB, 17, INK)
    xx += tw(" ou ", outfitB, 17)
    txt(xx, H - 70, "nada", outfitB, 17, CORAL)
    xx += tw("nada", outfitB, 17)
    txt(xx, H - 70, ".", outfitB, 17, INK)
    txt(W - M, H - 70, f"Fonte: Microdados ENEM 2025 / INEP{fonte_extra}", mono, 9.5, GRAY, ha="right")


def make_cover(W, H, tag, table):
    fig, ax, tw, txt, rrect, shadow = new_canvas(W, H)
    M = 64
    header(ax, txt, tw, W, M, "TRI DO ENEM · ACERTOS × NOTA")

    ytitle = 210 if H < 1500 else 300
    txt(M, ytitle, "Quantos acertos", outfitB, 46, INK)
    txt(M, ytitle + 58, "pra sua nota ", outfitB, 46, INK)
    txt(M + tw("pra sua nota ", outfitB, 46), ytitle + 58, "dos sonhos?", outfitB, 46, CORAL)
    txt(M, ytitle + 108, "Nota real por número de acertos, nas 4 áreas do ENEM 2025 —", outfit, 17, GRAY)
    txt(M, ytitle + 134, "dado oficial, não estimativa.", outfit, 17, GRAY)

    cy = ytitle + 190
    cw = W - 2 * M
    bx = M + 40
    bar_w_max = cw - 300
    n = len(table)

    # --- layout vertical explícito (espaços fixos, nunca deixa o rodapé encostar na barra) ---
    KICKER_H = 96      # topo do card -> baseline do 1º rótulo (folga p/ o kicker não tocar o nome)
    LABEL_BAR = 40     # baseline do rótulo -> base da barra (barra em +14, altura 26)
    CAP_GAP = 56       # base da última barra -> baseline da legenda (respiro real ≥ 40px)
    PAD_BOTTOM = 34    # baseline da legenda -> base do card
    HINT_GAP = 46      # base do card -> "Desliza..."
    # ROW_H se ajusta pra caber tudo acima do rodapé, com teto p/ não esticar demais
    bottom_limit = H - 70 - 40
    avail_rows = bottom_limit - cy - KICKER_H - LABEL_BAR - CAP_GAP - PAD_BOTTOM - HINT_GAP
    ROW_H = max(88, min(112, avail_rows / n))

    rows_top = cy + KICKER_H                              # baseline do 1º rótulo
    last_bar_bottom = rows_top + (n - 1) * ROW_H + LABEL_BAR
    cap_y = last_bar_bottom + CAP_GAP                     # baseline da legenda
    ch = cap_y + PAD_BOTTOM - cy

    shadow(M, cy, cw, ch, 22)
    rrect(M, cy, cw, ch, 22, CARD, z=2)
    txt(M + 34, cy + 42, "A NOTA DOS SONHOS PEDE ACERTAR QUASE TUDO", mono, 12.5, GRAY)

    # trilha (prova inteira) encurtada p/ abrir uma coluna fixa à direita, onde ficam
    # o alvo ("pra 700") e o valor ("42 acertos (93%)"). Assim o número NUNCA cai sobre a barra.
    track_w = 600
    val_x = bx + track_w + 26
    for i, r in enumerate(table):
        by = rows_top + i * ROW_H                         # baseline do rótulo da área
        txt(bx, by, r["name"], outfitB, 20, INK)
        txt(val_x, by - 2, f"pra {r['meta']}", mono, 11, GRAY, ha="left")
        bw = track_w * (r["acertos"] / r["itens_validos"])
        rrect(bx, by + 14, track_w, 26, 13, "#E7E8EA", z=2)
        rrect(bx, by + 14, bw, 26, 13, CORALd, z=3)
        txt(val_x, by + 32, f"{r['acertos']} acertos ({r['pct']}%)", monoB, 14, CORALd, va="center")

    txt(M + 34, cap_y, "Nas 4 áreas, a meta dos sonhos exige entre 93% e 96% da prova certa.",
        outfit, 14.5, INK)

    txt(M, cy + ch + HINT_GAP, "Desliza para ver sua área →", outfit, 14, GRAY)

    footer(ax, txt, tw, W, H, M)
    fig.savefig(f"{OUT}/xtri_acertos_nota_capa_{tag}.png", dpi=300, facecolor=BG)
    plt.close(fig)
    print(f"capa {tag} ok")


def make_area_card(W, H, tag, code, name, gancho, rs, iv, metas):
    fig, ax, tw, txt, rrect, shadow = new_canvas(W, H)
    M = 64
    header(ax, txt, tw, W, M, f"TRI DO ENEM · {name.upper()}")

    ytitle = 174 if H < 1500 else 250
    txt(M, ytitle, f"{name}: quantos acertos", outfitB, 34, INK)
    # linha 2: "pra 600, 700 ou 800?" — cada meta colorida (última = coral, resto = cyan)
    xx = M
    txt(xx, ytitle + 44, "pra ", outfitB, 34, INK)
    xx += tw("pra ", outfitB, 34)
    for i, mt in enumerate(metas):
        is_dream = i == len(metas) - 1
        color = CORALd if is_dream else CYANd
        if i > 0:
            sep = " ou " if is_dream else ", "
            txt(xx, ytitle + 44, sep, outfitB, 34, INK)
            xx += tw(sep, outfitB, 34)
        txt(xx, ytitle + 44, f"{mt}", outfitB, 34, color)
        xx += tw(f"{mt}", outfitB, 34)
    txt(xx, ytitle + 44, "?", outfitB, 34, INK)
    txt(M, ytitle + 82, gancho, outfit, 15.5, GRAY)

    # ---- chart panel embutido via inset axes ----
    chart_top = ytitle + 120
    chart_h = (H - 170 - chart_top) if H < 1500 else (H - 260 - chart_top)
    l = M / W
    b = 1 - (chart_top + chart_h) / H
    w = (W - 2 * M) / W
    h = chart_h / H
    axc = fig.add_axes([l, b, w, h])
    axc.set_facecolor(BG)

    xs = [r["acertos"] for r in rs]
    med = [r["mediana"] for r in rs]
    p10 = [r["p10"] for r in rs]
    p90 = [r["p90"] for r in rs]
    axc.fill_between(xs, p10, p90, color=CORAL, alpha=0.12, zorder=1)
    axc.plot(xs, med, color=CORALd, lw=3, zorder=4)

    # marca cada meta na régua; a última (dream) em coral cheio, as outras em cyan mais leve.
    # como a mediana é monótona não-decrescente, o espaço ACIMA-À-ESQUERDA de cada ponto
    # está sempre livre -> ancoro o rótulo em x=a, ha="right", deslocado pra cima, sem cruzar a curva.
    for i, mt in enumerate(metas):
        hit = milestone_hit(rs, mt)
        if not hit:
            continue
        a = hit["acertos"]
        med_a = hit["mediana"]
        is_dream = i == len(metas) - 1
        color = CORALd if is_dream else CYANd
        lw_line = 1.8 if is_dream else 1.2
        ms_dot = 8 if is_dream else 6
        axc.plot([a, a], [280, med_a], color=color, lw=lw_line, ls=(0, (3, 2)),
                 zorder=3, alpha=1.0 if is_dream else 0.85)
        axc.plot([a], [med_a], marker="o", color=color, ms=ms_dot, zorder=5)
        pct = round(100 * a / iv)
        # rótulo de 1 linha (~30px): cabe acima-à-esquerda (região vazia) até quase o topo.
        # só joga pra baixo se o ponto já estiver colado no teto do eixo (>985).
        if med_a + 55 > 985:
            y_lab, va = med_a - 60, "top"
        else:
            y_lab, va = med_a + 60, "bottom"
        axc.annotate(
            f"{a} ({pct}%) → {mt}",
            xy=(a, med_a), xytext=(a - 0.4, y_lab),
            fontproperties=monoB, fontsize=11, color=color, ha="right", va=va,
            arrowprops=dict(arrowstyle="-", color=color, lw=1.1),
        )

    axc.set_xlim(0, iv)
    axc.set_ylim(280, 1000)
    axc.set_xlabel(f"Nº de acertos ({code}, de {iv})", fontproperties=outfit, fontsize=11.5, color=INK)
    axc.set_ylabel("Nota TRI oficial", fontproperties=outfit, fontsize=11.5, color=INK)
    for s in ["top", "right"]:
        axc.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        axc.spines[s].set_color("#CFD2D5")
    axc.tick_params(colors=GRAY, labelsize=9)
    for lab in axc.get_xticklabels() + axc.get_yticklabels():
        lab.set_fontproperties(mono)
        lab.set_fontsize(9)
    axc.grid(axis="y", color="#E6E7E9", lw=0.8)
    axc.set_axisbelow(True)

    footer(ax, txt, tw, W, H, M, f" · Regular P1, todos os presentes ({code})")
    fig.savefig(f"{OUT}/xtri_acertos_nota_{code.lower()}_{tag}.png", dpi=300, facecolor=BG)
    plt.close(fig)
    print(f"{code} {tag} ok")


GANCHOS = {
    "LC": "Em Linguagens, 600 pedem 30 acertos; a nota dos sonhos (700) exige 42 dos 45.",
    "CH": "Em Humanas, de 600 a 800 pontos: veja quantos acertos cada patamar cobra.",
    "CN": "Em Natureza, a curva é a mais “linear” — de 600 a 800, passo a passo.",
    "MT": "Em Matemática, poucos acertos já valem muito: de 700 a 900, veja a régua.",
}

if __name__ == "__main__":
    table = load_table()
    preview = []
    for code, name, _ in AREAS:
        rs = table[code]
        meta = DREAM_TARGET[code]
        iv = rs[0]["itens_validos"]
        hit = milestone_hit(rs, meta)
        acertos = hit["acertos"] if hit else rs[-1]["acertos"]
        preview.append({
            "code": code, "name": name, "meta": meta, "acertos": acertos, "itens_validos": iv,
            "pct": round(100 * acertos / iv),
        })

    for tag, (W, H) in (("feed", (1080, 1350)), ("story", (1080, 1920))):
        make_cover(W, H, tag, preview)
        for code, name, _ in AREAS:
            rs = table[code]
            iv = rs[0]["itens_validos"]
            make_area_card(W, H, tag, code, name, GANCHOS[code], rs, iv, MILESTONES[code])
    print("FIM")
