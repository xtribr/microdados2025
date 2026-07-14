#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extração única do RESULTADOS_2025 para o estudo Marista Belém (COP30/BAM):
1) alunos.csv — linhas do CO_ESCOLA 15038424;
2) referencia_cop30.json + itens_cop30.csv — coorte COP30/BAM inteira (mesma prova
   da escola): média TRI por área, redação C1-C5 e %acerto item a item (por co_item).

Cadernos BAM em RESULTADOS (1583-1634) têm itens/params publicados em ITENS_PROVA
sob OUTROS códigos (1502-1532) — mapa validado por gabarito no estudo PRIMI
(analises_primi_2025_cop30/scripts/gerar_primi_cop30_2025.py, BAM_RESULT_TO_ITEM_CODE).
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
SRC = BASE / "DADOS/RESULTADOS_2025.csv"
CO_ESCOLA = "15038424"

AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
LETRAS = set("ABCDE")

# CO_PROVA em RESULTADOS -> CO_PROVA em ITENS_PROVA (mapa validado por gabarito)
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

KEEP = (["CO_ESCOLA", "NO_MUNICIPIO_ESC", "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC",
         "TP_LOCALIZACAO_ESC", "TP_LINGUA", "NU_NOTA_REDACAO"]
        + [f"TP_PRESENCA_{a}" for a in AREAS] + [f"CO_PROVA_{a}" for a in AREAS]
        + [f"NU_NOTA_{a}" for a in AREAS] + [f"TX_RESPOSTAS_{a}" for a in AREAS]
        + [f"NU_NOTA_COMP{i}" for i in range(1, 6)])


def pf(v):
    try:
        return float(v) if v else None
    except ValueError:
        return None


def load_itens():
    """{(area, item_code): [itens]} só dos cadernos BAM mapeados."""
    wanted = {(a, ic) for a, m in BAM_RESULT_TO_ITEM.items() for ic in m.values()}
    itens = defaultdict(list)
    with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            k = (r["SG_AREA"].strip(), r["CO_PROVA"].strip())
            if k not in wanted or r["IN_ITEM_ABAN"] == "1":
                continue
            itens[k].append({
                "pos": int(r["CO_POSICAO"]),
                "gab": (r["TX_GABARITO"] or "").strip().upper(),
                "lingua": (r["TP_LINGUA"] or "").strip().split(".")[0],
                "co_item": r["CO_ITEM"].strip(),
                "hab": f"H{int(r['CO_HABILIDADE'])}",
                "A": pf(r["NU_PARAM_A"]), "B": pf(r["NU_PARAM_B"]), "C": pf(r["NU_PARAM_C"]),
            })
    for k in itens:
        itens[k].sort(key=lambda it: it["pos"])
    return itens


