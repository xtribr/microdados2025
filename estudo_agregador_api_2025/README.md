# Agregador TRI/Habilidade 2025 — camada de dados para gráficos e estudos

Dataset real, verificado, cruzando a **API pública** (`api.questoes.xtri.online/api/exams/2025/questions/`) com os **microdados oficiais** (`ITENS_PROVA_2025.csv`, INEP), para preencher os dois campos que a API ainda não tem em 2025: `skill` (habilidade) e `param_b` (dificuldade TRI).

## Por que existe

A API pública já tem os 182 registros de 2025 (texto, gabarito, imagem, índice), mas **100% deles** estavam com `skill: null` e `param_b: null` — confirmado varrendo as 4 páginas do endpoint. Esses dois campos eu já tinha, reais e auditados, desde os posts anteriores desta sessão (`ITENS_PROVA_2025.csv`). Este agregador é a camada que junta as duas coisas, uma vez, para não precisar refazer o cruzamento (offset de posição, caderno, idioma) toda vez que um gráfico ou post novo precisar desses dados de 2025.

## Metodologia (auditável)

1. **Caderno de referência:** AZUL, aplicação regular (P1) — `CO_PROVA` 1459 (LC) · 1447 (CH) · 1483 (CN) · 1471 (MT). Mesmos códigos já usados em todo o acervo XTRI (`estudo_distratores`, `estudo_polemicas_tri`, `testlet_escolas_compute.py`).
2. **Join:** `index` da API == `CO_POSICAO` do CSV (confirmado: é global 1-180, não precisa de aritmética extra — LC 1-45, CH 46-90, CN 91-135, MT 136-180). Para Linguagens posições 1-5 (com variante de idioma), `language` da API mapeado para `TP_LINGUA` do CSV (0=Inglês, 1=Espanhol, conforme Dicionário oficial dos microdados).
3. **Verificação:** o gabarito do CSV (`TX_GABARITO`) foi comparado ao `correctAlternative` da própria API para confirmar que o join está pegando o item certo. Resultado: **178 de 182 batem exatamente (97,8%)**.

## O que achei (inclui um bug real na sua API)

- **4 divergências, todas no mesmo padrão:** posições 1, 2, 4 e 5 de Linguagens, variante **espanhol**. A API mostra o mesmo `correctAlternative` da variante inglês nessas 4 posições — ou seja, a resposta certa do item em espanhol está errada/duplicada na sua API (bug pré-existente, não fui eu que causei). O `skill`/`param_b` que este agregador entrega pra essas 4 posições **são os reais do item em espanhol** (peguei pelo campo `language`, que está correto — só o `correctAlternative` da API está com o bug).
- **3 posições que existem no CSV mas não existem na API:** CN índice 123, CN 132, MT 174. Os três são itens **anulados por "Previamente exposto"** no CSV oficial — ou seja, sua API já está certa em não trazê-los, não é uma falha.
- **2 itens anulados que a API TEM:** CN 125 e MT 172, anulados por "Problema de convergência" (a TRI não convergiu, mas o item foi mantido no gabarito). Nesses dois, `skill` vem preenchido mas **`param_b` fica `null` de propósito** — é a regra do projeto (nunca preencher parâmetro de item anulado) e é assim que os microdados oficiais também tratam.
- **Resultado final:** 182/182 registros com `skill`; **180/182 com `param_b` real** (só os 2 anulados-por-convergência ficam sem, corretamente).

## Arquivos

- `agregador_tri_habilidade_2025.json` — dataset completo, com metadado de metodologia embutido.
- `agregador_tri_habilidade_2025.csv` — mesmo dataset, achatado (`;` como separador), com coluna `observacao` explicando os casos especiais linha a linha.
- `agregador_2025.py` — módulo Python pra importar direto (`from agregador_2025 import load, by_area, get`) em qualquer script novo.
- `build_aggregador.py` — script que gerou o dataset a partir do zero (reprodutível/auditável).
- `page1.json`…`page4.json` — cópia bruta das 4 páginas da API no momento da checagem (08/07/2026), pra rastreabilidade.

## Como isso chega na sua API de verdade

Eu não tenho como escrever direto na sua API — só fiz leitura (`GET`), sem autenticação, e por regra própria não insiro chave/token de API mesmo que você me passe um. O caminho pra popular `skill`/`param_b` de 2025 de fato é um destes:

1. Seu time de dev roda um import a partir do `agregador_tri_habilidade_2025.json`/`.csv` (o `id` de cada linha já é o mesmo `id` da sua API, é só bater PATCH/UPDATE por id).
2. Ou, se você tiver Django admin / management command, esse CSV já está no formato pra um `loaddata`/script de bulk update.

Enquanto isso não acontece, qualquer gráfico ou post que eu (ou você) fizer sobre 2025 pode importar direto de `agregador_2025.py` — não depende da API estar atualizada.

*Fonte: Microdados ENEM 2025 / INEP. Checagem feita em 08/07/2026.*
