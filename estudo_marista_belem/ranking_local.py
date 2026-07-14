#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ranking LOCAL do Marista Nazaré (Belém/PA) — método do estudo Teresa:
média por CO_ESCOLA dos alunos presentes nos 2 dias com as 5 notas válidas,
corte N>=10, recortes Belém / Belém privadas / PA / PA privadas, por área.
Nomes das escolas: Censo Escolar 2025 (CO_ENTIDADE = CO_ESCOLA).
Fonte: Microdados ENEM 2025 e Censo Escolar 2025 / INEP. Nenhum dado inventado.
"""
import json
import zipfile
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent
BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
RESULTADOS = BASE / "DADOS/RESULTADOS_2025.csv"
CENSO_ZIP = BASE / "analises_primi_2025_cop30/cache/microdados_censo_escolar_2025.zip"
CENSO_INNER = "microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv"
CO_ESCOLA = 15038424
NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
AREAS = {"CN": "NU_NOTA_CN", "CH": "NU_NOTA_CH", "LC": "NU_NOTA_LC",
         "MT": "NU_NOTA_MT", "REDACAO": "NU_NOTA_REDACAO"}
MIN_N = 10


def agrega_pa() -> pd.DataFrame:
    usecols = ["CO_ESCOLA", "CO_MUNICIPIO_ESC", "NO_MUNICIPIO_ESC", "SG_UF_ESC",
               "TP_DEPENDENCIA_ADM_ESC"] + NOTAS
    partes = []
    for chunk in pd.read_csv(RESULTADOS, sep=";", encoding="latin-1",
                             usecols=usecols, chunksize=400_000):
        chunk = chunk[chunk["SG_UF_ESC"] == "PA"].dropna(subset=["CO_ESCOLA"] + NOTAS)
        if len(chunk):
            partes.append(chunk)
    df = pd.concat(partes, ignore_index=True)
    df["CO_ESCOLA"] = df["CO_ESCOLA"].astype("int64")
    agg = df.groupby("CO_ESCOLA").agg(
        N_ALUNOS=("NU_NOTA_CN", "size"),
        CN=("NU_NOTA_CN", "mean"), CH=("NU_NOTA_CH", "mean"),
        LC=("NU_NOTA_LC", "mean"), MT=("NU_NOTA_MT", "mean"),
        REDACAO=("NU_NOTA_REDACAO", "mean"),
        NO_MUNICIPIO=("NO_MUNICIPIO_ESC", "first"),
        CO_MUNICIPIO=("CO_MUNICIPIO_ESC", "first"),
        DEP=("TP_DEPENDENCIA_ADM_ESC", "first"),
    ).reset_index()
    agg["MEDIA_5"] = agg[["CN", "CH", "LC", "MT", "REDACAO"]].mean(axis=1)
    for c in ["CN", "CH", "LC", "MT", "REDACAO", "MEDIA_5"]:
        agg[c] = agg[c].round(1)
    return agg[agg["N_ALUNOS"] >= MIN_N].copy()


def nomes_censo(codigos: set) -> dict:
    nomes = {}
    with zipfile.ZipFile(CENSO_ZIP) as zf, zf.open(CENSO_INNER) as fp:
        for chunk in pd.read_csv(fp, sep=";", encoding="latin1",
                                 usecols=["CO_ENTIDADE", "NO_ENTIDADE"],
                                 chunksize=200_000):
            sub = chunk[chunk["CO_ENTIDADE"].isin(codigos)]
            nomes.update(dict(zip(sub["CO_ENTIDADE"], sub["NO_ENTIDADE"])))
    return nomes


def main():
    agg = agrega_pa()
    print(f"Escolas do PA com N>={MIN_N}: {len(agg)}")
    nomes = nomes_censo(set(agg["CO_ESCOLA"]))
    agg["NO_ENTIDADE"] = agg["CO_ESCOLA"].map(nomes).fillna("(sem nome no Censo)")

    recortes = {
        "belem": agg[agg["CO_MUNICIPIO"] == 1501402],
        "belem_privadas": agg[(agg["CO_MUNICIPIO"] == 1501402) & (agg["DEP"] == 4)],
        "pa": agg,
        "pa_privadas": agg[agg["DEP"] == 4],
    }
    metricas = ["MEDIA_5"] + list(AREAS)
    resumo = {"escola": "Marista Nazaré (Belém/PA)", "co_escola": CO_ESCOLA,
              "criterio": f"média dos presentes nos 2 dias com 5 notas, N>={MIN_N}",
              "recortes": {}}
    for nome_rec, df in recortes.items():
        total = len(df)
        pos = {}
        for m in metricas:
            rk = df.sort_values(m, ascending=False).reset_index(drop=True)
            rk.insert(0, "POSICAO", rk.index + 1)
            if nome_rec in ("belem", "pa"):  # grava CSV completo dos 2 recortes-base
                if m == "MEDIA_5":
                    cols = ["POSICAO", "NO_ENTIDADE", "NO_MUNICIPIO", "DEP", "N_ALUNOS",
                            "MEDIA_5", "CN", "CH", "LC", "MT", "REDACAO", "CO_ESCOLA"]
                    rk[cols].to_csv(D / f"ranking_{nome_rec}_media5.csv", index=False)
            linha = rk[rk["CO_ESCOLA"] == CO_ESCOLA]
            pos[m] = None if linha.empty else int(linha["POSICAO"].iloc[0])
        resumo["recortes"][nome_rec] = {"total_escolas": total, "posicao": pos}
        print(f"\n== {nome_rec} ({total} escolas) ==")
        print("  " + " · ".join(f"{m}: {pos[m]}º/{total}" for m in metricas))

    # top-10 de Belém por média5 (contexto do print)
    top = recortes["belem"].sort_values("MEDIA_5", ascending=False).head(10)
    print("\nTop-10 Belém (média 5):")
    for i, r in enumerate(top.itertuples(), 1):
        marca = " <== MARISTA" if r.CO_ESCOLA == CO_ESCOLA else ""
        print(f"  {i:2}. {r.NO_ENTIDADE[:52]:52} {r.MEDIA_5:6.1f} (N={r.N_ALUNOS}){marca}")

    (D / "resumo_ranking_local.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2))
    print("\nOK: resumo_ranking_local.json + ranking_belem_media5.csv + ranking_pa_media5.csv")


if __name__ == "__main__":
    main()