def main():
    itens = load_itens()
    print("Cadernos BAM carregados de ITENS_PROVA:",
          {f"{a}:{c}": len(v) for (a, c), v in sorted(itens.items())}, flush=True)

    out = (D / "alunos.csv").open("w", newline="", encoding="utf-8")
    w = csv.writer(out)
    w.writerow(KEEP)

    # acumuladores da coorte COP30 (todas as provas BAM, todas as escolas)
    item_ac = defaultdict(lambda: [0, 0])          # co_item -> [acertos, respostas]
    notas = defaultdict(lambda: [0.0, 0])          # area -> [soma, n]
    comps = defaultdict(lambda: [0.0, 0, 0, 0])    # Ci -> [soma, n, n200, n<=120]
    red_sum, red_n = 0.0, 0
    escola_rows = 0
    gab_check = defaultdict(lambda: [0, 0])        # cross-check: posições conferidas/divergentes

    lidas = 0
    with SRC.open(encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  {lidas:,} linhas | escola={escola_rows} | cop30 LC n={notas['LC'][1]:,}", flush=True)

            if (row.get("CO_ESCOLA") or "").strip() == CO_ESCOLA:
                escola_rows += 1
                w.writerow([row.get(k, "") for k in KEEP])

            lingua = (row.get("TP_LINGUA") or "").strip()
            is_bam = False
            for a in AREAS:
                cp = (row.get(f"CO_PROVA_{a}") or "").strip()
                ic = BAM_RESULT_TO_ITEM[a].get(cp)
                if not ic or row.get(f"TP_PRESENCA_{a}") != "1":
                    continue
                nota = pf(row.get(f"NU_NOTA_{a}"))
                resp = row.get(f"TX_RESPOSTAS_{a}") or ""
                its = itens.get((a, ic))
                if nota is None or nota <= 0 or not resp or not its:
                    continue
                is_bam = True
                notas[a][0] += nota
                notas[a][1] += 1
                off = AREA_START[a]
                # cross-check de gabarito (protocolo COP30): ITENS vs TX_GABARITO do aluno
                gab_of = row.get(f"TX_GABARITO_{a}") or ""
                if a == "LC" and len(gab_of) == 50:
                    gab45 = (gab_of[:5] if lingua == "0" else gab_of[5:10]) + gab_of[10:]
                else:
                    gab45 = gab_of
                for it in its:
                    if a == "LC" and it["lingua"] and it["lingua"] != lingua:
                        continue
                    idx = it["pos"] - off
                    if idx < 0 or idx >= len(resp):
                        continue
                    if idx < len(gab45) and gab45[idx] in LETRAS and it["gab"] in LETRAS:
                        k = (a, (row.get(f"CO_PROVA_{a}") or "").strip())
                        gab_check[k][0] += 1
                        gab_check[k][1] += (gab45[idx] != it["gab"])
                    ok = it["gab"] in LETRAS and resp[idx].upper() == it["gab"]
                    item_ac[it["co_item"]][1] += 1
                    item_ac[it["co_item"]][0] += ok

            if is_bam:
                red = pf(row.get("NU_NOTA_REDACAO"))
                if red is not None and red > 0:
                    red_sum += red
                    red_n += 1
                    for i in range(1, 6):
                        v = pf(row.get(f"NU_NOTA_COMP{i}"))
                        if v is not None:
                            c = comps[i]
                            c[0] += v
                            c[1] += 1
                            c[2] += (v == 200)
                            c[3] += (v <= 120)
    out.close()

    # itens_cop30.csv: um por co_item com params + %acerto da coorte
    seen = {}
    for (a, ic), its in itens.items():
        for it in its:
            if it["co_item"] not in seen:
                seen[it["co_item"]] = {"area": a, **it}
    with (D / "itens_cop30.csv").open("w", newline="", encoding="utf-8") as f:
        wi = csv.writer(f)
        wi.writerow(["area", "co_item", "habilidade", "lingua", "A", "B", "C",
                     "acertos_cop30", "respostas_cop30", "pct_acerto_cop30"])
        for ci, it in sorted(seen.items(), key=lambda x: (x[1]["area"], x[1]["pos"])):
            ac, tot = item_ac.get(ci, [0, 0])
            wi.writerow([it["area"], ci, it["hab"], it["lingua"], it["A"], it["B"], it["C"],
                         ac, tot, round(100 * ac / tot, 2) if tot else ""])

    div = {f"{k[0]}:{k[1]}": f"{v[1]}/{v[0]}" for k, v in sorted(gab_check.items()) if v[1]}
    ref = {
        "coorte": "COP30/BAM (presentes por área, nota>0)",
        "medias": {a: round(notas[a][0] / notas[a][1], 1) for a in AREAS if notas[a][1]},
        "n": {a: notas[a][1] for a in AREAS},
        "redacao": {"media": round(red_sum / red_n, 1) if red_n else None, "n": red_n},
        "redacao_comp": {f"C{i}": {"media": round(c[0] / c[1], 1), "n": c[1],
                                   "pct_200": round(100 * c[2] / c[1], 1),
                                   "pct_ate_120": round(100 * c[3] / c[1], 1)}
                         for i, c in sorted(comps.items()) if c[1]},
        "gabarito_divergencias": div or "zero — mapa RESULTADOS->ITENS confere",
    }
    (D / "referencia_cop30.json").write_text(json.dumps(ref, ensure_ascii=False, indent=2))
    print(f"\nFIM: {lidas:,} linhas | escola: {escola_rows} | cop30 n: {ref['n']}")
    print("Cross-check gabarito:", ref["gabarito_divergencias"])


if __name__ == "__main__":
    main()
