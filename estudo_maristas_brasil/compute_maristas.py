#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ranking de todos os colégios MARISTA do Brasil no ENEM 2025.

1) Censo Escolar 2025 (Tabela_Escola_2025.csv): escolas com "MARISTA" no nome.
2) RESULTADOS_2025.csv: alunos dessas escolas com as 5 notas presentes.
3) Ranking pela média das 5 notas (CN, CH, LC, MT, Redação) por escola.

Fonte: Microdados ENEM 2025 e Censo Escolar 2025 / INEP. Nenhum dado inventado.
"""
import zipfile
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CENSO_ZIP = BASE / "analises_primi_2025_cop30/cache/microdados_censo_escolar_2025.zip"
CENSO_INNER = "microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv"
RESULTADOS = BASE / "DADOS/RESULTADOS_2025.csv"
OUT = Path(__file__).resolve().parent

CO_MARISTA_NATAL = 24057134

NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]


def censo_maristas() -> pd.DataFrame:
    usecols = ["NO_ENTIDADE", "CO_ENTIDADE", "SG_UF", "NO_MUNICIPIO",
               "TP_DEPENDENCIA", "IN_COMUM_MEDIO_MEDIO"]
    frames = []
    with zipfile.ZipFile(CENSO_ZIP) as zf, zf.open(CENSO_INNER) as fp:
        for chunk in pd.read_csv(fp, sep=";", encoding="latin1",
                                 usecols=usecols, chunksize=100_000):
            sub = chunk[chunk["NO_ENTIDADE"].str.contains("MARISTA", case=False, na=False)]
            if not sub.empty:
                frames.append(sub.copy())
    df = pd.concat(frames, ignore_index=True)
    df["CO_ENTIDADE"] = df["CO_ENTIDADE"].astype("int64")
    return df


def enem_por_escola(codigos: set) -> pd.DataFrame:
    usecols = ["CO_ESCOLA"] + NOTAS
    frames = []
    for chunk in pd.read_csv(RESULTADOS, sep=";", encoding="latin-1",
                             usecols=usecols, chunksize=200_000):
        chunk = chunk.dropna(subset=["CO_ESCOLA"])
        chunk["CO_ESCOLA"] = chunk["CO_ESCOLA"].astype("int64")
        sub = chunk[chunk["CO_ESCOLA"].isin(codigos)]
        if not sub.empty:
            frames.append(sub.copy())
    df = pd.concat(frames, ignore_index=True)
    # apenas alunos com as 5 notas presentes (mesmo critério dos estudos anteriores)
    df = df.dropna(subset=NOTAS)
    df = df[(df[NOTAS] > 0).all(axis=1)]
    df["MEDIA_5"] = df[NOTAS].mean(axis=1)
    return df


def main() -> None:
    censo = censo_maristas()
    print(f"Escolas com 'MARISTA' no nome no Censo 2025: {len(censo)}")

    codigos = set(censo["CO_ENTIDADE"])
    alunos = enem_por_escola(codigos)
    print(f"Alunos ENEM 2025 com 5 notas nessas escolas: {len(alunos)}")

    agg = alunos.groupby("CO_ESCOLA").agg(
        N_ALUNOS=("MEDIA_5", "size"),
        MEDIA_5=("MEDIA_5", "mean"),
        CN=("NU_NOTA_CN", "mean"),
        CH=("NU_NOTA_CH", "mean"),
        LC=("NU_NOTA_LC", "mean"),
        MT=("NU_NOTA_MT", "mean"),
        REDACAO=("NU_NOTA_REDACAO", "mean"),
    ).reset_index()

    rank = agg.merge(
        censo[["CO_ENTIDADE", "NO_ENTIDADE", "NO_MUNICIPIO", "SG_UF"]],
        left_on="CO_ESCOLA", right_on="CO_ENTIDADE", how="left",
    ).drop(columns=["CO_ENTIDADE"])
    rank = rank.sort_values("MEDIA_5", ascending=False).reset_index(drop=True)
    rank.insert(0, "POSICAO", rank.index + 1)

    cols = ["POSICAO", "NO_ENTIDADE", "NO_MUNICIPIO", "SG_UF", "N_ALUNOS",
            "MEDIA_5", "CN", "CH", "LC", "MT", "REDACAO", "CO_ESCOLA"]
    rank = rank[cols].round(1)
    rank.to_csv(OUT / "ranking_maristas_brasil_enem2025.csv", index=False)

    sem_enem = censo[~censo["CO_ENTIDADE"].isin(set(agg["CO_ESCOLA"]))]
    sem_enem.to_csv(OUT / "maristas_censo_sem_alunos_enem.csv", index=False)

    pd.set_option("display.width", 220)
    print("\n=== RANKING MARISTAS BRASIL — ENEM 2025 (média das 5 notas) ===")
    print(rank.to_string(index=False))
    nat = rank[rank["CO_ESCOLA"] == CO_MARISTA_NATAL]
    if not nat.empty:
        print(f"\n>>> Marista Natal: posição {int(nat.iloc[0]['POSICAO'])} de {len(rank)}")
    print(f"\nEscolas do Censo sem alunos com 5 notas no ENEM: {len(sem_enem)}")


if __name__ == "__main__":
    main()
