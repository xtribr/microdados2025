# Card — As 2 questões que não convergiram no ENEM 2025

> 🚫 **NÃO PUBLICAR ESTA VERSÃO — claim central impreciso (10/jul, scripts 07-08 do projeto R).**
> Síntese final do achado: o item anulado por convergência teve efeito ZERO na nota ao
> longo de TODA a escala (314/322 grupos de "gêmeos de prova" com ganho exatamente 0),
> EXCETO para quem acertou todos os itens válidos — nesse grupo a resposta na anulada
> decidiu o teto da edição: MT Q172 A→980,3 vs 967,7 (+12,6); CN Q125 B→858,7 vs 852,4
> (+6,3). Ou seja: o "você perdeu tempo / não contou" do card é verdade para 99,99% dos
> candidatos, mas é falso exatamente para os gabaritadores — o público que mais repercute
> post de nota. Os "previamente exposto" não contaram para ninguém. Refazer com o ângulo
> completo (muito mais forte): "a questão anulada que decidiu quem fez 980 em Matemática".
> Ver NOTAS_investigacao_convergencia.md no projeto R.

## Legenda (feed)

Você perdeu tempo fazendo essas duas questões no ENEM 2025 — e não tem nada a ver com a sua prova.

Q125 (Ciências da Natureza) e Q172 (Matemática), aplicação regular, caderno Azul: o próprio INEP marca essas duas com o motivo oficial "Problema de convergência" no microdado. Na prática, o modelo estatístico da TRI nunca conseguiu calcular uma dificuldade estável pra esses itens — então nenhuma resposta, de ninguém, entrou na correção.

Isso é diferente de questão anulada por erro de conteúdo (tipo gabarito errado ou item vazado antes da prova). Aqui o problema é estatístico: aconteceu depois da prova, na hora de calibrar os parâmetros.

Conferi na base inteira de 2025 (todas as aplicações, todos os cadernos): são só essas 2 em todo o ano. Raro, mas real.

Fonte: Microdados ENEM 2025 / INEP — DADOS/ITENS_PROVA_2025.csv, coluna TX_MOTIVO_ABAN. Caderno Azul, 1ª aplicação (regular).

#enem #enem2025 #enem2026 #tri #vestibular #dicasenem #questoesenem #matematica #cienciasdanatureza

## Notas
- Q125 = CO_POSICAO 125, CO_ITEM 96748, Ciências da Natureza. Q172 = CO_POSICAO 172, CO_ITEM 97593, Matemática.
- Ambas com IN_ITEM_ABAN=1 e TX_MOTIVO_ABAN="Problema de convergência" — sem NU_PARAM_A/B/C (nunca calibraram).
- Verificado: são os ÚNICOS 2 CO_ITEM com esse motivo em toda a base 2025 (132 CO_PROVA distintos, todas as aplicações incl. reaplicação e COP30/BAM).
- Gabarito oficial publicado existe pra ambas (Q125=B, Q172=A) — cross-checado contra ENEM_2025_P1_GAB_07_DIA_2_AZUL.pdf — mas isso não significa que contou pra nota; o item foi excluído da TRI depois.
- Prints recortados do caderno oficial ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf (não o P1-BAM, que é o caderno do COP30/Belém — confirmado via rodapé "Belém - Ananindeua - Marituba" no PDF errado antes de eu achar o certo).
- Diferente de outros 3 anulados do mesmo caderno (CN Q123, CN Q132, MT Q174) — esses foram por "Previamente exposto", motivo de conteúdo, não de convergência.

## Explicação técnica — por que a convergência falha

Modelo ML3P do ENEM: `P(acerto|θ) = c + (1-c) × 1/(1 + e^(-a(θ-b)))`. Os parâmetros (a,b,c) são estimados por Expectation-Maximization (EM), que ajusta a curva iterativamente até estabilizar (convergir). Premissa estrutural: a curva é monotonicamente crescente em θ (aluno melhor sempre tem chance igual ou maior de acertar) e exige a > 0.

Calculado direto no RESULTADOS_2025.csv (TX_RESPOSTAS_CN/MT vs NU_NOTA_CN/MT, presentes no dia, string de 45 posições por área — CN Q125 = índice 34, MT Q172 = índice 36):

| Item | Gabarito | % acerto real | N respostas | Correlação item × nota da área |
|---|---|---|---|---|
| CN Q125 | B | 30,4% | ~2,26M presentes | **+0,092** (quase zero) |
| MT Q172 | A | 18,1% | ~2,25M presentes | **−0,067** (negativa) |

Referência: item saudável costuma ter correlação ponto-bisserial 0,25–0,50+. MT Q172 tem correlação NEGATIVA — alunos com nota maior em Matemática tiveram, em média, chance um pouco MENOR de acertar essa questão específica do que alunos com nota menor. É o oposto da premissa do modelo.

Por que isso quebra o EM: o passo que estima a discriminação (a) busca a inclinação de curva logística que melhor explica os dados. Se a relação empírica acerto×habilidade é achatada ou invertida, não existe nenhum a>0 que ajuste bem — a curva "certa" para os dados seria decrescente, fora do espaço de parâmetros válido do modelo. O algoritmo fica empurrando a estimativa pra zero/negativo ou oscilando sem estabilizar, a verossimilhança não converge dentro da tolerância/iterações, e o INEP exclui o item em vez de publicar um parâmetro não confiável.

Diferença de MT Q160 (dificuldade 923,7, também só 15% de acerto, mas convergiu normal): lá quem sabia mais acertava mais (item difícil mas bem-comportado), só que poucos sabiam. Em MT Q172 o padrão empírico é o oposto — não é "difícil", é estatisticamente quebrado.

Causa mais provável na prática (não confirmável sem revisão pedagógica do conteúdo, mas é o padrão clássico da literatura de TRI): alternativa "correta" oficial questionável, enunciado ambíguo, ou distrator que engana justamente quem raciocina mais fundo — aluno mais preparado erra tanto quanto ou mais que o menos preparado.
