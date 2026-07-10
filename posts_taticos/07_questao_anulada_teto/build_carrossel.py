#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel 'A questão anulada que decidiu quem fez 980' — 6 slides feed
(1080x1350) + capa story (1080x1920). PADRAO VISUAL XTRI.
Numeros reais: Microdados ENEM 2025 / INEP, analise em R (scripts 06-08 do
projeto '/Volumes/Kingston 1/microdados no R Studio/')."""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FD = "/Volumes/Kingston/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/173c3dab-6f51-4ed6-920d-43825f73e36c/a32ba23c-1f19-4aa1-8eaf-390193971d87/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB = F("Outfit-Bold"); outfit = F("Outfit-Regular")
mono = F("JetBrainsMono-Regular"); monoB = F("JetBrainsMono-Bold")
BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE, "..", "..", "logo_xtri_marca_real.png")

BG = "#F1F1F2"; CARD = "#FFFFFF"; INK = "#1D1D20"; GRAY = "#8C9298"
CORAL = "#FA5230"; CORALd = "#E8431F"; CYAN = "#1FAFEF"; CYANd = "#1597D8"
CHIP_CO = "#FBDDD3"; CHIP_CY = "#DCF0FB"; TRACK = "#E3E5E7"
CTA_BG = "#1B1B1E"; CTA_SUB = "#9AA0A6"
M = 72; W = 1080
NOTA = "Fonte: Microdados ENEM 2025 / INEP · análise em R (data.table + ggplot2) · aplicação regular"

class Slide:
    def __init__(self, H=1350):
        self.H = H
        self.fig = plt.figure(figsize=(W / 100, H / 100), dpi=300)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, W); self.ax.set_ylim(H, 0); self.ax.axis("off")
        self.ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))
        self.fig.canvas.draw()
        self.R = self.fig.canvas.get_renderer()
        self.PXU = self.fig.get_size_inches()[0] * self.fig.dpi / W

    def tw(self, s, fp, sz):
        t = self.ax.text(0, 0, s, fontproperties=fp, fontsize=sz)
        self.fig.canvas.draw()
        w = t.get_window_extent(self.R).width / self.PXU
        t.remove(); return w

    def txt(self, x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
        return self.ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

    def mix(self, x, y, partes, sz, fp_default=None):
        """escreve trechos coloridos em sequencia: partes = [(texto, cor, fonte?)]"""
        for parte in partes:
            texto, cor = parte[0], parte[1]
            fp = parte[2] if len(parte) > 2 else (fp_default or outfitB)
            self.txt(x, y, texto, fp, sz, cor)
            x += self.tw(texto, fp, sz)
        return x

    def rrect(self, x, y, w, h, rad, fc, z=2, alpha=1):
        self.ax.add_patch(FancyBboxPatch((x + rad, y + rad), w - 2 * rad, h - 2 * rad,
            boxstyle=f"round,pad={rad}", fc=fc, ec="none", zorder=z, alpha=alpha, mutation_aspect=1))

    def shadow(self, x, y, w, h, rad):
        for i in range(1, 9):
            self.rrect(x - 1.0 * i, y + 2.4 + 1.7 * i, w + 2.0 * i, h + 1.0 * i, rad + 1.2 * i,
                       "#000000", z=1.5, alpha=0.012)

    def header(self, pagina, logoy=82, logoz=0.115, wmy=140):
        try:
            self.ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=logoz),
                (M + 30, logoy), frameon=False, box_alignment=(0.5, 0.5), zorder=6))
        except Exception:
            pass
        self.txt(M, wmy, "X-TRI", outfitB, 16, CYANd)
        self.txt(W - M, 100, "ITENS ANULADOS", outfitB, 16.5, INK, ha="right")
        self.txt(W - M, 128, "ENEM 2025 · Aplicação regular", mono, 13, GRAY, ha="right")
        self.txt(W - M, 158, pagina, monoB, 12, GRAY, ha="right")

    def footer(self, handle_y=1170, sig_y=1214, nota_y=1284):
        self.txt(M, handle_y, "@xandaoxtri", outfitB, 28, INK)
        self.mix(M, sig_y, [("Transformamos ", INK), ("dados", CYAN), (" em ", INK),
                             ("aprovações", CORAL), (".", INK)], 23)
        self.txt(M, nota_y, NOTA, mono, 10.5, GRAY)

    def save(self, nome):
        out = os.path.join(BASE, nome)
        self.fig.savefig(out, dpi=300, facecolor=BG); plt.close(self.fig)
        print("salvo", out)


def hero_duplo(s, y, h, label_topo):
    """card com 980,3 vs 967,7 lado a lado + chip de diferenca"""
    s.shadow(M, y, W - 2 * M, h, 26); s.rrect(M, y, W - 2 * M, h, 26, CARD, z=2)
    s.txt(W / 2, y + 44, label_topo, mono, 12.5, GRAY, ha="center")
    cx = W / 2
    s.ax.add_line(Line2D([cx, cx], [y + 70, y + h - 76], color=TRACK, lw=1.5, zorder=3))
    lx = M + (W - 2 * M) / 4; rx = W - M - (W - 2 * M) / 4
    s.txt(lx, y + 92, "MARCOU A NA ANULADA", monoB, 12, CORALd, ha="center")
    s.txt(lx, y + 196, "980,3", outfitB, 68, CORAL, ha="center")
    s.txt(lx, y + 240, "86 candidatos", mono, 12.5, GRAY, ha="center")
    s.txt(rx, y + 92, "MARCOU OUTRA LETRA", monoB, 12, GRAY, ha="center")
    s.txt(rx, y + 196, "967,7", outfitB, 68, INK, ha="center")
    s.txt(rx, y + 240, "515 candidatos", mono, 12.5, GRAY, ha="center")
    cw, ch2 = 210, 46
    s.rrect(cx - cw / 2, y + h - 72, cw, ch2, 15, CORAL, z=4)
    s.txt(cx, y + h - 72 + ch2 / 2 + 1, "+12,6 pontos", monoB, 15, "#FFFFFF", ha="center", va="center", z=5)


# ============ SLIDE 1 — CAPA ============
def slide1(fmt):
    if fmt == "feed":
        s = Slide(1350)
        hy, hsz, suby = [252, 326, 400], 54, 462
        heroy, heroh, cuey = 528, 350, 946
        foot = dict(handle_y=1170, sig_y=1214, nota_y=1284)
    else:
        s = Slide(1920)
        s.header("1/6", logoy=140, logoz=0.135, wmy=204)
        hy, hsz, suby = [400, 486, 572], 60, 650
        heroy, heroh, cuey = 730, 430, 1250
        foot = dict(handle_y=1660, sig_y=1710, nota_y=1790)
    if fmt == "feed":
        s.header("1/6")
    s.mix(M, hy[0], [("A questão ", INK), ("ANULADA", CORAL)], hsz)
    s.txt(M, hy[1], "que decidiu quem", outfitB, hsz, INK)
    s.txt(M, hy[2], "fez 980 em Matemática.", outfitB, hsz, INK)
    s.mix(M, suby, [("Ela oficialmente não valia nada. ", INK)], 19.5)
    s.txt(M + s.tw("Ela oficialmente não valia nada. ", outfitB, 19.5), suby,
          "Os microdados contam outra história.", outfit, 19.5, GRAY)
    hero_duplo(s, heroy, heroh, "OS 601 QUE ACERTARAM TUDO QUE VALIA NOTA")
    s.txt(W / 2, cuey, "arrasta pra ver a prova completa →", outfit, 16.5, GRAY, ha="center")
    s.footer(**foot)
    s.save(f"c1_capa_{fmt}.png")


# ============ SLIDE 2 — O TESTE DOS GÊMEOS ============
def slide2():
    s = Slide(); s.header("2/6")
    s.mix(M, 250, [("O teste dos ", INK), ("gêmeos de prova", CORAL), (".", INK)], 40)
    s.mix(M, 322, [("601 candidatos", INK), (" acertaram TODOS os 43 itens válidos de Matemática.", GRAY, outfit)], 17.5)
    s.txt(M, 354, "Desempenho idêntico em tudo que valia nota. Pela TRI, nota igual.", outfit, 17.5, GRAY)
    s.mix(M, 386, [("Não foi o que saiu:", INK)], 17.5)
    hero_duplo(s, 434, 330, "MESMA PROVA VÁLIDA · NOTAS DIFERENTES")
    cy2 = 812
    s.shadow(M, cy2, W - 2 * M, 236, 24); s.rrect(M, cy2, W - 2 * M, 236, 24, CARD, z=2)
    s.txt(M + 40, cy2 + 48, "E NAS OUTRAS ÁREAS?", monoB, 12, GRAY)
    s.mix(M + 40, cy2 + 96, [("Ciências da Natureza, mesma história: ", INK),
                              ("858,7 × 852,4 (+6,3)", CORALd), (".", INK)], 17)
    s.txt(M + 40, cy2 + 140, "Linguagens e Humanas não tiveram item anulado — e lá todos os", outfit, 15.5, GRAY)
    s.txt(M + 40, cy2 + 168, "gabaritadores empataram (794,5 e 856,4), como manda a teoria.", outfit, 15.5, GRAY)
    s.txt(M + 40, cy2 + 204, "O padrão só quebra onde existe anulada.", outfitB, 15.5, INK)
    s.footer()
    s.save("c2_gemeos_feed.png")


# ============ SLIDE 3 — E O RESTO DA ESCALA? ============
def slide3():
    s = Slide(); s.header("3/6")
    s.mix(M, 250, [("E pra quem não gabaritou? ", INK), ("Zero.", CORAL)], 38)
    s.txt(M, 320, "Caçamos gêmeos na base inteira: mesmo caderno, mesmas respostas em", outfit, 17, GRAY)
    s.txt(M, 352, "todos os itens válidos — divergindo só na anulada.", outfit, 17, GRAY)

    cy, ch = 400, 430
    s.shadow(M, cy, W - 2 * M, ch, 24); s.rrect(M, cy, W - 2 * M, ch, 24, CARD, z=2)
    s.txt(M + 40, cy + 48, "GANHO POR ACERTAR A ANULADA · GRUPO A GRUPO", monoB, 12, GRAY)
    y0 = cy + ch - 92                       # linha do zero
    x0, x1 = M + 90, W - M - 60
    s.ax.add_line(Line2D([x0, x1], [y0, y0], color=TRACK, lw = 2, zorder=3))
    s.txt(x0 - 14, y0 + 5, "0", monoB, 13, GRAY, ha="right")
    # pontos azuis no zero (posicoes fixas, sem aleatoriedade)
    import numpy as np
    xs = np.linspace(x0 + 10, x1 - 130, 34)
    for i, x in enumerate(xs):
        s.ax.add_line(Line2D([x], [y0 - 6 - (i % 3) * 7], color=CYAN, marker="o",
                              markersize=4.6, alpha=0.6, lw=0, zorder=4))
    # os 2 pontos que fogem (teto)
    s.ax.add_line(Line2D([x1 - 95], [cy + 210], color=CORAL, marker="o", markersize=7, lw=0, zorder=5))
    s.txt(x1 - 95, cy + 190, "+6,3 (CN)", monoB, 12.5, CORALd, ha="center")
    s.ax.add_line(Line2D([x1 - 38], [cy + 110], color=CORAL, marker="o", markersize=7, lw=0, zorder=5))
    s.txt(x1 - 38, cy + 90, "+12,6 (MT)", monoB, 12.5, CORALd, ha="center")
    s.txt(x0, y0 + 34, "nota 362", mono, 11, GRAY)
    s.txt(x1, y0 + 34, "nota 980", mono, 11, GRAY, ha="right")
    s.txt(x1 - 66, cy + 250, "só quem", outfit, 12.5, GRAY, ha="center")
    s.txt(x1 - 66, cy + 272, "acertou tudo", outfit, 12.5, GRAY, ha="center")

    # chips de contexto
    chy = 866
    chips = [("322 grupos de gêmeos", CHIP_CY, CYANd), ("2.300 candidatos", CHIP_CY, CYANd),
             ("zero exceções", CHIP_CO, CORALd)]
    x = M
    for texto, bgc, txc in chips:
        cw = s.tw(texto, monoB, 13) + 44
        s.rrect(x, chy, cw, 42, 13, bgc, z=3)
        s.txt(x + cw / 2, chy + 22, texto, monoB, 13, txc, ha="center", va="center", z=4)
        x += cw + 18
    s.mix(M, 968, [("Em 314 dos 322 grupos, o ganho foi exatamente ", INK),
                    ("0,0", CYAN), (".", INK)], 18)
    s.mix(M, 1004, [("Os 8 restantes? Todos no topo — quem acertou ", INK), ("tudo", CORAL), (".", INK)], 18)
    s.footer()
    s.save("c3_escala_feed.png")


# ============ SLIDE 4 — GABARITO MINORITÁRIO ============
def slide4():
    s = Slide(); s.header("4/6")
    s.txt(M, 246, "O gabarito oficial era a resposta", outfitB, 36, INK)
    s.mix(M, 306, [("MINORITÁRIA", CORAL), (" entre os melhores.", INK)], 36)
    s.txt(M, 366, "O que os 601 melhores de Matemática marcaram na questão anulada:", outfit, 17, GRAY)

    cy, ch = 412, 470
    s.shadow(M, cy, W - 2 * M, ch, 24); s.rrect(M, cy, W - 2 * M, ch, 24, CARD, z=2)
    barras = [("D", 512, False), ("A", 86, True), ("C", 2, False), ("E", 1, False)]
    bx0, bx1 = M + 130, W - M - 200
    escala = (bx1 - bx0) / 512.0
    for i, (letra, n, oficial) in enumerate(barras):
        yc = cy + 78 + i * 104
        cor_badge = CHIP_CO if oficial else CHIP_CY
        cor_letra = CORALd if oficial else CYANd
        s.rrect(M + 44, yc - 24, 52, 48, 13, cor_badge, z=3)
        s.txt(M + 70, yc + 1, letra, outfitB, 22, cor_letra, ha="center", va="center", z=4)
        s.ax.add_line(Line2D([bx0, bx1], [yc, yc], color=TRACK, lw=11, solid_capstyle="round", zorder=3))
        xe = bx0 + max(n * escala, 6)
        s.ax.add_line(Line2D([bx0, xe], [yc, yc], color=CORAL if oficial else "#C5CACF",
                              lw=11, solid_capstyle="round", zorder=3.5))
        s.txt(bx1 + 24, yc + 1, f"{n}", monoB, 19, CORALd if oficial else INK, va="center")
        if oficial:
            s.txt(bx1 + 24 + s.tw(str(n), monoB, 19) + 14, yc + 1, "← GABARITO", monoB, 11.5, CORALd, va="center")
    s.mix(M, 940, [("85% dos melhores marcaram D. ", INK), ("A letra oficial (A) foi escolha de 14%.", GRAY, outfit)], 17.5)
    s.txt(M, 976, "O item estava mesmo quebrado — anulado por “problema de convergência”.", outfit, 17.5, GRAY)
    s.mix(M, 1012, [("E ainda assim separou o topo da edição.", INK)], 17.5)
    s.footer()
    s.save("c4_gabarito_feed.png")


# ============ SLIDE 5 — AFINAL, CONTA? ============
def slide5():
    s = Slide(); s.header("5/6")
    s.txt(M, 250, "Afinal: anulada conta ou não?", outfitB, 40, INK)

    c1y, c1h = 316, 254
    s.shadow(M, c1y, W - 2 * M, c1h, 24); s.rrect(M, c1y, W - 2 * M, c1h, 24, CARD, z=2)
    s.txt(M + 40, c1y + 48, "PARA 99,99% DOS CANDIDATOS", monoB, 12.5, CYANd)
    s.txt(M + 40, c1y + 118, "NÃO.", outfitB, 46, INK)
    s.txt(M + 40, c1y + 168, "Gêmeos exatos de prova, da nota 362 à 980:", outfit, 16.5, GRAY)
    s.txt(M + 40, c1y + 198, "diferença de 0,0 ponto. Nenhuma exceção.", outfit, 16.5, GRAY)

    c2y, c2h = 600, 254
    s.shadow(M, c2y, W - 2 * M, c2h, 24); s.rrect(M, c2y, W - 2 * M, c2h, 24, CARD, z=2)
    s.txt(M + 40, c2y + 48, "PARA QUEM ACERTOU TUDO QUE VALIA", monoB, 12.5, CORALd)
    s.txt(M + 40, c2y + 118, "SIM.", outfitB, 46, CORAL)
    s.txt(M + 40, c2y + 168, "+12,6 pontos em Matemática e +6,3 em Natureza —", outfit, 16.5, GRAY)
    s.txt(M + 40, c2y + 198, "a resposta na anulada decidiu as notas máximas da edição.", outfit, 16.5, GRAY)

    s.txt(M, 916, "NOSSA LEITURA TÉCNICA (INTERPRETAÇÃO)", monoB, 11.5, GRAY)
    s.txt(M, 952, "O item parece ter entrado no modelo com peso minúsculo: invisível onde a", outfit, 16, INK)
    s.txt(M, 982, "prova mede bem, decisivo onde a régua acaba. O processamento interno do", outfit, 16, INK)
    s.txt(M, 1012, "INEP não é público — o que provamos é o efeito, não o mecanismo.", outfit, 16, INK)
    s.footer()
    s.save("c5_conta_feed.png")


# ============ SLIDE 6 — MÉTODO ============
def slide6():
    s = Slide(); s.header("6/6")
    s.txt(M, 250, "Como a gente descobriu.", outfitB, 40, INK)
    cy, ch = 310, 700
    s.shadow(M, cy, W - 2 * M, ch, 24); s.rrect(M, cy, W - 2 * M, ch, 24, CARD, z=2)
    passos = [
        ("01", "Microdados oficiais do INEP",
         "4,8 milhões de candidatos — dado público, real e auditável."),
        ("02", "Análise em R",
         "data.table + ggplot2, scripts numerados e reproduzíveis."),
        ("03", "Gêmeos de prova",
         "candidatos com respostas idênticas em todos os itens válidos,\ndivergindo só na questão anulada."),
        ("04", "644 comparações, zero exceções",
         "a nota é função pura do padrão válido + resposta na anulada."),
    ]
    for i, (num, titulo, sub) in enumerate(passos):
        yc = cy + 92 + i * 158
        s.rrect(M + 44, yc - 30, 62, 62, 16, CHIP_CY, z=3)
        s.txt(M + 75, yc + 1, num, monoB, 17, CYANd, ha="center", va="center", z=4)
        s.txt(M + 136, yc - 6, titulo, outfitB, 21.5, INK)
        for j, linha in enumerate(sub.split("\n")):
            s.txt(M + 136, yc + 26 + j * 27, linha, outfit, 14.5, GRAY)

    # CTA + footer proprio (nota desce pra dar respiro ao CTA)
    s.txt(M, 1128, "@xandaoxtri", outfitB, 28, INK)
    s.mix(M, 1172, [("Transformamos ", INK), ("dados", CYAN), (" em ", INK),
                     ("aprovações", CORAL), (".", INK)], 23)
    cax, cay, caw, cah = 726, 1090, W - M - 726, 100
    s.rrect(cax, cay, caw, cah, 22, CTA_BG, z=3)
    s.txt(cax + 28, cay + 40, "VEJA MAIS ESTUDOS", mono, 11.5, CTA_SUB)
    s.txt(cax + 28, cay + 72, "xtri.online →", monoB, 14.5, "#FFFFFF")
    s.txt(M, 1284, NOTA, mono, 10.5, GRAY)
    s.save("c6_metodo_feed.png")


slide1("feed")
slide1("story")
slide2()
slide3()
slide4()
slide5()
slide6()
