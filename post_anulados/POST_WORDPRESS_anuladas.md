<!-- ===================== SEO / RankMath ===================== -->
**Focus keyphrase:** questões anuladas do ENEM 2025

**Prova de ineditismo — frases-foco JÁ usadas nos outros posts (nenhuma colide):**
- questões em branco no ENEM (`posts_fadiga`)
- reaplicação do ENEM (`estudo_curva_prova_1a_2a`)
- ordem das questões no ENEM (`estudo_dificuldade_ppl`)
- como funciona a nota do ENEM (`analise_psicometria_2025`)
- questões mais chutáveis do ENEM (`carrossel_chutadas_2025`)
- TRI das questões do ENEM 2025 (`TRI_dos_itens_post`)
- abstenção no ENEM 2025 (`posts_abstencao`)
- (planejadas no playbook: questões mais polêmicas ENEM 2025 · divergência entre corretores redação ENEM · questões mais difíceis ENEM 2025 · como funciona a TRI do ENEM · quem tirou 1000 na redação ENEM 2025)

**Título SEO (H1):** Questões anuladas do ENEM 2025: a autópsia das 6
**Slug:** questoes-anuladas-do-enem-2025  *(30 caracteres — ≤ 75 ✓)*
**Meta description (141 caracteres):** Questões anuladas do ENEM 2025: a autópsia das 6 — 3 vazadas e 3 reprovadas pela TRI. Análise item a item com os microdados oficiais do INEP.
**Keyphrases secundárias:** questão anulada ENEM · vazamento ENEM 2025 · efeito Edcley · TRI do ENEM · microdados ENEM 2025
**Categoria:** Microdados ENEM · **Tags:** ENEM 2025, questões anuladas, TRI, INEP, microdados, vazamento
**Imagem destacada:** `post_anulados/destacada_wp_anuladas_1200x630.png` (1200×630, pronta) — *alt:* "Questões anuladas do ENEM 2025: inventário das 6 com o motivo oficial do INEP — XTRI."
<!-- schema Article + FAQPage · author: Prof. Alexandre Emerson (XTRI) · datePublished -->
<!-- ====================================================== -->

# Questões anuladas do ENEM 2025: a autópsia das 6

As **questões anuladas do ENEM 2025** deixaram rastro — e ele está público nos [microdados oficiais do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). O campo `TX_MOTIVO_ABAN` registra, preto no branco, o motivo de cada uma das **6 anulações**. Fui atrás do rastro, item a item, nas marcações de cerca de **3,18 milhões de candidatos** da 1ª aplicação regular. Resultado da autópsia: 3 caíram por **vazamento** ("previamente exposto", o famoso efeito Edcley) e 3 morreram pela **própria estatística da prova**. Sem teoria da conspiração — só o que o dado mostra.

## O inventário das 6 questões anuladas do ENEM 2025

![Questões anuladas do ENEM 2025: inventário das 6 com o motivo oficial registrado pelo INEP](palestra_2025/graficos/g15_inventario_anulados.png)
*As 6 questões anuladas do ENEM 2025 e o motivo oficial de cada uma (TX_MOTIVO_ABAN). Fonte: Microdados ENEM 2025 / INEP, análise XTRI.*

| # | Área | Motivo oficial (TX_MOTIVO_ABAN) | Aplicação | O que os dados mostram |
|---|------|-------------------------------|-----------|------------------------|
| 1 | Ciências da Natureza | Previamente exposto | Regular (P1) | Curva saudável; piso dos alunos fracos = 26,7% |
| 2 | Ciências da Natureza | Previamente exposto | Regular (P1) | Curva saudável; piso = 9,4% (abaixo do acaso) |
| 3 | Matemática | Previamente exposto | Regular (P1) | Curva saudável; piso = 23,2% |
| 4 | Ciências da Natureza | Problema de convergência | Regular (P1) | Curva em U no gabarito oficial (B): 26% → 18% → 69% |
| 5 | Matemática | Problema de convergência | Regular (P1) | Gabarito oficial (A) cai de 15% para 8% conforme a nota sobe |
| 6 | Ciências Humanas | Bis<0,01 | 2ª aplicação (n=309) | Correlação bisserial ~zero; gabarito D não lidera em nenhum grupo |

