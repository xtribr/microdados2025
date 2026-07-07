# Ranking dos colégios MARISTA do Brasil — ENEM 2025

**Pergunta:** qual a colocação do Colégio Marista de Natal entre todos os Maristas do país?

**Resposta: 2º lugar entre 70 escolas Maristas com participantes no ENEM 2025.**
Só perde para o Colégio Marista Dom Silvério (Belo Horizonte/MG).

## Metodologia
1. **Censo Escolar 2025 / INEP** (`Tabela_Escola_2025.csv`): todas as escolas do Brasil com
   "MARISTA" no nome (`NO_ENTIDADE`) → 98 escolas.
2. **Microdados ENEM 2025 / INEP** (`RESULTADOS_2025.csv`): alunos dessas escolas
   (`CO_ESCOLA`) com as **5 notas presentes e > 0** (CN, CH, LC, MT, Redação) → 4.514 alunos
   em 70 escolas.
3. Ranking pela **média das 5 notas** por escola (média das médias individuais).

As 28 escolas do Censo sem alunos no ranking são, em 27 casos, unidades sem Ensino Médio
(educação infantil/fundamental, centros sociais, EJA). A exceção é o Colégio Marista Patos
de Minas (tem EM no Censo, mas nenhum aluno com as 5 notas nos microdados 2025).

**Ressalva:** o filtro pega tudo que tem "MARISTA" no nome — inclui os Centros
Educacionais/Sociais Maristas (unidades gratuitas da rede) e possivelmente escolas fora da
rede oficial (ex.: "Escola Kingdom Marista"). É ranking bruto por média — sem controle de
tamanho/seletividade (diferente da metodologia 54×54).

## Destaques — Marista Natal (CO_ESCOLA 24057134)
- 171 alunos com 5 notas (2ª maior delegação, atrás do Rosário/POA com 238)
- Média das 5 notas: **697,0** (líder Dom Silvério/BH: 703,1)
- **1º lugar em Redação** entre todos os Maristas: **867,3**
- Matemática 745,3 (2º, atrás do Dom Silvério com 761,7)

## Arquivos
- `compute_maristas.py` — script (reproduzível)
- `ranking_maristas_brasil_enem2025.csv` — ranking completo (70 escolas)
- `maristas_censo_sem_alunos_enem.csv` — 28 escolas do Censo sem alunos no ENEM

Fonte: Microdados ENEM 2025 e Censo Escolar 2025 / INEP.
