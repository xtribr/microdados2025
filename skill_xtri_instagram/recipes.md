# XTRI · Receitas de card (copiar e adaptar)

Todos usam `xtri_deck.py`. Coordenadas em pixel, y para baixo. Gere SEMPRE feed + story.

## 0) Esqueleto do script (feed + story numa passada)

```python
import sys; sys.path.insert(0, "PASTA_DA_SKILL")
import xtri_deck as X
from xtri_deck import outfitB, outfit, mono, monoB, INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd

W, M = 1080, 64

def card(H, suf):
    fig, ax, hp = X.new_slide(W, H)
    txt, tw, rrect, shadow = hp["txt"], hp["tw"], hp["rrect"], hp["shadow"]
    X.logo(ax, 182, 84)
    txt(W - M, 90, "ENEM 2025 · TRI", monoB, 11.5, GRAY, ha="right", va="center")
    # ... conteúdo ...
    X.footer(hp, H, "Fonte: Microdados ENEM 2025 / INEP.", "1/6", w=W, m=M)
    return X.save(fig, f"c1_capa{suf}", outdir=".")

for H, suf in [(1350, ""), (1920, "_story")]:
    card(H, suf)
```

## 1) Capa — título-herói com palavra colorida + card-legenda

```python
ty = 200
txt(M, ty,        "AS QUESTÕES QUE",  outfitB, 58, INK)
txt(M, ty + 74,   "SEPARAM O",        outfitB, 58, INK)
txt(M + 6 + tw("SEPARAM O ", outfitB, 58), ty + 74, "600", outfitB, 58, CYANd)   # palavra em cor
txt(M, ty + 148,  "DO",               outfitB, 58, INK)
txt(M + 6 + tw("DO ", outfitB, 58), ty + 148, "700", outfitB, 58, CORAL)
txt(M, ty + 208,  "Subtítulo em uma ou duas linhas, cinza.", outfit, 21, GRAY)
# card-destaque (branco + faixa lateral + sombra SUAVE)
py, hh = ty + 300, 210
shadow(M, py, W - 2*M, hh, 20); rrect(M, py, W - 2*M, hh, 20, CARD, z=6); rrect(M, py, 11, hh, 5, CYANd, z=7)
txt(M + 40, py + 60, "Chamada do card", outfitB, 26, INK, z=8)
```
Regra: título grande → **entrelinha ≥ 1,3×** o tamanho (aqui 58pt → 74px) senão o acento colide.

## 2) Card de conteúdo (header + gráfico embutido)

```python
txt(M, 132, "TÍTULO DO CARD", outfitB, 40, CORAL)      # ou cor da área
txt(M, 152, "linha de apoio explicando o gráfico", outfit, 11.5, GRAY)
axc = fig.add_axes([M/W, 0.30, (W-2*M)/W, 0.40])       # eixo matplotlib DENTRO do card
# ... plote em axc (bar/scatter) usando as cores da marca ...
# deixe >=60px entre o eixo e o rodapé (não invada a banda do footer)
```

## 3) Card de estatística "X% → Y%" (a virada)

```python
cor = CYANd
py = 858; hh = 396
rrect(M, py, W - 2*M, hh, 18, CARD, z=6); rrect(M, py, 11, hh, 5, cor, z=7)
cy = py + hh/2
txt(M + 40, cy - 6, "14%", outfitB, 74, GRAY, va="center", z=8)
aw = tw("14% ", outfitB, 74)
txt(M + 40 + aw, cy - 6, "→", outfitB, 46, GRAY, va="center", z=8)
txt(M + 40 + aw + tw("→ ", outfitB, 46), cy - 6, "91%", outfitB, 74, cor, va="center", z=8)
rx = M + 40 + aw + tw("→ ", outfitB, 46) + tw("91%  ", outfitB, 74)
txt(rx, cy - 22, "acertaram", outfit, 17, INK, va="center", z=8)
txt(rx, cy + 4,  "quem tirou 600", mono, 13, GRAY, va="center", z=8)
txt(rx, cy + 26, "quem tirou 700", monoB, 13, cor, va="center", z=8)
```

## 4) Card com PRINT de questão recortado do caderno (fitz/pymupdf)

