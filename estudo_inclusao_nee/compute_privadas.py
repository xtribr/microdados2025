#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escolas PRIVADAS que mais levaram alunos NEE ao ENEM 2025 (caderno adaptado).
Verificação dupla de dependência administrativa: TP_DEPENDENCIA_ADM_ESC=='4' no ENEM
E TP_DEPENDENCIA==4 no Censo (Tabela_Escola). Divergências são descartadas e reportadas.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ENEM = Path("/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv")
CENSO = Path("/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/"
             "14413e07-03d0-4c3c-aed0-944131b85a76/scratchpad/censo")

TIPO = {}
for c in [1451, 1463, 1475, 1487, 1587, 1599, 1611, 1623]: TIPO[c] = "Ampliada"
for c in [1452, 1464, 1476, 1488]: TIPO[c] = "Superampliada"
for c in [1454, 1466, 1478, 1490]: TIPO[c] = "Ledor"
for c in [1455, 1467, 1479, 1491]: TIPO[c] = "Libras"
for c in [1495, 1496, 1497, 1498, 1631, 1632, 1633, 1634]: TIPO[c] = "Atendimento Especializado"
AREAS = ["CN", "CH", "LC", "MT"]

# ---- ENEM: contagem de adaptados por escola, só onde o PRÓPRIO ENEM diz privada (dep=4) ----
print("ENEM: varrendo 4,8 mi linhas…")
enem_priv = defaultdict(lambda: {"n": 0, "dep_enem": set(), "mun": "", "uf": ""})
with ENEM.open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        tipo = None
        for a in AREAS:
            v = row.get("CO_PROVA_" + a)
            if v and v.isdigit() and int(v) in TIPO:
                tipo = TIPO[int(v)]
                break
        if not tipo:
            continue
        esc = (row.get("CO_ESCOLA") or "").strip()
        if not esc:
            continue
        d = enem_priv[esc]
        d["n"] += 1
        d["dep_enem"].add((row.get("TP_DEPENDENCIA_ADM_ESC") or "").strip())
        d["mun"] = row.get("NO_MUNICIPIO_ESC", "")
        d["uf"] = row.get("SG_UF_ESC", "")

# ---- Censo: atributos ----
print("Censo: Tabela_Escola…")
censo = {}
with (CENSO / "Tabela_Escola_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        co = (row.get("CO_ENTIDADE") or "").strip()
        if co:
            censo[co] = {
                "nome": (row.get("NO_ENTIDADE") or "").strip(),
                "dep_censo": (row.get("TP_DEPENDENCIA") or "").strip(),
                "mun": (row.get("NO_MUNICIPIO") or "").strip(),
                "uf": (row.get("SG_UF") or "").strip(),
                "exclusiva": (row.get("IN_ESPECIAL_EXCLUSIVA") or "").strip() == "1",
                "sala_aee": (row.get("IN_SALA_ATENDIMENTO_ESPECIAL") or "").strip() == "1",
            }

print("Censo: Tabela_Matricula (NEE-EM por escola)…")
nee_med = {}
with (CENSO / "Tabela_Matricula_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        co = (row.get("CO_ENTIDADE") or "").strip()
        v = (row.get("QT_MAT_ESP_MED") or "").strip()
        if co and v and v != ".":
            try:
                nee_med[co] = int(v)
            except ValueError:
                pass

# ---- cruzar: privada nos DOIS bancos ----
privadas, divergentes = [], []
for esc, d in enem_priv.items():
    c = censo.get(esc)
    dep_enem_priv = d["dep_enem"] == {"4"}
    dep_censo_priv = bool(c) and c["dep_censo"] == "4"
    if dep_enem_priv and dep_censo_priv:
        privadas.append({
            "co_escola": esc, "adaptado_enem": d["n"],
            "nome": c["nome"], "mun": c["mun"], "uf": c["uf"],
            "exclusiva_censo": c["exclusiva"], "sala_aee": c["sala_aee"],
            "nee_med_censo": nee_med.get(esc, 0),
            "verificacao": "privada no ENEM e no Censo",
        })
    elif (dep_enem_priv or dep_censo_priv) and d["n"] >= 5:
        divergentes.append({"co_escola": esc, "n": d["n"], "dep_enem": sorted(d["dep_enem"]),
                            "dep_censo": c["dep_censo"] if c else "(fora do Censo)"})

privadas.sort(key=lambda x: -x["adaptado_enem"])
res = {"top_privadas": privadas[:15], "n_escolas_privadas_com_adaptado": len(privadas),
       "total_adaptados_em_privadas": sum(p["adaptado_enem"] for p in privadas),
       "divergencias_dependencia_n5mais": divergentes}
(OUT / "dados_privadas.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))

print(f"\nescolas privadas (confirmadas nos 2 bancos) com >=1 adaptado: {len(privadas):,}")
print(f"total de candidatos adaptados vindos de privadas: {res['total_adaptados_em_privadas']:,}")
print(f"divergências de dependência (n>=5): {len(divergentes)}")
print("\nTOP 10 PRIVADAS:")
for p in privadas[:10]:
    tag = "ESPECIALIZADA" if p["exclusiva_censo"] else "comum"
    print(f"  {p['adaptado_enem']:3d} | {p['nome'][:44]:44s} | {p['mun']}/{p['uf']} | {tag} | NEE-EM censo: {p['nee_med_censo']}")
