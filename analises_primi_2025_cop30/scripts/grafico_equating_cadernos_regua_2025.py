#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feed XTRI - régua de equivalência das cores de caderno ENEM 2025.

O objetivo visual é simples: mostrar que os pontos das cores caem no mesmo
valor médio de DIF_XTRI dentro de cada área/percurso. Assim a peça comunica
melhor que a cor muda a posição, não a dificuldade do conjunto.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analises_primi_2025_cop30" / "outputs"
SUMMARY = OUT / "equating_cadernos_dificuldade_2025.csv"

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

CADERNO_COLORS = {
    "Azul": {"fc": "#27B8EF", "ec": "#128EC0", "tc": "#FFFFFF"},
    "Amarela": {"fc": "#FFD45A", "ec": "#B8941A", "tc": INK},
    "Verde": {"fc": "#58C77B", "ec": "#2E9150", "tc": INK},
    "Branca": {"fc": "#FFFFFF", "ec": "#AAB3C1", "tc": INK},
    "Cinza": {"fc": "#C9D1DD", "ec": "#7B8797", "tc": INK},
}

PAINEL_ORDER = [
    "Linguagens · Inglês",
    "Linguagens · Espanhol",
    "Humanas",
    "Natureza",
    "Matemática",
]


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
    width = w if w is not None else 0.0102 * len(text) + 0.042
    rounded_box(ax, x, y, width, 0.040, fc, ec, lw=1.0, radius=0.016)
    draw_text(ax, x + width / 2, y + 0.020, text, 9.7, color, "bold", "center")
    return width


def xmap(value: float, xmin: float, xmax: float, left: float, width: float) -> float:
    return left + (value - xmin) / (xmax - xmin) * width


