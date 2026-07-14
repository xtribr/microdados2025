#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorta o print das 4 questões que mais separam 600 de 700 (uma por área), caderno Azul P1."""
import re
from pathlib import Path
import fitz

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
PROVAS = BASE / "PROVAS E GABARITOS"
D1 = PROVAS / "ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf"
D2 = PROVAS / "ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf"
OUT = BASE / "estudo_600_700/crops"; OUT.mkdir(parents=True, exist_ok=True)
DPI = 260
QS = [("LC", 32, D1), ("CH", 59, D1), ("CN", 127, D2), ("MT", 157, D2)]


def headers_on_page(page):
    words = page.get_text("words")
    out = []
    for i, w in enumerate(words):
        if re.match(r"QUEST[ÃA]O$", w[4].upper()):
            for j in range(i + 1, min(i + 3, len(words))):
                mm = re.match(r"0*(\d{1,3})$", words[j][4])
                if mm:
                    out.append((int(mm.group(1)), w[0], w[1])); break
    return out


def crop_q(area, n, pdf):
    doc = fitz.open(pdf); target = None
    for pi in range(doc.page_count):
        hs = headers_on_page(doc[pi])
        for (hn, hx, hy) in hs:
            if hn == n:
                target = (pi, hx, hy, hs); break
        if target: break
    if not target:
        print(f"  !! Q{n} ({area}) não encontrada"); return
    pi, hx, hy, hs = target; page = doc[pi]
    Wp, Hp = page.rect.width, page.rect.height
    left = hx < Wp / 2
    x0, x1 = (0.028 * Wp, 0.497 * Wp) if left else (0.503 * Wp, 0.972 * Wp)
    ytop = max(0, hy - 4); ybot = Hp * 0.955
    for (hn, x, y) in hs:
        if ((x < Wp / 2) == left) and y > hy + 6 and y < ybot: ybot = y - 4
    pix = page.get_pixmap(matrix=fitz.Matrix(DPI / 72.0, DPI / 72.0), clip=fitz.Rect(x0, ytop, x1, ybot))
    fp = OUT / f"q{n:03d}_{area}.png"; pix.save(str(fp))
    print(f"  Q{n:>3} {area} pg{pi+1} col={'esq' if left else 'dir'} {pix.width}x{pix.height} -> {fp.name}")


for area, n, pdf in QS:
    crop_q(area, n, pdf)
print("ok")
