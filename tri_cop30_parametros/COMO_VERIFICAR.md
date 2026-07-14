# Os parâmetros TRI da COP30/BAM são públicos — como verificar

**Resumo em uma frase:** os 3 parâmetros (a, b, c) de todos os itens da prova
aplicada na COP30 (Belém, Ananindeua e Marituba — "BAM2" no Dicionário do INEP)
estão publicados nos próprios Microdados ENEM 2025, no arquivo
`ITENS_PROVA_2025.csv`, sob os **códigos de prova 1499–1538** — uma numeração
diferente da usada no `RESULTADOS_2025.csv` (1583–1634). Quem procurou pelos
códigos 1583+ encontrou zero linhas e concluiu que os parâmetros não existiam.
Eles existem; só mudou o número.

## Por que ninguém achou

| Arquivo | Como a prova COP30 aparece | Rótulo no Dicionário |
|---|---|---|
| `RESULTADOS_2025.csv` (candidato) | CO_PROVA **1583–1634** | "Azul - BAM2", "Amarela - BAM2"… |
| `ITENS_PROVA_2025.csv` (item/parâmetros) | CO_PROVA **1499–1538** | (o Dicionário não rotula códigos nesta aba) |

O caminho natural — pegar o código do candidato e procurar no ITENS_PROVA —
dá vazio. O INEP publicou os cadernos, mas com numeração desencontrada entre
os dois arquivos e sem tabela de correspondência.

## As três provas do microdado (zero itens em comum entre elas)

| Família | Códigos ITENS_PROVA | Itens únicos | Parâmetros |
|---|---|---|---|
| Regular P1 | 1447–1498 | 185 | completos (exceto anulados: 2 MT, 3 CN) |
| **COP30/BAM** | **1499–1538** | **185 (+1)** | **completos (100%, zero anulados)** |
| Reaplicação | 1539–1582 | 185+ | completos (exceto 1 item CH) |

O "+1" da COP30: o item **111728** (MT, posição 177) existe **só nos cadernos
adaptados** (Laranja ampliada/Braille e Leitor de Tela) — substitui o item da
mesma posição dos cadernos comuns e tem parâmetros próprios (A=2,304 ·
B=1,698 · C=0,158). Prática padrão do INEP para item não adaptável.

Interseção de `CO_ITEM`: COP30×Regular = **0** · COP30×Reaplicação = **0**.
Ou seja: não é a prova regular renumerada nem a reaplicação — é a prova própria
da COP30, com calibração própria.

## A prova da equivalência (por que 1502 = o caderno Azul de MT da COP30)

O `RESULTADOS_2025.csv` grava, para cada candidato, o **gabarito oficial** da
prova que ele fez (`TX_GABARITO_MT` etc.). Então dá para conferir sem confiar
em ninguém:

1. Pegue qualquer candidato com `CO_PROVA_MT = 1607` (MT Azul-BAM2 — todos
   fizeram prova em Belém/Ananindeua/Marituba). O `TX_GABARITO_MT` dele começa
   com: `EDAAACCBBDBDDDA…`
2. No `ITENS_PROVA_2025.csv`, filtre `CO_PROVA = 1502`, ordene por
   `CO_POSICAO` e leia a coluna `TX_GABARITO`: `EDAAACCBBDBDDDA…` — **idêntico,
   nas 45 posições**.
3. Compare com o MT Azul regular (`CO_PROVA = 1471`): `CBECECCADDBECBD…` —
   completamente diferente. Não há como confundir as provas.

Fizemos essa checagem para **todos os ~66 mil candidatos BAM2, nas 4 áreas,
nos 16 cadernos principais: zero divergências**. O script
`verificar_tri_cop30.R` roda essa validação inteira em poucos minutos e
imprime a tabela `confere = TRUE` caderno a caderno (16/16).

**Pegadinha na correspondência de CN:** a ordem NÃO é crescente —
1621 (Verde) → **1514** e 1622 (Cinza) → **1513**. Quem parear os códigos
"na sequência" erra exatamente esses dois cadernos; a validação por gabarito
pega o erro na hora (foi assim que pegamos o nosso).

## A prova externa (fora dos microdados) — a mais forte de todas

O INEP divulgou publicamente os **PDFs de prova e gabarito da aplicação
P1-BAM** (arquivos `ENEM_2025_P1-BAM_GAB_*.pdf`). Esses PDFs são a definição
oficial do que foi a prova da COP30 — e não dependem dos microdados.
Comparação feita em 12/jul/2026, caderno Azul:

| Área | Gabarito no PDF oficial P1-BAM | Caderno no ITENS_PROVA | Confere |
|---|---|---|---|
| LC inglês 1-5 | `BEBBE` | 1529 (TP_LINGUA=0) | ✔ |
| LC espanhol 1-5 | `BAEEE` | 1529 (TP_LINGUA=1) | ✔ |
| LC comuns 6-45 | `EDBBDADECABEABCDADEBAAEBADDDBABECCCABBAB` | 1529 | ✔ |
| CH 46-90 | `DBECBDEBECEDABEADDBCDCDECBBACCBDEAECEEADADBEB` | 1520 | ✔ |
| CN 91-135 | `DCABCDCCDBCBCCBCBCEDAEDBCDECDCBABCDDBCECEBBED` | 1511 | ✔ |
| MT 136-180 | `EDAAACCBBDBDDDAEABBEDDBCCAABDDACBEBEEDBCECDDA` | 1502 | ✔ |

**185 posições idênticas, incluindo as duas línguas.** Qualquer professor com
o PDF do gabarito de Belém confere isso em 5 minutos, sem abrir o RESULTADOS:
filtra o ITENS_PROVA no código, ordena por posição e compara letra a letra.

## Como mostrar a comunidade (roteiro)

1. **Mande a planilha** `TRI_COP30_BAM_ENEM2025.xlsx` (aba "LEIA-ME" explica
   tudo; abas MT/CN/CH/LC têm os cadernos; "Itens únicos" tem os 185 itens com
   a/b/c + % de acerto observado na coorte COP30).
2. **Mande o script** `verificar_tri_cop30.R` e peça para ele rodar nos
   microdados que ELE baixar do INEP (gov.br/inep). A prova não depende de
   nada nosso — só dos dois CSVs públicos. Ajustar `PASTA_DADOS` e rodar.
3. **Se ele não usa R:** o passo manual acima (itens 1–3) pode ser feito com
   qualquer ferramenta que abra CSV grande (o ITENS_PROVA tem só 6.106 linhas
   e abre até no Excel; para o RESULTADOS, basta UM candidato de Belém, e o
   gabarito `EDAAACCBBDBDDDA…` está citado aqui para conferência).

## Cuidados ao divulgar

- **Não** chamar de "parâmetros da regular": as provas são disjuntas (item 0
  em comum). O erro clássico é rotular parâmetros da P1 regular como "COP30".
- Os parâmetros são **oficiais do INEP, publicados** — nós não estimamos nada;
  o achado é a **correspondência de códigos**, validada pelo gabarito.
- Citar a fonte: *Microdados ENEM 2025 / INEP*. O `TP_LINGUA` em LC:
  0 = Inglês, 1 = Espanhol, vazio = tronco comum.

---
*Compilação e validação: Prof. Alexandre Emerson (XTRI) · 12/jul/2026 ·
dados públicos do INEP · nenhum valor estimado.*
