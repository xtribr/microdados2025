#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uma passada no RESULTADOS_2025 (Regular P1) computando:
 A) CHUTES / INCOERÊNCIA — por candidato, nas 4 áreas: quantas vezes errou item FÁCIL
    e acertou item DIFÍCIL (padrão de resposta incoerente = chute desordenado / person-fit).
    Fácil: b <= 0.6 (TRI<=560). Difícil: b >= 1.6 (TRI>=660). incoer_area = min(erros_faceis, acertos_dificeis).
 B) INGLÊS × ESPANHOL — no bloco de língua (5 itens) do LC: nota por acertos por língua (mediana)
    + coleta de CASOS REAIS de alunos (indivíduos) para comparar ing vs esp com mesmo desempenho.
"""
import csv
import json
import random
from collections import defaultdict
from pathlib import Path
import statistics

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
DADOS = BASE / "DADOS"
OUT = BASE / "palestra_2025"

AREAS = ["LC", "CH", "CN", "MT"]
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}
REGULAR = {
    "LC": {"1459", "1460", "1461", "1462"}, "CH": {"1447", "1448", "1449", "1450"},
    "CN": {"1483", "1484", "1485", "1486"}, "MT": {"1471", "1472", "1473", "1474"},
}
LETRAS = set("ABCDE")
EASY_B, HARD_B = 0.6, 1.6
SEED = 20250624


def pf(v):
    if not v:
        return None
    try:
        return float(v.replace(",", "."))
    except ValueError:
        return None


def load_items():
    itens = defaultdict(list)
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


def area_metrics(resp, area, items, lingua):
    off = AREA_START[area]
    acertos = ef = ad = 0
    for pos, gab, b, ling in items:
        if area == "LC" and ling and ling != lingua:
            continue
        idx = pos - off
        if idx < 0 or idx >= len(resp):
            continue
        ok = resp[idx].upper() == gab and gab in LETRAS
        if ok:
            acertos += 1
        if b is not None:
            if b <= EASY_B and not ok:
                ef += 1
            elif b >= HARD_B and ok:
                ad += 1
    return acertos, min(ef, ad)


def lc_lingua_metrics(resp, items, lingua):
    """acertos no bloco de língua (5) e total LC (45)."""
    off = AREA_START["LC"]
    ac_ling = ac_tot = 0
    for pos, gab, b, ling in items:
        if ling and ling != lingua:
            continue
        idx = pos - off
        if idx < 0 or idx >= len(resp):
            continue
        if resp[idx].upper() == gab and gab in LETRAS:
            ac_tot += 1
            if pos <= off + 4:  # posições 1-5 = bloco de língua
                ac_ling += 1
    return ac_ling, ac_tot


def main():
    itens = load_items()
    rng = random.Random(SEED)

    # A) chutes
    cat_counts = defaultdict(int)
    scatter = []
    seen_scatter = 0
    SCN = 120_000

    # B) lingua
    LANG = {"0": "Inglês", "1": "Espanhol"}
    cell_notas = defaultdict(list)   # (lang, acertos_tot) -> reservoir de notas
    CELL_CAP = 4000
    cell_seen = defaultdict(int)
    casos = defaultdict(list)        # (acertos_tot, acertos_ling, lang) -> lista de notas reais
    ALVOS = {20, 25, 30, 35}
    lang_count = defaultdict(int)
    lang_nota_sum = defaultdict(float)

    def cat_of(incoer):
        if incoer >= 8:
            return "Muitas incoerências (8+)"
        if incoer >= 4:
            return "Algumas incoerências (4–7)"
        if incoer >= 1:
            return "Poucas incoerências (1–3)"
        return "Coerente (0)"

    lidas = 0
    with (DADOS / "RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            lidas += 1
            if lidas % 1_000_000 == 0:
                print(f"  {lidas:,} linhas...")
            if not all(row.get(f"TP_PRESENCA_{a}") == "1" for a in AREAS):
                continue
            codes = {a: row.get(f"CO_PROVA_{a}", "") for a in AREAS}
            if not all(codes[a] in REGULAR[a] for a in AREAS):
                continue
            notas = {a: pf(row.get(f"NU_NOTA_{a}")) for a in AREAS}
            resps = {a: row.get(f"TX_RESPOSTAS_{a}") or "" for a in AREAS}
            if any(notas[a] is None or notas[a] <= 0 or not resps[a] for a in AREAS):
                continue
            lingua = row.get("TP_LINGUA", "")

            tot_ac = 0
            incoer = 0
            okc = True
            for a in AREAS:
                its = itens.get((a, codes[a]))
                if not its:
                    okc = False
                    break
                ac, inc = area_metrics(resps[a], a, its, lingua)
                tot_ac += ac
                incoer += inc
            if not okc:
                continue
            nota_media = sum(notas[a] for a in AREAS) / 4

            # scatter reservoir + contagem categoria
            cat = cat_of(incoer)
            cat_counts[cat] += 1
            seen_scatter += 1
            rec = (tot_ac, round(nota_media, 1), incoer, cat)
            if len(scatter) < SCN:
                scatter.append(rec)
            else:
                j = rng.randrange(seen_scatter)
                if j < SCN:
                    scatter[j] = rec

            # B) lingua (LC)
            if lingua in LANG:
                its = itens.get(("LC", codes["LC"]))
                if its:
                    ac_ling, ac_tot = lc_lingua_metrics(resps["LC"], its, lingua)
                    nlc = notas["LC"]
                    lang_count[lingua] += 1
                    lang_nota_sum[lingua] += nlc
                    key = (lingua, ac_tot)
                    cell_seen[key] += 1
                    if len(cell_notas[key]) < CELL_CAP:
                        cell_notas[key].append(nlc)
                    else:
                        j = rng.randrange(cell_seen[key])
                        if j < CELL_CAP:
                            cell_notas[key][j] = nlc
                    if ac_tot in ALVOS and len(casos[(ac_tot, ac_ling, lingua)]) < 200:
                        casos[(ac_tot, ac_ling, lingua)].append(nlc)

    print(f"\nTotal linhas: {lidas:,}")

    # ---- saída chutes ----
    total = sum(cat_counts.values())
    chutes_out = {"total": total,
                  "categorias": {k: {"n": v, "pct": round(100 * v / total, 2)} for k, v in cat_counts.items()},
                  "def": f"Fácil: b<={EASY_B}; Difícil: b>={HARD_B}; incoerência por área = min(erros em fáceis, acertos em difíceis)"}
    (OUT / "chutes_counts.json").write_text(json.dumps(chutes_out, ensure_ascii=False, indent=2))
    with (OUT / "chutes_scatter.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["acertos", "nota_media", "incoer", "cat"]); w.writerows(scatter)
    print("chutes:", {k: chutes_out["categorias"][k]["pct"] for k in cat_counts})

    # ---- saída lingua curva ----
    curve = {LANG[l]: {} for l in LANG}
    for (l, ac), notas in cell_notas.items():
        if len(notas) >= 30:
            curve[LANG[l]][ac] = {"mediana": round(statistics.median(notas), 1), "n_cell": cell_seen[(l, ac)]}
    lang_media = {LANG[l]: round(lang_nota_sum[l] / lang_count[l], 1) for l in LANG}
    lang_share = {LANG[l]: round(100 * lang_count[l] / sum(lang_count.values()), 1) for l in LANG}
    (OUT / "lingua_curve.json").write_text(json.dumps(
        {"curve": {k: {str(a): v for a, v in d.items()} for k, d in curve.items()},
         "media_geral": lang_media, "share": lang_share,
         "n": {LANG[l]: lang_count[l] for l in LANG}}, ensure_ascii=False, indent=2))
    print("língua média geral:", lang_media, "| share:", lang_share)

    # ---- casos reais: pares casados por (acertos_tot, acertos_ling) ----
    pares = []
    for ac_tot in sorted(ALVOS):
        for ac_ling in range(6):
            ki = (ac_tot, ac_ling, "0"); ke = (ac_tot, ac_ling, "1")
            if casos.get(ki) and casos.get(ke) and len(casos[ki]) >= 20 and len(casos[ke]) >= 20:
                mi = statistics.median(casos[ki]); me = statistics.median(casos[ke])
                pares.append({"acertos_total": ac_tot, "acertos_lingua": ac_ling,
                              "ingles_nota": round(mi, 1), "espanhol_nota": round(me, 1),
                              "dif": round(me - mi, 1), "n_ing": len(casos[ki]), "n_esp": len(casos[ke])})
    (OUT / "lingua_casos.json").write_text(json.dumps(pares, ensure_ascii=False, indent=2))
    print(f"casos reais (pares casados): {len(pares)}")
    for p in pares:
        print(f"  {p['acertos_total']} ac ({p['acertos_lingua']}/5 língua): ing {p['ingles_nota']} vs esp {p['espanhol_nota']} (dif {p['dif']:+})")


if __name__ == "__main__":
    main()
