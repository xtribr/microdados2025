<!-- ===================== SEO / METADADOS (Yoast) ===================== -->
**Título SEO (H1):** Não faça o ENEM na ordem: a prova da PPL pela TRI
**Slug:** nao-faca-enem-na-ordem-ppl-tri
**Meta description (152):** Na 2ª aplicação do ENEM (PPL), questões fáceis e quase impossíveis aparecem lado a lado. Veja a dificuldade por sequência pela TRI e a estratégia certa de prova.
**Focus keyphrase:** ordem das questões no ENEM
**Keyphrases secundárias:** estratégia de prova ENEM · ENEM PPL 2025 · dificuldade das questões ENEM · TRI ENEM · gestão de tempo na prova
**Categoria:** Estratégia ENEM · **Tags:** ENEM, PPL, TRI, estratégia de prova, dados ENEM
**Imagem destacada:** `xtri_ppl_wp_featured.png` — *alt:* "Não faça o ENEM na ordem — dificuldade das questões na PPL 2025 pela TRI (XTRI)."

<!-- ================================================================== -->

# Não faça o ENEM na ordem: a prova da PPL pela TRI

Começar o ENEM na sequência das questões — 1, 2, 3, 4, 5… — parece o caminho natural. **É um dos piores erros de estratégia de prova.** Eu provo isso nas palestras, nas mentorias e nas escolas da consultoria XTRI, e agora trago a evidência também da **2ª aplicação (PPL/reaplicação) do ENEM 2025**, lida pela Teoria de Resposta ao Item (TRI).

A conclusão é direta: a dificuldade **não cresce em ordem**. Numa mesma região do caderno, a prova coloca uma questão quase impossível ao lado de uma das mais acessíveis. Quem resolve linearmente, por hábito ou por orgulho, queima tempo caro nas difíceis e chega cansado nas fáceis — exatamente o oposto do que a TRI valoriza.

## Como medimos a dificuldade da PPL (e por que isso é honesto)

Um ponto técnico importante, porque rigor é o que sustenta uma análise: **o INEP não divulga a taxa de acerto da 2ª aplicação (PPL)**. Então aqui nada é "achismo". Usamos os **parâmetros oficiais de cada item** (discriminação *a*, dificuldade *b* e acerto ao acaso *c*) e calculamos duas coisas pelo modelo logístico de 3 parâmetros (3PL):

- **DIF TRI** = `100 × (1 − P(θ=0))` — o quão difícil o item é na régua da TRI (0 = trivial, 100 = quase impossível).
- **Acerto esperado** = `100 × P(θ=0)` — quanto um **aluno mediano** tende a acertar, segundo o modelo. É um valor previsto, sempre rotulado como "esperado", nunca uma taxa observada.

Toda a análise vem dos Microdados ENEM 2025 / INEP, caderno Azul, e nenhum número foi estimado fora do modelo.

![Dificuldade TRI por posição em cada área da PPL — a dificuldade não cresce em ordem](xtri_ppl_wp_skyline.png)
*A dificuldade por posição (P01→P45) em cada área da PPL. Repare: não há rampa — há picos e vales colados. Fonte: Microdados ENEM 2025/INEP, análise XTRI.*

## Mesma região, dois mundos: os contrastes da PPL Azul

O padrão se repete nas quatro áreas. Em cada uma, separei a **questão mais difícil de uma vizinhança** e a **fácil que está logo ao lado**:

- **Matemática:** a **P03 (H20)** é uma das mais difíceis da prova — DIF 95, cerca de **5%** de acerto esperado — e está a duas casas da **P05 (H1)**, DIF 14, cerca de **86%**.
- **Natureza:** a **P29 (H22)** (DIF 93, ~7%) está **colada** na **P28 (H12)** (DIF 29, ~71%). Adjacentes.
- **Humanas:** a **P25 (H17)** (DIF 82, ~18%) é **vizinha** da **P26 (H3)** (DIF 27, ~73%).
- **Linguagens:** a **P17 (H20)** (DIF 84, ~16%) está a dois passos da **P15 (H10)** (DIF 21, ~79%) — a mais acessível da vizinhança.

