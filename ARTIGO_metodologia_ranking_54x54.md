# Comparando escolas de forma justa: o ranking "54×54" na amplitude de uma escola-base

### Como ranquear colégios do Rio Grande do Norte no ENEM 2025 sem que o tamanho da escola distorça o resultado

---

## O problema: ranking de escola é quase sempre injusto

Rankings escolares do ENEM costumam comparar a **média geral** de cada escola. O problema é
que essa média mistura duas coisas muito diferentes: a **qualidade** do ensino e o **tamanho/seletividade**
da escola. Uma escola com 340 alunos e outra com 54 não competem em pé de igualdade — a maior
tem mais chances de "puxar" a média com casos extremos, e a comparação direta esconde mais do
que revela.

Quando se quer responder a uma pergunta específica — *"entre alunos de desempenho parecido,
qual escola entrega mais?"* — é preciso controlar dois fatores antes de comparar:

1. **O tamanho do grupo** (todas as escolas avaliadas com o mesmo número de alunos); e
2. **A faixa de desempenho** (todas comparadas dentro do mesmo intervalo de notas).

Este artigo descreve uma metodologia que faz exatamente isso, aplicada aos dados reais do
**ENEM 2025** para escolas do **Rio Grande do Norte**, usando o **Colégio Ciências Aplicadas
(Natal/RN)** como *escola-base* de referência.

---

## A ideia central: recorte "54×54" na amplitude da escola-base

A escola-base tinha **54 alunos** com as cinco notas completas (Ciências da Natureza, Ciências
Humanas, Linguagens, Matemática e Redação). A média das cinco notas desses alunos variava de
**613,5 a 843,5 pontos** — esse intervalo é a **amplitude da base**.

A metodologia consiste em três regras:

> **1. Toda escola entra com exatamente 54 alunos** — o mesmo tamanho da base.
>
> **2. Esses 54 alunos precisam reproduzir a amplitude (a distribuição de médias) da escola-base** —
>    de 613,5 a 843,5.
>
> **3. O ranking é feito pela média das 5 áreas desses 54 alunos.**

Assim, comparam-se sempre **54 alunos contra 54 alunos**, todos dentro da mesma faixa de
desempenho. O que sobra para diferenciar as escolas é a única coisa que interessa: **a qualidade
das notas dentro daquele recorte**.

---

## Passo a passo metodológico

**1. Fonte das notas.** Foram usados os **Microdados do ENEM 2025** do INEP (arquivo
`RESULTADOS_2025.csv`), que trazem, para cada participante (anonimizado por um número sequencial),
o código da escola (`CO_ESCOLA`), a UF da escola e as notas das quatro áreas objetivas mais a
redação. Nenhum dado foi inventado, estimado ou simulado.

**2. Universo.** Selecionaram-se todos os participantes de escolas do **RN** com as **cinco notas
presentes**. Para cada aluno, calculou-se a **média das 5 notas**.

**3. Filtro de amplitude.** Mantiveram-se apenas os alunos cuja média caísse na faixa da base
(**613,5 a 843,5**). No RN, isso resultou em **5.204 alunos** distribuídos por dezenas de escolas.

**4. Elegibilidade da escola.** Para garantir o recorte de 54, só entraram no ranking as escolas
com **pelo menos 54 alunos dentro dessa faixa** — ou seja, escolas do mesmo "porte" da base.
Foram **27 escolas**.

**5. Seleção dos 54 (espelhamento da distribuição).** A base tem 54 médias específicas. Para cada
escola, percorreu-se cada uma dessas 54 médias e selecionou-se o aluno da escola (dentro da faixa)
com a **média mais próxima**, sem repetir alunos. É uma forma de **pareamento por vizinho mais
próximo** (*nearest-neighbor matching*), técnica clássica de comparação estatística para tornar
dois grupos comparáveis. O resultado: cada escola fica com 54 alunos que **cobrem a mesma
amplitude** da base.

**6. Ranking.** Calculou-se a média das 5 áreas desses 54 alunos por escola e ordenou-se do maior
para o menor.

**7. Nomes das escolas.** Os microdados do ENEM divulgam apenas o **código** da escola
(`CO_ESCOLA`), nunca o nome. O de-para código → nome foi feito pelo **Catálogo de Escolas do
INEP / Censo Escolar**, consultado via **QEdu**.

---

## Por que o método não "empata todo mundo"

Uma objeção natural é: *"se você força todas as escolas a ter a mesma distribuição da base, todas
não ficam com a mesma média?"* Não — e esse é o ponto sutil.

