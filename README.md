# Microdados ENEM 2025 — Estudos XTRI

Estudos psicométricos (TRI) e conteúdo educacional produzidos pela **XTRI** a partir dos
Microdados oficiais do **ENEM 2025 / INEP**. Este repositório é o backup das **nossas
produções** — scripts de análise, artes/posts, textos e tabelas agregadas.

> **Transformamos dados em aprovações.** — Prof. Alexandre Emerson (@xandaoxtri) · [app.rankingenem.com](https://app.rankingenem.com)

---

## ⚠️ O que este repositório NÃO contém (por princípio)

Este repositório **não versiona microdados do INEP nem qualquer dado em grão individual.**
Ficam de fora (ver `.gitignore`):

- **Microdados brutos** do INEP (`DADOS/`, ~2,4 GB) — baixe direto do [INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).
- **Provas, gabaritos, dicionário e inputs** oficiais do INEP.
- **Qualquer arquivo em grão de aluno** — subconjuntos de microdado por escola, amostras
  candidato a candidato, notas individuais, strings de resposta. Nada disso sobe, mesmo
  anonimizado.

O que sobe são apenas **derivados agregados** (parâmetros por item, médias por escola/área),
**scripts** que reproduzem as análises, e as **peças de conteúdo** (imagens e textos).

Fonte primária de todos os números: **Microdados ENEM 2025 / INEP**.

---

## 📁 Estrutura

Cada pasta é um estudo ou uma leva de posts, tipicamente com: um `compute_*.py` (cálculo sobre
os microdados), um `ggplot_*.R` ou `*_graphics.py` (arte), um `LEIA-ME.md` (documentação do método
e achados) e um `TEXTO*.md`/`POST_WORDPRESS*.md` (legendas/artigo).

**Estudos técnicos (TRI):**
- `analise_psicometria_2025/` — CCI 3PL, função de informação, modelo × observado, paradoxo acerto×nota.
- `estudo_tri_marginal/` — valor marginal do acerto e "a questão que mais vale" por nível.
- `estudo_polemicas_tri/` — itens problemáticos (discriminação baixa + chute alto + misfit).
- `estudo_distratores/` — mapa de distratores: a alternativa errada que mais engana, item a item.
- `estudo_discriminacao_idade/` — parâmetro A por área; comparação 2024×2025 (proxy bisserial).
- `estudo_perfil_tri/` — função de informação × rede de ensino.
- `estudo_curva_prova_1a_2a/`, `estudo_dificuldade_ppl/` — 1ª vs 2ª aplicação.
- `estudo_cei_natal/`, `estudo_marista_natal/`, `estudo_dombosco_saoluis/`, `estudo_maristas_brasil/` — recortes por escola/rede (só saídas agregadas).
- `estudo_serie_historica/` — série de notas mín/máx por área (2015–2025).
- `dificuldade_sequencia_por_caderno/` — dificuldade por posição no caderno.

**Posts e carrosséis:**
- `post_distratores/`, `post_anulados/`, `post_discriminacao_2024_2025/`, `post_testlet/`, `post_45_lc/`
- `posts_abstencao/`, `posts_fadiga/`, `posts_lingua/`, `posts_idade - OK/`, `posts_treineiros/`,
  `posts_prioridade/`, `posts_acertos_nota/`, `posts_corretores/`, `carrossel_chutadas_2025/`
- `TRI_dos_itens_post/`

**Apresentações e material de apoio:**
- `palestra/`, `palestra_2025/` — deck com ~20 gráficos.
- `TRI_ITENS_AZUL_ENEM2025.xlsx` — tabela dos 180 itens (a, b, c, dificuldade TRI, % acerto).

**Documentos de projeto:**
- `CLAUDE.md` — regras fixas de marca, integridade de dados e SEO.
- `PADRAO_DESIGN_XTRI.md`, `SEO_PLAYBOOK_microdados_XTRI.md` — padrões de arte e SEO.
- `ROADMAP2_*.md`, `ROADMAP3_*.md` — cardápio de estudos.

---

## 🔬 Reprodutibilidade

Os scripts esperam os microdados oficiais em `DADOS/` (não incluído). Para rodar:

1. Baixe os Microdados ENEM 2025 do INEP e coloque `RESULTADOS_2025.csv`,
   `ITENS_PROVA_2025.csv` e `PARTICIPANTES_2025.csv` em `DADOS/`.
2. Dependências típicas: Python (`pandas`/`openpyxl`/`matplotlib`/`pymupdf`) e R (`ggplot2`, `jsonlite`, `gridExtra`).
3. Rode o `compute_*.py` do estudo desejado e depois a arte (`ggplot_*.R` ou `*_graphics.py`).

---

## 🔒 Integridade de dados (regra da casa)

- Nunca inventar ou estimar valor. Todo número vem de dado real (INEP).
- Valor vindo de modelo é rotulado como **"esperado/previsto"**, nunca como observado.
- Itens anulados são marcados, nunca preenchidos. Redação é múltiplo de 20.
- Perfil socioeconômico (`PARTICIPANTES`) não cruza com nota (`RESULTADOS`) — chaves distintas.
- Sempre citar **Fonte: Microdados ENEM 2025 / INEP**.

---

© XTRI. Conteúdo autoral baseado em dados públicos do INEP. Uso dos microdados conforme os termos do INEP.
