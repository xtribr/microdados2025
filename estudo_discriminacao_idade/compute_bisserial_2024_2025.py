#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparação 2024×2025 do poder discriminatório por área — via correlação ponto-bisserial
(item × nota da área), calculada de forma IDÊNTICA nos dois anos a partir do arquivo de
RESULTADOS (TX_RESPOSTAS/TX_GABARITO embutidos na própria linha do aluno — não depende do
ITENS_PROVA, que não está disponível para 2024 nesta máquina).

NOTA METODOLÓGICA: isto NÃO é o parâmetro A oficial do modelo 3PL (que o INEP calibra e
não publicou para 2024 nesta máquina) — é um proxy clássico e real de discriminação
(correlação ponto-bisserial acerto×nota), calculado do mesmo jeito nos dois anos para
tornar a comparação justa. Amostra: primeiras N linhas presentes com nota>0 por ano/área
(ordem do CSV não é sistemática por desempenho — não enviesa a amostra).
"""
import csv
import json
import statistics
from pathlib import Path

OUT = Path(__file__).resolve().parent
FILES = {
    2024: Path("/Volumes/HD/apps/RANKING ENEM/microdados-2024/MICRODADOS_ENEM_2024.csv"),
    2025: Path("/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv"),
}
AREAS = ["LC", "CH", "CN", "MT"]
N_AMOSTRA = 150_000
LETRAS = set("ABCDE")


def pf(v):
    try:
        return float(str(v).replace(",", ".")) if v else None
    except ValueError:
        return None


def point_biserial(bin_vec, cont_vec):
    n = len(bin_vec)
    mean_c = sum(cont_vec) / n
    mean_b = sum(bin_vec) / n
    if mean_b in (0, 1):
        return None
    cov = sum((b - mean_b) * (c - mean_c) for b, c in zip(bin_vec, cont_vec)) / n
    sd_b = (mean_b * (1 - mean_b)) ** 0.5
    sd_c = (sum((c - mean_c) ** 2 for c in cont_vec) / n) ** 0.5
    if sd_b == 0 or sd_c == 0:
        return None
    return cov / (sd_b * sd_c)


def alinha_gabarito_lc(gab, lingua):
    """TX_GABARITO_LC tem 50 chars (5 inglês + 5 espanhol + 40 comuns);
    TX_RESPOSTAS_LC tem 45 (bloco de língua já resolvido). Alinha pro idioma do aluno."""
    if len(gab) != 50:
        return gab
    bloco = gab[0:5] if lingua == "0" else gab[5:10]
    return bloco + gab[10:50]


def processa_ano(ano):
    path = FILES[ano]
    dados = {a: {"resp": [], "gab": [], "nota": []} for a in AREAS}
    n_lidas = {a: 0 for a in AREAS}
    with path.open(encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            done = True
            for a in AREAS:
                if n_lidas[a] >= N_AMOSTRA:
                    continue
                done = False
                if row.get(f"TP_PRESENCA_{a}") != "1":
                    continue
                nota = pf(row.get(f"NU_NOTA_{a}"))
                resp = row.get(f"TX_RESPOSTAS_{a}") or ""
                gab = row.get(f"TX_GABARITO_{a}") or ""
                if a == "LC" and gab:
                    lingua = (row.get("TP_LINGUA") or "").strip()
                    if lingua not in ("0", "1"):
                        continue
                    gab = alinha_gabarito_lc(gab, lingua)
                if nota is None or nota <= 0 or not resp or not gab or len(resp) != len(gab):
                    continue
                dados[a]["resp"].append(resp)
                dados[a]["gab"].append(gab)
                dados[a]["nota"].append(nota)
                n_lidas[a] += 1
            if done:
                break
    print(f"  {ano}: amostras coletadas —", {a: n_lidas[a] for a in AREAS})

    resumo = {}
    for a in AREAS:
        resp_list = dados[a]["resp"]
        gab_list = dados[a]["gab"]
        notas = dados[a]["nota"]
        n_itens = len(gab_list[0]) if gab_list else 0
        rs = []
        for pos in range(n_itens):
            gabs_pos = {g[pos] for g in gab_list[:500] if pos < len(g)}
            # ignora posições sem gabarito consistente (ex.: anulado 'X' pra todos, ou bloco de língua)
            bin_vec = []
            cont_vec = []
            for resp, gab, nota in zip(resp_list, gab_list, notas):
                if pos >= len(gab) or gab[pos] not in LETRAS:
                    continue
                bin_vec.append(1 if resp[pos] == gab[pos] else 0)
                cont_vec.append(nota)
            if len(bin_vec) < 1000:
                continue
            r = point_biserial(bin_vec, cont_vec)
            if r is not None:
                rs.append(r)
        resumo[a] = {
            "n_itens_validos": len(rs),
            "n_amostra": n_lidas[a],
            "r_media": round(statistics.mean(rs), 3) if rs else None,
            "r_mediana": round(statistics.median(rs), 3) if rs else None,
            "r_min": round(min(rs), 3) if rs else None,
            "r_max": round(max(rs), 3) if rs else None,
            "pct_r_abaixo_020": round(100 * sum(1 for r in rs if r < 0.20) / len(rs), 1) if rs else None,
            "todos_r": [round(r, 3) for r in rs],
        }
    return resumo


def main():
    out = {}
    for ano in (2024, 2025):
        print(f"processando {ano}...")
        out[ano] = processa_ano(ano)
    (OUT / "bisserial_2024_2025.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(json.dumps({a: {y: {k: v for k, v in out[y][a].items() if k != "todos_r"} for y in (2024, 2025)}
                      for a in AREAS}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
