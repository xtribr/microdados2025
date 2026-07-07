# Legendas explicativas — Deck ENEM 2025 (Estudo XTRI)

> Uma legenda por gráfico: **o que mostra**, **como ler** e o **destaque**. Fonte de todos: **Microdados ENEM 2025 / INEP** (itens, notas TRI e redação). Pode usar como nota de palestra ou legenda de post. Prof. Alexandre Emerson — XTRI.

---

## 1. Redação — a queda da C2

**`g02a_c2_hero.png` — A C2 foi a que mais caiu.**
Compara a média nacional da **Competência 2** (compreensão do tema e desenvolvimento) entre 2024 e 2025: caiu de **152,53 → 136,97**, uma perda de **−15,6 pontos**. Isso é **2,5× a queda média** das outras quatro competências. Leitura: a C2, que vinha estável, virou o epicentro da queda de 2025 — o candidato entendeu menos o que a proposta pedia.

**`g02b_comp_5.png` — As 5 competências, 2024 × 2025.**
Barras lado a lado por competência. Todas caíram, mas em ordem muito diferente: **C1 −5,6 · C2 −15,6 · C3 −4,8 · C4 −8,7 · C5 −5,6**. Leitura: a queda não foi geral e uniforme — concentrou-se na C2 (compreensão do tema). É onde o professor deve focar em 2026.

**`g02c_status_2025.png` — Onde a redação dá problema.**
Distribuição de todas as redações por situação: **93,9% válidas** (3.245.696). Entre os problemas: **em branco 3,33%** (134.329), **cópia do texto motivador 1,59%** (54.860), **texto insuficiente 0,49%**, **fuga ao tema 0,39%**, **não atendimento ao tipo textual 0,16%**, **parte desconectada 0,10%** e **anuladas 0,09%**. Leitura: o "zero" mais comum não é conteúdo ruim — é **não escrever** (branco) ou **copiar** o motivador.

**`g02d_faixas_2025.png` — Onde estão as notas.**
Distribuição das **3.245.696 redações válidas** em faixas de 100 pontos. O pico está em **600–699 (23,8%)**, seguido de 500–599 (22,9%); 800–899 são 11,7% e 900–999 apenas 5,3%. **Só 10 pessoas** no país tiraram **1000**. Leitura: a nota "boa" de redação (700+) é bem mais rara do que se imagina; o 1000 é quase inexistente.

---

## 2. A redação prevê a prova objetiva?

**`g03a_ggplot_redacao_r2.png` — Quanto da nota objetiva a redação "explica".**
Mostra o R² (variância explicada) entre a nota de redação e cada prova objetiva, por área: de **24% (Natureza) a 31% (Matemática e Linguagens)**. Leitura: a redação prevê **só cerca de um quarto a um terço** da nota objetiva — correlação real, mas **moderada**. Quem vai bem na redação tende a ir bem na prova, mas está longe de ser regra.

**`g03b_ggplot_redacao_densidade.png` — A nuvem é larga.**
Gráfico de densidade nota de redação × nota TRI da área, com a correlação r por área (**MT 0,56 · LC 0,55 · CH 0,51 · CN 0,49**; n = 3.067.856). Leitura: a nuvem é dispersa — para uma mesma nota de redação há um leque enorme de notas objetivas. Redação **não "entrega" a nota** da prova; são competências parcialmente distintas.

---

## 3. Acerto não é nota (TRI)

> As quatro (LC, CH, CN, MT) mostram a mesma verdade da TRI: **o mesmo número de acertos gera notas diferentes**. Cada ponto é um candidato; eixo X = nº de acertos, eixo Y = nota TRI; a **cor** indica a fração de itens **difíceis** que ele acertou (arco-íris). Leitura: acertar as **difíceis** empurra a nota para cima — dois alunos com o mesmo total de acertos podem estar separados por dezenas de pontos.

**`g01_ggplot_scatter_LC.png` — Linguagens** (45 itens). A dispersão vertical mostra que "número de acertos" não define a nota; a coerência (acertar difícil, não fácil) define.

**`g01_ggplot_scatter_CH.png` — Ciências Humanas** (45 itens). Mesmo padrão; a faixa de notas para um mesmo total de acertos é ampla.

**`g01_ggplot_scatter_CN.png` — Ciências da Natureza** (42 itens após anulações). O topo do eixo X coincide com o total real de itens.

