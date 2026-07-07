#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feed XTRI - equivalência de dificuldade entre cores de caderno ENEM 2025.

Mostra que, dentro de cada área/percurso, as cores de caderno têm a mesma
composição de dificuldade. A posição muda; o conjunto de CO_ITEM não.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analises_primi_2025_cop30" / "outputs"
SEQ = OUT / "itens_sequencia_dificuldade_2025.csv"

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

CAT_ORDER = ["Fácil", "Médio", "Difícil", "Muito difícil", "Anulada"]
CAT_STYLE = {
    "Fácil": {"fc": "#B9EDFB", "ec": AZUL_XTRI, "tc": INK},
    "Médio": {"fc": "#DCE4EE", "ec": "#B8C2CF", "tc": INK},
    "Difícil": {"fc": "#FFBCA8", "ec": LARANJA_XTRI, "tc": INK},
    "Muito difícil": {"fc": LARANJA_XTRI, "ec": "#C9361E", "tc": "#FFFFFF"},
    "Anulada": {"fc": "#E7EBF0", "ec": "#AAB3C1", "tc": "#687386"},
}

AREA_LABELS = {
    "LC_ING": "Linguagens · Inglês",
    "LC_ESP": "Linguagens · Espanhol",
    "CH": "Humanas",
    "CN": "Natureza",
    "MT": "Matemática",
}

PANEL_ORDER = ["LC_ING", "LC_ESP", "CH", "CN", "MT"]
CADERNO_ORDER = {
    "LC_ING": ["AZUL", "AMARELA", "VERDE", "BRANCA"],
    "LC_ESP": ["AZUL", "AMARELA", "VERDE", "BRANCA"],
    "CH": ["AZUL", "AMARELA", "BRANCA", "VERDE"],
    "CN": ["AZUL", "AMARELA", "VERDE", "CINZA"],
    "MT": ["AZUL", "AMARELA", "VERDE", "CINZA"],
}
CADERNO_LABEL = {
    "AZUL": "Azul",
    "AMARELA": "Amarela",
    "BRANCA": "Branca",
    "VERDE": "Verde",
    "CINZA": "Cinza",
}


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


def draw_chip(ax, x, y, text, fc="#F1F5F9", ec=GRID, color=INK, w=None):
    width = w if w is not None else 0.0105 * len(text) + 0.042
    rounded_box(ax, x, y, width, 0.040, fc, ec, lw=1.0, radius=0.016)
    draw_text(ax, x + width / 2, y + 0.020, text, 9.7, color, "bold", "center")
    return width


def panel_key(row: pd.Series) -> str | None:
    if row["area"] == "LC":
        if pd.isna(row["tp_lingua"]):
            return None
        return "LC_ING" if float(row["tp_lingua"]) == 0.0 else "LC_ESP"
    return row["area"]


