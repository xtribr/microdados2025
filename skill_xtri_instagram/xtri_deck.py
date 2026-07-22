#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xtri_deck — helper de design da XTRI para artes de Instagram (matplotlib).
Padrão de marca: fundo claro, Outfit + JetBrains Mono, coral/cyan, logo X-TRI,
assinatura "Transformamos dados em aprovações.", CTA xtri.online.

USO:
    import xtri_deck as X
    fig, ax, hp = X.new_slide(*X.FEED)          # 1080x1350
    txt, tw, rrect, shadow = hp["txt"], hp["tw"], hp["rrect"], hp["shadow"]
    X.logo(ax, 182, 84)                          # topo-esquerda
    txt(64, 200, "TÍTULO", X.outfitB, 46, X.INK)
    X.footer(hp, ax, X.FEED[1], "Fonte: ...", "1/6")
    X.save(fig, "meu_card", outdir=".")

FONTES: aponte XTRI_FONT_DIR para uma pasta com Outfit-Bold.ttf, Outfit-Regular.ttf,
JetBrainsMono-Regular.ttf, JetBrainsMono-Bold.ttf (baixe em fonts.google.com).
Sem elas, cai num fallback (DejaVu) — funciona, mas perde a cara da marca.

GLIFOS QUE VIRAM "TOFU" na Outfit/JetBrains: ≥, ≤, θ, ² e emojis. Escreva
"10 ou mais", "theta", "a2", e nada de emoji no texto — use CAPS/→ para ênfase.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import font_manager as fm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import FancyBboxPatch, Circle

# ---------------- formatos ----------------
FEED = (1080, 1350)     # Instagram feed 4:5  (TODO post = feed + story)
STORY = (1080, 1920)    # Instagram story 9:16
WP = (1200, 630)        # capa WordPress / social

# ---------------- cores da marca ----------------
BG = "#F1F1F2"      # fundo (claro — PROIBIDO fundo preto)
CARD = "#FFFFFF"
INK = "#1D1D20"     # tinta (texto principal)
GRAY = "#8C9298"    # cinza (rótulos, notas)
CORAL = "#FA5230"; CORALd = "#E8431F"
CYAN = "#1FAFEF"; CYANd = "#1597D8"
# categorias de dificuldade (usar SÓ estas 4 quando o assunto for dificuldade TRI)
DIF_FACIL = "#56C2F2"; DIF_MEDIO = "#C7CBD0"; DIF_DIFICIL = "#FB9276"; DIF_MDIFICIL = "#FA5230"

# ---------------- fontes ----------------
_FONT_CANDIDATES = [
    os.environ.get("XTRI_FONT_DIR", ""),
    os.path.expanduser("~/.fonts/xtri"),
    os.path.expanduser("~/Library/Fonts"),
    "/usr/share/fonts/truetype",
]


def _find(name):
    for base in _FONT_CANDIDATES:
        if base and os.path.exists(os.path.join(base, f"{name}.ttf")):
            return fm.FontProperties(fname=os.path.join(base, f"{name}.ttf"))
    # fallback: tenta pelo nome instalado no sistema; senão DejaVu
    try:
        fam = {"Outfit-Bold": ("Outfit", "bold"), "Outfit-Regular": ("Outfit", "normal"),
               "JetBrainsMono-Bold": ("JetBrains Mono", "bold"),
               "JetBrainsMono-Regular": ("JetBrains Mono", "normal")}[name]
        path = fm.findfont(fm.FontProperties(family=fam[0], weight=fam[1]), fallback_to_default=False)
        return fm.FontProperties(fname=path)
    except Exception:
        print(f"[xtri_deck] AVISO: fonte {name} não encontrada — usando fallback. "
              f"Baixe Outfit e JetBrains Mono e aponte XTRI_FONT_DIR.")
        return fm.FontProperties(weight="bold" if "Bold" in name else "normal")


outfitB = _find("Outfit-Bold")
outfit = _find("Outfit-Regular")
monoB = _find("JetBrainsMono-Bold")
mono = _find("JetBrainsMono-Regular")

LOGO = os.environ.get("XTRI_LOGO", "")   # caminho do PNG do logo X-TRI (opcional)


