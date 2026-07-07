# ROADMAP 2 — Novos posts e estudos (ENEM 2025 · XTRI)

> Continuação do `PLANO_conteudo_xtri.md`. Foco definido com o usuário: **equilíbrio aluno × professor**, ênfase em **TRI** e **TRI por área**, dicas acionáveis para alunos e estudos técnicos. Todas as ideias têm gancho em **dado real INEP** que já existe nos seus CSVs — **coluna citada explicitamente**. Nada aqui depende de inventar dado.

---

## 1. Mapa do que JÁ está pronto (para não repetir)

**Posts publicados/prontos:** fadiga (branco por posição), chutadas (parâmetro c, 10/área), abstenção (dia 1×2), idade, língua (espanhol×inglês), prioridade, treineiros, custo de errar (LC).

**Estudos prontos:** psicometria (CCI 3 parâmetros, informação do teste, modelo×observado r=0,955, paradoxo acerto×nota MT) · TRI marginal (zona cara 9–13 acertos, "questão do seu nível") · habilidades difíceis H1–H30 · sequência de dificuldade por caderno · equating de cadernos · ranking escolas RN 54×54 + artigo · planilha TRI dos 185 itens (Azul) · COP30×regular · palestra 20 gráficos · Artigo Seis Itens.

**Conclusão:** o "panorama TRI" e o "diagnóstico de dificuldade" já estão fortes. Os **veios ainda intocados** são: **redação por dentro** (corretores, competências), **distratores**, **person-fit**, **regionalização por item** e uma **série fechada de TRI por área**. É onde este roadmap concentra o que é novo.

---

## 2. Trava de integridade (vale para tudo abaixo)

- **Socioeconômico NÃO cruza com nota** (sem chave comum entre `PARTICIPANTES` e `RESULTADOS`). Perfil só narra perfil; nota só narra nota. Nunca "pobre tira X, rico tira Y".
- **Redação é múltiplo de 20**; `TP_STATUS_REDACAO` não tem código 5; não existe status "fere direitos humanos" isolado.
- Análises por item usam **caderno Azul** (LC 1459 · CH 1447 · CN 1483 · MT 1471). Parâmetros TRI são intrínsecos ao item.
- **5 itens anulados** (CN Q123, Q125, Q132; MT Q172, Q174) — marcar "Anulada", nunca estimar.
- Parâmetros reais extrapolam limites de skill (a até 7,35; c até 0,40) — são reais, manter.
- Marca: **sem fundo preto**, "sexo feminino/masculino", gancho na voz do aluno, fonte **INEP** no rodapé, proibido "loteria"/buzzword-muleta, **nunca inventar/estimar nulo**.

---

## TRILHA A — Dores & dicas do aluno (engajamento)

### A6. "Sua redação caiu num corretor mais duro?" — A CALCULAR · esforço médio · **NOVIDADE ALTA / INÉDITO**
- **Gancho (voz do aluno):** "tive azar de corretor?" — medo universal. Os dados mostram quão perto (ou longe) dois avaliadores ficam, e que existe revisão quando discordam.
- **Dado real:** `RESULTADOS_2025.csv` → `NU_NOTA_AV1` vs `NU_NOTA_AV2` (e `NU_NOTA_COMP1..5_AV1` vs `..._AV2`). Calcular |diferença| por competência, % de redações em que os dois concordam dentro de 1 nível, e fração que acionou `NU_NOTA_AV3`/`AV4` (3ª/4ª correção por divergência).
- **Por que engaja:** transforma ansiedade em confiança no processo. Número-herói: "em X% das redações os dois corretores concordaram dentro de 80 pontos".
- **Formato:** card número-herói + barra de |divergência| por competência. Possível story "como funciona a 3ª correção".

### A7. "A competência que mais derruba a redação" — A CALCULAR · esforço baixo-médio · *pendente A1 do plano*
- **Gancho:** a competência de menor média nacional puxa a nota de quase todo mundo — é onde focar.
- **Dado real:** `RESULTADOS` → média e distribuição de `NU_NOTA_COMP1..5` (0–200 cada); % de alunos com nota baixa (ex.: ≤120) em cada competência.
- **Formato:** carrossel (1 card por competência, com a dica de blindagem) ou card único do gargalo.

### A8. "Quem tira 1000 (e quem zera) — e por quê" — A CALCULAR · esforço baixo · *pendente A2 do plano*
- **Gancho:** o número de mil é raríssimo; e a forma mais comum de zerar **não é errar conteúdo**, é não escrever ou copiar.
- **Dado real:** `NU_NOTA_REDACAO == 1000` (contagem) e `== 0` cruzado com `TP_STATUS_REDACAO` (em branco, cópia do motivador, fuga ao tema, texto insuficiente, anulada…). A palestra já tem o número macro; aqui vira post dedicado com a **barra dos motivos**.
- **Formato:** card número-herói + barra de motivos do zero.

