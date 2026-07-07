#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recalcula o bisserial 2025 por posição (pos_area 1-45) pra CN e MT, achando os itens
mais fracos e checando se batem com os 2 anulados-por-convergência (que mantêm gabarito-letra)."""
import csv
import statistics
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
AREAS = ["CN", "MT"]
N_AMOSTRA = 150_000
LETRAS = set("ABCDE")


def pf(v):
    try:
        return float(str(v).replace(",", ".")) if v else None
    except ValueError:
        return None


def point_biserial(bin_vec, cont_vec):
    n = len(bin_vec)
    mean_c = sum(cont_vec) / n
    mean_b = sum(bin_vec) / n
    if mean_b in (0, 1):
        return None
    cov = sum((b - mean_b) * (c - mean_c) for b, c in zip(bin_vec, cont_vec)) / n
    sd_b = (mean_b * (1 - mean_b)) ** 0.5
    sd_c = (sum((c - mean_c) ** 2 for c in cont_vec) / n) ** 0.5
    if sd_b == 0 or sd_c == 0:
        return None
    return cov / (sd_b * sd_c)


dados = {a: {"resp": [], "gab": [], "nota": []} for a in AREAS}
n_lidas = {a: 0 for a in AREAS}
with (BASE / "DADOS/RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        done = True
        for a in AREAS:
            if n_lidas[a] >= N_AMOSTRA:
                continue
            done = False
            if row.get(f"TP_PRESENCA_{a}") != "1":
                continue
            nota = pf(row.get(f"NU_NOTA_{a}"))
            resp = row.get(f"TX_RESPOSTAS_{a}") or ""
            gab = row.get(f"TX_GABARITO_{a}") or ""
            if nota is None or nota <= 0 or not resp or not gab or len(resp) != len(gab):
                continue
            dados[a]["resp"].append(resp)
            dados[a]["gab"].append(gab)
            dados[a]["nota"].append(nota)
            n_lidas[a] += 1
        if done:
            break

for a in AREAS:
    resp_list = dados[a]["resp"]; gab_list = dados[a]["gab"]; notas = dados[a]["nota"]
    n_itens = len(gab_list[0])
    print(f"\n=== {a} — r por posição (pos_area 1-indexado), ordenado do mais fraco ===")
    linhas = []
    for pos in range(n_itens):
        bin_vec = []; cont_vec = []
        gab_letra = None
        for resp, gab, nota in zip(resp_list, gab_list, notas):
            if pos >= len(gab) or gab[pos] not in LETRAS:
                continue
            gab_letra = gab[pos]
            bin_vec.append(1 if resp[pos] == gab[pos] else 0)
            cont_vec.append(nota)
        if len(bin_vec) < 1000:
            continue
        r = point_biserial(bin_vec, cont_vec)
        acerto = 100 * sum(bin_vec) / len(bin_vec)
        linhas.append((pos + 1, gab_letra, r, acerto, len(bin_vec)))
    linhas.sort(key=lambda x: x[2] if x[2] is not None else 99)
    for pos, gab, r, acerto, n in linhas[:6]:
        print(f"  pos_area {pos:2d} | gab {gab} | r={r:.3f} | acerto={acerto:.1f}% | n={n}")
