#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estudo: o ENEM inclui o aluno com necessidades especiais (NEE)?
Cruza Censo Escolar 2025 (matrícula de Educação Especial no EM, por escola — AGREGADO, sem PII)
com ENEM 2025 (caderno adaptado, por escola/UF). 3 ângulos: funil nacional, mapa por UF, escolas.
Fontes: Microdados Censo Escolar 2025 / INEP e Microdados ENEM 2025 / INEP.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ENEM = Path("/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv")
CENSO = Path("/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/"
             "14413e07-03d0-4c3c-aed0-944131b85a76/scratchpad/censo")

DEP = {"1": "Federal", "2": "Estadual", "3": "Municipal", "4": "Privada"}

# tipos de caderno adaptado no ENEM (CO_PROVA)
TIPO = {}
for c in [1451, 1463, 1475, 1487, 1587, 1599, 1611, 1623]: TIPO[c] = "Ampliada"
for c in [1452, 1464, 1476, 1488]: TIPO[c] = "Superampliada"
for c in [1454, 1466, 1478, 1490]: TIPO[c] = "Ledor"
for c in [1455, 1467, 1479, 1491]: TIPO[c] = "Libras"
for c in [1495, 1496, 1497, 1498, 1631, 1632, 1633, 1634]: TIPO[c] = "Atendimento Especializado"
AREAS = ["CN", "CH", "LC", "MT"]


def gi(v):
    v = (v or "").strip()
    try:
        return int(v) if v not in ("", ".") else 0
    except ValueError:
        return 0