### A9. "Quantos acertos para a SUA nota dos sonhos? (por área)" — A CALCULAR · esforço médio · **NOVIDADE ALTA · dica TRI**
- **Gancho:** responde à pergunta nº1 do vestibulando — e prova, de novo, que "acerto não é nota" (mostra a faixa).
- **Dado real:** `RESULTADOS` → contar acertos de `TX_RESPOSTAS_{LC,CH,CN,MT}` vs `TX_GABARITO_*`, cruzar com `NU_NOTA_*`. Tabela acertos→nota **mediana + faixa (p10–p90)** por área, na amostra de presentes.
- **Por que engaja:** é a busca mais comum; vira conteúdo salvável e reutilizável todo ano.
- **Formato:** carrossel 4 áreas; **opcional: mini-calculadora HTML** "digite acertos → veja a faixa de nota" (SPA leve, sua praia).

### A10. "A ordem certa de fazer a prova" — esforço baixo (assets existem) · novidade média · **dica de estratégia**
- **Gancho:** nem linear, nem "de trás pra frente" — garanta as questões do **seu nível** antes de cansar.
- **Dado real (síntese de prontos):** sequência de dificuldade por caderno (`dificuldade_sequencia_por_caderno/`) + valor marginal do acerto (`estudo_tri_marginal`) + curva de branco por posição (`posts_fadiga`).
- **Formato:** carrossel didático "3 regras para a ordem da prova".

### A11. "Espanhol × Inglês por dentro: qual item mais separa" — A CALCULAR · esforço médio · novidade média
- **Gancho:** aprofunda o post de língua já feito — não só "quem escolhe o quê", mas **qual das 5 questões de língua mais pesa** em cada idioma.
- **Dado real:** `RESULTADOS` `TX_RESPOSTAS_LC` posições 1–5 × `TP_LINGUA` × `TX_GABARITO_LC`; parâmetros dos itens de inglês **e** espanhol em `ITENS_PROVA_2025.csv` (a planilha Azul já lista ambos).
- **Formato:** card comparativo + dica de escolha de língua.

---

## TRILHA B — Estudos técnicos / professor (profundidade)

### B6. "Mapa de distratores: a alternativa errada que mais engana" — A CALCULAR · esforço médio-alto · **TEACHER GOLD · INÉDITO** · *pendente B2*
- **Gancho:** por questão, qual alternativa **errada** atrai mais — revela a **concepção equivocada** que o professor precisa atacar.
- **Dado real:** distribuição de `TX_RESPOSTAS_*` por posição vs `TX_GABARITO_*`; achar o distrator dominante por item e cruzar com `CO_HABILIDADE` (em `ITENS_PROVA`). Tema da questão lido da prova oficial (como no carrossel de chutáveis).
- **Formato:** carrossel "a pegadinha mais eficaz de cada área" + **tabela para professor** (item, habilidade, distrator-campeão, % que caiu).

### B7. "Person-fit: o aluno que acerta a difícil e erra a fácil" — A CALCULAR · esforço alto · **INÉDITO · TRI avançada**
- **Gancho:** leva o "paradoxo acerto×nota" para o **nível do indivíduo**: padrões de resposta incoerentes existem e a TRI os enxerga. Quantos alunos têm padrão "estranho" e o que isso diz sobre chute desordenado.
- **Dado real:** `RESULTADOS` `TX_RESPOSTAS_*` + `b` por posição (de `ITENS_PROVA`). Estatística de person-fit (ex.: índice U3 ou lz) por área; correlacionar incidência com a nota.
- **Formato:** estudo técnico (1–2 figuras) + 1 card didático "por que chutar fora de ordem atrapalha".

### B8. "O mesmo item pega diferente por região?" — A CALCULAR · esforço alto · **INÉDITO** (só `RESULTADOS`, sem ferir a trava)
- **Gancho:** um item "derruba" mais no Norte que no Sudeste? Diferença de **acerto por item entre regiões**, sem cruzar perfil socioeconômico.
- **Dado real:** `RESULTADOS` `TX_RESPOSTAS_*` × `SG_UF_PROVA`/`SG_UF_ESC`; % de acerto por item por UF/região. Versão rigorosa: DIF Mantel-Haenszel usando o **escore total como proxy de θ** (viável só com `RESULTADOS`).
- **Cuidado:** se não controlar proficiência, nomear como "acerto por item por região", não "DIF" formal.
- **Formato:** estudo + heatmap item × região; lista dos maiores gaps.

