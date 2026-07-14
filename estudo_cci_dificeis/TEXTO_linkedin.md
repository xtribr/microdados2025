# As curvas das questões mais difíceis do ENEM 2025 — comentário (LinkedIn)

## Post principal

"Difícil" não é uma coisa só. A questão mais difícil do ENEM 2025 é, ao mesmo tempo, a que menos mede.

Peguei os parâmetros oficiais da TRI (Microdados ENEM 2025 / INEP) e desenhei a Curva Característica do Item — a CCI — do item de maior dificuldade (maior b) de cada área. Cada curva responde a uma pergunta simples: dada a nota TRI do candidato, qual a probabilidade de ele acertar aquele item?

Três parâmetros governam cada curva:
→ b (dificuldade): onde, na escala de nota, a curva "sobe". Quanto mais à direita, mais difícil.
→ a (discriminação): a inclinação. Curva íngreme separa bem quem domina de quem não domina; curva "deitada" quase não distingue.
→ c (acerto ao acaso): o piso. É a probabilidade de acerto de quem não faz ideia — o efeito do chute em item de 5 alternativas.

O que as quatro curvas contam:

Ciências Humanas — Q66 (a=1,73 · b=2,72 · c=0,14). O item difícil bem-comportado. Discriminação altíssima (na escala de Baker, ≥1,70 é "muito alta") e piso de chute baixo (14%). A curva é íngreme: sobe rápido em torno da nota 772. É difícil de verdade e mede bem — sobe de nível quem realmente sabe.

Matemática — Q160 (a=0,93 · b=4,24 · c=0,12). A mais difícil da prova inteira: dificuldade equivalente à nota 924, muito além de onde quase qualquer candidato está. Só 15% acertaram. Mas repare na inclinação: a curva é rasa. Mesmo um candidato de nota 1000 tem só ~71% de chance de acertar. Discriminação apenas moderada (a=0,93). Tradução psicométrica: como o item "vive" numa faixa de nota praticamente desabitada e separa pouco, ele quase não acrescenta informação à prova — a informação de um item é máxima perto do seu b e cresce com a². É difícil, sim; mas difícil e pouco útil.

Ciências da Natureza — Q119 (a=1,32 · b=2,88 · c=0,29). O detalhe que engana: piso de chute de 0,29. Quem chuta tem quase 1 em 3 de acertar — acima do 1/5 esperado num item de 5 alternativas. Os 32% de acerto observados são, em boa parte, sorte: a curva já nasce em 29%. "Acertou" aqui mede menos domínio do que parece.

Linguagens — Q17 (a=1,57 · b=1,95 · c=0,24). A "mais difícil" de LC é a menos difícil entre as quatro (nota 695). Boa discriminação, mas c=0,24 também deixa espaço para o chute.

A lição pra quem constrói e pra quem faz prova: dificuldade alta não é sinônimo de boa questão. O item que separa os melhores não é o mais impossível — é o mais íngreme (alto a) e com menor piso de chute (baixo c). O ENEM 2025 tem um exemplar de cada caso.

Dados: Microdados ENEM 2025 / INEP · Caderno Azul, 1ª aplicação · modelo logístico de 3 parâmetros (3PL), D=1. Dificuldade TRI = b×100+500. Escala de discriminação: Baker, F. B. (2001), The Basics of Item Response Theory, 2ª ed.

— Alexandre Emerson · X-TRI

---

## Números de apoio (não precisa ir no post)

| Área | Questão | a | b | c | dif. TRI | % acerto | P(nota 1000) |
|------|---------|-----|-----|-----|---------|----------|--------------|
| Linguagens | Q17 (LC-H18) | 1,57 | 1,95 | 0,24 | 695 | 29,8% | ~99% |
| C. Humanas | Q66 (CH-H24) | 1,73 | 2,72 | 0,14 | 772 | 17,4% | ~98% |
| C. Natureza | Q119 (CN-H2) | 1,32 | 2,88 | 0,29 | 788 | 31,7% | ~95% |
| Matemática | Q160 (MT-H19) | 0,93 | 4,24 | 0,12 | 924 | 15,0% | ~71% |

- No ponto b, por construção P = (1+c)/2 → CH Q66: 57%; MT Q160: 56%; CN Q119: 65%; LC Q17: 62%.
- Baker (a): CH 1,73 = muito alta; LC 1,57 = alta; CN 1,32 e MT 0,93 = moderada.
- Item mais difícil da prova = MT Q160 (b=4,24). Item que melhor discrimina entre os quatro = CH Q66 (a=1,73).
- Maior "armadilha do chute" = CN Q119 (c=0,29): 32% de acerto inflado pelo piso.
