#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel IG — as questões mais FÁCEIS do ENEM 2025 (Linguagens + Humanas), com o print de cada.
Capa + grade LC + grade CH. Thumbnails recortados do caderno Azul dia 1. Marca XTRI."""
import json
import sys
from pathlib import Path
import matplotlib.image as mpimg
from PIL import Image

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64
FACIL = "#56C2F2"
META = {it["n"]: it for it in json.loads((D / "faceis_meta.json").read_text())["itens"]}
LC = [26, 19, 18, 27, 12, 22]
CH = [57, 73, 77, 71, 56, 61]


def vir(x):
    return f"{x:.1f}".replace(".", ",")


def thumb(ax, n, x0, y0, cw, ch, accent):
    """desenha o thumbnail (topo do print) da questão n numa célula cw×ch (y para baixo)."""
    rr = None
    im = Image.open(META[n]["crop"]).convert("RGB")
    iw, ih = im.size
    scale = cw / iw
    disp_h = ih * scale
    if disp_h > ch:                      # mostra só o topo
        im = im.crop((0, 0, iw, int(ch / scale)))
    else:
        ch = disp_h
    arr = mpimg.pil_to_array(im)
    ax.imshow(arr, extent=(x0, x0 + cw, y0 + ch, y0), zorder=3, aspect="auto")
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((x0, y0), cw, ch, fill=False, ec="#DADBDD", lw=1.1, zorder=4))
    ax.add_patch(Rectangle((x0, y0), 6, ch, fc=accent, ec="none", zorder=5))
    return ch


def grade(fig, ax, hp, qs, area_nome, accent, tag, idx):
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, tag, monoB, 11.5, GRAY, ha="right", va="center")
    ty = 176
    txt(M, ty, area_nome.upper(), outfitB, 44, accent)
    txt(M, ty + 46, "AS 6 QUESTÕES MAIS FÁCEIS", outfitB, 26, INK)
    txt(M, ty + 82, "com o print de cada uma · % = quem acertou · caderno Azul, ENEM 2025", outfit, 13.5, GRAY)

    cols, rows = 3, 2
    gap = 20
    cw = (W - 2 * M - (cols - 1) * gap) / cols
    th = 300
    lab_h = 96
    gy0 = ty + 116
    for i, n in enumerate(qs):
        r, c = divmod(i, cols)
        x0 = M + c * (cw + gap)
        y0 = gy0 + r * (th + lab_h + 24)
        real_th = thumb(ax, n, x0, y0, cw, th, accent)
        # faixa de rótulo
        ly = y0 + th + 8
        it = META[n]
        txt(x0, ly + 24, f"Q{n}", outfitB, 26, INK)
        rrect(x0 + tw(f"Q{n}  ", outfitB, 26), ly + 6, 96, 26, 7, "#E7F6FE", z=4)
        txt(x0 + tw(f"Q{n}  ", outfitB, 26) + 12, ly + 24, "FÁCIL", monoB, 11, "#1597D8", z=5)
        txt(x0, ly + 54, f"{vir(it['pct'])}% acertaram", outfitB, 16, accent, z=5)
        txt(x0, ly + 80, f"dif TRI {it['dif']} · {area_nome}", mono, 11, GRAY, z=5)

    fy = H - 62
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · caderno Azul, 1ª aplicação · dif TRI = b×100+500 (Fácil ≤ 548)", mono, 9, GRAY)
    txt(W - M, fy, idx, monoB, 11, GRAY, ha="right")
    return save(fig, f"c{idx[0]}_{area_nome.lower()}")


# ---------- capa ----------
def capa():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · CADERNO AZUL", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 190
    txt(M, ty, "AS QUESTÕES MAIS", outfitB, 46, INK)
    txt(M, ty + 56, "FÁCEIS DO ENEM 2025", outfitB, 46, CYANd)
    txt(M, ty + 104, "Linguagens & Humanas — as que MAIS gente acertou, com o print", outfit, 17, GRAY)
    txt(M, ty + 130, "de cada uma. Deslize e veja se você teria acertado.", outfit, 17, GRAY)

    # print da mais fácil (Q26) em destaque
    cw = W - 2 * M
    y0 = ty + 176
    tmax = H - 300 - y0
    real = thumb(ax, 26, M, y0, cw, tmax, CYANd)

    py = y0 + real + 22
    hh = H - 96 - py
    shadow(M, py, cw, hh, 18); rrect(M, py, cw, hh, 18, CARD, z=6); rrect(M, py, 10, hh, 5, CYANd, z=7)
    txt(M + 34, py + 52, "A MAIS FÁCIL DE 2025: Q26 de Linguagens", outfitB, 20, INK, z=8)
    txt(M + 34, py + 88, "87% do Brasil acertou (variação linguística). Nenhuma de", outfit, 15.5, INK, z=8)
    txt(M + 34, py + 116, "Humanas chegou perto: a mais fácil delas teve 60%.", outfit, 15.5, INK, z=8)

    fy = H - 62
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · caderno Azul, 1ª aplicação", mono, 9.5, GRAY)
    txt(W - M, fy, "1/3", monoB, 11, GRAY, ha="right")
    return save(fig, "c1_capa")


if __name__ == "__main__":
    capa()
    fig, ax, hp = new_slide(w=W, h=H); grade(fig, ax, hp, LC, "Linguagens", CYANd, "MAIS FÁCEIS · LINGUAGENS", "2/3")
    fig, ax, hp = new_slide(w=W, h=H); grade(fig, ax, hp, CH, "Humanas", CORAL, "MAIS FÁCEIS · HUMANAS", "3/3")