def make_feed() -> tuple[Path, Path]:
    df = pd.read_csv(SUMMARY)

    audit = {
        "fonte": "Microdados ENEM 2025 / INEP",
        "base": str(SUMMARY),
        "tipo_visual": "régua/dot plot de média DIF_XTRI por cor",
        "leitura": "pontos alinhados dentro do painel indicam mesma dificuldade média por cor",
        "paineis": {},
    }

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

    draw_text(ax, 0.055, 0.890, "Não existe cor mais difícil", 32, INK, "bold")
    draw_text(
        ax,
        0.055,
        0.867,
        "As cores reorganizam os mesmos itens. A dificuldade média por cor fica igual.",
        12.8,
        MUTED,
    )

    chip_x = 0.055
    for text in ["Regular P1 nacional", "comparação por CO_ITEM", "diferença entre cores = 0,00"]:
        chip_x += draw_chip(ax, chip_x, 0.807, text) + 0.012

    # Faixa própria de legenda, fora dos painéis, para evitar colisão visual.
    draw_text(ax, 0.055, 0.764, "Cada ponto = uma cor de caderno", 9.8, MUTED, "bold")
    legend_x = 0.305
    for label in ["Azul", "Amarela", "Verde", "Branca", "Cinza"]:
        style = CADERNO_COLORS[label]
        ax.scatter(
            [legend_x + 0.010],
            [0.764],
            s=120,
            facecolor=style["fc"],
            edgecolor=style["ec"],
            linewidth=1.2,
            zorder=4,
        )
        draw_text(ax, legend_x + 0.026, 0.764, label, 9.6, INK)
        legend_x += 0.106 if label != "Amarela" else 0.126
    draw_text(ax, 0.055, 0.734, "Régua horizontal: dificuldade média do conjunto de itens.", 8.8, MUTED)

    # Régua comum.
    xmin, xmax = 62.0, 76.0
    plot_left, plot_w = 0.318, 0.425
    top_y = 0.626
    row_h = 0.092
    row_gap = 0.015

    for idx, painel in enumerate(PAINEL_ORDER):
        y0 = top_y - idx * (row_h + row_gap)
        rounded_box(ax, 0.055, y0, 0.89, row_h, PANEL, GRID, lw=1.0, radius=0.018)

        part = df[df["painel_label"] == painel].copy()
        values = part["media_dif_xtri"].astype(float)
        mean = float(values.mean())
        delta = float(values.max() - values.min())
        valid = int(part["itens_validos"].iloc[0])
        anul = int(part["anuladas"].iloc[0])
        same_set = "mesmo conjunto de itens"

        audit["paineis"][painel] = {
            "media_dif_xtri": mean,
            "delta_entre_cores": delta,
            "itens_validos": valid,
            "anuladas": anul,
            "cores": part[["cor_label", "co_prova", "media_dif_xtri"]].to_dict("records"),
        }

        draw_text(ax, 0.080, y0 + row_h - 0.020, painel, 12.7, INK, "bold")
        subtitle = f"{valid} válidas"
        if anul:
            subtitle += f" + {anul} anul."
        draw_text(ax, 0.080, y0 + row_h - 0.043, subtitle, 9.0, MUTED)
        draw_text(ax, 0.080, y0 + row_h - 0.063, same_set, 8.4, MUTED)

        # Linha base da régua e ponto médio da área/percurso.
        base_y = y0 + 0.035
        ax.plot([plot_left, plot_left + plot_w], [base_y, base_y], color="#D6DCE7", lw=5, solid_capstyle="round")
        ax.plot(
            [xmap(mean, xmin, xmax, plot_left, plot_w)] * 2,
            [base_y - 0.023, base_y + 0.023],
            color=LARANJA_XTRI,
            lw=1.5,
            alpha=0.55,
        )

        offsets = [-0.015, -0.005, 0.005, 0.015, 0.025]
        ordered = part.sort_values("cor_label")
        # Mantém ordem visual mais intuitiva quando as cores existem no painel.
        color_order = ["Azul", "Amarela", "Verde", "Branca", "Cinza"]
        ordered["ord"] = ordered["cor_label"].map({c: i for i, c in enumerate(color_order)})
        ordered = ordered.sort_values("ord")
        for j, (_, row) in enumerate(ordered.iterrows()):
            label = str(row["cor_label"])
            style = CADERNO_COLORS[label]
            x = xmap(float(row["media_dif_xtri"]), xmin, xmax, plot_left, plot_w)
            y = base_y + offsets[j]
            ax.scatter(
                [x],
                [y],
                s=210,
                facecolor=style["fc"],
                edgecolor=style["ec"],
                linewidth=1.5,
                zorder=5,
            )

        status = f"média {mean:.2f}".replace(".", ",")
        draw_text(ax, 0.790, y0 + row_h - 0.025, status, 11.7, INK, "bold")
        draw_text(ax, 0.790, y0 + row_h - 0.050, "diferença entre cores", 8.2, MUTED)
        draw_text(ax, 0.790, y0 + row_h - 0.071, f"{delta:.2f}".replace(".", ","), 18.0, LARANJA_XTRI, "bold")

    rounded_box(ax, 0.055, 0.058, 0.89, 0.082, "#F3F6FA", GRID, lw=1.0, radius=0.020)
    draw_text(ax, 0.075, 0.116, "Leitura correta", 11.5, INK, "bold")
    draw_text(
        ax,
        0.075,
        0.094,
        "Cor do caderno é permutação: muda P01-P45, mas o conjunto de itens é equivalente.",
        9.5,
        MUTED,
    )
    draw_text(
        ax,
        0.075,
        0.075,
        "Fonte: Microdados ENEM 2025 / INEP · dificuldade por CO_ITEM · presentes na área analisada.",
        8.7,
        MUTED,
    )
    draw_text(ax, 0.945, 0.025, "Dados reais ou nada.", 10.5, LARANJA_XTRI, "bold", "right")

    png_path = OUT / "xtri_enem_2025_equating_cadernos_regua.png"
    json_path = OUT / "auditoria_equating_cadernos_regua_2025.json"
    fig.savefig(png_path, dpi=100, facecolor=BG)
    plt.close(fig)
    audit["arquivo_png"] = str(png_path)
    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return png_path, json_path


def main() -> None:
    png, audit = make_feed()
    legenda = OUT / "legenda_feed_equating_cadernos_2025.md"
    legenda.write_text(
        "\n".join(
            [
                "# Legenda - Equivalência dos cadernos ENEM 2025",
                "",
                "Não existe caderno de cor mais difícil.",
                "",
                "A cor muda a posição das questões dentro do caderno, mas o conjunto de itens é equivalente.",
                "",
                "Neste gráfico, cada ponto é uma cor de caderno. Quando os pontos ficam alinhados na mesma régua, a dificuldade média é a mesma.",
                "",
                "A comparação foi feita por `CO_ITEM`, usando os parâmetros oficiais da TRI e a porcentagem real de acerto dos participantes presentes na área.",
                "",
                "Importante: `P01-P45` são posições dentro de cada cor de caderno, não identificadores universais da questão.",
                "",
                "Fonte: Microdados ENEM 2025 / INEP. Recorte: 1ª aplicação regular nacional.",
                "",
                "Dados reais ou nada.",
            ]
        ),
        encoding="utf-8",
    )
    print("PNG:", png)
    print("JSON:", audit)
    print("LEGENDA:", legenda)


if __name__ == "__main__":
    main()
