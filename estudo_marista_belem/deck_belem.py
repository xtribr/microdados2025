#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deck 16:9 (1920x1080) — apresentação do estudo Marista Nazaré (Belém/PA) na escola.
Slides custom via xtri_deck + gráficos 16:9 já renderizados (copiados numerados)
+ PDF final APRESENTACAO_marista_belem.pdf. Todos os números vêm dos arquivos
do estudo (resumo.json, rankings) — nada digitado à mão sem fonte.
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

D = Path(__file__).resolve().parent
sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H)

SL = D / "slides"
SL.mkdir(exist_ok=True)
X.OUTDIR = str(SL)
R = json.loads((D / "resumo.json").read_text())
RK = json.loads((D / "resumo_ranking_local.json").read_text())
ESCOLA = "Colégio Marista Nossa Senhora de Nazaré"
AREAS = [("LC", "Linguagens"), ("CH", "Humanas"), ("CN", "Natureza"), ("MT", "Matemática")]


def vir(x, d=1):
    return f"{float(x):.{d}f}".replace(".", ",")


def base_slide(kicker, titulo, sub=None):
    fig, ax, hp = new_slide()
    txt = hp["txt"]
    M = 90
    txt(M, 92, kicker, monoB, 15, CORALd)
    txt(M, 158, titulo, outfitB, 42, INK)
    if sub:
        txt(M, 204, sub, outfit, 19, GRAY)
    logo(ax, W - M, 110, zoom=0.10)
    assinatura(hp, ax, M, H - 46)
    return fig, ax, hp, M


# ---------------- 01 CAPA ----------------
def s01():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]
    M = 120
    rrect(0, 0, 26, H, 0, CORAL, z=1)
    txt(M, 300, "RAIO-X ENEM 2025 · MICRODADOS INEP", monoB, 17, CORALd)
    txt(M, 400, "Colégio Marista", outfitB, 76, INK)
    txt(M, 490, "Nossa Senhora de Nazaré", outfitB, 76, CORAL)
    txt(M, 570, "Belém/PA — a prova, os rankings e onde crescer em 2026", outfit, 27, GRAY)
    y = 690
    for s, cor in [("142 concluintes analisados aluno a aluno, item a item", INK),
                   ("Prova COP30/BAM — comparação justa: os 62 mil candidatos da mesma prova", INK),
                   ("Fonte oficial: Microdados ENEM 2025 e Censo Escolar 2025 / INEP", INK)]:
        txt(M, y, "•", outfitB, 22, CORAL)
        txt(M + 34, y, s, outfit, 22, cor)
        y += 56
    txt(M, 920, "Prof. Alexandre Emerson", outfitB, 24, INK)
    txt(M, 956, "XTRI · app.rankingenem.com · @xandaoxtri", mono, 15, GRAY)
    logo(ax, W - 110, 150, zoom=0.16)
    assinatura(hp, ax, M, H - 46)
    save(fig, "01_capa")