# ---------------- slide base ----------------
def new_slide(w=FEED[0], h=FEED[1], bg=BG):
    """Cria uma arte com coordenadas em PIXEL (0,0 no topo-esq, y cresce p/ baixo).
    Retorna (fig, ax, helpers) onde helpers = {txt, tw, rrect, shadow, line}."""
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), w, h, boxstyle="square,pad=0", fc=bg, ec="none", zorder=0))
    fig.canvas.draw(); R = fig.canvas.get_renderer()
    PXU = fig.get_size_inches()[0] * fig.dpi / w

    def tw(s, fp, sz):
        t = ax.text(0, 0, s, fontproperties=fp, fontsize=sz); fig.canvas.draw()
        wd = t.get_window_extent(R).width / PXU; t.remove(); return wd

    def txt(x, y, s, fp, sz, c=INK, ha="left", va="baseline", z=5):
        return ax.text(x, y, s, fontproperties=fp, fontsize=sz, color=c, ha=ha, va=va, zorder=z)

    def rrect(x, y, ww, hh, rad, fc, z=2, ec="none", lw=0):
        ax.add_patch(FancyBboxPatch((x + rad, y + rad), ww - 2 * rad, hh - 2 * rad,
                     boxstyle=f"round,pad={rad}", fc=fc, ec=ec, lw=lw, zorder=z))

    def shadow(x, y, ww, hh, rad):
        """Sombra suave (sem deslocamento lateral, senão a caixa parece torta)."""
        for i in range(1, 7):
            rrect(x - i, y + 2 + 1.6 * i, ww + 2 * i, hh + i, rad + 1.1 * i, "#000000", z=1.5)

    def line(x1, y, x2, c="#E2E3E6", lw=1.2):
        ax.plot([x1, x2], [y, y], color=c, lw=lw, zorder=3, solid_capstyle="round")

    return fig, ax, {"tw": tw, "txt": txt, "rrect": rrect, "shadow": shadow, "line": line, "ax": ax, "fig": fig}


def logo(ax, x, y, zoom=0.062):
    """Logo X-TRI. box_alignment=(1,.5): x é a borda DIREITA do logo (topo-esq clássico: x~182)."""
    if LOGO and os.path.exists(LOGO):
        try:
            ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO), zoom=zoom), (x, y),
                          frameon=False, box_alignment=(1, 0.5), zorder=8)); return
        except Exception:
            pass
    ax.text(x, y, "X-TRI", fontproperties=outfitB, fontsize=26, color=INK, ha="right", va="center", zorder=8)


def assinatura(hp, x, y, sz=15):
    """Rodapé de marca: Transformamos [dados=cyan] em [aprovações=coral]."""
    txt, tw = hp["txt"], hp["tw"]
    for s, c in [("Transformamos ", INK), ("dados", CYAN), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
        txt(x, y, s, outfitB, sz, c); x += tw(s, outfitB, sz)


def footer(hp, h, source, pg, w=FEED[0], m=64):
    """Rodapé padrão: nota de fonte (mono, cinza, PEQUENA) + assinatura + paginação.
    Regra: fonte MENOR que o corpo; banda própria; nunca colar na assinatura."""
    txt = hp["txt"]
    hp["line"](m, h - 96, w - m)
    txt(m, h - 72, source, mono, 9, GRAY)          # nota de fonte <= 10pt
    assinatura(hp, m, h - 46, 15)                  # assinatura ~50px abaixo da nota
    txt(w - m, h - 46, pg, monoB, 12, GRAY, ha="right")


def assert_layout(blocks, h, w=FEED[0], footer_height=112, margin=32):
    """Valida blocos declarados como (nome, x, y, largura, altura).

    Use antes de ``save`` em artes sociais. A checagem é propositalmente rígida:
    detecta interseções, saída da tela e qualquer invasão da banda reservada ao
    rodapé. Elementos decorativos só entram na lista se puderem tocar texto.
    """
    errors = []
    for name, x, y, ww, hh in blocks:
        if x < margin or y < margin or x + ww > w - margin or y + hh > h - footer_height:
            errors.append(f"{name}: fora da área segura")
    for index, (name_a, x_a, y_a, w_a, h_a) in enumerate(blocks):
        for name_b, x_b, y_b, w_b, h_b in blocks[index + 1:]:
            if x_a < x_b + w_b and x_a + w_a > x_b and y_a < y_b + h_b and y_a + h_a > y_b:
                errors.append(f"sobreposição: {name_a} × {name_b}")
    if errors:
        raise ValueError("Layout XTRI inválido: " + "; ".join(errors))


def save(fig, name, outdir=".", bg=BG):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"{name}.png")
    fig.savefig(path, dpi=100, facecolor=bg); plt.close(fig)
    print("ok:", path); return path
