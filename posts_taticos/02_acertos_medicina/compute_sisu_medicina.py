#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Predição de acertos para Medicina a partir das notas de corte + pesos REAIS do SISU 2026
(que usa notas do ENEM 2025). Fontes:
  - /Volumes/HD/apps/MIRT/exports/sisu_2026_pesos.csv        (pesos e mínimos por curso)
  - /Volumes/HD/apps/MIRT/exports/sisu_2026_notas_corte.csv  (corte por modalidade; parcial diário)
  - posts_acertos_nota/acertos_para_nota_2025_full.csv        (nota TRI mediana por nº de acertos, ENEM 2025)

Modelo (assunções ROTULADAS):
  corte = (Wr·Nred + Wl·Nlc + Wm·Nmt + Wh·Nch + Wc·Ncn) / ΣW
  Assumimos redação = RED_FIXA e as 4 áreas objetivas com a MESMA nota N.
  Resolvemos N e convertemos em acertos por área via a mediana acertos→nota do ENEM 2025.
  (é uma estimativa central honesta; a nota real de um nº de acertos varia por quais itens.)
"""
import ast
import csv
import json
from pathlib import Path

MIRT = Path("/Volumes/HD/apps/MIRT/exports")
BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
OUT = BASE / "posts_taticos/02_acertos_medicina"
RED_FIXA = 900.0  # redação assumida (candidato forte de Medicina); rotulado no post

# sigla -> fragmento do nome oficial (a coluna 'university' traz o nome completo)
ALVOS = {
    "UFRN": "RIO GRANDE DO NORTE",
    "UECE": "ESTADUAL DO CEAR",
    "UFC": "UNIVERSIDADE FEDERAL DO CEAR",
    "UFPE": "FEDERAL DE PERNAMBUCO",
    "UFBA": "FEDERAL DA BAHIA",
    "UFMA": "FEDERAL DO MARANHÃO",
    "UFMG": "FEDERAL DE MINAS GERAIS",
    "UFPB": "FEDERAL DA PARAÍBA",
    "UnB": "DE BRASÍLIA",
    "UERN": "ESTADUAL DO RIO GRANDE DO NORTE",
}


def sigla_de(uni_up):
    for sig, frag in ALVOS.items():
        if frag.upper() in uni_up:
            return sig
    return None

# ---- acertos -> nota mediana por área (do ENEM 2025) ----
med = {a: {} for a in ("LC", "CH", "CN", "MT")}
for r in csv.DictReader((BASE / "posts_acertos_nota/acertos_para_nota_2025_full.csv").open(encoding="utf-8")):
    med[r["area"]][int(r["acertos"])] = float(r["mediana"])


def acertos_para_nota(area, alvo):
    for ac in range(0, 46):
        if med[area].get(ac, 0) >= alvo:
            return ac
    return None  # nem 45 acertos atinge pela mediana


# ---- pesos de Medicina por course_id ----
pesos = {}
for r in csv.DictReader((MIRT / "sisu_2026_pesos.csv").open(encoding="utf-8")):
    if r["course_name"].strip().lower() == "medicina":
        try:
            pesos[r["course_id"]] = {
                "uni": r["university"], "campus": r["campus"], "city": r["city"], "uf": r["state"],
                "Wr": float(r["peso_red"]), "Wl": float(r["peso_ling"]), "Wm": float(r["peso_mat"]),
                "Wh": float(r["peso_ch"]), "Wc": float(r["peso_cn"]),
            }
        except (ValueError, KeyError):
            pass


def ultimo_parcial(s):
    try:
        lst = ast.literal_eval(s)
        return float(lst[-1]["score"]) if lst else None
    except Exception:
        return None


# ---- corte ampla concorrência de Medicina ----
cortes = {}
for r in csv.DictReader((MIRT / "sisu_2026_notas_corte.csv").open(encoding="utf-8")):
    if r["course_name"].strip().lower() != "medicina":
        continue
    if "ampla" not in (r["modality_name"] or "").lower():
        continue
    c = r["cut_score"].strip()
    corte = float(c) if c else ultimo_parcial(r["partial_scores"])
    if corte:
        cortes[r["course_id"]] = corte

# ---- montar resultado para as universidades-alvo ----
res = []
for cid, p in pesos.items():
    if cid not in cortes:
        continue
    uni_up = p["uni"].upper()
    sig = sigla_de(uni_up)
    if sig is None:
        continue
    C = cortes[cid]
    sw = p["Wr"] + p["Wl"] + p["Wm"] + p["Wh"] + p["Wc"]
    w_obj = p["Wl"] + p["Wm"] + p["Wh"] + p["Wc"]
    # N tal que (Wr*RED + w_obj*N)/sw = C
    N = (C * sw - p["Wr"] * RED_FIXA) / w_obj
    ac = {a: acertos_para_nota(a, N) for a in ("MT", "CN", "CH", "LC")}
    res.append({
        "uni": p["uni"], "sigla": sig,
        "campus": p["campus"], "city": p["city"], "uf": p["uf"],
        "corte": round(C, 1),
        "pesos": {"red": p["Wr"], "lc": p["Wl"], "mt": p["Wm"], "ch": p["Wh"], "cn": p["Wc"]},
        "nota_por_area_necessaria": round(N, 1),
        "acertos": ac,
    })

res.sort(key=lambda x: -x["corte"])
(OUT / "sisu_medicina.json").write_text(json.dumps(
    {"red_assumida": RED_FIXA, "universidades": res,
     "fonte": "SISU 2026 (ENEM 2025) — cortes e pesos oficiais / MIRT; acertos→nota: Microdados ENEM 2025 / INEP"},
    ensure_ascii=False, indent=2))

print(f"redação assumida: {RED_FIXA:.0f}\n")
print(f"{'univ':10s} {'campus/UF':22s} {'corte':>7s} {'N/área':>7s} | acertos MT/CN/CH/LC  | pesos R-L-M-H-C")
for x in res:
    ac = x["acertos"]
    acs = "/".join(str(ac[a]) if ac[a] is not None else "45+" for a in ("MT", "CN", "CH", "LC"))
    pz = x["pesos"]
    pzs = f"{pz['red']:.0f}-{pz['lc']:.0f}-{pz['mt']:.0f}-{pz['ch']:.0f}-{pz['cn']:.0f}"
    print(f"{x['sigla']:10s} {(x['city']+'/'+x['uf']):22s} {x['corte']:7.1f} {x['nota_por_area_necessaria']:7.1f} | {acs:20s} | {pzs}")
