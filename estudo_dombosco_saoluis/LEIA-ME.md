# Estudo Colégio Dom Bosco (São Luís/MA) — ENEM 2025

**Escola:** CO_ENTIDADE `21010331` — COLÉGIO DOM BOSCO LTDA (São Luís/MA, privada, urbana; nome do Censo Escolar 2025/INEP).
**Amostra:** 56 candidatos extraídos → **51 processados** (50 presentes nas 4 provas). ⚠ n pequeno: percentuais por habilidade têm mais ruído. Alunos anônimos.

## Metodologia
Mesma do estudo CEI (`estudo_cei_natal/LEIA-ME.md`); pipeline parametrizado `config.json` → `compute_escola.py` → `ggplot_escola.R` + `painel_escola.py`.

## Resultados-chave
| | Dom Bosco | Brasil (P1) |
|---|---|---|
| Linguagens | 602,3 | 533,4 |
| Humanas | 592,5 | 513,1 |
| Natureza | 578,5 | 500,6 |
| Matemática | **720,3** | 521,2 |
| Redação | 845,5 | — |

- **Alertas (erro acima do Brasil): 6 habilidades, concentradas em CN** — CN-H6 (**86,0%** × BR 71,1%), CN-H30 (50,0×43,9), CN-H2 (70,0×68,3), LC-H3 (56,9×56,1)…
- **Degrau MT:** 80%→36% (Brasil 50%→17%) — **2,1× o Brasil no item pesado**.
- **Incoerência:** média 4,30/aluno (mediana 4, máx 10).
- **Redação:** gargalo **C1 norma culta** (média 155; **0,0%** gabaritam) · nota: C5 (173) abaixo de C4 (177), diferente do padrão das outras escolas estudadas.

- **Testlet LC (Q6–Q10 Azul, 1 texto):** `graficos/testlet_erro.png` + `testlet.csv` — erro médio no bloco 41,2% × Brasil 61,1%; Q8 (H29): 57% × BR 68%.

## Arquivos
`graficos/`: painel_resumo · hab_{LC,CH,CN,MT} · dificuldade_{LC,CH,CN,MT} · discriminacao · incoerencia_{LC,CH,CN,MT} · chutes · redacao_competencias · redacao_200
Dados: alunos.csv (extração) · habilidades/categorias/disc/alunos_proc/alunos_area.csv · redacao_comp.json · resumo.json · referências nacionais copiadas do estudo CEI.

*Fonte: Microdados ENEM 2025 / INEP · Censo Escolar 2025 · "Dados reais ou nada."*