O pareamento só consegue espelhar a base **se a escola tiver alunos naquela faixa de nota**.
Escolas mais fortes têm alunos sobrando em todo o intervalo, inclusive perto do teto (médias acima
de 800), e por isso quase encostam na base. Escolas mais fracas **não têm alunos suficientes no
topo da faixa**: quando o método procura alguém com média ~840, encontra, no máximo, alguém com
~705. Isso puxa a média dos 54 para baixo.

O resultado é um ranking com **amplitude real de 77 pontos** (de 726,4 a 649,4) — longe de um
empate. A coluna "maior média dos 54" de cada escola explica visualmente a posição: quem não
alcança o topo da faixa, cai.

---

## Resultados (ENEM 2025, RN — 27 escolas, recorte 54×54)

| Pos. | Escola | Cidade | Média (5 áreas, 54 alunos) |
|----:|--------|--------|:----:|
| **1º** | **Colégio Ciências Aplicadas (BASE)** | Natal | **726,4** |
| 2º | Colégio Marista de Natal | Natal | 725,6 |
| 3º | Centro de Educação Integrada (CEI Romualdo) | Natal | 725,4 |
| 4º | Colégio Porto | Natal | 724,1 |
| 5º | IFRN – Campus Natal Central | Natal | 723,6 |
| 6º | IFRN – Campus Mossoró | Mossoró | 716,1 |
| 7º | Centro de Educação Integrada (CEI Roberto Freire) | Natal | 713,8 |
| 8º | Colégio Salesiano Dom Bosco | Parnamirim | 712,7 |
| 9º | Colégio Diocesano Santa Luzia | Mossoró | 711,1 |
| 10º | Centro de Educação Integrada Mais (CEI Mais) | Natal | 704,7 |

*(O ranking completo, com as 27 escolas até o IFRN – Campus Macau (649,4) e as médias por área,
está na planilha de resultados.)*

**Leitura honesta dos números.** A escola-base lidera por construção parcial (a faixa é a régua
dela), mas o que chama atenção é como o pelotão de elite de Natal — Marista, CEI, Porto, IFRN
Central — fica praticamente colado, separado por menos de 3 pontos. Isso indica que, **dentro de
uma mesma faixa de desempenho e com turmas do mesmo tamanho, essas escolas entregam resultados
estatisticamente muito próximos**. As diferenças maiores aparecem mais abaixo, à medida que as
escolas perdem capacidade de preencher a parte alta do intervalo.

---

## Limitações (para usar o ranking sem exagerar)

- **A faixa é a régua da base.** Como o intervalo 613,5–843,5 vem da própria escola-base, ela
  participa com 100% dos seus alunos, enquanto as demais têm cortados os alunos acima de 843,5.
  Em escolas de elite com muitos alunos no topo, esse corte **subestima** o nível real da escola.
  Portanto, este é um **ranking de comparação dentro da mesma faixa**, e **não** o ranking ENEM
  tradicional da escola inteira.
- **Não é causal.** O método controla tamanho e faixa de nota, mas não controla perfil
  socioeconômico, seletividade de ingresso ou treineiros. Ele mostra *correlação de desempenho
  comparável*, não "valor agregado" pela escola.
- **Recorte de um ano.** Reflete apenas o ENEM 2025; tendências exigem múltiplos anos.

---

## Conclusão

Comparar escolas pela média bruta é como comparar atletas sem separar por categoria de peso. O
recorte **"54×54 na amplitude da base"** impõe uma categoria comum — mesmo número de alunos, mesma
faixa de desempenho — e deixa o ranking revelar o que de fato distingue as escolas naquele recorte.
O método é **transparente, reprodutível e baseado em dados oficiais**, e pode ser replicado para
qualquer escola-base, estado ou ano do ENEM.

---

## Fontes

- **INEP — Microdados do ENEM 2025.** Instituto Nacional de Estudos e Pesquisas Educacionais
  Anísio Teixeira (INEP/MEC). Arquivo `RESULTADOS_2025.csv`. Portal de Dados Abertos do INEP:
  https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
- **INEP — Catálogo de Escolas / Censo Escolar da Educação Básica** (de-para código da escola →
  nome). https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/inep-data/catalogo-de-escolas
- **QEdu** (Iede / Fundação Lemann), consulta dos nomes das escolas por código INEP:
  https://qedu.org.br
- **Referência metodológica — pareamento por vizinho mais próximo (nearest-neighbor matching):**
  Stuart, E. A. (2010). *Matching Methods for Causal Inference: A Review and a Look Forward.*
  Statistical Science, 25(1), 1–21.

*Dados anonimizados: os microdados do ENEM não divulgam nomes de alunos. As notas são reais; os
participantes são identificados apenas por número sequencial anônimo do INEP.*

*Elaboração: XTRI — análise dos microdados ENEM 2025.*