# ---------- 1) ESCOLA: rótulos por CO_ENTIDADE ----------
print("lendo Tabela_Escola…")
escola = {}
with (CENSO / "Tabela_Escola_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        co = (row.get("CO_ENTIDADE") or "").strip()
        if not co:
            continue
        escola[co] = {
            "nome": (row.get("NO_ENTIDADE") or "").strip(),
            "uf": (row.get("SG_UF") or "").strip(),
            "mun": (row.get("NO_MUNICIPIO") or "").strip(),
            "dep": DEP.get((row.get("TP_DEPENDENCIA") or "").strip(), "?"),
            "exclusiva": (row.get("IN_ESPECIAL_EXCLUSIVA") or "").strip() == "1",
            "sala_aee": (row.get("IN_SALA_ATENDIMENTO_ESPECIAL") or "").strip() == "1",
            "acess_inexist": (row.get("IN_ACESSIBILIDADE_INEXISTENTE") or "").strip() == "1",
        }
print(f"  {len(escola):,} escolas")

# ---------- 2) MATRICULA: NEE no EM por escola + nacional + por UF ----------
print("lendo Tabela_Matricula…")
nat = defaultdict(int)
uf_censo = defaultdict(lambda: defaultdict(int))
nee_med_por_escola = {}
with (CENSO / "Tabela_Matricula_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        co = (row.get("CO_ENTIDADE") or "").strip()
        med = gi(row.get("QT_MAT_MED"))
        esp = gi(row.get("QT_MAT_ESP_MED"))
        cc = gi(row.get("QT_MAT_ESP_CC_MED"))
        ce = gi(row.get("QT_MAT_ESP_CE_MED"))
        nat["med"] += med
        nat["esp_med"] += esp
        nat["cc_med"] += cc
        nat["ce_med"] += ce
        if esp:
            nee_med_por_escola[co] = esp
        uf = escola.get(co, {}).get("uf", "")
        if uf:
            uf_censo[uf]["med"] += med
            uf_censo[uf]["esp_med"] += esp
            uf_censo[uf]["cc_med"] += cc

# ---------- 3) ENEM: caderno adaptado por escola / UF / tipo ----------
print("lendo RESULTADOS ENEM (4,8 mi linhas)…")
enem_tipo = defaultdict(int)
enem_uf = defaultdict(int)
enem_por_escola = defaultdict(int)
enem_total = 0
with ENEM.open(encoding="latin-1", newline="") as f:
    for i, row in enumerate(csv.DictReader(f, delimiter=";")):
        tipo = None
        for a in AREAS:
            v = row.get("CO_PROVA_" + a)
            if v and v.isdigit() and int(v) in TIPO:
                tipo = TIPO[int(v)]
                break
        if not tipo:
            continue
        enem_total += 1
        enem_tipo[tipo] += 1
        ufp = (row.get("SG_UF_PROVA") or "").strip()
        if ufp:
            enem_uf[ufp] += 1
        esc = (row.get("CO_ESCOLA") or "").strip()
        if esc:
            enem_por_escola[esc] += 1
        if (i + 1) % 1_000_000 == 0:
            print(f"    {i+1:,}")

# ---------- 4) combinar ----------
# funil nacional
funil = {
    "escolas_censo": len(escola),
    "mat_med_total": nat["med"],
    "nee_med": nat["esp_med"],
    "nee_med_cc": nat["cc_med"],
    "nee_med_ce": nat["ce_med"],
    "pct_cc": round(100 * nat["cc_med"] / max(nat["esp_med"], 1), 1),
    "pct_ce": round(100 * nat["ce_med"] / max(nat["esp_med"], 1), 1),
    "enem_adaptado": enem_total,
    "enem_por_tipo": dict(sorted(enem_tipo.items(), key=lambda x: -x[1])),
    "razao_adaptado_sobre_nee_med": round(100 * enem_total / max(nat["esp_med"], 1), 1),
}

# por UF: NEE-EM (censo) vs adaptado-ENEM (prova UF) -> taxa de chegada
por_uf = []
for uf in sorted(set(list(uf_censo) + list(enem_uf))):
    nee = uf_censo[uf]["esp_med"]
    ad = enem_uf.get(uf, 0)
    por_uf.append({
        "uf": uf,
        "nee_med": nee,
        "pct_cc": round(100 * uf_censo[uf]["cc_med"] / max(nee, 1), 1),
        "adaptado_enem": ad,
        "taxa_chegada_pct": round(100 * ad / max(nee, 1), 2),
    })
por_uf.sort(key=lambda x: -x["taxa_chegada_pct"])

# top escolas por adaptado-ENEM, caracterizadas pelo Censo
top = []
for esc, n in sorted(enem_por_escola.items(), key=lambda x: -x[1])[:25]:
    e = escola.get(esc, {})
    top.append({
        "co_escola": esc,
        "adaptado_enem": n,
        "nome": e.get("nome", "(não encontrada no Censo)"),
        "mun": e.get("mun", ""), "uf": e.get("uf", ""), "dep": e.get("dep", "?"),
        "exclusiva_censo": e.get("exclusiva", None),
        "sala_aee_censo": e.get("sala_aee", None),
        "nee_med_censo": nee_med_por_escola.get(esc, 0),
    })

result = {"funil_nacional": funil, "por_uf": por_uf, "top_escolas": top,
          "notas": {
              "fonte": "Microdados Censo Escolar 2025 e ENEM 2025 / INEP",
              "censo_agregado": "Tabela_Matricula do Censo é agregada por escola (QT_MAT_*), não tem aluno individual.",
              "enem_adaptado_def": "caderno adaptado = CO_PROVA em {Ampliada, Superampliada, Ledor, Libras, Atendimento Especializado}; capta só quem mudou o caderno físico; condição (TEA/TDAH) nunca registrada.",
              "ressalva_funil": "razão adaptado/NEE-EM mistura estoque (3 anos de EM) com fluxo (quem prestou) e subconta NEE que fez caderno regular — é ilustrativa do gap de VISIBILIDADE, não taxa de transição exata.",
              "uf_basis": "NEE-EM por UF da escola (Censo); adaptado-ENEM por UF de prova (ENEM).",
          }}

(OUT / "dados_inclusao.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
print("\n== FUNIL NACIONAL ==")
print(f"  NEE no EM: {funil['nee_med']:,}  (classe comum {funil['pct_cc']}% · exclusiva {funil['pct_ce']}%)")
print(f"  ENEM adaptado: {funil['enem_adaptado']:,}  ({funil['razao_adaptado_sobre_nee_med']}% do estoque NEE-EM)")
print("  por tipo:", funil["enem_por_tipo"])
print("\n== TOP 5 UF por taxa de chegada ==")
for u in por_uf[:5]:
    print(f"  {u['uf']}: NEE-EM {u['nee_med']:,} · adaptado {u['adaptado_enem']:,} · taxa {u['taxa_chegada_pct']}% · CC {u['pct_cc']}%")
print("\n== TOP 6 escolas (adaptado ENEM) ==")
for t in top[:6]:
    print(f"  {t['nome'][:40]} | {t['mun']}/{t['uf']} {t['dep']} | adaptado {t['adaptado_enem']} | NEE-EM censo {t['nee_med_censo']} | exclusiva={t['exclusiva_censo']}")
print("\nok: dados_inclusao.json")