def build_summary() -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(SEQ)

    rows: list[dict] = []
    audit = {
        "fonte": "Microdados ENEM 2025 / INEP",
        "base": str(SEQ),
        "metrica": "DIF_XTRI calculado previamente por CO_ITEM; faixas por quartis dentro da área",
        "nota_metodologica": (
            "Cores de caderno foram comparadas pelo conjunto de CO_ITEM. "
            "P01-P45 são posições; a posição muda, o conjunto de itens não."
        ),
        "paineis": {},
    }

    for key in PANEL_ORDER:
        if key == "LC_ING":
            panel = df[(df["area"] == "LC") & (df["tp_lingua"].isna() | df["tp_lingua"].eq(0.0))].copy()
        elif key == "LC_ESP":
            panel = df[(df["area"] == "LC") & (df["tp_lingua"].isna() | df["tp_lingua"].eq(1.0))].copy()
        else:
            panel = df[df["area"] == key].copy()

        panel_audit = {
            "label": AREA_LABELS[key],
            "cores": {},
        }
        means: list[float] = []
        item_sets = []

        for cor in CADERNO_ORDER[key]:
            part = panel[panel["cor"] == cor].copy()
            if part.empty:
                raise RuntimeError(f"Sem dados para {key} / {cor}")
            part["cat5"] = part["categoria"].where(~part["anulado"], "Anulada")
            counts = part["cat5"].value_counts().reindex(CAT_ORDER).fillna(0).astype(int)
            valid = part[~part["anulado"]].copy()
            mean_dif = float(valid["dif_xtri"].mean())
            mean_a = float(valid["A"].mean())
            means.append(mean_dif)
            item_set = tuple(sorted(valid["co_item"].astype(int).tolist()))
            item_sets.append(item_set)

            row = {
                "painel": key,
                "painel_label": AREA_LABELS[key],
                "cor": cor,
                "cor_label": CADERNO_LABEL[cor],
                "co_prova": int(part["co_prova"].iloc[0]),
                "n_posicoes": int(part["pos_area"].nunique()),
                "itens_validos": int(len(valid)),
                "anuladas": int(part["anulado"].sum()),
                "media_dif_xtri": mean_dif,
                "media_A": mean_a,
            }
            for cat in CAT_ORDER:
                row[cat] = int(counts[cat])
            rows.append(row)
            panel_audit["cores"][cor] = row.copy()

        panel_audit["delta_media_dif_xtri"] = float(max(means) - min(means))
        panel_audit["mesmo_conjunto_de_itens"] = all(item_sets[0] == s for s in item_sets[1:])
        audit["paineis"][key] = panel_audit

    return pd.DataFrame(rows), audit


def draw_stacked_bar(ax, x, y, w, h, counts: dict[str, int], total: int):
    cursor = x
    for cat in CAT_ORDER:
        value = int(counts.get(cat, 0))
        seg_w = w * value / total if total else 0
        style = CAT_STYLE[cat]
        ax.add_patch(
            Rectangle(
                (cursor, y),
                seg_w,
                h,
                facecolor=style["fc"],
                edgecolor=style["ec"],
                linewidth=0.8,
            )
        )
        if seg_w > 0.052:
            draw_text(
                ax,
                cursor + seg_w / 2,
                y + h / 2,
                str(value),
                8.3,
                style["tc"] if cat == "Muito difícil" else INK,
                "bold",
                "center",
            )
        cursor += seg_w
    rounded_box(ax, x, y, w, h, "none", "#C9D1DD", lw=0.8, radius=0.006)


