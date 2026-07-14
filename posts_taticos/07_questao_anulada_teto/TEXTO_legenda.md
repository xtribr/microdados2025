# Carrossel — A questão anulada que decidiu quem fez 980 (ENEM 2025)

## Legenda (feed)

A questão anulada que decidiu quem fez 980 em Matemática no ENEM 2025.

O INEP anulou a Q172 de Matemática e a Q125 de Ciências da Natureza por "problema de convergência", o modelo estatístico da TRI não conseguiu calibrar esses itens. 

Questão anulada não deveria valer nada, certo?

Fomos verificar nos microdados com um teste que não deixa margem: gêmeos de prova. 

Candidatos do mesmo caderno, com respostas idênticas em TODOS os itens válidos, divergindo só na anulada. 

Se a anulada não conta, gêmeo tem que ter nota igual.

E na maior parte da escala é exatamente isso: em 314 de 322 grupos de gêmeos, da nota 362 à 980, a diferença foi de 0,0 ponto. Zero. 

A anulada não mudou a nota de praticamente ninguém.

O plot twist está no topo. 

Entre os 601 candidatos que acertaram todos os 43 itens válidos de Matemática, quem marcou A na anulada levou 980,3. 

Quem marcou qualquer outra letra, 967,7. 

Mesmo desempenho em tudo que valia, 12,6 pontos de diferença, e foi isso que separou as maiores notas do país. 

Em Ciências da Natureza, mesma história: 858,7 contra 852,4.

E o detalhe que fecha o caso: dos 601 melhores, só 86 marcaram a letra oficial (A). 

512 marcaram D. O gabarito era minoritário entre os melhores do Brasil, o item estava mesmo quebrado.

Nossa leitura técnica: o item parece ter entrado no cálculo com peso minúsculo, invisível onde a prova mede bem e decisivo onde a régua acaba. 


Método usado por mim e XTRI: microdados oficiais do INEP (4,8 milhões de candidatos), análise em R com data.table e ggplot2, 644 comparações de gêmeos, zero exceções. Dado real, auditável, reproduzível.

Fonte: Microdados ENEM 2025 / INEP — gov.br/inep

#enem #enem2025 #enem2026 #tri #matematica #vestibular #notadoenem #dicasenem

## Notas (documentação interna)
- Números de scripts R rodados pelo usuário no projeto "microdados no R Studio": 06 (teto), 07 (gabaritadores), 08 (gêmeos).
- MT: 601 gabaritadores de 43/43 válidos; resp. na anulada Q172-azul (item 97593): A=86→980,3 · D=512, C=2, E=1→967,7. CN: 84 de 42/42; Q125-azul (item 96748): B=67→858,7 · outras 17→852,4.
- Gêmeos (script 08): CN 112 grupos/432 candidatos, MT 210/1.868; 314 grupos ganho 0; 8 com ganho = padrões válidos perfeitos (4 por cor de caderno em cada área); determinismo 644 subgrupos sem exceção.
- LC/CH (sem anulados): gabaritadores com nota única (794,5 / 856,4) — controle negativo.
- Itens "previamente exposto" (CN Q123/Q132, MT Q174): efeito zero comprovado; gabarito mascarado como 'X' na string do aluno.
- Slides (v2, 10/jul): c1 capa "SUA VAGA DE MEDICINA..." (feed+story), c2 gabaritadores, c3 gêmeos na escala, c4 PROVA: console R de Matemática (saída real do script 08 — 0 de 420, ganho >0 só em 4 grupos, máx 12.6), c5 síntese conta/não-conta, c6 PROVA: console R de Ciências da Natureza (0 de 224, máx 6.3) + CTA. Os slides antigos de "gabarito minoritário" e "método" foram substituídos a pedido pelos consoles com a base empírica; o dado do gabarito minoritário (86×512) segue na legenda e no post WP.
- Registro técnico completo: NOTAS_investigacao_convergencia.md no projeto R.
