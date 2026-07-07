#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel-síntese: poder discriminatório × idade — achados + limites estruturais documentados."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, CYAN, CYANd, W, H)

D = Path(__file__).resolve().parent
X.OUTDIR = str(D / "graficos")
AREAS = json.loads((D / "discriminacao_areas.json").read_text())
DEM = json.loads((D / "demografia_2025.json").read_text())
BIS = json.loads((D / "bisserial_2024_2025.json").read_text())
NOMES = {"LC": "Linguagens", "CH": "Humanas", "CN": "Natureza", "MT": "Matemática"}
AREA_COL = {"LC": "#1FAFEF", "CH": "#E84855", "CN": "#2EC4B6", "MT": "#3A86FF"}


def vir(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 60
    txt(M, 70, "Poder discriminatório × idade: ", outfitB, 28, INK)
    txt(M + tw("Poder discriminatório × idade: ", outfitB, 28), 70, "o que os dados provam", outfitB, 28, CORAL)
    txt(M, 104, "ENEM 2025 — 4 áreas, retrato etário completo e os limites reais dos microdados públicos.",
        outfit, 14, GRAY)
    logo(ax, W - M - 4, 78, zoom=0.06)

    # ---- tabela A por área ----
    ty = 148
    rowh = 46
    tw_all = (W - 2 * M) * 0.56
    cols = [0.30, 0.18, 0.18, 0.18, 0.16]
    heads = ["Área", "A médio", "A mediana", "% alta+", "navalhas (A≥3)"]
    shadow(M, ty, tw_all, rowh * 5, 12)
    rrect(M, ty, tw_all, rowh * 5, 12, CARD, z=2)
    cx = M
    for j, hh_ in enumerate(heads):
        txt(cx + tw_all * cols[j] / 2, ty + rowh * 0.62, hh_, monoB, 12, GRAY, ha="center")
        cx += tw_all * cols[j]
    for i, a in enumerate(["LC", "CH", "CN", "MT"]):
        yy = ty + (i + 1) * rowh
        if i % 2 == 0:
            rrect(M, yy, tw_all, rowh, 0, "#F7F7F8", z=2.5)
        d = AREAS[a]
        vals = [NOMES[a], vir(d["A_media"], 2), vir(d["A_mediana"], 2),
                f"{vir(d['pct_alta_ou_mais'], 0)}%", str(d["n_navalha_A3mais"])]
        cx = M
        for j, v in enumerate(vals):
            col = AREA_COL[a] if j == 0 else INK
            fp = outfitB if j == 0 else mono
            txt(cx + tw_all * cols[j] / 2, yy + rowh * 0.64, v, fp, 15 if j == 0 else 14, col, ha="center", z=5)
            cx += tw_all * cols[j]

    # ---- bloco demografia (direita da tabela) ----
    dx = M + tw_all + 28
    dw = W - M - dx
    dh = rowh * 5
    shadow(dx, ty, dw, dh, 12)
    rrect(dx, ty, dw, dh, 12, "#EAF4FB", z=2)
    txt(dx + 24, ty + 34, "O RETRATO ETÁRIO 2025", monoB, 12, CYANd, z=5)
    txt(dx + 24, ty + 66, f"{DEM['n_70mais']} candidatos com 70+ anos", outfitB, 17, INK, z=5)
    txt(dx + 24, ty + 92, f"{DEM['n_66_70']} entre 66 e 70 anos · questionário 100% preenchido", mono, 11, GRAY, z=5)
    txt(dx + 24, ty + 130, f"COP30/BAM: {vir(DEM['pct_26mais_cop30'], 1)}% têm 26+ anos", outfitB, 15, INK, z=5)
    txt(dx + 24, ty + 152, f"vs {vir(DEM['pct_26mais_regular'], 1)}% no resto do Brasil (quase o dobro)", mono, 11, GRAY, z=5)
    txt(dx + 24, ty + 190, "Nenhum candidato 46+ anos é treineiro (IN_TREINEIRO=0",
        outfit, 12.5, INK, z=5)
    txt(dx + 24, ty + 210, "em 100% dos casos) — são candidatos genuínos.", outfit, 12.5, INK, z=5)

    # ---- limites estruturais ----
    ly = ty + rowh * 5 + 30
    lh = 300
    rrect(M, ly, W - 2 * M, lh, 16, "#FCEDE9", z=2)
    rrect(M, ly, 10, lh, 5, CORAL, z=3)
    txt(M + 34, ly + 34, "O QUE OS MICRODADOS NÃO DEIXAM PROVAR (verificado, não suposto)", monoB, 13, CORALd, z=5)
    itens_lim = [
        ["1. RESULTADOS usa NU_SEQUENCIAL; PARTICIPANTES usa NU_INSCRICAO — chaves DIFERENTES, sem correspondência.",
         "Não dá pra cruzar idade individual com resposta a item (nenhum \"aluno de 70 anos acertou a questão X\")."],
        ["2. Regular P1 e COP30/BAM (a aplicação com perfil mais velho) usam bancos de itens 100% diferentes —",
         "0 co_item em comum, verificado linha a linha. Não dá pra comparar o MESMO item entre as duas populações."],
        ["3. Os parâmetros A/B/C do banco COP30/BAM não são publicados no ITENS_PROVA_2025.csv — só o Regular é",
         "documentado. Não dá nem para comparar o nível agregado dos dois bancos."],
        ["4. Parâmetros OFICIAIS (3PL) de 2024 seguem indisponíveis (arquivo em nuvem não sincronizável) — mas",
         "achamos o RESULTADOS_2024 completo e calculamos um proxy honesto (bisserial), ver quadro abaixo."],
    ]
    yy = ly + 62
    for bloco in itens_lim:
        for j, linha in enumerate(bloco):
            txt(M + 34, yy, linha, outfit, 13.5, INK, z=5)
            yy += 25
        yy += 12

    # ---- conclusão ----
    cy = ly + lh + 20
    ch_ = 116
    cw_ = (W - 2 * M) * 0.60
    rrect(M, cy, cw_, ch_, 14, CARD, z=2)
    rrect(M, cy, 8, ch_, 4, CYANd, z=3)
    txt(M + 30, cy + 34, "A RESPOSTA HONESTA", monoB, 12.5, CYANd, z=5)
    txt(M + 30, cy + 62,
        "As 4 áreas discriminam bem (0% de itens \"baixa\"/\"muito baixa\") — prova tecnicamente sólida.",
        outfit, 14, INK, z=5)
    txt(M + 30, cy + 88,
        "Mas equilíbrio ENTRE perfis etários é hipótese do modelo — os microdados não permitem testar.",
        outfit, 14, INK, z=5)

    # ---- quadro bisserial 2024x2025 (ao lado da resposta honesta) ----
    bx = M + cw_ + 20
    bw = W - M - bx
    rrect(bx, cy, bw, ch_, 14, "#FCEDE9", z=2)
    rrect(bx, cy, 8, ch_, 4, CORAL, z=3)
    txt(bx + 24, cy + 30, "2024×2025 (proxy bisserial)", monoB, 12, CORALd, z=5)
    ordem = ["LC", "CH", "CN", "MT"]
    xx0 = bx + 24
    yy0 = cy + 62
    colw = (bw - 48) / 4
    for i, a in enumerate(ordem):
        d24 = BIS["2024"][a]["r_media"]; d25 = BIS["2025"][a]["r_media"]
        dif = d25 - d24
        cx_ = xx0 + i * colw
        cor_dif = "#2EA84F" if dif >= 0 else CORALd
        txt(cx_, yy0, a, monoB, 11.5, GRAY)
        txt(cx_, yy0 + 22, f"{dif:+.3f}".replace(".", ","), outfitB, 17, cor_dif)
    txt(bx + 24, cy + 100, "Δ correlação ponto-bisserial média (n=150k/área/ano)", mono, 10, GRAY, z=5)

    txt(M, H - 30, "Estudo XTRI — Prof. Alexandre Emerson  |  Microdados ENEM 2025 e 2024 / INEP  |  Transformamos dados em aprovações.",
        mono, 10, GRAY)
    return save(fig, "painel_sintese")


if __name__ == "__main__":
    main()
