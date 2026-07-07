# Roadmap de conteúdo XTRI — "Dores dos alunos" + "Informação para professores" (ENEM 2025)

## Contexto
O usuário (XTRI) está construindo uma série de posts sobre TRI/ENEM a partir dos microdados oficiais 2025. Já publicamos vários ângulos "psicométricos" (dificuldade do item, discriminação Baker, % acerto, CCI, função de informação, paradoxo acerto×nota, mais chutáveis por tema, perfil dos treineiros). Agora ele quer **dois recortes editoriais novos**: (1) **dores dos alunos** — temas emocionais/angustiantes do vestibulando; (2) **informação para professores** — material pedagógico acionável. Este plano é um **roadmap de temas**, cada um com gancho de dado REAL (verificado ou viável), formato, esforço e status (pronto / a calcular). Regras de marca já firmadas: sem jargão como muleta, sem buzzword-muleta ("loteria" proibido), "sexo feminino/masculino", **nada de fundo preto**, gancho na voz do aluno, citar fonte INEP, **nunca inventar dado**.

## Trava de integridade (vale para todo o roadmap)
- **Socioeconômico NÃO cruza com nota** em 2025: `PARTICIPANTES` (perfil, Q001–Q023, sem `NU_NOTA`) e `RESULTADOS` (notas) não têm chave comum (`NU_INSCRICAO`≠`NU_SEQUENCIAL`, confirmado no dicionário oficial). Só dá pra narrar perfil, nunca "pobre tira X, rico tira Y".
- Caderno-base das análises por item = **Azul regular** (LC 1459 / CH 1447 / CN 1483 / MT 1471). Parâmetros TRI são intrínsecos ao item (independem da cor).
- Redação: nota final é **múltiplo de 20** (média de 2 avaliadores). `TP_STATUS_REDACAO` não tem código 5; não existe categoria "ferir direitos humanos" como status.

---

## TRILHA A — Dores dos alunos (emocional, voz do aluno)

### A1. "A redação que mais derruba: qual competência é o gargalo" — A CALCULAR · esforço médio
- **Gancho real**: a competência com menor média nacional puxa a nota de quase todo mundo.
- **Dado**: `RESULTADOS_2025.csv` → média e distribuição de `NU_NOTA_COMP1..5` (cada 0–200). Identificar a comp. de menor média e % de alunos com nota baixa nela.
- **Por que engaja**: redação é a maior angústia; mostra ONDE focar.
- **Formato**: card único ou carrossel (1 card por competência).

### A2. "Quem tira 1000 na redação? (e quem tira 0 — e por quê)" — A CALCULAR · esforço baixo
- **Gancho**: contagem real de notas 1000 vs 0, e o motivo dos zeros.
- **Dado**: `NU_NOTA_REDACAO==1000` (contagem) e `==0` cruzado com `TP_STATUS_REDACAO` (anulada, cópia, em branco, fuga ao tema, texto insuficiente…).
- **Formato**: card único de impacto (número herói) + barra dos motivos de zero.

### A3. "A prova cansa: a partir de qual questão a galera começa a deixar em branco" — A CALCULAR · esforço médio · ALTA NOVIDADE
- **Gancho**: a taxa de "em branco" sobe ao longo da prova — fadiga é coletiva, "não é só você".
- **Dado**: fração de `.` em `TX_RESPOSTAS_*` por posição 1→45 (filtrar `9` em LC = língua não escolhida). Comparar branco×erro×acerto por posição.
- **Formato**: gráfico de linha (branco por posição) + recado anti-ansiedade.

### A4. "Acertei a difícil e errei a fácil — e perdi mais" — PARCIALMENTE PRONTO · esforço baixo
- Já temos `feed_xtri_custo_de_errar_LC.png` e a resposta da aluna. Estender para as 4 áreas / virar série "A TRI responde" (perguntas simuladas rotuladas como "pergunta de vestibulando", nunca testemunho falso).

### A5. "Faltei/zerei: abstenção do dia 1 vs dia 2" — A CALCULAR · esforço baixo
- **Dado**: `TP_PRESENCA_*` (0 faltou, 2 eliminado). Dia 1 = CH+LC; Dia 2 = CN+MT. Mostrar quanta gente some no 2º dia.
- **Cuidado**: medido sobre a base de Resultados (não sobre inscritos do questionário).

---

## TRILHA B — Informação para professores (pedagógico, acionável)

### B1. "Habilidades (H1–H30) mais difíceis por área" — JÁ PRONTO · esforço baixo (republicar/atualizar)
- **Assets prontos**: `analises_primi_2025_cop30/outputs/habilidades_dificuldade_2025.csv` (% acerto + B + A + descrição por habilidade, 119 linhas, 4 áreas), `auditoria_dificuldade_habilidades_2025.json`, `post_ig_habilidades_dificeis_2025.png` + `legenda_post_habilidades_2025.md`, `dashboard_habilidades_dificeis_2025.html`.
- **Ação**: revisar a arte no padrão atual (sem fundo preto, marca) e publicar; é o conteúdo-professor mais direto.

