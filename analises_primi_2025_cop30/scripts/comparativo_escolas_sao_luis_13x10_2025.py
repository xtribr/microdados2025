#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparativo ENEM 2025 - São Luís/MA - N equalizado.

Metodologia:
- São Luís/MA, escola de conclusão do ensino médio.
- Escolas privadas com Ensino Médio regular no Censo Escolar 2025.
- Alunos com as 5 notas válidas: CN, CH, LC, MT e Redação.
- Seleciona as 10 primeiras escolas pela média da coorte completa válida.
- A escola líder tem 13 alunos válidos; portanto, o confronto é 13 x 13.
- Líder entra inteira; demais escolas entram com seus 13 melhores por média
  simples das 5 notas.
"""

from __future__ import annotations

import json
import zipfile
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DADOS = ROOT / "DADOS"
OUT = ROOT / "analises_primi_2025_cop30" / "outputs"
CACHE = ROOT / "analises_primi_2025_cop30" / "cache"
RESULTADOS = DADOS / "RESULTADOS_2025.csv"
CENSO_ZIP = CACHE / "microdados_censo_escolar_2025.zip"
CENSO_ESCOLAS = "microdados_censo_escolar_2025/dados/Tabela_Escola_2025.csv"

LOGOS = [
    Path("/Users/home/Desktop/logotipo.png"),
    ROOT / "logo_xtri_marca_real.png",
    OUT / "crop_logo.png",
]

NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
PRESENCAS = ["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]

BG = "#FBFCFE"
PANEL = "#FFFFFF"
PANEL_SOFT = "#F3F6FA"
INK = "#182032"
MUTED = "#687386"
GRID = "#E3E8F0"
XTRI_BLUE = "#27B8EF"
XTRI_ORANGE = "#FF4E2E"
GREEN = "#1F9D63"

REQUESTED_NAME_TERMS = ["RF", "LITERATO", "DOM BOSCO", "EDUCALLIS"]


def fmt_num(value: float, casas: int = 1) -> str:
    return f"{value:.{casas}f}".replace(".", ",")


def load_logo() -> Image.Image | None:
    for path in LOGOS:
        if not path.exists():
            continue
        img = Image.open(path).convert("RGBA")
        bbox = img.getbbox()
        return img.crop(bbox) if bbox else img
    return None


def rounded_box(ax, x, y, w, h, fc=PANEL, ec=GRID, lw=1.0, radius=0.018):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
    )
    ax.add_patch(patch)
    return patch


def draw_text(ax, x, y, text, size, color=INK, weight="normal", ha="left", va="center"):
    ax.text(
        x,
        y,
        text,
        fontsize=size,
        color=color,
        fontweight=weight,
        ha=ha,
        va=va,
        family="DejaVu Sans",
    )


def short_name(name: str) -> str:
    replacements = {
        "MAPLE BEAR SAO LUIS": "Maple Bear",
        "CENTRO EDUCACIONAL MONTESSORIANO REINO INFANTIL": "Montessoriano",
        "RF ENSINO MEDIO LTDA": "RF Ensino Médio",
        "COLEGIO LITERATO": "Literato",
        "COLEGIO DOM BOSCO LTDA": "Dom Bosco",
        "COLEGIO EDUCALLIS": "Educallis",
        "AUDAZ COLEGIO LTDA": "Audaz",
        "D PEDRO II EMPREENDIMENTOS EDUCACIONAIS LTDA": "D. Pedro II",
        "ESCOLA CRESCIMENTO": "Crescimento",
    }
    return replacements.get(str(name).strip(), str(name).title())


def read_censo_private_sao_luis() -> pd.DataFrame:
    if not CENSO_ZIP.exists():
        raise FileNotFoundError(
            f"ZIP do Censo Escolar não encontrado: {CENSO_ZIP}. "
            "Baixe de https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip"
        )
    usecols = [
        "NU_ANO_CENSO",
        "NO_UF",
        "SG_UF",
        "NO_MUNICIPIO",
        "CO_MUNICIPIO",
        "NO_ENTIDADE",
        "CO_ENTIDADE",
        "TP_DEPENDENCIA",
        "TP_LOCALIZACAO",
        "DS_ENDERECO",
        "NO_BAIRRO",
        "IN_COMUM_MEDIO_MEDIO",
    ]
    frames: list[pd.DataFrame] = []
    with zipfile.ZipFile(CENSO_ZIP) as zf, zf.open(CENSO_ESCOLAS) as fp:
        for chunk in pd.read_csv(fp, sep=";", encoding="latin1", usecols=usecols, chunksize=50_000):
            sub = chunk[
                chunk["SG_UF"].eq("MA")
                & chunk["NO_MUNICIPIO"].eq("São Luís")
                & chunk["TP_DEPENDENCIA"].eq(4)
                & chunk["IN_COMUM_MEDIO_MEDIO"].eq(1)
            ].copy()
            if not sub.empty:
                frames.append(sub)
    if not frames:
        raise RuntimeError("Nenhuma escola privada de Ensino Médio encontrada no Censo Escolar 2025 para São Luís/MA.")
    df = pd.concat(frames, ignore_index=True)
    df["CO_ENTIDADE"] = df["CO_ENTIDADE"].astype(int)
    df["NOME_CURTO"] = df["NO_ENTIDADE"].map(short_name)
    crescimento = df["NO_ENTIDADE"].eq("ESCOLA CRESCIMENTO")
    df.loc[crescimento & df["NO_BAIRRO"].eq("CALHAU"), "NOME_CURTO"] = "Crescimento Calhau"
    df.loc[crescimento & ~df["NO_BAIRRO"].eq("CALHAU"), "NOME_CURTO"] = "Crescimento Ren."
    return df


def read_enem_sao_luis(censo: pd.DataFrame) -> pd.DataFrame:
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
    private_codes = set(censo["CO_ENTIDADE"].astype(float))
    frames: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        RESULTADOS,
        sep=";",
        encoding="latin1",
        usecols=usecols,
        chunksize=500_000,
    ):
        sub = chunk[
            chunk["SG_UF_ESC"].eq("MA")
            & chunk["NO_MUNICIPIO_ESC"].eq("São Luís")
            & chunk["CO_ESCOLA"].isin(private_codes)
        ].copy()
        if not sub.empty:
            frames.append(sub)
    if not frames:
        raise RuntimeError("Nenhum candidato encontrado para escolas privadas de São Luís/MA.")
    df = pd.concat(frames, ignore_index=True)
    for col in ["CO_ESCOLA", "CO_MUNICIPIO_ESC", "TP_STATUS_REDACAO", *PRESENCAS]:
        df[col] = df[col].astype("Int64")
    return df


def build_study(censo: pd.DataFrame, raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, int, int]:
    valid = raw.dropna(subset=NOTAS).copy()
    valid = valid[valid[PRESENCAS].eq(1).all(axis=1) & valid["TP_STATUS_REDACAO"].eq(1)].copy()
    valid["MEDIA_4_TRI"] = valid[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"]].mean(axis=1)
    valid["MEDIA_5"] = valid[NOTAS].mean(axis=1)

    pool = (
        valid.groupby("CO_ESCOLA")
        .agg(
            n_pool_5_notas=("MEDIA_5", "size"),
            media_pool_5=("MEDIA_5", "mean"),
            mediana_pool_5=("MEDIA_5", "median"),
            max_pool_5=("MEDIA_5", "max"),
        )
        .reset_index()
    )
    pool["CO_ESCOLA"] = pool["CO_ESCOLA"].astype(int)
    pool = pool.merge(
        censo[["CO_ENTIDADE", "NO_ENTIDADE", "NOME_CURTO", "DS_ENDERECO", "NO_BAIRRO"]],
        left_on="CO_ESCOLA",
        right_on="CO_ENTIDADE",
        how="left",
    )
    pool = pool.sort_values(["media_pool_5", "n_pool_5_notas"], ascending=[False, False]).reset_index(drop=True)
    top10 = pool.head(10).copy()
    top10["rank_pool_cidade"] = np.arange(1, len(top10) + 1)

    leader_code = int(top10.iloc[0]["CO_ESCOLA"])
    n_equalizado = int(top10.iloc[0]["n_pool_5_notas"])
    if n_equalizado < 5:
        raise RuntimeError(f"N equalizado muito pequeno para estudo público: {n_equalizado}")

    selected_parts: list[pd.DataFrame] = []
    for _, school in top10.iterrows():
        code = int(school["CO_ESCOLA"])
        sub = valid[valid["CO_ESCOLA"].eq(code)].copy()
        sub = sub.sort_values(
            ["MEDIA_5", "MEDIA_4_TRI", "NU_NOTA_REDACAO", "NU_NOTA_MT"],
            ascending=False,
        ).reset_index(drop=True)
        sub["RANK_POOL"] = np.arange(1, len(sub) + 1)
        if code == leader_code:
            selected = sub.copy()
            criterio = "todos_validos_lider"
        else:
            selected = sub.head(n_equalizado).copy()
            criterio = f"top_{n_equalizado}_media_5"
        selected["RANK_AMOSTRA"] = np.arange(1, len(selected) + 1)
        selected["CRITERIO_AMOSTRA"] = criterio
        selected["NO_ENTIDADE"] = school["NO_ENTIDADE"]
        selected["NOME_CURTO"] = school["NOME_CURTO"]
        selected["RANK_POOL_CIDADE"] = int(school["rank_pool_cidade"])
        selected_parts.append(selected)

    selected = pd.concat(selected_parts, ignore_index=True)
    selected["ALUNO_ID_LOCAL"] = selected.apply(
        lambda r: f"SLZ_{int(r['CO_ESCOLA'])}_{int(r['RANK_AMOSTRA']):02d}", axis=1
    )

    rows = []
    leader_mean = None
    for _, school in top10.iterrows():
        code = int(school["CO_ESCOLA"])
        sel = selected[selected["CO_ESCOLA"].eq(code)]
        row = {
            "rank_pool_cidade": int(school["rank_pool_cidade"]),
            "codigo_inep": code,
            "escola": school["NOME_CURTO"],
            "nome_oficial_censo": school["NO_ENTIDADE"],
            "n_pool_5_notas": int(school["n_pool_5_notas"]),
            "n_amostra": int(len(sel)),
            "criterio_amostra": str(sel["CRITERIO_AMOSTRA"].iloc[0]),
            "media_pool_5": float(school["media_pool_5"]),
            "media_amostra_5": float(sel["MEDIA_5"].mean()),
            "mediana_amostra_5": float(sel["MEDIA_5"].median()),
            "dp_amostra_5": float(sel["MEDIA_5"].std(ddof=1)),
            "min_amostra_5": float(sel["MEDIA_5"].min()),
            "max_amostra_5": float(sel["MEDIA_5"].max()),
            "media_4_tri": float(sel["MEDIA_4_TRI"].mean()),
            "media_cn": float(sel["NU_NOTA_CN"].mean()),
            "media_ch": float(sel["NU_NOTA_CH"].mean()),
            "media_lc": float(sel["NU_NOTA_LC"].mean()),
            "media_mt": float(sel["NU_NOTA_MT"].mean()),
            "media_redacao": float(sel["NU_NOTA_REDACAO"].mean()),
            "endereco": school["DS_ENDERECO"],
            "bairro": school["NO_BAIRRO"],
        }
        if code == leader_code:
            leader_mean = row["media_amostra_5"]
        rows.append(row)
    summary = pd.DataFrame(rows)
    summary["delta_amostra_5_vs_lider"] = summary["media_amostra_5"] - float(leader_mean)
    summary = summary.sort_values("media_amostra_5", ascending=False).reset_index(drop=True)
    summary["rank_equalizado"] = np.arange(1, len(summary) + 1)
    return top10, selected, summary, leader_code, n_equalizado


def save_outputs(censo: pd.DataFrame, top10: pd.DataFrame, selected: pd.DataFrame, summary: pd.DataFrame, leader_code: int, n_equalizado: int) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    censo_path = OUT / "escolas_sao_luis_censo_2025_privadas_em.csv"
    top10_path = OUT / "comparativo_escolas_sao_luis_2025_top10_pool.csv"
    selected_path = OUT / "comparativo_escolas_sao_luis_2025_amostra_13x10.csv"
    summary_path = OUT / "comparativo_escolas_sao_luis_2025_resumo_13x10.csv"
    audit_path = OUT / "auditoria_comparativo_escolas_sao_luis_2025_13x10.json"

    censo.to_csv(censo_path, index=False)
    top10.to_csv(top10_path, index=False)

    selected_public = selected[
        [
            "ALUNO_ID_LOCAL",
            "CO_ESCOLA",
            "NO_ENTIDADE",
            "NOME_CURTO",
            "RANK_POOL_CIDADE",
            "CRITERIO_AMOSTRA",
            "RANK_POOL",
            "RANK_AMOSTRA",
            "MEDIA_5",
            "MEDIA_4_TRI",
            *NOTAS,
        ]
    ].copy()
    selected_public.to_csv(selected_path, index=False)
    summary.to_csv(summary_path, index=False)

    requested_hits = {
        term: summary[summary["nome_oficial_censo"].str.upper().str.contains(term, regex=False)][
            ["codigo_inep", "escola", "nome_oficial_censo", "n_pool_5_notas", "media_pool_5", "media_amostra_5"]
        ].to_dict("records")
        for term in REQUESTED_NAME_TERMS
    }
    audit = {
        "gerado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
        "fonte_enem": str(RESULTADOS),
        "fonte_censo_escolar_2025": str(CENSO_ZIP),
        "fonte_censo_url": "https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip",
        "recorte": "São Luís/MA; escolas privadas com Ensino Médio no Censo 2025; ENEM 2025",
        "criterio_5_notas": {
            "presenca": "TP_PRESENCA_CN/CH/LC/MT == 1",
            "redacao": "TP_STATUS_REDACAO == 1",
            "notas_obrigatorias": NOTAS,
        },
        "selecao_top10": "10 primeiras escolas por média da coorte completa com 5 notas válidas",
        "lider_codigo_inep": leader_code,
        "n_equalizado": n_equalizado,
        "criterio_amostra": "lider entra inteiro; demais escolas entram com top N por MEDIA_5",
        "ranking_publicado": "ordenado pela média do grupo equalizado (media_amostra_5)",
        "termos_pedidos_encontrados": requested_hits,
        "n_amostra_total": int(len(selected_public)),
        "arquivos": {
            "censo_privadas_em": str(censo_path),
            "top10_pool": str(top10_path),
            "amostra": str(selected_path),
            "resumo": str(summary_path),
        },
    }
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "censo": censo_path,
        "top10": top10_path,
        "selected": selected_path,
        "summary": summary_path,
        "audit": audit_path,
    }


def make_feed(summary: pd.DataFrame, n_equalizado: int, leader_code: int) -> Path:
    W, H = 1080, 1350
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    logo = load_logo()
    if logo is not None:
        logo_ax = fig.add_axes([0.055, 0.934, 0.064, 0.054])
        logo_ax.axis("off")
        logo_ax.imshow(logo)
    draw_text(ax, 0.128, 0.965, "XTRI ENEM 2025", 18, INK, "bold")
    draw_text(ax, 0.128, 0.943, "São Luís/MA · N equalizado · microdados oficiais", 10.5, MUTED)

    draw_text(ax, 0.055, 0.895, f"{n_equalizado} contra {n_equalizado}", 33, INK, "bold")
    draw_text(
        ax,
        0.055,
        0.866,
        "A líder entra inteira; as demais entram com o mesmo tamanho de grupo.",
        12.6,
        MUTED,
    )

    chips = [
        ("10 escolas privadas", 0.055, 0.813, 0.205),
        ("Ranking: média das 5 notas", 0.275, 0.813, 0.260),
        ("Redação válida + 4 TRI", 0.550, 0.813, 0.230),
        (f"N = {len(summary) * n_equalizado}", 0.795, 0.813, 0.115),
    ]
    for text, x, y, w in chips:
        rounded_box(ax, x, y, w, 0.040, "#F1F5F9", GRID, lw=1, radius=0.016)
        draw_text(ax, x + w / 2, y + 0.020, text, 9.5, INK, "bold", "center")

    # Barras principais: média da amostra N equalizada.
    ordered = summary.sort_values("media_amostra_5", ascending=True).copy()
    colors = [XTRI_ORANGE if int(r.codigo_inep) == leader_code else XTRI_BLUE for _, r in ordered.iterrows()]
    bar_ax = fig.add_axes([0.270, 0.430, 0.655, 0.330])
    y = np.arange(len(ordered))
    bar_ax.barh(y, ordered["media_amostra_5"], color=colors, alpha=0.88, height=0.58)
    bar_ax.set_yticks(y)
    bar_ax.set_yticklabels(ordered["escola"], fontsize=9.5, color=INK)
    bar_ax.set_xlim(660, max(ordered["media_amostra_5"]) + 12)
    bar_ax.tick_params(axis="x", colors=MUTED, labelsize=8.5, length=0)
    bar_ax.tick_params(axis="y", length=0)
    bar_ax.grid(axis="x", color=GRID, linewidth=1)
    bar_ax.set_axisbelow(True)
    for side in ["top", "right", "left", "bottom"]:
        bar_ax.spines[side].set_visible(False)
    bar_ax.set_title("Média dos grupos equalizados", loc="left", fontsize=12.3, color=INK, fontweight="bold", pad=8)
    for yi, (_, row) in zip(y, ordered.iterrows()):
        bar_ax.text(
            row.media_amostra_5 + 1.2,
            yi,
            fmt_num(row.media_amostra_5),
            va="center",
            ha="left",
            fontsize=9.2,
            color=INK,
            fontweight="bold",
        )

    # Tabela compacta em ordem do ranking equalizado, que é a régua do estudo.
    table = summary.sort_values("rank_equalizado").copy()
    rounded_box(ax, 0.055, 0.105, 0.890, 0.280, PANEL_SOFT, GRID, lw=1, radius=0.020)
    headers = ["# N", "Escola", "Pool", "Amostra", "Média N", "Média pool", "Δ Maple"]
    colx = [0.090, 0.185, 0.468, 0.565, 0.670, 0.787, 0.902]
    for h, xh in zip(headers, colx):
        draw_text(ax, xh, 0.358, h, 8.7, MUTED, "bold", ha="center" if h != "Escola" else "left")
    ax.plot([0.075, 0.925], [0.338, 0.338], color=GRID, lw=1)

    start_y = 0.314
    row_gap = 0.0205
    for i, (_, row) in enumerate(table.iterrows()):
        yy = start_y - i * row_gap
        leader = int(row.codigo_inep) == leader_code
        color = XTRI_ORANGE if leader else INK
        draw_text(ax, 0.090, yy, str(int(row.rank_equalizado)), 8.9, MUTED, "bold", ha="center")
        draw_text(ax, 0.120, yy, "●", 8.6, XTRI_ORANGE if leader else XTRI_BLUE, "bold")
        draw_text(ax, 0.138, yy, str(row.escola), 8.8, color, "bold" if leader else "normal")
        draw_text(ax, 0.468, yy, str(int(row.n_pool_5_notas)), 8.7, INK, ha="center")
        amostra = "todos" if leader else f"top {n_equalizado}"
        draw_text(ax, 0.565, yy, amostra, 8.5, INK, ha="center")
        draw_text(ax, 0.670, yy, fmt_num(row.media_amostra_5), 8.8, INK, "bold", ha="center")
        draw_text(ax, 0.787, yy, fmt_num(row.media_pool_5), 8.6, INK, ha="center")
        delta = float(row.delta_amostra_5_vs_lider)
        delta_txt = "base" if leader else ("+" if delta >= 0 else "") + fmt_num(delta)
        delta_color = XTRI_ORANGE if leader else (GREEN if delta > 0 else INK)
        draw_text(ax, 0.902, yy, delta_txt, 8.6, delta_color, "bold", ha="center")

    rounded_box(ax, 0.055, 0.052, 0.890, 0.046, "#FFFFFF", GRID, lw=1, radius=0.018)
    draw_text(ax, 0.075, 0.082, "Leitura correta", 9.7, INK, "bold")
    draw_text(
        ax,
        0.075,
        0.064,
        "Equiparação por N: compara grupos do mesmo tamanho; não é média geral bruta das escolas.",
        8.2,
        MUTED,
    )
    draw_text(
        ax,
        0.075,
        0.033,
        "Fonte: Microdados ENEM 2025/INEP + Censo Escolar 2025/INEP · 5 notas válidas.",
        8.2,
        MUTED,
    )
    draw_text(ax, 0.945, 0.023, "Dados reais ou nada.", 10.5, XTRI_ORANGE, "bold", "right")

    png_path = OUT / "comparativo_escolas_sao_luis_2025_13x10_feed.png"
    fig.savefig(png_path, dpi=100, facecolor=BG)
    plt.close(fig)
    return png_path


def main() -> None:
    censo = read_censo_private_sao_luis()
    raw = read_enem_sao_luis(censo)
    top10, selected, summary, leader_code, n_equalizado = build_study(censo, raw)
    paths = save_outputs(censo, top10, selected, summary, leader_code, n_equalizado)
    png = make_feed(summary, n_equalizado, leader_code)

    legenda = OUT / "legenda_comparativo_escolas_sao_luis_2025_13x10.md"
    leader = summary[summary["codigo_inep"].eq(leader_code)].iloc[0]
    legenda.write_text(
        "\n".join(
            [
                "# Legenda - Comparativo São Luís/MA ENEM 2025",
                "",
                f"São Luís tem uma escola líder no recorte de 5 notas com apenas {n_equalizado} alunos válidos: {leader['escola']}.",
                "",
                f"Para comparar com justiça de tamanho amostral, fizemos um confronto {n_equalizado} contra {n_equalizado}: a líder entra inteira e as demais escolas entram com seus {n_equalizado} melhores alunos por média simples das 5 notas.",
                "",
                "Entraram no estudo as 10 primeiras escolas privadas de Ensino Médio de São Luís pela média da coorte completa com 5 notas válidas.",
                "",
                "Critério: presença nas quatro áreas objetivas, redação válida e notas em CN, CH, LC, MT e Redação.",
                "",
                "O ranking exibido na arte está ordenado pela média do grupo equalizado, não pela média pool.",
                "",
                "Importante: isso não é ranking geral bruto das escolas. É uma comparação com N equalizado, útil para discutir desempenho de topo com o mesmo tamanho de grupo.",
                "",
                "Fonte: Microdados ENEM 2025/INEP + Censo Escolar 2025/INEP.",
                "",
                "Dados reais ou nada.",
            ]
        ),
        encoding="utf-8",
    )

    print("PNG:", png)
    for key, path in paths.items():
        print(f"{key.upper()}:", path)
    print("LEGENDA:", legenda)
    print("N_EQUALIZADO:", n_equalizado)


if __name__ == "__main__":
    main()
