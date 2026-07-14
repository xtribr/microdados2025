# Estudo por escola — Colégio Marista Nossa Senhora de Nazaré (Belém/PA)

**CO_ESCOLA 15038424 · ENEM 2025 · aplicação COP30/BAM** — estudo no padrão do
pipeline por escola (CEI Natal / Marista Natal), adaptado para a particularidade
de Belém: os alunos fizeram a **prova COP30/BAM** (Belém-Ananindeua-Marituba),
que tem **zero itens em comum** com a Regular P1.

## O ponto metodológico central (Belém ≠ resto do Brasil)

1. **Códigos de prova.** Em `RESULTADOS_2025`, os alunos BAM aparecem com
   CO_PROVA 1583-1587/1631 (CH), 1595-1599/1632 (LC), 1607-1611/1633 (MT),
   1619-1623/1634 (CN) — rótulo oficial "BAM2" no Dicionário. Esses códigos têm
   0 linhas em `ITENS_PROVA_2025`, mas os itens/parâmetros **da própria prova
   COP30** estão lá sob **outros códigos** (CH 1520-1523, LC 1529-1532,
   MT 1502-1505, CN 1511-1514) — é desencontro de numeração entre os dois
   arquivos, não ausência de parâmetro. Três famílias DISJUNTAS em ITENS_PROVA
   (zero CO_ITEM em comum entre elas): Regular P1 (1447-1486), COP30/BAM
   (1502-1532) e Reaplicação (1539-1572, rótulo "(Reaplicação)" no Dicionário).
   Usamos o mapa RESULTADOS→ITENS do estudo PRIMI (`BAM_RESULT_TO_ITEM_CODE`)
   e **re-validamos aqui**: cross-check do gabarito de ITENS contra
   `TX_GABARITO_*` de todos os ~66 mil alunos BAM = **zero divergências**
   (ver `referencia_cop30.json`), e as cores dos cadernos 1502-1532 batem com
   as dos códigos BAM2. Nenhum parâmetro da Regular nem da Reaplicação entrou
   no estudo. Protocolo do incidente COP30 cumprido.
2. **Referência item a item = coorte COP30**, não o Brasil: habilidade,
   dificuldade, discriminação e as nuvens de fundo comparam a escola com os
   ~62-66 mil presentes da mesma prova. Comparar erro por habilidade com o BR
   regular seria comparar itens diferentes.
3. **Nota TRI compara com todo mundo** (escala equalizada entre aplicações):
   a tabela do painel traz escola × coorte COP30 × Brasil Regular P1.
4. **Redação**: o tema da aplicação BAM difere do regular → competências C1-C5
   comparadas com a coorte COP30 (mesma prova, mesmo tema).
5. **Categorias de dificuldade**: quartis de `dif_xtri` (100×(1−P(θ=0)), 3PL
   D=1,7) dentro de cada área, sobre os itens da prova BAM (não dá para usar o
   mapa de categorias da Regular). Prova BAM: **zero itens anulados** → 45
   válidos/área, 180 no total.

## População

- **142** concluintes com escola declarada (treineiros ficam fora — CO_ESCOLA
  não existe para eles).
- **~100 por área fizeram a prova BAM**; **17 por área fizeram a Regular P1**
  (prestaram fora dos 3 municípios). Item a item usa só o subgrupo BAM
  (100 processados, 97 presentes nas 4); notas TRI usam todos.
- Língua: 136 inglês × 6 espanhol.

## Resultados-chave (Microdados ENEM 2025 / INEP)

| | Escola | Coorte COP30 | Brasil Regular P1 |
|---|---|---|---|
| Linguagens | 597,5 | 497,3 | 533,4 |
| Humanas | 611,4 | 492,6 | 513,1 |
| Natureza | 592,3 | 486,1 | 500,6 |
| Matemática | 669,7 | 484,0 | 521,2 |
| Redação | 830,6 | 609,2 | — |

- **16º entre os 70 colégios Maristas do Brasil** (média das 5 = 661,2; ver
  `estudo_maristas_brasil/`).
- **Alertas** — habilidades com erro ACIMA da coorte COP30 (mesma prova):
  **CH-H22** (85,0% × 76,3%), **LC-H13** (67,0% × 60,4%), CN-H5 (89,7% × 88,8%),
  CN-H29 (66,0% × 65,8%). CN-H5 com quase 90% de erro é o maior bolsão absoluto.
- Gargalo de redação: **C1 norma culta** (média 148; 0% gabaritam) — mesmo padrão
  das outras 4 escolas fortes estudadas.
- Incoerência (person-fit): média 4,99/aluno (4 provas), mediana 5 — nível
  semelhante ao CEI/Marista Natal (deslizes em itens fáceis, não chute).
- Degrau da dificuldade: no item pesado a escola acerta ~2x a coorte
  (MT 36% × 17%).

## Ranking local (método Teresa: presentes 2 dias c/ 5 notas, N≥10)

`ranking_local.py` → `resumo_ranking_local.json`, `ranking_belem_media5.csv`,
`ranking_pa_media5.csv`. N=114 alunos (bate com o ranking Maristas).

| Recorte | Média 5 | CN | CH | LC | MT | Redação |
|---|---|---|---|---|---|---|
| Belém (163 escolas) | 7º | 7º | 7º | 7º | **6º** | 8º |
| Belém privadas (64) | 6º | 6º | 6º | 6º | **5º** | 8º |
| Pará (850) | 10º | 9º | 9º | 11º | 9º | 22º |
| Pará privadas (186) | 9º | 8º | 8º | 10º | 8º | 22º |

- Top-6 de Belém acima dele: Equipe (760,2, N=38), Integrado IN, Physics,
  Equipe Cristal, Colégio Militar (federal — sai do recorte privadas) e
  Sta Catarina de Sena (662,4, N=89) — Marista 661,2 com N=114, o maior N do top-7.
- MT é a melhor posição relativa (6º Belém); **Redação é a pior no estadual**
  (22º/850) — várias escolas do interior pontuam alto em redação.

## Arquivos

- `extract_belem.py` — passada única no RESULTADOS (2,1 GB): `alunos.csv` da
  escola + referência da coorte COP30 (`referencia_cop30.json`, `itens_cop30.csv`
  com %acerto por item) + cross-check de gabarito.
- `extract_scatter_cop30.py` — nuvens acertos×nota da coorte
  (`plot_data/scatter_*.csv`, `chutes_scatter_cop30.csv`); roda sobre pré-filtro
  em bytes dos municípios 1501402/1500800/1504422 (grep do macOS falha no CSV
  latin-1 — usar Python).
- `compute_belem.py` — correção item a item do subgrupo BAM → `habilidades.csv`,
  `categorias.csv`, `disc.csv`, `alunos_proc.csv`, `alunos_area.csv`,
  `itens_categoria.csv`, `redacao_comp.json`, `resumo.json`.
- `ggplot_belem.R` — 16 gráficos (hab×4, dificuldade×4, discriminação,
  incoerência×4, nuvem, redação×2) em `graficos/`.
- `painel_belem.py` — `graficos/painel_resumo.png` (usa `xtri_deck` da palestra).
- Sem gráfico de chutes-vs-BR nem testlet (referências são da prova regular).

Fonte: Microdados ENEM 2025 / INEP. Nome da escola: Censo Escolar 2025.
Nenhum dado individual identificável é exportado.
