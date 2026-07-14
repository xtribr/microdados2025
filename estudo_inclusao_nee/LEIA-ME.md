# Estudo: O ENEM inclui o aluno com necessidades especiais (NEE)?

Cruza **Censo Escolar 2025** (matrícula de Educação Especial no Ensino Médio) com **ENEM 2025**
(quem fez prova adaptada), para entender se — e como — o estudante com necessidades especiais chega à prova.

## Pergunta
O ENEM realmente inclui o aluno com necessidades educacionais especiais, ou a inclusão "some"
na hora da prova? A escola que tem 19 alunos adaptados numa aplicação e a que tem 1 — o que dizem?

## Fontes (100% dado real INEP, agregado — sem PII)
- **Censo Escolar 2025** — `Tabela_Matricula` é **agregada por escola** (`QT_MAT_*`, uma linha por
  `CO_ENTIDADE`), não tem aluno individual. Usadas: `QT_MAT_MED` (total EM), `QT_MAT_ESP_MED`
  (Ed. Especial no EM), `QT_MAT_ESP_CC_MED` (em classe comum = inclusão), `QT_MAT_ESP_CE_MED`
  (classe exclusiva). `Tabela_Escola` para nome/UF/dependência/`IN_ESPECIAL_EXCLUSIVA`.
- **ENEM 2025** — `RESULTADOS_2025.csv`; "caderno adaptado" = `CO_PROVA` ∈ {Ampliada, Superampliada,
  Ledor, Libras, Atendimento Especializado}. `CO_ESCOLA` (ENEM) = `CO_ENTIDADE` (Censo) → mesmo
  código INEP, permite o cruzamento escola a escola (agregado).

## Achados
### 1) O funil / a invisibilidade
- **294.089 matrículas de Educação Especial no Ensino Médio** no Brasil.
- **99,4% em classes comuns** (só 0,6% em classes exclusivas/segregadas) → pela definição oficial,
  a inclusão *na matrícula* é altíssima. O Brasil escolheu incluir, não segregar.
- No ENEM 2025, só **22.500 fizeram prova adaptada** — e o dado só "enxerga" quem precisou **mudar
  o caderno físico**. A **condição nunca é registrada**: TEA, TDAH e dislexia (que costumam usar só
  tempo adicional) são **invisíveis**. Por tipo: Atendimento Especializado 15.809 · Ampliada 4.241 ·
  Libras 1.388 · Superampliada 820 · Ledor 242.
- **A tese honesta:** não dá para afirmar se o ENEM "inclui bem" — porque ele **não registra quem é**
  o aluno NEE. Vê-se só a ponta visível (caderno adaptado).

### 2) O mapa por UF (índice: adaptados no ENEM por 100 matrículas NEE no EM)
- Lideram **Sergipe (17,1), DF (14,3), Paraíba (12,6), Pará (12,6), Amapá (11,9)** — padrão
  Norte/Nordeste + DF. **Ceará NÃO lidera por taxa** (é grande em número absoluto, não em proporção).
- Quase toda UF tem 98–100% da Ed. Especial do EM em classe comum.
- ⚠️ Índice ilustrativo: NEE-EM (Censo) é por UF da **escola**; adaptado (ENEM) é por UF de **prova**.

### 3) As escolas concentradoras (a de "19" vs a de "1")
- As escolas que mais levam NEE ao ENEM adaptado são, em sua maioria, **escolas públicas comuns**
  (não especializadas), concentradas no **Ceará** (EEM Dom Terceiro/Boa Viagem = 19; Granja; Fortaleza;
  Eusébio…), todas `exclusiva=False` → inclusão acontecendo na escola regular.
- Contraponto: **EMEBS Helen Keller (São Paulo, municipal)** aparece com 14 e é `exclusiva=True` —
  escola **especializada**. Mostra os dois modelos convivendo.
- 71% das ~6.856 escolas com ≥1 aluno adaptado têm **exatamente 1** — inclusão pulverizada; ranking
  de "melhor escola inclusora" por essa via seria ruído (e dado sensível).

### 4) Escolas PRIVADAS (`compute_privadas.py`, verificação dupla)
- Dependência administrativa conferida nos **dois** bancos (ENEM `TP_DEPENDENCIA_ADM_ESC==4` E
  Censo `TP_DEPENDENCIA==4`); divergências descartadas. **1.592 privadas** tiveram ≥1 candidato
  adaptado, **2.204 candidatos** no total (~1 em cada 5 dos 10,2 mil com escola identificada).
- Top privada: **Filippo Smaldone (Fortaleza/CE), 11 — instituto ESPECIALIZADO** (`exclusiva=1`).
  Entre as privadas **comuns** o topo é 7 (Colégio Sophos/Belém, Colégio Gabarito/Uberlândia).
  A inclusão visível no ENEM é, na maioria, **pública**.

### Verificação independente (contra questionamentos)
Todas as contagens das 10 escolas de destaque (6 privadas + 4 públicas) foram **reconferidas por
um workflow adversarial** que recontou do zero sobre os arquivos brutos (ENEM 4,8 mi linhas em
streaming; Censo linha a linha). Bateu 100%: adaptados, dependência, `QT_MAT_ESP_MED` e
`IN_ESPECIAL_EXCLUSIVA` idênticos ao `compute_*`. Filippo Smaldone e Helen Keller confirmadas como
educação especial exclusiva.

## Ressalvas de integridade (mantidas em toda arte)
- "22,5k de 294k" mistura estoque (3 anos de EM) com fluxo (quem prestou) e **subconta** (NEE que fez
  caderno regular é invisível) → é o **gap de visibilidade**, não taxa de transição exata.
- Caderno adaptado ≠ condição. Nunca inferir TEA/TDAH a partir dele.
- Dado sensível: sempre agregado; nunca expor aluno individual.

## Arquivos
- `compute_inclusao.py` — cruzamento Censo × ENEM (agregado, sem PII): funil, UF, top escolas públicas.
- `compute_privadas.py` — escolas privadas com verificação dupla de dependência.
- `dados_inclusao.json`, `dados_privadas.json` — saídas.
- `carrossel/` — carrossel IG (feed, **8 cards**): capa com fontes oficiais · matrícula+legislação ·
  ENEM invisibiliza · funil · mapa UF · escolas públicas · escolas privadas · fechamento.
  `TEXTO_legenda.md` cita fonte e amparo o tempo todo (+ alt-text e "Fontes e método").

*Fontes: Microdados Censo Escolar 2025 e ENEM 2025 / INEP.*