![Acerto esperado da questão mais difícil e da fácil vizinha em cada área da PPL](xtri_ppl_wp_contraste.png)
*Mesma região do caderno, retornos opostos. A barra azul é a fácil; a coral, a difícil ao lado. Fonte: Microdados ENEM 2025/INEP, análise XTRI.*

A diferença de retorno entre essas questões vizinhas é, na prática, a diferença entre **subir e estagnar** na escala da TRI.

## A armadilha do mesmo bloco visual

Tem um caso que ilustra a cilada com perfeição. Em Matemática, a **P05 (H1)** — cerca de **86%** de acerto esperado, a mais tranquila da região — está **cercada** pela P03 (DIF 95) e pelas P06 e P07 (DIF 78 e 81). Quem vai linear cansa o cérebro nas brutais, chega na P05 já desgastado e arrisca errar por fadiga o que era, nas suas palavras, **dinheiro na conta**.

## A estratégia certa: prova não é lista numerada

A leitura é a mesma da 1ª aplicação, e é o que ensino aos meus alunos:

1. **Faça uma primeira passada garantindo o que você domina.** Marque as fáceis e médias com segurança, na ordem que o seu repertório pedir — não na ordem do caderno.
2. **Não trave por orgulho.** Gastar 8 minutos numa questão de ~7% de acerto para deixar três de ~70% em branco no fim é o pior trade possível.
3. **Construa um padrão de respostas coerente.** A TRI premia quem acerta de forma consistente as questões compatíveis com o seu nível; ela "desconfia" de acertos isolados em itens muito acima da sua faixa.
4. **Gestão de energia é gestão de nota.** Deixe as difíceis para quando as fáceis já estiverem asseguradas.

## Transparência e método

DIF TRI e acerto esperado derivam dos parâmetros oficiais (a, b, c) de cada item da 2ª aplicação, pelo 3PL com `P(θ=0) = c + (1 − c)/(1 + e^{a·b})`. As cores das figuras seguem os **quartis de dificuldade dentro de cada área** (fácil, médio, difícil, muito difícil), e o selo de discriminação marca o poder de separação do item. A PPL não tem taxa de acerto pública — por isso trabalhamos com o **esperado pelo modelo**, sempre sinalizado. Fonte: Microdados ENEM 2025 / INEP.

## Perguntas frequentes

**Posso pular questões no ENEM?** Pode e deve. Não há penalidade por ordem; o cartão-resposta aceita qualquer sequência. O que conta é acertar — e acertar as compatíveis com o seu nível primeiro.

**A ordem das questões importa para a nota?** A ordem em que você *resolve* não muda a nota diretamente, mas muda **quantas você acerta**: resolver linearmente desperdiça tempo e energia, e isso derruba o resultado.

**O que é "DIF TRI"?** É um índice de dificuldade de 0 a 100 calculado a partir dos parâmetros oficiais do item pela Teoria de Resposta ao Item. Quanto maior, mais difícil.

**A PPL é mais difícil que a aplicação regular?** São provas diferentes, com itens próprios. O que mostramos aqui é que, como na regular, a **dificuldade aparece fora de ordem** — e é isso que define a estratégia.

## Conclusão

A prova da PPL confirma a regra de ouro: **não se faz o ENEM em linha reta.** Quem entende a TRI lê o caderno como um campo de oportunidades, não como uma fila. Garanta as fáceis e médias, blinde os pontos baratos e deixe o orgulho de lado nas questões de 5% de acerto.

Quer ver a dificuldade questão a questão, por área e por caderno? Acesse o estudo completo em **[app.rankingenem.com](https://app.rankingenem.com)**.

*Dados reais ou nada. — XTRI · Microdados ENEM 2025 / INEP.*
