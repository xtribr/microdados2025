# Estudo: Poder discriminatório (parâmetro A) × perfil etário — ENEM 2025

## Pergunta original
Relacionar o poder de discriminação (parâmetro A) de cada área com a faixa etária dos
candidatos (inclusive 70+ anos e "fora da universidade"), avaliar se o ENEM é equilibrado
ou enviesado, e comparar 2024×2025 usando só o parâmetro A.

## Limite estrutural (verificado, não suposto) — define o escopo do estudo
1. **RESULTADOS_2025.csv usa `NU_SEQUENCIAL`; PARTICIPANTES_2025.csv usa `NU_INSCRICAO`** —
   chaves diferentes, sem correspondência. **Não é possível** cruzar idade individual
   com resposta a item nos microdados públicos.
2. **Regular P1 × COP30/BAM usam bancos de itens 100% diferentes** — 0 `co_item` em comum
   entre os dois (verificado linha a linha em ITENS_PROVA_2025.csv). Não dá pra comparar
   o *mesmo* item entre populações de perfil etário diferente.
3. **Os parâmetros A/B/C do banco COP30/BAM não são publicados** no ITENS_PROVA_2025.csv —
   só o banco Regular tem essas colunas preenchidas. Não dá nem para comparar o nível
   agregado de discriminação dos dois bancos.
4. **2024: parâmetros OFICIAIS (3PL) seguem indisponíveis.** O único `ITENS_PROVA_2024.csv`
   localizado está em container iCloud cujo app de origem foi desinstalado (`brctl`:
   "SYNC DISABLED (app not installed)") — toda tentativa de leitura resulta em timeout
   imediato. **Resolvido de forma alternativa** (ver seção seguinte): o usuário localizou
   `MICRODADOS_ENEM_2024.csv` completo (RESULTADOS, 1,68GB) em
   `/Volumes/HD/apps/RANKING ENEM/microdados-2024/`, o que permitiu calcular um **proxy**
   honesto de discriminação para os dois anos.

## Comparação 2024×2025 (proxy: correlação ponto-bisserial)
Como os parâmetros A/B/C oficiais de 2024 são irrecuperáveis, calculei a **correlação
ponto-bisserial** (acerto do item × nota da área) — proxy clássico e real de discriminação,
**não é o parâmetro A do 3PL**, mas mede o mesmo conceito e foi calculado de forma
**idêntica** nos dois anos a partir de `TX_RESPOSTAS_*`/`TX_GABARITO_*` (que vêm embutidos
na própria linha do aluno em ambos os arquivos — não depende do ITENS_PROVA).
Amostra: 150.000 presentes/área/ano. Achado: **CH caiu de 0,360 para 0,322** (maior queda,
-0,038); MT subiu (+0,019); LC e CN ficaram estáveis. Nota técnica: o cálculo usa todas as
posições com gabarito-letra da linha do aluno — os 2 itens anulados por "problema de
convergência" (que mantêm gabarito-letra) entram no cálculo; os 3 anulados por vazamento
(gabarito 'X') são excluídos automaticamente. `g4_bisserial_2024_2025.png`.

## O que o estudo prova (100% real)
- **Retrato etário 2025**: distribuição completa por `TP_FAIXA_ETARIA` (questionário
  obrigatório, 100% preenchido pela 1ª vez). 1.674 candidatos com 70+ anos; 3.834 entre
  66-70. Nenhum candidato de 46+ anos é treineiro (`IN_TREINEIRO`=0 em 100% dos casos).
- **COP30/BAM tem perfil etário comprovadamente mais velho**: 26,3% têm 26+ anos contra
  14,8% no resto do Brasil — quase o dobro (verificado por `CO_MUNICIPIO_PROVA` ∈
  {Belém, Ananindeua, Marituba} em PARTICIPANTES, sem depender de RESULTADOS).
- **Parâmetro A por área (banco Regular, caderno Azul, 2025)**: nenhuma área tem item
  "baixa" ou "muito baixa" discriminação. LC tem a maior mediana (2,30) e MT a menor
  (1,89), mas mesmo MT tem 84% dos itens em "alta" ou "muito alta".

## Metodologia
`compute_estudo.py`: parte1 varre PARTICIPANTES_2025.csv (4,8M linhas) para demografia;
parte2 lê ITENS_PROVA_2025.csv (pequeno) para os parâmetros A/B/C do banco Regular por área
(dedupe por co_item, exclui anulados). `ggplot_estudo.R`: G1 (distribuição etária),
G2 (COP30 × Regular), G3 (dot-plot do A por área com faixas de Baker). `painel_sintese.py`:
card-resumo com tabela + limitações + conclusão (estilo xtri_deck).

## Arquivos
- `graficos/g1_distribuicao_etaria.png`, `g2_cop30_vs_regular_idade.png`,
  `g3_parametro_a_por_area.png`, `painel_sintese.png`
- `demografia_2025.json`, `discriminacao_areas.json`, `discriminacao_itens.csv`

*Fonte: Microdados ENEM 2025 / INEP. "Transformamos dados em aprovações."*
