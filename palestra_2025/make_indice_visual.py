#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Índice visual (contact-sheet) de todos os cards do deck palestra_2025.
Agrupa por tema, miniatura + legenda de cada card, marca XTRI. Saída: INDICE_deck_visual.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, Rectangle

from xtri_deck import outfitB, outfit, mono, monoB, INK, GRAY, CORAL, CYAN, CYANd, BG, OUTDIR, BASE

G = OUTDIR  # pasta dos PNGs

SECOES = [
    ("Redação — a queda da C2", [
        ("g02a_c2_hero.png", "C2 em queda (número-herói)"),
        ("g02b_comp_5.png", "As 5 competências 2024×2025"),
        ("g02c_status_2025.png", "Status da redação 2025"),
        ("g02d_faixas_2025.png", "Faixas de nota da redação"),
    ]),
    ("Redação prevê a prova objetiva?", [
        ("g03a_ggplot_redacao_r2.png", "Redação × objetiva (correlação)"),
        ("g03b_ggplot_redacao_densidade.png", "Densidade redação × nota"),
    ]),
    ("Acerto não é nota (TRI)", [
        ("g01_ggplot_scatter_LC.png", "Acerto × nota — Linguagens"),
        ("g01_ggplot_scatter_CH.png", "Acerto × nota — Humanas"),
        ("g01_ggplot_scatter_CN.png", "Acerto × nota — Natureza"),
        ("g01_ggplot_scatter_MT.png", "Acerto × nota — Matemática"),
    ]),
    ("Dificuldade ao longo do caderno", [
        ("g04_dificuldade_posicao_LC.png", "Dificuldade × posição — LC"),
        ("g04_dificuldade_posicao_CH.png", "Dificuldade × posição — CH"),
        ("g04_dificuldade_posicao_CN.png", "Dificuldade × posição — CN"),
        ("g04_dificuldade_posicao_MT.png", "Dificuldade × posição — MT"),
    ]),
    ("Taxa de erro por habilidade", [
        ("g05_taxa_erro_LC.png", "Taxa de erro — Linguagens"),
        ("g05_taxa_erro_CH.png", "Taxa de erro — Humanas"),
        ("g05_taxa_erro_CN.png", "Taxa de erro — Natureza"),
        ("g05_taxa_erro_MT.png", "Taxa de erro — Matemática"),
    ]),
    ("Acerto → nota (tabelas)", [
        ("g07_tabela_acerto_nota_LC.png", "Acerto→nota — Linguagens"),
        ("g07_tabela_acerto_nota_CH.png", "Acerto→nota — Humanas"),
        ("g07_tabela_acerto_nota_CN.png", "Acerto→nota — Natureza"),
        ("g07_tabela_acerto_nota_MT.png", "Acerto→nota — Matemática"),
    ]),
    ("Prova regular × 2ª aplicação", [
        ("g06_comparacao_provas.png", "Comparação de dificuldade das provas"),
    ]),
    ("Chutes e coerência (person-fit)", [
        ("g08a_chutes_scatter.png", "Chutes × incoerência (scatter)"),
        ("g08b_chutes_insight.png", "Mesma nota, mais incoerência"),
    ]),
    ("Inglês × Espanhol", [
        ("g09a_ingles_espanhol_curva.png", "Inglês × Espanhol (curva)"),
        ("g09b_casos_reais_lingua.png", "Casos reais de alunos"),
    ]),
    ("Maiores TRIs por estado", [
        ("g10a_top_uf_leaderboard.png", "Leaderboard por UF + escola"),
        ("g10b_top_uf_barras.png", "Barras por UF"),
    ]),
    ("Testlet de Linguagens (Q6–10)", [
        ("g11_testlet_linguagens.png", "Taxa de erro do testlet"),
        ("g11b_testlet_narrativa.png", "Escada de enunciados"),
        ("g11c_testlet_AxB.png", "Plano discriminação × dificuldade"),
        ("g11d_testlet_tabela.png", "Tabela de parâmetros A·B·C"),
    ]),
    ("Discriminação (A) por área", [
        ("g12_top_discriminacao.png", "Questão mais discriminativa por área"),
    ]),
]

W = 2000
M = 56
COLS = 4
GAP = 28
CELL_W = (W - 2 * M - (COLS - 1) * GAP) / COLS
THUMB_H = 244
CAP_H = 36
ROW_GAP = 22
HEAD_H = 58
SEC_PAD = 12
TITLE_H = 156
FOOTER_H = 80