# ---------------- 02 METODOLOGIA ----------------
def s02():
    fig, ax, hp, M = base_slide("COMO O ESTUDO FOI FEITO", "Dado oficial, aluno a aluno, item a item",
                                "Nenhum número estimado: tudo sai dos microdados públicos do INEP.")
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    cards = [
        ("QUEM ENTRA NA CONTA", "142", "concluintes com escola declarada nos microdados. "
         "114 presentes nos 2 dias com as 5 notas — é com eles que se calcula média e ranking."),
        ("A PROVA DE BELÉM", "COP30", "Belém fez a aplicação COP30/BAM: outra prova, itens próprios. "
         "Validamos o gabarito item a item — zero divergências."),
        ("A RÉGUA CERTA", "62 mil", "candidatos de Belém, Ananindeua e Marituba fizeram a MESMA prova. "
         "É contra eles que comparamos acerto por item, não contra o Brasil."),
        ("CORREÇÃO ITEM A ITEM", "180", "itens objetivos corrigidos por aluno (45 por área), "
         "com dificuldade e discriminação da TRI de cada item."),
    ]
    cw = (W - 2 * 90 - 3 * 36) / 4
    y0, ch = 280, 470
    for i, (k, num, corpo) in enumerate(cards):
        x = 90 + i * (cw + 36)
        shadow(x, y0, cw, ch, 18)
        rrect(x, y0, cw, ch, 18, CARD, z=2)
        rrect(x, y0, cw, 10, 5, CORAL, z=3)
        txt(x + 30, y0 + 74, k, monoB, 13.5, CORALd, z=5)
        txt(x + 30, y0 + 170, num, outfitB, 52, INK, z=5)
        # corpo com quebra manual
        palavras = corpo.split()
        linha, yy = "", y0 + 236
        for p in palavras:
            t = (linha + " " + p).strip()
            if hp["tw"](t, outfit, 16.5) > cw - 60:
                txt(x + 30, yy, linha, outfit, 16.5, GRAY, z=5)
                yy += 30
                linha = p
            else:
                linha = t
        if linha:
            txt(x + 30, yy, linha, outfit, 16.5, GRAY, z=5)
    save(fig, "02_metodologia")


# ---------------- 03 RESULTADO GERAL ----------------
def s03():
    fig, ax, hp, M = base_slide("RESULTADO GERAL", "Bem acima da régua local em todas as áreas",
                                "Nota TRI média · a coorte COP30 fez a MESMA prova; Brasil Regular P1 como contexto.")
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    ty, rowh = 270, 92
    tw_all = W - 2 * M
    cols = [0.28, 0.24, 0.24, 0.24]
    heads = ["Área", "Marista Nazaré", "Coorte COP30", "Brasil (Regular P1)"]
    shadow(M, ty, tw_all, rowh * 6, 16)
    rrect(M, ty, tw_all, rowh * 6, 16, CARD, z=2)
    cx = M
    for j, hd in enumerate(heads):
        txt(cx + tw_all * cols[j] / 2, ty + rowh * 0.62, hd, monoB, 17,
            [INK, CORALd, GRAY, GRAY][j], ha="center", z=5)
        cx += tw_all * cols[j]
    ax.plot([M + 30, W - M - 30], [ty + rowh - 8, ty + rowh - 8], color="#E3E4E6", lw=1.6, zorder=4)
    linhas = [(n, R["medias_todos"][a], R["cop30"][a], R["nacional_regular_p1"][a]) for a, n in AREAS]
    linhas.append(("Redação", R["redacao_media"], R["cop30_redacao"]["media"], None))
    for i, (nome, e, c, b) in enumerate(linhas):
        yy = ty + (i + 1) * rowh
        if i % 2 == 0:
            rrect(M, yy, tw_all, rowh, 0, "#F7F7F8", z=2.5)
        cx = M
        txt(cx + tw_all * cols[0] / 2, yy + rowh * 0.62, nome, outfit, 24, INK, ha="center", z=5)
        cx += tw_all * cols[0]
        for j, v in enumerate([e, c, b]):
            s = vir(v) if v is not None else "—"
            txt(cx + tw_all * cols[j + 1] / 2, yy + rowh * 0.62, s,
                outfitB if j == 0 else mono, 30 if j == 0 else 22,
                [CORALd, GRAY, GRAY][j], ha="center", z=5)
            cx += tw_all * cols[j + 1]
    by = ty + rowh * 6 + 44
    rrect(M, by, tw_all, 110, 16, "#FCEDE9", z=2)
    rrect(M, by, 12, 110, 6, CORAL, z=3)
    dmt = R["medias_todos"]["MT"] - R["cop30"]["MT"]
    txt(M + 44, by + 46, "DESTAQUE", monoB, 14, CORALd, z=5)
    txt(M + 44, by + 86, f"Matemática: 669,7 — {vir(dmt, 0)} pontos acima da coorte da mesma prova. "
        f"Redação 830,6 contra 609,2 da coorte.", outfit, 22, INK, z=5)
    save(fig, "03_resultado_geral")


