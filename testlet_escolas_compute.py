#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taxa de erro NO TESTLET de Linguagens (Q6–Q10 do caderno AZUL P1 — um texto, 5 questões)
para as escolas estudadas. Os 5 itens são identificados por CO_ITEM e localizados no
caderno (cor) de cada aluno — funciona para qualquer cor do P1 regular.
Referência Brasil: % de acerto ponderada por respondentes, todas as cores (itens_sequencia).
Grava testlet.csv em cada pasta de estudo.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
LC_OFF = 1

FOLDERS = [
    (BASE / "estudo_cei_natal", "alunos_cei.csv",
     {"24069191": "CEI Romualdo", "24089214": "CEI Roberto Freire"}),
    (BASE / "estudo_marista_natal", "alunos.csv", None),   # None => nome do config.json
    (BASE / "estudo_dombosco_saoluis", "alunos.csv", None),
]


def testlet_items():
    """CO_ITEMs das posições 6-10 do LC AZUL (1459) + posição/gabarito em TODAS as provas LC."""
    azul = {}       # co_item -> (pos_azul, hab)
    posmap = defaultdict(dict)  # co_prova -> {co_item: (pos, gab)}
    rows = []
    with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["SG_AREA"].strip() != "LC" or r["IN_ITEM_ABAN"] == "1":
                continue
            rows.append(r)
            if r["CO_PROVA"].strip() == "1459":
                pos = int(r["CO_POSICAO"])
                if 6 <= pos <= 10:
                    azul[r["CO_ITEM"].strip()] = (pos, f"H{int(r['CO_HABILIDADE'])}")
    for r in rows:
        ci = r["CO_ITEM"].strip()
        if ci in azul:
            posmap[r["CO_PROVA"].strip()][ci] = (int(r["CO_POSICAO"]),
                                                 (r["TX_GABARITO"] or "").strip().upper())
    return azul, posmap


def nacional(azul):
    acc = defaultdict(lambda: [0.0, 0.0])
    with (BASE / "analises_primi_2025_cop30/outputs/itens_sequencia_dificuldade_2025.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ci = str(r["co_item"]).split(".")[0].strip()
            if ci in azul:
                try:
                    acc[ci][0] += float(r["pct_acerto"]) * float(r["total"])
                    acc[ci][1] += float(r["total"])
                except ValueError:
                    continue
    return {ci: round(100 - v[0] / v[1], 1) for ci, v in acc.items() if v[1] > 0}


def main():
    azul, posmap = testlet_items()
    nac = nacional(azul)
    print("testlet co_items:", {ci: azul[ci] for ci in azul})
    for folder, fname, names in FOLDERS:
        if names is None:
            cfg = json.loads((folder / "config.json").read_text())
            names = {cfg["co_escola"]: cfg["curto"]}
        err = defaultdict(lambda: [0, 0])   # (escola, co_item) -> [erros, tot]
        skipped = 0
        with (folder / fname).open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                esc = names.get((row["CO_ESCOLA"] or "").strip())
                if not esc or row.get("TP_PRESENCA_LC") != "1":
                    continue
                prova = (row.get("CO_PROVA_LC") or "").strip()
                resp = row.get("TX_RESPOSTAS_LC") or ""
                pm = posmap.get(prova)
                if not pm or len(pm) < 5 or not resp:
                    skipped += 1
                    continue
                for ci, (pos, gab) in pm.items():
                    idx = pos - LC_OFF
                    if 0 <= idx < len(resp) and gab in set("ABCDE"):
                        k = (esc, ci)
                        err[k][1] += 1
                        err[k][0] += (resp[idx].upper() != gab)
        out = folder / "testlet.csv"
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["escola", "q_azul", "habilidade", "erro_pct", "n", "erro_nacional"])
            for (esc, ci), (e, t) in sorted(err.items(), key=lambda kv: (kv[0][0], azul[kv[0][1]][0])):
                pos, hab = azul[ci]
                w.writerow([esc, f"Q{pos:02d}", hab, round(100 * e / t, 1), t, nac[ci]])
        print(f"{folder.name}: ok ({sum(t for _, t in err.values())//5} alunos no testlet, {skipped} fora do P1/sem resposta)")


if __name__ == "__main__":
    main()
