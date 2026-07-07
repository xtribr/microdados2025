#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Série AUTÓPSIA TRI (3 posts, um por item anulado pela TRI no ENEM 2025):
 1/3 MT 97593  — convergência: gabarito A cai, D sobe (discriminação negativa)
 2/3 CN 96748  — convergência: curva em U do gabarito B
 3/3 CH 152715 — Bis<0,01: bisserial ~zero (2ª aplicação, n=309)
Feed 1080×1350 + Story 1080×1920 cada. Dados: anulados_curvas.csv + ch_bis_pares.json.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "palestra_2025"))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W = 1080
M = 64


def curva(co_item):
    out = {}
    with (D.parent / "palestra_2025/anulados_curvas.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["co_item"] == co_item and r["alt"] != "outros":
                out.setdefault(r["alt"], []).append((float(r["banda_meio"]), float(r["pct"])))
    for a in out:
        out[a].sort()
    return out


def rodape(hp, ax, H, l1, l2):
    txt = hp["txt"]; tw = hp["tw"]
    fy = H - 116
    txt(M, fy, l1, mono, 10, GRAY)
    txt(M, fy + 18, l2, mono, 10, GRAY)
    ay = H - 44
    txt(M, ay, "Transformamos ", outfitB, 15, INK)
    xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(W - M, ay, "@xandaoxtri · app.rankingenem.com", mono, 12, GRAY, ha="right")


def header(hp, ax, ty, kicker, t1, t2, sub1, sub2):
    txt = hp["txt"]
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, kicker, monoB, 13, GRAY, ha="right", va="center")
    txt(M, ty, t1, outfitB, 44, CORAL)
    txt(M, ty + 60, t2, outfitB, 44, INK)
    txt(M, ty + 112, sub1, outfit, 17, GRAY)
    txt(M, ty + 140, sub2, outfit, 17, GRAY)


def legenda_cores(hp, ax, x, y, itens):
    """Swatch colorido + rótulo, em linha. itens: [(cor, texto), ...]. Retorna x final."""
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    cx = x
    for cor, label in itens:
        rrect(cx, y - 10, 15, 15, 4, cor, z=6)
        txt(cx + 21, y + 3, label, mono, 12.5, INK, va="center", z=6)
        cx += 21 + tw(label, mono, 12.5) + 30
    return cx


