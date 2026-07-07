#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoria final do estudo 54 x 54 - ENEM 2025 Natal/RN.

Objetivo: checar a veracidade dos dados publicados no comparativo de escolas:
- origem dos arquivos oficiais;
- mapeamento dos códigos INEP pelo Censo Escolar;
- filtros de presença, redação e 5 notas;
- formação da amostra 54 x 54;
- consistência entre recálculo e CSV final;
- ausência de identificadores individuais nos outputs públicos.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analises_primi_2025_cop30" / "outputs"
RESULTADOS = ROOT / "DADOS" / "RESULTADOS_2025.csv"
CENSO_ZIP = ROOT / "analises_primi_2025_cop30" / "cache" / "microdados_censo_escolar_2025.zip"
VERIF_ENEM = OUT / "verificacao_crc_local_vs_zip_oficial_2025.json"
CENSO_CODES = OUT / "escolas_natal_censo_2025_codigos.csv"
SUMMARY_CSV = OUT / "comparativo_escolas_natal_2025_resumo.csv"
SELECTED_CSV = OUT / "comparativo_escolas_natal_2025_amostra_54x54.csv"
POOL_CSV = OUT / "comparativo_escolas_natal_2025_pool_5notas.csv"

NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
PRESENCAS = ["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]

ESCOLAS = {
    24097004: {"nome": "Ciências Aplicadas", "criterio": "todos_5_notas"},
    24088846: {"nome": "Colégio Porto", "criterio": "top_54_media_5"},
    24069191: {"nome": "CEI S/A Romualdo", "criterio": "top_54_media_5"},
    24057134: {"nome": "Marista de Natal", "criterio": "top_54_media_5"},
}
CEI_MAIS_NAO_USADO = 24350303


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fp:
        for block in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_target_rows() -> pd.DataFrame:
    usecols = [
        "NU_SEQUENCIAL",
        "CO_ESCOLA",
        "CO_MUNICIPIO_ESC",
        "NO_MUNICIPIO_ESC",
        "SG_UF_ESC",
        "TP_STATUS_REDACAO",
        *PRESENCAS,
        *NOTAS,
    ]
    wanted = set(ESCOLAS) | {CEI_MAIS_NAO_USADO}
    frames: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        RESULTADOS,
        sep=";",
        encoding="latin1",
        usecols=usecols,
        chunksize=500_000,
    ):
        sub = chunk[
            chunk["CO_ESCOLA"].isin(wanted)
            & chunk["SG_UF_ESC"].eq("RN")
            & chunk["NO_MUNICIPIO_ESC"].eq("Natal")
        ].copy()
        if not sub.empty:
            frames.append(sub)
    if not frames:
        raise RuntimeError("Nenhum registro encontrado para os códigos auditados.")
    df = pd.concat(frames, ignore_index=True)
    for col in ["CO_ESCOLA", "CO_MUNICIPIO_ESC", "TP_STATUS_REDACAO", *PRESENCAS]:
        df[col] = df[col].astype("Int64")
    return df


