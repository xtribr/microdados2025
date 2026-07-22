---
name: xtri-instagram-design
description: Cria artes de Instagram (carrossel, card, capa, story) no padrão visual da XTRI — fundo claro, Outfit + JetBrains Mono, coral #FA5230 e cyan #1FAFEF, logo X-TRI, assinatura "Transformamos dados em aprovações.", CTA xtri.online. Use SEMPRE que o usuário pedir post/card/carrossel/capa/story do Instagram no estilo XTRI, arte de dados educacionais (ENEM/TRI), ou mencionar "design XTRI", "arte pro feed", "carrossel", "story 1080x1920". NÃO usar para gráficos científicos limpos sem marca (aí é ggplot puro).
---

# XTRI · Sistema de design para Instagram

Você desenha artes de dados educacionais (ENEM / TRI) no estilo da XTRI: **limpo, Apple-like, fundo claro**, hierarquia forte, muito respiro. Nada de traço "cartunesco" nem fundo escuro. As artes são feitas em **matplotlib** com o helper `xtri_deck.py` (nesta pasta).

## Fluxo obrigatório (NUNCA pule etapas)

1. **Entenda o formato.** Todo post = **feed 1080×1350** E **story 1080×1920** (gere as duas). Capa de WordPress = 1200×630.
2. **Monte com `xtri_deck.py`** (veja `recipes.md` para os moldes prontos: capa, card de conteúdo, card com print, card de estatística, tabela de ranking, fecho/CTA).
3. **RENDERIZE e CONFIRA COM ZOOM cada card antes de entregar** — esta é a etapa que separa uma arte boa de uma amadora. Regras invioláveis abaixo.
4. **Escreva a legenda em TEXTO PURO** (sem markdown — nem `**`, nem `*`, nem `#`, nem `[](`). O Instagram mostra esses símbolos literais. Ênfase só com CAIXA ALTA ou "→". Máx. ~2.200 caracteres.

## Design tokens (constantes em `xtri_deck.py`)

- **Fundo:** `BG` #F1F1F2 (claro). **PROIBIDO fundo preto/dark mode.** Cards brancos `CARD`.
- **Cores:** tinta `INK` #1D1D20 · cinza `GRAY` #8C9298 · **coral** `CORAL` #FA5230 (escuro #E8431F) · **cyan** `CYAN` #1FAFEF (escuro #1597D8). Acentos saturados com parcimônia.
- **Dificuldade TRI** (só quando o tema for dificuldade): Fácil #56C2F2 · Médio #C7CBD0 · Difícil #FB9276 · Muito difícil #FA5230.
- **Fontes:** **Outfit** (títulos/corpo — `outfitB`/`outfit`) + **JetBrains Mono** (rótulos, notas, números técnicos — `monoB`/`mono`). Aponte `XTRI_FONT_DIR` para os `.ttf` (Google Fonts).
- **Logo** X-TRI topo-esquerda (`logo(ax, ~182, 84)`). Aponte `XTRI_LOGO` para o PNG.

## Anatomia de um card (feed 1080×1350, margem M=64)

```
┌─ logo X-TRI (topo-esq, y~84)          TAG · CONTEXTO (mono, cinza, topo-dir) ─┐
│                                                                              │
│  TÍTULO (Outfit Bold ~40–62, INK ou accent)                                  │
│  subtítulo/linha de apoio (Outfit Regular ~15–24, GRAY)                      │
│                                                                              │
│  ────────────  CONTEÚDO  ────────────                                        │
│  (gráfico, número-herói, print recortado, tabela, ilustração)                │
│                                                                              │
│  ── banda do rodapé (própria) ──                                             │
│  Fonte: ... (mono, cinza, ≤10pt)        Transformamos dados em aprovações.  1/6│
└──────────────────────────────────────────────────────────────────────────────┘
```

