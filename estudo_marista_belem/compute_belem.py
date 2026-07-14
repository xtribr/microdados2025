#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute do estudo Marista Belém (aplicação COP30/BAM). Mesma metodologia do
pipeline por escola (CEI/Marista Natal), com UMA diferença estrutural: todas as
referências item a item (habilidade, dificuldade, discriminação) são a COORTE
COP30 (~62k presentes de Belém-Ananindeua-Marituba, MESMA prova) — não o BR
regular, que fez itens diferentes (zero em comum). Nota TRI, por ser escala
equalizada, compara com BR regular P1 e com a rede Marista.

Categoria de dificuldade: quartis de dif_xtri (100×(1−P(θ=0)), 3PL D=1,7)
dentro de cada área, sobre os 45 itens da prova BAM.
"""
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
CFG = json.loads((D / "config.json").read_text())
NOME = CFG["curto"]

AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
LETRAS = set("ABCDE")
EASY_B, HARD_B = 0.6, 1.6
DISC_ORDER = ["baixa/moderada (A<1,35)", "alta (1,35–1,69)", "muito alta (A≥1,70)"]
CAT_ORDER = ["Fácil", "Médio", "Difícil", "Muito difícil"]

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
        return float(str(v).replace(",", ".")) if v not in (None, "") else None
    except ValueError:
        return None


def disc_bucket(a):
    if a is None:
        return None
    if a < 1.35:
        return DISC_ORDER[0]
    if a < 1.70:
        return DISC_ORDER[1]
    return DISC_ORDER[2]


def dif_xtri(a, b, c):
    p = c + (1 - c) / (1 + math.exp(1.7 * a * b))
    return 100 * (1 - p)


def load_itens_bam():
    wanted = {(ar, ic) for ar, m in BAM_RESULT_TO_ITEM.items() for ic in m.values()}
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
    return itens


def categorias_por_quartil(itens):
    """{co_item: categoria} — quartis de dif_xtri por área (45 itens únicos/área;
    LC considera os 40 comuns + 5 da língua como itens distintos, ~50)."""
    uniq = {}
    for (ar, _), its in itens.items():
        for it in its:
            if it["co_item"] not in uniq and it["A"] is not None:
                uniq[it["co_item"]] = (ar, dif_xtri(it["A"], it["B"], it["C"]))
    cat = {}
    by_area = defaultdict(list)
    for ci, (ar, d) in uniq.items():
        by_area[ar].append((d, ci))
    for ar, lst in by_area.items():
        lst.sort()
        n = len(lst)
        for i, (_, ci) in enumerate(lst):
            cat[ci] = CAT_ORDER[min(3, i * 4 // n)]
    return cat, {ci: d for ci, (_, d) in uniq.items()}


def load_ref_cop30_itens():
    """Referência COP30 item a item -> agregados por hab/categoria/disc."""
    rows = []
    with (D / "itens_cop30.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["A"] = pf(r["A"])
            r["pct"] = pf(r["pct_acerto_cop30"])
            r["n"] = pf(r["respostas_cop30"]) or 0
            rows.append(r)
    return rows


def main():
    itens = load_itens_bam()
    cat_map, dif_map = categorias_por_quartil(itens)
    ref_itens = load_ref_cop30_itens()
    ref_cop30 = json.loads((D / "referencia_cop30.json").read_text())
    ref_nac = json.loads((D / "referencia_nacional.json").read_text())

    # referências COP30 agregadas (ponderadas por nº de respostas da coorte)
    nac_hab, nac_cat, nac_disc = {}, {}, {}
    acc_h = defaultdict(lambda: [0.0, 0.0])
    acc_c = defaultdict(lambda: [0.0, 0.0])
    acc_d = defaultdict(lambda: [0.0, 0.0])
    for r in ref_itens:
        if r["pct"] is None or not r["n"]:
            continue
        acc_h[(r["area"], r["habilidade"])][0] += r["pct"] * r["n"]
        acc_h[(r["area"], r["habilidade"])][1] += r["n"]
        cat = cat_map.get(r["co_item"])
        if cat:
            acc_c[(r["area"], cat)][0] += r["pct"] * r["n"]
            acc_c[(r["area"], cat)][1] += r["n"]
        db = disc_bucket(r["A"])
        if db:
            acc_d[(r["area"], db)][0] += r["pct"] * r["n"]
            acc_d[(r["area"], db)][1] += r["n"]
    nac_hab = {k: round(100 - v[0] / v[1], 1) for k, v in acc_h.items() if v[1]}  # ERRO %
    nac_cat = {k: round(v[0] / v[1], 1) for k, v in acc_c.items() if v[1]}        # ACERTO %
    nac_disc = {k: round(v[0] / v[1], 1) for k, v in acc_d.items() if v[1]}

    hab_err = defaultdict(lambda: [0, 0])
    cat_ac = defaultdict(lambda: [0, 0])
    dsc_ac = defaultdict(lambda: [0, 0])
    alunos, area_rows = [], []
    notas_area = defaultdict(list)
    redacoes = []
    comps = defaultdict(list)
    lingua_cnt = defaultdict(int)
    provas_vistas = defaultdict(int)
    extraidos = fora_bam = 0

    with (D / "alunos.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            extraidos += 1
            lingua = (row["TP_LINGUA"] or "").strip()
            lingua_cnt[lingua] += 1
            red = pf(row["NU_NOTA_REDACAO"])
            if red is not None and red > 0:
                redacoes.append(red)
                for i in range(1, 6):
                    v = pf(row.get(f"NU_NOTA_COMP{i}"))
                    if v is not None:
                        comps[i].append(v)
            tot_ac = tot_itens = incoer = 0
            areas_ok = 0
            notas = {}
            for a in AREAS:
                if row.get(f"TP_PRESENCA_{a}") != "1":
                    continue
                cp = (row.get(f"CO_PROVA_{a}") or "").strip()
                provas_vistas[f"{a}:{cp}"] += 1
                ic = BAM_RESULT_TO_ITEM[a].get(cp)
                nota = pf(row.get(f"NU_NOTA_{a}"))
                resp = row.get(f"TX_RESPOSTAS_{a}") or ""
                its = itens.get((a, ic)) if ic else None
                if nota is None or nota <= 0:
                    continue
                # nota TRI vale para TODOS (escala equalizada entre aplicações)
                notas_area[a].append(nota)
                if not ic:
                    fora_bam += 1
                if not resp or not its:
                    continue  # item a item: só o subgrupo BAM (mesma prova da coorte)
                notas[a] = nota
                areas_ok += 1
                off = AREA_START[a]
                ac_a = ef = ad = 0
                for it in its:
                    if a == "LC" and it["lingua"] and it["lingua"] != lingua:
                        continue
                    idx = it["pos"] - off
                    if idx < 0 or idx >= len(resp):
                        continue
                    ok = resp[idx].upper() == it["gab"] and it["gab"] in LETRAS
                    ac_a += ok
                    tot_itens += 1
                    tot_ac += ok
                    hab_err[(a, it["hab"])][1] += 1
                    hab_err[(a, it["hab"])][0] += (not ok)
                    cat = cat_map.get(it["co_item"])
                    if cat:
                        cat_ac[(a, cat)][1] += 1
                        cat_ac[(a, cat)][0] += ok
                    db = disc_bucket(it["A"])
                    if db:
                        dsc_ac[(a, db)][1] += 1
                        dsc_ac[(a, db)][0] += ok
                    if it["B"] is not None:
                        if it["B"] <= EASY_B and not ok:
                            ef += 1
                        elif it["B"] >= HARD_B and ok:
                            ad += 1
                inc_a = min(ef, ad)
                incoer += inc_a
                area_rows.append([NOME, a, ac_a, nota, inc_a])
            if areas_ok:
                alunos.append({"escola": NOME, "areas": areas_ok, "acertos": tot_ac,
                               "itens": tot_itens, "nota_media": round(sum(notas.values()) / len(notas), 1),
                               "incoer": incoer})

    with (D / "habilidades.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "habilidade", "erro_pct", "n_resp", "erro_cop30"])
        for (a, h), (e, t) in sorted(hab_err.items()):
            if t >= 20:
                w.writerow([NOME, a, h, round(100 * e / t, 1), t, nac_hab.get((a, h), "")])
    with (D / "categorias.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "categoria", "acerto_pct", "n_resp", "acerto_cop30"])
        for (a, c), (ac, t) in sorted(cat_ac.items()):
            w.writerow([NOME, a, c, round(100 * ac / t, 1), t, nac_cat.get((a, c), "")])
    with (D / "disc.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "faixa_disc", "acerto_pct", "n_resp", "acerto_cop30"])
        for (a, b), (ac, t) in sorted(dsc_ac.items()):
            w.writerow([NOME, a, b, round(100 * ac / t, 1), t, nac_disc.get((a, b), "")])
    with (D / "alunos_proc.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(alunos[0].keys()))
        w.writeheader()
        w.writerows(alunos)
    with (D / "alunos_area.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "acertos", "nota", "incoer"])
        w.writerows(area_rows)
    with (D / "itens_categoria.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["co_item", "area", "dif_xtri", "categoria"])
        for r in ref_itens:
            ci = r["co_item"]
            if ci in cat_map:
                w.writerow([ci, r["area"], round(dif_map[ci], 1), cat_map[ci]])

    red_comp = {}
    for i in range(1, 6):
        vals = comps[i]
        if vals:
            red_comp[f"C{i}"] = {"media": round(statistics.mean(vals), 1), "n": len(vals),
                                 "pct_200": round(100 * sum(1 for v in vals if v == 200) / len(vals), 1),
                                 "pct_ate_120": round(100 * sum(1 for v in vals if v <= 120) / len(vals), 1)}
    (D / "redacao_comp.json").write_text(json.dumps({NOME: red_comp}, ensure_ascii=False, indent=2))

    full = [al for al in alunos if al["areas"] == 4]
    incs = [al["incoer"] for al in full] or [0]
    resumo = {"nome": CFG["nome"], "co_escola": CFG["co_escola"],
              "aplicacao": CFG["aplicacao"], "extraidos": extraidos,
              "processados_bam": len(alunos), "presentes_4_bam": len(full),
              "areas_fora_bam_p1_regular": fora_bam,
              "provas_vistas": dict(sorted(provas_vistas.items())),
              "medias_todos": {a: round(statistics.mean(notas_area[a]), 1) for a in AREAS if notas_area[a]},
              "n_notas": {a: len(notas_area[a]) for a in AREAS},
              "redacao_media": round(statistics.mean(redacoes), 1) if redacoes else None,
              "redacoes_validas": len(redacoes),
              "incoer": {"media": round(statistics.mean(incs), 2), "mediana": statistics.median(incs),
                         "max": max(incs), "zero_pct": round(100 * sum(1 for i in incs if i == 0) / len(incs), 1)},
              "lingua": {"ingles": lingua_cnt.get("0", 0), "espanhol": lingua_cnt.get("1", 0)},
              "cop30": {a: ref_cop30["medias"].get(a) for a in AREAS},
              "cop30_redacao": ref_cop30["redacao"],
              "nacional_regular_p1": {a: ref_nac["nacional_regular_p1"][a]["media"] for a in AREAS}}
    (D / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