def chart_curvas(hp, ax, gy0, gh, dados, foco, rival, header_lab):
    """Curvas por alternativa: foco coral (gabarito), rival cyan (mais marcada pelos
    melhores), demais em cinza como grupo — com legenda de cores explícita."""
    txt = hp["txt"]
    gx0, gx1 = M + 56, W - M - 120
    base = gy0 + gh

    def xx(n):
        return gx0 + (n - 325) / (825 - 325) * (gx1 - gx0)

    def yy(p):
        return base - p / 100 * gh

    # cabeçalho do gráfico + legenda de cores (acima da área de plotagem)
    txt(M, gy0 - 66, header_lab, monoB, 12, INK, z=3)
    legenda_cores(hp, ax, M, gy0 - 34, [
        (CORAL, f"gabarito oficial ({foco})"),
        (CYANd, f"mais marcada pelos melhores ({rival})"),
        ("#C7CBD0", "demais alternativas"),
    ])

    for v in (0, 25, 50, 75, 100):
        ax.plot([gx0, W - M], [yy(v), yy(v)], color="#E2E3E5", lw=1, zorder=1)
        txt(gx0 - 12, yy(v), f"{v}%", mono, 11, GRAY, ha="right", va="center", z=3)
    ax.plot([gx0, W - M], [yy(20), yy(20)], color="#8C9298", lw=1.5, linestyle=(0, (4, 4)), zorder=2)
    txt(gx1 - 4, yy(20) + 20, "acaso (20%)", mono, 11, GRAY, ha="right", z=3)

    # cinzas primeiro (sem rótulo individual — a legenda já cobre o grupo)
    for alt, pts in sorted(dados.items()):
        if alt in (foco, rival):
            continue
        xs = [xx(n) for n, _ in pts]
        ys = [yy(p) for _, p in pts]
        ax.plot(xs, ys, color="#C7CBD0", lw=1.6, zorder=3, solid_capstyle="round")

    # rival (cyan) e foco (coral) por cima, com rótulo só destes dois
    ends = []
    for alt, cor, lw, z in [(rival, CYANd, 3.0, 4), (foco, CORAL, 4.6, 5)]:
        pts = dados[alt]
        xs = [xx(n) for n, _ in pts]
        ys = [yy(p) for _, p in pts]
        ax.plot(xs, ys, color=cor, lw=lw, zorder=z, solid_capstyle="round")
        if alt == foco:
            ax.scatter(xs, ys, s=34, color=cor, zorder=z + 1)
        ends.append([ys[-1], alt, cor])
    ends.sort()
    if ends[1][0] - ends[0][0] < 34:
        ends[1][0] = ends[0][0] + 34
    if ends[-1][0] > base - 10:
        ends[-1][0] = base - 10
        ends[0][0] = min(ends[0][0], ends[-1][0] - 34)
    for ye, alt, cor in ends:
        txt(gx1 + 16, ye + 6, alt, outfitB, 19, cor, z=6)

    for n in (400, 500, 600, 700, 800):
        txt(xx(n), base + 26, str(n), mono, 11.5, GRAY, ha="center", z=3)
    txt((gx0 + gx1) / 2, base + 54, "nota TRI do aluno na área", outfit, 14.5, INK, ha="center", z=3)
    return base


def bloco_hero(hp, ax, hy, big, l1, l2):
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    hh = 132
    shadow(M, hy, W - 2 * M, hh, 18)
    rrect(M, hy, W - 2 * M, hh, 18, CARD, z=3)
    txt(M + 36, hy + 88, big, outfitB, 46, CORAL, z=5)
    bx = M + 36 + hp["tw"](big, outfitB, 46) + 26
    txt(bx, hy + 56, l1, outfitB, 19, INK, z=5)
    txt(bx, hy + 90, l2, outfit, 14.5, GRAY, z=5)
    return hy + hh


def bloco_hero_3(hp, ax, hy, itens, caption):
    """3 valores com rótulo próprio + seta entre eles + 1 linha de leitura embaixo.
    itens: [(valor_str, rotulo_str), ...] — ex.: [('26%','nota baixa'), ('17%','meio da prova'), ('69%','nota alta')].
    Cada bloco (valor + rótulo) é centralizado na MAIOR das duas larguras — evita rótulo comprido
    colidir com o próximo bloco."""
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    hh = 168
    shadow(M, hy, W - 2 * M, hh, 18)
    rrect(M, hy, W - 2 * M, hh, 18, CARD, z=3)
    blocos = [(val, rot, tw(val, outfitB, 34), tw(rot, mono, 12)) for val, rot in itens]
    arrow_w = tw("→", outfitB, 26)
    x = M + 36
    for i, (val, rot, vw, rw) in enumerate(blocos):
        bw = max(vw, rw)
        cx = x + bw / 2
        txt(cx - vw / 2, hy + 58, val, outfitB, 34, CORAL, z=5)
        txt(cx - rw / 2, hy + 84, rot, mono, 12, GRAY, z=5)
        x += bw
        if i < len(blocos) - 1:
            x += 16
            txt(x, hy + 56, "→", outfitB, 26, "#C7CBD0", z=5)
            x += arrow_w + 16
    txt(M + 36, hy + 128, caption, outfitB, 18.5, INK, z=5)
    return hy + hh


