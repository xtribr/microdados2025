#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estudo: poder discriminatório (parâmetro A) por área × perfil etário dos candidatos.

LIMITE ESTRUTURAL DOCUMENTADO (verificado, não suposto):
- RESULTADOS_2025.csv usa NU_SEQUENCIAL; PARTICIPANTES_2025.csv usa NU_INSCRICAO — chaves
  DIFERENTES, sem correspondência. Não é possível cruzar idade individual com resposta a item.
- Regular P1 e COP30/BAM (aplicação especial em Belém/Ananindeua/Marituba) usam bancos de
  itens DIFERENTES — 0 co_item em comum (verificado). Não dá para comparar o MESMO item
  entre as duas populações.
- 2024: parâmetros oficiais de item (ITENS_PROVA_2024.csv) indisponíveis nesta máquina —
  arquivo em container iCloud cujo app de origem foi desinstalado (sync bloqueado,
  "Operation timed out" em toda tentativa de leitura). Comparação 2024×2025 fica PENDENTE.

O que este script computa (100% real, sem estimativa):
1. Distribuição etária 2025 (TP_FAIXA_ETARIA), Brasil inteiro — questionário 100% preenchido.
2. Mesma distribuição, comparando município da prova em {Belém, Ananindeua, Marituba}
   (COP30/BAM, população comprovadamente mais velha) vs resto do Brasil (Regular).
3. Parâmetro A por área, banco Regular P1 (2025): média, mediana, faixas de Baker, extremos.
4. Parâmetro A por área, banco COP30/BAM (2025): idem — para comparar o NÍVEL de discriminação
   dos dois bancos de itens (não item a item, pois não há itens em comum).
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
OUT = Path(__file__).resolve().parent
AREAS = ["LC", "CH", "CN", "MT"]
NOMES = {"LC": "Linguagens", "CH": "Ciências Humanas", "CN": "Ciências da Natureza", "MT": "Matemática"}

REGULAR = {
    "LC": {"1459", "1460", "1461", "1462"}, "CH": {"1447", "1448", "1449", "1450"},
    "CN": {"1483", "1484", "1485", "1486"}, "MT": {"1471", "1472", "1473", "1474"},
}
# BAM2 = COP30/BAM (verificado em memória: prova-code family, inclui cadernos de acessibilidade)
BAM = {
    "LC": {"1595", "1596", "1597", "1598", "1599", "1632"},
    "CH": {"1583", "1584", "1585", "1586", "1587", "1631"},
    "CN": {"1619", "1620", "1621", "1622", "1623", "1634"},
    "MT": {"1607", "1608", "1609", "1610", "1611", "1633"},
}
BAM_MUNICIPIOS = {"1501402", "1500800", "1504422"}  # Belém, Ananindeua, Marituba

LABELS_FAIXA = {
    1: "<17", 2: "17", 3: "18", 4: "19", 5: "20", 6: "21", 7: "22", 8: "23", 9: "24", 10: "25",
    11: "26-30", 12: "31-35", 13: "36-40", 14: "41-45", 15: "46-50", 16: "51-55", 17: "56-60",
    18: "61-65", 19: "66-70", 20: "70+",
}


def baker(a):
    if a < 0.35:
        return "muito baixa"
    if a < 0.65:
        return "baixa"
    if a < 1.35:
        return "moderada"
    if a < 1.70:
        return "alta"
    return "muito alta"