Detalhe importante: nas 3 questões vazadas, o INEP **apagou o gabarito** dos microdados (um "X" no lugar da letra). Nas outras 3, o gabarito oficial permanece registrado — e é isso que permite a autópsia.

## As anuladas pela TRI: quando a estatística reprova a questão

Antes dos casos, 30 segundos de técnica. A nota do ENEM vem do modelo **3PL**, em que cada questão é descrita por três parâmetros: **A** (discriminação: o quanto o item separa quem sabe de quem não sabe), **B** (dificuldade) e **C** (probabilidade de acerto no chute). Com eles, o modelo desenha a **ICC** — a curva característica do item, a chance de acerto em cada nível de proficiência. Uma regra é inegociável: **a ICC deve ser crescente**. Quanto melhor o aluno, maior a chance de acertar. Quando o padrão real de respostas contraria isso, a calibração **não converge**: não existe combinação de A, B e C que explique aquele comportamento. A TRI, na prática, reprova a questão — e o INEP anula.

Foi o que aconteceu com 3 das questões anuladas do ENEM 2025.

### Matemática: o gabarito oficial que despenca

![Uma das questões anuladas do ENEM 2025 por problema de convergência: curva da questão de Matemática](palestra_2025/graficos/g13_anulado_tri_MT.png)
*Gabarito oficial A cai conforme a nota sobe; os melhores convergem em D. Fonte: Microdados ENEM 2025 / INEP, análise XTRI.*

Na questão de Matemática, a marcação no gabarito oficial (**A**) **cai de 15% para 8%** conforme a nota do candidato sobe. Enquanto isso, os melhores alunos convergem em massa para a alternativa **D**: **73% na faixa mais alta de nota**. Formulação honesta: os dados não me autorizam a cravar qual seria a resposta "certa". O que eles mostram é que **o padrão é incompatível com o modelo 3PL** — a curva do gabarito deveria subir com a proficiência, e ela desce. A calibração não convergiu, e o item saiu da prova.

### Ciências da Natureza: a curva em U

![Curva em U da questão de Ciências da Natureza anulada pela TRI no ENEM 2025](palestra_2025/graficos/g13_anulado_tri_CN.png)
*A curva em U de uma das questões anuladas do ENEM 2025: 26% nos fracos, 18% no meio, 69% no topo. Fonte: Microdados ENEM 2025 / INEP, análise XTRI.*

O caso de Ciências da Natureza é ainda mais curioso: a marcação no gabarito oficial (**B**) começa em **26%** entre os alunos de nota baixa, **cai para 18%** no meio da distribuição e **dispara para 69%** no topo. Uma curva em **U**. Para a TRI, é um monstro matemático: nenhuma ICC crescente descreve uma chance de acerto que desce e depois sobe. De novo: não se trata de apontar erro de resposta, e sim de constatar que a calibração não fecha. Item anulado.

### Ciências Humanas: a questão que não mede nada

![Correlação bisserial da questão de Ciências Humanas anulada na 2ª aplicação do ENEM 2025](palestra_2025/graficos/g13_anulado_tri_CH.png)
*Gabarito D não lidera em nenhum grupo: fracos 25%, médios 12%, fortes 18% — e os fortes preferem E (51%). Fonte: Microdados ENEM 2025 / INEP, análise XTRI.*

