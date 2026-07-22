#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel IG — O ENEM segue o próprio manual do INEP? Confronto guia oficial (DAEB 2010) x prova 2025.
Marca XTRI. Dados reais: verificação de comandos (0 proibidos) + distratores (45/180) + Q111 (print)."""
import sys
from pathlib import Path
from PIL import Image
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle, Circle

sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)
D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64
VERDE = "#1E8449"


def foot(hp, idx, nota="Fonte: Microdados ENEM 2025 / INEP · Guia de Elaboração e Revisão de Itens (INEP/DAEB, 2010)."):
    hp["txt"](M, H - 62, nota, mono, 9, GRAY)
    hp["txt"](W - M, H - 62, idx, monoB, 11, GRAY, ha="right")


def head(hp, ax, tag):
    logo(ax, M + 118, 84, zoom=0.062)
    hp["txt"](W - M, 90, tag, monoB, 11.5, GRAY, ha="right", va="center")


# 1 — capa
def capa():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect, shadow = hp["txt"], hp["tw"], hp["rrect"], hp["shadow"]
    head(hp, ax, "ENEM 2025 · AUDITORIA")
    ty = 210
    txt(M, ty, "O ENEM SEGUE", outfitB, 60, INK)
    txt(M, ty + 72, "O PRÓPRIO", outfitB, 60, INK)
    txt(M, ty + 144, "MANUAL?", outfitB, 60, CORAL)
    txt(M, ty + 214, "O INEP tem um guia oficial de como cada questão deve ser", outfit, 20, GRAY)
    txt(M, ty + 242, "feita. Peguei esse guia e confrontei com as 180 questões", outfit, 20, GRAY)
    txt(M, ty + 270, "de 2025. Spoiler: na forma, quase perfeito. No espírito…", outfit, 20, GRAY)
    py, hh = ty + 330, 200
    shadow(M, py, W - 2*M, hh, 20); rrect(M, py, W - 2*M, hh, 20, CARD, z=6); rrect(M, py, 11, hh, 5, CORAL, z=7)
    txt(M + 40, py + 58, "A regra nº 9 do INEP proíbe pegadinha.", outfitB, 24, INK, z=8)
    txt(M + 40, py + 116, "1 em cada 4", outfitB, 52, CORAL, z=8)
    txt(M + 40 + tw("1 em cada 4 ", outfitB, 52), py + 116, "questões", outfit, 22, INK, z=8)
    txt(M + 40, py + 156, "tem um distrator que atrai mais gente que o gabarito.", mono, 14, GRAY, z=8)
    txt(M, H - 150, "Deslize: o que o manual manda x o que a prova faz.", outfit, 17, INK)
    foot(hp, "1/7")
    return save(fig, "c1_capa")


# 2 — o manual existe
def manual():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]
    head(hp, ax, "O MANUAL")
    ty = 170
    txt(M, ty, "SIM, EXISTE UM MANUAL", outfitB, 40, INK)
    txt(M, ty + 46, "e ele é bem específico", outfit, 24, CYANd)
    txt(M, ty + 100, "\"Guia de Elaboração e Revisão de Itens\" (INEP / DAEB, 2010) —", outfit, 17, GRAY)
    txt(M, ty + 126, "a diretoria da educação básica, a mesma que faz o ENEM.", outfit, 17, GRAY)
    py = ty + 176; hh = 470
    rrect(M, py, W - 2*M, hh, 18, CARD, z=2)
    txt(M + 40, py + 66, "15", outfitB, 80, CYANd, z=5)
    txt(M + 40 + tw("15 ", outfitB, 80), py + 60, "etapas obrigatórias", outfitB, 26, INK, z=5)
    txt(M + 40 + tw("15 ", outfitB, 80), py + 92, "pra construir cada questão", outfit, 18, GRAY, z=5)
    itens = ["1 habilidade da Matriz por questão", "fonte primária + referência ABNT (proibido livro didático)",
             "item inédito · sem tema polêmico", "comando impessoal, sem \"exceto/incorreto/não\"",
             "distratores plausíveis, nunca absurdos", "pré-teste por TRI antes de entrar no banco"]
    yy = py + 150
    for it in itens:
        ax.add_patch(Circle((M + 54, yy - 6), 5, fc=CYANd, ec="none", zorder=5))
        txt(M + 78, yy, it, outfit, 17.5, INK, z=5); yy += 46
    foot(hp, "2/7")
    return save(fig, "c2_manual")


# 3 — na forma, nota 10
def forma():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]
    head(hp, ax, "O QUE A PROVA CUMPRE")
    ty = 170
    txt(M, ty, "NA FORMA, NOTA 10", outfitB, 40, INK)
    txt(M, ty + 46, "o ENEM 2025 segue o manual à risca", outfit, 22, VERDE)
    txt(M, ty + 96, "Chequei as 180 questões contra as regras de forma. Resultado:", outfit, 16.5, GRAY)
    checks = [("0 comandos com \"exceto\", \"incorreto\", \"não\", \"falso\"", "regra 10 do guia"),
              ("0 \"todas as anteriores\" / \"nenhuma das anteriores\"", "regra 11"),
              ("100% dos textos-base com fonte citada (ABNT)", "regra 3"),
              ("alternativas com paralelismo e extensão parecida", "regra 11"),
              ("~3 minutos por questão", "regra 15"),
              ("todo item pré-testado por TRI (a, b, c)", "etapa 5 de validação")]
    yy = ty + 150
    for main, reg in checks:
        rrect(M, yy, W - 2*M, 92, 14, CARD, z=2)
        ax.add_patch(Circle((M + 48, yy + 46), 20, fc=VERDE, ec="none", zorder=4))
        txt(M + 48, yy + 46, "✓", outfitB, 24, "#FFFFFF", ha="center", va="center", z=5)
        txt(M + 88, yy + 34, main, outfitB, 18.5, INK, z=5)
        txt(M + 88, yy + 66, reg, mono, 12.5, GRAY, z=5)
        yy += 104
    txt(M, yy + 40, "Na forma, o ENEM tira nota 10. O problema é a regra nº 9  →", outfitB, 20, INK)
    foot(hp, "3/7")
    return save(fig, "c3_forma")


# 4 — a regra 9 (quote)
def regra9():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect, shadow = hp["txt"], hp["tw"], hp["rrect"], hp["shadow"]
    head(hp, ax, "A REGRA Nº 9")
    ty = 210
    txt(M, ty, "MAS TEM UMA REGRA", outfitB, 40, INK)
    txt(M, ty + 46, "que a prova contraria", outfit, 24, CORALd)
    py, hh = ty + 130, 470
    shadow(M, py, W - 2*M, hh, 22); rrect(M, py, W - 2*M, hh, 22, CARD, z=6); rrect(M, py, 12, hh, 5, CORAL, z=7)
    txt(M + 44, py + 96, "REGRA Nº 9", monoB, 18, CORAL, z=8)
    txt(M + 44, py + 168, "\"Evite induzir o", outfitB, 40, INK, z=8)
    txt(M + 44, py + 220, "participante ao erro", outfitB, 40, INK, z=8)
    txt(M + 44, py + 272, "(pegadinhas).\"", outfitB, 40, CORALd, z=8)
    txt(M + 44, py + 344, "— Guia de Elaboração e Revisão de Itens,", outfit, 16, GRAY, z=8)
    txt(M + 44, py + 370, "   INEP / DAEB, 2010 · etapa 9 (texto condensado)", outfit, 16, GRAY, z=8)
    txt(M, py + hh + 60, "O próprio INEP define pegadinha como a questão que faz o", outfit, 18, INK)
    txt(M, py + hh + 88, "aluno errar por um detalhe — não por não saber a matéria.", outfit, 18, INK)
    foot(hp, "4/7")
    return save(fig, "c4_regra9")


# 5 — os dados (25%)
def dados():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect, shadow = hp["txt"], hp["tw"], hp["rrect"], hp["shadow"]
    head(hp, ax, "O QUE O DADO MOSTRA")
    ty = 170
    txt(M, ty, "SÓ QUE A PROVA", outfitB, 40, INK)
    txt(M, ty + 46, "INDUZ AO ERRO", outfitB, 40, CORAL)
    txt(M, ty + 96, "Medi, questão a questão, qual alternativa errada mais atraiu:", outfit, 16.5, GRAY)
    py, hh = ty + 150, 190
    shadow(M, py, W - 2*M, hh, 18); rrect(M, py, W - 2*M, hh, 18, CARD, z=6); rrect(M, py, 11, hh, 5, CORAL, z=7)
    txt(M + 40, py + 116, "45", outfitB, 96, CORAL, z=8)
    txt(M + 40 + tw("45 ", outfitB, 96), py + 88, "de 180 questões (25%)", outfitB, 26, INK, z=8)
    txt(M + 40 + tw("45 ", outfitB, 96), py + 124, "têm um distrator que atrai MAIS", outfit, 19, INK, z=8)
    txt(M + 40 + tw("45 ", outfitB, 96), py + 150, "gente do que o próprio gabarito.", outfit, 19, INK, z=8)
    py2 = py + hh + 40; hh2 = 200
    rrect(M, py2, W - 2*M, hh2, 18, "#FEF3F0", z=2)
    txt(M + 40, py2 + 56, "E tem a \"pegadinha\" clássica do manual:", outfitB, 21, INK, z=5)
    txt(M + 40, py2 + 100, "questões FÁCEIS em que até 29% dos alunos de", outfit, 18, INK, z=5)
    txt(M + 40, py2 + 128, "nota 700+ erraram — exatamente a que a regra 9", outfit, 18, INK, z=5)
    txt(M + 40, py2 + 156, "diz para evitar (\"atrai o aluno de bom desempenho\").", outfit, 18, INK, z=5)
    txt(M, py2 + 240, "O caso mais gritante da prova de 2025  →", outfitB, 20, INK)
    foot(hp, "5/7")
    return save(fig, "c5_dados")


# 6 — Q111 (print)
def q111():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect = hp["txt"], hp["tw"], hp["rrect"]
    head(hp, ax, "O CASO EXTREMO")
    ty = 168
    txt(M, ty, "A QUESTÃO Q111", outfitB, 40, CORAL)
    txt(M, ty + 42, "onde a resposta errada ganhou de lavada", outfitB, 22, INK)
    txt(M, ty + 76, "Ciências da Natureza · habilidade CNH9 · dificuldade TRI 641", mono, 13, GRAY)
    # print
    gy = ty + 108
    im = Image.open(D.parent / "post_distratores/carrossel/q111_enem2025.png").convert("RGB")
    iw, ih = im.size; cw = W - 2*M; sc = cw/iw; dh = ih*sc; chmax = 660
    if dh > chmax: im = im.crop((0, 0, iw, int(chmax/sc))); ch = chmax
    else: ch = dh
    ax.imshow(mpimg.pil_to_array(im), extent=(M, M+cw, gy+ch, gy), zorder=3, aspect="auto")
    ax.add_patch(Rectangle((M, gy), cw, ch, fill=False, ec="#DADBDD", lw=1.2, zorder=4))
    ax.add_patch(Rectangle((M, gy), 7, ch, fc=CORAL, ec="none", zorder=5))
    # stat
    py = gy + ch + 22; hh = H - 96 - py
    rrect(M, py, W - 2*M, hh, 18, CARD, z=6); rrect(M, py, 11, hh, 5, CORAL, z=7)
    cy = py + hh/2
    txt(M + 40, cy - 26, "Gabarito B (certo):", outfit, 18, INK, va="center", z=8)
    txt(W - M - 40, cy - 26, "16,5%", outfitB, 30, GRAY, ha="right", va="center", z=8)
    txt(M + 40, cy + 24, "Alternativa A (errada):", outfit, 18, INK, va="center", z=8)
    txt(W - M - 40, cy + 24, "45,9%", outfitB, 40, CORAL, ha="right", va="center", z=8)
    foot(hp, "6/7")
    return save(fig, "c6_q111")


# 7 — veredito
def fecho():
    fig, ax, hp = new_slide(w=W, h=H); txt, tw, rrect, shadow = hp["txt"], hp["tw"], hp["rrect"], hp["shadow"]
    head(hp, ax, "O VEREDITO")
    ty = 200
    txt(M, ty, "O VEREDITO", outfitB, 54, INK)
    txt(M, ty + 76, "Na FORMA, o ENEM segue o próprio manual quase à", outfit, 20, GRAY)
    txt(M, ty + 104, "perfeição: comando, fonte, tempo, pré-teste por TRI.", outfit, 20, GRAY)
    txt(M, ty + 148, "No ESPÍRITO da regra 9, não: a prova induz ao erro", outfit, 20, GRAY)
    txt(M, ty + 176, "em 1 de cada 4 questões.", outfit, 20, GRAY)
    py, hh = ty + 226, 250
    shadow(M, py, W - 2*M, hh, 20); rrect(M, py, W - 2*M, hh, 20, CARD, z=6); rrect(M, py, 11, hh, 5, CORAL, z=7)
    txt(M + 40, py + 58, "Pra você que faz a prova", outfitB, 24, INK, z=8)
    txt(M + 40, py + 100, "A alternativa \"óbvia\" é, muitas vezes, a armadilha", outfit, 18, INK, z=8)
    txt(M + 40, py + 128, "projetada. Desconfie do que parece fácil demais.", outfit, 18, INK, z=8)
    txt(M + 40, py + 182, "O raio-X completo da prova está em:", outfit, 17, GRAY, z=8)
    txt(M + 40, py + 210, "xtri.online", monoB, 22, CYANd, z=8)
    txt(M, H - 150, "Salva e marca quem sempre cai na pegadinha do ENEM.", outfit, 16, INK)
    foot(hp, "7/7", "Fontes: Microdados ENEM 2025 / INEP · Guia de Elaboração e Revisão de Itens (INEP/DAEB, 2010).")
    return save(fig, "c7_fecho")


if __name__ == "__main__":
    capa(); manual(); forma(); regra9(); dados(); q111(); fecho()