def parte1_demografia():
    """Distribuição etária 2025 — geral e COP30/BAM vs Regular."""
    geral = defaultdict(int)
    cop = defaultdict(int)
    reg = defaultdict(int)
    treineiro_por_faixa = defaultdict(int)
    concluiu_por_faixa_70mais = defaultdict(int)  # TP_ST_CONCLUSAO nas faixas 46+
    n = 0
    with (BASE / "DADOS/PARTICIPANTES_2025.csv").open(encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            n += 1
            fe = int(row["TP_FAIXA_ETARIA"])
            geral[fe] += 1
            mun = (row.get("CO_MUNICIPIO_PROVA") or "").strip()
            if mun in BAM_MUNICIPIOS:
                cop[fe] += 1
            else:
                reg[fe] += 1
            if row.get("IN_TREINEIRO") == "1":
                treineiro_por_faixa[fe] += 1
            if fe >= 15:
                concluiu_por_faixa_70mais[(fe, row.get("TP_ST_CONCLUSAO"))] += 1

    tot_cop = sum(cop.values())
    tot_reg = sum(reg.values())
    out = {
        "total_participantes": n,
        "geral_por_faixa": {LABELS_FAIXA[k]: v for k, v in sorted(geral.items())},
        "cop30_por_faixa_pct": {LABELS_FAIXA[k]: round(100 * cop.get(k, 0) / tot_cop, 2) for k in range(1, 21)},
        "regular_por_faixa_pct": {LABELS_FAIXA[k]: round(100 * reg.get(k, 0) / tot_reg, 2) for k in range(1, 21)},
        "n_cop30": tot_cop, "n_regular": tot_reg,
        "pct_26mais_cop30": round(100 * sum(v for k, v in cop.items() if k >= 11) / tot_cop, 1),
        "pct_26mais_regular": round(100 * sum(v for k, v in reg.items() if k >= 11) / tot_reg, 1),
        "n_70mais": geral.get(20, 0),
        "n_66_70": geral.get(19, 0),
        "treineiros_70mais": treineiro_por_faixa.get(20, 0),
        "concluiu_status_46mais": {str(k): v for k, v in concluiu_por_faixa_70mais.items()},
    }
    (OUT / "demografia_2025.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print("demografia: total", n, "| 70+:", out["n_70mais"], "| COP30 26+:", out["pct_26mais_cop30"],
          "% vs Regular:", out["pct_26mais_regular"], "%")
    return out


def parte2_discriminacao():
    """Parâmetro A por área: banco Regular P1 (2025). NOTA: verificado que o banco
    COP30/BAM (codes 1595-1599+1632 etc., confirmados via RESULTADOS) NÃO tem
    parâmetros A/B/C publicados no ITENS_PROVA_2025.csv — só o banco Regular é
    documentado publicamente. Por isso não há comparação de nível agregado
    Regular×BAM aqui (ficaria inventando números que o INEP não libera)."""
    itens = defaultdict(list)  # area -> [(A,B,C,co_item)]
    seen = set()
    with (BASE / "DADOS/ITENS_PROVA_2025.csv").open(encoding="latin-1", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["IN_ITEM_ABAN"] == "1":
                continue
            area = r["SG_AREA"].strip()
            if area not in AREAS:
                continue
            cp = r["CO_PROVA"].strip()
            ci = r["CO_ITEM"].strip()
            if cp not in REGULAR[area]:
                continue
            key = (area, ci)
            if key in seen:
                continue
            seen.add(key)
            try:
                a = float(r["NU_PARAM_A"]); b = float(r["NU_PARAM_B"]); c = float(r["NU_PARAM_C"])
            except ValueError:
                continue
            itens[area].append((a, b, c, ci))

    resumo = {}
    for area in AREAS:
        vals = itens.get(area, [])
        as_ = [v[0] for v in vals]
        bakers = defaultdict(int)
        for a in as_:
            bakers[baker(a)] += 1
        resumo[area] = {
            "n_itens": len(vals),
            "A_media": round(statistics.mean(as_), 3),
            "A_mediana": round(statistics.median(as_), 3),
            "A_dp": round(statistics.pstdev(as_), 3),
            "A_min": round(min(as_), 3), "A_max": round(max(as_), 3),
            "pct_muito_alta": round(100 * bakers["muito alta"] / len(as_), 1),
            "pct_alta_ou_mais": round(100 * (bakers["muito alta"] + bakers["alta"]) / len(as_), 1),
            "pct_moderada_ou_menos": round(100 * (len(as_) - bakers["muito alta"] - bakers["alta"]) / len(as_), 1),
            "n_navalha_A3mais": sum(1 for a in as_ if a >= 3.0),
            "dist_baker": {k: bakers[k] for k in ("muito baixa", "baixa", "moderada", "alta", "muito alta")},
        }
    (OUT / "discriminacao_areas.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))

    with (OUT / "discriminacao_itens.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["area", "co_item", "A", "B", "C", "baker"])
        for area, vals in itens.items():
            for a, b, c, ci in vals:
                w.writerow([area, ci, a, b, c, baker(a)])

    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    return resumo


if __name__ == "__main__":
    parte1_demografia()
    print()
    parte2_discriminacao()
