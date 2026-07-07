#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A9 (v2) — acertos->nota usando a POPULACAO COMPLETA Regular P1 (nao so a amostra de 100k),
pra ter n robusto ate a cauda (perto do maximo de acertos, onde miram os 700/800/900).
Reaproveita a mesma logica de contagem de acertos ja usada e validada em
analises_primi_2025_cop30/scripts/gerar_primi_cop30_2025.py (apenas sem o reservoir sampling).
"""
from __future__ import annotations
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import numpy as np

BASE_DIR = Path("/Volumes/Kingston 1/microdados_enem_2025")
DADOS_DIR = BASE_DIR / "DADOS"
OUT_DIR = BASE_DIR / "posts_acertos_nota"

AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
REGULAR_P1_CODES = {
    "LC": {"1459": "Azul", "1460": "Amarela", "1461": "Verde", "1462": "Branca"},
    "CH": {"1447": "Azul", "1448": "Amarela", "1449": "Branca", "1450": "Verde"},
    "CN": {"1483": "Azul", "1484": "Amarela", "1485": "Verde", "1486": "Cinza"},
    "MT": {"1471": "Azul", "1472": "Amarela", "1473": "Verde", "1474": "Cinza"},
}
MIN_N = 15  # baixado de 30 pra 15: com a populacao inteira, ainda e uma amostra robusta na cauda


@dataclass(frozen=True)
class Item:
    posicao: int
    gabarito: str
    lingua: str


def parse_float(v):
    if not v:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def carregar_itens():
    itens = defaultdict(list)
    with (DADOS_DIR / "ITENS_PROVA_2025.csv").open("r", encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["IN_ITEM_ABAN"] == "1":
                continue
            itens[(row["SG_AREA"], row["CO_PROVA"])].append(
                Item(posicao=int(row["CO_POSICAO"]), gabarito=row["TX_GABARITO"], lingua=row["TP_LINGUA"] or "")
            )
    return itens


def itens_para_candidato(itens_por_prova, area, item_code, lingua):
    out = []
    for item in itens_por_prova[(area, item_code)]:
        if area == "LC" and item.lingua and item.lingua != lingua:
            continue
        out.append(item)
    return out


def calcular_acertos(resposta: str, area: str, itens: Iterable[Item]):
    acertos = 0
    validos = 0
    offset = AREA_START[area]
    for item in itens:
        idx = item.posicao - offset
        if idx < 0 or idx >= len(resposta):
            continue
        marcado = resposta[idx]
        validos += 1
        if marcado and marcado not in {"*", "."} and marcado == item.gabarito:
            acertos += 1
    return acertos, validos


def main():
    itens_por_prova = carregar_itens()
    acc = {area: defaultdict(list) for area in AREAS}
    itens_validos_area = {}

    lidas = 0
    with (DADOS_DIR / "RESULTADOS_2025.csv").open("r", encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            lidas += 1
            if lidas % 500_000 == 0:
                print(f"  ...{lidas:,} linhas processadas")
            presente_2_dias = all(row[f"TP_PRESENCA_{a}"] == "1" for a in AREAS)
            if not presente_2_dias:
                continue
            for area in AREAS:
                result_code = row[f"CO_PROVA_{area}"]
                if result_code not in REGULAR_P1_CODES[area]:
                    continue
                nota = parse_float(row[f"NU_NOTA_{area}"])
                resposta = row[f"TX_RESPOSTAS_{area}"]
                if nota is None or not resposta:
                    continue
                lingua = row["TP_LINGUA"] if area == "LC" else ""
                itens_cand = itens_para_candidato(itens_por_prova, area, result_code, lingua)
                acertos, validos = calcular_acertos(resposta, area, itens_cand)
                if validos == 0:
                    continue
                acc[area][acertos].append(nota)
                itens_validos_area[area] = validos

    print(f"\nTotal de linhas lidas: {lidas:,}")
    rows_out = []
    for area in AREAS:
        total_n = sum(len(v) for v in acc[area].values())
        print(f"[{area}] itens_validos={itens_validos_area[area]}  total Regular P1 (presente_2_dias)={total_n:,}  "
              f"faixa acertos observada={min(acc[area])}..{max(acc[area])}")
        for k in sorted(acc[area]):
            vals = acc[area][k]
            n = len(vals)
            if n < MIN_N:
                continue
            arr = np.array(vals)
            rows_out.append({
                "area": area, "acertos": k, "itens_validos": itens_validos_area[area], "n": n,
                "min": round(float(arr.min()), 1), "p10": round(float(np.percentile(arr, 10)), 1),
                "mediana": round(float(np.median(arr)), 1), "p90": round(float(np.percentile(arr, 90)), 1),
                "max": round(float(arr.max()), 1),
            })

    out_path = OUT_DIR / "acertos_para_nota_2025_full.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["area", "acertos", "itens_validos", "n", "min", "p10", "mediana", "p90", "max"])
        w.writeheader()
        w.writerows(rows_out)
    print(f"\nGravado: {out_path} ({len(rows_out)} linhas)")

    # spot-check vs paradoxo MT publicado (353-635 aos 15 acertos)
    for r in rows_out:
        if r["area"] == "MT" and r["acertos"] == 15:
            print(f"\n[spot-check] MT 15 acertos: min={r['min']} max={r['max']} mediana={r['mediana']} n={r['n']}")

    # onde cada area cruza a meta "dos sonhos" pedida: LC 700, CH 800, CN 800, MT 900
    metas = {"LC": 700, "CH": 800, "CN": 800, "MT": 900}
    print("\n[metas dos sonhos]")
    for area, alvo in metas.items():
        rs = [r for r in rows_out if r["area"] == area]
        hit = next((r for r in rs if r["mediana"] >= alvo), None)
        if hit:
            print(f"  {area} cruza {alvo}: acertos={hit['acertos']}/{hit['itens_validos']} (n={hit['n']}, mediana={hit['mediana']})")
        else:
            maxr = rs[-1]
            print(f"  {area} NAO cruza {alvo} nesta base -- maximo: acertos={maxr['acertos']}/{maxr['itens_validos']} mediana={maxr['mediana']} n={maxr['n']}")

    # checar contiguidade (sem gaps) no comeco de cada area
    print("\n[contiguidade no inicio]")
    for area in AREAS:
        rs = [r["acertos"] for r in rows_out if r["area"] == area]
        gaps = [(rs[i], rs[i+1]) for i in range(len(rs)-1) if rs[i+1] - rs[i] > 1]
        print(f"  {area}: primeiros acertos = {rs[:8]}  | gaps = {gaps[:5]}")


if __name__ == "__main__":
    main()