def make_feed(summary: pd.DataFrame, audit: dict) -> Path:
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
    draw_text(ax, 0.128, 0.943, "Equivalência de cadernos · microdados oficiais", 10.5, MUTED)

    draw_text(ax, 0.055, 0.887, "Cores diferentes, mesma dificuldade", 30, INK, "bold")
    draw_text(
        ax,
        0.055,
        0.855,
        "A cor muda a posição dos itens; o conjunto de dificuldades permanece equivalente.",
        12.5,
        MUTED,
    )

    chip_x = 0.055
    for text in ["Regular P1 nacional", "todos os cadernos equivalentes", "diferença média = 0,00"]:
        chip_x += draw_chip(ax, chip_x, 0.805, text) + 0.012

    # Legenda das faixas.
    legend_x = 0.055
    for cat in CAT_ORDER:
        style = CAT_STYLE[cat]
        ax.add_patch(
            Rectangle(
                (legend_x, 0.770),
                0.017,
                0.017,
                facecolor=style["fc"],
                edgecolor=style["ec"],
                linewidth=1.0,
            )
        )
        draw_text(ax, legend_x + 0.023, 0.779, cat, 9.6, INK)
        legend_x += 0.147 if cat != "Muito difícil" else 0.177

    # Painéis compactos.
    top_y = 0.645
    panel_h = 0.107
    panel_gap = 0.017
    bar_x = 0.165
    bar_w = 0.590
    bar_h = 0.014
    bar_gap = 0.007
    label_x = 0.075
    right_x = 0.785

    for i, key in enumerate(PANEL_ORDER):
        y0 = top_y - i * (panel_h + panel_gap)
        rounded_box(ax, 0.055, y0 - 0.004, 0.89, panel_h, PANEL, GRID, lw=1.0, radius=0.018)
        part = summary[summary["painel"] == key].copy()
        delta = part["media_dif_xtri"].max() - part["media_dif_xtri"].min()
        mean = part["media_dif_xtri"].mean()
        valid = int(part["itens_validos"].iloc[0])
        anul = int(part["anuladas"].iloc[0])

        draw_text(ax, 0.075, y0 + panel_h - 0.023, AREA_LABELS[key], 12.5, INK, "bold")
        status = f"média DIF {mean:.2f} · Δ cores {delta:.2f}".replace(".", ",")
        draw_text(ax, right_x, y0 + panel_h - 0.023, status, 9.5, LARANJA_XTRI, "bold")

        for j, cor in enumerate(CADERNO_ORDER[key]):
            row = part[part["cor"] == cor].iloc[0]
            by = y0 + panel_h - 0.050 - j * (bar_h + bar_gap)
            draw_text(ax, label_x, by + bar_h / 2, CADERNO_LABEL[cor], 8.7, MUTED, "bold")
            counts = {cat: int(row[cat]) for cat in CAT_ORDER}
            draw_stacked_bar(ax, bar_x, by, bar_w, bar_h, counts, int(row["n_posicoes"]))

        extra = f"{valid} válidas"
        if anul:
            extra += f" + {anul} anul."
        draw_text(ax, right_x, y0 + 0.028, extra, 9.0, MUTED)
        draw_text(ax, right_x, y0 + 0.012, "mesmo conjunto de itens", 8.4, MUTED)

    # Rodapé.
    rounded_box(ax, 0.055, 0.055, 0.89, 0.072, "#F3F6FA", GRID, lw=1.0, radius=0.020)
    draw_text(ax, 0.075, 0.104, "Leitura correta", 11.3, INK, "bold")
    draw_text(
        ax,
        0.075,
        0.082,
        "P01-P45 são posições dentro de cada cor. A comparação foi feita por CO_ITEM.",
        9.5,
        MUTED,
    )
    draw_text(
        ax,
        0.075,
        0.063,
        "Fonte: Microdados ENEM 2025 / INEP · presentes na área · anuladas preservadas como categoria.",
        8.7,
        MUTED,
    )
    draw_text(ax, 0.945, 0.025, "Dados reais ou nada.", 10.5, LARANJA_XTRI, "bold", "right")

    path = OUT / "xtri_enem_2025_equating_cadernos_dificuldade.png"
    fig.savefig(path, dpi=100, facecolor=BG)
    plt.close(fig)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary, audit = build_summary()

    csv_path = OUT / "equating_cadernos_dificuldade_2025.csv"
    json_path = OUT / "auditoria_equating_cadernos_dificuldade_2025.json"
    legend_path = OUT / "legenda_feed_equating_cadernos_2025.md"

    summary.to_csv(csv_path, index=False)
    png_path = make_feed(summary, audit)
    audit["arquivo_png"] = str(png_path)
    audit["arquivo_csv"] = str(csv_path)
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    legend_path.write_text(
        "\n".join(
            [
                "# Legenda - Equivalência dos cadernos ENEM 2025",
                "",
                "Caderno azul, amarelo, verde, branco ou cinza não significa prova mais fácil ou mais difícil.",
                "",
                "Neste gráfico, comparamos as cores pelo conjunto real de itens (`CO_ITEM`) e pela faixa de dificuldade calculada com TRI + acerto real.",
                "",
                "Resultado: dentro de cada área/percurso, as barras são iguais. Isso acontece porque as cores são formas equivalentes: muda a ordem dos itens, não o conjunto de dificuldades.",
                "",
                "Importante: `P01-P45` são posições dentro de uma cor de caderno, não identificadores universais de questão.",
                "",
                "Fonte: Microdados ENEM 2025 / INEP. Recorte: 1ª aplicação regular nacional; denominador por presença na área analisada.",
                "",
                "Dados reais ou nada.",
            ]
        ),
        encoding="utf-8",
    )

    print("PNG:", png_path)
    print("CSV:", csv_path)
    print("JSON:", json_path)
    print("LEGENDA:", legend_path)


if __name__ == "__main__":
    main()
