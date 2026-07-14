#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agregador TRI/Habilidade 2025 - dados reais (ITENS_PROVA_2025.csv, INEP)
casados contra o schema da API publica api.questoes.xtri.online (id/index/discipline/language).

Regra de ouro (CLAUDE.md): nunca inventar dado. So usa o que esta no CSV oficial.
Cruzamento feito por index (== CO_POSICAO global, confirmado: LC=1-45 CH=46-90 CN=91-135 MT=136-180)
+ language (TP_LINGUA: 0=ingles, 1=espanhol, confirmado no Dicionario oficial).
Caderno de referencia: AZUL, aplicacao regular P1 (CO_PROVA 1459 LC / 1447 CH / 1483 CN / 1471 MT
- mesmos codigos ja usados em todo o acervo XTRI, ex. estudo_distratores/compute_distratores.py).
"""
import csv, json, glob, os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(THIS_DIR)  # raiz do projeto (pasta acima de estudo_agregador_api_2025/)
OUT_DIR = THIS_DIR
ITENS = f"{BASE}/DADOS/ITENS_PROVA_2025.csv"
HAB_DESC = f"{BASE}/analises_primi_2025_cop30/outputs/habilidades_desc.json"

CO_PROVA_AZUL = {"LC": 1459, "CH": 1447, "CN": 1483, "MT": 1471}
DISCIPLINE_TO_AREA = {
    "linguagens": "LC",
    "ciencias-humanas": "CH",
    "ciencias-natureza": "CN",
    "matematica": "MT",
}
LANGUAGE_TO_TPLINGUA = {"ingles": "0", "espanhol": "1", None: ""}

def fnum(s):
    s = (s or "").strip().replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None

# ---------- 1. Carregar CSV real, filtrar Azul regular ----------
csv_by_key = {}   # (area, co_posicao, tp_lingua) -> row dict
aban_positions = []
with open(ITENS, encoding="latin-1") as f:
    r = csv.DictReader(f, delimiter=";")
    for row in r:
        area = row["SG_AREA"]
        if area not in CO_PROVA_AZUL:
            continue
        if int(row["CO_PROVA"]) != CO_PROVA_AZUL[area]:
            continue
        key = (area, int(row["CO_POSICAO"]), row["TP_LINGUA"])
        csv_by_key[key] = row
        if row["IN_ITEM_ABAN"] == "1":
            aban_positions.append((area, int(row["CO_POSICAO"]), row["TP_LINGUA"], row.get("TX_MOTIVO_ABAN")))

print(f"CSV Azul-regular carregado: {len(csv_by_key)} registros (LC+CH+CN+MT)")
print(f"Itens anulados no caderno Azul regular: {aban_positions}")

# ---------- 2. Carregar habilidades_desc.json ----------
with open(HAB_DESC, encoding="utf-8") as f:
    hab_desc = json.load(f)

def skill_obj(area, hab_code):
    if not hab_code or not hab_code.strip():
        return None
    code = f"H{hab_code.strip()}"
    key = f"{area}{code}"
    label = hab_desc.get(key)
    return {"area": area, "code": code, "label": label}

# ---------- 3. Carregar as 4 paginas da API ----------
api_records = []
for pg in sorted(glob.glob(f"{OUT_DIR}/api_snapshot_2025-07-08/page*.json")):
    with open(pg, encoding="utf-8") as f:
        data = json.load(f)
    api_records.extend(data["results"])
print(f"API 2025 carregada: {len(api_records)} registros (esperado 182)")

# ---------- 4. Cruzar e verificar ----------
matched, mismatched, no_csv_match = [], [], []

for rec in api_records:
    area = DISCIPLINE_TO_AREA.get(rec["discipline"])
    tp_lingua = LANGUAGE_TO_TPLINGUA.get(rec["language"])
    key = (area, rec["index"], tp_lingua)
    row = csv_by_key.get(key)
    if row is None:
        no_csv_match.append(rec)
        continue

    csv_gab = row["TX_GABARITO"]
    api_gab = rec["correctAlternative"]
    gab_confere = (csv_gab == api_gab)

    enriched = {
        "id": rec["id"],
        "index": rec["index"],
        "discipline": rec["discipline"],
        "language": rec["language"],
        "area": area,
        "co_posicao_csv": int(row["CO_POSICAO"]),
        "tp_lingua_csv": row["TP_LINGUA"],
        "correctAlternative_api": api_gab,
        "gabarito_csv_azul_regular": csv_gab,
        "gabarito_confere": gab_confere,
        "anulado": row["IN_ITEM_ABAN"] == "1",
        "skill": skill_obj(area, row["CO_HABILIDADE"]),
        "param_a": fnum(row["NU_PARAM_A"]),
        "param_b": fnum(row["NU_PARAM_B"]),
        "param_c": fnum(row["NU_PARAM_C"]),
        "co_prova_csv": int(row["CO_PROVA"]),
        "tx_cor_csv": row["TX_COR"],
    }
    if gab_confere:
        matched.append(enriched)
    else:
        mismatched.append(enriched)

print(f"\n=== RESULTADO DO CRUZAMENTO ===")
print(f"Match total (gabarito CSV == gabarito API): {len(matched)}")
print(f"Mismatch (gabarito difere): {len(mismatched)}")
print(f"Sem correspondencia no CSV: {len(no_csv_match)}")

if mismatched:
    print("\n--- Detalhe dos mismatches ---")
    for m in mismatched:
        print(f"  index={m['index']} area={m['area']} lang={m['language']} "
              f"API={m['correctAlternative_api']} CSV={m['gabarito_csv_azul_regular']} "
              f"(TP_LINGUA csv={m['tp_lingua_csv']})")

if no_csv_match:
    print("\n--- Sem correspondencia no CSV (indices da API) ---")
    for m in no_csv_match:
        print(f"  index={m['index']} discipline={m['discipline']} language={m['language']} slug={m['slug']}")

# quais indices/areas EXISTEM no CSV mas NAO aparecem na API (gaps ja notados: 123,132,174)
api_keys_seen = set()
for rec in api_records:
    area = DISCIPLINE_TO_AREA.get(rec["discipline"])
    api_keys_seen.add((area, rec["index"]))
csv_positions = set((k[0], k[1]) for k in csv_by_key.keys())
missing_from_api = sorted(csv_positions - api_keys_seen)
print(f"\n--- Posicoes que existem no CSV Azul-regular mas NAO existem na API (por index) ---")
for area, pos in missing_from_api:
    # ver se e anulado
    is_aban = any(a==area and p==pos for a,p,_,_ in aban_positions)
    print(f"  area={area} index={pos} anulado_no_csv={is_aban}")

# ---------- 5. Salvar dataset final ----------
all_enriched = matched + mismatched
all_enriched.sort(key=lambda r: (r["index"], r["language"] or ""))

with open(f"{OUT_DIR}/agregador_tri_habilidade_2025.json", "w", encoding="utf-8") as f:
    json.dump({
        "fonte": "Microdados ENEM 2025 / INEP - ITENS_PROVA_2025.csv",
        "caderno_referencia": "AZUL, aplicacao regular (P1)",
        "co_prova_usado": CO_PROVA_AZUL,
        "metodologia": "Join por index(API)==CO_POSICAO(CSV, global 1-180) + language->TP_LINGUA (0=ingles,1=espanhol, conforme Dicionario oficial). Gabarito CSV comparado ao correctAlternative da API para validar o join.",
        "total_registros": len(all_enriched),
        "matches_gabarito": len(matched),
        "mismatches_gabarito": len(mismatched),
        "itens_anulados_csv": [{"area":a,"index":p,"tp_lingua":t,"motivo":mo} for a,p,t,mo in aban_positions],
        "registros": all_enriched,
    }, f, ensure_ascii=False, indent=2)

print(f"\nSalvo: {OUT_DIR}/agregador_tri_habilidade_2025.json")
