#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estudo: mapa de distratores do ENEM 2025 — qual alternativa ERRADA mais engana em cada item.
Caderno Azul regular (mesmos CO_PROVA usados em todo o acervo XTRI: CH 1447 · CN 1483 · LC 1459 · MT 1471).
Full streaming sobre RESULTADOS_2025.csv (4,81 mi linhas) — nada de amostra, cálculo exato.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
OUT = Path(__file__).resolve().parent
AREAS = ["LC", "CH", "CN", "MT"]
CO_PROVA_AZUL = {"LC": 1459, "CH": 1447, "CN": 1483, "MT": 1471}
# CO_POSICAO no ITENS_PROVA e absoluto no dia (LC 1-45, CH 46-90, CN 91-135, MT 136-180);
# TX_RESPOSTAS_{AREA} e local a area (indice 0 = 1a questao daquela area) -> precisa somar o offset.
OFFSET_POSICAO = {"LC": 0, "CH": 45, "CN": 90, "MT": 135}
LETRAS = ["A", "B", "C", "D", "E"]
NOMES_AREA = {"LC": "Linguagens", "CH": "Ciências Humanas", "CN": "Ciências da Natureza", "MT": "Matemática"}

# ---- 1) metadados do item (gabarito, habilidade, a/b/c) a partir de ITENS_PROVA_2025.csv ----
# chave: (area, posicao) para CH/CN/MT e posicoes 6-45 de LC; (area, posicao, tp_lingua) para LC 1-5.
meta = {}
with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        area = row["SG_AREA"]
        if area not in AREAS:
            continue
        if int(row["CO_PROVA"]) != CO_PROVA_AZUL[area]:
            continue
        if row.get("IN_ITEM_ABAN") == "1":
            continue  # exclui os 5 itens anulados (CN 3, MT 2) automaticamente
        pos = int(row["CO_POSICAO"])
        info = {
            "co_item": row["CO_ITEM"],
            "gabarito": row["TX_GABARITO"],
            "habilidade": row["CO_HABILIDADE"],
            "a": float(row["NU_PARAM_A"]), "b": float(row["NU_PARAM_B"]), "c": float(row["NU_PARAM_C"]),
        }
        if area == "LC" and pos <= 5:
            lingua = row.get("TP_LINGUA") or ""
            meta[(area, pos, lingua)] = info
        else:
            meta[(area, pos)] = info

n_itens = sum(1 for k in meta if not (isinstance(k, tuple) and len(k) == 3))
print(f"metadados carregados: {len(meta)} entradas (LC pos1-5 tem 2 cada por lingua)")

# ---- 2) tally de letras por posicao, full streaming (1 unica passada) ----
tally = {area: defaultdict(lambda: defaultdict(int)) for area in AREAS}  # tally[area][pos][letra] = n
tally_lc15 = {"0": defaultdict(lambda: defaultdict(int)), "1": defaultdict(lambda: defaultdict(int))}
n_presentes = {area: 0 for area in AREAS}

