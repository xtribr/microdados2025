#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serie completa 2010-2025 (16 anos, TODOS presentes -- 2018 recuperado direto do
zip oficial do INEP, ja que a copia no Supabase estava corrompida) de dificuldade
TRI media por area, + regressao linear (OLS) e previsao 2026 com IC 95%.
Mesma metodologia em toda a serie: caderno Azul regular (P1, nao-reaplicacao),
itens nao anulados, |b|<=6.

2018: ITENS_PROVA_2018.csv baixado via HTTP Range request diretamente do zip
oficial (https://download.inep.gov.br/microdados/microdados_enem_2018.zip,
extraido so o membro DADOS/ITENS_PROVA_2018.csv, ~15KB comprimidos, CRC32
conferido byte a byte contra o header do zip -- integridade confirmada).
Grupo Azul-Regular (P1) identificado cruzando TX_COR='Azul' com o conjunto de
CO_PROVA que tambem contem Laranja/Verde (ledor/libras, exclusivos do P1 -- o
P2/reaplicacao de 2018 nao tem essas variantes de acessibilidade), o que ancora
sem ambiguidade a faixa de codigos 447-470 = P1: {LC:455, CH:451, CN:447, MT:459}.
"""
import csv, math
import numpy as np

BASE = "/sessions/kind-gracious-heisenberg/mnt/microdados_enem_2025"
OUT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026"

CO_PROVA_AZUL = {"LC": 1459, "CH": 1447, "CN": 1483, "MT": 1471}
CO_PROVA_AZUL_2018 = {"CN": "447", "CH": "451", "LC": "455", "MT": "459"}


def fnum(s):
    s = (s or "").strip().replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None


# ---------- 2025: recomputar da fonte real ja verificada nesta sessao ----------
rows2025 = []
with open(f"{BASE}/DADOS/ITENS_PROVA_2025.csv", encoding="latin-1") as f:
    r = csv.DictReader(f, delimiter=";")
    for row in r:
        area = row["SG_AREA"]
        if area not in CO_PROVA_AZUL:
            continue
        if int(row["CO_PROVA"]) != CO_PROVA_AZUL[area]:
            continue
        if row["IN_ITEM_ABAN"] == "1":
            continue
        b = fnum(row["NU_PARAM_B"]); a = fnum(row["NU_PARAM_A"])
        if b is None:
            continue
        if not (-6 <= b <= 6):
            continue
        rows2025.append((area, b, a))

serie2025 = {}
for area in CO_PROVA_AZUL:
    bs = [b for a2, b, a in rows2025 if a2 == area]
    as_ = [a for a2, b, a in rows2025 if a2 == area]
    serie2025[area] = {
        "n": len(bs),
        "b_medio": float(np.mean(bs)),
        "b_mediana": float(np.median(bs)),
        "b_dp": float(np.std(bs, ddof=1)),
        "a_medio": float(np.mean(as_)),
    }
    print(f"2025 {area}: n={len(bs)} b_medio={np.mean(bs):.4f} b_mediana={np.median(bs):.4f}")

# ---------- 2018: recomputar do arquivo oficial baixado direto do INEP ----------
rows2018 = []
with open(f"{OUT}/ITENS_PROVA_2018.csv", encoding="latin-1") as f:
    r = csv.DictReader(f, delimiter=";")
    for row in r:
        area = row["SG_AREA"]
        if area not in CO_PROVA_AZUL_2018:
            continue
        if row["CO_PROVA"] != CO_PROVA_AZUL_2018[area]:
            continue
        if row["IN_ITEM_ABAN"] == "1":
            continue
        b = fnum(row["NU_PARAM_B"]); a = fnum(row["NU_PARAM_A"])
        if b is None:
            continue
        if not (-6 <= b <= 6):
            continue
        rows2018.append((area, b, a))

serie2018 = {}
for area in CO_PROVA_AZUL_2018:
    bs = [b for a2, b, a in rows2018 if a2 == area]
    serie2018[area] = float(np.mean(bs))
    print(f"2018 {area}: n={len(bs)} b_medio={np.mean(bs):.4f} (recuperado do INEP oficial)")

# ---------- carregar serie 2010-2024 (Supabase, ja limpa, 2018 nao entra daqui) ----------
hist = {}  # (ano,area) -> b_medio
with open(f"{OUT}/serie_dificuldade_supabase_2010_2024.csv", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        hist[(int(row["ano"]), row["area"])] = float(row["b_medio"])

# ---------- montar serie completa por area (16 anos, 2010-2025, TODOS presentes) ----------
AREAS = ["LC", "CH", "CN", "MT"]
full_series = {a: [] for a in AREAS}
for ano in range(2010, 2026):
    for area in AREAS:
        if ano == 2025:
            val = serie2025[area]["b_medio"]
        elif ano == 2018:
            val = serie2018[area]
        else:
            val = hist.get((ano, area))
        if val is not None:
            full_series[area].append((ano, val))


# ---------- regressao linear OLS + previsao 2026 com IC 95% ----------
def ols_forecast(xs, ys, x_pred):
    xs = np.array(xs, dtype=float); ys = np.array(ys, dtype=float)
    n = len(xs)
    xbar = xs.mean(); ybar = ys.mean()
    sxx = np.sum((xs - xbar) ** 2)
    sxy = np.sum((xs - xbar) * (ys - ybar))
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    y_hat = intercept + slope * xs
    resid = ys - y_hat
    dof = n - 2
    s2 = np.sum(resid ** 2) / dof
    se_pred = math.sqrt(s2 * (1 + 1 / n + (x_pred - xbar) ** 2 / sxx))
    y_pred = intercept + slope * x_pred
    t_table = {10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086}
    tcrit = t_table.get(dof, 2.10)
    ic_low = y_pred - tcrit * se_pred
    ic_high = y_pred + tcrit * se_pred
    ss_tot = np.sum((ys - ybar) ** 2)
    ss_res = np.sum(resid ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return dict(slope=slope, intercept=intercept, y_pred=y_pred, ic_low=ic_low, ic_high=ic_high,
                r2=r2, n=n, dof=dof, se_pred=se_pred, tcrit=tcrit)


print("\n=== SERIE COMPLETA (16 ANOS, 2018 RECUPERADO) E PREVISAO 2026 (OLS, IC 95%) ===")
resultados = {}
for area in AREAS:
    pts = sorted(full_series[area])
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    res = ols_forecast(xs, ys, 2026)
    resultados[area] = res
    dif_2025 = ys[-1]
    print(f"\n{area}: n_anos={res['n']} (2010-2025, completo) | slope={res['slope']:.5f}/ano | R2={res['r2']:.3f}")
    print(f"  b medio 2025 (observado) = {dif_2025:.4f}  ->  dificuldade TRI 2025 = {dif_2025*100+500:.1f}")
    print(f"  b previsto 2026 = {res['y_pred']:.4f} (IC95%: {res['ic_low']:.4f} a {res['ic_high']:.4f})")
    print(f"  dificuldade TRI prevista 2026 = {res['y_pred']*100+500:.1f} (IC95%: {res['ic_low']*100+500:.1f} a {res['ic_high']*100+500:.1f})")

import json
out = {"serie_completa": {a: sorted(full_series[a]) for a in AREAS},
       "previsao_2026": {a: {k: (v if not isinstance(v, (np.floating,)) else float(v)) for k, v in resultados[a].items()} for a in AREAS},
       "serie2025_detalhe": serie2025,
       "serie2018_detalhe": serie2018}
with open(f"{OUT}/dados_previsao_2026.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2, default=float)
print("\nSalvo:", f"{OUT}/dados_previsao_2026.json")
