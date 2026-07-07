# ROADMAP 3 — Estudos psicométricos: **TRI × perfil do aluno** (ENEM 2025 · XTRI)

> Continuação de `PLANO_conteudo_xtri.md` e `ROADMAP2_novos_posts_e_estudos_XTRI.md`. Foco deste documento: **unir TRI + perfil do aluno, com gráficos**. Toda ideia tem gancho em **dado real INEP** com a **coluna citada**. Nada depende de inventar dado ([[no-fake-data-enem-microdados]]).

---

## 0. A descoberta que organiza tudo: qual "perfil" cruza com a nota?

A viabilidade de "perfil × TRI" depende de **onde** a coluna de perfil vive. Conferido direto no header dos CSVs:

| Perfil **JOINÁVEL** com nota/TRI (vive em `RESULTADOS`, mesma linha) | Perfil **NÃO joinável** (vive em `PARTICIPANTES`, chave diferente) |
|---|---|
| `TP_DEPENDENCIA_ADM_ESC` — rede (1 federal · 2 estadual · 3 municipal · 4 privada) | `TP_FAIXA_ETARIA`, `TP_SEXO`, `TP_COR_RACA`, `TP_ESTADO_CIVIL` |
| `TP_LOCALIZACAO_ESC` — urbana/rural | `TP_ST_CONCLUSAO`, `IN_TREINEIRO`, `TP_ENSINO` |
| `SG_UF_ESC` / `SG_UF_PROVA` — UF/região | `Q001`–`Q023` (renda, escolaridade dos pais, bens…) |
| `TP_LINGUA` — inglês/espanhol | — |

**Regra de ouro (trava de integridade):** perfil socioeconômico/demográfico de `PARTICIPANTES` **NUNCA** cruza com nota (chaves `NU_INSCRICAO` ≠ `NU_SEQUENCIAL`; arquivos não alinhados). *Perfil narra perfil; nota narra nota.*
**Permitido** cruzar com nota só o que está em `RESULTADOS`: **rede, urbano/rural, UF, língua** — são recortes que o próprio INEP publica.

> **Veio novo, quente e pouco explorado:** "**perfil joinável (rede/região/língua) × TRI**". É o coração deste roadmap.

### Trava operacional (vale para todo estudo deste roadmap)
- **Campos de escola só existem em 36,1% das linhas** (1.739.028) — o subconjunto ligado a escola (concluintes/treineiros que declararam escola; egressos ficam em branco). Composição confirmada: **estadual 79,5% · privada 15,7% · federal 4,3% · municipal 0,5%**. Sempre narrar esse denominador.
- **Nunca ler como causa socioeconômica.** É "nota média por rede" — recorte factual, não "rico × pobre". Não cruzar com `PARTICIPANTES`.
- Caderno-base por item = **Azul regular** (filtrar `TX_COR=='AZUL'`; valores reais: AZUL/AMARELA/BRANCA/CINZA/LARANJA/ROXA/VERDE/LEITOR TELA). Parâmetros `a,b,c` são **do item** (não mudam por cor; a cor só fixa seleção/ordem dos 45).
- 5 itens anulados (CN 123/125/132, MT 172/174) → filtrar `IN_ITEM_ABAN==1`, **nunca estimar**.
- LC: `TX_GABARITO_LC`=50 chars (5 ing + 5 esp + 40 comuns), `TX_RESPOSTAS_LC`=45 → alinhar por `TP_LINGUA` (lógica já no `dif_chunk.py`).
- Redação múltiplo de 20; `TP_STATUS_REDACAO` sem código 5; anuladas/em branco marcadas, nunca chutadas.
- Marca: sem fundo preto, "sexo feminino/masculino", fonte INEP no rodapé, gancho na voz do aluno, sem buzzword-muleta, as 4 áreas quando fizer sentido.

---

## 1. O que JÁ está pronto (acervo psicométrico — não repetir)

Catálogo dos 15 estudos existentes (todos **prontos**):

