# Estudo TRI — Valor marginal do acerto & A questão que mais vale (ENEM 2025)

Dois estudos sobre **onde a TRI "presta atenção"** no seu desempenho — ambos derivam da função de informação.
Fonte: Microdados ENEM 2025 / INEP. Caderno Azul para parâmetros de item; amostra Regular (100 mil/área) para a conversão acertos→nota.

## Estudo 1 — Cada acerto a mais não vale a mesma coisa
**Arquivo:** `estudo1_valor_marginal.png`
Mede quanto a **mediana da nota** sobe ao passar de N para N+1 acertos (por área).

Achados (o valor de +1 acerto varia de ~7 a ~25 pontos):
- **Existe uma "zona cara"** por volta de **9–13 acertos**, onde cada acerto a mais vale mais: LC 9→10 = **19,2 pts**; CN 9→10 = 18,9; CH 12→13 = 17,8; **MT 11→12 = 25,5 pts** (o acerto mais caro de toda a prova).
- **Vale em "U":** depois cai para um vale na faixa de **20–30 acertos** (cada acerto ~7–10 pts, os mais "baratos") e volta a subir lá no topo (efeito do teto da escala; nos extremos há mais ruído, mesmo com n≥80).
- **Matemática é a área onde cada acerto vale mais** em quase toda a faixa.

Leitura prática: sair do básico (≈10 acertos) rende muito ponto por acerto; no "miolo" (20–30) o ganho por questão é menor. E, ponto por ponto, **Matemática paga melhor cada acerto**.

## Estudo 2 — A questão que mais vale acertar depende do SEU nível
**Arquivo:** `estudo2_questao_que_mais_vale.png`
Para cada nível de proficiência, qual item tem maior **informação** — ou seja, qual questão, se você virasse de errado para certo, mais moveria sua nota.

Achado central (a "campeã" acompanha o nível — Matemática):
| Seu nível | Questão que mais vale | Dificuldade TRI do item | Discriminação (a) |
|---|---|---|---|
| ~450 (abaixo da média) | **Q168** (hab H4) | 532 | 1,42 |
| ~600 (boa) | **Q147** (hab H24) | 597 | 2,50 |
| ~750 (alta) | **Q177** (hab H12) | 737 | 3,04 |

Em Linguagens, o mesmo padrão: ~450 → Q26 (dif. 440) · ~600 → Q38 (dif. 598, **a=4,75**, super discriminativa) · ~750 → Q30 (dif. 672).

Lição (TRI pura): **a questão que mais sobe a sua nota não é a mais difícil da prova — é a que está no seu nível** (dificuldade ≈ sua proficiência) E discrimina bem. Item fácil demais ou difícil demais quase não move seu resultado. É a função de informação em ação: cada item "mede" melhor quem está perto da sua dificuldade.

## Como vira conteúdo
- Estudo 1 → card "cada acerto vale diferente; em Matemática o acerto paga mais".
- Estudo 2 → card/carrossel "a questão que mais vale acertar é a do seu nível" (gancho anti-"vou caçar a mais difícil").