def bloco_leitura(hp, ax, ry, linhas):
    txt = hp["txt"]; rrect = hp["rrect"]
    rh = 34 + 34 * len(linhas) + 16
    rrect(M, ry, W - 2 * M, rh, 18, "#FCEDE9", z=3)
    rrect(M, ry, 10, rh, 5, CORAL, z=4)
    txt(M + 34, ry + 32, "A LEITURA TÉCNICA", monoB, 12, CORALd, z=5)
    for i, (s, fp, cor) in enumerate(linhas):
        txt(M + 34, ry + 66 + i * 34, s, fp, 17, cor, z=5)
    return ry + rh


def post_mt(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    story = H > 1400
    ty = 190 if not story else 244
    header(hp, ax, ty, "AUTÓPSIA TRI · 1 DE 3",
           "OS MELHORES MARCARAM D.", "O GABARITO OFICIAL DIZIA A.",
           "Matemática — anulada por “problema de convergência”: a calibração",
           "do 3PL não fechou. A curva empírica por alternativa mostra o porquê.")
    gy0 = ty + 232
    gh = 356 if not story else 456
    dados = curva("97593")
    base = chart_curvas(hp, ax, gy0, gh, dados, "A", "D",
                        "% QUE MARCOU CADA ALTERNATIVA — MT, ITEM ANULADO (GAB. A)")
    hy = bloco_hero(hp, ax, base + 84, "15% → 8%",
                    "a marcação do gabarito A CAI conforme a nota sobe",
                    "e a distratora D sobe a 73% nos melhores: discriminação negativa")
    bloco_leitura(hp, ax, hy + 26, [
        ("No 3PL, a ICC do gabarito tem que CRESCER com a proficiência (a > 0).", outfit, INK),
        ("Aqui ela cai — e uma distratora cresce no lugar. O estimador não converge.", outfit, INK),
        ("Sem parâmetros estáveis, o item não pode pontuar: a TRI anulou.", outfitB, CORALd),
    ])
    rodape(hp, ax, H,
           "Fonte: Microdados ENEM 2025 / INEP · Regular P1 · 3.176.102 respostas · motivo: 'Problema de convergência'",
           "curvas = % de marcação por faixa de 50 pts de nota · item anulado não entra na nota de ninguém")
    return save(fig, f"xtri_anulada_MT_{tag}")


def post_cn(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    story = H > 1400
    ty = 190 if not story else 244
    header(hp, ax, ty, "AUTÓPSIA TRI · 2 DE 3",
           "A CURVA EM U", "QUE O 3PL NÃO EXPLICA",
           "Ciências da Natureza — anulada por “problema de convergência”:",
           "o gabarito B se comporta de um jeito que o modelo proíbe.")
    gy0 = ty + 232
    gh = 356 if not story else 456
    dados = curva("96748")
    base = chart_curvas(hp, ax, gy0, gh, dados, "B", "E",
                        "% QUE MARCOU CADA ALTERNATIVA — CN, ITEM ANULADO (GAB. B)")
    hy = bloco_hero_3(hp, ax, base + 84,
                      [("26%", "nota baixa"), ("17%", "meio da escala"), ("69%", "nota alta")],
                      "o gabarito B cai abaixo do acaso no meio da prova e só domina no topo")
    bloco_leitura(hp, ax, hy + 26, [
        ("A ICC do 3PL é monotônica por construção: P(acerto) só sobe com a proficiência.", outfit, INK),
        ("Um U viola o modelo — padrão típico de item com dupla interpretação.", outfit, INK),
        ("Sem convergência não há A, B e C: item fora da régua, anulado.", outfitB, CORALd),
    ])
    rodape(hp, ax, H,
           "Fonte: Microdados ENEM 2025 / INEP · Regular P1 · 3.176.181 respostas · motivo: 'Problema de convergência'",
           "curvas = % de marcação por faixa de 50 pts de nota · theta = proficiência estimada pela TRI")
    return save(fig, f"xtri_anulada_CN_{tag}")


def post_ch(H, tag):
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]
    story = H > 1400
    ty = 190 if not story else 244
    header(hp, ax, ty, "AUTÓPSIA TRI · 3 DE 3",
           "BISSERIAL ZERO:", "O ITEM QUE NÃO MEDIA NADA",
           "Ciências Humanas (2ª aplicação) — anulada por “Bis<0,01”: correlação",
           "entre acertar o item e saber a matéria era praticamente nula.")
    # dados: terciles de ch_bis_pares.json
    pares = json.loads((D.parent / "palestra_2025/ch_bis_pares.json").read_text())
    pares = [(float(n), a) for n, a in pares if a in "ABCDE"]
    notas = sorted(n for n, _ in pares)
    q1, q2 = notas[len(notas) // 3], notas[2 * len(notas) // 3]
    grupos = [("nota baixa", lambda n: n <= q1), ("nota média", lambda n: q1 < n <= q2),
              ("nota alta", lambda n: n > q2)]
    gy0 = ty + 208
    gh = 330 if not story else 420
    base = gy0 + gh
    pw = (W - 2 * M - 2 * 36) / 3
    txt(M, gy0 - 16, "% QUE MARCOU CADA ALTERNATIVA — CH 2ª APLICAÇÃO (GAB. D)", monoB, 12, INK, z=3)
    for gi, (glab, cond) in enumerate(grupos):
        gx = M + gi * (pw + 36)
        sub = [a for n, a in pares if cond(n)]
        tot = len(sub)
        ax.plot([gx, gx + pw], [base, base], color="#C9CBCE", lw=1.6, zorder=2)
        # linha do acaso no painel
        ya = base - 20 / 78 * gh
        ax.plot([gx, gx + pw], [ya, ya], color="#8C9298", lw=1.2, linestyle=(0, (4, 4)), zorder=2)
        bw = pw / 5 * 0.72
        for ai, alt in enumerate("ABCDE"):
            pct = 100 * sub.count(alt) / tot
            bh = pct / 78 * gh
            bx = gx + ai * pw / 5 + (pw / 5 - bw) / 2
            cor = CORAL if alt == "D" else "#C7CBD0"
            rrect(bx, base - bh, bw, max(bh, 4), 6, cor, z=3)
            txt(bx + bw / 2, base - bh - 12, f"{pct:.0f}", monoB, 12.5, INK, ha="center", z=5)
            txt(bx + bw / 2, base + 22, alt, monoB, 12.5,
                CORALd if alt == "D" else GRAY, ha="center", z=5)
        txt(gx + pw / 2, base + 50, glab, outfitB, 15, INK, ha="center", z=5)
        txt(gx + pw / 2, base + 72, f"n = {tot}", mono, 10.5, GRAY, ha="center", z=5)
    txt(W - M, gy0 + 2, "linha tracejada = acaso (20%)", mono, 10.5, GRAY, ha="right", z=4)
    hy = bloco_hero(hp, ax, base + 104, "25 · 12 · 18",
                    "% que marca o gabarito D, do grupo fraco ao forte",
                    "não sobe com a nota — e os fortes preferem E (51%)")
    bloco_leitura(hp, ax, hy + 26, [
        ("A bisserial mede a correlação acerto × proficiência. Perto de zero,", outfit, INK),
        ("o item vira ruído: quem sabe não acerta mais do que quem não sabe.", outfit, INK),
        ("Amostra pequena (n=309, 2ª aplicação) amplia o dano — a TRI cortou.", outfitB, CORALd),
    ])
    rodape(hp, ax, H,
           "Fonte: Microdados ENEM 2025 / INEP · 2ª aplicação (reaplicação) · n = 309 respondentes · motivo oficial: 'Bis<0,01'",
           "grupos = tercis da nota de CH · barras = % de marcação por alternativa · gabarito oficial: D")
    return save(fig, f"xtri_anulada_CH_{tag}")


if __name__ == "__main__":
    for H, tag in [(1350, "feed"), (1920, "story")]:
        post_mt(H, tag)
        post_cn(H, tag)
        post_ch(H, tag)