| Estudo | Eixo TRI | Tem perfil? |
|---|---|---|
| **Psicometria base** (CCI 3PL, função de informação, modelo×observado r=0,955, paradoxo acerto×nota MT, custo de errar=discriminação) | CCI, TIF, validação | proficiência θ (sem perfil categórico) |
| **TRI marginal** (valor do acerto; zona cara 9–13; "a questão do seu nível") | função de informação por θ | nível de proficiência |
| **Polêmicas TRI** (IPT: a baixo + c alto + misfit; ranking dos 180) | a, c, resíduo | — |
| **Dificuldade-sequência por caderno** (P01–P45, hab + DIF) | b por posição | — |
| **Chutadas** (parâmetro c por tema, 10/área) | c | — |
| **PRIMI COP30** (habilidades H1–H30, dificuldade, COP30×regular) | b, %acerto por hab | grupo COP30 |
| **Posts**: fadiga (branco por posição), abstenção dia1×2, idade, língua ing×esp, prioridade, treineiros | descritivo | idade/língua/treineiro |
| **Corretores** (redação dupla pauta — filosofia) | concordância | — |
| **Palestra** (20 gráficos) · **Artigo ranking RN 54×54** · **planilha TRI 185 itens Azul** | consolidação | escola (ranking) |

**Conclusão:** o "panorama TRI do item" e o "diagnóstico de dificuldade" estão fortes. **O que falta — e é o pedido atual — é cruzar TRI com o perfil do aluno.** É exatamente onde quase nada foi feito.

---

## 2. Âncoras REAIS já calculadas (1 passada sobre `RESULTADOS`, 4,81 mi linhas)

Para provar que o veio é real, já rodei `estudo_perfil_tri/anchor_nota_por_perfil.py`. Resultados (média de presentes, dado INEP, **não estimado**):

**Nota média por rede de ensino** (subset escolar = 36,1%) — gráfico pronto em `estudo_perfil_tri/TEASER_nota_por_rede.png`:

| Área | Estadual | Municipal | Federal | Privada | Gap Priv−Est |
|---|---|---|---|---|---|
| Natureza (CN) | 473 | 500 | 536 | 552 | **+79** |
| Humanas (CH) | 485 | 518 | 549 | 567 | **+82** |
| Linguagens (LC) | 508 | 542 | 564 | 578 | **+70** |
| Matemática (MT) | 481 | 532 | 587 | 620 | **+140** |
| Redação | 527 | 595 | 676 | 730 | **+203** |

**Outras âncoras prontas:**
- **Urbana × rural** (n rural = 94.173): MT 516 vs 466 · Redação 577 vs 505.
- **UF (média 4 áreas objetivas):** SP 543 (topo) → PA 480 (base); amplitude 62 pts. Topo: SP/DF/SC/RS/MG; base: PA/AM/MA/AP/AC.
- **Língua LC:** inglês 550 (n=2,06 mi) vs espanhol 506 (n=1,39 mi) — **seleção** de quem escolhe, não dificuldade do bloco.

---

## 3. Cardápio de estudos NOVOS (priorizado por novidade × viabilidade × engajamento × integridade)

### 🟢 PRIMEIRA LEVA — "fazer já" (alto valor, viável, integridade limpa)

#### E1 ⭐ FLAGSHIP — "A prova mede melhor quem?" Função de Informação × rede de ensino
- **Gancho:** "Será que a prova consegue medir direito quem ainda está começando — ou foi calibrada pra quem já está voando?"
- **TRI:** Função de Informação do Teste `I(θ)` e erro-padrão `SE(θ)=1/√I(θ)` por área, a partir de `NU_PARAM_A/B/C` (caderno Azul, `IN_ITEM_ABAN==1` fora). Fórmula correta 3PL: `I(θ)=Σ aᵢ²·(1−P)/P·((P−c)/(1−c))²`.
- **Perfil:** densidade de `NU_NOTA_{área}` por `TP_DEPENDENCIA_ADM_ESC` sobreposta à curva de informação.
- **Achado-tese:** o **pico de informação cai onde sentam privada/federal**; a maioria estadual cai na cauda, onde a prova mede com **menos precisão** (SE maior). Hero-stat: "o ENEM mede o aluno mediano de escola privada com erro-padrão X pontos menor que o da estadual".
- **Gráfico:** painel 2×2 (4 áreas), eixo X = nota TRI; linha = `I(θ)`; densidade da nota por rede ao fundo; variante com `SE(θ)` e medianas por rede.
- **Público:** ambos · **Esforço:** médio · **Score 18 · INÉDITO** (o overlay por rede é novo; a TIF já existe).

