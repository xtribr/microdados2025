#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparativo ENEM 2025 - 54 alunos por escola em Natal/RN.

Recorte:
- Colégio Ciências Aplicadas: todos os alunos com as 5 notas válidas.
- Colégio Porto, CEI S/A Romualdo e Marista de Natal: 54 melhores por média
  simples das 5 notas (CN, CH, LC, MT e Redação).

O script não exporta identificadores individuais do ENEM. A base de alunos
selecionados recebe IDs locais por escola, suficientes para auditar a
distribuição sem expor o identificador original.
"""

from __future__ import annotations

import json
import zipfile
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

ESCOLAS = {
    24097004: {
        "slug": "CCA",
        "nome_curto": "Ciências Aplicadas",
        "criterio": "todos_5_notas",
        "cor": "#FF4E2E",
    },
    24088846: {
        "slug": "PORTO",
        "nome_curto": "Colégio Porto",
        "criterio": "top_54_media_5",
        "cor": "#27B8EF",
    },
    24069191: {
        "slug": "CEI_SA",
        "nome_curto": "CEI S/A Romualdo",
        "criterio": "top_54_media_5",
        "cor": "#3CBF7B",
    },
    24057134: {
        "slug": "MARISTA",
        "nome_curto": "Marista de Natal",
        "criterio": "top_54_media_5",
        "cor": "#F5B43F",
    },
}

CODIGO_CEI_MAIS_NAO_USADO = 24350303
NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
PRESENCAS = ["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]
AREA_LABELS = {
    "NU_NOTA_CN": "Natureza",
    "NU_NOTA_CH": "Humanas",
    "NU_NOTA_LC": "Linguagens",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_REDACAO": "Redação",
}

BG = "#FBFCFE"
PANEL = "#FFFFFF"
PANEL_SOFT = "#F3F6FA"
INK = "#182032"
MUTED = "#687386"
GRID = "#E3E8F0"
XTRI_BLUE = "#27B8EF"
XTRI_ORANGE = "#FF4E2E"


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


def fmt_num(value: float, casas: int = 1) -> str:
    return f"{value:.{casas}f}".replace(".", ",")


def read_censo_escolas() -> pd.DataFrame:
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
        "NU_ENDERECO",
        "NO_BAIRRO",
        "CO_CEP",
        "IN_COMUM_MEDIO_MEDIO",
    ]
    wanted = list(ESCOLAS.keys()) + [CODIGO_CEI_MAIS_NAO_USADO]
    frames: list[pd.DataFrame] = []
    with zipfile.ZipFile(CENSO_ZIP) as zf, zf.open(CENSO_ESCOLAS) as fp:
        for chunk in pd.read_csv(fp, sep=";", encoding="latin1", usecols=usecols, chunksize=50_000):
            sub = chunk[chunk["CO_ENTIDADE"].isin(wanted)].copy()
            if not sub.empty:
                frames.append(sub)
    if not frames:
        raise RuntimeError("Nenhuma escola alvo encontrada no Censo Escolar 2025.")
    return pd.concat(frames, ignore_index=True)


def read_enem_pool() -> pd.DataFrame:
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
    frames: list[pd.DataFrame] = []
    wanted = set(ESCOLAS.keys()) | {CODIGO_CEI_MAIS_NAO_USADO}
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
        raise RuntimeError("Nenhum candidato encontrado para os códigos-alvo em Natal/RN.")
    df = pd.concat(frames, ignore_index=True)
    for col in ["CO_ESCOLA", "CO_MUNICIPIO_ESC", "TP_STATUS_REDACAO", *PRESENCAS]:
        df[col] = df[col].astype("Int64")
    return df


def build_selected(pool_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid = pool_raw.dropna(subset=NOTAS).copy()
    for col in PRESENCAS:
        valid = valid[valid[col].eq(1)].copy()
    valid = valid[valid["TP_STATUS_REDACAO"].eq(1)].copy()
    valid["MEDIA_4_TRI"] = valid[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"]].mean(axis=1)
    valid["MEDIA_5"] = valid[NOTAS].mean(axis=1)

    selected_parts: list[pd.DataFrame] = []
    pool_parts: list[pd.DataFrame] = []

    for codigo, meta in ESCOLAS.items():
        school = valid[valid["CO_ESCOLA"].eq(codigo)].copy()
        school = school.sort_values(
            ["MEDIA_5", "MEDIA_4_TRI", "NU_NOTA_REDACAO", "NU_NOTA_MT"],
            ascending=False,
        ).reset_index(drop=True)
        school["RANK_POOL"] = np.arange(1, len(school) + 1)
        pool_parts.append(school.assign(ESCOLA=meta["nome_curto"], SLUG=meta["slug"]))

        if meta["criterio"] == "todos_5_notas":
            selected = school.copy()
        else:
            selected = school.head(54).copy()
        selected["RANK_AMOSTRA"] = np.arange(1, len(selected) + 1)
        selected["ESCOLA"] = meta["nome_curto"]
        selected["SLUG"] = meta["slug"]
        selected["CRITERIO_AMOSTRA"] = meta["criterio"]
        selected_parts.append(selected)

    selected_df = pd.concat(selected_parts, ignore_index=True)
    pool_df = pd.concat(pool_parts, ignore_index=True)

    # Exporta sem identificador original. O ID local depende só do ranking da amostra.
    selected_df["ALUNO_ID_LOCAL"] = selected_df.apply(
        lambda r: f"{r['SLUG']}_{int(r['RANK_AMOSTRA']):03d}", axis=1
    )
    return pool_df, selected_df


def summarize(pool_df: pd.DataFrame, selected_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for codigo, meta in ESCOLAS.items():
        pool = pool_df[pool_df["CO_ESCOLA"].eq(codigo)]
        sel = selected_df[selected_df["CO_ESCOLA"].eq(codigo)]
        row = {
            "codigo_inep": codigo,
            "escola": meta["nome_curto"],
            "criterio_amostra": meta["criterio"],
            "n_pool_5_notas": int(len(pool)),
            "n_amostra": int(len(sel)),
            "media_5": float(sel["MEDIA_5"].mean()),
            "mediana_5": float(sel["MEDIA_5"].median()),
            "dp_5": float(sel["MEDIA_5"].std(ddof=1)),
            "p25_5": float(sel["MEDIA_5"].quantile(0.25)),
            "p75_5": float(sel["MEDIA_5"].quantile(0.75)),
            "min_5": float(sel["MEDIA_5"].min()),
            "max_5": float(sel["MEDIA_5"].max()),
            "media_4_tri": float(sel["MEDIA_4_TRI"].mean()),
        }
        for nota in NOTAS:
            row[f"media_{nota.replace('NU_NOTA_', '').lower()}"] = float(sel[nota].mean())
        rows.append(row)
    summary = pd.DataFrame(rows)
    cca_mean = float(summary.loc[summary["codigo_inep"].eq(24097004), "media_5"].iloc[0])
    summary["delta_media_5_vs_cca"] = summary["media_5"] - cca_mean
    return summary.sort_values("media_5", ascending=False).reset_index(drop=True)


def save_outputs(censo_df: pd.DataFrame, pool_df: pd.DataFrame, selected_df: pd.DataFrame, summary: pd.DataFrame) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)

    censo_path = OUT / "escolas_natal_censo_2025_codigos.csv"
    pool_path = OUT / "comparativo_escolas_natal_2025_pool_5notas.csv"
    selected_path = OUT / "comparativo_escolas_natal_2025_amostra_54x54.csv"
    summary_path = OUT / "comparativo_escolas_natal_2025_resumo.csv"
    audit_path = OUT / "auditoria_comparativo_escolas_natal_2025_5notas.json"

    censo_df.to_csv(censo_path, index=False)

    pool_public = pool_df[
        [
            "SLUG",
            "ESCOLA",
            "CO_ESCOLA",
            "RANK_POOL",
            "MEDIA_5",
            "MEDIA_4_TRI",
            *NOTAS,
        ]
    ].copy()
    pool_public.to_csv(pool_path, index=False)

    selected_public = selected_df[
        [
            "ALUNO_ID_LOCAL",
            "SLUG",
            "ESCOLA",
            "CO_ESCOLA",
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

    audit = {
        "fonte_enem": str(RESULTADOS),
        "fonte_censo_escolar_2025": str(CENSO_ZIP),
        "fonte_censo_url": "https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip",
        "recorte": "Natal/RN; escolas privadas com Ensino Medio no Censo 2025; ENEM 2025",
        "criterio_5_notas": {
            "presenca": "TP_PRESENCA_CN/CH/LC/MT == 1",
            "redacao": "TP_STATUS_REDACAO == 1",
            "notas_obrigatorias": NOTAS,
        },
        "criterio_ranking": "media simples das 5 notas; desempate por MEDIA_4_TRI, Redacao e Matematica",
        "criterio_amostra": {
            "COLEGIO CIENCIAS APLICADAS": "todos os 54 alunos com 5 notas",
            "demais_escolas": "54 melhores por MEDIA_5",
        },
        "codigos_usados": {str(k): v["nome_curto"] for k, v in ESCOLAS.items()},
        "codigo_cei_mais_nao_usado": {
            "codigo": CODIGO_CEI_MAIS_NAO_USADO,
            "motivo": "usuario pediu Centro de Educacao Integrada S A; codigo 24350303 e CEI Mais Ltda",
        },
        "n_pool_5_notas_por_escola": summary.set_index("escola")["n_pool_5_notas"].astype(int).to_dict(),
        "n_amostra_por_escola": summary.set_index("escola")["n_amostra"].astype(int).to_dict(),
        "arquivos": {
            "censo_escolas": str(censo_path),
            "pool_5_notas": str(pool_path),
            "amostra_54x54": str(selected_path),
            "resumo": str(summary_path),
        },
    }
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "censo": censo_path,
        "pool": pool_path,
        "selected": selected_path,
        "summary": summary_path,
        "audit": audit_path,
    }


def make_feed(summary: pd.DataFrame, selected_df: pd.DataFrame) -> Path:
    W, H = 1080, 1350
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    canvas = fig.add_axes([0, 0, 1, 1])
    canvas.set_axis_off()
    canvas.set_xlim(0, 1)
    canvas.set_ylim(0, 1)

    logo = load_logo()
    if logo is not None:
        logo_ax = fig.add_axes([0.055, 0.934, 0.064, 0.054])
        logo_ax.axis("off")
        logo_ax.imshow(logo)
    draw_text(canvas, 0.128, 0.965, "XTRI ENEM 2025", 18, INK, "bold")
    draw_text(canvas, 0.128, 0.943, "Estudo 54 x 54 · Natal/RN · microdados oficiais", 10.5, MUTED)

    draw_text(canvas, 0.055, 0.895, "Quem segura o topo?", 31, INK, "bold")
    draw_text(
        canvas,
        0.055,
        0.868,
        "Ciências Aplicadas inteiro contra os 54 melhores de Porto, CEI S/A e Marista.",
        12.4,
        MUTED,
    )

    chips = [
        ("Ranking: média das 5 notas", 0.055, 0.815, 0.255),
        ("Redação válida + 4 TRI", 0.325, 0.815, 0.225),
        ("Natal/RN · 2025", 0.565, 0.815, 0.180),
        ("N = 216", 0.760, 0.815, 0.140),
    ]
    for text, x, y, w in chips:
        rounded_box(canvas, x, y, w, 0.040, "#F1F5F9", GRID, lw=1, radius=0.016)
        draw_text(canvas, x + w / 2, y + 0.020, text, 9.9, INK, "bold", "center")

    ordered = summary.sort_values("media_5", ascending=False).copy()
    colors = [ESCOLAS[int(r.codigo_inep)]["cor"] for _, r in ordered.iterrows()]

    # Painel de distribuição.
    ax_box = fig.add_axes([0.070, 0.485, 0.470, 0.270])
    ax_box.set_facecolor(BG)
    box_data = [
        selected_df[selected_df["CO_ESCOLA"].eq(int(row.codigo_inep))]["MEDIA_5"].to_numpy()
        for _, row in ordered.iterrows()
    ]
    bp = ax_box.boxplot(
        box_data,
        patch_artist=True,
        widths=0.56,
        medianprops={"color": INK, "linewidth": 2},
        whiskerprops={"color": MUTED, "linewidth": 1.2},
        capprops={"color": MUTED, "linewidth": 1.2},
        flierprops={"marker": "o", "markersize": 3, "markerfacecolor": "none", "markeredgecolor": MUTED},
    )
    rng = np.random.default_rng(20250625)
    for idx, (box, cor, vals, (_, row)) in enumerate(zip(bp["boxes"], colors, box_data, ordered.iterrows()), start=1):
        box.set(facecolor=cor, alpha=0.20, edgecolor=cor, linewidth=1.6)
        xs = rng.normal(idx, 0.045, len(vals))
        ax_box.scatter(xs, vals, s=11, color=cor, alpha=0.55, edgecolor="none", zorder=3)
        ax_box.text(idx, row.media_5 + 2, fmt_num(row.media_5), ha="center", va="bottom", fontsize=9.4, color=INK, fontweight="bold")
    ax_box.set_title("Distribuição da média das 5 notas", loc="left", fontsize=12.4, color=INK, fontweight="bold", pad=8)
    ax_box.set_xticks(range(1, len(ordered) + 1))
    ax_box.set_xticklabels([r.escola.replace(" ", "\n") for _, r in ordered.iterrows()], fontsize=8.9, color=INK)
    ax_box.tick_params(axis="y", colors=MUTED, labelsize=9.0, length=0)
    ax_box.tick_params(axis="x", length=0)
    ax_box.grid(axis="y", color=GRID, linewidth=1)
    ax_box.set_axisbelow(True)
    for side in ["top", "right"]:
        ax_box.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax_box.spines[side].set_color(GRID)
    ax_box.set_ylabel("média simples CN+CH+LC+MT+Red", fontsize=9.2, color=MUTED)

    # Painel de médias por área.
    ax_bar = fig.add_axes([0.602, 0.485, 0.345, 0.270])
    ax_bar.set_facecolor(BG)
    areas = NOTAS
    x = np.arange(len(areas))
    width = 0.18
    for i, (_, row) in enumerate(ordered.iterrows()):
        vals = [row[f"media_{nota.replace('NU_NOTA_', '').lower()}"] for nota in areas]
        ax_bar.bar(x + (i - 1.5) * width, vals, width=width, color=ESCOLAS[int(row.codigo_inep)]["cor"], alpha=0.86)
    ax_bar.set_title("Média por nota", loc="left", fontsize=12.4, color=INK, fontweight="bold", pad=8)
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(["CN", "CH", "LC", "MT", "Red"], fontsize=9.6, color=INK)
    ax_bar.tick_params(axis="y", colors=MUTED, labelsize=9.0, length=0)
    ax_bar.tick_params(axis="x", length=0)
    ax_bar.grid(axis="y", color=GRID, linewidth=1)
    ax_bar.set_axisbelow(True)
    ax_bar.set_ylim(580, 950)
    for side in ["top", "right"]:
        ax_bar.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax_bar.spines[side].set_color(GRID)

    # Tabela resumo.
    rounded_box(canvas, 0.055, 0.138, 0.890, 0.300, PANEL_SOFT, GRID, lw=1, radius=0.020)
    headers = ["Escola", "Pool", "Amostra", "Média 5", "Mediana", "4 TRI", "Redação", "Δ vs CCA"]
    colx = [0.078, 0.312, 0.398, 0.514, 0.625, 0.726, 0.817, 0.914]
    for h, xh in zip(headers, colx):
        draw_text(canvas, xh, 0.410, h, 9.5, MUTED, "bold", ha="center" if h != "Escola" else "left")
    canvas.plot([0.075, 0.925], [0.386, 0.386], color=GRID, lw=1)

    row_y = [0.345, 0.295, 0.245, 0.195]
    for y, (_, row) in zip(row_y, ordered.iterrows()):
        code = int(row.codigo_inep)
        cor = ESCOLAS[code]["cor"]
        draw_text(canvas, 0.078, y, "●", 11.7, cor, "bold")
        draw_text(canvas, 0.094, y, str(row.escola), 10.2, INK, "bold")
        draw_text(canvas, 0.312, y, str(int(row.n_pool_5_notas)), 10.0, INK, ha="center")
        amostra = "todos 54" if code == 24097004 else "top 54"
        draw_text(canvas, 0.398, y, amostra, 9.6, INK, ha="center")
        draw_text(canvas, 0.514, y, fmt_num(row.media_5), 10.8, INK, "bold", ha="center")
        draw_text(canvas, 0.625, y, fmt_num(row.mediana_5), 10.0, INK, ha="center")
        draw_text(canvas, 0.726, y, fmt_num(row.media_4_tri), 10.0, INK, ha="center")
        draw_text(canvas, 0.817, y, fmt_num(row.media_redacao), 10.0, INK, ha="center")
        delta = float(row.delta_media_5_vs_cca)
        delta_txt = "base" if code == 24097004 else ("+" if delta >= 0 else "") + fmt_num(delta)
        delta_color = XTRI_ORANGE if code == 24097004 else (INK if abs(delta) < 0.05 else ("#1F9D63" if delta > 0 else XTRI_ORANGE))
        draw_text(canvas, 0.914, y, delta_txt, 10.0, delta_color, "bold", ha="center")

    rounded_box(canvas, 0.055, 0.058, 0.890, 0.067, "#FFFFFF", GRID, lw=1, radius=0.018)
    draw_text(canvas, 0.075, 0.107, "Leitura correta", 11.2, INK, "bold")
    draw_text(
        canvas,
        0.075,
        0.084,
        "Comparação de coortes: CCA completo contra recorte top 54 das demais escolas; não é ranking geral bruto.",
        9.0,
        MUTED,
    )
    draw_text(
        canvas,
        0.075,
        0.044,
        "Fonte: Microdados ENEM 2025/INEP + Censo Escolar 2025/INEP · alunos com 4 TRI e redação válida.",
        8.9,
        MUTED,
    )
    draw_text(canvas, 0.945, 0.023, "Dados reais ou nada.", 10.5, XTRI_ORANGE, "bold", "right")

    png_path = OUT / "comparativo_escolas_natal_2025_54x54_feed.png"
    fig.savefig(png_path, dpi=100, facecolor=BG)
    plt.close(fig)
    return png_path


def main() -> None:
    censo_df = read_censo_escolas()
    pool_raw = read_enem_pool()
    pool_df, selected_df = build_selected(pool_raw)
    summary = summarize(pool_df, selected_df)
    paths = save_outputs(censo_df, pool_df, selected_df, summary)
    png = make_feed(summary, selected_df)

    legenda = OUT / "legenda_comparativo_escolas_natal_2025_54x54.md"
    legenda.write_text(
        "\n".join(
            [
                "# Legenda - Comparativo 54 x 54 ENEM 2025 Natal/RN",
                "",
                "Estudo com dados reais dos Microdados ENEM 2025/INEP.",
                "",
                "O recorte compara o Colégio Ciências Aplicadas inteiro, com seus 54 alunos com as 5 notas válidas, contra os 54 melhores alunos de Colégio Porto, CEI S/A Romualdo e Marista de Natal.",
                "",
                "Critério: alunos de Natal/RN, escola de conclusão do ensino médio informada, presença nas quatro áreas objetivas, redação válida e notas em CN, CH, LC, MT e Redação.",
                "",
                "Ranking dos 54 melhores: média simples das 5 notas. Desempate: média das 4 TRI, Redação e Matemática.",
                "",
                "Importante: isso não é ranking geral bruto das escolas. É um estudo de comparação de coortes: uma escola inteira versus o topo de outras três escolas.",
                "",
                "Fonte adicional para validação dos códigos INEP das escolas: Microdados do Censo Escolar 2025/INEP.",
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


if __name__ == "__main__":
    main()
