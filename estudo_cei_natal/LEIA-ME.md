# Estudo CEI — Romualdo × Roberto Freire (ENEM 2025)

**Escolas (Censo Escolar 2025 / INEP):**
- `24069191` — Centro de Educação Integrada S A — **Romualdo** (Natal/RN, privada, urbana)
- `24089214` — Centro de Educação Integrada S A — **Roberto Freire** (Natal/RN, privada, urbana)

**Amostra:** 212 candidatos com `CO_ESCOLA` nas duas unidades (concluintes que declararam escola) →
**209 presentes nas 4 provas** (Romualdo 139, Roberto Freire 70). 2 alunos fizeram a reaplicação (2ª aplicação).
Alunos anônimos — microdados não têm nome.

## Metodologia
1. `extract_cei.py` — varre RESULTADOS_2025.csv (4,81 M linhas) filtrando as duas escolas; de carona acumula a média nacional por área (`referencia_nacional.json`).
2. `compute_cei.py` — corrige **item a item** (175 itens válidos: LC 45 + CH 45 + CN 42 + MT 43) usando ITENS_PROVA_2025 (gabarito por posição/cor, trata anulados e língua):
   - **erro por habilidade** por área × nacional (`habilidades_dificuldade_2025.csv`);
   - **acerto por categoria de dificuldade** (mapa XTRI por `co_item`) e **por faixa de discriminação** (Baker, parâmetro A);
   - **índice de chute/incoerência** (person-fit): por área, `min(erros em itens fáceis b≤0,6; acertos em itens difíceis b≥1,6)`, somado nas 4 áreas — mesma definição do estudo nacional (referência: `chutes_counts.json` / `chutes_scatter.csv`, Regular P1).
3. `ggplot_cei.R` + `painel_cei.py` — gráficos.

## Resultados-chave
| | Romualdo | Roberto Freire | Brasil (P1) |
|---|---|---|---|
| Linguagens | 624,6 | 618,7 | 533,4 |
| Humanas | 629,8 | 613,4 | 513,1 |
| Natureza | 629,1 | 639,2 | 500,6 |
| Matemática | **734,9** | **719,4** | 521,2 |
| Redação | 873,1 | 862,9 | — |

- **Habilidades mais erradas** (top-3 por unidade): LC H29/H16 (+H19 Rom, +H28 RF) · CH **H10/H12/H13** · CN **H26/H6** (+H7 Rom, +H2 RF) · MT **H7/H22** (+H18 Rom, +H9 RF).
- **⚠ Acima do erro nacional** (mesmo sendo escolas fortes): **CH-H10** (Rom 84,9% × BR 73,1%; RF 75,7%), **CH-H12** (ambas ~78% ≈ BR), **CN-H6** (74,8/77,1 × BR 71,1), **LC-H28** (RF 50,0 × BR 45,0).
- **Dificuldade (B):** acerto cai em degrau Fácil→Muito difícil (ex.: MT 82→44 Rom), mas sempre bem acima do Brasil (Muito difícil MT: 44/41 × 18 BR).
- **Discriminação (A):** a distância p/ o Brasil é MAIOR nos itens de A muito alto (≥1,70) — ex.: MT 58/56 × 27 BR; CH 63/59 × 37. Coerente com θ alto: item "navalha" favorece quem sabe.
- **Chute:** incoerência média 4,55 (Rom) / 4,63 (RF), mediana 4–5, máx 9 — perfil igual à categoria nacional majoritária ("algumas incoerências", 56% do BR). Na turma forte o índice é limitado pelos **erros em itens fáceis** (deslizes), não por acerto de sorte em difícil.

- **Redação por competência** (`cei_redacao_comp.json`, gráficos `cei_redacao_competencias.png` + `cei_redacao_200.png`): o gargalo é a **C1 (norma culta)** — média 156,8 (Rom) / 150,3 (RF), só 1,4%/0% gabaritam; 2º ponto fraco: **C3 (argumentação)** 169/167. **C2 é força** (179 ambas — a "vilã nacional" de 2025, média BR 137, foi domada). C4/C5 perto do teto (182–184; C5: 65%/61% com nota 200). Referência nacional: `redacao_2024_2025.json`.

- **Testlet LC (Q6–Q10 Azul, 1 texto):** `graficos/cei_testlet_erro.png` + `testlet.csv` — erro médio no bloco: Romualdo 37,7% e Roberto Freire 37,7% × Brasil 61,1%; Q8 (H29) é a mais difícil para todos (57/59% × BR 68%). Itens localizados por co_item no caderno de cada aluno.

## Arquivos
- Gráficos: `graficos/` — `cei_painel_resumo.png`, `cei_hab_{LC,CH,CN,MT}.png`, `cei_dificuldade.png` (degrau, v2), `cei_discriminacao.png` (degrau, v2), `cei_chutes.png` (4 áreas juntas), **`cei_incoerencia_{LC,CH,CN,MT}.png`** (gráfico de incoerência por área: nuvem nacional + aluno CEI, tamanho = incoerência da área)
- v2 (2026-07-01): dificuldade/discriminação refeitos como **linhas de degrau com rótulo direto** (Romualdo/Roberto Freire/Brasil tracejado) — mais didáticos que as barras agrupadas; `compute_cei_area.py` + `cei_alunos_area.csv` geram a incoerência por área; nuvens nacionais por área em `plot_data/` (restauradas do deck)
- v3 (2026-07-01): **`cei_dificuldade_{LC,CH,CN,MT}.png`** — degrau da dificuldade POR ÁREA, 100% auto-explicativo: instrução de leitura no subtítulo, % em todos os pontos, callout da razão CEI/BR no Fácil e **seta vermelha com a razão no Muito difícil** (LC 1,9× · CH 1,9× · CN 2,4× · MT 2,5×). Rótulo dinâmico: unidade mais alta rotula acima, mais baixa abaixo. Estes são os canônicos p/ apresentação; o facetado `cei_dificuldade.png` fica como visão-resumo.
- Dados: `alunos_cei.csv` (extração), `cei_alunos.csv` (por aluno, anônimo), `cei_habilidades.csv`, `cei_categorias.csv`, `cei_disc.csv`, `cei_resumo.json`, `referencia_nacional.json`, `chutes_counts.json`/`chutes_scatter.csv` (referência nacional)

*Fonte: Microdados ENEM 2025 / INEP · Censo Escolar 2025 (nomes de escola) · "Dados reais ou nada."*