# ---------------- 04 RANKING LOCAL ----------------
def s04():
    fig, ax, hp, M = base_slide("RANKING LOCAL — POR ÁREA",
                                "Top-7 de Belém, com o maior N do grupo da frente",
                                "Média dos presentes nos 2 dias com as 5 notas · escolas com 10+ alunos · nomes do Censo Escolar 2025.")
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    ty, rowh = 276, 84
    tw_all = W - 2 * M
    cols = [0.25, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
    heads = ["Recorte", "Média 5", "Natureza", "Humanas", "Linguagens", "Matemática", "Redação"]
    rec = RK["recortes"]
    linhas = [
        ("Belém (163 escolas)", "belem"),
        ("Belém — privadas (64)", "belem_privadas"),
        ("Pará (850)", "pa"),
        ("Pará — privadas (186)", "pa_privadas"),
    ]
    shadow(M, ty, tw_all, rowh * 5, 16)
    rrect(M, ty, tw_all, rowh * 5, 16, CARD, z=2)
    cx = M
    for j, hd in enumerate(heads):
        txt(cx + tw_all * cols[j] / 2, ty + rowh * 0.62, hd, monoB, 15.5,
            INK if j == 0 else GRAY, ha="center", z=5)
        cx += tw_all * cols[j]
    ax.plot([M + 30, W - M - 30], [ty + rowh - 8, ty + rowh - 8], color="#E3E4E6", lw=1.6, zorder=4)
    for i, (nome, key) in enumerate(linhas):
        yy = ty + (i + 1) * rowh
        if i % 2 == 0:
            rrect(M, yy, tw_all, rowh, 0, "#F7F7F8", z=2.5)
        p = rec[key]["posicao"]
        vals = [p["MEDIA_5"], p["CN"], p["CH"], p["LC"], p["MT"], p["REDACAO"]]
        best = min(vals)
        cx = M
        txt(cx + 34, yy + rowh * 0.62, nome, outfit, 21, INK, z=5)
        cx += tw_all * cols[0]
        for j, v in enumerate(vals):
            destaque = (v == best)
            txt(cx + tw_all * cols[j + 1] / 2, yy + rowh * 0.62, f"{v}º",
                outfitB, 26, CORALd if destaque else INK, ha="center", z=5)
            cx += tw_all * cols[j + 1]
    by = ty + rowh * 5 + 40
    rrect(M, by, tw_all, 150, 16, "#FCEDE9", z=2)
    rrect(M, by, 12, 150, 6, CORAL, z=3)
    txt(M + 44, by + 44, "COMO LER", monoB, 14, CORALd, z=5)
    txt(M + 44, by + 84, "7º de Belém na média geral — a 1,2 ponto do 6º — e 6º entre as privadas. "
        "Matemática é a melhor área (5º privadas).", outfit, 21, INK, z=5)
    txt(M + 44, by + 122, "Com 114 alunos, é o maior contingente do grupo da frente (o 1º colocado tem 38): "
        "média alta com turma grande vale mais.", outfit, 21, INK, z=5)
    save(fig, "04_ranking_local")


# ---------------- 05 RANKING MARISTAS ----------------
def s05():
    fig, ax, hp, M = base_slide("REDE MARISTA — BRASIL", "16º entre os 70 Maristas do país",
                                "Mesmo critério: média das 5 notas dos presentes nos 2 dias, por escola.")
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    linhas = [
        (1, "Marista Dom Silvério", "Belo Horizonte/MG", 98, 703.1),
        (2, "Marista de Natal", "Natal/RN", 171, 697.0),
        (3, "Marista de Ribeirão Preto", "Ribeirão Preto/SP", 68, 681.8),
        (4, "Marista Anjo da Guarda", "Curitiba/PR", 50, 679.3),
        (5, "Marista Varginha", "Varginha/MG", 67, 678.8),
        (None, "···", "", None, None),
        (16, "Marista Nossa Senhora de Nazaré", "Belém/PA", 114, 661.2),
    ]
    ty, rowh = 272, 78
    tw_all = W - 2 * M
    shadow(M, ty, tw_all, rowh * len(linhas) + 24, 16)
    rrect(M, ty, tw_all, rowh * len(linhas) + 24, 16, CARD, z=2)
    for i, (pos, nome, cid, n, m5) in enumerate(linhas):
        yy = ty + 16 + i * rowh
        eh_nos = (pos == 16)
        if eh_nos:
            rrect(M + 16, yy + 6, tw_all - 32, rowh - 6, 12, "#FCEDE9", z=2.5)
        if pos is None:
            txt(M + 70, yy + rowh * 0.62, "···", outfitB, 26, GRAY, z=5)
            continue
        cor = CORALd if eh_nos else INK
        txt(M + 70, yy + rowh * 0.62, f"{pos}º", outfitB, 28, cor, ha="center", z=5)
        txt(M + 140, yy + rowh * 0.62, nome, outfitB if eh_nos else outfit, 24, cor, z=5)
        txt(M + tw_all * 0.56, yy + rowh * 0.62, cid, mono, 17, GRAY, z=5)
        txt(M + tw_all * 0.76, yy + rowh * 0.62, f"N={n}", mono, 17, GRAY, z=5)
        txt(W - M - 60, yy + rowh * 0.62, vir(m5), outfitB, 28, cor, ha="right", z=5)
    txt(M, ty + rowh * len(linhas) + 84, "Entre os 70 Maristas, só o de Natal tem mais alunos no ENEM que o Nazaré (171 × 114).",
        outfit, 20, GRAY)
    save(fig, "05_ranking_maristas")


# ---------------- 08 ALERTAS (com hab_CH embutido) ----------------
def s08():
    fig, ax, hp, M = base_slide("ONDE ACENDER O FAROL", "4 bolsões: erro acima até da coorte local",
                                "Habilidades em que a escola erra MAIS que os 62 mil da mesma prova — mesmo sendo muito mais forte no geral.")
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    alertas = [
        ("CH-H22", "85,0%", "76,3%", "Analisar a ação de grupos sociais na vida política/cultural — "
         "8,7 pontos acima do erro da coorte, o maior descolamento do estudo."),
        ("LC-H13", "67,0%", "60,4%", "Recursos expressivos e procedimentos de convencimento — "
         "6,6 pontos acima da coorte, num grupo que domina Linguagens."),
        ("CN-H5", "89,7%", "88,8%", "O maior erro absoluto da prova: 9 em cada 10 alunos erram — "
         "e a escola erra até um pouco mais que a coorte."),
        ("CN-H29", "66,0%", "65,8%", "Empate técnico com a coorte — habilidade que não acompanhou "
         "o salto do resto de Natureza."),
    ]
    cw = (W - 2 * 90 - 44) / 2
    chh = 260
    for i, (h, e, c, desc) in enumerate(alertas):
        x = 90 + (i % 2) * (cw + 44)
        y = 272 + (i // 2) * (chh + 40)
        shadow(x, y, cw, chh, 16)
        rrect(x, y, cw, chh, 16, CARD, z=2)
        rrect(x, y, 10, chh, 5, CORAL, z=3)
        txt(x + 40, y + 62, h, outfitB, 32, CORALd, z=5)
        txt(x + 240, y + 62, f"escola {e}", monoB, 19, INK, z=5)
        txt(x + 470, y + 62, f"×  coorte {c}", mono, 19, GRAY, z=5)
        palavras = desc.split()
        linha, yy = "", y + 122
        for p in palavras:
            t = (linha + " " + p).strip()
            if hp["tw"](t, outfit, 18.5) > cw - 80:
                txt(x + 40, yy, linha, outfit, 18.5, GRAY, z=5)
                yy += 34
                linha = p
            else:
                linha = t
        if linha:
            txt(x + 40, yy, linha, outfit, 18.5, GRAY, z=5)
    save(fig, "08_alertas_habilidades")


# ---------------- 12 FECHAMENTO ----------------
def s12():
    fig, ax, hp, M = base_slide("O QUE FAZER COM ISSO", "Três frentes para 2026",
                                "O diagnóstico vira plano quando cada frente tem dono, turma e prazo.")
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    cards = [
        ("1 · FECHAR OS BOLSÕES", "CH-H22, LC-H13 e CN-H5 são pontos cegos: a escola erra ali "
         "mais que uma coorte 170 pontos mais fraca. Diagnóstico por turma e reforço dirigido "
         "custam pouco e movem nota."),
        ("2 · REDAÇÃO: C1 E C3", "830,6 é forte, mas 22º no Pará. Ninguém gabarita C1 (norma culta) "
         "e só 5% gabaritam C3 (argumentação). C5 (59% no 200) mostra que o método funciona — "
         "falta calibrar revisão de língua e repertório."),
        ("3 · SEGURAR O ITEM FÁCIL", "Incoerência média de 5,0 por aluno: turma forte perdendo "
         "ponto em item fácil por deslize, não por falta de conteúdo. Treino de prova e ritmo "
         "valem nota TRI — o item fácil é o que ela mais pune."),
    ]
    cw = (W - 2 * 90 - 2 * 40) / 3
    y0, ch = 280, 470
    for i, (k, corpo) in enumerate(cards):
        x = 90 + i * (cw + 40)
        shadow(x, y0, cw, ch, 18)
        rrect(x, y0, cw, ch, 18, CARD, z=2)
        rrect(x, y0, cw, 10, 5, CORAL if i != 2 else CYAN, z=3)
        txt(x + 34, y0 + 80, k, monoB, 16, CORALd if i != 2 else CYANd, z=5)
        palavras = corpo.split()
        linha, yy = "", y0 + 150
        for p in palavras:
            t = (linha + " " + p).strip()
            if hp["tw"](t, outfit, 19.5) > cw - 68:
                txt(x + 34, yy, linha, outfit, 19.5, INK, z=5)
                yy += 36
                linha = p
            else:
                linha = t
        if linha:
            txt(x + 34, yy, linha, outfit, 19.5, INK, z=5)
    txt(90, 900, "Obrigado!", outfitB, 26, INK)
    txt(90, 944, "Prof. Alexandre Emerson · XTRI · app.rankingenem.com · @xandaoxtri", mono, 16, GRAY)
    save(fig, "12_fechamento")


# ---------------- gráficos 16:9 copiados ----------------
COPIAS = [
    ("dificuldade_MT.png", "06_degrau_matematica.png"),
    ("discriminacao.png", "07_discriminacao.png"),
    ("redacao_competencias.png", "09_redacao_competencias.png"),
    ("redacao_200.png", "10_redacao_200.png"),
    ("chutes.png", "11_nuvem_cop30.png"),
]


def copias():
    for src, dst in COPIAS:
        shutil.copy(D / "graficos" / src, SL / dst)
        print("ok:", dst)


def pdf():
    pngs = sorted(SL.glob("*.png"))
    imgs = [Image.open(p).convert("RGB") for p in pngs]
    # normaliza tudo para 1920x1080 (charts são 2000x1125, mesma razão)
    imgs = [im if im.size == (1920, 1080) else im.resize((1920, 1080), Image.LANCZOS) for im in imgs]
    out = D / "APRESENTACAO_marista_belem.pdf"
    imgs[0].save(out, save_all=True, append_images=imgs[1:], resolution=96)
    print("PDF:", out, f"({len(imgs)} slides)")


if __name__ == "__main__":
    s01(); s02(); s03(); s04(); s05(); s08(); s12()
    copias()
    pdf()
