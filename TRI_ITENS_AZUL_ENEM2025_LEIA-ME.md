# TRI dos itens — ENEM 2025 (caderno Azul)

**Arquivo:** `TRI_ITENS_AZUL_ENEM2025.xlsx`
**Fonte:** Microdados ENEM 2025 / INEP (`DADOS/ITENS_PROVA_2025.csv`) + `analises_primi_2025_cop30/outputs/dificuldade_consolidado.json`.
**O que é:** dificuldade TRI, discriminação e % de acerto observado de cada item objetivo das 4 áreas.

## Como foi calculado

| Coluna | Cálculo / fonte |
|---|---|
| **TRI dificuldade** | `NU_PARAM_B × 100 + 500` — leva o parâmetro **b** (dificuldade) da escala θ para a escala ENEM (média 500, desvio 100). Ex.: b = 2,88 → **788**. |
| **Parâmetro A** | `NU_PARAM_A` (discriminação) direto do microdado. |
| **Discriminação (Baker)** | Faixas de Baker (2001) sobre o A: 0–0,34 Muito baixa · 0,35–0,64 Baixa · 0,65–1,34 Moderada · 1,35–1,69 Alta · ≥1,70 Muito alta. |
| **% de acerto observado** | Proporção de acerto real (`p` do `dificuldade_consolidado.json`), por `CO_ITEM`. Denominador = presentes do dia. |

> Os parâmetros TRI são **intrínsecos ao item** (`CO_ITEM`) — não dependem da cor do caderno; a cor só muda a ordem das questões. Foi usado o **caderno Azul da aplicação regular** (ITENS `CO_PROVA`: LC 1459, CH 1447, CN 1483, MT 1471).

## Abas
- **`TRI_itens`** — completa, 185 linhas. LC inclui as Q1–5 em inglês **e** espanhol (itens distintos). Colunas: Nº, Área, Língua, CO_ITEM, Hab., Gab., a, b, c, TRI, % acerto, N respondentes.
- **`Resumo`** — médias e correlação TRI × % acerto por área.
- **`Visão simples`** — Nº, Área, TRI, Parâmetro A, Discriminação (Baker), % acerto. Ordenada na **ordem da prova** (Nº crescente). 180 itens válidos.

## Observações de integridade
- **5 itens anulados** (CN Q123, Q125, Q132; MT Q172, Q174) não têm `b` nem `p` no microdado → marcados como **"Anulada"**, nunca preenchidos com valor estimado.
- A aba `Visão simples` traz os **180 itens válidos** (anuladas fora), por isso a sequência de Nº pula esses números.

## Principais achados
- **corr(TRI, % acerto) ≈ −0,83** — quanto maior a dificuldade-modelo, menor o acerto observado (forte, como esperado).
- Dificuldade média por área: **Linguagens 574 < C. Humanas 607 < C. Natureza 619 < Matemática 674** (MT é a mais difícil).
- A correlação **não é perfeita** porque o acerto também depende de discriminação (a) e chute (c):
  - **CN Q119** — b altíssimo (TRI 788) mas **31,7 % de acerto** (chute alto).
  - **MT Q160** — maior TRI da prova (**924**), porém discriminação só **Moderada** (a = 0,925): dificílimo, mas separa pouco os alunos.

_Mesma lição do estudo COP30: número de acertos ≠ nota TRI._
