#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai numa única passada do RESULTADOS_2025 os alunos do Marista Natal (24057134)
e do Dom Bosco São Luís (21010331), gravando alunos.csv na pasta de cada estudo."""
import csv
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
SRC = BASE / "DADOS/RESULTADOS_2025.csv"
DEST = {
    "24057134": BASE / "estudo_marista_natal",
    "21010331": BASE / "estudo_dombosco_saoluis",
}
AREAS = ["LC", "CH", "CN", "MT"]
KEEP = (["CO_ESCOLA", "NO_MUNICIPIO_ESC", "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC",
         "TP_LOCALIZACAO_ESC", "TP_LINGUA", "NU_NOTA_REDACAO"]
        + [f"TP_PRESENCA_{a}" for a in AREAS] + [f"CO_PROVA_{a}" for a in AREAS]
        + [f"NU_NOTA_{a}" for a in AREAS] + [f"TX_RESPOSTAS_{a}" for a in AREAS]
        + [f"NU_NOTA_COMP{i}" for i in range(1, 6)])

writers = {}
files = {}
for code, d in DEST.items():
    d.mkdir(exist_ok=True)
    files[code] = (d / "alunos.csv").open("w", newline="", encoding="utf-8")
    writers[code] = csv.writer(files[code])
    writers[code].writerow(KEEP)

found = {c: 0 for c in DEST}
lidas = 0
with SRC.open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        lidas += 1
        if lidas % 1_000_000 == 0:
            print(f"  {lidas:,} linhas... {found}", flush=True)
        ce = (row.get("CO_ESCOLA") or "").strip()
        if ce in DEST:
            found[ce] += 1
            writers[ce].writerow([row.get(k, "") for k in KEEP])
for fp in files.values():
    fp.close()
print(f"\nTotal: {lidas:,} | Marista(24057134): {found['24057134']} | DomBosco(21010331): {found['21010331']}")
