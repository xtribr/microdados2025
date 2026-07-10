#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Card 'Voce perdeu tempo' -- 2 itens anulados por Problema de convergencia
(ENEM 2025, aplicacao regular). PADRAO VISUAL XTRI. Gera feed + story."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FD = "/Volumes/Kingston/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/173c3dab-6f51-4ed6-920d-43825f73e36c/a32ba23c-1f19-4aa1-8eaf-390193971d87/skills/canvas-design/canvas-fonts"
def F(n): return fm.FontProperties(fname=f"{FD}/{n}.ttf")
outfitB = F("Outfit-Bold"); outfit = F("Outfit-Regular")
mono = F("JetBrainsMono-Regular"); monoB = F("JetBrainsMono-Bold")
import os
BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE, "..", "..", "logo_xtri_marca_real.png")
IMG_Q125 = mpimg.imread(BASE + "/q125_teaser.png")
IMG_Q172 = mpimg.imread(BASE + "/q172_teaser.png")

BG = "#F1F1F2"; CARD = "#FFFFFF"; INK = "#1D1D20"; GRAY = "#8C9298"
CORAL = "#FA5230"; CORALd = "#E8431F"; CYAN = "#1FAFEF"; CYANd = "#1597D8"
CTA_BG = "#1B1B1E"; CTA_SUB = "#9AA0A6"
M = 72; W = 1080

LAY = {
  "feed": dict(H=1350, logoy=82, logoz=0.115, wmy=140, k1=100, k2=128,
    h1=232, h2=308, hsz=54, suby=364,
    qy=404, qh=372, qlabel_off=30, qimg_top_off=64, qimg_bot_pad=22,
    ey=800, eh=210, elab=846, eval_=902, esub=944,
    fhandle=1076, fsig=1124, fcap=1180, ctaon=True, ctay=1206, ctah=80),
  "story": dict(H=1920, logoy=140, logoz=0.135, wmy=204, k1=168, k2=200,
    h1=344, h2=440, hsz=60, suby=506,
    qy=560, qh=560, qlabel_off=34, qimg_top_off=70, qimg_bot_pad=26,
    ey=1160, eh=250, elab=1214, eval_=1280, esub=1328,
    fhandle=1502, fsig=1570, fcap=1650, ctaon=True, ctay=1688, ctah=110),
}

def fit_extent(img, x0, x1, y0, y1):
    """Encaixa a imagem (mantendo proporcao) dentro da caixa, centralizada."""
    ih, iw = img.shape[0], img.shape[1]
    box_w, box_h = x1 - x0, y1 - y0
    scale = min(box_w / iw, box_h / ih)
    dw, dh = iw * scale, ih * scale
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return [cx - dw / 2, cx + dw / 2, cy + dh / 2, cy - dh / 2]  # left,right,bottom,top (y invertido)

