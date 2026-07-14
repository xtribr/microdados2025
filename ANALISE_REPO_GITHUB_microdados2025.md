# Análise do repositório GitHub — xtribr/microdados2025

Análise feita clonando o repositório público (`git clone`), inspecionando os 645 arquivos versionados e comparando com a pasta local conectada. Achados abaixo checados diretamente (grep de segredos, teste de pixel em amostra de artes, leitura de scripts, `git status`/`check-ignore`), não por inferência.

## Resumo executivo

O repositório é o backup público das produções da XTRI (estudos TRI/psicometria + conteúdo de posts sobre o ENEM 2025), não dos microdados. A regra de nunca versionar dado bruto ou em grão individual está, na prática, sendo respeitada — com uma exceção pontual de configuração (item 3) que vale corrigir esta semana. O maior gap é reprodutibilidade: a maioria dos scripts não roda em outra máquina sem edição manual. Há também um descompasso de marca entre o `CLAUDE.md` (fonte de verdade) e três documentos operacionais que ainda citam a assinatura antiga.

## 1. O que é o repositório

Repositório público, **148 MB, 645 arquivos, um único commit** ("Backup dos estudos XTRI ENEM 2025"). É espelho de parte da sua pasta local: o branch local `github-backup` está 100% sincronizado com `origin/main`, sem commits pendentes — o backup está atualizado.

Conteúdo: 90 scripts Python, 20 scripts R, 372 PNGs, 56 JSONs, 34 CSVs, 3 XLSX. Estrutura consistente — cada estudo/post segue o padrão `compute_*.py` (cálculo) + `*_graphics.py`/`ggplot_*.R` (arte) + `LEIA-ME.md` (método) + `TEXTOS*.md`/`POST_WORDPRESS*.md` (legenda). 12 pastas `estudo_*` (psicometria/TRI: CCI, função de informação, distratores, discriminação, polêmicas, recortes por escola) e 13 pastas `post_*`/`posts_*` (Instagram/WordPress/LinkedIn), além dos documentos de projeto (`CLAUDE.md`, `PADRAO_DESIGN_XTRI.md`, `SEO_PLAYBOOK`, dois roadmaps) e dois XLSX-produto (`TRI_ITENS_AZUL_ENEM2025.xlsx` com 185 itens, `RANKING_ESCOLAS_RN_54x54...xlsx` com 27 escolas) — ambos batendo exatamente com o que os respectivos LEIA-ME descrevem.

## 2. Segurança e privacidade — sem problemas encontrados

Como o repo é **público**, testei especificamente por vazamento. Busquei por chaves de API, tokens, senhas, `.env`/credenciais e não encontrei nenhum. Busquei por CPF e e-mail em CSV/JSON/scripts: nenhuma ocorrência. Todo dado versionado é agregado (por escola ou por item, com `n` de dezenas a milhões), nunca linha-a-aluno — confirmado inspecionando amostras de `estudo_marista_natal`, `estudo_dombosco_saoluis` e `estudo_cei_natal`. Comparando a pasta local com o repo, confirmei que `DADOS/`, `PROVAS E GABARITOS/`, `INPUTS/`, o Excel de 71 MB dos microdados e os arquivos `*_alunos.csv` realmente não subiram — o `.gitignore` está fazendo o que promete.

## 3. Governança de dados — uma falha de configuração a corrigir

Achei uma exceção pontual ao ponto acima. As pastas `DICIONÁRIO/` e `LEIA-ME E DOCUMENTOS TÉCNICOS/` (materiais oficiais do INEP — que pela sua própria regra de ouro nunca deveriam subir) **estão listadas no `.gitignore`, mas o git não está de fato as ignorando**: `git status` as mostra como "untracked" em vez de ignoradas.

Causa: o macOS grava esses nomes de pasta com acento em Unicode **NFD** (decomposto), enquanto o `.gitignore` tem os mesmos nomes em **NFC** (precomposto) — são bytes diferentes para o mesmo texto visível, e o git compara byte a byte. Hoje isso não vazou nada porque ninguém rodou um `git add` genérico nessas pastas. Mas o mecanismo de proteção está, tecnicamente, furado para esses dois nomes: um `git add .`/`git add -A` sem revisão colocaria material oficial do INEP no repo público.

Correção (uma linha, local, sem tocar no GitHub): `git config core.precomposeunicode true` no repositório local — ou, alternativa mais portátil, duplicar as duas entradas no `.gitignore` nas duas formas Unicode.

## 4. Reprodutibilidade dos scripts — gap real

