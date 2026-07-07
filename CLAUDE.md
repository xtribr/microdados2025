# CLAUDE.md — Regras fixas do projeto XTRI (ENEM)

> Este arquivo é carregado automaticamente em toda sessão. **Siga-o sempre, sem exceção.** Detalhe completo em `PADRAO_DESIGN_XTRI.md`.

## ⛔ INVIOLÁVEL — verificar ANTES de entregar qualquer arte
Antes de devolver QUALQUER card/gráfico, renderizar e **conferir com zoom os 4 cantos e o rodapé**:
1. **Nenhum texto sobre imagem, barra, foto ou outro texto.** Zero sobreposição.
2. **Nada sai da arte.** Tudo dentro das margens, com folga até a borda.
3. **Nota de rodapé (fonte/método/ressalva) em fonte MENOR que o corpo** — JetBrains Mono, cinza, **≤ 10pt**.
4. **Respiro mínimo: ≥ 60px** entre conteúdo/eixo e o rodapé; **≥ 28px** entre blocos. O rodapé tem **banda própria** — nenhum eixo/barra/rótulo invade.
5. Número-herói nunca "estoura" a faixa (Outfit Bold ~40–48).

Se houver qualquer dúvida de colisão/borda, **dar mais espaço e re-renderizar**. Não entregar sem essa checagem.

## ⛔ INTEGRIDADE DE DADOS
- **Nunca inventar/estimar dado.** Só dado real (Microdados INEP, Baserow, arquivo fornecido).
- Valor vindo de modelo é rotulado como **"esperado/previsto"**, nunca como observado.
- **PPL / 2ª aplicação não tem taxa de acerto** no nosso dado → usar só TRI (a, b, c); acerto = "esperado (θ=0)"; marcar "sem acerto observado".
- Socioeconômico (PARTICIPANTES) **não cruza** com nota (RESULTADOS) — sem chave comum.
- Itens anulados: marcar, nunca preencher. Redação é múltiplo de 20.
- Sempre citar **Fonte: Microdados ENEM <ano> / INEP**.

## 🎨 MARCA XTRI
- Cores: coral `#FA5230` (escuro `#E8431F`) · cyan `#1FAFEF` (escuro `#1597D8`) · tinta `#1D1D20` · cinza `#8C9298` · fundo `#F1F1F2` · cards brancos. **Proibido fundo preto.**
- Categorias dificuldade: Fácil `#56C2F2` · Médio `#C7CBD0` · Difícil `#FB9276` · Muito difícil `#FA5230`.
- Fontes: **Outfit** (títulos/corpo) + **JetBrains Mono** (rótulos/notas).
- Logo **X-TRI** topo-esquerda · assinatura **"Transformamos dados em aprovações."** ("dados" cyan, "aprovações" coral) no rodapé — a antiga "Dados reais ou nada." foi APOSENTADA (jul/2026): não usar em NENHUMA arte nova · handle **@xandaoxtri** · domínio **app.rankingenem.com**.
- Rodapé: nota de fonte NUNCA colada na assinatura — mínimo ~50px de respiro entre as duas.
- "Dificuldade TRI" = **b × 100 + 500**. DIF (0–100) = 100×(1−P(θ=0)).
- Terminologia: "sexo feminino/masculino". **Proibido** "loteria" e buzzword-muleta.

## 📐 FORMATOS — sempre gerar as DUAS versões
- Instagram **feed 1080×1350** + **story 1080×1920** (toda arte de post = as duas).
- WordPress: destaque/social **1200×630**; inline em paisagem (largura 1200) com rodapé folgado.

## 🔎 SEO — RankMath (todo post WordPress tem que passar VERDE)
A análise é feita no **RankMath**. A **frase-foco (exata, mesma grafia)** DEVE aparecer em TODOS estes:
1. **Título SEO** (de preferência no começo) — e o título deve ter um **número** e uma palavra de impacto.
2. **Meta descrição** (≤ 155 car., com a frase-foco literal).
3. **Slug/URL** (a frase-foco "slugificada"; ex.: foco "questões mais chutáveis do ENEM" → slug `questoes-mais-chutaveis-do-enem...`). URL ≤ 75 car.
4. **Primeiros 10%** do texto (1º parágrafo).
5. **≥1 subtítulo H2** e **≥1 `alt` de imagem**.
- **Densidade** da frase-foco ~**1–1,5%** (nem 0,x%, nem keyword stuffing).
- **≥1 link externo dofollow** para fonte autoritativa (ex.: INEP `gov.br/inep`) **+** links internos para o pilar/satélites.
- Conteúdo **≥ 600 palavras**. Frase-foco **inédita** (não reutilizar entre posts).
> Antes de entregar qualquer post: conferir título/meta/slug/1º parágrafo/H2/alt batendo com a frase-foco exata, link externo presente. Detalhe em `SEO_PLAYBOOK_microdados_XTRI.md`.

## ✍️ VOZ
Técnica mas acessível, autoral em 1ª pessoa (professor/CEO XTRI), orientada a dado, energia sem exagero. Sempre fundamentar em número real e citar a fonte INEP.

## 🧭 NOMENCLATURA (evitar ambiguidade)
- **P1 / P2** = aplicação (1ª regular / 2ª PPL-reaplicação).
- **Posição** da questão no caderno = "Q01…Q45" ou "posição 01" — **não** usar "P" para posição (conflita com P1/P2).