Use `footer(hp, H, "Fonte: ...", "1/6")` — ele já posiciona a nota de fonte, a assinatura e a paginação com o respiro certo.

## ⛔ REGRAS INVIOLÁVEIS — checar renderizando e dando ZOOM antes de entregar

Depois de gerar cada PNG, **abra a imagem e inspecione os 4 cantos e o rodapé**. Se houver qualquer dúvida de colisão/borda, dê mais espaço e **re-renderize**. Não entregue sem essa conferência.

1. **Zero sobreposição.** Nenhum texto sobre imagem, barra, foto ou outro texto. Acentos (Ê, Á, Õ) da linha de baixo não podem tocar a linha de cima → em títulos grandes use entrelinha ≥ ~1,3× o tamanho da fonte.
2. **Nada sai da arte.** Tudo dentro das margens, com folga até a borda. Texto longo não pode vazar do card — trunque no limite da palavra com "…" ou reduza a fonte.
3. **Nota de rodapé em fonte MENOR que o corpo** — JetBrains Mono, cinza, **≤ 10pt**. Ela tem **banda própria**: nenhum eixo/barra/rótulo invade o rodapé.
4. **Respiro:** ≥ 60px entre conteúdo/eixo e o rodapé; ≥ 28px entre blocos; ≥ ~50px entre a nota de fonte e a assinatura.
5. **Número-herói** nunca "estoura" a faixa/card (Outfit Bold ~40–48; confira a largura com `tw()`).
6. **Sombra suave** (a do helper: sem deslocamento lateral, senão a caixa parece torta). Cantos arredondados generosos, bordas finas.
7. **Painéis coloridos NÃO levam sombra** (a sombra desloca a percepção pra esquerda e quebra a simetria).
8. **Glifos que viram "tofu"** na Outfit/JetBrains: `≥ ≤ θ ² ×`(às vezes) e **emojis**. Escreva "10 ou mais", "theta", "a2"; nada de emoji no texto.

## Grade segura — correção obrigatória de 21/07/2026

Estas regras existem porque um card pode estar tecnicamente dentro da tela e ainda assim parecer amador: uma faixa pode atravessar um selo, o H1 pode esmagar o H2 e um vazio pode quebrar a narrativa.

1. **Cabeçalho é uma zona reservada.** No feed, reserve `y=40–165` para logo, contexto e selo da série. O selo fica em `y~128–142`; qualquer linha/faixa decorativa só pode começar abaixo de `y=154`. Nunca desenhe uma linha por baixo ou por cima do texto do selo.
2. **Hierarquia tipográfica fixa.** H1 do feed: `40–44pt` (máximo 46); H1 do Story: `42–48pt` (máximo 50). H2/subtítulo: `20–23pt`. Rótulo mono: `11–13pt`. O H1 não pode ser maior que 2,1 vezes o subtítulo e deve ter entrelinha de pelo menos 1,18 vezes o corpo. Dois níveis grandes consecutivos são proibidos.
3. **Densidade mínima.** Entre o fim do cabeçalho e a banda de rodapé, cada feed precisa de pelo menos três zonas informativas: evidência principal + contexto/metodologia + ação. No Story, use quatro zonas ou distribua as três ao longo da altura. Não deixe um vazio vertical contínuo maior que 150px no feed ou 240px no Story, exceto margem deliberada imediatamente abaixo do logo.
4. **Cards de estatística não terminam nos números.** Depois da grade de números, sempre inclua um bloco “COMO LER” e um bloco “O QUE FAZER AGORA” antes do rodapé. O espaço restante deve receber evidência, limite metodológico ou tarefa — nunca ficar vazio.
5. **Pré-voo geométrico.** Antes de salvar, registre os retângulos de cada bloco de texto, faixa e card e passe-os em `assert_layout()`. A função acusa sobreposição e invasão da banda do rodapé. Se falhar, reposicione e renderize de novo.
6. **Revisão em tamanho real.** Além do mosaico, abra cada família de layout em 100%: capa, estatística, ranking, pares, gráfico e pegadinha. O recorte do topo precisa conferir logo, selo, faixa e H1; o do fim precisa conferir CTA e rodapé.
7. **Altura nasce do texto.** Cards de ação, chamadas e métricas multilinha não podem ter altura fixa: calcule `topo + n_linhas × entrelinha + respiro inferior`. A última linha deve terminar pelo menos 28px antes da borda interna.
8. **Guarda entre H1 e subtítulo.** Depois da última linha do H1, reserve no mínimo 20px livres além da caixa tipográfica medida. Descendentes e acentos (como o “P”, “g”, “ç” ou “ê”) nunca podem tocar a primeira linha do subtítulo.

