#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel IG (feed 1080x1350) — O ENEM inclui o aluno com necessidades especiais (NEE)?
Censo Escolar 2025 x ENEM 2025 / INEP. 8 cards. Marca XTRI.
v3: fontes oficiais na capa · legislação no card 2 · painéis coloridos sem sombra (simetria) ·
TDA/TDAH no card 3 · destaque centralizado no card 4 · card 5 sem analogia (só dado) ·
card 7 novo: escolas privadas (verificação dupla ENEM×Censo)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D)
W, H = 1080, 1350
M = 64
VERDE = "#2EA84F"
VERDEd = "#1F8F3E"
DADOS = json.loads((D.parent / "dados_inclusao.json").read_text())
PRIV = json.loads((D.parent / "dados_privadas.json").read_text())
F = DADOS["funil_nacional"]
N_TOTAL = 8
PANEL_BOTTOM = 1214


def vir(x):
    return f"{x:,}".replace(",", ".")


def header(hp, tag, t1, t2=None, cor2=CORAL, t1size=35):
    txt = hp["txt"]
    logo(hp["ax"], M + 118, 84, zoom=0.062)
    txt(W - M, 90, tag, monoB, 11.5, GRAY, ha="right", va="center")
    ty = 196
    txt(M, ty, t1, outfitB, t1size, INK)
    if t2:
        txt(M, ty + 58, t2, outfitB, t1size, cor2)
    return ty


def footer(hp, i, fonte=True):
    txt = hp["txt"]
    fy = H - 58
    if fonte:
        txt(M, fy, "Fontes: Microdados do Censo Escolar 2025 e do ENEM 2025 — INEP/MEC", mono, 9, GRAY)
    txt(W - M, fy, f"{i}/{N_TOTAL}", monoB, 11, GRAY, ha="right")


def hbar(hp, x, y, w, frac, cor, h=26, bg="#E6E7E9"):
    rr = hp["rrect"]
    rr(x, y, w, h, h / 2, bg, z=3)
    if frac > 0:
        rr(x, y, max(w * frac, h), h, h / 2, cor, z=4)


def painel(hp, top, bg, barra, titulo, linhas, destaque=None, dcor=None, nota=None, notac=None,
           sombra=False, destaque_center=False):
    """Painel de conclusão de `top` até PANEL_BOTTOM. Painéis coloridos SEM sombra (simetria
    visual — a sombra deslocada + barra lateral pesavam o lado esquerdo)."""
    txt = hp["txt"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    h = PANEL_BOTTOM - top
    if sombra:
        shadow(M, top, W - 2 * M, h, 20)
    rrect(M, top, W - 2 * M, h, 20, bg, z=3)
    rrect(M, top, 10, h, 5, barra, z=4)
    x = M + 38
    txt(x, top + 58, titulo, outfitB, 20, INK, z=5)
    yy = top + 104
    for ln in linhas:
        txt(x, yy, ln, outfit, 17, INK, z=5)
        yy += 34
    if destaque:
        gap = 48  # folga mínima abaixo da última linha do corpo
        if nota:
            dy = yy + 34
        else:
            avail_top, avail_bot = yy + gap, PANEL_BOTTOM - 46
            dy = (avail_top + avail_bot) / 2 if avail_bot > avail_top else avail_top
        if destaque_center:
            txt(W / 2, dy, destaque, outfitB, 21, dcor or barra, ha="center", z=5)
        else:
            txt(x, dy, destaque, outfitB, 21, dcor or barra, z=5)
    if nota:
        txt(x, PANEL_BOTTOM - 30, nota, mono, 12, notac or GRAY, z=5)


# ---------- 1 capa (fontes oficiais explícitas) ----------
def s1():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]; hp["ax"] = ax
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "INEP/MEC · DADOS OFICIAIS", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 240
    txt(M, ty, "O ENEM INCLUI O ALUNO", outfitB, 44, INK)
    txt(M, ty + 58, "COM NECESSIDADES", outfitB, 44, CORAL)
    txt(M, ty + 116, "ESPECIAIS?", outfitB, 44, CORAL)
    txt(M, ty + 186, "Cruzei duas bases oficiais do INEP, escola por escola,", outfit, 18.5, GRAY)
    txt(M, ty + 216, "e o resultado incomoda. Todos os números têm fonte:", outfit, 18.5, GRAY)

    # bloco de fontes oficiais
    sy = ty + 258
    rrect(M, sy, W - 2 * M, 108, 14, "#E9EAEC", z=3)
    txt(M + 30, sy + 42, "FONTES OFICIAIS (dados públicos):", monoB, 11.5, GRAY, z=5)
    txt(M + 30, sy + 72, "Microdados do Censo Escolar da Educação Básica 2025 · INEP/MEC", mono, 12.5, INK, z=5)
    txt(M + 30, sy + 94, "Microdados do ENEM 2025 · INEP/MEC", mono, 12.5, INK, z=5)

    hy = 790
    hh = PANEL_BOTTOM - hy
    shadow(M, hy, W - 2 * M, hh, 22); rrect(M, hy, W - 2 * M, hh, 22, CARD, z=3)
    txt(M + 44, hy + 86, "294 mil", outfitB, 56, CYANd, z=5)
    bx = M + 44 + tw("294 mil", outfitB, 56) + 26
    txt(bx, hy + 68, "estudantes da Educação", outfitB, 19, INK, z=5)
    txt(bx, hy + 98, "Especial no Ensino Médio.", outfitB, 19, INK, z=5)
    ax.plot([M + 44, W - M - 44], [hy + 152, hy + 152], color="#E6E7E9", lw=1, zorder=4)
    txt(M + 44, hy + 236, "22,5 mil", outfitB, 56, CORAL, z=5)
    bx2 = M + 44 + tw("22,5 mil", outfitB, 56) + 26
    txt(bx2, hy + 218, "apareceram no ENEM com", outfitB, 19, INK, z=5)
    txt(bx2, hy + 248, "prova adaptada. E o resto?", outfitB, 19, INK, z=5)
    txt(M + 44, hy + hh - 34, "desliza →", mono, 14, GRAY, z=5)
    footer(hp, 1)
    return save(fig, "s1_capa")


