#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta, por UF (SG_UF_PROVA), os alunos que GABARITARAM Linguagens (45/45)
na 1ª aplicação regular. Validação: total nacional deve ser 85 (acertos_para_nota_full)."""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
LC_PROVAS = {"1459", "1460", "1461", "1462"}
LETRAS = set("ABCDE")

itens = defaultdict(list)
with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        if r["SG_AREA"].strip() == "LC" and r["CO_PROVA"].strip() in LC_PROVAS and r["IN_ITEM_ABAN"] != "1":
            itens[r["CO_PROVA"].strip()].append((int(r["CO_POSICAO"]),
                                                 (r["TX_GABARITO"] or "").strip().upper(),
                                                 (r["TP_LINGUA"] or "").strip()))

por_uf = defaultdict(int)
detalhe = []
lidas = 0
with (BASE / "DADOS/RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        lidas += 1
        if lidas % 1_000_000 == 0:
            print(f"  {lidas:,} linhas... ({sum(por_uf.values())} gabaritos)", flush=True)
        if row.get("TP_PRESENCA_LC") != "1":
            continue
        prova = (row.get("CO_PROVA_LC") or "").strip()
        its = itens.get(prova)
        resp = row.get("TX_RESPOSTAS_LC") or ""
        if not its or not resp:
            continue
        lingua = (row.get("TP_LINGUA") or "").strip()
        ac = 0
        for pos, gab, ling in its:
            if ling and ling != lingua:
                continue
            idx = pos - 1
            if 0 <= idx < len(resp) and gab in LETRAS and resp[idx].upper() == gab:
                ac += 1
        if ac == 45:
            uf = (row.get("SG_UF_PROVA") or "?").strip()
            por_uf[uf] += 1
            detalhe.append({"uf": uf, "lingua": "Inglês" if lingua == "0" else "Espanhol",
                            "nota_lc": row.get("NU_NOTA_LC", "")})

out = {"total": sum(por_uf.values()), "por_uf": dict(sorted(por_uf.items(), key=lambda kv: -kv[1])),
       "detalhe": detalhe}
(BASE / "post_45_lc/gabaritos_lc_uf.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"\nTotal linhas: {lidas:,} | gabaritos LC 45/45: {out['total']}")
print(out["por_uf"])