#### E2 ⭐ Redação por dentro do perfil joinável — o gargalo de competência muda por rede?
- **Gancho:** "A competência que mais me derruba é a mesma pra todo mundo?" Não necessariamente.
- **Dado:** médias de `NU_NOTA_COMP1..5` (0–200) por `TP_DEPENDENCIA_ADM_ESC`, `TP_LOCALIZACAO_ESC` e `SG_UF_ESC`; só redações válidas (`TP_STATUS_REDACAO`). Identificar **onde mora o fosso público-privado** (provável C1 norma culta / C5 intervenção) e se o gargalo é o mesmo em todas as redes.
- **Gráfico:** barras agrupadas C1..C5 × rede; ranking do gap por competência; mini-mapa por UF.
- **Público:** ambos · **Esforço:** baixo-médio · **Score 18 · carro-chefe do pedido** (TRI/rubrica × perfil joinável).
- *Âncora já existe:* redação estadual 527 → privada 730.

#### E3 ⭐ Inglês × Espanhol por dentro — qual bloco mede melhor e qual item mais separa
- **Gancho:** "Escolhi espanhol achando mais fácil — mas será que inglês 'rende' mais ponto por acerto?"
- **Dado:** isolar os 5 itens de cada idioma (`TP_LINGUA`, `CO_POSICAO` 1–5); FIT de cada bloco (`NU_PARAM_A/B/C`); item de maior discriminação (`a`); % acerto observado por item alinhado por `TP_LINGUA`.
- **Gráfico:** 2 curvas de informação (inglês × espanhol) + barras do `a` dos 10 itens; densidade de `NU_NOTA_LC` por língua.
- **Público:** aluno · **Esforço:** médio · **Score 18** · aprofunda o post de língua (ângulo item-level/FIT é novo).

#### E4 A redação prevê suas notas objetivas? (validade convergente/discriminante)
- **Gancho:** "Sou bom de redação — então vou bem nas provas?" Nem tanto.
- **Dado:** correlação de `NU_NOTA_REDACAO` com cada nota TRI; `r²` (variância compartilhada). Amostra indica **r≈0,47–0,53 — só ~¼ compartilhado** — e a redação correlaciona **quase igual com MT e com LC**.
- **Gráfico:** 4 barras (r por área) + painel-herói "¼"; hexbin redação × MT.
- **Público:** ambos · **Esforço:** médio · **Score 17 · INÉDITO** (nota × nota, mesma linha — permitido).

#### E5 Urbano × rural na escala TRI + habilidades que mais penalizam o campo
- **Gancho:** "Estudei no interior, na zona rural — a prova é mais dura pra mim em alguma área?"
- **Dado:** gap de `NU_NOTA_{área}` por `TP_LOCALIZACAO_ESC` (rural n=94.173); depois recomputar % acerto por item e agregar por `CO_HABILIDADE` para o ranking de habilidades com maior gap campo×cidade.
- **Gráfico:** barras do gap por área + dumbbell top-10 habilidades.
- **Público:** ambos · **Esforço:** médio · **Score 16 · INÉDITO** (recorte menos inflamável que público/privado).

#### E6 A pegadinha campeã muda de escola? Distrator dominante por rede
- **Gancho:** "A 'errada que mais engana' na escola pública é a mesma da privada?"
- **Dado:** entre **quem errou**, distribuição A–E por item, separada por pública (`TP_DEPENDENCIA` 1/2/3) × privada (4); distrator-campeão por rede; contexto `NU_PARAM_B` + `CO_HABILIDADE`.
- **Gráfico:** barras pareadas 100% (pública × privada) + tabela professor.
- **Público:** professor · **Esforço:** médio · **Score 15** (B6 do roadmap + recorte rede).

#### E7 As 5 competências são mesmo 5 notas? (efeito-halo / dimensionalidade da rubrica)
- **Gancho:** "Por que minhas 5 notas vêm quase coladas?"
- **Dado:** matriz de correlação 5×5 de `NU_NOTA_COMP1..5` + alfa. Amostra: **C1–C4 r 0,82–0,89; C5 (Proposta de Intervenção) é a rebelde (0,67–0,75)**.
- **Gráfico:** heatmap 5×5 + alfa.
- **Público:** ambos · **Esforço:** baixo · **Score 15 · INÉDITO** (psicometria da rubrica é nova no acervo).

### 🟡 SEGUNDA LEVA — "fazer depois" (selecionados)

