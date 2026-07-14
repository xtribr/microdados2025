#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Painel-resumo Marista Belém (aplicação COP30/BAM): médias × coorte COP30 ×
Brasil P1, redação, incoerência e alerta de habilidades acima da coorte."""
import csv
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")))
import xtri_deck as X
from xtri_deck import (new_slide, logo, assinatura, save, outfitB, outfit, mono, monoB,
                       INK, GRAY, CARD, CORAL, CORALd, W, H)

CFG = json.loads((D / "config.json").read_text())
R = json.loads((D / "resumo.json").read_text())
X.OUTDIR = str(D / "graficos")
COR = CFG["cor"]
CORd = CFG["cor_escura"]
AREAS = [("LC", "Linguagens"), ("CH", "Humanas"), ("CN", "Natureza"), ("MT", "Matemática")]


def vir(x, d=1):
    return f"{float(x):.{d}f}".replace(".", ",")


def alertas():
    """Habilidades onde a escola erra MAIS que a coorte COP30 (mesma prova)."""
    out = []
    with (D / "habilidades.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                e = float(r["erro_pct"]); n = float(r["erro_cop30"])
            except ValueError:
                continue
            if e > n:
                out.append((r["area"], r["habilidade"], e, n))
    out.sort(key=lambda t: -(t[2] - t[3]))
    return out


def main():
    fig, ax, hp = new_slide()
    txt = hp["txt"]; tw = hp["tw"]; rrect = hp["rrect"]; shadow = hp["shadow"]
    M = 64
    txt(M, 76, CFG["nome"], outfitB, 26, COR)
    txt(M + tw(CFG["nome"], outfitB, 26), 76, " — raio-X ENEM 2025", outfitB, 26, INK)
    txt(M, 114, f"{R['extraidos']} concluintes com escola declarada · {R['processados_bam']} fizeram a prova COP30/BAM "
                f"({R['presentes_4_bam']} presentes nas 4) e foram corrigidos item a item (180 itens).", outfit, 15, GRAY)
    logo(ax, W - M - 4, 84, zoom=0.072)

    # ---- tabela ----
    ty = 170
    rowh = 64
    tw_all = W - 2 * M
    cols = [0.28, 0.24, 0.24, 0.24]
    heads = ["Área", CFG["curto"], "Coorte COP30", "Brasil (Regular P1)"]
    hcols = [INK, CORd, GRAY, GRAY]
    shadow(M, ty, tw_all, rowh * 6, 14)
    rrect(M, ty, tw_all, rowh * 6, 14, CARD, z=2)
    cx = M
    for j, hd in enumerate(heads):
        txt(cx + tw_all * cols[j] / 2, ty + rowh * 0.62, hd, monoB, 13, hcols[j], ha="center")
        cx += tw_all * cols[j]
    ax.plot([M + 24, W - M - 24], [ty + rowh - 6, ty + rowh - 6], color="#E3E4E6", lw=1.4, zorder=4)
    for i, (a, nome) in enumerate(AREAS + [("RED", "Redação")]):
        yy = ty + (i + 1) * rowh
        if i % 2 == 0:
            rrect(M, yy, tw_all, rowh, 0, "#F7F7F8", z=2.5)
        if a == "RED":
            vals = [R["redacao_media"], R["cop30_redacao"]["media"], None]
        else:
            vals = [R["medias_todos"][a], R["cop30"][a], R["nacional_regular_p1"][a]]
        cx = M
        txt(cx + tw_all * cols[0] / 2, yy + rowh * 0.62, nome, outfit, 17, INK, ha="center", z=5)
        cx += tw_all * cols[0]
        for j, v in enumerate(vals):
            col = [CORd, GRAY, GRAY][j]
            s = vir(v) if v is not None else "—"
            txt(cx + tw_all * cols[j + 1] / 2, yy + rowh * 0.62, s, outfitB if j == 0 else mono,
                21 if j == 0 else 16, col, ha="center", z=5)
            cx += tw_all * cols[j + 1]

    # ---- incoerência ----
    by = ty + rowh * 6 + 36
    bh = 140
    shadow(M, by, tw_all, bh, 16)
    rrect(M, by, tw_all, bh, 16, CARD, z=2)
    rrect(M, by, 10, bh, 5, COR, z=3)
    inc = R["incoer"]
    txt(M + 34, by + 38, "ÍNDICE DE CHUTE (INCOERÊNCIA) — POR ALUNO, 4 PROVAS", monoB, 12, CORd, z=5)
    txt(M + 34, by + 88, vir(inc["media"], 2), outfitB, 40, INK, z=5)
    txt(M + 34 + tw(vir(inc["media"], 2), outfitB, 40) + 14, by + 88, "média por aluno", mono, 12, GRAY, z=5)
    txt(M + 34, by + 120, f"mediana {vir(inc['mediana'], 0)} · máx {inc['max']} · {vir(inc['zero_pct'])}% com zero  —  "
        "na turma forte, incoerência = deslize em item fácil", mono, 12.5, GRAY, z=5)

    # ---- leitura/alertas ----
    ly = by + bh + 30
    lh = 170
    rrect(M, ly, tw_all, lh, 16, "#FCEDE9", z=2)
    rrect(M, ly, 12, lh, 6, COR, z=3)
    al = alertas()
    delta_mt = R["medias_todos"]["MT"] - R["cop30"]["MT"]
    txt(M + 40, ly + 36, "COMO LER", monoB, 13, CORd, z=5)
    txt(M + 40, ly + 70, f"Turma bem acima da coorte COP30 em todas as áreas (maior distância em Matemática: "
        f"+{vir(delta_mt)} pontos sobre a média da coorte).", outfit, 16.5, INK, z=5)
    if al:
        top = " · ".join(f"{a}-{h} ({vir(e)}% × coorte {vir(n)}%)" for a, h, e, n in al[:4])
        txt(M + 40, ly + 104, f"Alerta — habilidades com erro ACIMA da coorte COP30 (mesma prova): {len(al)}.", outfit, 16.5, INK, z=5)
        txt(M + 40, ly + 140, top, outfitB, 15.5, CORd, z=5)
    else:
        txt(M + 40, ly + 104, "Nenhuma habilidade com erro acima da coorte COP30 — sem bolsões críticos.", outfit, 16.5, INK, z=5)

    assinatura(hp, ax, M, H - 40, extra=" · aplicação COP30/BAM · Censo Escolar 2025 (nome) · alunos anônimos")
    return save(fig, "painel_resumo")


if __name__ == "__main__":
    main()