def compute_pool_and_selection(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []
    selected_parts = []
    strict_parts = []

    for codigo, meta in ESCOLAS.items():
        raw = df[df["CO_ESCOLA"].eq(codigo)].copy()
        missing_any_note = raw[NOTAS].isna().any(axis=1)
        absent_any_area = ~raw[PRESENCAS].eq(1).all(axis=1)
        red_invalid = ~raw["TP_STATUS_REDACAO"].eq(1)
        strict = raw[~missing_any_note & ~absent_any_area & ~red_invalid].copy()
        strict["MEDIA_4_TRI"] = strict[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"]].mean(axis=1)
        strict["MEDIA_5"] = strict[NOTAS].mean(axis=1)
        strict = strict.sort_values(
            ["MEDIA_5", "MEDIA_4_TRI", "NU_NOTA_REDACAO", "NU_NOTA_MT"],
            ascending=False,
        ).reset_index(drop=True)
        strict["RANK_POOL"] = np.arange(1, len(strict) + 1)
        strict["ESCOLA"] = meta["nome"]
        strict_parts.append(strict)

        if meta["criterio"] == "todos_5_notas":
            selected = strict.copy()
        else:
            selected = strict.head(54).copy()
        selected["RANK_AMOSTRA"] = np.arange(1, len(selected) + 1)
        selected["CRITERIO_AMOSTRA"] = meta["criterio"]
        selected_parts.append(selected)

        next_after_cut = None
        if len(strict) > 54:
            next_after_cut = float(strict.iloc[54]["MEDIA_5"])
        rows.append(
            {
                "codigo_inep": codigo,
                "escola": meta["nome"],
                "criterio": meta["criterio"],
                "raw_resultados_natal": int(len(raw)),
                "excluidos_total": int(len(raw) - len(strict)),
                "excluidos_alguma_nota_ausente": int(missing_any_note.sum()),
                "excluidos_alguma_area_ausente": int(absent_any_area.sum()),
                "excluidos_redacao_invalida": int(red_invalid.sum()),
                "pool_5_notas_validas": int(len(strict)),
                "amostra_n": int(len(selected)),
                "menor_media_5_amostra": float(selected["MEDIA_5"].min()),
                "maior_media_5_fora_top54": next_after_cut,
                "top54_respeitado": bool(
                    len(strict) <= 54
                    or float(selected["MEDIA_5"].min()) >= float(strict.iloc[54]["MEDIA_5"])
                ),
            }
        )

    counts = pd.DataFrame(rows)
    strict_all = pd.concat(strict_parts, ignore_index=True)
    selected_all = pd.concat(selected_parts, ignore_index=True)
    return counts, strict_all, selected_all


def audit_non_used_code(df: pd.DataFrame) -> dict:
    raw = df[df["CO_ESCOLA"].eq(CEI_MAIS_NAO_USADO)].copy()
    if raw.empty:
        return {
            "codigo": CEI_MAIS_NAO_USADO,
            "raw_resultados_natal": 0,
            "pool_5_notas_validas": 0,
            "motivo_nao_uso": "não encontrado no RESULTADOS_2025.csv para Natal/RN",
        }
    strict = raw.dropna(subset=NOTAS).copy()
    strict = strict[strict[PRESENCAS].eq(1).all(axis=1) & strict["TP_STATUS_REDACAO"].eq(1)]
    return {
        "codigo": CEI_MAIS_NAO_USADO,
        "raw_resultados_natal": int(len(raw)),
        "pool_5_notas_validas": int(len(strict)),
        "motivo_nao_uso": "Censo Escolar identifica como CENTRO DE EDUCACAO INTEGRADA MAIS LTDA, diferente do CEI S/A Romualdo pedido",
    }


def compare_outputs(counts: pd.DataFrame, selected_recalc: pd.DataFrame) -> dict:
    summary = pd.read_csv(SUMMARY_CSV)
    selected = pd.read_csv(SELECTED_CSV)
    pool = pd.read_csv(POOL_CSV)

    expected_counts = counts.set_index("escola")["amostra_n"].to_dict()
    actual_counts = selected.groupby("ESCOLA").size().to_dict()
    pool_counts = pool.groupby("ESCOLA").size().to_dict()

    recalculated_summary = []
    for codigo, meta in ESCOLAS.items():
        sel = selected_recalc[selected_recalc["CO_ESCOLA"].eq(codigo)]
        recalculated_summary.append(
            {
                "escola": meta["nome"],
                "media_5_recalculada": float(sel["MEDIA_5"].mean()),
                "media_4_tri_recalculada": float(sel["MEDIA_4_TRI"].mean()),
                "media_redacao_recalculada": float(sel["NU_NOTA_REDACAO"].mean()),
            }
        )
    rec = pd.DataFrame(recalculated_summary)
    merged = summary.merge(rec, on="escola", how="left")
    merged["diff_media_5"] = merged["media_5"] - merged["media_5_recalculada"]
    merged["diff_media_4_tri"] = merged["media_4_tri"] - merged["media_4_tri_recalculada"]
    merged["diff_media_redacao"] = merged["media_redacao"] - merged["media_redacao_recalculada"]

    forbidden_cols = {"NU_SEQUENCIAL", "NU_INSCRICAO"}
    forbidden_in_public = sorted(forbidden_cols.intersection(selected.columns))

    return {
        "selected_rows": int(len(selected)),
        "selected_counts_match": actual_counts == expected_counts,
        "selected_counts": actual_counts,
        "pool_counts": pool_counts,
        "summary_max_abs_diff": {
            "media_5": float(merged["diff_media_5"].abs().max()),
            "media_4_tri": float(merged["diff_media_4_tri"].abs().max()),
            "media_redacao": float(merged["diff_media_redacao"].abs().max()),
        },
        "summary_values_match_recalculation": bool(
            (merged["diff_media_5"].abs().max() < 1e-9)
            and (merged["diff_media_4_tri"].abs().max() < 1e-9)
            and (merged["diff_media_redacao"].abs().max() < 1e-9)
        ),
        "forbidden_identifier_columns_in_selected_csv": forbidden_in_public,
        "selected_public_has_no_original_identifier": len(forbidden_in_public) == 0,
    }


def make_markdown(audit: dict, counts: pd.DataFrame, censo: pd.DataFrame) -> str:
    lines = [
        "# Auditoria final - Comparativo 54 x 54 ENEM 2025 Natal/RN",
        "",
        f"Gerado em: {audit['generated_at']}",
        "",
        "## Veredito",
        "",
        f"**Status:** {audit['verdict']}.",
        "",
        "Os dados do estudo foram recalculados a partir do `RESULTADOS_2025.csv` local, que já bate CRC32 e tamanho com o ZIP oficial do INEP. Os códigos das escolas foram conferidos no Censo Escolar 2025/INEP. A amostra final tem 216 linhas, com 54 alunos por escola, e o CSV público não exporta identificador individual original.",
        "",
        "## Fontes auditadas",
        "",
        f"- ENEM 2025: `{RESULTADOS}`",
        f"- Verificação ENEM local x ZIP oficial: `{VERIF_ENEM}`",
        f"- Censo Escolar 2025: `{CENSO_ZIP}`",
        f"- Resumo publicado: `{SUMMARY_CSV}`",
        f"- Amostra publicada: `{SELECTED_CSV}`",
        "",
        "## Códigos oficiais das escolas",
        "",
        "| Código INEP | Nome no Censo Escolar 2025 | Município/UF | Usado? |",
        "|---:|---|---|---|",
    ]
    for _, row in censo.sort_values("CO_ENTIDADE").iterrows():
        usado = "sim" if int(row["CO_ENTIDADE"]) in ESCOLAS else "não"
        lines.append(
            f"| {int(row['CO_ENTIDADE'])} | {row['NO_ENTIDADE']} | {row['NO_MUNICIPIO']}/{row['SG_UF']} | {usado} |"
        )

    lines += [
        "",
        "## Contagens e filtros",
        "",
        "| Escola | Bruto no ENEM | Excluídos | Pool 5 notas | Amostra | Critério | Top 54 OK? |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for _, row in counts.sort_values("escola").iterrows():
        lines.append(
            f"| {row['escola']} | {int(row['raw_resultados_natal'])} | {int(row['excluidos_total'])} | "
            f"{int(row['pool_5_notas_validas'])} | {int(row['amostra_n'])} | {row['criterio']} | "
            f"{'sim' if row['top54_respeitado'] else 'não'} |"
        )

    lines += [
        "",
        "## Checagens automáticas",
        "",
        f"- Amostra final tem 216 linhas: `{audit['checks']['selected_rows'] == 216}`.",
        f"- Contagem 54 por escola confere: `{audit['checks']['selected_counts_match']}`.",
        f"- Médias do resumo conferem com recálculo: `{audit['checks']['summary_values_match_recalculation']}`.",
        f"- CSV público sem `NU_SEQUENCIAL`/`NU_INSCRICAO`: `{audit['checks']['selected_public_has_no_original_identifier']}`.",
        f"- Código CEI Mais não usado: `{audit['cei_mais_nao_usado']['motivo_nao_uso']}`.",
        "",
        "## Hashes SHA-256",
        "",
    ]
    for label, value in audit["sha256"].items():
        lines.append(f"- `{label}`: `{value}`")

    lines += [
        "",
        "## Observação metodológica",
        "",
        "Este estudo não é média geral bruta das escolas. Ele compara N equalizado: todos os 54 alunos do Ciências Aplicadas com os 54 melhores de Porto, CEI S/A Romualdo e Marista de Natal, usando média simples das 5 notas como régua.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    verif = json.loads(VERIF_ENEM.read_text(encoding="utf-8"))
    enem_matches = all(
        item.get("match_crc32") and item.get("match_size")
        for item in verif.get("comparacoes", [])
        if item.get("alvo") in {"DADOS/RESULTADOS_2025.csv", "DADOS/ITENS_PROVA_2025.csv"}
    )

    censo = pd.read_csv(CENSO_CODES)
    target_codes_in_censo = set(censo["CO_ENTIDADE"].astype(int)).issuperset(set(ESCOLAS) | {CEI_MAIS_NAO_USADO})

    raw = read_target_rows()
    counts, _strict, selected_recalc = compute_pool_and_selection(raw)
    checks = compare_outputs(counts, selected_recalc)
    cei_mais = audit_non_used_code(raw)

    all_ok = (
        enem_matches
        and target_codes_in_censo
        and bool(counts["top54_respeitado"].all())
        and checks["selected_rows"] == 216
        and checks["selected_counts_match"]
        and checks["summary_values_match_recalculation"]
        and checks["selected_public_has_no_original_identifier"]
        and set(checks["selected_counts"].values()) == {54}
    )

    audit = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "verdict": "APROVADO" if all_ok else "REVISAR",
        "sources": {
            "enem_zip_url": verif.get("url"),
            "resultados_local": str(RESULTADOS),
            "censo_zip_url": "https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip",
            "censo_zip_local": str(CENSO_ZIP),
        },
        "source_checks": {
            "enem_crc32_and_size_match_official_zip": enem_matches,
            "target_codes_present_in_censo_2025": target_codes_in_censo,
        },
        "counts": counts.to_dict("records"),
        "cei_mais_nao_usado": cei_mais,
        "checks": checks,
        "sha256": {
            "RESULTADOS_2025.csv": sha256(RESULTADOS),
            "microdados_censo_escolar_2025.zip": sha256(CENSO_ZIP),
            "comparativo_escolas_natal_2025_resumo.csv": sha256(SUMMARY_CSV),
            "comparativo_escolas_natal_2025_amostra_54x54.csv": sha256(SELECTED_CSV),
        },
    }

    json_path = OUT / "auditoria_final_comparativo_escolas_natal_2025.json"
    md_path = OUT / "auditoria_final_comparativo_escolas_natal_2025.md"
    counts_path = OUT / "auditoria_final_comparativo_escolas_natal_2025_contagens.csv"

    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    counts.to_csv(counts_path, index=False)
    md_path.write_text(make_markdown(audit, counts, censo), encoding="utf-8")

    print("VERDICT:", audit["verdict"])
    print("JSON:", json_path)
    print("MD:", md_path)
    print("COUNTS:", counts_path)


if __name__ == "__main__":
    main()