# ---------- 2 lado escola (com a legislação) ----------
def s2():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; hp["ax"] = ax
    header(hp, "1 · NA MATRÍCULA", "NA ESCOLA, O BRASIL", "INCLUI DE VERDADE", VERDEd)
    txt(M, 330, "Matrículas de Educação Especial no Ensino Médio (Censo 2025):", outfit, 16.5, GRAY)
    txt(M, 470, vir(F["nee_med"]), outfitB, 96, INK)
    txt(M, 518, "estudantes com necessidades educacionais especiais (NEE) no EM", mono, 13, GRAY)

    by = 626
    txt(M, by - 16, "ONDE ELES ESTUDAM:", monoB, 12, GRAY)
    hbar(hp, M, by, W - 2 * M, F["pct_cc"] / 100, VERDE, h=54)
    txt(M + 26, by + 27, f"{str(F['pct_cc']).replace('.',',')}% em CLASSE COMUM", outfitB, 21, "#FFFFFF", va="center", z=5)
    txt(M, by + 88, f"classe comum: {vir(F['nee_med_cc'])}", mono, 12, VERDEd)
    txt(W - M, by + 88, f"exclusiva/segregada: {vir(F['nee_med_ce'])} ({str(F['pct_ce']).replace('.',',')}%)", mono, 12, GRAY, ha="right")

    painel(hp, 792, "#EAF7EE", VERDEd, "É o que a lei manda — e está acontecendo:",
           ["a Constituição (art. 208) e a Lei Brasileira de Inclusão",
            "(Lei 13.146/2015) determinam a matrícula na classe comum,",
            "junto com todos — não em salas separadas. O Censo mostra",
            "que, na matrícula, essa regra é cumprida."],
           destaque="99,4% na classe comum, como a lei pede.", dcor=VERDEd,
           nota="o problema aparece depois, na prova →", notac=VERDEd)
    footer(hp, 2)
    return save(fig, "s2_escola")


