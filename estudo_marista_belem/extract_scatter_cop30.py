#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Passada 2 — nuvem da coorte COP30 para os gráficos de incoerência/chutes:
por aluno BAM: acertos × nota por área (plot_data/scatter_{area}.csv) e
acertos totais × nota média (presentes-4) (chutes_scatter_cop30.csv).
Entrada: arquivo pré-filtrado por grep (linhas com código BAM) + header.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
SRC = Path(sys.argv[1])  # pré-filtrado

AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
LETRAS = set("ABCDE")
EASY_B, HARD_B = 0.6, 1.6

BAM_RESULT_TO_ITEM = {
    "CH": {"1583": "1520", "1584": "1521", "1585": "1522", "1586": "1523",
           "1587": "1522", "1631": "1522"},
    "LC": {"1595": "1529", "1596": "1530", "1597": "1531", "1598": "1532",
           "1599": "1532", "1632": "1532"},
    "MT": {"1607": "1502", "1608": "1503", "1609": "1504", "1610": "1505",
           "1611": "1505", "1633": "1505"},
    "CN": {"1619": "1511", "1620": "1512", "1621": "1514", "1622": "1513",
           "1623": "1513", "1634": "1513"},
}


def pf(v):
    try:
        return float(v) if v else None
    except ValueError:
        return None


def load_itens():
    wanted = {(a, ic) for a, m in BAM_RESULT_TO_ITEM.items() for ic in m.values()}
    itens = defaultdict(list)
    with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            k = (r["SG_AREA"].strip(), r["CO_PROVA"].strip())
            if k not in wanted or r["IN_ITEM_ABAN"] == "1":
                continue
            itens[k].append({"pos": int(r["CO_POSICAO"]),
                             "gab": (r["TX_GABARITO"] or "").strip().upper(),
                             "lingua": (r["TP_LINGUA"] or "").strip().split(".")[0],
                             "B": pf(r["NU_PARAM_B"])})
    return itens


def main():
    itens = load_itens()
    # header do RESULTADOS original
    with (BASE / "DADOS/RESULTADOS_2025.csv").open(encoding="latin-1") as f:
        header = f.readline().rstrip("\n").split(";")

    (D / "plot_data").mkdir(exist_ok=True)
    wa = {}
    fa = {}
    for a in AREAS:
        fa[a] = (D / "plot_data" / f"scatter_{a}.csv").open("w", newline="", encoding="utf-8")
        wa[a] = csv.writer(fa[a])
        wa[a].writerow(["acertos", "nota", "incoer"])
    fch = (D / "chutes_scatter_cop30.csv").open("w", newline="", encoding="utf-8")
    wch = csv.writer(fch)
    wch.writerow(["acertos", "nota_media", "incoer"])

    lidas = usados = 0
    with SRC.open(encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f, fieldnames=header, delimiter=";"):
            lidas += 1
            lingua = (row.get("TP_LINGUA") or "").strip()
            tot_ac = areas_ok = incoer = 0
            notas = []
            eh_bam = False
            for a in AREAS:
                if row.get(f"TP_PRESENCA_{a}") != "1":
                    continue
                cp = (row.get(f"CO_PROVA_{a}") or "").strip()
                ic = BAM_RESULT_TO_ITEM[a].get(cp)
                if not ic:
                    continue
                nota = pf(row.get(f"NU_NOTA_{a}"))
                resp = row.get(f"TX_RESPOSTAS_{a}") or ""
                its = itens.get((a, ic))
                if nota is None or nota <= 0 or not resp or not its:
                    continue
                eh_bam = True
                off = AREA_START[a]
                ac = ef = ad = 0
                for it in its:
                    if a == "LC" and it["lingua"] and it["lingua"] != lingua:
                        continue
                    idx = it["pos"] - off
                    if idx < 0 or idx >= len(resp):
                        continue
                    ok = resp[idx].upper() == it["gab"] and it["gab"] in LETRAS
                    ac += ok
                    if it["B"] is not None:
                        if it["B"] <= EASY_B and not ok:
                            ef += 1
                        elif it["B"] >= HARD_B and ok:
                            ad += 1
                inc = min(ef, ad)
                wa[a].writerow([ac, nota, inc])
                tot_ac += ac
                incoer += inc
                notas.append(nota)
                areas_ok += 1
            if eh_bam:
                usados += 1
            if areas_ok == 4:
                wch.writerow([tot_ac, round(sum(notas) / 4, 1), incoer])
    for fp in fa.values():
        fp.close()
    fch.close()
    print(f"linhas pré-filtradas: {lidas:,} | alunos BAM usados: {usados:,}")


if __name__ == "__main__":
    main()
