#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise CEI (Romualdo × Roberto Freire) — correção item a item dos 212 alunos:
 - erro por habilidade por área (vs nacional)
 - acerto por categoria de dificuldade (Fácil→Muito difícil, mapa XTRI por co_item) e
   por faixa de discriminação (Baker, via parâmetro A)
 - índice de chute (incoerência person-fit: min(erros em fáceis b<=0.6, acertos em difíceis b>=1.6))
 - notas TRI por aluno/área vs média nacional
Fontes: alunos_cei.csv (RESULTADOS/INEP), ITENS_PROVA_2025 (INEP),
itens_sequencia_dificuldade_2025.csv (categorias XTRI), habilidades_dificuldade_2025.csv (nacional).
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
D = BASE / "estudo_cei_natal"
AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
LETRAS = set("ABCDE")
EASY_B, HARD_B = 0.6, 1.6
ESCOLA_NOME = {"24069191": "CEI Romualdo", "24089214": "CEI Roberto Freire"}
CAT_ORDER = ["Fácil", "Médio", "Difícil", "Muito difícil"]
DISC_ORDER = ["baixa/moderada (A<1,35)", "alta (1,35–1,69)", "muito alta (A≥1,70)"]


def pf(v):
    if not v:
        return None
    try:
        return float(str(v).replace(",", "."))
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
            if r["IN_ITEM_ABAN"] == "1":
                continue
            area = r["SG_AREA"].strip()
            if area not in AREA_START:
                continue
            itens[(area, r["CO_PROVA"].strip())].append({
                "pos": int(r["CO_POSICAO"]), "gab": (r["TX_GABARITO"] or "").strip().upper(),
                "A": pf(r["NU_PARAM_A"]), "B": pf(r["NU_PARAM_B"]), "C": pf(r["NU_PARAM_C"]),
                "lingua": (r["TP_LINGUA"] or "").strip(), "hab": f"H{int(r['CO_HABILIDADE'])}",
                "co_item": r["CO_ITEM"].strip()})
    return itens


def load_categorias():
    """co_item -> categoria XTRI (do estudo de dificuldade, P1 regular)."""
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
    """erro/acerto nacional por (area, categoria) e por (area, disc bucket), ponderado pelo nº de respondentes."""
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
    nc = {k: round(v[0] / v[1], 1) for k, v in acc_cat.items() if v[1] > 0}
    nd = {k: round(v[0] / v[1], 1) for k, v in acc_dsc.items() if v[1] > 0}
    return nc, nd


