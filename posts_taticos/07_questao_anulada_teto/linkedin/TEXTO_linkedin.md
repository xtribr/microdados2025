# Post LinkedIn — A questão anulada que decidiu o teto de Matemática (ENEM 2025)

Imagem: `capa_linkedin_1200x1200.png` (1200×1200)

---

Uma questão anulada decidiu as maiores notas de Matemática do ENEM 2025. Eu fui aos microdados provar.

Quem acompanhou minha autópsia das questões anuladas vai lembrar dela: a questão de Matemática anulada por "problema de convergência", em que os melhores alunos convergiam numa letra diferente do gabarito. A regra que todo mundo conhece diz que questão anulada não vale nada. Fui verificar se a regra se cumpriu.

O método é simples e auditável — chamo de gêmeos de prova: candidatos do mesmo caderno com respostas idênticas em TODOS os itens válidos, divergindo apenas na questão anulada. Se a anulada não conta, gêmeos têm que ter a mesma nota. Sem modelo, sem regressão: comparação exata, linha a linha.

O que encontrei em 322 grupos de gêmeos, cobrindo a escala de 362 a 980 pontos:

1️⃣ Em 314 grupos, diferença de exatamente 0,0 ponto. Para praticamente toda a escala, a exclusão funcionou — a anulada não mudou a nota de ninguém.

2️⃣ Os únicos 8 grupos com diferença foram os padrões perfeitos. Entre os 601 candidatos que acertaram todos os 43 itens válidos de Matemática, quem marcou A na anulada ficou com 980,3; quem marcou qualquer outra letra, 967,7. Desempenho válido idêntico, 12,6 pontos de diferença — e foi isso que separou as maiores notas de Matemática do país. Em Ciências da Natureza, o item anulado da área repete o padrão: 858,7 contra 852,4.

3️⃣ O detalhe que fecha o caso: dos 601, apenas 86 marcaram a letra oficial (A). 512 marcaram D. O gabarito era a resposta minoritária entre os melhores candidatos do Brasil — o item estava mesmo quebrado.

Minha leitura técnica (interpretação — o processamento interno do INEP não é público): o item parece ter permanecido no modelo com parâmetros fraquíssimos. Onde a prova tem informação, o efeito fica abaixo do arredondamento de uma casa decimal; no extremo da escala, onde a informação desaba, o mesmo item vale de 6 a 13 pontos. O que está provado nos dados é o efeito, não o mecanismo.

Nada disso muda a vida de quem fez 500 ou 700. Mas num exame em que décimos decidem vaga de Medicina, o topo da escala de Matemática foi decidido por uma questão oficialmente anulada.

Método completo: microdados públicos do INEP (4,8 milhões de candidatos), análise em R (data.table + ggplot2), 644 comparações de gêmeos, zero exceções. Nas duas áreas sem item anulado (Linguagens e Humanas), todos os que gabaritaram empataram — o controle negativo perfeito.

No XTRI, é esse o nosso trabalho: transformamos dados em aprovações.
xtri.online

#ENEM #TRI #psicometria #dados #educação

---

## Notas (documentação interna)
- Chamada da capa: "Uma questão ANULADA decidiu as maiores notas de Matemática." + sub "Gêmeos de prova: desempenho válido idêntico, 12,6 pontos de diferença."
- Números dos scripts R 06-08 (projeto "microdados no R Studio"), mesmos do carrossel IG (ver ../TEXTO_legenda.md).
- Referência ao post anterior de LinkedIn (post_anulados/linkedin/): lá as curvas empíricas já mostravam os melhores convergindo em D no item de convergência — este post fecha aquele ciclo.
- CTA: xtri.online (padrão vigente desde 10/jul; o post antigo usava app.rankingenem.com).
