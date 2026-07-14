#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige, na PROPRIA fonte (glyf table), a distancia vertical entre marca
diacritica (acento) e a letra-base, para todo glifo composto acentuado.
Causa raiz confirmada via fontTools: no Outfit-Bold, o gap letra-base -> acento
e de apenas ~4-6% do em-square (vs ~6-7% no Regular) -- no peso Bold, com
traco mais grosso, esse gap renderiza como "colado"/sobreposto em tamanhos
grandes (ex.: 44pt), especialmente com anti-aliasing. Isso afeta TODAS as
maiusculas/minusculas acentuadas em Bold (Ã, Õ, Í, Ê, Á, ã, ê, í ...), nao so
o "NAO SOBE" reportado -- por isso o fix e feito na fonte (uma vez), nao
em cada chamada de texto.

Estrategia: para cada glifo composto cuja marca e um acento/diacritico
conhecido, se o gap atual (topo da base -> base do acento) for menor que
TARGET_GAP_PCT do unitsPerEm, empurra o componente do acento para cima o
suficiente para atingir esse minimo. Nao mexe em glifos que ja tem folga
suficiente (preserva o desenho original sempre que possivel).
"""
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import re

FD = "/sessions/kind-gracious-heisenberg/mnt/.claude/skills/canvas-design/canvas-fonts"
OUT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"

TARGET_GAP_PCT = 0.12  # 12% do em-square de folga minima entre base e acento

# Apenas marcas que ficam ACIMA da letra-base (acento agudo/grave/til/circunflexo/
# trema/breve/anel/macron/ponto). NAO inclui cedilha/ogonek/caron/virgula-abaixo,
# que se prendem por BAIXO da letra (geometria oposta -- around/soltar essas
# quebraria ç, ą, ř etc.). uni0237 (dotless-j) tambem fica de fora: e uma letra-base,
# nao uma marca.
MARK_PATTERN = re.compile(
    r"^(acutecomb|gravecomb|tildecomb|uni0302|uni0304|uni0306|uni0307|uni0308|uni030A|"
    r"acute|grave|tilde|circumflex|breve|ring|macron|dotaccent)$"
)


def fix_font(src, dst):
    f = TTFont(src)
    glyf = f["glyf"]
    gs = f.getGlyphSet()
    upm = f["head"].unitsPerEm
    target_gap = TARGET_GAP_PCT * upm

    n_fixed, n_skip_multi, n_ok = 0, 0, 0
    report = []

    for name in list(glyf.keys()):
        g = glyf[name]
        if g.numberOfContours is None or g.numberOfContours >= 0:
            continue  # glifo simples, nao composto
        comps = g.components
        marks = [c for c in comps if MARK_PATTERN.match(c.glyphName)]
        bases = [c for c in comps if not MARK_PATTERN.match(c.glyphName)]
        if len(marks) != 1 or len(bases) != 1:
            if marks:
                n_skip_multi += 1
            continue  # so tratamos o caso comum: 1 base + 1 marca

        base_c, mark_c = bases[0], marks[0]
        if not (hasattr(base_c, "x") and hasattr(mark_c, "x")):
            continue  # componente com transform/escala -- nao mexe (caso raro aqui)

        pen = BoundsPen(gs)
        gs[base_c.glyphName].draw(pen)
        if pen.bounds is None:
            continue
        base_top = pen.bounds[3]

        pen2 = BoundsPen(gs)
        gs[mark_c.glyphName].draw(pen2)
        if pen2.bounds is None:
            continue
        mark_bottom_abs = pen2.bounds[1] + mark_c.y

        gap = mark_bottom_abs - base_top
        # guarda de seguranca: so mexe se a marca ja esta ACIMA da base (gap >= 0)
        # e so faltando folga (gap < alvo). Gap negativo/absurdo = geometria que o
        # heuristico nao entende (marca abaixo, base errada etc.) -- nao tocar.
        if 0 <= gap < target_gap:
            shift = int(round(target_gap - gap))
            mark_c.y = int(mark_c.y) + shift
            n_fixed += 1
            report.append((name, gap, gap + shift))
        elif gap >= target_gap:
            n_ok += 1
        else:
            n_skip_multi += 1  # gap negativo/anomalo -- geometria nao reconhecida, ignorado

    f.save(dst)
    print(f"{src.split('/')[-1]} -> {dst.split('/')[-1]}: "
          f"{n_fixed} glifos corrigidos, {n_ok} ja OK, {n_skip_multi} multi-marca ignorados (upm={upm})")
    for name, before, after in report[:200]:
        print(f"    {name:20s} gap {before:5.1f} -> {after:5.1f}")
    return report


if __name__ == "__main__":
    fix_font(f"{FD}/Outfit-Bold.ttf", f"{OUT}/Outfit-Bold-Fixed.ttf")
    print()
    fix_font(f"{FD}/Outfit-Regular.ttf", f"{OUT}/Outfit-Regular-Fixed.ttf")