# ---------- 3 lado ENEM (TDA/TDAH) ----------
def s3():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; hp["ax"] = ax
    header(hp, "2 · NA PROVA", "MAS NO ENEM,", "ELES QUASE SOMEM", CORAL)
    txt(M, 330, "Microdados do ENEM 2025: só dá pra 'ver' quem mudou o CADERNO:", outfit, 16, GRAY)

    tipos = list(F["enem_por_tipo"].items())
    gy = 392
    maxv = max(v for _, v in tipos)
    lbl_x = M + 300
    bw_area = W - M - lbl_x - 120
    for i, (nome, v) in enumerate(tipos):
        yy = gy + i * 74
        txt(M, yy + 19, nome, outfit, 15, INK)
        frac = v / maxv
        hbar(hp, lbl_x, yy, bw_area, frac, CORAL, h=38)
        txt(lbl_x + max(bw_area * frac, 38) + 12, yy + 19, vir(v), monoB, 14, CORALd, va="center", z=5)

    painel(hp, 830, CARD, CORALd, "Total: 22.500 — e o ENEM não registra quem é o aluno.",
           ["Quem tem TDA, TDAH, dislexia e usa só tempo adicional",
            "faz o caderno normal — e some do dado. Esses 22,5 mil",
            "são só a ponta que precisou de um papel diferente;",
            "o resto fica invisível na própria prova."],
           destaque="A necessidade do aluno não fica registrada.", dcor=CORALd,
           nota="sem tipo de necessidade, sem recurso, sem laudo — nada consta no dado",
           sombra=True)
    footer(hp, 3)
    return save(fig, "s3_enem")


# ---------- 4 contraste (destaque centralizado) ----------
def s4():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; hp["ax"] = ax
    header(hp, "3 · O CONTRASTE", "294 MIL NA ESCOLA.", "22 MIL VISÍVEIS NA PROVA.", CORAL, t1size=32)

    cy = 360
    bw = W - 2 * M
    rrect(M, cy, bw, 170, 18, "#EAF7EE", z=3); rrect(M, cy, 10, 170, 5, VERDEd, z=4)
    txt(M + 40, cy + 74, vir(F["nee_med"]), outfitB, 56, VERDEd, z=5)
    bx = M + 40 + tw(vir(F['nee_med']), outfitB, 56) + 26
    txt(bx, cy + 60, "matriculados na Educação", outfit, 19, INK, z=5)
    txt(bx, cy + 92, "Especial (EM) — Censo 2025", outfit, 19, INK, z=5)

    cy2 = cy + 280
    inset = 240
    rrect(M + inset, cy2, bw - 2 * inset, 150, 18, "#FCEDE9", z=3); rrect(M + inset, cy2, 10, 150, 5, CORALd, z=4)
    txt(M + inset + 34, cy2 + 66, "22.500", outfitB, 50, CORALd, z=5)
    txt(M + inset + 34, cy2 + 110, "com prova adaptada — ENEM 2025", mono, 12, GRAY, z=5)
    ax.plot([M + 44, M + inset], [cy + 170, cy2 + 10], color="#C7CBD0", lw=2.4, zorder=2)
    ax.plot([M + bw - 44, M + bw - inset], [cy + 170, cy2 + 10], color="#C7CBD0", lw=2.4, zorder=2)

    painel(hp, 862, CARD, CYANd, "Cuidado com a leitura:",
           ["isto NÃO é 'só 8% chega ao ENEM'. Os 294 mil são o",
            "estoque dos 3 anos do EM, e muito aluno com necessidade",
            "especial faz a prova SEM caderno adaptado — logo, é",
            "invisível aqui."],
           destaque="É o tamanho do PONTO CEGO, não uma taxa de exclusão.",
           dcor=INK, destaque_center=True, sombra=True)
    footer(hp, 4)
    return save(fig, "s4_contraste")


