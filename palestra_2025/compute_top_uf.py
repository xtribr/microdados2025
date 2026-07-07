#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maior nota TRI por estado + a escola do aluno.
Métrica: média das 4 notas objetivas (TRI) — CN, CH, LC, MT. Presente nos dois dias.
Para cada UF (SG_UF_PROVA) guarda: o TOP geral e o TOP com escola declarada (CO_ESCOLA).
Resolve o código da escola pelo Censo Escolar 2025 (Tabela_Escola_2025 → NO_ENTIDADE).
Nada inventado: nome da escola vem do Censo/INEP; aluno é anônimo (microdado).
"""
import csv
import json
import zipfile
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
SRC = BASE / "DADOS/RESULTADOS_2025.csv"
CENSO_ZIP = BASE / "analises_primi_2025_cop30/cache/microdados_censo_escolar_2025.zip"
CENSO_INNER = "microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv"
OUT = BASE / "palestra_2025/top_uf_2025.json"

AREAS = ["CN", "CH", "LC", "MT"]
DEP = {"1": "Federal", "2": "Estadual", "3": "Municipal", "4": "Privada"}


def pf(v):
    if not v:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def stream_top():
    best_any = {}     # uf -> rec
    best_school = {}   # uf -> rec (só com CO_ESCOLA)
    lidas = 0
    with SRC.open(encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  {lidas:,} linhas...")
            if not all(row.get(f"TP_PRESENCA_{a}") == "1" for a in AREAS):
                continue
            notas = {a: pf(row.get(f"NU_NOTA_{a}")) for a in AREAS}
            if any(notas[a] is None or notas[a] <= 0 for a in AREAS):
                continue
            uf = (row.get("SG_UF_PROVA") or "").strip()
            if not uf:
                continue
            media = sum(notas[a] for a in AREAS) / 4
            area_max = max(AREAS, key=lambda a: notas[a])
            red = pf(row.get("NU_NOTA_REDACAO"))
            co_esc = (row.get("CO_ESCOLA") or "").strip()
            rec = {
                "uf": uf, "media4": round(media, 1),
                "notas": {a: notas[a] for a in AREAS},
                "area_max": area_max, "nota_max": notas[area_max],
                "redacao": red,
                "co_escola": co_esc,
                "uf_esc": (row.get("SG_UF_ESC") or "").strip(),
                "munic_esc": (row.get("NO_MUNICIPIO_ESC") or "").strip(),
                "dep": DEP.get((row.get("TP_DEPENDENCIA_ADM_ESC") or "").strip(), ""),
                "munic_prova": (row.get("NO_MUNICIPIO_PROVA") or "").strip(),
            }
            if uf not in best_any or media > best_any[uf]["media4"]:
                best_any[uf] = rec
            if co_esc and (uf not in best_school or media > best_school[uf]["media4"]):
                best_school[uf] = rec
    print(f"Total linhas: {lidas:,}")
    return best_any, best_school


def resolve_names(codes):
    names = {}
    with zipfile.ZipFile(CENSO_ZIP) as zf, zf.open(CENSO_INNER) as fp:
        import io
        reader = csv.DictReader(io.TextIOWrapper(fp, encoding="latin-1"), delimiter=";")
        wanted = set(codes)
        for r in reader:
            c = (r.get("CO_ENTIDADE") or "").strip()
            if c in wanted:
                names[c] = {
                    "nome": (r.get("NO_ENTIDADE") or "").strip(),
                    "municipio": (r.get("NO_MUNICIPIO") or "").strip(),
                    "uf": (r.get("SG_UF") or "").strip(),
                }
                if len(names) == len(wanted):
                    break
    return names


def main():
    best_any, best_school = stream_top()
    codes = {r["co_escola"] for r in best_school.values() if r["co_escola"]}
    codes |= {r["co_escola"] for r in best_any.values() if r["co_escola"]}
    print(f"Resolvendo {len(codes)} códigos de escola no Censo...")
    names = resolve_names(codes)

    def attach(rec):
        c = rec.get("co_escola")
        if c and c in names:
            rec["escola_nome"] = names[c]["nome"]
            rec["escola_municipio"] = names[c]["municipio"]
            rec["escola_uf"] = names[c]["uf"]
        return rec

    out = {"best_any": {u: attach(r) for u, r in best_any.items()},
           "best_school": {u: attach(r) for u, r in best_school.items()}}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGravado: {OUT.name}\n")
    print("=== TOP por UF (média das 4 objetivas) — aluno com escola declarada ===")
    for uf in sorted(best_school, key=lambda u: -best_school[u]["media4"]):
        r = best_school[uf]
        esc = r.get("escola_nome", "(código " + r["co_escola"] + " não encontrado)")
        print(f"  {uf}: {r['media4']}  máx {r['area_max']} {r['nota_max']:.1f}  | {r['dep']} · {esc} ({r.get('escola_municipio','?')})")


if __name__ == "__main__":
    main()
