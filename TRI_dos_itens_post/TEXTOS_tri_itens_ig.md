# Post IG "TRI dos itens" — 2 artes (feed 1080×1350 + story 1080×1920)

Versões Instagram do post de WordPress (`POST_WORDPRESS_tri_itens.md`).
Geradas por `tri_itens_ig.py`. Dado real: `TRI_ITENS_AZUL_ENEM2025.xlsx` (caderno Azul).

| Arquivo | Formato | Conteúdo |
|---|---|---|
| `xtri_tri_itens_capa_feed.png` / `_story.png` | 1080×1350 / 1080×1920 | Faixa de dificuldade por área + a mais brutal e a mais fácil |
| `xtri_tri_itens_scatter_feed.png` / `_story.png` | 1080×1350 / 1080×1920 | Dispersão dificuldade × acerto dos 175 itens |

Sugestão: carrossel de 2 cards (capa → scatter).

---

## 1) CAPA — legenda (feed)

A questão mais brutal do ENEM 2025 tem dificuldade TRI 923,7. A mais fácil, 440,4.

Peguei as 180 questões do caderno Azul e coloquei todas na mesma régua: a dificuldade TRI que o próprio INEP calibrou, item a item. 175 valeram nota (5 foram anuladas). O resultado é o raio-X da prova.

A campeã de crueldade: Matemática Q160, dificuldade TRI 923,7. Só 15% acertaram.
A mais generosa: Linguagens Q26, dificuldade TRI 440,4. 87% acertaram.

Olha as faixas de cada área no card. Elas contam a história:

Linguagens: de 440,4 a 694,9 — média 571,8. É a área mais "comportada": nem a pior questão de LC chega perto do que Matemática faz.
Humanas: de 501,7 a 772,1 — média 607,0.
Natureza: de 477,9 a 788,1 — média 618,6.
Matemática: de 481,1 a 923,7 — média 674,3. A área mais difícil da prova, e não é perto.

Repare: a questão mais difícil de Linguagens (694,9) seria uma questão MEDIANA em Matemática. As áreas não jogam o mesmo jogo — e é por isso que a mesma quantidade de acertos vale nota diferente em cada uma.

Dificuldade TRI aqui é b×100+500, a mesma escala da sua nota. Uma questão de dificuldade 700 é aquela que um aluno de nota 700 tem chance média de acertar.

Fonte: Microdados ENEM 2025 / INEP — TRI dos itens, caderno Azul.

Transformamos dados em aprovações. xtri.online

#enem #enem2025 #enem2026 #tri #matematica #linguagens #dificuldade #vestibular #estudos #microdados

## 1b) CAPA — texto alternativo

Gráfico com quatro barras horizontais mostrando a faixa de dificuldade TRI de cada área do ENEM 2025, da mínima à máxima: Linguagens de 440,4 a 694,9, Humanas de 501,7 a 772,1, Natureza de 477,9 a 788,1 e Matemática de 481,1 a 923,7. Dois destaques: Matemática Q160, a mais difícil, com dificuldade TRI 923,7 e 15% de acerto; Linguagens Q26, a mais fácil, com 440,4 e 87% de acerto.

---

## 2) SCATTER — legenda (feed)

A questão mais errada do ENEM 2025 não é a mais difícil. Parece contradição. Não é.

Cada ponto desse gráfico é uma das 175 questões que valeram nota, medida pela TRI do INEP. Quanto mais difícil, menor o acerto: a correlação é -0,83. Forte, como tinha que ser.

Mas olha o que os pontos escondem:

Matemática Q160 é a mais difícil da prova inteira (dificuldade TRI 923,7). Acerto: 15%.
Matemática Q140 é bem menos difícil (792,5). Acerto: 9,1%.

Ou seja: MENOS gente acertou a questão MAIS fácil das duas. Como?

A resposta está num parâmetro que quase ninguém conhece: a discriminação (o "a" da TRI). Ela mede o quanto a questão separa quem sabe de quem não sabe.

Q140 tem discriminação 3,47 — altíssima. É uma questão cirúrgica: ou você domina, ou você erra. Não tem meio-termo, não tem chute salvador.
Q160 tem discriminação 0,93 — baixa. É uma questão confusa, que erra gente boa e acerta gente que chutou. Tanto que o parâmetro de acerto ao acaso dela é 12%: quase todo o "acerto" dela é chute.

Por isso os 15% da Q160 são enganosos. Ela é dificílima, mas mal calibrada — e a TRI sabe disso. É por isso que acertar uma questão dessas quase não levanta sua nota, enquanto acertar a Q140 levanta muito.

A TRI não conta acerto. Ela lê PADRÃO de acerto. Guarda isso.

Fonte: Microdados ENEM 2025 / INEP — TRI dos itens, caderno Azul.

Transformamos dados em aprovações. xtri.online

#enem #enem2025 #enem2026 #tri #matematica #discriminacao #notaenem #vestibular #estudos #microdados

## 2b) SCATTER — texto alternativo

Gráfico de dispersão com 175 pontos, um para cada questão do ENEM 2025, coloridos por área. O eixo horizontal mostra a dificuldade TRI, de 450 a 950; o vertical, o percentual de acerto, de 0% a 90%. Os pontos formam uma nuvem descendente: quanto maior a dificuldade, menor o acerto, com correlação de -0,83. Destaques: Linguagens Q26, a mais fácil, no alto à esquerda com 87% de acerto; Matemática Q160, a mais difícil, embaixo à direita com 15%.

---

## Notas de integridade

- Fonte única: `TRI_ITENS_AZUL_ENEM2025.xlsx` (caderno Azul). Nada estimado.
- **175 itens** plotados = 185 linhas − 5 de Espanhol (LC usa Inglês nas 1–5) − 5 anuladas
  (CN 123, 125, 132 · MT 172, 174). Anulados nunca entram.
- Verificados na geração: correlação TRI × %acerto = **−0,8278** (arredondada p/ −0,83) ·
  mais difícil = **MT Q160** (TRI 923,7 · 15%) · mais fácil = **LC Q26** (TRI 440,4 · 87%).
- Médias/faixas por área (verificadas): LC 571,8 (440,4–694,9) · CH 607,0 (501,7–772,1) ·
  CN 618,6 (477,9–788,1) · MT 674,3 (481,1–923,7).
- **Q140 × Q160** (gancho do card 2, verificado na planilha):
  - Q140: TRI 792,5 · acerto 9,1% · a = 3,466 · c = 0,0795
  - Q160: TRI 923,7 · acerto 15,0% · a = 0,925 · c = 0,1209
  - Q140 é a de MENOR %acerto de toda a prova, mas NÃO é a de maior dificuldade TRI.
- Dificuldade TRI = b×100+500 (regra do CLAUDE.md). N respondentes = 3.176.917 (dia 2).
- **Correções feitas em relação à arte antiga** (`tri_itens_graphics.py`):
  1. Assinatura aposentada "Dados reais ou nada." → "Transformamos dados em aprovações."
  2. Sem `xtri.online` → CTA presente.
  3. Caminhos de sandbox (`/sessions/brave-sharp-fermi/...`) → caminhos reais do disco.
  4. Reta de tendência não era clipada: previa acerto de −19,7% em TRI 980 e vazava por
     cima do rodapé. Agora para onde cruza 0% (TRI 856,5).
