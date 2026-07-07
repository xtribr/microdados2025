#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline por escola (lê config.json da própria pasta): correção item a item →
erro por habilidade, acerto por dificuldade (mapa XTRI) e discriminação (Baker),
incoerência (total e por área), redação C1-C5 e resumo. Mesma metodologia do estudo CEI.
"""
import csv
import json
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


def pf(v):
    try:
        return float(str(v).replace(",", ".")) if v else None
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


def load_itens_prova():
    itens = defaultdict(list)
    with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["IN_ITEM_ABAN"] == "1" or r["SG_AREA"].strip() not in AREA_START:
                continue
            itens[(r["SG_AREA"].strip(), r["CO_PROVA"].strip())].append({
                "pos": int(r["CO_POSICAO"]), "gab": (r["TX_GABARITO"] or "").strip().upper(),
                "A": pf(r["NU_PARAM_A"]), "B": pf(r["NU_PARAM_B"]),
                "lingua": (r["TP_LINGUA"] or "").strip(), "hab": f"H{int(r['CO_HABILIDADE'])}",
                "co_item": r["CO_ITEM"].strip()})
    return itens


def load_categorias():
    cat = {}
    with (BASE / "analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ci = str(r["co_item"]).split(".")[0].strip()
            if ci and r.get("categoria"):
                cat[ci] = r["categoria"]
    return cat


def load_nacional_hab():
    nac = {}
    with (BASE / "analises_primi_2025_cop30/outputs/habilidades_dificuldade_2025.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            hab = r["habilidade"]
            hab = hab if hab.startswith("H") else f"H{hab}"
            nac[(r["area"], hab)] = round(100 - float(r["pct_acerto_ponderado"]), 1)
    return nac


def nacional_categorias():
    acc_cat = defaultdict(lambda: [0.0, 0.0])
    acc_dsc = defaultdict(lambda: [0.0, 0.0])
    with (BASE / "analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                pct = float(r["pct_acerto"]); tot = float(r["total"]); a = float(r["A"])
            except (ValueError, KeyError):
                continue
            if r.get("categoria"):
                k = (r["area"], r["categoria"])
                acc_cat[k][0] += pct * tot
                acc_cat[k][1] += tot
            db = disc_bucket(a)
            if db:
                k = (r["area"], db)
                acc_dsc[k][0] += pct * tot
                acc_dsc[k][1] += tot
    return ({k: round(v[0] / v[1], 1) for k, v in acc_cat.items() if v[1] > 0},
            {k: round(v[0] / v[1], 1) for k, v in acc_dsc.items() if v[1] > 0})


def main():
    itens = load_itens_prova()
    cat_map = load_categorias()
    nac_hab = load_nacional_hab()
    nac_cat, nac_disc = nacional_categorias()

    hab_err = defaultdict(lambda: [0, 0])
    cat_ac = defaultdict(lambda: [0, 0])
    dsc_ac = defaultdict(lambda: [0, 0])
    alunos = []
    area_rows = []
    notas_area = defaultdict(list)
    redacoes = []
    comps = defaultdict(list)
    lingua_cnt = defaultdict(int)
    sem_cat = 0
    extraidos = 0

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
                nota = pf(row.get(f"NU_NOTA_{a}"))
                resp = row.get(f"TX_RESPOSTAS_{a}") or ""
                its = itens.get((a, (row.get(f"CO_PROVA_{a}") or "").strip()))
                if nota is None or nota <= 0 or not resp or not its:
                    continue
                notas[a] = nota
                notas_area[a].append(nota)
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
                    k = (a, it["hab"])
                    hab_err[k][1] += 1
                    hab_err[k][0] += (not ok)
                    cat = cat_map.get(it["co_item"])
                    if cat:
                        cat_ac[(a, cat)][1] += 1
                        cat_ac[(a, cat)][0] += ok
                    else:
                        sem_cat += 1
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
        w.writerow(["escola", "area", "habilidade", "erro_pct", "n_resp", "erro_nacional"])
        for (a, h), (e, t) in sorted(hab_err.items()):
            if t >= 20:
                w.writerow([NOME, a, h, round(100 * e / t, 1), t, nac_hab.get((a, h), "")])
    with (D / "categorias.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "categoria", "acerto_pct", "n_resp", "acerto_nacional"])
        for (a, c), (ac, t) in sorted(cat_ac.items()):
            w.writerow([NOME, a, c, round(100 * ac / t, 1), t, nac_cat.get((a, c), "")])
    with (D / "disc.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "faixa_disc", "acerto_pct", "n_resp", "acerto_nacional"])
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

    red_comp = {}
    for i in range(1, 6):
        vals = comps[i]
        if vals:
            red_comp[f"C{i}"] = {"media": round(statistics.mean(vals), 1), "n": len(vals),
                                 "pct_200": round(100 * sum(1 for v in vals if v == 200) / len(vals), 1),
                                 "pct_ate_120": round(100 * sum(1 for v in vals if v <= 120) / len(vals), 1)}
    (D / "redacao_comp.json").write_text(json.dumps({NOME: red_comp}, ensure_ascii=False, indent=2))

    ref = json.loads((D / "referencia_nacional.json").read_text())
    full = [al for al in alunos if al["areas"] == 4]
    incs = [al["incoer"] for al in full]
    resumo = {"nome": CFG["nome"], "co_escola": CFG["co_escola"], "extraidos": extraidos,
              "processados": len(alunos), "presentes_4": len(full),
              "medias": {a: round(statistics.mean(notas_area[a]), 1) for a in AREAS if notas_area[a]},
              "redacao_media": round(statistics.mean(redacoes), 1) if redacoes else None,
              "redacoes_validas": len(redacoes),
              "incoer": {"media": round(statistics.mean(incs), 2), "mediana": statistics.median(incs),
                         "max": max(incs), "zero_pct": round(100 * sum(1 for i in incs if i == 0) / len(incs), 1)},
              "lingua": {"ingles": lingua_cnt.get("0", 0), "espanhol": lingua_cnt.get("1", 0)},
              "nacional_regular_p1": {a: ref["nacional_regular_p1"][a]["media"] for a in AREAS},
              "sem_categoria": sem_cat}
    (D / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
