#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tema 3: "A redação prevê a prova objetiva?"
Correlação de Pearson entre NU_NOTA_REDACAO e cada nota TRI objetiva (LC/CH/CN/MT),
na MESMA LINHA do RESULTADOS_2025 (nota×nota é permitido — não cruza PARTICIPANTES).
Filtro: presente nos dois dias, redação válida (status=1), 5 notas presentes (>0).
Exporta: correlação exata (toda a base) + uma amostra p/ o gráfico de densidade.
"""
import csv
import json
import math
import random
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
SRC = BASE / "DADOS/RESULTADOS_2025.csv"
OUT_JSON = BASE / "palestra_2025/correlacao_redacao.json"
OUT_CSV = BASE / "palestra_2025/amostra_redacao_objetiva.csv"

AREAS = ["LC", "CH", "CN", "MT"]
SAMPLE_N = 120_000
SEED = 20250624


def pf(v):
    if not v:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


class Corr:
    __slots__ = ("n", "sx", "sy", "sxx", "syy", "sxy")

    def __init__(self):
        self.n = 0; self.sx = 0.0; self.sy = 0.0
        self.sxx = 0.0; self.syy = 0.0; self.sxy = 0.0

    def add(self, x, y):
        self.n += 1; self.sx += x; self.sy += y
        self.sxx += x * x; self.syy += y * y; self.sxy += x * y

    def r(self):
        n = self.n
        if n < 2:
            return None
        num = n * self.sxy - self.sx * self.sy
        den = math.sqrt((n * self.sxx - self.sx**2) * (n * self.syy - self.sy**2))
        return num / den if den else None


def main():
    corr = {a: Corr() for a in AREAS}
    rng = random.Random(SEED)
    sample = []
    seen = 0
    lidas = 0
    with open(SRC, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  {lidas:,} linhas...")
            if row.get("TP_STATUS_REDACAO") != "1":
                continue
            if not all(row.get(f"TP_PRESENCA_{a}") == "1" for a in AREAS):
                continue
            red = pf(row.get("NU_NOTA_REDACAO"))
            notas = {a: pf(row.get(f"NU_NOTA_{a}")) for a in AREAS}
            if red is None or red <= 0 or any(notas[a] is None or notas[a] <= 0 for a in AREAS):
                continue
            for a in AREAS:
                corr[a].add(red, notas[a])
            # reservoir sample
            seen += 1
            rec = {"RED": red, **{a: notas[a] for a in AREAS}}
            if len(sample) < SAMPLE_N:
                sample.append(rec)
            else:
                j = rng.randrange(seen)
                if j < SAMPLE_N:
                    sample[j] = rec

    out = {"n_total": corr["LC"].n, "por_area": {}}
    print(f"\nn (candidatos completos c/ redação válida) = {corr['LC'].n:,}")
    for a in AREAS:
        r = corr[a].r()
        out["por_area"][a] = {"r": round(r, 4), "r2": round(r * r, 4),
                              "pct_compartilhado": round(100 * r * r, 1)}
        print(f"  RED × {a}: r={r:.3f}  r²={r*r:.3f}  ({100*r*r:.1f}% da variância)")
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["RED"] + AREAS)
        w.writeheader()
        w.writerows(sample)
    print(f"\nGravado: {OUT_JSON.name} + {OUT_CSV.name} (amostra n={len(sample):,})")


if __name__ == "__main__":
    main()