**`g01_ggplot_scatter_MT.png` — Matemática** (43 itens). É onde o efeito é mais forte: acertar as difíceis vale muito.

---

## 4. Dificuldade ao longo do caderno

> Por área, mostra o **parâmetro B (dificuldade)** de cada questão na ordem do caderno. Cada rótulo é a **habilidade (H)** daquela posição; a **cor** é o nível de dificuldade (fácil→muito difícil) e a **linha vermelha** é a tendência (loess). Leitura: revela se a prova "esquenta" no meio, no fim, ou oscila — útil para estratégia de tempo.

**`g04_dificuldade_posicao_LC.png` — Linguagens.** Dificuldade mais irregular; picos pontuais (ex.: o testlet Q6–10).
**`g04_dificuldade_posicao_CH.png` — Ciências Humanas.** Oscila ao longo do caderno.
**`g04_dificuldade_posicao_CN.png` — Ciências da Natureza.** Tendência de subida no miolo.
**`g04_dificuldade_posicao_MT.png` — Matemática.** Patamar de dificuldade mais alto do que as outras áreas em toda a extensão.

---

## 5. Taxa de erro por habilidade

> Por área, o **percentual de erro nacional** de cada habilidade (H), ordenado da que menos para a que mais se erra. Leitura simples e acionável: **onde a barra é maior = onde a turma mais erra = onde focar** o ensino em 2026.

**`g05_taxa_erro_LC.png` — Linguagens.**  **`g05_taxa_erro_CH.png` — Humanas.**  **`g05_taxa_erro_CN.png` — Natureza.**  **`g05_taxa_erro_MT.png` — Matemática.**
Cada barra é uma habilidade da matriz de referência; use para priorizar conteúdo pelas habilidades de maior erro na sua área.

---

## 6. As três provas têm a mesma dificuldade?

**`g06_comparacao_provas.png` — Dificuldade média por aplicação.**
Barras da **dificuldade média (B)** do caderno Azul em três aplicações: **Regular (1ª) · COP30/BAM · PPL/2ª aplicação**. Valores: **LC 0,72 / 0,85 / 0,67 · CH 1,07 / 1,01 / 0,83 · CN 1,19 / 1,23 / 1,19 · MT 1,74 / 1,90 / 1,90**. Leitura: **Matemática é disparado a mais difícil** em qualquer aplicação; as provas são calibradas para dificuldade parecida dentro de cada área. **Ressalva:** o INEP não separa PPL de reaplicação — a barra "2ª aplicação" é a reaplicação; usamos só parâmetros de item (não notas de PPL).

---

## 7. Acerto → nota (tabelas de consulta)

> Por área, tabela de referência: para cada **número de acertos**, a **frequência** de alunos e a nota TRI **mínima, mediana e máxima** que aquele total gerou (Regular P1, população completa). Leitura: é a "tabela de conversão" real — mostra o intervalo de notas possível por total de acertos (reforçando que acerto não é nota única).

**`g07_tabela_acerto_nota_LC.png` · `..._CH.png` · `..._CN.png` · `..._MT.png`**
Consulte a linha do total de acertos do aluno; a distância entre a coluna **Mín** e **Máx** é o "prêmio" por acertar as questões certas.

---

## 8. Chutes e coerência (person-fit)

**`g08a_chutes_scatter.png` — Chute deixa marca.**
Cada ponto é um aluno; mostra a relação entre desempenho e **incoerência** — definida como o mínimo entre *erros em questões fáceis* e *acertos em questões difíceis* (o padrão típico de quem chutou/teve sorte alternada). Leitura: para um mesmo número de acertos, mais incoerência tende a puxar a nota TRI **para baixo**.

**`g08b_chutes_insight.png` — Mesma quantidade de acertos, notas diferentes.**
O caso limpo: dois alunos com **90 acertos** cada. O de **incoerência 1** tira ≈ **606**; o de **incoerência 10** tira ≈ **582** — **~24 pontos a menos** só pela incoerência do padrão de respostas. Leitura: a TRI "desconfia" de acertos incoerentes; consistência vale nota.

---

## 9. Inglês × Espanhol

**`g09a_ingles_espanhol_curva.png` — Mesma quantidade de acertos, quem faz espanhol tira um pouco mais.**
Curva de nota média por número de acertos, separando os dois idiomas. Leitura: no bloco de língua, o **espanhol rende ligeiramente mais por acerto** que o inglês.

