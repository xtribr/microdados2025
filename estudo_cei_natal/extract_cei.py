#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai dos microdados (RESULTADOS_2025) todos os alunos com CO_ESCOLA nas duas
unidades CEI (Natal/RN): 24069191 e 24089214. De carona, acumula a média nacional
por área (presentes, nota>0) — geral e só Regular P1 — como referência.
Nada inventado: só filtragem e somas sobre o CSV oficial INEP.
"""
import csv
import json
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
SRC = BASE / "DADOS/RESULTADOS_2025.csv"
OUTD = BASE / "estudo_cei_natal"
ESCOLAS = {"24069191", "24089214"}
AREAS = ["LC", "CH", "CN", "MT"]
REGULAR = {
    "LC": {"1459", "1460", "1461", "1462"}, "CH": {"1447", "1448", "1449", "1450"},
    "CN": {"1483", "1484", "1485", "1486"}, "MT": {"1471", "1472", "1473", "1474"},
}
KEEP = (["CO_ESCOLA", "NO_MUNICIPIO_ESC", "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC",
         "TP_LOCALIZACAO_ESC", "TP_LINGUA", "NU_NOTA_REDACAO"]
        + [f"TP_PRESENCA_{a}" for a in AREAS] + [f"CO_PROVA_{a}" for a in AREAS]
        + [f"NU_NOTA_{a}" for a in AREAS] + [f"TX_RESPOSTAS_{a}" for a in AREAS]
        + [f"NU_NOTA_COMP{i}" for i in range(1, 6)])


def pf(v):
    if not v:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def main():
    nat = {a: [0.0, 0] for a in AREAS}       # todas as aplicações
    nat_p1 = {a: [0.0, 0] for a in AREAS}    # só Regular P1
    found = 0
    lidas = 0
    with SRC.open(encoding="latin-1", newline="") as f, \
         (OUTD / "alunos_cei.csv").open("w", newline="", encoding="utf-8") as fo:
        reader = csv.DictReader(f, delimiter=";")
        w = csv.writer(fo)
        w.writerow(KEEP)
        for row in reader:
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  {lidas:,} linhas... ({found} alunos CEI)", flush=True)
            for a in AREAS:
                if row.get(f"TP_PRESENCA_{a}") == "1":
                    n = pf(row.get(f"NU_NOTA_{a}"))
                    if n and n > 0:
                        nat[a][0] += n
                        nat[a][1] += 1
                        if row.get(f"CO_PROVA_{a}", "") in REGULAR[a]:
                            nat_p1[a][0] += n
                            nat_p1[a][1] += 1
            if (row.get("CO_ESCOLA") or "").strip() in ESCOLAS:
                found += 1
                w.writerow([row.get(k, "") for k in KEEP])
    ref = {"nacional_geral": {a: {"media": round(nat[a][0] / nat[a][1], 1), "n": nat[a][1]} for a in AREAS},
           "nacional_regular_p1": {a: {"media": round(nat_p1[a][0] / nat_p1[a][1], 1), "n": nat_p1[a][1]} for a in AREAS}}
    (OUTD / "referencia_nacional.json").write_text(json.dumps(ref, ensure_ascii=False, indent=2))
    print(f"\nTotal linhas: {lidas:,} | alunos CEI extraídos: {found}")
    print(json.dumps(ref["nacional_regular_p1"], indent=1))


if __name__ == "__main__":
    main()