with (BASE / "DADOS/RESULTADOS_2025.csv").open(encoding="latin-1", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    for i, row in enumerate(reader):
        for area in AREAS:
            if row.get(f"TP_PRESENCA_{area}") != "1":
                continue
            cop = row.get(f"CO_PROVA_{area}")
            if not cop or int(cop) != CO_PROVA_AZUL[area]:
                continue
            resp = row.get(f"TX_RESPOSTAS_{area}") or ""
            if len(resp) != 45:
                continue
            n_presentes[area] += 1
            for idx in range(45):
                pos = idx + 1
                letra = resp[idx]
                if letra not in LETRAS:
                    continue
                tally[area][pos][letra] += 1
            if area == "LC":
                lingua = row.get("TP_LINGUA") or ""
                if lingua in ("0", "1"):
                    for pos in range(1, 6):
                        letra = resp[pos - 1]
                        if letra in LETRAS:
                            tally_lc15[lingua][pos][letra] += 1
        if (i + 1) % 1_000_000 == 0:
            print(f"  ... {i+1:,} linhas lidas")

print("presentes por area (Azul):", n_presentes)

# ---- 3) resumo por item: campeao de distrator, lift vs 25% uniforme ----
try:
    habs = json.loads((BASE / "analises_primi_2025_cop30/outputs/habilidades_desc.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    habs = {}

linhas = []
for area in AREAS:
    for pos in range(1, 46):
        if area == "LC" and pos <= 5:
            # duas versões (ingles/espanhol) -- soma nao se aplica; tratar cada lingua separadamente
            for lingua, rotulo in (("0", "Inglês"), ("1", "Espanhol")):
                info = meta.get((area, pos, lingua))
                if not info:
                    continue
                # tally já está agregado por posição sem separar língua -- refeito abaixo em bloco especial
                pass
            continue
        abs_pos = OFFSET_POSICAO[area] + pos
        info = meta.get((area, abs_pos))
        if not info:
            continue
        counts = tally[area][pos]
        n_valid = sum(counts.values())
        if n_valid < 1000:
            continue
        gab = info["gabarito"]
        certo = counts.get(gab, 0)
        errados = {l: counts.get(l, 0) for l in LETRAS if l != gab}
        n_errados = sum(errados.values())
        if n_errados < 100:
            continue
        campeao, n_campeao = max(errados.items(), key=lambda kv: kv[1])
        pct_acerto = 100 * certo / n_valid
        pct_campeao_errados = 100 * n_campeao / n_errados
        pct_campeao_base = 100 * n_campeao / n_valid
        lift = pct_campeao_errados / 25.0
        hab_key = f"{area}H{info['habilidade']}"
        linhas.append({
            "area": area, "posicao": pos, "co_posicao_abs": abs_pos, "co_item": info["co_item"],
            "habilidade_cod": hab_key, "habilidade_desc": habs.get(hab_key, ""),
            "gabarito": gab, "n_valido": n_valid, "pct_acerto": round(pct_acerto, 1),
            "distrator_campeao": campeao, "pct_campeao_entre_errados": round(pct_campeao_errados, 1),
            "pct_campeao_da_base": round(pct_campeao_base, 1), "lift_vs_uniforme": round(lift, 2),
            "param_a": info["a"], "param_b": info["b"], "param_c": info["c"],
            "dif_tri": round(info["b"] * 100 + 500, 1),
        })

# bloco especial LC posicoes 1-5 (por lingua) -- tally_lc15 já preenchido na passada única acima
for lingua, rotulo in (("0", "Inglês"), ("1", "Espanhol")):
    for pos in range(1, 6):
        info = meta.get(("LC", pos, lingua))
        if not info:
            continue
        counts = tally_lc15[lingua][pos]
        n_valid = sum(counts.values())
        if n_valid < 1000:
            continue
        gab = info["gabarito"]
        certo = counts.get(gab, 0)
        errados = {l: counts.get(l, 0) for l in LETRAS if l != gab}
        n_errados = sum(errados.values())
        if n_errados < 100:
            continue
        campeao, n_campeao = max(errados.items(), key=lambda kv: kv[1])
        pct_acerto = 100 * certo / n_valid
        pct_campeao_errados = 100 * n_campeao / n_errados
        pct_campeao_base = 100 * n_campeao / n_valid
        lift = pct_campeao_errados / 25.0
        hab_key = f"LCH{info['habilidade']}"
        linhas.append({
            "area": "LC", "posicao": pos, "co_posicao_abs": pos, "co_item": info["co_item"],
            "habilidade_cod": hab_key, "habilidade_desc": habs.get(hab_key, ""),
            "gabarito": gab, "n_valido": n_valid, "pct_acerto": round(pct_acerto, 1),
            "distrator_campeao": campeao, "pct_campeao_entre_errados": round(pct_campeao_errados, 1),
            "pct_campeao_da_base": round(pct_campeao_base, 1), "lift_vs_uniforme": round(lift, 2),
            "param_a": info["a"], "param_b": info["b"], "param_c": info["c"],
            "dif_tri": round(info["b"] * 100 + 500, 1),
            "lingua": rotulo,
        })

linhas.sort(key=lambda x: (x["area"], x["posicao"]))
with (OUT / "distratores_itens.csv").open("w", newline="", encoding="utf-8") as f:
    cols = ["area", "posicao", "co_posicao_abs", "co_item", "habilidade_cod", "habilidade_desc", "gabarito",
            "n_valido", "pct_acerto", "distrator_campeao", "pct_campeao_entre_errados", "pct_campeao_da_base",
            "lift_vs_uniforme", "param_a", "param_b", "param_c", "dif_tri", "lingua"]
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for l in linhas:
        w.writerow({c: l.get(c, "") for c in cols})

print(f"\n{len(linhas)} itens processados -> distratores_itens.csv")

# ---- 4) resumo: top 12 pegadinhas campeãs (maior lift), por área ----
top_geral = sorted(linhas, key=lambda x: -x["lift_vs_uniforme"])[:15]
por_area = {}
for area in AREAS:
    itens_area = [l for l in linhas if l["area"] == area]
    if not itens_area:
        print(f"AVISO: nenhum item processado para {area} -- checar offset/meta")
        continue
    itens_area.sort(key=lambda x: -x["lift_vs_uniforme"])
    por_area[area] = {
        "n_itens": len(itens_area),
        "lift_medio": round(sum(x["lift_vs_uniforme"] for x in itens_area) / len(itens_area), 2),
        "top3": itens_area[:3],
    }

resumo = {
    "n_presentes_azul": n_presentes,
    "top_geral_15": top_geral,
    "por_area": por_area,
}
(OUT / "distratores_resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))
print("distratores_resumo.json gravado")
print("\nTOP 5 GERAL (maior lift vs uniforme 25%):")
for l in top_geral[:5]:
    print(f"  {l['area']} pos{l['posicao']:2d} | gab {l['gabarito']} -> distrator {l['distrator_campeao']} "
          f"| {l['pct_campeao_entre_errados']}% dos que erraram | lift {l['lift_vs_uniforme']}x | "
          f"hab {l['habilidade_cod']} | acerto {l['pct_acerto']}%")
