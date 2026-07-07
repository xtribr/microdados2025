# Estudo Colégio Marista de Natal — ENEM 2025

**Escola:** CO_ENTIDADE `24057134` — COLÉGIO MARISTA DE NATAL (Natal/RN, privada, urbana; nome do Censo Escolar 2025/INEP).
**Amostra:** 171 concluintes com escola declarada (171 presentes nas 4 provas). Alunos anônimos.

## Metodologia
Mesma do estudo CEI (`estudo_cei_natal/LEIA-ME.md`): correção item a item (175 itens válidos) via ITENS_PROVA_2025;
categorias de dificuldade XTRI por co_item; discriminação em faixas de Baker (parâmetro A);
incoerência person-fit = min(erros em fáceis b≤0,6; acertos em difíceis b≥1,6). Pipeline parametrizado:
`config.json` → `compute_escola.py` → `ggplot_escola.R` + `painel_escola.py`.

## Resultados-chave
| | Marista Natal | Brasil (P1) |
|---|---|---|
| Linguagens | 623,0 | 533,4 |
| Humanas | 629,7 | 513,1 |
| Natureza | 619,7 | 500,6 |
| Matemática | **745,3** | 521,2 |
| Redação | 867,3 | — |

- **Alertas (erro acima do Brasil):** CH-H10 (80,7% × BR 73,1%) e CN-H6 (74,3% × 71,1%) — mesmos bolsões vistos nas CEI.
- **Degrau MT:** 84%→44% (Brasil 50%→17%) — **2,6× o Brasil no item pesado**.
- **Incoerência:** média 4,01/aluno (mediana 4, máx 9) — deslizes em itens fáceis.
- **Redação:** gargalo **C1 norma culta** (média 154; só **0,6%** gabaritam) · C5 é a força (190).

- **Testlet LC (Q6–Q10 Azul, 1 texto):** `graficos/testlet_erro.png` + `testlet.csv` — erro médio no bloco 35,3% × Brasil 61,1%; Q8 (H29) é a pedra: 54% × BR 68%.

## Arquivos
`graficos/`: painel_resumo · hab_{LC,CH,CN,MT} · dificuldade_{LC,CH,CN,MT} · discriminacao · incoerencia_{LC,CH,CN,MT} · chutes · redacao_competencias · redacao_200
Dados: alunos.csv (extração) · habilidades/categorias/disc/alunos_proc/alunos_area.csv · redacao_comp.json · resumo.json · referências nacionais copiadas do estudo CEI.

*Fonte: Microdados ENEM 2025 / INEP · Censo Escolar 2025 · "Dados reais ou nada."*
