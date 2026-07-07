#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers compartilhados para os gráficos da apresentação XTRI 2025 (16:9, 1920x1080).
Padrão de marca: fundo #F1F1F2, card branco arredondado, Outfit + JetBrains Mono,
logo X-TRI, assinatura do Prof. Alexandre Emerson / rodapé INEP.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import font_manager as fm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import FancyBboxPatch

BASE = "/Volumes/Kingston 1/microdados_enem_2025"
FD = ("/Volumes/Kingston/Library/Application Support/Claude/local-agent-mode-sessions/"
      "skills-plugin/173c3dab-6f51-4ed6-920d-43825f73e36c/"
      "a32ba23c-1f19-4aa1-8eaf-390193971d87/skills/canvas-design/canvas-fonts")
LOGO = f"{BASE}/logo_xtri_marca_real.png"
OUTDIR = f"{BASE}/palestra_2025/graficos"


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
# categorias de dificuldade XTRI
DIF_FACIL = "#56C2F2"
DIF_MEDIO = "#C7CBD0"
DIF_DIFICIL = "#FB9276"
DIF_MDIFICIL = "#FA5230"

W, H = 1920, 1080


def new_slide(w=W, h=H):
    """Cria um slide 16:9 com fundo XTRI. Retorna (fig, ax, helpers dict)."""
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

    def shadow(x, y, ww, hh, rad):
        for i in range(1, 7):
            rrect(x - i, y + 2 + 1.6 * i, ww + 2 * i, hh + i, rad + 1.1 * i, "#000000", z=1.5)

    return fig, ax, {"tw": tw, "txt": txt, "rrect": rrect, "shadow": shadow, "PXU": PXU}


def logo(ax, x, y, zoom=0.10):
    try:
        ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=zoom), (x, y),
                                     frameon=False, box_alignment=(1, 0.5), zorder=8))
    except Exception:
        pass


def assinatura(hp, ax, x, y, extra=""):
    """Rodapé de marca: 'Transformamos dados em aprovações.' + fonte INEP + autoria."""
    txt = hp["txt"]; tw = hp["tw"]
    txt(x, y, "Transformamos ", outfitB, 15, INK)
    xx = x + tw("Transformamos ", outfitB, 15)
    txt(xx, y, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, y, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, y, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, y, ".", outfitB, 15, INK)
    txt(W - 60, y, f"Estudo XTRI · Prof. Alexandre Emerson · Microdados ENEM / INEP{extra}",
        mono, 11, GRAY, ha="right")


def style_axes(axc, xlabel, ylabel):
    for s in ["top", "right"]:
        axc.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        axc.spines[s].set_color("#CFD2D5")
    axc.set_xlabel(xlabel, fontproperties=outfit, fontsize=15, color=INK)
    axc.set_ylabel(ylabel, fontproperties=outfit, fontsize=15, color=INK)
    axc.tick_params(colors=GRAY, labelsize=11)
    for lab in axc.get_xticklabels() + axc.get_yticklabels():
        lab.set_fontproperties(mono)
        lab.set_fontsize(11)
    axc.grid(color="#E6E7E9", lw=0.9)
    axc.set_axisbelow(True)


def save(fig, name):
    import os
    os.makedirs(OUTDIR, exist_ok=True)
    path = f"{OUTDIR}/{name}.png"
    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)
    print(f"ok: {name}.png")
    return path
