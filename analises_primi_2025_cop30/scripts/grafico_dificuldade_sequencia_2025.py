#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráficos XTRI - sequência de dificuldade por área no ENEM 2025.

Fonte obrigatória:
- DADOS/ITENS_PROVA_2025.csv
- analises_primi_2025_cop30/outputs/itens_dificuldade_2025.csv

O CSV de dificuldade já foi calculado a partir do RESULTADOS_2025.csv oficial
validado por CRC contra o ZIP do INEP. A porcentagem de acerto usa todos os
cadernos regulares equivalentes da 1ª aplicação nacional; a sequência visual é
gerada por cor de caderno porque a posição dos itens muda entre cores.
"""

from __future__ import annotations

import json
import math
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analises_primi_2025_cop30" / "outputs"
PNG_DIR = OUT / "dificuldade_sequencia_por_caderno"
ITENS = ROOT / "DADOS" / "ITENS_PROVA_2025.csv"
METRICAS = OUT / "itens_dificuldade_2025.csv"

LOGOS = [
    Path("/Users/home/Desktop/logotipo.png"),
    ROOT / "logo_xtri_marca_real.png",
    OUT / "crop_logo.png",
]

AZUL_XTRI = "#27B8EF"
LARANJA_XTRI = "#FF4E2E"
BG = "#FBFCFE"
PANEL = "#FFFFFF"
INK = "#182032"
MUTED = "#687386"
GRID = "#E3E8F0"

AREA_INFO = {
    "LC": {
        "label": "Linguagens",
        "full": "Linguagens, Códigos e suas Tecnologias",
        "cadernos": {
            "AZUL": "1459",
            "AMARELA": "1460",
            "VERDE": "1461",
            "BRANCA": "1462",
        },
        "base_pos": 1,
    },
    "CH": {
        "label": "Humanas",
        "full": "Ciências Humanas e suas Tecnologias",
        "cadernos": {
            "AZUL": "1447",
            "AMARELA": "1448",
            "BRANCA": "1449",
            "VERDE": "1450",
        },
        "base_pos": 46,
    },
    "CN": {
        "label": "Natureza",
        "full": "Ciências da Natureza e suas Tecnologias",
        "cadernos": {
            "AZUL": "1483",
            "AMARELA": "1484",
            "VERDE": "1485",
            "CINZA": "1486",
        },
        "base_pos": 91,
    },
    "MT": {
        "label": "Matemática",
        "full": "Matemática e suas Tecnologias",
        "cadernos": {
            "AZUL": "1471",
            "AMARELA": "1472",
            "VERDE": "1473",
            "CINZA": "1474",
        },
        "base_pos": 136,
    },
}

CADERNO_SLUG = {
    "AZUL": "azul",
    "AMARELA": "amarela",
    "BRANCA": "branca",
    "VERDE": "verde",
    "CINZA": "cinza",
}

CADERNO_LABEL = {
    "AZUL": "Azul",
    "AMARELA": "Amarela",
    "BRANCA": "Branca",
    "VERDE": "Verde",
    "CINZA": "Cinza",
}

CAT_ORDER = ["Fácil", "Médio", "Difícil", "Muito difícil"]
CAT_STYLE = {
    "Fácil": {"fc": "#D8F4FC", "bar": "#B9EDFB", "ec": AZUL_XTRI, "tc": INK},
    "Médio": {"fc": "#EFF3F8", "bar": "#DCE4EE", "ec": "#B8C2CF", "tc": INK},
    "Difícil": {"fc": "#FFD9CB", "bar": "#FFBCA8", "ec": LARANJA_XTRI, "tc": INK},
    "Muito difícil": {"fc": LARANJA_XTRI, "ec": "#C9361E", "tc": "#FFFFFF"},
    "Anulada": {"fc": "#E7EBF0", "ec": "#AAB3C1", "tc": "#687386"},
}
CAT_STYLE["Muito difícil"]["bar"] = CAT_STYLE["Muito difícil"]["fc"]


def load_logo() -> Image.Image | None:
    """Carrega e recorta o logotipo mantendo transparência."""
    for path in LOGOS:
        if not path.exists():
            continue
        img = Image.open(path).convert("RGBA")
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        return img
    return None


def p_modelo_3pl_theta0(row: pd.Series) -> float:
    """Probabilidade de acerto prevista pela CCI 3PL no theta zero."""
    a = float(row["A"])
    b = float(row["B"])
    c = float(row["C"])
    return c + (1.0 - c) / (1.0 + math.exp(-1.7 * a * (0.0 - b)))


def discr_tier(a: float | None) -> str:
    """Faixa visual de discriminação do item."""
    if a is None or pd.isna(a):
        return "-"
    if a >= 2.5:
        return "A+"
    if a >= 1.35:
        return "A"
    return "A-"


def make_dataset() -> pd.DataFrame:
    """Monta a sequência visual por cor de caderno regular P1."""
    itens = pd.read_csv(ITENS, sep=";", encoding="latin1")
    metricas = pd.read_csv(METRICAS)
    metricas["co_item"] = metricas["co_item"].astype(int)
    metricas["p_emp"] = metricas["pct_acerto"] / 100.0
    metricas["p_modelo_theta0"] = metricas.apply(p_modelo_3pl_theta0, axis=1)
    metricas["dif_xtri"] = 100 * (
        0.65 * (1.0 - metricas["p_modelo_theta0"])
        + 0.35 * (1.0 - metricas["p_emp"])
    )

    rows: list[dict] = []
    for area, info in AREA_INFO.items():
        caderno_codes = set(info["cadernos"].values())
        sub = itens[
            (itens["SG_AREA"] == area)
            & (itens["CO_PROVA"].astype(str).isin(caderno_codes))
        ].copy()
        sub["pos_area"] = sub["CO_POSICAO"] - info["base_pos"] + 1

        for _, row in sub.sort_values(["CO_PROVA", "pos_area", "TP_LINGUA"]).iterrows():
            co_item = int(row["CO_ITEM"])
            hit = metricas.loc[metricas["co_item"] == co_item]
            anulado = int(row["IN_ITEM_ABAN"]) == 1
            base = {
                "area": area,
                "area_label": info["label"],
                "area_full": info["full"],
                "co_prova": int(row["CO_PROVA"]),
                "cor": row["TX_COR"],
                "pos_area": int(row["pos_area"]),
                "co_posicao": int(row["CO_POSICAO"]),
                "co_item": co_item,
                "habilidade": f"H{int(row['CO_HABILIDADE'])}",
                "tp_lingua": row["TP_LINGUA"],
                "lingua_label": "",
                "anulado": anulado,
                "motivo_anulacao": row["TX_MOTIVO_ABAN"] if anulado else "",
                "gab": row["TX_GABARITO"],
            }
            if area == "LC" and pd.notna(row["TP_LINGUA"]):
                base["lingua_label"] = "ING" if int(row["TP_LINGUA"]) == 0 else "ESP"

            if anulado or hit.empty:
                base.update(
                    {
                        "pct_acerto": None,
                        "A": None,
                        "B": None,
                        "C": None,
                        "p_modelo_theta0": None,
                        "dif_xtri": None,
                        "total": None,
                    }
                )
            else:
                h = hit.iloc[0]
                base.update(
                    {
                        "pct_acerto": float(h["pct_acerto"]),
                        "A": float(h["A"]),
                        "B": float(h["B"]),
                        "C": float(h["C"]),
                        "p_modelo_theta0": float(h["p_modelo_theta0"]),
                        "dif_xtri": float(h["dif_xtri"]),
                        "total": int(h["total"]),
                    }
                )
            rows.append(base)

    df = pd.DataFrame(rows)
    df["categoria"] = None
    df["categoria_ordem"] = None
    for area in AREA_INFO:
        valid_items = (
            df[(df["area"] == area) & (~df["anulado"])]
            .drop_duplicates("co_item")
            .copy()
        )
        cats = pd.qcut(
            valid_items["dif_xtri"].rank(method="first"),
            q=4,
            labels=CAT_ORDER,
        ).astype(str)
        cat_by_item = dict(zip(valid_items["co_item"], cats))
        mask = (df["area"] == area) & (~df["anulado"])
        df.loc[mask, "categoria"] = df.loc[mask, "co_item"].map(cat_by_item)
        df.loc[mask, "categoria_ordem"] = df.loc[mask, "categoria"].map(
            {cat: i for i, cat in enumerate(CAT_ORDER)}
        )
    df.loc[df["anulado"], "categoria"] = "Anulada"
    df.loc[df["anulado"], "categoria_ordem"] = -1
    df["discriminacao"] = df["A"].apply(discr_tier)
    return df


def rounded_box(ax, x, y, w, h, fc, ec, lw=1.0, radius=0.018, alpha=1.0):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        alpha=alpha,
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


def draw_chip(ax, x, y, text, fc="#F1F5F9", ec=GRID, color=INK, w=None):
    width = w if w is not None else 0.014 * len(text) + 0.035
    rounded_box(ax, x, y, width, 0.044, fc, ec, lw=1.0, radius=0.018)
    draw_text(ax, x + width / 2, y + 0.022, text, 10.5, color, "bold", "center")
    return width


def draw_area_card(
    area: str,
    df: pd.DataFrame,
    logo: Image.Image | None,
    *,
    caderno_cor: str,
    lc_language: int | None = None,
) -> Path:
    info = AREA_INFO[area]
    caderno_label = CADERNO_LABEL[caderno_cor]
    caderno_slug = CADERNO_SLUG[caderno_cor]
    co_prova = int(info["cadernos"][caderno_cor])
    area_df = df[(df["area"] == area) & (df["co_prova"] == co_prova)].copy()
    lc_language_label = None
    lc_language_slug = None
    if area == "LC" and lc_language is not None:
        lc_language_label = "Inglês" if lc_language == 0 else "Espanhol"
        lc_language_slug = "ingles" if lc_language == 0 else "espanhol"
        is_common = area_df["tp_lingua"].isna()
        is_language = area_df["tp_lingua"].fillna(-1).astype(float).eq(float(lc_language))
        area_df = area_df[is_common | is_language].copy()

    valid = area_df[~area_df["anulado"]].copy()
    presente_n = int(valid["total"].dropna().max())
    anuladas = int(area_df["anulado"].sum())
    valid_slots = area_df.loc[~area_df["anulado"], "pos_area"].nunique()
    counts = (
        valid["categoria"]
        .value_counts()
        .reindex(CAT_ORDER)
        .fillna(0)
        .astype(int)
        .to_dict()
    )

    fig = plt.figure(figsize=(10.8, 13.5), dpi=100)
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    if logo is not None:
        logo_ax = fig.add_axes([0.055, 0.936, 0.064, 0.052])
        logo_ax.axis("off")
        logo_ax.imshow(logo)
    draw_text(ax, 0.128, 0.965, "XTRI ENEM 2025", 18, INK, "bold")
    draw_text(ax, 0.128, 0.943, "Dificuldade por questão · microdados oficiais", 10.5, MUTED)

    title_label = f"{info['label']} · {caderno_label}"
    if lc_language_label:
        title_label = f"{info['label']} · {lc_language_label} · {caderno_label}"
    draw_text(ax, 0.055, 0.884, title_label, 29, INK, "bold")
    subtitle = (
        f"P01-P45 são posições do caderno {caderno_label.lower()} · acerto usa todos os cadernos regulares equivalentes."
    )
    if lc_language_label:
        subtitle = (
            f"Percurso com {lc_language_label}: P01-P05 usam essa língua; "
            f"P06-P45 são comuns no caderno {caderno_label.lower()}."
        )
    draw_text(ax, 0.055, 0.850, subtitle, 12.2, MUTED)

    chip_x = 0.055
    for text in [
        f"N={presente_n:,}".replace(",", "."),
        f"{valid_slots} válidas",
        f"{anuladas} anuladas",
        f"A médio {valid['A'].mean():.2f}".replace(".", ","),
    ]:
        chip_x += draw_chip(ax, chip_x, 0.793, text) + 0.012

    # Distribuição por categoria.
    draw_text(ax, 0.055, 0.779, "Distribuição da área", 12.5, INK, "bold")
    bar_x, bar_y, bar_w, bar_h = 0.055, 0.724, 0.89, 0.030
    total_valid = sum(counts.values())
    cursor = bar_x
    for cat in CAT_ORDER:
        width = bar_w * counts[cat] / total_valid if total_valid else 0
        ax.add_patch(
            Rectangle(
                (cursor, bar_y),
                width,
                bar_h,
                facecolor=CAT_STYLE[cat]["bar"],
                edgecolor=CAT_STYLE[cat]["ec"],
                linewidth=0.8,
            )
        )
        if width > 0.07:
            draw_text(
                ax,
                cursor + width / 2,
                bar_y + bar_h / 2,
                f"{counts[cat]}",
                9.5,
                CAT_STYLE[cat]["tc"] if cat == "Muito difícil" else INK,
                "bold",
                "center",
            )
        cursor += width
    rounded_box(ax, bar_x, bar_y, bar_w, bar_h, "none", "#C9D1DD", lw=1.0, radius=0.01)

    legend_x = 0.055
    for cat in CAT_ORDER:
        style = CAT_STYLE[cat]
        ax.add_patch(
            Rectangle(
                (legend_x, 0.697),
                0.018,
                0.018,
                facecolor=style["fc"],
                edgecolor=style["ec"],
                linewidth=1.0,
            )
        )
        draw_text(ax, legend_x + 0.024, 0.706, f"{cat} ({counts[cat]})", 9.8, INK)
        legend_x += 0.18 if cat != "Muito difícil" else 0.22
    draw_text(ax, 0.735, 0.706, "A+ alta discriminação", 9.8, LARANJA_XTRI, "bold")
    draw_text(ax, 0.900, 0.706, "A- baixa", 9.8, MUTED, "bold")

    # Grade 9 x 5: posições 1 a 45 em ordem de leitura.
    grid_x, grid_y, grid_w, grid_h = 0.055, 0.220, 0.89, 0.445
    cols, rows = 9, 5
    gap_x, gap_y = 0.0065, 0.010
    cell_w = (grid_w - (cols - 1) * gap_x) / cols
    cell_h = (grid_h - (rows - 1) * gap_y) / rows

    for pos in range(1, 46):
        idx = pos - 1
        row_i, col_i = divmod(idx, cols)
        x = grid_x + col_i * (cell_w + gap_x)
        y = grid_y + (rows - 1 - row_i) * (cell_h + gap_y)
        slot = area_df[area_df["pos_area"] == pos].sort_values("lingua_label")

        if slot.empty:
            rounded_box(ax, x, y, cell_w, cell_h, "#F2F4F7", GRID, lw=1.0, radius=0.014)
            draw_text(ax, x + 0.010, y + cell_h - 0.018, f"P{pos:02d}", 8.5, MUTED, "bold")
            continue

        if bool(slot["anulado"].all()):
            style = CAT_STYLE["Anulada"]
            rounded_box(ax, x, y, cell_w, cell_h, style["fc"], style["ec"], lw=1.2, radius=0.014)
            draw_text(ax, x + 0.010, y + cell_h - 0.018, f"P{pos:02d}", 8.5, style["tc"], "bold")
            draw_text(ax, x + cell_w / 2, y + cell_h * 0.55, "ANUL.", 13.2, style["tc"], "bold", "center")
            motivo = str(slot.iloc[0]["motivo_anulacao"] or "")
            motivo = "exp." if "exposto" in motivo.lower() else "conv."
            draw_text(ax, x + cell_w / 2, y + cell_h * 0.30, motivo, 8.5, style["tc"], "bold", "center")
            continue

        # LC combinada: só usada se o script for chamado sem filtro de língua.
        if area == "LC" and len(slot) == 2 and pos <= 5:
            rounded_box(ax, x, y, cell_w, cell_h, PANEL, GRID, lw=1.1, radius=0.014)
            draw_text(ax, x + cell_w / 2, y + cell_h - 0.011, f"P{pos:02d}", 7.8, MUTED, "bold", "center")
            lang_rows = slot.sort_values("tp_lingua").reset_index(drop=True)
            header_h = 0.020
            inner_y = y + 0.006
            inner_h = cell_h - header_h - 0.010
            band_gap = 0.004
            band_h = (inner_h - band_gap) / 2
            for j, rec in lang_rows.iterrows():
                band_y = inner_y + (band_h + band_gap) * (1 - j)
                cat = rec["categoria"]
                style = CAT_STYLE[cat]
                ax.add_patch(
                    Rectangle(
                        (x + 0.006, band_y),
                        cell_w - 0.012,
                        band_h,
                        facecolor=style["fc"],
                        edgecolor=style["ec"],
                        linewidth=0.8,
                    )
                )
                txt = style["tc"]
                label = rec["lingua_label"] or "LC"
                tag_w = 0.027
                ax.add_patch(
                    Rectangle(
                        (x + 0.006, band_y),
                        tag_w,
                        band_h,
                        facecolor=PANEL if cat != "Muito difícil" else "#FF725B",
                        edgecolor=style["ec"],
                        linewidth=0.6,
                    )
                )
                tag_color = style["ec"] if cat != "Muito difícil" else "#FFFFFF"
                draw_text(ax, x + 0.006 + tag_w / 2, band_y + band_h * 0.52, label, 5.7, tag_color, "bold", "center")
                draw_text(ax, x + 0.039, band_y + band_h * 0.56, rec["habilidade"], 9.8, txt, "bold")
                draw_text(ax, x + cell_w - 0.010, band_y + band_h * 0.68, rec["discriminacao"], 5.9, txt, "bold", "right")
                draw_text(ax, x + cell_w - 0.010, band_y + band_h * 0.28, f"{rec['pct_acerto']:.0f}%", 6.5, txt, "bold", "right")
            continue

        rec = slot.iloc[0]
        cat = rec["categoria"]
        style = CAT_STYLE[cat]
        tier = rec["discriminacao"]
        lw = 2.1 if tier == "A+" else 1.15
        rounded_box(ax, x, y, cell_w, cell_h, style["fc"], style["ec"], lw=lw, radius=0.014)
        txt = style["tc"]
        draw_text(ax, x + 0.010, y + cell_h - 0.018, f"P{pos:02d}", 8.5, txt, "bold")
        draw_text(ax, x + cell_w - 0.010, y + cell_h - 0.018, tier, 8.5, txt, "bold", "right")
        draw_text(ax, x + cell_w / 2, y + cell_h * 0.56, rec["habilidade"], 17.5, txt, "bold", "center")
        draw_text(ax, x + cell_w / 2, y + cell_h * 0.31, f"{rec['pct_acerto']:.0f}% acerto", 8.7, txt, "bold", "center")
        draw_text(ax, x + cell_w / 2, y + cell_h * 0.14, f"DIF {rec['dif_xtri']:.0f}", 7.6, txt, "bold", "center")

    # Rodapé analítico.
    top_a = valid.sort_values("A", ascending=False).head(3)
    ranking_bits = [
        f"P{int(r.pos_area):02d} {r.habilidade} a={r.A:.2f} p={r.pct_acerto:.0f}%"
        for r in top_a.itertuples()
    ]
    rounded_box(ax, 0.055, 0.126, 0.89, 0.066, PANEL, GRID, lw=1.0, radius=0.020)
    draw_text(ax, 0.075, 0.172, "Maior poder discriminativo na sequência", 11.5, INK, "bold")
    draw_text(ax, 0.075, 0.148, " · ".join(ranking_bits), 10.5, MUTED)

    note = (
        "DIF_XTRI = 65% erro previsto pela CCI 3PL no θ=0 (A, B, C oficiais) + "
        "35% erro real dos presentes na área. As faixas são quartis dentro da área."
    )
    draw_text(ax, 0.055, 0.086, textwrap.fill(note, width=126), 9.0, MUTED)
    draw_text(
        ax,
        0.055,
        0.054,
        "Fonte: Microdados ENEM 2025 / INEP · RESULTADOS_2025.csv + ITENS_PROVA_2025.csv · regular P1 nacional.",
        8.6,
        MUTED,
    )
    draw_text(
        ax,
        0.055,
        0.038,
        f"Posição no caderno {caderno_label.lower()} · acerto por área; não exige 4 áreas válidas.",
        8.6,
        MUTED,
    )
    draw_text(ax, 0.945, 0.020, "Dados reais ou nada.", 10.5, LARANJA_XTRI, "bold", "right")

    suffix = f"{area}_{caderno_slug}" if lc_language_slug is None else f"{area}_{lc_language_slug}_{caderno_slug}"
    path = PNG_DIR / f"xtri_enem_2025_dificuldade_sequencia_{suffix}.png"
    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    df = make_dataset()
    csv_path = OUT / "itens_sequencia_dificuldade_2025.csv"
    df.to_csv(csv_path, index=False)

    resumo = {
        "fonte": "Microdados ENEM 2025 / INEP",
        "populacao": "ENEM Regular P1 nacional; presentes na área analisada",
        "cadernos_calculo_acerto": {
            "CN": ["1483", "1484", "1485", "1486"],
            "CH": ["1447", "1448", "1449", "1450"],
            "LC": ["1459", "1460", "1461", "1462"],
            "MT": ["1471", "1472", "1473", "1474"],
        },
        "sequencia_visual": "gerada separadamente por cor de caderno; P01-P45 são posições, não identificadores universais de item",
        "criterio_presenca": "TP_PRESENCA da área == 1; não exige presença/notas válidas nas 4 áreas",
        "metrica": (
            "DIF_XTRI = 65% erro previsto pela CCI 3PL no theta=0 "
            "(A, B, C oficiais) + 35% erro real observado"
        ),
        "categorias": "quartis de DIF_XTRI dentro de cada área; anuladas sem categoria",
        "discriminacao": "A+ se A>=2.5; A se 1.35<=A<2.5; A- se A<1.35",
        "areas": {},
    }
    logo = load_logo()
    paths = []
    for area in ["LC", "CH", "CN", "MT"]:
        area_df = df[df["area"] == area]
        valid = area_df[~area_df["anulado"]].drop_duplicates("co_item")
        anuladas_unicas = area_df[area_df["anulado"]].drop_duplicates("co_item")
        resumo["areas"][area] = {
            "label": AREA_INFO[area]["full"],
            "cadernos": AREA_INFO[area]["cadernos"],
            "presentes": int(valid["total"].dropna().max()),
            "itens_validos": int(len(valid)),
            "anuladas": int(len(anuladas_unicas)),
            "distribuicao": (
                valid["categoria"].value_counts().reindex(CAT_ORDER).fillna(0).astype(int).to_dict()
            ),
            "media_A": round(float(valid["A"].mean()), 4),
            "media_B": round(float(valid["B"].mean()), 4),
            "media_pct_acerto": round(float(valid["pct_acerto"].mean()), 4),
            "top_A": [
                {
                    "pos_area": int(r.pos_area),
                    "habilidade": r.habilidade,
                    "co_item": int(r.co_item),
                    "A": round(float(r.A), 5),
                    "B": round(float(r.B), 5),
                    "pct_acerto": round(float(r.pct_acerto), 2),
                    "dif_xtri": round(float(r.dif_xtri), 2),
                }
                for r in valid.sort_values("A", ascending=False).head(5).itertuples()
            ],
        }
        for caderno_cor in AREA_INFO[area]["cadernos"]:
            if area == "LC":
                paths.append(draw_area_card(area, df, logo, caderno_cor=caderno_cor, lc_language=0))
                paths.append(draw_area_card(area, df, logo, caderno_cor=caderno_cor, lc_language=1))
            else:
                paths.append(draw_area_card(area, df, logo, caderno_cor=caderno_cor))

    resumo["arquivos"] = [str(p) for p in paths]
    json_path = OUT / "auditoria_sequencia_dificuldade_2025.json"
    json_path.write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    legenda = OUT / "legenda_feed_dificuldade_sequencia_2025.md"
    legenda.write_text(
        "\n".join(
            [
                "# Legenda - Dificuldade por questão ENEM 2025",
                "",
                "Cada card mostra a sequência de uma cor de caderno da 1ª aplicação regular.",
                "`P01-P45` são posições naquela cor de caderno, não identificadores universais da questão.",
                "A porcentagem de acerto foi calculada usando todos os cadernos regulares equivalentes da área.",
                "O denominador é presença válida na área analisada, não presença válida nas 4 áreas.",
                "Em Linguagens, gerei duas versões por cor: percurso com Inglês e percurso com Espanhol, porque P01-P05 dependem da língua escolhida.",
                "A cor indica a faixa relativa de dificuldade dentro da área: fácil, médio, difícil e muito difícil.",
                "",
                "A métrica cruza os parâmetros oficiais dos itens com o desempenho real dos participantes:",
                "`DIF_XTRI = 65% erro previsto pela CCI 3PL no θ=0 + 35% erro real observado`.",
                "",
                "O selo `A+` marca itens com maior poder discriminativo: são questões que tendem a separar melhor candidatos próximos ao nível de dificuldade do item.",
                "",
                "Fonte: Microdados ENEM 2025 / INEP. Questões anuladas aparecem em cinza e não entram na classificação.",
            ]
        ),
        encoding="utf-8",
    )

    print("CSV:", csv_path)
    print("JSON:", json_path)
    for path in paths:
        print("PNG:", path)


if __name__ == "__main__":
    main()
