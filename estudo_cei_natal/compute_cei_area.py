#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta, por aluno CEI e por ÁREA: acertos, nota TRI e incoerência da área
(min(erros em fáceis b<=0.6, acertos em difíceis b>=1.6)) — p/ o gráfico de incoerência."""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
D = BASE / "estudo_cei_natal"
AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
LETRAS = set("ABCDE")
EASY_B, HARD_B = 0.6, 1.6
ESCOLA_NOME = {"24069191": "CEI Romualdo", "24089214": "CEI Roberto Freire"}


def pf(v):
    try:
        return float(str(v).replace(",", ".")) if v else None
    except ValueError:
        return None


itens = defaultdict(list)
with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        if r["IN_ITEM_ABAN"] == "1" or r["SG_AREA"].strip() not in AREA_START:
            continue
        itens[(r["SG_AREA"].strip(), r["CO_PROVA"].strip())].append(
            (int(r["CO_POSICAO"]), (r["TX_GABARITO"] or "").strip().upper(),
             pf(r["NU_PARAM_B"]), (r["TP_LINGUA"] or "").strip()))

rows = []
with (D / "alunos_cei.csv").open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        esc = ESCOLA_NOME[row["CO_ESCOLA"].strip()]
        lingua = (row["TP_LINGUA"] or "").strip()
        for a in AREAS:
            if row.get(f"TP_PRESENCA_{a}") != "1":
                continue
            nota = pf(row.get(f"NU_NOTA_{a}"))
            resp = row.get(f"TX_RESPOSTAS_{a}") or ""
            its = itens.get((a, (row.get(f"CO_PROVA_{a}") or "").strip()))
            if nota is None or nota <= 0 or not resp or not its:
                continue
            off = AREA_START[a]
            ac = ef = ad = 0
            for pos, gab, b, ling in its:
                if a == "LC" and ling and ling != lingua:
                    continue
                idx = pos - off
                if idx < 0 or idx >= len(resp):
                    continue
                ok = resp[idx].upper() == gab and gab in LETRAS
                ac += ok
                if b is not None:
                    if b <= EASY_B and not ok:
                        ef += 1
                    elif b >= HARD_B and ok:
                        ad += 1
            rows.append([esc, a, ac, nota, min(ef, ad)])

with (D / "cei_alunos_area.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["escola", "area", "acertos", "nota", "incoer"])
    w.writerows(rows)
print(f"ok: cei_alunos_area.csv ({len(rows)} linhas aluno×área)")
