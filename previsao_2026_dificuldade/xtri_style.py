#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helpers de marca XTRI (adaptado de palestra_2025/xtri_deck.py, paths corrigidos p/ esta sessao)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import font_manager as fm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import FancyBboxPatch

FD = "/sessions/kind-gracious-heisenberg/mnt/.claude/skills/canvas-design/canvas-fonts"
OUTFD = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"
LOGO = "/sessions/kind-gracious-heisenberg/mnt/microdados_enem_2025/logo_xtri_marca_real.png"


def F(n):
    return fm.FontProperties(fname=f"{FD}/{n}.ttf")


# Outfit-Bold/Regular ORIGINAIS tem um bug de fonte: o gap vertical entre a
# letra-base e o acento (~, ´, ^) em glifos compostos e de so ~4-6% do
# em-square no peso Bold (~6-7% no Regular) -- insuficiente, renderiza como
# acento "colado"/sobreposto na letra em tamanhos grandes (ex.: "NÃO", "DIFÍCIL",
# "CIÊNCIAS" em titulos 40+pt). Corrigido uma vez, na propria fonte (glyf table,
# via fix_accent_font.py), empurrando so o componente do acento pra cima o
# suficiente pra garantir >=12% de gap -- sem mexer em glifos ja OK (cedilha,
# ogonek etc., que se prendem por BAIXO, ficam intocados). Ver fix_accent_font.py.
outfitB = fm.FontProperties(fname=f"{OUTFD}/Outfit-Bold-Fixed.ttf")
outfit = fm.FontProperties(fname=f"{OUTFD}/Outfit-Regular-Fixed.ttf")
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


def new_canvas(w, h):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), w, h, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    PXU = fig.get_size_inches()[0] * fig.dpi / w

    def tw(s, fp, sz):
        t = ax.text(0, 0, s, fontproperties=fp, fontsize=sz)
        fig.canvas.draw()
        wd = t.get_window_extent(R).width / PXU
        t.remove()
        return wd

    def txt(x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
        return ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

    def rrect(x, y, ww, hh, rad, fc, z=2, ec="none", lw=0):
        ax.add_patch(FancyBboxPatch((x + rad, y + rad), ww - 2 * rad, hh - 2 * rad,
                                    boxstyle=f"round,pad={rad}", fc=fc, ec=ec, lw=lw,
                                    zorder=z, mutation_aspect=1))

    return fig, ax, {"tw": tw, "txt": txt, "rrect": rrect, "w": w, "h": h}


def add_logo(ax, x, y, zoom=0.10):
    try:
        ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=zoom), (x, y),
                                     frameon=False, box_alignment=(0, 0.5), zorder=8))
    except Exception as e:
        print("logo falhou:", e)


def assinatura(hp, x, y, small=False):
    txt = hp["txt"]; tw = hp["tw"]
    sz = 13 if small else 15
    txt(x, y, "Transformamos ", outfitB, sz, INK)
    xx = x + tw("Transformamos ", outfitB, sz)
    txt(xx, y, "dados", outfitB, sz, CYAN); xx += tw("dados", outfitB, sz)
    txt(xx, y, " em ", outfitB, sz, INK); xx += tw(" em ", outfitB, sz)
    txt(xx, y, "aprovações", outfitB, sz, CORAL); xx += tw("aprovações", outfitB, sz)
    txt(xx, y, ".", outfitB, sz, INK)


def style_axes(axc, ylabel="", xlabel=""):
    for s in ["top", "right"]:
        axc.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        axc.spines[s].set_color("#CFD2D5")
    if ylabel:
        axc.set_ylabel(ylabel, fontproperties=outfit, fontsize=11, color=INK)
    if xlabel:
        axc.set_xlabel(xlabel, fontproperties=outfit, fontsize=11, color=INK)
    axc.tick_params(colors=GRAY, labelsize=9)
    for lab in axc.get_xticklabels() + axc.get_yticklabels():
        lab.set_fontproperties(mono)
        lab.set_fontsize(9)
    axc.grid(color="#E6E7E9", lw=0.8)
    axc.set_axisbelow(True)


def save(fig, path):
    fig.savefig(path, facecolor=BG)
    plt.close(fig)
    print("salvo:", path)
