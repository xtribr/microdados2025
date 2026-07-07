#!/usr/bin/env python3
"""
Gera gráficos PRIMI ENEM 2025 comparando:
  - ENEM Regular P1: amostra determinística de 100 mil por área;
  - ENEM COP30/BAM: todos os presentes válidos em Belém, Ananindeua e Marituba.

O gráfico usa dados oficiais do pacote de microdados 2025:
  - x = acertos válidos recalculados a partir de respostas + gabarito;
  - y = nota TRI oficial do INEP no microdado;
  - itens anulados (IN_ITEM_ABAN=1) são removidos do cálculo de acertos.

Nenhum identificador de participante é exportado.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.offsetbox import AnnotationBbox, OffsetImage  # noqa: E402
from PIL import Image  # noqa: E402


BASE_DIR = Path(__file__).resolve().parents[2]
DADOS_DIR = BASE_DIR / "DADOS"
OUTPUT_DIR = BASE_DIR / "analises_primi_2025_cop30" / "outputs"
LOGO_PATH = BASE_DIR / "logotipo.png"

SEED = 20250624
AMOSTRA_REGULAR_POR_AREA = 100_000

AREAS = ["LC", "CH", "CN", "MT"]
AREA_LABEL = {
    "LC": "Linguagens",
    "CH": "Ciências Humanas",
    "CN": "Ciências da Natureza",
    "MT": "Matemática",
}
AREA_START = {"LC": 1, "CH": 46, "CN": 91, "MT": 136}

XTRI_BLUE = "#27B6EA"
XTRI_ORANGE = "#FF4A2D"
TEXT_DARK = "#182230"
TEXT_MUTED = "#667085"
GRID = "#D0D5DD"
BG = "#F7F8FA"

# Cadernos padrão da primeira aplicação nacional.
REGULAR_P1_CODES = {
    "LC": {"1459": "Azul", "1460": "Amarela", "1461": "Verde", "1462": "Branca"},
    "CH": {"1447": "Azul", "1448": "Amarela", "1449": "Branca", "1450": "Verde"},
    "CN": {"1483": "Azul", "1484": "Amarela", "1485": "Verde", "1486": "Cinza"},
    "MT": {"1471": "Azul", "1472": "Amarela", "1473": "Verde", "1474": "Cinza"},
}

# O INPUT_R_RESULTADOS_2025 rotula estes códigos como BAM, mas o arquivo
# ITENS_PROVA_2025 traz os parâmetros/gabaritos BAM em outro intervalo.
# O mapeamento abaixo foi validado comparando os gabaritos oficiais.
# Os cadernos de acessibilidade BAM (ampliada/superampliada/ledor/especializado)
# são item-idênticos ao caderno-base da área (CH/LC: branca; CN/MT: cinza) —
# mesmo conjunto e ordem de itens, 0 anulados — então reaproveitam o item_code base.
BAM_RESULT_TO_ITEM_CODE = {
    "CH": {
        "1583": ("1520", "Azul - BAM"),
        "1584": ("1521", "Amarela - BAM"),
        "1585": ("1522", "Branca - BAM"),
        "1586": ("1523", "Verde - BAM"),
        "1587": ("1522", "Laranja Ampliada - BAM"),
        "1631": ("1522", "Atendimento Especializado - BAM"),
    },
    "LC": {
        "1595": ("1529", "Azul - BAM"),
        "1596": ("1530", "Amarela - BAM"),
        "1597": ("1531", "Verde - BAM"),
        "1598": ("1532", "Branca - BAM"),
        "1599": ("1532", "Laranja Ampliada - BAM"),
        "1632": ("1532", "Atendimento Especializado - BAM"),
    },
    "MT": {
        "1607": ("1502", "Azul - BAM"),
        "1608": ("1503", "Amarela - BAM"),
        "1609": ("1504", "Verde - BAM"),
        "1610": ("1505", "Cinza - BAM"),
        "1611": ("1505", "Laranja Ampliada - BAM"),
        "1633": ("1505", "Atendimento Especializado - BAM"),
    },
    "CN": {
        "1619": ("1511", "Azul - BAM"),
        "1620": ("1512", "Amarela - BAM"),
        "1621": ("1514", "Verde - BAM"),
        "1622": ("1513", "Cinza - BAM"),
        "1623": ("1513", "Laranja Ampliada - BAM"),
        "1634": ("1513", "Atendimento Especializado - BAM"),
    },
}

BAM_MUNICIPIOS = {"Belém", "Ananindeua", "Marituba"}


@dataclass(frozen=True)
class Item:
    posicao: int
    gabarito: str
    b: float | None
    lingua: str


def parse_float(valor: str) -> float | None:
    if not valor:
        return None
    try:
        return float(valor.replace(",", "."))
    except ValueError:
        return None


def carregar_itens() -> dict[tuple[str, str], list[Item]]:
    itens: dict[tuple[str, str], list[Item]] = defaultdict(list)
    with (DADOS_DIR / "ITENS_PROVA_2025.csv").open("r", encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if row["IN_ITEM_ABAN"] == "1":
                continue
            itens[(row["SG_AREA"], row["CO_PROVA"])].append(
                Item(
                    posicao=int(row["CO_POSICAO"]),
                    gabarito=row["TX_GABARITO"],
                    b=parse_float(row["NU_PARAM_B"]),
                    lingua=row["TP_LINGUA"] or "",
                )
            )
    return itens


def contar_itens_anulados() -> dict[tuple[str, str], int]:
    anulados: dict[tuple[str, str], int] = Counter()
    with (DADOS_DIR / "ITENS_PROVA_2025.csv").open("r", encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if row["IN_ITEM_ABAN"] == "1":
                anulados[(row["SG_AREA"], row["CO_PROVA"])] += 1
    return dict(anulados)


def itens_para_candidato(
    itens_por_prova: dict[tuple[str, str], list[Item]],
    area: str,
    item_code: str,
    lingua: str,
) -> list[Item]:
    itens = []
    for item in itens_por_prova[(area, item_code)]:
        if area == "LC" and item.lingua and item.lingua != lingua:
            continue
        itens.append(item)
    return itens


def calcular_metricas_resposta(
    resposta: str,
    area: str,
    itens: Iterable[Item],
) -> tuple[int, int, float]:
    acertos = 0
    validos = 0
    dificeis = 0
    acertos_dificeis = 0
    offset = AREA_START[area]
    for item in itens:
        idx = item.posicao - offset
        if idx < 0 or idx >= len(resposta):
            continue
        marcado = resposta[idx]
        validos += 1
        acertou = bool(marcado) and marcado not in {"*", "."} and marcado == item.gabarito
        if acertou:
            acertos += 1
        if item.b is not None and item.b > 1.5:
            dificeis += 1
            if acertou:
                acertos_dificeis += 1
    acert_dif = acertos_dificeis / dificeis if dificeis else math.nan
    return acertos, validos, acert_dif


def reservoir_add(
    amostra: list[dict],
    total_vistos: int,
    item: dict,
    limite: int,
    rng: random.Random,
) -> None:
    if len(amostra) < limite:
        amostra.append(item)
        return
    j = rng.randrange(total_vistos)
    if j < limite:
        amostra[j] = item


def validar_mapeamento_bam(itens_por_prova: dict[tuple[str, str], list[Item]]) -> dict:
    """Valida códigos BAM por comparação com TX_GABARITO_* do RESULTADOS."""
    pendentes = {
        (area, result_code, item_code)
        for area, mapa in BAM_RESULT_TO_ITEM_CODE.items()
        for result_code, (item_code, _) in mapa.items()
    }
    validacao = {}
    with (DADOS_DIR / "RESULTADOS_2025.csv").open("r", encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            if not pendentes:
                break
            for area, result_code, item_code in list(pendentes):
                if row[f"CO_PROVA_{area}"] != result_code:
                    continue
                lingua = row["TP_LINGUA"] if area == "LC" else ""
                itens = itens_para_candidato(itens_por_prova, area, item_code, lingua)
                reconstruido = ["?"] * 45
                for item in itens:
                    reconstruido[item.posicao - AREA_START[area]] = item.gabarito
                oficial = row[f"TX_GABARITO_{area}"]
                if area == "LC":
                    # LC no RESULTADOS guarda 50 caracteres: 5 ingles + 5 espanhol + 40 comuns.
                    prefixo = oficial[:5] if lingua == "0" else oficial[5:10]
                    oficial_45 = prefixo + oficial[10:]
                else:
                    oficial_45 = oficial
                ok = all(a == "?" or a == b for a, b in zip(reconstruido, oficial_45))
                validacao[f"{area}:{result_code}->{item_code}"] = ok
                pendentes.remove((area, result_code, item_code))
    return validacao


def coletar_dados() -> tuple[dict[str, list[dict]], dict]:
    itens_por_prova = carregar_itens()
    anulados = contar_itens_anulados()
    validacao_bam = validar_mapeamento_bam(itens_por_prova)

    rngs = {area: random.Random(SEED + i) for i, area in enumerate(AREAS)}
    dados_brutos_regular = {area: [] for area in AREAS}
    dados_brutos_bam = {area: [] for area in AREAS}
    regulares_vistos = Counter()
    candidatos = Counter()
    descartes = Counter()
    codigos_usados = defaultdict(Counter)

    with (DADOS_DIR / "RESULTADOS_2025.csv").open("r", encoding="latin-1", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            presente_2_dias = all(row[f"TP_PRESENCA_{area}"] == "1" for area in AREAS)
            if not presente_2_dias:
                continue

            for area in AREAS:
                result_code = row[f"CO_PROVA_{area}"]
                nota = parse_float(row[f"NU_NOTA_{area}"])
                resposta = row[f"TX_RESPOSTAS_{area}"]
                if nota is None or not resposta:
                    descartes[(area, "sem_nota_ou_resposta")] += 1
                    continue

                aplicacao = None
                item_code = None
                rotulo_prova = None
                if result_code in REGULAR_P1_CODES[area]:
                    aplicacao = "Regular P1"
                    item_code = result_code
                    rotulo_prova = REGULAR_P1_CODES[area][result_code]
                elif (
                    result_code in BAM_RESULT_TO_ITEM_CODE[area]
                    and row["SG_UF_PROVA"] == "PA"
                    and row["NO_MUNICIPIO_PROVA"] in BAM_MUNICIPIOS
                ):
                    aplicacao = "COP30/BAM"
                    item_code, rotulo_prova = BAM_RESULT_TO_ITEM_CODE[area][result_code]
                else:
                    continue

                registro = {
                    "area": area,
                    "aplicacao": aplicacao,
                    "nota": nota,
                    "resposta": resposta,
                    "lingua": row["TP_LINGUA"] if area == "LC" else "",
                    "codigo_resultado": result_code,
                    "codigo_itens": item_code,
                    "prova": rotulo_prova,
                }
                codigos_usados[(area, aplicacao)][f"{result_code}->{item_code}"] += 1

                if aplicacao == "Regular P1":
                    regulares_vistos[area] += 1
                    reservoir_add(
                        dados_brutos_regular[area],
                        regulares_vistos[area],
                        registro,
                        AMOSTRA_REGULAR_POR_AREA,
                        rngs[area],
                    )
                else:
                    dados_brutos_bam[area].append(registro)
                candidatos[(area, aplicacao)] += 1

    dados = {area: [] for area in AREAS}
    for area in AREAS:
        registros = dados_brutos_regular[area] + dados_brutos_bam[area]
        for registro in registros:
            itens_candidato = itens_para_candidato(
                itens_por_prova,
                area,
                registro["codigo_itens"],
                registro["lingua"],
            )
            acertos, validos, acert_dif = calcular_metricas_resposta(
                registro["resposta"],
                area,
                itens_candidato,
            )
            if validos == 0:
                descartes[(area, "sem_itens_validos_amostra")] += 1
                continue
            dados[area].append(
                {
                    "area": area,
                    "aplicacao": registro["aplicacao"],
                    "acertos": acertos,
                    "itens_validos": validos,
                    "nota": registro["nota"],
                    "acert_dif": acert_dif,
                    "codigo_resultado": registro["codigo_resultado"],
                    "codigo_itens": registro["codigo_itens"],
                    "prova": registro["prova"],
                }
            )

    meta = {
        "seed": SEED,
        "amostra_regular_por_area": AMOSTRA_REGULAR_POR_AREA,
        "criterios": {
            "ano": 2025,
            "presenca": "TP_PRESENCA_LC/CH/CN/MT == 1",
            "regular": "cadernos padrao da primeira aplicacao nacional",
            "cop30_bam": "codigos BAM oficiais no PA, municipios Belem/Ananindeua/Marituba",
            "itens_anulados": "IN_ITEM_ABAN=1 removidos do calculo de acertos",
            "tri": "NU_NOTA_* oficial do INEP no microdado 2025",
            "sem_exportar_identificador": True,
        },
        "validacao_bam": validacao_bam,
        "candidatos_elegiveis": {
            f"{area}|{aplicacao}": n for (area, aplicacao), n in sorted(candidatos.items())
        },
        "regulares_vistos_antes_da_amostra": dict(regulares_vistos),
        "descartes": {f"{area}|{motivo}": n for (area, motivo), n in sorted(descartes.items())},
        "codigos_usados": {
            f"{area}|{aplicacao}": dict(counter)
            for (area, aplicacao), counter in sorted(codigos_usados.items())
        },
        "itens_anulados_por_codigo_itens": {
            f"{area}|{code}": n for (area, code), n in sorted(anulados.items())
        },
    }
    return dados, meta


def stats_por_aplicacao(registros: list[dict]) -> dict[str, dict]:
    stats = {}
    for aplicacao in ["Regular P1", "COP30/BAM"]:
        arr = [r for r in registros if r["aplicacao"] == aplicacao]
        if not arr:
            stats[aplicacao] = {"n": 0}
            continue
        acertos = np.array([r["acertos"] for r in arr], dtype=float)
        notas = np.array([r["nota"] for r in arr], dtype=float)
        stats[aplicacao] = {
            "n": int(len(arr)),
            "media_acertos": float(np.mean(acertos)),
            "media_nota": float(np.mean(notas)),
            "mediana_nota": float(np.median(notas)),
            "corr_acertos_nota": float(np.corrcoef(acertos, notas)[0, 1]),
            "itens_validos_dist": dict(Counter(r["itens_validos"] for r in arr)),
            "acert_dif_medio": float(np.nanmean([r["acert_dif"] for r in arr])),
        }
    return stats


def linhas_por_acerto(registros: list[dict], aplicacao: str, minimo: int = 30) -> dict[str, np.ndarray]:
    grupos = defaultdict(list)
    for r in registros:
        if r["aplicacao"] == aplicacao:
            grupos[r["acertos"]].append(r["nota"])

    xs, p10, med, p90 = [], [], [], []
    for acertos in sorted(grupos):
        notas = grupos[acertos]
        if len(notas) < minimo:
            continue
        xs.append(acertos)
        p10.append(np.percentile(notas, 10))
        med.append(np.percentile(notas, 50))
        p90.append(np.percentile(notas, 90))
    return {
        "x": np.array(xs),
        "p10": np.array(p10),
        "med": np.array(med),
        "p90": np.array(p90),
    }


def recortar_linha_visual(linha: dict[str, np.ndarray], y_min: float = 320.0) -> dict[str, np.ndarray]:
    """Remove o trecho inicial da curva que encosta na borda inferior do gráfico."""
    if not len(linha["x"]):
        return linha
    mascara = linha["med"] >= y_min
    return {chave: valores[mascara] for chave, valores in linha.items()}


def formatar_int(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def adicionar_logo(fig: plt.Figure) -> None:
    if not LOGO_PATH.exists():
        return
    logo = Image.open(LOGO_PATH).convert("RGBA")
    imagem = OffsetImage(np.asarray(logo), zoom=0.115)
    ab = AnnotationBbox(
        imagem,
        (0.895, 0.935),
        xycoords=fig.transFigure,
        frameon=False,
        box_alignment=(0.5, 0.5),
        zorder=20,
    )
    fig.add_artist(ab)


def desenhar_grafico_area(area: str, registros: list[dict], meta_area: dict) -> Path:
    fig = plt.figure(figsize=(8, 10), dpi=135, facecolor=BG)
    ax = fig.add_axes([0.11, 0.16, 0.82, 0.63], facecolor="white")

    rng = np.random.default_rng(SEED + len(area))
    estilos = {
        "Regular P1": {"cor": XTRI_BLUE, "alpha": 0.12, "label": "Regular P1"},
        "COP30/BAM": {"cor": XTRI_ORANGE, "alpha": 0.20, "label": "COP30 / BAM"},
    }

    for aplicacao, estilo in estilos.items():
        arr = [r for r in registros if r["aplicacao"] == aplicacao]
        if not arr:
            continue
        x = np.array([r["acertos"] for r in arr], dtype=float)
        y = np.array([r["nota"] for r in arr], dtype=float)
        jitter = rng.uniform(-0.18, 0.18, size=len(arr))
        ax.scatter(
            x + jitter,
            y,
            s=7,
            color=estilo["cor"],
            alpha=estilo["alpha"],
            edgecolors="none",
            rasterized=True,
            label=estilo["label"],
        )
        linha = linhas_por_acerto(registros, aplicacao, minimo=120 if aplicacao == "Regular P1" else 60)
        linha = recortar_linha_visual(linha, y_min=320.0)
        if len(linha["x"]):
            ax.fill_between(
                linha["x"],
                linha["p10"],
                linha["p90"],
                color=estilo["cor"],
                alpha=0.08,
                linewidth=0,
            )
            ax.plot(linha["x"], linha["med"], color=estilo["cor"], linewidth=3.0)

    todos_acertos = [r["acertos"] for r in registros]
    todos_notas = [r["nota"] for r in registros]
    ax.set_xlim(max(-0.8, min(todos_acertos) - 1), max(todos_acertos) + 1)
    ax.set_ylim(max(250, min(todos_notas) - 25), min(1000, max(todos_notas) + 30))
    ax.grid(True, color=GRID, alpha=0.38, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#98A2B3")
    ax.spines["bottom"].set_color("#98A2B3")
    ax.tick_params(axis="both", labelsize=12, colors=TEXT_DARK)
    ax.set_xlabel("Acertos válidos (questões anuladas fora)", fontsize=13, color=TEXT_DARK, labelpad=10)
    ax.set_ylabel("Nota TRI oficial ENEM 2025", fontsize=13, color=TEXT_DARK, labelpad=10)

    legenda = ax.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor="#EAECF0",
        framealpha=0.94,
        fontsize=10.5,
        markerscale=1.7,
    )
    for handle in legenda.legend_handles:
        handle.set_alpha(0.9)

    stats = stats_por_aplicacao(registros)
    fig.text(0.08, 0.925, "XTRI ENEM 2025", fontsize=17, color=TEXT_MUTED, weight="bold")
    fig.text(0.08, 0.885, AREA_LABEL[area], fontsize=28, color=TEXT_DARK, weight="bold")
    fig.text(
        0.08,
        0.852,
        "ENEM COP30/BAM x ENEM Regular P1 · presentes nos dois dias",
        fontsize=12.5,
        color=TEXT_MUTED,
    )

    n_reg = stats["Regular P1"]["n"]
    n_bam = stats["COP30/BAM"]["n"]
    fig.text(
        0.08,
        0.812,
        f"N Regular={formatar_int(n_reg)}   N COP30={formatar_int(n_bam)}",
        fontsize=13,
        color=TEXT_DARK,
        weight="bold",
    )

    anuladas_txt = ", ".join(
        f"{aplicacao}: {valor}"
        for aplicacao, valor in meta_area["anuladas_por_aplicacao"].items()
    )
    fig.text(
        0.08,
        0.05,
        f"Fonte: Microdados ENEM 2025/INEP · seed {SEED} · anuladas removidas ({anuladas_txt})",
        fontsize=8.4,
        color=TEXT_MUTED,
    )
    adicionar_logo(fig)

    out = OUTPUT_DIR / f"xtri_enem_2025_cop30_vs_regular_{area}.png"
    fig.savefig(out, dpi=135, facecolor=BG)
    plt.close(fig)
    return out


def salvar_csv_area(area: str, registros: list[dict]) -> Path:
    out = OUTPUT_DIR / f"amostra_xtri_2025_{area}.csv"
    campos = [
        "area",
        "aplicacao",
        "acertos",
        "itens_validos",
        "nota",
        "acert_dif",
        "codigo_resultado",
        "codigo_itens",
        "prova",
    ]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for row in registros:
            writer.writerow(row)
    return out


def salvar_legenda_feed(resumo: dict) -> Path:
    out = OUTPUT_DIR / "legendas_feed_xtri_2025_cop30.md"
    linhas = [
        "# Legendas Feed - XTRI ENEM 2025 COP30 x Regular",
        "",
        "Base real: Microdados ENEM 2025/INEP. Critério: presentes nos dois dias; "
        "Regular P1 com amostra aleatória determinística de 100.000 por área; "
        "COP30/BAM com todos os elegíveis de Belém, Ananindeua e Marituba. "
        "Questões anuladas removidas do cálculo de acertos.",
        "",
    ]
    for area in AREAS:
        dados_area = resumo["areas"][area]
        reg = dados_area["stats"]["Regular P1"]
        bam = dados_area["stats"]["COP30/BAM"]
        anuladas = dados_area["anuladas_por_aplicacao"]
        linhas.extend(
            [
                f"## {dados_area['label']}",
                "",
                f"N Regular P1: {formatar_int(reg['n'])}",
                f"N COP30/BAM: {formatar_int(bam['n'])}",
                f"Media TRI Regular P1: {reg['media_nota']:.1f}",
                f"Media TRI COP30/BAM: {bam['media_nota']:.1f}",
                f"Media de acertos Regular P1: {reg['media_acertos']:.1f}",
                f"Media de acertos COP30/BAM: {bam['media_acertos']:.1f}",
                f"Correlacao acertos x TRI Regular P1: {reg['corr_acertos_nota']:.3f}",
                f"Correlacao acertos x TRI COP30/BAM: {bam['corr_acertos_nota']:.3f}",
                f"Questoes anuladas removidas - Regular P1: {anuladas['Regular P1']}; COP30/BAM: {anuladas['COP30/BAM']}",
                "",
            ]
        )
    out.write_text("\n".join(linhas), encoding="utf-8")
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dados, meta = coletar_dados()

    resumo = {"meta": meta, "areas": {}}
    graficos = []
    csvs = []

    for area in AREAS:
        stats = stats_por_aplicacao(dados[area])

        anuladas_por_aplicacao = {}
        for aplicacao in ["Regular P1", "COP30/BAM"]:
            pares = {
                (r["area"], r["codigo_itens"])
                for r in dados[area]
                if r["aplicacao"] == aplicacao
            }
            anuladas_por_aplicacao[aplicacao] = int(
                max(
                    [
                        meta["itens_anulados_por_codigo_itens"].get(f"{a}|{codigo}", 0)
                        for a, codigo in pares
                    ]
                    or [0]
                )
            )

        resumo["areas"][area] = {
            "label": AREA_LABEL[area],
            "stats": stats,
            "anuladas_por_aplicacao": anuladas_por_aplicacao,
        }
        csvs.append(str(salvar_csv_area(area, dados[area])))
        graficos.append(str(desenhar_grafico_area(area, dados[area], resumo["areas"][area])))

    legenda_feed = str(salvar_legenda_feed(resumo))
    resumo["arquivos"] = {"graficos": graficos, "csvs": csvs, "legenda_feed": legenda_feed}
    auditoria_path = OUTPUT_DIR / "auditoria_xtri_2025_cop30.json"
    with auditoria_path.open("w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)

    print(json.dumps(resumo["areas"], ensure_ascii=False, indent=2))
    print("\nArquivos gerados:")
    for path in graficos + csvs + [legenda_feed, str(auditoria_path)]:
        print(path)


if __name__ == "__main__":
    main()