Das questões anuladas do ENEM 2025, esta é a única fora da aplicação regular: um item de Ciências Humanas exclusivo da **2ª aplicação** (apenas **309 respondentes**), com o motivo mais técnico de todos, **"Bis<0,01"**. A **correlação bisserial** mede a relação entre acertar aquele item e a nota total na prova — o termômetro mais simples de que uma questão "funciona". Aqui ela deu **praticamente zero**: acertar ou errar não dizia nada sobre o nível do candidato. O retrato é eloquente: o gabarito oficial (**D**) **não lidera em nenhum grupo** — 25% entre os fracos, 12% entre os médios, 18% entre os fortes. Os melhores preferiram **E**, com **51%**. Um item que não separa ninguém de ninguém não mede nada; a TRI o descarta.

## As vazadas e o efeito Edcley: houve vantagem em massa?

As outras 3 questões anuladas do ENEM 2025 — 2 de Ciências da Natureza e 1 de Matemática — caíram pelo motivo "**Previamente exposto**": circularam antes da prova, no episódio do **efeito Edcley**. O INEP apagou até o gabarito. A pergunta que todo mundo fez: **quem viu antes levou vantagem?**

O teste é direto. Fraude em massa deixa rastro inconfundível: aluno de nota baixa acertando **muito acima dos 20%** do chute puro entre 5 alternativas. Corrigi as marcações desses 3 itens, faixa por faixa de nota, usando como referência o consenso dos alunos de nota mais alta.

![Curva de marcação de questão vazada de Ciências da Natureza no ENEM 2025 — comportamento saudável](palestra_2025/graficos/g14_exposto_CN_141774.png)
*Entre as questões anuladas do ENEM 2025 por exposição, a curva é de item saudável: piso no chute, topo em consenso. Fonte: Microdados ENEM 2025 / INEP, análise XTRI.*

Resultado: nos alunos de nota **350–449**, a marcação na resposta-consenso ficou em **26,7%, 9,4% e 23,2%** — no nível do acaso (20%), e uma delas **abaixo** dele. No topo, o consenso dos fortes foi de **62,5%, 82,6% e 68,1%**. É a assinatura de item **saudável**: piso no chute, curva subindo degrau a degrau com a nota. Conclusão honesta: **se alguém se beneficiou do vazamento, foi um grupo pequeno demais para aparecer numa base de 3 milhões**. A anulação foi **preventiva**: diante de exposição comprovada, remover o item protege a isonomia do exame antes que qualquer vantagem localizada contamine a régua de todos.

## O custo invisível: Natureza valeu 42 e Matemática 43

Nenhuma das questões anuladas do ENEM 2025 entra na nota de quem quer que seja — a TRI simplesmente as ignora no cálculo, sem "ponto de presente". O custo é outro, e é coletivo: com as anulações, **Ciências da Natureza mediu 2025 com 42 itens** (2 expostos + 1 convergência) e **Matemática com 43** (1 exposto + 1 convergência), contra 45 de Linguagens e 45 de Humanas na aplicação regular. Menos itens = menos chances de mostrar o que sabe e um pouco menos de precisão na medida. Quem estudou o conteúdo daquelas questões perdeu a chance de pontuar com ele.

## Perguntas frequentes sobre as questões anuladas do ENEM 2025

**Quantas foram as questões anuladas do ENEM 2025?** Seis, segundo o campo TX_MOTIVO_ABAN dos microdados do INEP: 3 por exposição prévia (vazamento — 2 de Ciências da Natureza e 1 de Matemática), 2 por problema de convergência na TRI (1 CN e 1 MT) e 1 por correlação bisserial abaixo de 0,01 (Ciências Humanas, apenas na 2ª aplicação).

**Questão anulada dá ponto no ENEM?** Não. Nenhuma das questões anuladas do ENEM 2025 dá ponto: o item é excluído do cálculo da TRI — não conta a favor nem contra ninguém.

**O gabarito da questão de Matemática anulada estava errado?** Os microdados não permitem afirmar isso. Eles mostram que o padrão de respostas é incompatível com o modelo 3PL — a curva do gabarito deveria crescer com a nota e fez o contrário — e que a calibração não convergiu. Por isso o INEP anulou.

---

