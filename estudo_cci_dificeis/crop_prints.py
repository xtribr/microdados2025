#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorta o print das 4 questões mais difíceis (uma por área) do ENEM 2025, caderno Azul P1.
Acha o header 'QUESTÃO N', detecta a coluna (prova em 2 colunas) e recorta do header
até o próximo header na MESMA coluna (ou rodapé). Saída: PNG por questão."""
import json
import re
from pathlib import Path
import fitz

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
PROVAS = BASE / "PROVAS E GABARITOS"
OUT = BASE / "estudo_cci_dificeis/prints"; OUT.mkdir(parents=True, exist_ok=True)
DPI = 260

# item -> (numero da questão no caderno, pdf, área)
ITENS = json.loads((BASE / "estudo_cci_dificeis.json").read_text())
PDF = {
    "LC": PROVAS / "ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf",
    "CH": PROVAS / "ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf",
    "CN": PROVAS / "ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf",
    "MT": PROVAS / "ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf",
}


def headers_on_page(page):
    """lista (num, x0, y0) de cada header 'QUESTÃO N' da página."""
    words = page.get_text("words")  # x0,y0,x1,y1,word,block,line,wno
    out = []
    for i, w in enumerate(words):
        if re.match(r"QUEST[ÃA]O$", w[4].upper()):
            for j in range(i + 1, min(i + 3, len(words))):
                mm = re.match(r"0*(\d{1,3})$", words[j][4])
                if mm:
                    out.append((int(mm.group(1)), w[0], w[1]))
                    break
    return out


def crop_q(area, n):
    doc = fitz.open(PDF[area])
    # acha a página do header da questão n
    target = None
    for pi in range(doc.page_count):
        hs = headers_on_page(doc[pi])
        for (hn, hx, hy) in hs:
            if hn == n:
                target = (pi, hx, hy, hs)
                break
        if target:
            break
    if not target:
        print(f"  !! Q{n} ({area}) não encontrada")
        return None
    pi, hx, hy, hs = target
    page = doc[pi]
    Wp, Hp = page.rect.width, page.rect.height
    left = hx < Wp / 2
    # colunas: um pouco mais à esquerda p/ preservar o 'Q' de QUESTÃO
    x0, x1 = (0.028 * Wp, 0.497 * Wp) if left else (0.503 * Wp, 0.972 * Wp)
    ytop = max(0, hy - 4)   # margem justa acima do header (evita a faixa de microtexto do topo)
    ybot = Hp * 0.955
    for (hn, x, y) in hs:
        same_col = (x < Wp / 2) == left
        if same_col and y > hy + 6 and y < ybot:
            ybot = y - 4
    mat = fitz.Matrix(DPI / 72.0, DPI / 72.0)
    clip = fitz.Rect(x0, ytop, x1, ybot)
    pix = page.get_pixmap(matrix=mat, clip=clip)
    fp = OUT / f"q{n:03d}_{area}.png"
    pix.save(str(fp))
    print(f"  Q{n:>3} {area}  pg{pi+1} col={'esq' if left else 'dir'}  "
          f"{pix.width}x{pix.height}  -> {fp.name}")
    return str(fp)


for it in ITENS:
    crop_q(it["area"], it["n"])
print("ok")