O `README.md` promete: baixe os microdados, coloque em `DADOS/`, rode o `compute_*.py`. Na prática, **81 dos 110 scripts (74%)** têm caminho absoluto hardcoded apontando para uma máquina ou sessão específica — a maioria para `/Volumes/Kingston 1/microdados_enem_2025/...` (seu Mac), mas vários apontam para pastas temporárias de sessões antigas do Claude/Cowork, por exemplo:

- `analises_primi_2025_cop30/scripts/dif_chunk.py` → `/sessions/funny-kind-hawking/mnt/...`
- `estudo_perfil_tri/anchor_nota_por_perfil.py` → grava saída em `/private/tmp/claude-502/.../scratchpad/...`

Esse segundo tipo é o mais frágil: são pastas de sessão que são apagadas ao final — nem você consegue re-rodar esses scripts hoje sem editar o caminho manualmente primeiro. Isso não compromete os números já publicados (a lógica em si está correta, ver item 6), mas quebra a promessa de "reprodutibilidade" do próprio README para qualquer execução futura, sua ou de terceiros. Não há `requirements.txt`/`environment.yml`; dependências (pandas, openpyxl, matplotlib, pymupdf, ggplot2, jsonlite, gridExtra) estão só documentadas em prosa.

## 5. Consistência de marca — três documentos desatualizados

O `CLAUDE.md` (fonte de verdade, datado jul/2026) aposentou oficialmente a assinatura **"Dados reais ou nada."** em favor de **"Transformamos dados em aprovações."**, e o `README.md` já usa a nova frase. Só que `PADRAO_DESIGN_XTRI.md`, `SEO_PLAYBOOK_microdados_XTRI.md` e `.claude/brand-voice-guidelines.md` — os três manuais que na prática orientam a produção de arte e texto novos — ainda citam a assinatura antiga como regra vigente. Quem seguir esses três documentos ao pé da letra (em vez do `CLAUDE.md`) vai produzir peça com a frase errada.

## 6. Amostra de qualidade técnica — passou

Revisei o código de dois scripts centrais para checar se a lógica implementa mesmo as regras de integridade declaradas: `dif_chunk.py` (alinhamento de idioma inglês/espanhol em LC e exclusão de itens anulados) e `anchor_nota_por_perfil.py` (cruzamento perfil × nota). Ambos implementam corretamente o que os documentos prometem: não cruzam `PARTICIPANTES` com `RESULTADOS`, excluem itens anulados sem preencher valor, tratam nota objetiva zero como ausência mas redação zero como dado real. Encoding `latin-1` e delimitador `;` — corretos para os Microdados INEP. Também testei 7 PNGs de posts diferentes (pixel dos 4 cantos + centro): nenhum fundo preto, dimensões batendo com os formatos exigidos (1080×1350 feed, 1080×1920 story, múltiplos exatos de 1200×630 para WordPress). Amostra pequena, mas 100% conforme ao `PADRAO_DESIGN_XTRI.md`.

## 7. Organização — pontos menores

Pastas `files 2`, `files 3`, `files 4` e `posts_idade - OK` quebram o padrão descritivo do resto do repo (`estudo_*`, `post_*`) — parecem exports/uploads sem renomear. Não afeta funcionamento, mas dificulta achar conteúdo depois. O histórico do git é um único commit de backup: ótimo para simplicidade, mas significa que não dá para usar `git log`/`git blame` para saber quando cada estudo foi de fato produzido.

## Recomendações, em ordem de prioridade

| Prioridade | Ação | Motivo |
|---|---|---|
| Alta | Rodar `git config core.precomposeunicode true` no repo local (ou duplicar as entradas NFC/NFD no `.gitignore`) | Fecha a brecha real na regra de "nunca versionar dado oficial do INEP" |
| Alta | Atualizar a assinatura em `PADRAO_DESIGN_XTRI.md`, `SEO_PLAYBOOK_microdados_XTRI.md` e `.claude/brand-voice-guidelines.md` | Hoje contradizem o `CLAUDE.md`; risco de peça nova sair com frase aposentada |
| Média | Trocar paths hardcoded por variável de ambiente/argumento (`DADOS_DIR`) nos ~81 scripts, começando pelos que apontam para pastas de sessão já inexistentes | Sem isso, "reprodutibilidade" no README é só promessa |
| Baixa | Adicionar `requirements.txt`/`environment.yml` | Facilita reexecução por você mesmo em outra máquina |
| Baixa | Renomear `files 2/3/4` e `posts_idade - OK` para nomes descritivos | Organização/achabilidade, sem urgência |
