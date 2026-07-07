#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redação C1-C5: médias nacionais 2024 vs 2025 (foco na C2), + distribuição de status
e faixas de nota de 2025. Dado real, streaming (arquivos de ~1.6-2.1 GB).
Válida = TP_STATUS_REDACAO == 1 ("Sem problemas"). Competências 0-200 (múltiplos de 20).
"""
import csv
import json
from pathlib import Path

FILES = {
    2024: "/Volumes/HD/apps/RANKING ENEM/microdados-2024/MICRODADOS_ENEM_2024.csv",
    2025: "/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv",
}
OUT = Path("/Volumes/Kingston 1/microdados_enem_2025/palestra_2025/redacao_2024_2025.json")
COMPS = ["NU_NOTA_COMP1", "NU_NOTA_COMP2", "NU_NOTA_COMP3", "NU_NOTA_COMP4", "NU_NOTA_COMP5"]

# rótulos oficiais TP_STATUS_REDACAO
STATUS_LABEL = {
    "1": "Sem problemas", "2": "Anulada", "3": "Cópia Texto Motivador",
    "4": "Em Branco", "6": "Fuga ao tema", "7": "Não atendimento ao tipo textual",
    "8": "Texto insuficiente", "9": "Parte desconectada",
}


def parse_num(v):
    if v is None or v == "":
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def process(year, path):
    somas = {c: 0.0 for c in COMPS}
    n_valid = 0
    status_count = {}
    redacao_bands = {}  # faixas de 100 da nota final, só válidas
    n_total_status = 0
    lidas = 0
    with open(path, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  [{year}] {lidas:,} linhas...")
            st = (row.get("TP_STATUS_REDACAO") or "").strip()
            if st == "":
                continue
            n_total_status += 1
            status_count[st] = status_count.get(st, 0) + 1
            if st != "1":
                continue
            comps = {c: parse_num(row.get(c)) for c in COMPS}
            if any(comps[c] is None for c in COMPS):
                continue
            n_valid += 1
            for c in COMPS:
                somas[c] += comps[c]
            red = parse_num(row.get("NU_NOTA_REDACAO"))
            if red is not None:
                lo = int(red // 100) * 100
                redacao_bands[lo] = redacao_bands.get(lo, 0) + 1
    medias = {c: (somas[c] / n_valid if n_valid else None) for c in COMPS}
    return {
        "year": year, "linhas_lidas": lidas, "n_com_status": n_total_status,
        "n_validas": n_valid,
        "medias_comp": {c: round(medias[c], 2) for c in COMPS},
        "status_count": {STATUS_LABEL.get(k, k): v for k, v in sorted(status_count.items())},
        "status_count_raw": status_count,
        "redacao_bands_validas": {str(k): v for k, v in sorted(redacao_bands.items())},
    }


def main():
    out = {}
    for year, path in FILES.items():
        if not Path(path).exists():
            print(f"[{year}] ARQUIVO NAO ENCONTRADO: {path}")
            continue
        print(f"=== processando {year}: {path} ===")
        out[str(year)] = process(year, path)
        m = out[str(year)]["medias_comp"]
        print(f"[{year}] válidas={out[str(year)]['n_validas']:,} médias C1-C5: "
              + " | ".join(f"C{i+1}={m[COMPS[i]]}" for i in range(5)))

    # delta 2024->2025 por competência
    if "2024" in out and "2025" in out:
        delta = {}
        for i, c in enumerate(COMPS):
            a, b = out["2024"]["medias_comp"][c], out["2025"]["medias_comp"][c]
            delta[f"C{i+1}"] = {"2024": a, "2025": b, "delta": round(b - a, 2)}
        out["delta_comp"] = delta
        print("\n=== DELTA C1-C5 (2025 - 2024) ===")
        for k, v in delta.items():
            print(f"  {k}: 2024={v['2024']}  2025={v['2025']}  Δ={v['delta']:+.2f}")

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGravado: {OUT}")


if __name__ == "__main__":
    main()