- **E8 DIF geográfico (Mantel-Haenszel)** — "o mesmo item, dois Brasis": acerto **condicionado ao escore** (proxy θ), Norte+NE × S+SE. A versão *inferencialmente correta* do B8. Dumbbell dos 10 maiores |Δ-MH|. Esforço alto · Score 16 · **joia técnica**.
- **E9 Mapas do Brasil** — 4 coropléticos da nota TRI por UF (SP 543 → PA 480) + mapa da **precisão** (TIF/pico por UF) + mapa de abstenção/branco dia 2. Esforço médio · Score 13–15.
- **E10 Mil & zero + concordância entre corretores** — motivos do zero (`TP_STATUS_REDACAO`), qual competência mais aciona a 3ª correção (`AV1..AV4`), kappa ponderado. Esforço médio · Score 14 (roadmap A6/A8).
- **E11 Ridgeline rede × escala TRI** — distribuições completas de `NU_NOTA` por rede (não só média), um violino por área. Esforço médio · Score 14.
- **E12 Person-fit por escola/região** — índice lz (acerta difícil/erra fácil) por urbano×rural × rede. Esforço alto · Score 13 (B7 + perfil).
- **E13 KR-20 / discriminação observada por área × rede** — confiabilidade clássica por rede. Esforço médio · Score 13 (B9 + perfil).

### 🔵 TRILHA "Retrato do candidato 2025" (`PARTICIPANTES` — perfil narra perfil; TRI entra só como ressalva didática, **nunca cruza nota**)

- **E14 Primeira geração — quem é o primeiro da família a encarar o ENEM** (`Q001`/`Q002`): pai com superior **15,3%**, mãe **23,3%**; "não sei" do pai **12,0%** vs mãe **4,5%**. Pirâmide divergente. **Score 17**, esforço baixo, forte identitário. *(números exatos, base inteira.)*
- **E15 A geração do celular** (`Q020/Q021/Q022`): **98,2% têm celular, 52,1% não têm computador**, 11,7% sem internet. Estratégico para o XTRI (app no celular). Score 16, esforço baixo.
- **E16 Renda dividida** (`Q005`×`Q007`, heatmap): 44,2% até 1 SM; domicílio mais comum = 4 pessoas; 22,7% em casas de 5+. Score 13 — **cuidado: não computar renda per capita** (faixas, não valor).

---

## 4. Recomendação de execução (primeira leva sugerida)

| Ordem | Estudo | Por que primeiro |
|---|---|---|
| 1 | **E1** Função de informação × rede | Flagship: o conceito TRI mais central encontra o perfil joinável; âncora de nota por rede já pronta |
| 2 | **E2** Redação: gargalo de competência por rede | Único que cumpre 100% o pedido (rubrica × perfil); esforço baixo; gap redação +203 já existe |
| 3 | **E4** Redação prevê as objetivas? | Gancho perfeito na voz do aluno; achado contraintuitivo; barato |
| 4 | **E3** Inglês × espanhol item-level | Decisão estratégica real do aluno; aprofunda asset existente |
| 5 | **E14/E15** Retrato do candidato | Quick wins de engajamento, números exatos, esforço baixo |

**Quick wins (esforço baixo):** E2, E4, E7, E14, E15.
**Alto ineditismo + valor TRI×perfil:** E1, E2, E3, E5, E8.

---

## 5. Verificação (ao executar cada tema)
1. Rodar o cálculo na coluna citada; conferir contagens (presentes CN/MT ~3,18 mi; CH/LC ~3,37 mi; 4,81 mi linhas; subset escolar 1,74 mi).
2. Spot-check de 3–5 valores contra a fonte (planilha TRI Azul, PDF da prova, dicionário).
3. Arte no padrão (sem fundo preto, marca X-TRI, fonte INEP, "sexo feminino/masculino").
4. Nunca preencher nulo/estimar; anuladas marcadas; redação múltiplo de 20; **perfil de `PARTICIPANTES` nunca cruza nota**.

## 6. Insumos
- Dados: `DADOS/RESULTADOS_2025.csv`, `DADOS/PARTICIPANTES_2025.csv`, `DADOS/ITENS_PROVA_2025.csv`.
- Já calculado: `estudo_perfil_tri/anchor_nota_por_perfil_RESULTADOS.json` + `TEASER_nota_por_rede.png` + scripts.
- Reaproveitar: `analise_psicometria_2025/` (TIF/CCI), `estudo_tri_marginal/`, `dif_chunk.py` (acerto byte-a-byte, split LC), `TRI_ITENS_AZUL_ENEM2025.xlsx`.
</content>