### B9. "Quão confiável é cada prova? (KR-20 por área)" — A CALCULAR · esforço médio-alto · **INÉDITO · técnico**
- **Gancho:** medida clássica de consistência interna de cada prova — complementa a discriminação Baker que você já mostrou.
- **Dado real:** `RESULTADOS` → matriz de acerto por item (de `TX_RESPOSTAS_*` × gabarito) por área; calcular **KR-20 / alfa** por prova.
- **Formato:** estudo técnico (1 figura) + nota de leitura para professor.

### B10. "Itens que se comportaram fora do esperado" — A CALCULAR · esforço médio · novidade média-alta (amplia o *Artigo Seis Itens*)
- **Gancho:** onde o modelo TRI e o acerto observado mais divergem — itens para auditar/discutir em sala.
- **Dado real:** parâmetros de `ITENS_PROVA` + acerto observado (`dificuldade_consolidado.json` ou recomputar de `TX_RESPOSTAS`); resíduo modelo−observado por item; rankear os maiores.
- **Formato:** estudo + carrossel "os itens mais 'estranhos' de 2025".

---

## TRILHA C — Série "TRI por área" (LC · CH · CN · MT) — *pedido explícito*

**Ideia:** quatro dossiês-perfil, **um por área**, cada um reunindo num só lugar (a maioria já existe; faltam 2 cálculos):
dificuldade média e distribuição de `b` · discriminação `a` (Baker) · chute `c` · função de informação (onde a prova mede) · habilidades mais difíceis · **distrator-campeão** (de B6) · **tabela acertos→nota** (de A9) · "a questão que mais vale no nível típico".

- **C1 — TRI de Linguagens** · **C2 — TRI de Humanas** · **C3 — TRI de Natureza** · **C4 — TRI de Matemática**.
- **Gancho:** "Tudo o que a TRI diz sobre a prova de [área], num lugar."
- **Esforço:** médio (reembala assets prontos + puxa A9 e B6). **Alto valor** para aluno (estratégia) e professor (diagnóstico).
- **Formato:** 1 carrossel/estudo por área → vira **série fechada** e, no fim, um **dossiê/e-book "ENEM 2025 em TRI, área por área"**.

---

## 3. Priorização sugerida (primeira leva)

| Ordem | Item | Trilha | Esforço | Novidade | Por que primeiro |
|---|---|---|---|---|---|
| 1 | **A8** Mil & zero (motivos) | Aluno | Baixo | Média | Quase pronto (número já existe), forte engajamento |
| 2 | **A9** Acertos → nota por área | Aluno | Médio | Alta | Pergunta nº1; reutilizável; reforça "acerto≠nota" |
| 3 | **B6** Mapa de distratores | Professor | Médio-alto | Alta | Conteúdo-professor mais original e acionável |
| 4 | **A6** Corretores da redação | Aluno | Médio | Alta | Veio inédito, alto apelo emocional |
| 5 | **C1–C4** Série TRI por área | Ambos | Médio | Média | Empacota o acervo + A9/B6 num produto fechado |

**Quick wins (baixo esforço, asset pronto):** A8, A10, A7.
**Alto impacto/ineditismo:** A6, A9, B6, B7.

---

## 4. Verificação (ao executar cada tema)

1. Rodar o cálculo em Python na coluna citada; conferir contagens contra totais conhecidos (presentes CN/MT ~3,18 mi; CH/LC ~3,37 mi; 4,81 mi linhas).
2. Spot-check de 3–5 valores contra a fonte (PDF da prova, dicionário, planilha TRI Azul).
3. Arte no padrão: sem fundo preto, marca X-TRI, fonte INEP no rodapé, "sexo feminino/masculino".
4. Nunca preencher nulo/estimar; anuladas marcadas, nunca chutadas. Redação sempre múltiplo de 20.

## 5. Insumos-chave
- Dados: `DADOS/RESULTADOS_2025.csv` (notas, `TX_RESPOSTAS_*`, `TX_GABARITO_*`, redação `COMP*`/`AV*`, `SG_UF_*`), `DADOS/PARTICIPANTES_2025.csv` (perfil — só narra perfil), `DADOS/ITENS_PROVA_2025.csv` (`NU_PARAM_A/B/C`, `CO_HABILIDADE`, `CO_POSICAO`).
- Prontos a reaproveitar: `analises_primi_2025_cop30/outputs/` (habilidades, sequência), `analise_psicometria_2025/`, `estudo_tri_marginal/`, `TRI_ITENS_AZUL_ENEM2025.xlsx`, `palestra/`.
