#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monta o dado do scatter "acerto não é nota" garantindo que o TOPO (máx. de acertos)
sempre apareça no gráfico — corrige o descasamento eixo-x vs. subtítulo.
Estratégia: amostra aleatória do miolo + TODOS os candidatos da cauda superior
(acertos >= iv-3). Calcula acert_dif (proporção de itens DIFÍCEIS, b>1.5, acertados).
Regular P1, presente nos dois dias, nota>0, itens anulados fora.
"""
import csv
import random
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
DADOS = BASE / "DADOS"
OUTDIR = BASE / "palestra_2025/plot_data"
OUTDIR.mkdir(parents=True, exist_ok=True)

AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
IV = {"LC": 45, "CH": 45, "CN": 42, "MT": 43}
REGULAR_P1_CODES = {
    "LC": {"1459", "1460", "1461", "1462"}, "CH": {"1447", "1448", "1449", "1450"},
    "CN": {"1483", "1484", "1485", "1486"}, "MT": {"1471", "1472", "1473", "1474"},
}
LETRAS = set("ABCDE")
TARGET_BULK = 100_000
SEED = 20250624


def pf(v):
    if not v:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def load_items():
    itens = defaultdict(list)  # (area, prova) -> [(pos, gab, b, lingua)]
    with (DADOS / "ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            if row["IN_ITEM_ABAN"] == "1":
                continue
            area = row["SG_AREA"].strip()
            if area not in AREA_START:
                continue
            itens[(area, row["CO_PROVA"].strip())].append((
                int(row["CO_POSICAO"]), (row["TX_GABARITO"] or "").strip().upper(),
                pf(row["NU_PARAM_B"]), (row["TP_LINGUA"] or "").strip()))
    return itens


def metrics(resp, area, items, lingua):
    off = AREA_START[area]
    acertos = validos = dificeis = ac_dif = 0
    for pos, gab, b, ling in items:
        if area == "LC" and ling and ling != lingua:
            continue
        idx = pos - off
        if idx < 0 or idx >= len(resp):
            continue
        validos += 1
        ok = resp[idx].upper() == gab and gab in LETRAS
        if ok:
            acertos += 1
        if b is not None and b > 1.5:
            dificeis += 1
            if ok:
                ac_dif += 1
    ad = (ac_dif / dificeis) if dificeis else None
    return acertos, validos, ad


def main():
    itens = load_items()
    rng = random.Random(SEED)
    bulk = {a: [] for a in AREAS}
    tail = {a: [] for a in AREAS}
    seen_bulk = {a: 0 for a in AREAS}
    lidas = 0
    with (DADOS / "RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  {lidas:,} linhas...")
            if not all(row.get(f"TP_PRESENCA_{a}") == "1" for a in AREAS):
                continue
            for a in AREAS:
                code = row.get(f"CO_PROVA_{a}", "")
                if code not in REGULAR_P1_CODES[a]:
                    continue
                nota = pf(row.get(f"NU_NOTA_{a}"))
                resp = row.get(f"TX_RESPOSTAS_{a}") or ""
                if nota is None or nota <= 0 or not resp:
                    continue
                lingua = row.get("TP_LINGUA", "") if a == "LC" else ""
                ac, val, ad = metrics(resp, a, itens[(a, code)], lingua)
                if val == 0 or ac < 1 or ad is None:
                    continue
                rec = (ac, round(nota, 1), round(ad, 4))
                if ac >= IV[a] - 3:      # cauda superior: guarda TODOS
                    tail[a].append(rec)
                else:                     # miolo: reservoir sampling
                    seen_bulk[a] += 1
                    if len(bulk[a]) < TARGET_BULK:
                        bulk[a].append(rec)
                    else:
                        j = rng.randrange(seen_bulk[a])
                        if j < TARGET_BULK:
                            bulk[a][j] = rec

    print(f"\nTotal linhas: {lidas:,}")
    for a in AREAS:
        recs = bulk[a] + tail[a]
        recs.sort()
        mx = max(r[0] for r in recs)
        n_mx = sum(1 for r in recs if r[0] == mx)
        nota_mx = max(r[1] for r in recs if r[0] == mx)
        with (OUTDIR / f"scatter_{a}.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["acertos", "nota", "acert_dif"])
            w.writerows(recs)
        print(f"  {a}: plot n={len(recs):,} (miolo {len(bulk[a]):,} + cauda {len(tail[a]):,}) "
              f"| MAX acertos={mx} (de {IV[a]}), n_no_topo={n_mx}, nota_max={nota_mx}")


if __name__ == "__main__":
    main()