# ---------- 5 mapa por UF (sem analogia — só o dado) ----------
def s5():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; hp["ax"] = ax
    header(hp, "4 · O MAPA", "QUAIS ESTADOS MAIS", "LEVAM NEE AO ENEM", CYANd, t1size=32)
    txt(M, 330, "Provas adaptadas (ENEM) por 100 matrículas NEE no EM (Censo):", outfit, 16, GRAY)

    ufs = DADOS["por_uf"][:8]
    gy = 388
    maxv = ufs[0]["taxa_chegada_pct"]
    bx = M + 70
    bw_area = W - M - bx - 110
    for i, u in enumerate(ufs):
        yy = gy + i * 70
        txt(M, yy + 19, u["uf"], monoB, 16, INK)
        cor = CORAL if i == 0 else "#8FD0F0"
        frac = u["taxa_chegada_pct"] / maxv
        hbar(hp, bx, yy, bw_area, frac, cor, h=38)
        txt(bx + max(bw_area * frac, 38) + 12, yy + 19,
            str(u["taxa_chegada_pct"]).replace(".", ","), monoB, 14.5, INK, va="center", z=5)

    painel(hp, 976, "#EAF4FB", CYANd, "O dado, sem retoque:",
           ["Sergipe, Paraíba e Pará têm os maiores índices;",
            "Santa Catarina (3,6) e Rio Grande do Sul (4,2), os menores.",
            "Média nacional: 7,7 por 100 matrículas."],
           nota="índice de participação visível (caderno adaptado) — não é ranking de inclusão")
    footer(hp, 5)
    return save(fig, "s5_uf")


# ---------- 6 escolas públicas ----------
def s6():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; hp["ax"] = ax
    header(hp, "5 · AS ESCOLAS PÚBLICAS", "A ESCOLA COM 19.", "A ESCOLA COM 1.", CORAL)
    txt(M, 330, "Públicas que mais levaram NEE ao ENEM (candidatos com caderno adaptado):", outfit, 14.5, GRAY)

    tops = [t for t in DADOS["top_escolas"] if not t["exclusiva_censo"]][:4]
    gy = 384
    for i, t in enumerate(tops):
        yy = gy + i * 100
        rrect(M, yy, W - 2 * M, 84, 14, "#FFFFFF", z=3); rrect(M, yy, 8, 84, 4, CORAL, z=4)
        txt(M + 30, yy + 36, t["nome"][:34], outfitB, 16.5, INK, z=5)
        txt(M + 30, yy + 62, f"{t['mun']}/{t['uf']} · {t['dep']} · classe comum · {t['nee_med_censo']} NEE matriculados (Censo)", mono, 10.5, GRAY, z=5)
        txt(W - M - 28, yy + 48, str(t["adaptado_enem"]), outfitB, 34, CORALd, ha="right", va="center", z=5)

    painel(hp, 830, CARD, CORALd, "O padrão é o Ceará — rede estadual, escolas regulares.",
           ["Não são institutos especializados: são escolas comuns",
            "(IN_ESPECIAL_EXCLUSIVA = não, no Censo).",
            "Mas 71% das 6.856 escolas com aluno adaptado têm só 1 —",
            "por isso não publicamos 'ranking de escola inclusora':"],
           destaque="seria ruído — e exporia um aluno. Não se faz.", dcor=GRAY,
           nota="contagens conferidas nos dois bancos: ENEM (CO_ESCOLA) × Censo (CO_ENTIDADE)",
           sombra=True)
    footer(hp, 6)
    return save(fig, "s6_escolas")


# ---------- 7 escolas privadas (NOVO) ----------
def s7():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; rrect = hp["rrect"]; hp["ax"] = ax
    header(hp, "6 · E AS PRIVADAS?", "NAS PRIVADAS, O NÚMERO", "É AINDA MENOR", CORAL, t1size=33)
    txt(M, 330, "Privadas que mais levaram NEE ao ENEM (verificado ENEM × Censo):", outfit, 15, GRAY)

    tops = PRIV["top_privadas"][:4]
    gy = 384
    for i, t in enumerate(tops):
        yy = gy + i * 100
        rrect(M, yy, W - 2 * M, 84, 14, "#FFFFFF", z=3); rrect(M, yy, 8, 84, 4, CYANd, z=4)
        tag = "ESPECIALIZADA (Censo)" if t["exclusiva_censo"] else "classe comum"
        txt(M + 30, yy + 36, t["nome"][:36].title(), outfitB, 16.5, INK, z=5)
        txt(M + 30, yy + 62, f"{t['mun']}/{t['uf']} · Privada · {tag} · {t['nee_med_censo']} NEE matriculados (Censo)", mono, 10.5, GRAY, z=5)
        txt(W - M - 28, yy + 48, str(t["adaptado_enem"]), outfitB, 34, CYANd, ha="right", va="center", z=5)

    n_priv = PRIV["n_escolas_privadas_com_adaptado"]
    tot_priv = PRIV["total_adaptados_em_privadas"]
    painel(hp, 830, CARD, CYANd, "A nº 1 privada é um instituto especializado.",
           [f"Nas comuns, o topo é 7 alunos. Ao todo, {vir(n_priv)} escolas",
            f"privadas tiveram ao menos 1 candidato adaptado — {vir(tot_priv)}",
            "candidatos, cerca de 1 em cada 5 dos 10,2 mil com escola",
            "identificada. O restante veio da rede pública."],
           destaque="A inclusão visível no ENEM é, na maioria, pública.", dcor=CYANd,
           nota="dependência conferida nos dois bancos: ENEM e Censo (INEP)",
           sombra=True)
    footer(hp, 7)
    return save(fig, "s7_privadas")


