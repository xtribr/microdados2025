# Newsletter LinkedIn — O ENEM inclui o aluno com necessidades especiais?

Capa: `capa_linkedin_inclusao.png` (1280×720)
Gráficos (nesta ordem): `g1_matricula_inclusao.png` · `g2_tipos_prova.png` · `g4_contraste.png` · `g3_indice_uf.png`

---

## Título
O ENEM inclui o aluno com necessidades especiais? O que os microdados oficiais mostram — e o que eles deixam de mostrar

## Subtítulo
Cruzei duas bases do INEP — o Censo Escolar 2025 e os Microdados do ENEM 2025 — escola por escola. A boa notícia começa na matrícula. O problema aparece na prova.

---

## Corpo

Uma pergunta simples abre um buraco incômodo nos dados públicos: o ENEM inclui o estudante com necessidades educacionais especiais? Para responder sem achismo, fui às duas bases oficiais do INEP e as cruzei escola por escola — o Censo Escolar da Educação Básica 2025 e os Microdados do ENEM 2025. Cada número aqui tem fonte, e eu digo qual.

### 1. Na matrícula, o Brasil inclui — e cumpre a lei

Começo pela boa notícia, que vem do Censo Escolar 2025. Há 294.089 matrículas de Educação Especial no Ensino Médio no país (variável `QT_MAT_ESP_MED`). Dessas, 292.201 estão em classe comum e apenas 1.888 em classe exclusiva — ou seja, 99,4% estudam junto com todos os demais.

Isso não é acaso: a Constituição (art. 208, III) e a Lei Brasileira de Inclusão (Lei 13.146/2015, art. 28) determinam a matrícula na rede regular, não em salas segregadas. Na matrícula, essa regra está sendo cumprida. Esse é o primeiro passo da inclusão — estar junto — e ele está sendo dado.

> [GRÁFICO 1 — g1_matricula_inclusao.png]

### 2. Mas na prova, eles quase somem

Agora o outro lado. Nos Microdados do ENEM 2025, apenas 22.500 candidatos fizeram prova adaptada — e esse é o único rastro que o dado deixa, porque o ENEM só registra quem precisou mudar o caderno físico (variável `CO_PROVA`): Atendimento Especializado (15.809), Ampliada (4.241), Libras (1.388), Superampliada (820) e Ledor (242).

Aqui está o ponto cego: o ENEM não registra o tipo de necessidade do aluno, nem o recurso solicitado, nem laudo. Quem tem TDA, TDAH ou dislexia e utiliza apenas tempo adicional faz o caderno comum — e desaparece do dado. Não há como saber quantos são.

> [GRÁFICO 2 — g2_tipos_prova.png]

### 3. Cuidado com a leitura: é ponto cego, não taxa de exclusão

É tentador colocar os dois números lado a lado e concluir "só 8% dos alunos com necessidades especiais chega ao ENEM". Isso seria um erro — e eu não faço isso. Os 294 mil são o estoque dos três anos do Ensino Médio; os 22,5 mil são o fluxo de um único exame. E, principalmente, muitíssimo aluno com necessidade especial presta a prova sem caderno adaptado — e, portanto, é invisível nesse recorte.

O contraste, então, não mede exclusão. Ele mede outra coisa, igualmente importante: o tamanho do ponto cego. O ENEM simplesmente não enxerga quem é esse estudante.

> [GRÁFICO 3 — g4_contraste.png]

### 4. Um dado regional que contraria o senso comum

Quando calculo um índice de participação visível — provas adaptadas no ENEM por 100 matrículas de Educação Especial no EM — aparece um padrão que costuma surpreender: lideram o Nordeste e o Norte (Sergipe, Paraíba, Pará à frente), enquanto o Sul fica no fim (Santa Catarina e Rio Grande do Sul com os menores índices). A média nacional é 7,7.

Reforço o cuidado metodológico: isto é índice de participação visível, não um ranking de qualidade da inclusão. A diferença pode refletir prática de solicitação de recursos, organização das redes ou forma de registro. O dado está aqui; a leitura fina é de quem lê.

> [GRÁFICO 4 — g3_indice_uf.png]

### 5. E as escolas? A inclusão visível é majoritariamente pública

Descendo à escola (cruzando `CO_ESCOLA` do ENEM com `CO_ENTIDADE` do Censo e conferindo a dependência administrativa nas duas bases), a escola que mais levou alunos NEE ao ENEM adaptado foi uma estadual comum do Ceará — a EEM Dom Terceiro, de Boa Viagem, com 19 candidatos. O padrão se repete: são escolas públicas regulares, não institutos especializados.

Nas privadas, o número é ainda menor. A primeira colocada é justamente um instituto especializado (Filippo Smaldone, Fortaleza/CE, com 11); entre as privadas comuns, o topo é 7. Ao todo, 1.592 escolas privadas tiveram ao menos um candidato adaptado — cerca de 1 em cada 5 dos 10,2 mil candidatos com escola identificada. A maior parte da inclusão visível no ENEM está na rede pública.

(Todas as contagens de escola foram reconferidas de forma independente, recontando do zero sobre os arquivos brutos das duas bases, antes de publicar.)

---

## Fechamento

Então, o ENEM inclui? No acesso, sim — existe prova em Braille, Libras, ampliada e com atendimento especializado, e a lei da matrícula em classe comum está sendo cumprida. Mas o exame é cego aos próprios dados: não registra quem tem necessidade especial e, por isso, não permite medir se inclui bem.

O primeiro passo da inclusão é ser contado. Enquanto o ENEM não conta esse estudante, ele o mantém invisível na própria prova — e o que não se mede, não se melhora.

Se você trabalha com educação, políticas públicas ou avaliação, fica o convite: o dado para tornar essa população visível já é coletado no Censo. Falta conectá-lo ao exame que decide o futuro de milhões.

Transformamos dados em aprovações.
— Prof. Alexandre Emerson (@xandaoxtri)

---

## Fontes e método
- Censo Escolar da Educação Básica 2025 / INEP-MEC — `Tabela_Matricula` (agregada por escola; `QT_MAT_ESP_MED`, `QT_MAT_ESP_CC_MED`, `QT_MAT_ESP_CE_MED`) e `Tabela_Escola` (`NO_ENTIDADE`, `TP_DEPENDENCIA`, `IN_ESPECIAL_EXCLUSIVA`).
- Microdados do ENEM 2025 / INEP-MEC — caderno adaptado via `CO_PROVA` (versões Ampliada/Superampliada/Ledor/Libras/Atendimento Especializado).
- Cruzamento — `CO_ESCOLA` (ENEM) = `CO_ENTIDADE` (Censo); dependência conferida nas duas bases; contagens verificadas de forma independente.
- Ressalva — o contraste 294 mil × 22,5 mil é gap de visibilidade (mistura estoque×fluxo e subconta NEE em caderno regular), não taxa de exclusão. Índice por UF: NEE-EM por UF da escola (Censo) × prova adaptada por UF de prova (ENEM).
- Base legal citada — Constituição Federal, art. 208, III; Lei 13.146/2015 (LBI), art. 28.
- Todos os dados são públicos e agregados, sem identificação de aluno.