**`g09b_casos_reais_lingua.png` — Casos reais + o paradoxo da seleção.**
Alunos reais com o mesmo desempenho (3/5 no bloco de língua): a **25 acertos** o espanhol tira **+5,4**; a **30**, **+8,3**; a **35**, **+12,3**. **Mas** a média geral do inglês (**553**) é maior que a do espanhol (**509**) — porque **60,2%** fazem inglês e são, em média, alunos mais fortes (**39,8%** fazem espanhol). Leitura: a vantagem aparente do inglês é **seleção de quem escolhe**, não vantagem da prova.

---

## 10. Maiores TRIs por estado

**`g10a_top_uf_leaderboard.png` — O melhor aluno de cada UF + a escola.**
Ranking da maior **média das 4 provas objetivas** por estado, com a **escola** do aluno (nome vindo do Censo Escolar 2025; aluno anônimo). Topo: **PI 843,0** (Instituto Dom Barreto), **RS 840,4**, **RN 839,3**, **BA 838,7** (Bernoulli)… Leitura: **26 das 27** UFs têm o melhor aluno na **rede privada**; a única exceção é **RR (752,1)**, num colégio **federal** (Aplicação da UFRR).

**`g10b_top_uf_barras.png` — O mesmo ranking em barras**, colorido pela rede da escola. Reforça visualmente o domínio da rede privada no topo de cada estado.

---

## 11. Testlet de Linguagens (Q6–Q10)

> As **Q6 a Q10 do caderno Azul (P1)** derivam de **um único texto** — a crônica *"De próprio punho"* (formato *testlet*). Os quatro cards respondem "como a turma absorveu esse formato".

**`g11_testlet_linguagens.png` — Taxa de erro do testlet.**
Erro por questão: **Q6 49,4% · Q7 53,5% · Q8 68,3% · Q9 68,5% · Q10 65,9%**. Média do bloco **61,1%**, contra **52,2%** no resto de Linguagens (Q11–45). Leitura: o testlet foi ~9 pontos mais difícil que o resto da prova, e o erro **sobe** dentro do bloco.

**`g11b_testlet_narrativa.png` — A escada, com o enunciado de cada questão.**
Mostra o que cada questão pedia: reconhecer gênero/tipo (Q6–Q7, erro 49–54%) versus interpretar a tese e a síntese da autora (Q8–Q10, erro 66–69%). Leitura: o mesmo texto; o que subiu o erro foi a **profundidade de leitura exigida** (+14,8 pontos ao passar do reconhecimento para a interpretação).

**`g11c_testlet_AxB.png` — Plano discriminação × dificuldade.**
Cada ponto é uma questão de LC no plano **A (discriminação) × B (dificuldade)**. Os 5 do testlet estão **difíceis E com discriminação muito alta** (acima de A=1,70 de Baker). Leitura: a dificuldade do testlet **informa** — separa quem sabe de quem não sabe; não é erro "aleatório".

**`g11d_testlet_tabela.png` — Os parâmetros lado a lado.**
Tabela com **A, B, C, Dificuldade TRI, erro e veredito** das 5 questões. Leitura: todas com A muito alta — Q6–Q8 "difícil/muito difícil + afiado", Q9–Q10 "muito difícil + navalha" (A 3,44 e 3,67). Erro alto que é **sinal, não ruído**.

---

## 12. Discriminação (A) por área

**`g12_top_discriminacao.png` — A questão mais discriminativa de cada área (P1, Azul).**
A campeã de **parâmetro A** (poder de separar quem sabe) por área: **CN — Q120** (Física, cinemática/sensor de movimento) com **A = 6,00**, a mais "navalha" da prova; **LC — Q4** (Inglês, *"snowflake generation"*) A = 4,90; **CH — Q50** (Filosofia, justiça × direito em Derrida) A = 4,66; **MT — Q167** (custo de combustível GNV × gasolina) A = 3,86. Leitura: são as questões que mais "ordenam" os alunos. **Ressalvas:** o número da questão é o do caderno **Azul** (A é o mesmo em todas as cores); o campeão de LC é um item de **Inglês** (respondido só por quem escolheu inglês).

---

*Fonte de todos os gráficos: Microdados ENEM 2025 / INEP. Estudo XTRI — Prof. Alexandre Emerson Melo de Araújo. "Dados reais ou nada."*
