#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta, por UF (SG_UF_PROVA), os alunos que GABARITARAM (acertaram TODOS os itens
válidos) em MT, CH e CN na 1ª aplicação regular (4 cores principais).
Espelha post_45_lc/compute_45lc_uf.py. Itens anulados excluídos:
CN tem 3 anulados (42 válidas), MT tem 2 (43 válidas), CH tem 0 (45 válidas)."""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
PROVAS = {"MT": {"1471", "1472", "1473", "1474"},
          "CH": {"1447", "1448", "1449", "1450"},
          "CN": {"1483", "1484", "1485", "1486"}}
# CO_POSICAO é global (1-180); TX_RESPOSTAS_<area> tem 45 chars indexados do 0.
OFFSET = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
LETRAS = set("ABCDE")

# itens[area][co_prova] = [(posicao, gabarito), ...]  — só itens válidos
itens = {a: defaultdict(list) for a in PROVAS}
with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        a = r["SG_AREA"].strip()
        p = r["CO_PROVA"].strip()
        if a in PROVAS and p in PROVAS[a] and r["IN_ITEM_ABAN"] != "1":
            itens[a][p].append((int(r["CO_POSICAO"]), (r["TX_GABARITO"] or "").strip().upper()))

N_VALIDAS = {a: {p: len(v) for p, v in itens[a].items()} for a in PROVAS}
print("Itens válidos por prova:", N_VALIDAS, flush=True)

por_uf = {a: defaultdict(int) for a in PROVAS}
detalhe = {a: [] for a in PROVAS}
presentes = {a: 0 for a in PROVAS}
lidas = 0

with (BASE / "DADOS/RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        lidas += 1
        if lidas % 1_000_000 == 0:
            print(f"  {lidas:,} linhas... " +
                  " ".join(f"{a}={sum(por_uf[a].values())}" for a in PROVAS), flush=True)
        for area in PROVAS:
            if row.get(f"TP_PRESENCA_{area}") != "1":
                continue
            prova = (row.get(f"CO_PROVA_{area}") or "").strip()
            its = itens[area].get(prova)
            if not its:
                continue
            presentes[area] += 1
            resp = row.get(f"TX_RESPOSTAS_{area}") or ""
            if not resp:
                continue
            ac = 0
            for pos, gab in its:
                idx = pos - OFFSET[area]
                if 0 <= idx < len(resp) and gab in LETRAS and resp[idx].upper() == gab:
                    ac += 1
            if ac == len(its):
                uf = (row.get("SG_UF_PROVA") or "?").strip()
                por_uf[area][uf] += 1
                detalhe[area].append({"uf": uf, "prova": prova,
                                      "nota": row.get(f"NU_NOTA_{area}", "")})

out = {}
for area in PROVAS:
    notas = sorted({d["nota"] for d in detalhe[area]})
    out[area] = {
        "total": sum(por_uf[area].values()),
        "presentes": presentes[area],
        "n_validas": N_VALIDAS[area],
        "por_uf": dict(sorted(por_uf[area].items(), key=lambda kv: -kv[1])),
        "notas_distintas": notas,
        "detalhe": detalhe[area],
    }
(BASE / "post_45_areas/gabaritos_areas_uf.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2))

print(f"\nTotal linhas: {lidas:,}")
for area in PROVAS:
    o = out[area]
    print(f"{area}: gabaritos={o['total']} | presentes(4 cores)={o['presentes']:,} | "
          f"notas={o['notas_distintas']}")
    print("   ", o["por_uf"])