# ---------- 8 fechamento ----------
def s8():
    fig, ax, hp = new_slide(w=W, h=H)
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]; hp["ax"] = ax
    logo(ax, M + 118, 84, zoom=0.062)
    txt(W - M, 90, "ENTÃO, O ENEM INCLUI?", monoB, 11.5, GRAY, ha="right", va="center")
    ty = 208
    txt(M, ty, "ENTÃO — O ENEM", outfitB, 44, INK)
    txt(M, ty + 56, "INCLUI OU NÃO?", outfitB, 44, CORAL)

    blocos = [
        (VERDEd, "#EAF7EE", "SIM, no acesso.", "existe prova em Braille, Libras, ampliada e atendimento especializado."),
        (CORALd, "#FCEDE9", "MAS é cego aos dados.", "não registra a necessidade — não dá pra medir se inclui BEM."),
        (CYANd, "#EAF4FB", "E a participação visível é pequena.", "22,5 mil num universo de 294 mil no Ensino Médio."),
    ]
    by = 350
    for cor, bg, t, s in blocos:
        rrect(M, by, W - 2 * M, 162, 16, bg, z=3); rrect(M, by, 10, 162, 5, cor, z=4)
        txt(M + 32, by + 60, t, outfitB, 21, INK, z=5)
        txt(M + 32, by + 106, s, outfit, 15.5, INK, z=5)
        by += 182

    ry = by + 6
    rh = PANEL_BOTTOM - 128 - ry
    shadow(M, ry, W - 2 * M, rh, 18); rrect(M, ry, W - 2 * M, rh, 18, CARD, z=3)
    txt(M + 32, ry + 52, "O primeiro passo da inclusão é ser contado.", outfitB, 19, INK, z=5)
    txt(M + 32, ry + 90, "Nisso, o ENEM ainda deixa quem tem necessidade", outfit, 15.5, INK, z=5)
    txt(M + 32, ry + 116, "especial invisível na própria prova.", outfit, 15.5, INK, z=5)

    fy = H - 150
    txt(M, fy, "Fontes: Microdados do Censo Escolar 2025 e do ENEM 2025 — INEP/MEC · dados agregados, sem identificação de aluno", mono, 9.5, GRAY)
    ay = fy + 44
    txt(M, ay, "Transformamos ", outfitB, 15, INK); xx = M + tw("Transformamos ", outfitB, 15)
    txt(xx, ay, "dados", outfitB, 15, CYAN); xx += tw("dados", outfitB, 15)
    txt(xx, ay, " em ", outfitB, 15, INK); xx += tw(" em ", outfitB, 15)
    txt(xx, ay, "aprovações", outfitB, 15, CORAL); xx += tw("aprovações", outfitB, 15)
    txt(xx, ay, ".", outfitB, 15, INK)
    txt(M, ay + 30, "@xandaoxtri · app.rankingenem.com", mono, 12.5, GRAY)
    txt(W - M, H - 58, f"{N_TOTAL}/{N_TOTAL}", monoB, 11, GRAY, ha="right")
    return save(fig, "s8_fecho")


if __name__ == "__main__":
    s1(); s2(); s3(); s4(); s5(); s6(); s7(); s8()
