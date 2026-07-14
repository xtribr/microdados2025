# Post — O ENEM fica mais difícil a cada ano?

Imagens: `xtri_previsao_2026_feed.png` (1080×1350) · `xtri_previsao_2026_story.png` (1080×1920)

## Legenda (feed)

O ENEM fica mais difícil a cada ano? Levantei 16 edições (2010-2025) do parâmetro oficial de dificuldade da TRI para responder com dado, não com sensação de quem acabou de sair da prova.

Resultado, área por área — faixa histórica da Dificuldade TRI, 16 anos completos:

Linguagens: 560-619
Ciências Humanas: 541-649
Ciências da Natureza: 608-665
Matemática: 639-737

Rodei regressão linear com intervalo de confiança de 95% em cada área. O R² — quanto da variação a passagem do tempo explica sozinha — ficou abaixo de 0,05 nas 4 áreas. Ou seja: menos de 5% da variação tem a ver com o ano. O resto é oscilação normal de edição para edição, não tendência disfarçada.

O que não muda: Matemática teve a Dificuldade TRI mais alta das 4 áreas em TODOS os 16 anos da série, sem exceção. Essa é a constante real — não "o ENEM fica mais difícil", mas "Matemática segue estruturalmente mais exigente pela TRI".

Um detalhe de rigor: quando fui montar a série, os parâmetros de 2018 que eu tinha vieram fora de qualquer escala plausível nas 4 áreas — problema de cópia, não resultado real. Em vez de deixar o ano de fora ou estimar um número, fui atrás da fonte oficial: baixei a tabela de itens de 2018 direto do zip do INEP, conferi a integridade por CRC32 e recalculei do zero. Bateu certinho — Matemática 2018 (737) virou o novo teto da série.

Pra quem estuda pra 2027: não dá pra torcer por uma prova "mais fácil" nem se blindar pra uma "mais difícil" — dá pra se preparar pra faixa histórica inteira de cada área, porque qualquer ponto dela é plausível.

Fonte: banco de parâmetros de item por edição (2010-2024, Supabase) + microdados oficiais do INEP (2018 e 2025, recalculados direto da fonte). Dado real, sem estimativa.

#enem #enem2026 #enem2027 #tri #psicometria #previsao #microdados #vestibular #professor

## Texto alternativo (acessibilidade)

Gráfico com a faixa histórica de Dificuldade TRI por área do ENEM, 2010-2025 (16 anos completos): Linguagens 560-619, Ciências Humanas 541-649, Ciências da Natureza 608-665, Matemática 639-737 — a maior faixa das quatro. Card de resposta: "Oscila, não sobe", com R² abaixo de 0,05 nas quatro áreas, indicando ausência de tendência linear real.

## Notas de integridade
- Parâmetro b oficial do modelo 3PL da TRI (não é proxy/estimativa) — banco Regular, caderno Azul, itens não anulados.
- Série 2010-2024 filtrada por reaplicação e itens não convergentes (`|b| ≤ 6`); 2018 e 2025 recalculados direto dos arquivos oficiais do INEP, mesma metodologia.
- 2018 estava corrompido na cópia usada originalmente (Supabase) — recuperado direto do zip oficial do INEP (integridade conferida por CRC32) e recalculado do zero. Nenhum valor estimado ou preenchido.
- Fonte: Microdados ENEM / INEP.