As questões anuladas do ENEM 2025 mostram a TRI trabalhando de guardiã da prova. Quer entender o que cada questão vale de verdade na sua nota — e treinar com simulados corrigidos pela mesma TRI do ENEM? Vem para a plataforma: [app.rankingenem.com](https://app.rankingenem.com). **Transformamos dados em aprovações.**

*Por Prof. Alexandre Emerson (Xandão) — professor, CEO da XTRI e analista de microdados do ENEM. Leia também: [Microdados do ENEM: o guia completo](microdados-do-enem-guia-completo), [TRI das questões do ENEM 2025](tri-das-questoes-do-enem-2025), [questões mais chutáveis do ENEM](questoes-mais-chutaveis-do-enem-2025) e [como funciona a nota do ENEM](como-funciona-a-nota-do-enem). Fonte: Microdados ENEM 2025 / INEP (ITENS_PROVA_2025, TX_MOTIVO_ABAN; respostas da 1ª aplicação regular).*

*Dados reais ou nada.*

<!-- ===================== LINKS USADOS ===================== -->
**Link externo (dofollow):** https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem (no 1º parágrafo)
**Links internos:**
- Pilar: `microdados-do-enem-guia-completo` — Microdados do ENEM: o guia completo
- Satélite 1: `tri-das-questoes-do-enem-2025` — TRI das questões do ENEM 2025
- Satélite 2: `questoes-mais-chutaveis-do-enem-2025` — Questões mais chutáveis do ENEM
- Satélite 3: `como-funciona-a-nota-do-enem` — Como funciona a nota do ENEM
- CTA: https://app.rankingenem.com
<!-- ====================================================== -->

<!-- ===================== CHECKLIST RankMath ===================== -->
| Item RankMath | Status | Evidência |
|---|---|---|
| Frase-foco inédita | ✅ | "questões anuladas do ENEM 2025" não usada em nenhum dos 7 posts existentes nem nas planejadas do playbook (lista acima) |
| Frase-foco no Título SEO (início, número + impacto) | ✅ | "**Questões anuladas do ENEM 2025**: a autópsia das **6**" — começa com a frase, números (2025, 6), palavra de impacto "autópsia" |
| Frase-foco na meta description ≤155 | ✅ | Literal na meta; 144 caracteres |
| Frase-foco no slug, URL ≤75 | ✅ | `questoes-anuladas-do-enem-2025` (30 caracteres) |
| Frase-foco nos primeiros 10% | ✅ | 1ª frase do 1º parágrafo |
| Frase-foco em ≥1 H2 | ✅ | 2 H2: "O inventário das 6 questões anuladas do ENEM 2025" e "Perguntas frequentes sobre as questões anuladas do ENEM 2025" |
| Frase-foco em ≥1 alt de imagem | ✅ | Alt da imagem destacada/inventário: "Questões anuladas do ENEM 2025: inventário das 6…" |
| Densidade 1–1,5% | ✅ | 16 ocorrências ÷ 1.479 palavras (corpo com legendas e alts) = **1,08%**; só texto visível: 14 ÷ 1.404 = **1,00%** |
| Link externo dofollow autoritativo | ✅ | gov.br/inep (microdados), no 1º parágrafo, sem nofollow |
| Links internos (pilar + ≥2 satélites) | ✅ | Pilar + 3 satélites (lista acima) |
| ≥600 palavras | ✅ | 1.479 palavras no corpo do artigo (contagem via script, H1 → assinatura) |
| Voz/terminologia | ✅ | 1ª pessoa, sem "loteria", sem buzzword-muleta; "incompatível com o 3PL / calibração não convergiu" (nunca "gabarito errado") |
| Fonte citada | ✅ | Microdados ENEM 2025 / INEP em todas as legendas + rodapé |
<!-- densidade: recalcular após qualquer edição do corpo (16 occ / 1.479 palavras em 03-jul-2026) -->
<!-- ====================================================== -->