def measure():
    y = TITLE_H
    for _, items in SECOES:
        y += HEAD_H
        rows = -(-len(items) // COLS)
        y += rows * (THUMB_H + CAP_H + ROW_GAP)
        y += SEC_PAD
    return int(y + FOOTER_H)


def main():
    H = measure()
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    bax = fig.add_axes([0, 0, 1, 1]); bax.set_xlim(0, W); bax.set_ylim(H, 0); bax.axis("off")
    bax.add_patch(Rectangle((0, 0), W, H, fc=BG, ec="none", zorder=0))

    def T(x, y, s, fp, sz, c, ha="left", va="baseline"):
        bax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=6)

    n_cards = sum(len(it) for _, it in SECOES)
    # título
    T(M, 74, "Deck ENEM 2025 — ", outfitB, 34, INK)
    wtt = bax.text(0, 0, "Deck ENEM 2025 — ", fontproperties=outfitB, fontsize=34); fig.canvas.draw()
    off = wtt.get_window_extent(fig.canvas.get_renderer()).width / (fig.get_size_inches()[0] * fig.dpi / W); wtt.remove()
    T(M + off, 74, "índice visual", outfitB, 34, CORAL)
    T(M, 112, f"{n_cards} cards · o que cada gráfico mostra · Estudo XTRI — Prof. Alexandre Emerson · Microdados ENEM 2025 / INEP",
      outfit, 15, GRAY)
    bax.plot([M, W - M], [134, 134], color="#D9D9DB", lw=1.2, zorder=5)

    y = TITLE_H
    for sec, items in SECOES:
        # cabeçalho de seção
        bax.add_patch(Rectangle((M, y + 14), 8, HEAD_H - 26, fc=CORAL, ec="none", zorder=5))
        T(M + 22, y + HEAD_H - 22, sec, outfitB, 21, INK)
        T(W - M, y + HEAD_H - 22, f"{len(items)} card" + ("s" if len(items) > 1 else ""), mono, 13, GRAY, ha="right")
        y += HEAD_H
        for i, (fn, cap) in enumerate(items):
            r, c = divmod(i, COLS)
            cx = M + c * (CELL_W + GAP)
            cy = y + r * (THUMB_H + CAP_H + ROW_GAP)
            path = os.path.join(G, fn)
            if not os.path.exists(path):
                T(cx + CELL_W / 2, cy + THUMB_H / 2, "(faltando)", mono, 12, "#C0392B", ha="center", va="center")
                continue
            img = mpimg.imread(path); ih, iw = img.shape[0], img.shape[1]
            scale = min(CELL_W / iw, THUMB_H / ih)
            dw, dh = iw * scale, ih * scale
            ox = cx + (CELL_W - dw) / 2
            oy = cy + (THUMB_H - dh) / 2
            # moldura
            bax.add_patch(FancyBboxPatch((ox + 3, oy + 3), dw - 6, dh - 6, boxstyle="round,pad=3",
                                         fc="white", ec="#DADCDE", lw=1.0, zorder=3))
            iax = fig.add_axes([ox / W, (H - oy - dh) / H, dw / W, dh / H], zorder=4)
            iax.imshow(img); iax.axis("off")
            # legenda
            T(cx + CELL_W / 2, cy + THUMB_H + 24, cap, outfit, 13.5, INK, ha="center")
        rows = -(-len(items) // COLS)
        y += rows * (THUMB_H + CAP_H + ROW_GAP) + SEC_PAD

    # rodapé
    T(M, H - 34, "Dados reais", outfitB, 15, CYAN)
    wr = bax.text(0, 0, "Dados reais", fontproperties=outfitB, fontsize=15); fig.canvas.draw()
    o2 = wr.get_window_extent(fig.canvas.get_renderer()).width / (fig.get_size_inches()[0] * fig.dpi / W); wr.remove()
    T(M + o2, H - 34, " ou ", outfitB, 15, INK)
    T(M + o2 + 34, H - 34, "nada.", outfitB, 15, CORAL)
    T(W - M, H - 34, "app.rankingenem.com · @xandaoxtri", mono, 12, GRAY, ha="right")

    out = os.path.join(BASE, "palestra_2025", "INDICE_deck_visual.png")
    fig.savefig(out, dpi=100, facecolor=BG)
    plt.close(fig)
    print("ok:", out, f"({W}x{H}, {n_cards} cards)")


if __name__ == "__main__":
    main()
