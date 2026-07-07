# Estudo: Mapa de Distratores — a alternativa ERRADA que mais engana (ENEM 2025)

## Pergunta
Em cada questão do ENEM 2025, entre quem ERROU, existe uma alternativa errada que concentra a maioria
dos erros — a "pegadinha campeã"? Ela revela uma concepção equivocada específica, mais acionável pro
professor do que só "% de acerto".

## Método (100% dado real INEP, nada estimado)
1. **Caderno Azul regular**, mesmos `CO_PROVA` já usados em todo o acervo XTRI (LC 1459 · CH 1447 ·
   CN 1483 · MT 1471) — confirmado via `ITENS_PROVA_2025.csv` que cada área tem, na verdade, **3 edições
   diferentes sob a mesma cor** (ex.: CH também tem 1520 e 1539, com itens totalmente diferentes por
   posição); os códigos acima são a edição amplamente majoritária (>99,9% dos presentes), a mesma que os
   estudos anteriores (`estudo_perfil_tri`, `TRI_ITENS_AZUL_ENEM2025.xlsx`) já usavam.
2. **`CO_POSICAO` é absoluto no dia** (LC 1–45, CH 46–90, CN 91–135, MT 136–180), mas
   `TX_RESPOSTAS_{ÁREA}` é local à área (índice 0 = 1ª questão daquela área) — precisa somar o offset
   (CH +45, CN +90, MT +135) para casar item com resposta. Bug pego e corrigido durante o desenvolvimento
   (1ª rodada zerou CH/CN/MT por não converter o offset).
3. **1 única passada streaming** sobre as 4,81 milhões de linhas de `RESULTADOS_2025.csv` (sem amostra),
   contando a letra marcada em cada uma das 45 posições de cada área, só de presentes na edição Azul
   majoritária. Excluídos: os 5 itens anulados (`IN_ITEM_ABAN==1`), respostas fora de A–E (branco/dupla
   marcação), e LC posições 1–5 tratadas à parte por `TP_LINGUA` (a área tem 2 itens diferentes ali,
   um por idioma).
4. Por item: `% acerto` (gabarito/válidos), `distrator campeão` = alternativa errada mais marcada entre
   quem errou, `% entre os errados`, `% da base` (de todos os presentes, não só de quem errou), e
   **lift vs. uniforme** = `% entre os errados ÷ 25%` (25% é o esperado se as 4 alternativas erradas
   fossem escolhidas ao acaso, já que cada item tem exatamente 5 alternativas).
5. Habilidade de cada item identificada via `CO_HABILIDADE` + descrição oficial já catalogada em
   `analises_primi_2025_cop30/outputs/habilidades_desc.json` (BNCC/matriz do ENEM, real, não inventada).

**Verificação:** 4 itens conferidos manualmente contra `TRI_ITENS_AZUL_ENEM2025.xlsx` (fonte independente
já auditada em estudo anterior) — `co_item`, gabarito, habilidade e parâmetros a/b/c batem exatamente;
`% acerto` bate com diferença de ≤0,8 p.p. (esperado por pequena diferença de critério de invalidação
de resposta entre os dois scripts).

## Achados

**180 itens** analisados (LC 50 — incluindo os 2 blocos de língua — · CH 45 · CN 42 · MT 43, após excluir
os 5 anulados). Lift médio: **1,59×** — ou seja, em média, a alternativa campeã é escolhida quase **60%
mais** do que se o erro fosse puramente aleatório entre as 4 opções erradas. Isso mostra que o erro no
ENEM raramente é ruído: na maioria das questões, existe uma pegadinha específica pra qual o aluno é
empurrado.

- **49,4% dos itens (89 de 180)** têm um distrator "claro" (lift ≥ 1,5×) — pegadinha bem definida.
- Só **7,8% (14 itens)** têm distribuição quase uniforme entre as erradas (lift < 1,2×) — aí sim o erro
  parece mais aleatório/chute puro.
- **Sem viés sistemático de posição**: a letra campeã se distribui de forma relativamente equilibrada
  (A: 45 · B: 36 · C: 43 · D: 30 · E: 26) — não existe "a alternativa C costuma ser a errada mais
  escolhida" como lenda popular sugere.

### O achado mais forte: em 45 itens (25% da prova), mais gente ERROU pra UMA alternativa específica
### do que ACERTOU

Ou seja: a alternativa errada campeã não é só "a mais escolhida entre quem errou" — em 1 de cada 4
questões do ENEM 2025, ela é **a resposta mais marcada da questão inteira**, batendo até o gabarito.

**Exemplo mais extremo:** CN posição 21 (Q111, hab. CNH9 — ciclos biogeoquímicos e fluxo de energia).
Gabarito B: só **16,5%** acertaram. Alternativa A: **45,9%** de todos os presentes marcaram — quase 3×
mais gente errou para essa alternativa específica do que acertou.

### Campeão por área (maior lift = pegadinha mais "concentrada")

| Área | Posição | Habilidade | Gabarito | % acerto | Distrator campeão | % dos que erraram | Lift |
|---|---|---|---|---|---|---|---|
| Linguagens | 19 | LCH10 — hábitos corporais/necessidades cinestésicas | E | 78,0% | B | 69,0% | 2,76× |
| Ciências da Natureza | 17 | CNH13 — mecanismos de transmissão da vida | E | 43,3% | C | 67,7% | 2,71× |
| Ciências Humanas | 33 | CHH11 — registros de práticas sociais no tempo/espaço | B | 34,7% | A | 57,8% | 2,31× |
| Matemática | 13 | MTH11 — noção de escalas | C | 35,8% | A | 57,3% | 2,29× |

No item de Ciências Humanas acima, o distrator A (37,8% da base) já é **mais popular que o próprio
gabarito** (34,7%) — outro caso da categoria "a pegadinha venceu a questão".

## Leitura para o professor
"% de acerto" diz que uma questão foi difícil. O mapa de distratores diz **para onde** o erro foi —
e isso é o que se ataca em sala: não é "revisar o conteúdo todo de novo", é atacar a concepção
equivocada específica que está por trás da alternativa campeã.

## Arquivos
- `compute_distratores.py` — script (streaming único sobre 4,81 mi linhas, ~55s).
- `distratores_itens.csv` — os 180 itens com todas as métricas.
- `distratores_resumo.json` — top 15 geral + top 3 por área + lift médio por área.
- `MAPA_DISTRATORES_ENEM2025.xlsx` — tabela formatada para professor (ver script de geração).

*Fonte: Microdados ENEM 2025 / INEP. "Transformamos dados em aprovações."*