def render(fmt):
    L = LAY[fmt]; H = L["H"]
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), W, H, boxstyle="square,pad=0", fc=BG, ec="none", zorder=0))
    fig.canvas.draw(); R = fig.canvas.get_renderer(); PXU = fig.get_size_inches()[0] * fig.dpi / W

    def tw(s, fp, sz):
        t = ax.text(0, 0, s, fontproperties=fp, fontsize=sz); fig.canvas.draw()
        w = t.get_window_extent(R).width / PXU; t.remove(); return w

    def txt(x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
        return ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

    def rrect(x, y, w, h, rad, fc, z=2, alpha=1, ec="none", lw=0):
        ax.add_patch(FancyBboxPatch((x + rad, y + rad), w - 2 * rad, h - 2 * rad, boxstyle=f"round,pad={rad}",
                     fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha, mutation_aspect=1))

    def shadow(x, y, w, h, rad):
        for i in range(1, 9):
            rrect(x - 1.0 * i, y + 2.4 + 1.7 * i, w + 2.0 * i, h + 1.0 * i, rad + 1.2 * i, "#000000", z=1.5, alpha=0.012)

    # LOGO + wordmark
    try:
        ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=L["logoz"]),
            (M + 30, L["logoy"]), frameon=False, box_alignment=(0.5, 0.5), zorder=6))
    except Exception:
        pass
    txt(M, L["wmy"], "X-TRI", outfitB, 16, CYANd)
    # KICKER
    txt(W - M, L["k1"], "ITENS DA PROVA", outfitB, 16.5, INK, ha="right")
    txt(W - M, L["k2"], "ENEM 2025 · Aplicação regular", mono, 13, GRAY, ha="right")

    # HEADLINE
    a1 = "Você perdeu tempo"
    txt(M, L["h1"], a1, outfitB, L["hsz"], CORAL)
    b1 = "fazendo essas 2 questões."
    txt(M, L["h2"], b1, outfitB, L["hsz"], INK)
    # SUBHEAD
    s1 = "Nenhuma resposta contou pra nota "; s2 = "— não importa o que você marcou."
    txt(M, L["suby"], s1, outfitB, 19.5, INK)
    txt(M + tw(s1, outfitB, 19.5), L["suby"], s2, outfit, 19.5, GRAY)

    # ---- QUESTION CARDS (lado a lado) ----
    qy, qh = L["qy"], L["qh"]
    gap = 32; cw = (W - 2 * M - gap) / 2
    cards = [(M, IMG_Q125, "Questão 125", "Ciências da Natureza"),
             (M + cw + gap, IMG_Q172, "Questão 172", "Matemática")]
    for cx, img, qlabel, arealabel in cards:
        shadow(cx, qy, cw, qh, 22); rrect(cx, qy, cw, qh, 22, CARD, z=2)
        # imagem da questao real, encaixada dentro da area central do card
        ext = fit_extent(img, cx + 18, cx + cw - 18, qy + L["qimg_top_off"], qy + qh - L["qimg_bot_pad"] - 44)
        ax.imshow(img, extent=ext, zorder=3)
        # selo ANULADA
        bw, bh = cw - 36, 34
        rrect(cx + 18, qy + qh - bh - 16, bw, bh, 10, CORAL, z=4)
        txt(cx + cw / 2, qy + qh - 16 - bh / 2 + 1, "ANULADA — SEM VALOR NA NOTA",
            monoB, 11.3, "#FFFFFF", ha="center", va="center", z=5)
        # label acima da imagem
        txt(cx + 18, qy + L["qlabel_off"], qlabel, outfitB, 17, INK)
        txt(cx + cw - 18, qy + L["qlabel_off"], arealabel, mono, 11.5, GRAY, ha="right")

    # ---- HERO EXPLICACAO ----
    ey, eh = L["ey"], L["eh"]
    shadow(M, ey, W - 2 * M, eh, 26); rrect(M, ey, W - 2 * M, eh, 26, CARD, z=2)
    txt(M + 40, L["elab"], "MOTIVO OFICIAL (INEP) — TX_MOTIVO_ABAN", mono, 13, GRAY)
    txt(M + 40, L["eval_"], "Problema de convergência", outfitB, 30, CORALd)
    sub1 = "O modelo estatístico do TRI nunca fechou uma dificuldade pra esses"
    sub2 = "2 itens — por isso a resposta de ninguém entrou na correção."
    txt(M + 40, L["esub"], sub1, outfit, 16, INK)
    txt(M + 40, L["esub"] + 26, sub2, outfit, 16, INK)

    # ---- FOOTER ----
    txt(M, L["fhandle"], "@xandaoxtri", outfitB, 28, INK)
    fy = L["fsig"]
    s1 = "Transformamos "; s2 = "dados"; s3 = " em "; s4 = "aprovações"; s5 = "."
    xx = M
    txt(xx, fy, s1, outfitB, 23, INK); xx += tw(s1, outfitB, 23)
    txt(xx, fy, s2, outfitB, 23, CYAN); xx += tw(s2, outfitB, 23)
    txt(xx, fy, s3, outfitB, 23, INK); xx += tw(s3, outfitB, 23)
    txt(xx, fy, s4, outfitB, 23, CORAL); xx += tw(s4, outfitB, 23)
    txt(xx, fy, s5, outfitB, 23, INK)
    txt(M, L["fcap"], "Fonte: Microdados ENEM 2025 / INEP — DADOS/ITENS_PROVA_2025.csv", mono, 11.5, GRAY)

    if L["ctaon"]:
        cax, cay, caw, cah = 630, L["ctay"], W - M - 630, L["ctah"]
        rrect(cax, cay, caw, cah, 22, CTA_BG, z=3)
        txt(cax + 28, cay + 38, "VEJA O ESTUDO", mono, 11.5, CTA_SUB)
        txt(cax + 28, cay + 70, "xtri.online →", monoB, 14.5, "#FFFFFF")

    out = f"{BASE}/card_{fmt}.png"
    fig.savefig(out, dpi=300, facecolor=BG); plt.close(fig)
    print("salvo", out)

for f in ("feed", "story"):
    render(f)
