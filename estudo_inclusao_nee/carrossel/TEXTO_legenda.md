# Carrossel — O ENEM inclui o aluno com necessidades especiais?

8 cards · feed 1080×1350 · Fontes: Microdados do Censo Escolar 2025 e do ENEM 2025 — INEP/MEC

## Legenda (feed) — 1.310 caracteres (limite IG: 2.200)

O ENEM inclui o aluno com necessidades especiais? Cruzei duas bases oficiais do INEP: o Censo Escolar 2025 e os Microdados do ENEM 2025.

Na matrícula, o Brasil inclui: são 294.089 estudantes da Educação Especial no Ensino Médio (Censo), e 99,4% estão em classe comum — como manda a Lei Brasileira de Inclusão. Junto com todo mundo.

Mas na prova eles quase somem. No ENEM 2025, só 22.500 fizeram prova adaptada — e o dado só "vê" quem mudou o caderno (Libras, ampliada, ledor, atendimento especializado). Quem tem TDA, TDAH ou dislexia e usa só tempo adicional faz o caderno comum e não deixa rastro. O ENEM não registra a necessidade do aluno.

Atenção: isso NÃO é "só 8% chega ao ENEM". Os 294 mil são o estoque dos 3 anos do EM, e muita gente faz a prova sem caderno adaptado. O número mostra o tamanho do ponto cego, não uma taxa de exclusão.

Dois recortes que checei escola por escola: a inclusão visível é majoritariamente da rede pública (as que mais levam NEE ao ENEM são escolas estaduais comuns do Ceará); nas privadas o número é ainda menor.

Então, o ENEM inclui? No acesso, sim. Mas é cego aos próprios dados — não conta quem tem necessidade especial, então não dá pra medir se inclui bem. O primeiro passo da inclusão é ser contado.

Fontes: Microdados do Censo Escolar 2025 e do ENEM 2025 — INEP/MEC. Dados agregados, sem identificação de aluno.

#enem #enem2025 #educacaoespecial #inclusao #censoescolar #TDAH #acessibilidade #microdados

---

## Comentário fixado (método e fontes — fora do limite da legenda)

Metodologia, para quem quiser conferir: Censo Escolar 2025 → matrículas de Educação Especial no EM = variável QT_MAT_ESP_MED (classe comum QT_MAT_ESP_CC_MED 292.201 + exclusiva 1.888 = 294.089). ENEM 2025 → caderno adaptado = CO_PROVA nas versões especiais (Atend. Especializado 15.809 · Ampliada 4.241 · Libras 1.388 · Superampliada 820 · Ledor 242). Cruzamento CO_ESCOLA (ENEM) = CO_ENTIDADE (Censo), dependência conferida nas duas bases. Base legal: Constituição art. 208, III e Lei 13.146/2015 (LBI), art. 28. Índice por UF: SE 17,15 · PB 12,62 · PA 12,6 · SC 3,6 · RS 4,2 · média BR 7,7.

## Texto alternativo (acessibilidade)

Carrossel de 8 cards cruzando o Censo Escolar 2025 e o ENEM 2025 (INEP/MEC). Card 1: fontes oficiais; 294 mil estudantes da Educação Especial no Ensino Médio e 22,5 mil com prova adaptada no ENEM. Card 2: 99,4% das matrículas de Educação Especial do EM estão em classe comum, como determinam a Constituição e a Lei 13.146/2015. Card 3: tipos de prova adaptada no ENEM — Atendimento Especializado 15.809, Ampliada 4.241, Libras 1.388, Superampliada 820, Ledor 242; o ENEM não registra a necessidade do aluno. Card 4: funil de 294.089 matriculados para 22.500 visíveis, com aviso de que não é taxa de exclusão. Card 5: índice de provas adaptadas por 100 matrículas NEE por estado, liderado por Sergipe (17,15). Card 6: escolas públicas que mais levaram NEE ao ENEM, todas comuns do Ceará, com EEM Dom Terceiro em primeiro (19). Card 7: escolas privadas, lideradas pelo instituto especializado Filippo Smaldone (11); a inclusão visível é majoritariamente pública. Card 8: conclusão — o ENEM inclui no acesso, mas é cego aos dados.

## Fontes e método (para responder a questionamentos)
- Censo Escolar 2025 (INEP) — `Tabela_Matricula` é agregada por escola (uma linha por `CO_ENTIDADE`, variáveis `QT_MAT_*`), sem aluno individual. NEE no EM = `QT_MAT_ESP_MED`; classe comum = `QT_MAT_ESP_CC_MED`; classe exclusiva = `QT_MAT_ESP_CE_MED`. Atributos de escola (nome, UF, dependência, `IN_ESPECIAL_EXCLUSIVA`) em `Tabela_Escola`.
- ENEM 2025 (INEP) — caderno adaptado = `CO_PROVA` nas versões Ampliada/Superampliada/Ledor/Libras/Atendimento Especializado. Capta só quem mudou o caderno físico; a condição nunca é registrada.
- Cruzamento — `CO_ESCOLA` (ENEM) = `CO_ENTIDADE` (Censo). Dependência administrativa conferida nas DUAS bases; divergências descartadas. Contagens reconferidas por verificação independente sobre os arquivos brutos.
- Ressalva — o funil mistura estoque (3 anos de EM) com fluxo (quem prestou) e subconta NEE em caderno regular → é gap de visibilidade, não taxa de transição/exclusão. O índice por UF usa NEE-EM por UF da escola (Censo) × adaptado por UF de prova (ENEM).
- Base legal citada: Constituição Federal, art. 208, III; Lei 13.146/2015 (LBI), art. 28.