### B2. "Mapa de distratores: a alternativa errada que mais engana" — A CALCULAR · esforço médio-alto · TEACHER GOLD / ALTA NOVIDADE
- **Gancho**: por questão, qual alternativa ERRADA atrai mais — revela a concepção equivocada (o "porquê do erro").
- **Dado**: distribuição de `TX_RESPOSTAS_*` por posição vs `TX_GABARITO_*`; achar o distrator dominante por item e cruzar com `CO_HABILIDADE`. Tema da questão por visão (como no carrossel de chutáveis).
- **Formato**: carrossel por área "a pegadinha mais eficaz" + tabela para professor.

### B3. "Sequência da prova por dificuldade" — JÁ PRONTO · esforço baixo
- **Assets**: `dificuldade_sequencia_por_caderno/*.png` (grade P01–P45 com habilidade + DIF por questão) e `itens_sequencia_dificuldade_2025.csv`. Útil para professor planejar ordem de resolução.

### B4. "Formação de professor sobre TRI" (CCI, informação, paradoxo) — JÁ PRONTO · esforço baixo
- **Assets**: `analise_psicometria_2025/` (01_CCI, 02_informacao_teste, 03_modelo_vs_observado, 04_paradoxo) + LEIA-ME. Vira um mini-guia/carrossel didático para docentes.

### B5. "Onde a prova mede melhor (foco por área)" — PRONTO (figura) + legenda feita · esforço baixo
- `02_informacao_teste.png` + legenda da metáfora da câmera já redigida. Recado para professor: em que faixa cada prova diferencia melhor o aluno.

---

## Primeira leva (decidido com o usuário)
- **Produzir primeiro: A3 — "A prova cansa: branco por questão"** (dor do aluno, novo, original). É o único tema da 1ª leva.
- **Trilha professores = "os dois" focos** ao longo da série: diagnóstico do que caiu (B1 habilidades, B2 distratores, B3 sequência) **+** formação em TRI (B4 CCI/informação/paradoxo, B5 foco por área). Não priorizar um sobre o outro; alternar.

### Detalhe de execução de A3 (1ª leva)
- Varrer `RESULTADOS_2025.csv` (2,1 GB, streaming): para cada `TX_RESPOSTAS_{CN,CH,LC,MT}`, contar `.` (em branco) por posição 1→45. Em LC, ignorar `9` (item da língua não escolhida) antes de calcular a taxa de branco.
- Gerar 2 curvas: (a) % em branco por posição dentro de cada área; (b) visão "fim da prova" — comparar branco nas últimas 5 questões vs primeiras 5. Opcional: separar branco×erro×acerto por posição.
- Cuidado de leitura: posição = ordem do item no caderno; usar caderno Azul como referência de qual habilidade está em cada posição (via `ITENS_PROVA_2025.csv`, `CO_POSICAO`).
- Arte: gráfico de linha (fundo claro, marca X-TRI), gancho na voz do aluno ("não é só você que travou no fim"), recado anti-ansiedade, fonte INEP. Card feed 1080×1350 + possível story.

## Verificação (ao executar cada tema)
1. Rodar o cálculo em Python sobre o arquivo/coluna citado; conferir contagens contra totais conhecidos (presentes: CN/MT ~3,18 mi; CH/LC ~3,37 mi; 4,81 mi linhas).
2. Spot-check de 3–5 valores contra a fonte (ex.: um item no PDF da prova; um motivo de zero no dicionário).
3. Validar arte: sem fundo preto, marca X-TRI, fonte INEP no rodapé, terminologia "sexo feminino/masculino".
4. Nunca preencher nulo/estimar; itens anulados marcados, nunca chutados.

## Arquivos/insumos-chave
- Dados: `DADOS/RESULTADOS_2025.csv`, `DADOS/PARTICIPANTES_2025.csv`, `DADOS/ITENS_PROVA_2025.csv`.
- Prontos (professor): `analises_primi_2025_cop30/outputs/habilidades_dificuldade_2025.csv`, `.../post_ig_habilidades_dificeis_2025.png`, `.../dashboard_habilidades_dificeis_2025.html`, `.../dificuldade_sequencia_por_caderno/`, `analise_psicometria_2025/*`.
- Referência: `TRI_ITENS_AZUL_ENEM2025.xlsx`, `Matriz_Referencia_ENEM.pdf` / `outputs/matriz_full.txt` / `outputs/habilidades_desc.json` (descrições H1–H30).
