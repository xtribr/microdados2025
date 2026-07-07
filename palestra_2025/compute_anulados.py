#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTÓPSIA DOS ITENS ANULADOS 2025 — curvas empíricas por alternativa.
Para os 6 anulados (3 pela TRI, 3 previamente expostos) + 3 itens saudáveis de referência:
% de marcação de cada alternativa (A-E + branco/outros) por faixa de nota da área.
População: Regular P1 (presentes, nota>0). Uma passada no RESULTADOS_2025.
Saída: anulados_curvas.csv + anulados_resumo.json
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
OUT = BASE / "palestra_2025"
AREA_START = {"CH": 46, "CN": 91, "MT": 136}
REGULAR = {"CH": {"1447", "1448", "1449", "1450"},
           "CN": {"1483", "1484", "1485", "1486"},
           "MT": {"1471", "1472", "1473", "1474"}}

# co_item -> metadados (motivo do ITENS_PROVA; refs escolhidos por B mediano, A 1.5-2.5)
ALVOS = {
    "152715": {"area": "CH", "tipo": "tri",     "motivo": "Bis<0,01",                "gab": "D"},
    "96748":  {"area": "CN", "tipo": "tri",     "motivo": "Problema de convergência", "gab": "B"},
    "97593":  {"area": "MT", "tipo": "tri",     "motivo": "Problema de convergência", "gab": "A"},
    "141557": {"area": "CN", "tipo": "exposto", "motivo": "Previamente exposto",      "gab": None},
    "141774": {"area": "CN", "tipo": "exposto", "motivo": "Previamente exposto",      "gab": None},
    "31350":  {"area": "MT", "tipo": "exposto", "motivo": "Previamente exposto",      "gab": None},
    "125735": {"area": "CH", "tipo": "ref",     "motivo": "item saudável (A=1,93 B=0,98)", "gab": "D"},
    "141577": {"area": "CN", "tipo": "ref",     "motivo": "item saudável (A=2,33 B=1,10)", "gab": "E"},
    "117856": {"area": "MT", "tipo": "ref",     "motivo": "item saudável (A=2,17 B=1,83)", "gab": "C"},
}
BANDS = list(range(300, 850, 50))  # 300-350 ... 800-850 (última acumula 850+)


def band_of(nota):
    b = int((nota - 300) // 50)
    return max(0, min(b, len(BANDS) - 1))


def pf(v):
    try:
        return float(str(v).replace(",", ".")) if v else None
    except ValueError:
        return None


# posições dos alvos em cada prova regular
pos_map = defaultdict(dict)   # (area, prova) -> {co_item: pos}
with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        ci = r["CO_ITEM"].strip()
        if ci in ALVOS:
            a = ALVOS[ci]["area"]
            if r["CO_PROVA"].strip() in REGULAR[a]:
                pos_map[(a, r["CO_PROVA"].strip())][ci] = int(r["CO_POSICAO"])

cnt = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # ci -> band -> alt -> n
lidas = 0
with (BASE / "DADOS/RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
    for row in csv.DictReader(f, delimiter=";"):
        lidas += 1
        if lidas % 1_000_000 == 0:
            print(f"  {lidas:,} linhas...", flush=True)
        for a in AREA_START:
            if row.get(f"TP_PRESENCA_{a}") != "1":
                continue
            prova = (row.get(f"CO_PROVA_{a}") or "").strip()
            pm = pos_map.get((a, prova))
            if not pm:
                continue
            nota = pf(row.get(f"NU_NOTA_{a}"))
            resp = row.get(f"TX_RESPOSTAS_{a}") or ""
            if nota is None or nota <= 0 or not resp:
                continue
            b = band_of(nota)
            off = AREA_START[a]
            for ci, pos in pm.items():
                idx = pos - off
                if 0 <= idx < len(resp):
                    ch = resp[idx].upper()
                    alt = ch if ch in "ABCDE" else "outros"
                    cnt[ci][b][alt] += 1

with (OUT / "anulados_curvas.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["co_item", "area", "tipo", "motivo", "gab", "banda_ini", "banda_meio",
                "n_banda", "alt", "pct"])
    for ci, meta in ALVOS.items():
        for b, alts in sorted(cnt[ci].items()):
            n = sum(alts.values())
            if n < 200:
                continue
            ini = BANDS[b]
            meio = ini + 25
            for alt in ["A", "B", "C", "D", "E", "outros"]:
                w.writerow([ci, meta["area"], meta["tipo"], meta["motivo"], meta["gab"] or "X",
                            ini, meio, n, alt, round(100 * alts.get(alt, 0) / n, 2)])

# resumo: totais, consenso dos fortes (bandas >=750), piso (bandas 350-449)
resumo = {}
for ci, meta in ALVOS.items():
    tot = defaultdict(int)
    top = defaultdict(int)
    low = defaultdict(int)
    for b, alts in cnt[ci].items():
        for alt, n in alts.items():
            tot[alt] += n
            if BANDS[b] >= 750:
                top[alt] += n
            if 350 <= BANDS[b] < 450:
                low[alt] += n
    n_tot = sum(tot.values())
    n_top = sum(top.values())
    n_low = sum(low.values())
    consenso = max(top, key=top.get) if n_top else None
    resumo[ci] = {**{k: v for k, v in meta.items()},
                  "n_total": n_tot,
                  "consenso_fortes": consenso,
                  "pct_consenso_fortes": round(100 * top[consenso] / n_top, 1) if n_top else None,
                  "pct_consenso_geral": round(100 * tot[consenso] / n_tot, 1) if n_tot and consenso else None,
                  "pct_consenso_fracos_350_449": round(100 * low[consenso] / n_low, 1) if n_low and consenso else None,
                  "dist_geral": {k: round(100 * v / n_tot, 1) for k, v in sorted(tot.items())}}
(OUT / "anulados_resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))
print(f"\nTotal linhas: {lidas:,}")
print(json.dumps(resumo, ensure_ascii=False, indent=1))