def main():
    itens = load_itens_prova()
    cat_map = load_categorias()
    nac_hab = load_nacional_hab()
    nac_cat, nac_disc = nacional_categorias()

    hab_err = defaultdict(lambda: [0, 0])     # (esc, area, hab) -> [erros, total]
    cat_ac = defaultdict(lambda: [0, 0])      # (esc, area, categoria) -> [acertos, total]
    dsc_ac = defaultdict(lambda: [0, 0])      # (esc, area, bucket) -> [acertos, total]
    alunos = []
    notas_area = defaultdict(list)            # (esc, area) -> notas
    red_area = defaultdict(list)              # esc -> redação
    lingua_cnt = defaultdict(int)
    sem_cat = 0

    with (D / "alunos_cei.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            esc = row["CO_ESCOLA"].strip()
            lingua = (row["TP_LINGUA"] or "").strip()
            lingua_cnt[(esc, lingua)] += 1
            red = pf(row["NU_NOTA_REDACAO"])
            if red is not None and red > 0:
                red_area[esc].append(red)
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
                notas_area[(esc, a)].append(nota)
                areas_ok += 1
                off = AREA_START[a]
                ef = ad = 0
                for it in its:
                    if a == "LC" and it["lingua"] and it["lingua"] != lingua:
                        continue
                    idx = it["pos"] - off
                    if idx < 0 or idx >= len(resp):
                        continue
                    ok = resp[idx].upper() == it["gab"] and it["gab"] in LETRAS
                    tot_itens += 1
                    tot_ac += ok
                    k = (esc, a, it["hab"])
                    hab_err[k][1] += 1
                    hab_err[k][0] += (not ok)
                    cat = cat_map.get(it["co_item"])
                    if cat:
                        kc = (esc, a, cat)
                        cat_ac[kc][1] += 1
                        cat_ac[kc][0] += ok
                    else:
                        sem_cat += 1
                    db = disc_bucket(it["A"])
                    if db:
                        kd = (esc, a, db)
                        dsc_ac[kd][1] += 1
                        dsc_ac[kd][0] += ok
                    if it["B"] is not None:
                        if it["B"] <= EASY_B and not ok:
                            ef += 1
                        elif it["B"] >= HARD_B and ok:
                            ad += 1
                incoer += min(ef, ad)
            if areas_ok:
                media = round(sum(notas.values()) / len(notas), 1)
                alunos.append({"escola": ESCOLA_NOME[esc], "areas": areas_ok,
                               "acertos": tot_ac, "itens": tot_itens,
                               "nota_media": media, "incoer": incoer,
                               **{f"nota_{a}": notas.get(a, "") for a in AREAS}})

    # ---- exports ----
    with (D / "cei_habilidades.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "habilidade", "erro_pct", "n_resp", "erro_nacional"])
        for (esc, a, h), (e, t) in sorted(hab_err.items()):
            if t >= 20:  # denominador mínimo p/ % estável
                w.writerow([ESCOLA_NOME[esc], a, h, round(100 * e / t, 1), t, nac_hab.get((a, h), "")])

    with (D / "cei_categorias.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "categoria", "acerto_pct", "n_resp", "acerto_nacional"])
        for (esc, a, c), (ac, t) in sorted(cat_ac.items()):
            w.writerow([ESCOLA_NOME[esc], a, c, round(100 * ac / t, 1), t, nac_cat.get((a, c), "")])

    with (D / "cei_disc.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["escola", "area", "faixa_disc", "acerto_pct", "n_resp", "acerto_nacional"])
        for (esc, a, b), (ac, t) in sorted(dsc_ac.items()):
            w.writerow([ESCOLA_NOME[esc], a, b, round(100 * ac / t, 1), t, nac_disc.get((a, b), "")])

    with (D / "cei_alunos.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(alunos[0].keys()))
        w.writeheader()
        w.writerows(alunos)

    ref = json.loads((D / "referencia_nacional.json").read_text())
    resumo = {"n_alunos": {ESCOLA_NOME[e]: sum(1 for al in alunos if al["escola"] == ESCOLA_NOME[e]) for e in ESCOLA_NOME},
              "medias": {}, "redacao": {}, "incoer": {}, "lingua": {}}
    for e, nome in ESCOLA_NOME.items():
        resumo["medias"][nome] = {a: round(statistics.mean(notas_area[(e, a)]), 1)
                                  for a in AREAS if notas_area[(e, a)]}
        resumo["redacao"][nome] = round(statistics.mean(red_area[e]), 1) if red_area[e] else None
        incs = [al["incoer"] for al in alunos if al["escola"] == nome and al["areas"] == 4]
        resumo["incoer"][nome] = {"media": round(statistics.mean(incs), 2), "mediana": statistics.median(incs),
                                  "max": max(incs), "zero_pct": round(100 * sum(1 for i in incs if i == 0) / len(incs), 1),
                                  "n": len(incs)}
        resumo["lingua"][nome] = {"ingles": lingua_cnt[(e, "0")], "espanhol": lingua_cnt[(e, "1")]}
    resumo["nacional_regular_p1"] = {a: ref["nacional_regular_p1"][a]["media"] for a in AREAS}
    resumo["chutes_nacional"] = json.loads((D / "chutes_counts.json").read_text())["categorias"]
    (D / "cei_resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))

    print(f"alunos processados: {len(alunos)} | itens sem categoria XTRI (fora P1): {sem_cat}")
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