## Convenção Apple-like da XTRI

1. **Um protagonista por capa.** A capa tem uma única manchete H1. Número, dado ou metáfora visual podem ser o herói, mas nunca disputam o mesmo nível do H1. Proibido empilhar “H1 + número gigante + segunda manchete”.
2. **Rótulos servem ao dado.** Evite rótulos genéricos repetidos como “Mentoria Tema-TRI”, “Em uma frase” e “Como ler” quando não acrescentarem contexto. O nome do estudo no cabeçalho e uma microlegenda específica bastam.
3. **Cada tema ganha uma composição.** Mapa usa percurso/camadas; rota usa sequência de prioridade; diagnóstico usa contraste/comparação; pegadinha usa tensão entre facilidade e erro. Não aplique a mesma estrutura de cards às capas de estudos diferentes.
4. **Texto explicativo nunca divide a linha do número.** Métrica e qualificador ficam em faixas verticais distintas, com caixa calculada por `tw()` e altura reservada. Nunca sobrepor texto sobre algarismos grandes.
5. **Cores como sinal, não preenchimento.** Fundo permanece claro; use coral para o insight/alerta e cyan para navegação ou ação. Evite grandes retângulos coloridos quando uma linha, ponto, chip ou área branca comunica melhor.
6. **Ação é específica ao post.** Não repita uma frase genérica em todas as capas. A chamada final precisa apontar a próxima decisão do aluno com base naquele estudo.

## Regras de marca e conteúdo

- **Site: SEMPRE `xtri.online`** em todo CTA/rodapé (nunca outro domínio em material novo).
- **Assinatura:** "Transformamos **dados** em **aprovações**." ("dados" cyan, "aprovações" coral). Handle **@xandaoxtri**.
- **Integridade de dados:** só dado REAL (cite a fonte, ex.: "Microdados ENEM 2025 / INEP"). Valor de modelo = rotular "esperado/previsto", nunca como observado. Nunca inventar número.
- **Voz:** técnica mas acessível, 1ª pessoa (professor), fundamentada em dado. Gancho na dúvida do aluno.
- **Cobertura:** análise por área do ENEM cobre as **4 áreas** (LC, CH, CN, MT).

## Moldes prontos

Veja **`recipes.md`** nesta pasta — tem código copiável para: capa, card de conteúdo, **card de estatística "X% → Y%"**, **card com print de questão recortado**, **gráfico de barras (U-invertido)**, **tabela de ranking**, e **fecho/CTA**. Sempre parametrize `H` (1350 feed / 1920 story) e gere as duas versões no mesmo script.

## Checklist final (antes de dizer "pronto")

- [ ] Renderizei e olhei CADA card com zoom (4 cantos + rodapé).
- [ ] Nenhuma sobreposição; nada vaza; nota de fonte menor e na banda dela.
- [ ] Feed 1080×1350 **e** story 1080×1920 gerados.
- [ ] Fundo claro; cores da marca; logo + assinatura + `xtri.online`.
- [ ] Legenda em texto puro (rodei `grep '\*'` — zero asteriscos).
- [ ] Todo número é real e a fonte está citada.
