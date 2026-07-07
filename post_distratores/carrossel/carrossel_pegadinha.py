#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carrossel IG — anatomia de uma pegadinha real do ENEM 2025 (Ciências da Natureza, Q111).
6 slides, feed 1080x1350. Reusa xtri_deck (marca XTRI).
"""
import sys
from pathlib import Path

import matplotlib.image as mpimg

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64

LETRAS = [("A", 45.9, "distrator campeão — ERRADA"), ("B", 16.5, "GABARITO (certa)"),
          ("C", 23.5, "errada"), ("D", 6.8, "errada"), ("E", 7.4, "errada")]


def header(hp, tag, titulo1, titulo2=None, cor2=CORAL):
    txt = hp["txt"]
    logo(hp["ax"], M + 118, 84, zoom=0.062)
    txt(W - M, 90, tag, monoB, 11.5, GRAY, ha="right", va="center")
    ty = 190
    txt(M, ty, titulo1, outfitB, 34, INK)
    if titulo2:
        txt(M, ty + 56, titulo2, outfitB, 34, cor2)
    return ty


def footer_slide(hp, n_total, n_atual, show_fonte=True):
    txt = hp["txt"]
    fy = H - 56
    if show_fonte:
        txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP", mono, 9.5, GRAY)
    txt(W - M, fy, f"{n_atual}/{n_total}", monoB, 11, GRAY, ha="right")


def slide1():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    hp["ax"] = ax
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENEM 2025 · MAPA DE DISTRATORES", monoB, 11.5, GRAY, ha="right", va="center")

    ty = 420
    txt(M, ty, "VOCÊ CAIRIA NESSA", outfitB, 46, INK)
    txt(M, ty + 56, "PEGADINHA DO ENEM 2025?", outfitB, 46, CORAL)

    hy = ty + 140
    hh = 300
    shadow(M, hy, W - 2 * M, hh, 20)
    rrect(M, hy, W - 2 * M, hh, 20, CARD, z=3)
    txt(M + 40, hy + 56, "Nesta questão real de Ciências da Natureza,", outfit, 19, INK, z=5)
    txt(M + 40, hy + 90, "quase 3× mais gente ERROU para UMA alternativa", outfit, 19, INK, z=5)
    txt(M + 40, hy + 124, "específica do que ACERTOU.", outfit, 19, INK, z=5)
    txt(M + 40, hy + 182, "792 mil candidatos.", outfitB, 24, CORAL, z=5)
    txt(M + 40, hy + hh - 34, "Qual alternativa você marcaria? Desliza →", mono, 13.5, GRAY, z=5)

    y2 = hy + hh + 90
    txt(M, y2, "Uma pegadinha, na TRI, não é a questão mais difícil —", outfit, 17, GRAY)
    txt(M, y2 + 28, "é a que empurra quase todo mundo pro MESMO erro.", outfit, 17, GRAY)

    y3 = y2 + 90
    ax.plot([M, W - M], [y3, y3], color="#D9D9D9", lw=1, zorder=2)
    txt(W / 2, y3 + 46, "É DADO REAL. NÃO É ESTIMATIVA.", monoB, 13, GRAY, ha="center")
    txt(W / 2, y3 + 74, "792.190 candidatos presentes nesta questão", mono, 12, GRAY, ha="center")

    footer_slide(hp, 6, 1)
    return save(fig, "slide1_capa")


def slide2():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; hp["ax"] = ax
    ty = header(hp, "A QUESTÃO REAL", "A QUESTÃO REAL DO ENEM 2025", "CIÊNCIAS DA NATUREZA · Q111", CYANd)

    img = mpimg.imread(str(D / "q111_enem2025.png"))
    ih, iw = img.shape[0], img.shape[1]
    card_w = W - 2 * M
    y0 = ty + 116
    card_h = H - y0 - 130
    scale = min(card_w / iw, card_h / ih)
    disp_w, disp_h = iw * scale, ih * scale
    x0 = M + (card_w - disp_w) / 2
    ax.imshow(img, extent=(x0, x0 + disp_w, y0 + disp_h, y0), zorder=3)
    ax.add_patch(__import__("matplotlib.patches", fromlist=["Rectangle"]).Rectangle(
        (x0, y0), disp_w, disp_h, fill=False, ec="#D9D9D9", lw=1.2, zorder=4))

    txt(M, y0 + disp_h + 40, "Pensa na tua resposta antes de ver o resultado real →", mono, 12.5, GRAY)
    footer_slide(hp, 6, 2)
    return save(fig, "slide2_questao")


def slide3():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    hp["ax"] = ax
    ty = header(hp, "O RESULTADO REAL", "O RESULTADO REAL", "792 MIL CANDIDATOS", CORAL)

    gy0 = ty + 90
    gh = 560
    base = gy0 + gh
    n = len(LETRAS)
    group_w = (W - 2 * M) / n
    bw = group_w * 0.6
    maxv = max(v for _, v, _ in LETRAS)
    scale = gh / (maxv * 1.2)

    for letra, pct, rotulo in LETRAS:
        i = "ABCDE".index(letra)
        gx = M + i * group_w + (group_w - bw) / 2
        hgt = pct * scale
        is_gab = letra == "B"
        is_campeao = letra == "A"
        cor = CYANd if is_gab else (CORAL if is_campeao else "#C7CBD0")
        rrect(gx, base - hgt, bw, hgt, 10, cor, z=3)
        txt(gx + bw / 2, base - hgt - 16, f"{pct}%".replace(".", ","), outfitB, 21,
            CYANd if is_gab else (CORALd if is_campeao else "#6B7076"), ha="center", z=5)
        txt(gx + bw / 2, base + 32, letra, outfitB, 22, INK, ha="center", z=5)
        tag = "gabarito" if is_gab else ("campeã" if is_campeao else "")
        if tag:
            txt(gx + bw / 2, base + 60, tag, mono, 10.5, GRAY, ha="center", z=5)

    hy = base + 110
    hh = 190
    shadow_fn = hp["shadow"]; shadow_fn(M, hy, W - 2 * M, hh, 20)
    rrect(M, hy, W - 2 * M, hh, 20, CARD, z=3)
    txt(M + 32, hy + 42, "A resposta CERTA (B) foi só a 3ª mais escolhida —", outfitB, 18, INK, z=5)
    txt(M + 32, hy + 72, "atrás de A (errada, 45,9%) e de C (errada, 23,5%).", outfitB, 18, INK, z=5)
    txt(M + 32, hy + hh - 26, "gabarito: eutrofização dos corpos de água", mono, 12, GRAY, z=5)

    footer_slide(hp, 6, 3)
    return save(fig, "slide3_resultado")


def slide4():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    hp["ax"] = ax
    ty = header(hp, "A ANATOMIA DA PEGADINHA", "POR QUE TANTA GENTE", "ERROU PRA ESSA ALTERNATIVA?", CORAL)

    y = ty + 90
    # certa
    hh1 = 190
    rrect(M, y, W - 2 * M, hh1, 18, "#EAF4FB", z=3)
    rrect(M, y, 10, hh1, 5, CYANd, z=4)
    txt(M + 34, y + 40, "B (certa) — eutrofização dos corpos de água:", outfitB, 16.5, INK, z=5)
    txt(M + 34, y + 72, "o excesso de nutrientes do adubo/dejeto que escoa pra", outfit, 14.5, INK, z=5)
    txt(M + 34, y + 98, "água faz algas crescerem demais e consome o oxigênio", outfit, 14.5, INK, z=5)
    txt(M + 34, y + 124, "da água — é um processo de EXCESSO DE NUTRIENTE.", outfit, 14.5, INK, z=5)
    txt(M + 34, y + hh1 - 22, "por isso a etapa 4 (usar como fertilizante controlado) evita isso", mono, 10.5, GRAY, z=5)

    y2 = y + hh1 + 26
    hh2 = 190
    rrect(M, y2, W - 2 * M, hh2, 18, "#FCEDE9", z=3)
    rrect(M, y2, 10, hh2, 5, CORALd, z=4)
    txt(M + 34, y2 + 40, "A (a pegadinha) — bioacumulação de toxinas:", outfitB, 16.5, INK, z=5)
    txt(M + 34, y2 + 72, "é o acúmulo de substâncias tóxicas (metal pesado,", outfit, 14.5, INK, z=5)
    txt(M + 34, y2 + 98, "agrotóxico) subindo na cadeia alimentar — um processo", outfit, 14.5, INK, z=5)
    txt(M + 34, y2 + 124, "DIFERENTE, sem relação com adubo orgânico.", outfit, 14.5, INK, z=5)
    txt(M + 34, y2 + hh2 - 22, "dejeto/resíduo ≠ tóxico — mas soa parecido", mono, 10.5, GRAY, z=5)

    y3 = y2 + hh2 + 30
    txt(M, y3, "A pegadinha: as duas alternativas 'soam' como problema", outfit, 15.5, GRAY)
    txt(M, y3 + 26, "ambiental de resíduo — só quem sabe a diferença entre", outfit, 15.5, GRAY)
    txt(M, y3 + 52, "os dois conceitos escapa da armadilha.", outfit, 15.5, GRAY)

    y4 = y3 + 110
    hh3 = 210
    shadow(M, y4, W - 2 * M, hh3, 20)
    rrect(M, y4, W - 2 * M, hh3, 20, CARD, z=3)
    txt(M + 36, y4 + 50, "NÃO É FALTA DE ESTUDO GERAL —", outfitB, 19, INK, z=5)
    txt(M + 36, y4 + 84, "É FALTA DE PRECISÃO NUM CONCEITO", outfitB, 19, INK, z=5)
    txt(M + 36, y4 + 118, "ESPECÍFICO.", outfitB, 19, CORAL, z=5)
    txt(M + 36, y4 + hh3 - 30, "quem revisa a diferença entre os dois termos, na próxima vez, acerta", mono, 11.5, GRAY, z=5)

    footer_slide(hp, 6, 4)
    return save(fig, "slide4_explicacao")


def slide5():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    hp["ax"] = ax
    ty = header(hp, "ISSO É UM PADRÃO", "ISSO NÃO É SÓ", "ESSA QUESTÃO", CORAL)

    txt(M, ty + 86, "Mapeei as 180 questões do caderno Azul do ENEM 2025.", outfit, 16.5, GRAY)

    hy = ty + 130
    hh = 220
    shadow(M, hy, W - 2 * M, hh, 20)
    rrect(M, hy, W - 2 * M, hh, 20, CARD, z=3)
    txt(M + 36, hy + 40, "EM 45 DE 180 QUESTÕES (25% DA PROVA)", monoB, 12, GRAY, z=5)
    txt(M + 36, hy + 100, "a alternativa errada mais marcada", outfitB, 24, INK, z=5)
    txt(M + 36, hy + 136, "venceu o próprio gabarito em popularidade.", outfitB, 24, CORAL, z=5)
    txt(M + 36, hy + hh - 24, "Ciências da Natureza (esta) é a área com o caso mais extremo", mono, 11, GRAY, z=5)

    y2 = hy + hh + 56
    txt(M, y2, "POR ÁREA, A PEGADINHA MAIS EFICAZ (% DE QUEM ERROU)", monoB, 12, GRAY)
    rows = [("Linguagens", "69,0%"), ("Ciências da Natureza", "67,7%"),
            ("Ciências Humanas", "57,8%"), ("Matemática", "57,3%")]
    ry = y2 + 56
    row_gap = 108
    for i, (nome, pct) in enumerate(rows):
        yy = ry + i * row_gap
        txt(M, yy, nome, outfitB, 22, INK)
        txt(W - M, yy, pct, outfitB, 30, CORALd, ha="right")
        if i < len(rows) - 1:
            ax.plot([M, W - M], [yy + 42, yy + 42], color="#DEE0E2", lw=1, zorder=2)

    y3 = ry + len(rows) * row_gap + 20
    txt(M, y3, "Análise completa das 180 questões: link no perfil.", mono, 12.5, GRAY)

    footer_slide(hp, 6, 5)
    return save(fig, "slide5_padrao")


def slide6():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    hp["ax"] = ax
    logo(ax, M + 118, 120, zoom=0.075)
    ty = 260
    txt(M, ty, "SALVA ESSE CARROSSEL", outfitB, 38, INK)
    txt(M, ty + 48, "E MANDA PRO GRUPO DE ESTUDOS", outfitB, 32, CORAL)

    txt(M, ty + 110, "% de acerto diz que uma questão foi difícil.", outfit, 17, GRAY)
    txt(M, ty + 138, "O mapa de distrator diz PRA ONDE o erro foi —", outfit, 17, GRAY)
    txt(M, ty + 166, "e é isso que se ataca em revisão.", outfit, 17, GRAY)

    # ---- stat de fechamento, centralizado, preenche o meio do card ----
    cy = ty + 320
    ch = 420
    shadow(M, cy, W - 2 * M, ch, 24)
    rrect(M, cy, W - 2 * M, ch, 24, CARD, z=3)
    txt(W / 2, cy + 130, "25%", outfitB, 96, CORAL, ha="center", z=5)
    txt(W / 2, cy + 210, "DA PROVA TEM UMA PEGADINHA REAL", outfitB, 22, INK, ha="center", z=5)
    txt(W / 2, cy + 246, "— mapeada item por item, questão por questão.", outfit, 16, GRAY, ha="center", z=5)
    ax.plot([W / 2 - 120, W / 2 + 120], [cy + 300, cy + 300], color="#E2E3E5", lw=1, zorder=4)
    txt(W / 2, cy + 340, "180 QUESTÕES · 4,81 MILHÕES DE CANDIDATOS", monoB, 11.5, GRAY, ha="center", z=5)
    txt(W / 2, cy + 368, "ANALISADOS — NADA ESTIMADO", monoB, 11.5, GRAY, ha="center", z=5)

    fy = H - 180
    txt(M, fy, "Fonte: Microdados ENEM 2025 / INEP · caderno Azul, 180 itens,", mono, 10, GRAY)
    txt(M, fy + 18, "itens anulados excluídos · streaming completo (4,81 mi de linhas)", mono, 10, GRAY)

    ay = fy + 60
    txt(M, ay, "Transformamos ", outfitB, 16, INK)
    xx = M + tw("Transformamos ", outfitB, 16)
    txt(xx, ay, "dados", outfitB, 16, CYAN); xx += tw("dados", outfitB, 16)
    txt(xx, ay, " em ", outfitB, 16, INK); xx += tw(" em ", outfitB, 16)
    txt(xx, ay, "aprovações", outfitB, 16, CORAL); xx += tw("aprovações", outfitB, 16)
    txt(xx, ay, ".", outfitB, 16, INK)
    txt(M, ay + 32, "@xandaoxtri · app.rankingenem.com", mono, 13, GRAY)

    footer_slide(hp, 6, 6, show_fonte=False)
    return save(fig, "slide6_cta")


if __name__ == "__main__":
    slide1(); slide2(); slide3(); slide4(); slide5(); slide6()