```python
import fitz, re
from PIL import Image
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

def crop_questao(pdf, n, dpi=260):
    doc = fitz.open(pdf)
    for pi in range(doc.page_count):
        words = doc[pi].get_text("words")
        heads = []
        for i, wd in enumerate(words):
            if re.match(r"QUEST[ÃA]O$", wd[4].upper()):
                for j in range(i+1, min(i+3, len(words))):
                    if re.match(r"0*(\d{1,3})$", words[j][4]):
                        heads.append((int(words[j][4]), wd[0], wd[1])); break
        tgt = [h for h in heads if h[0] == n]
        if not tgt:
            continue
        _, hx, hy = tgt[0]; Wp, Hp = doc[pi].rect.width, doc[pi].rect.height
        left = hx < Wp/2
        x0, x1 = (0.028*Wp, 0.497*Wp) if left else (0.503*Wp, 0.972*Wp)
        ybot = Hp*0.955
        for (hn, x, y) in heads:
            if (x < Wp/2) == left and y > hy+6 and y < ybot: ybot = y-4
        pix = doc[pi].get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72),
                                 clip=fitz.Rect(x0, max(0, hy-4), x1, ybot))
        out = f"q{n:03d}.png"; pix.save(out); return out

def thumb(ax, crop, x0, y0, cw, chmax, accent):   # mostra o TOPO do print numa moldura
    im = Image.open(crop).convert("RGB"); iw, ih = im.size; sc = cw/iw; dh = ih*sc
    if dh > chmax: im = im.crop((0, 0, iw, int(chmax/sc))); ch = chmax
    else: ch = dh
    ax.imshow(mpimg.pil_to_array(im), extent=(x0, x0+cw, y0+ch, y0), zorder=3, aspect="auto")
    ax.add_patch(Rectangle((x0, y0), cw, ch, fill=False, ec="#DADBDD", lw=1.2, zorder=4))
    ax.add_patch(Rectangle((x0, y0), 7, ch, fc=accent, ec="none", zorder=5))   # faixa lateral
    return ch
```
Nota: recorte da coluna esquerda pode "comer" o Q de QUESTÃO (vira UESTÃO) — o usuário aceita, o importante é preservar texto-base + alternativas.

## 5) Gráfico de barras manual (ex.: U-invertido) — sem depender de eixo mpl

```python
bx0 = M + 40; bw = (W - 2*M - 80) / len(BANDS); base = 900; scale = 7.0
for i, (lab, val, col) in enumerate(BANDS):          # BANDS = [("640–700", 31, CORAL), ...]
    x = bx0 + i*bw; bh = val*scale
    rrect(x + 14, base - bh, bw - 28, bh, 10, col, z=4)
    txt(x + bw/2, base - bh - 16, f"{val:.0f}", outfitB, 26, col, ha="center", z=5)
    txt(x + bw/2, base + 30, lab, mono, 12.5, GRAY, ha="center", z=5)
```

## 6) Tabela de ranking (linhas zebradas + linha destacada)

```python
x0, twid = M, W - 2*M; rowh = 24; y = 182
rrect(x0, y, twid, rowh, 6, INK, z=2)                          # cabeçalho escuro
# ... escreva os títulos de coluna em monoB branco ...
y += rowh
for k, row in enumerate(dados):
    hot = row["destaque"]
    rrect(x0, y, twid, rowh, 5, "#FFF0EC" if hot else (CARD if k%2==0 else "#F7F7F8"), z=2)
    if hot: rrect(x0, y, 5, rowh, 2, CORAL, z=3)               # faixa lateral no destaque
    # ... colunas: nome à esq (outfit), números à dir (mono); destaque em CORALd/bold ...
    y += rowh
```

## 7) Fecho / CTA (o último card)

```python
txt(M, 250, "O BIZU", outfitB, 54, INK)
txt(M, 324, "a ação em uma frase", CORAL := CORAL, 20, GRAY)   # linha de fecho
py, hh = 500, 250
shadow(M, py, W-2*M, hh, 20); rrect(M, py, W-2*M, hh, 20, CARD, z=6); rrect(M, py, 11, hh, 5, CORAL, z=7)
txt(M+40, py+60, "Na prática", outfitB, 24, INK, z=8)
txt(M+40, py+190, "Simule sua nota:", outfit, 17, GRAY, z=8)
txt(M+40, py+218, "xtri.online", monoB, 19, CYANd, z=8)        # CTA SEMPRE xtri.online
```

---
**Depois de rodar qualquer script: abra os PNGs e confira com zoom (regras invioláveis do SKILL.md). Se algo colidir ou vazar, ajuste as coordenadas e re-renderize antes de entregar.**
