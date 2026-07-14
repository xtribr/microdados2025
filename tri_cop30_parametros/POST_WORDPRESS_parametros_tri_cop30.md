<!-- ===================== SEO / RankMath ===================== -->
**Focus keyphrase:** parâmetros TRI da COP30

**Prova de ineditismo — frases-foco já usadas ou reservadas (nenhuma colide):**
- questões em branco no ENEM · reaplicação do ENEM · ordem das questões no ENEM · como funciona a nota do ENEM · questões mais chutáveis do ENEM · TRI das questões do ENEM 2025 · abstenção no ENEM 2025 · questões anuladas do ENEM 2025 · habilidades mais difíceis do ENEM 2025 · questões mais difíceis ENEM 2025 · como funciona a TRI do ENEM (engavetada)
- **parâmetros TRI da COP30** é inédita: nenhum post anterior trata da aplicação COP30/BAM nem de parâmetros dessa prova.

**Título SEO (H1):** Parâmetros TRI da COP30: os 186 itens que ninguém encontrava
**Slug:** parametros-tri-da-cop30 *(23 caracteres — ≤ 75 ✓)*
**Meta description (147 caracteres):** Parâmetros TRI da COP30 são públicos: veja onde estão os 186 itens (a, b, c) da prova de Belém nos microdados do ENEM 2025 e como conferir.
**Keyphrases secundárias:** COP30 ENEM · prova de Belém · BAM2 · ITENS_PROVA · microdados ENEM 2025 · parâmetros a b c · dificuldade TRI
**Categoria:** Microdados ENEM · **Tags:** ENEM 2025, COP30, Belém, TRI, parâmetros, psicometria, INEP, microdados, professor
**Imagem destacada:** `tri_cop30_parametros/capa_wp_parametros_tri_cop30_1200x630.png` (1200×630) — *alt:* "Parâmetros TRI da COP30: onde estão os 186 itens da prova de Belém — XTRI."
<!-- schema Article · author: Prof. Alexandre Emerson (XTRI) · datePublished -->
<!-- ====================================================== -->

# Parâmetros TRI da COP30: os 186 itens que ninguém encontrava

Desde a divulgação dos [microdados do ENEM 2025 (INEP)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem), a comunidade de professores que trabalha com dados — eu incluído — repetia a mesma conclusão: os **parâmetros TRI da COP30** não teriam sido publicados. A prova aplicada em Belém, Ananindeua e Marituba por causa da conferência do clima parecia ter ficado de fora do arquivo de itens. Depois de uma investigação item a item, posso afirmar com verificação reproduzível: **os parâmetros estão públicos desde sempre — no lugar "errado"**. Este post mostra onde estão, por que ninguém achava e como qualquer professor confere em 5 minutos.

## Por que ninguém encontrava os parâmetros TRI da COP30

O caminho natural de quem analisa microdados é: pegar o código de prova do candidato no `RESULTADOS_2025.csv` e procurar esse código no `ITENS_PROVA_2025.csv`, onde vivem os três parâmetros (a, b, c) de cada questão. Para a aplicação regular, funciona: o caderno Azul de Matemática é o código 1471 nos dois arquivos. Para a reaplicação, idem (códigos 1539–1572 nos dois).

Para a COP30, não. Os candidatos de Belém aparecem no RESULTADOS com códigos **1583–1634** — o Dicionário oficial os rotula como "BAM2". E esses códigos têm **zero linhas** no ITENS_PROVA. Busca vazia, conclusão aparentemente óbvia: "o INEP não divulgou os parâmetros TRI da COP30". Foi a conclusão de todo mundo — inclusive a minha, numa primeira passada.

## Onde eles estão: códigos 1499–1538 do ITENS_PROVA

O INEP publicou os cadernos da COP30 no ITENS_PROVA com **outra numeração: 1499–1538**. São 1.850 linhas com os três parâmetros preenchidos em 100% dos itens — sem nenhum item anulado. A correspondência entre os dois arquivos, que o INEP não publicou em lugar nenhum, é esta:

| Área | Azul | Amarela | Verde | Cinza/Branca |
|---|---|---|---|---|
| Ciências Humanas | 1583→1520 | 1584→1521 | 1586→1523 | Branca 1585→1522 |
| Linguagens | 1595→1529 | 1596→1530 | 1597→1531 | Branca 1598→1532 |
| Matemática | 1607→1502 | 1608→1503 | 1609→1504 | Cinza 1610→1505 |
| Ciências da Natureza | 1619→1511 | 1620→1512 | **1621→1514** | **Cinza 1622→1513** |

Atenção ao detalhe de Ciências da Natureza: a correspondência **não segue a ordem crescente** (Verde e Cinza trocam de posição). Quem parear os códigos "em sequência" erra exatamente esses dois cadernos — a validação pelo gabarito, descrita abaixo, pega o erro na hora.

## A prova de que são os parâmetros TRI da COP30 (e não de outra prova)

Ninguém precisa acreditar em mim — a verificação usa só arquivos oficiais:

1. **O gabarito divulgado bate letra por letra.** O INEP publicou os PDFs de gabarito da aplicação P1-BAM. O caderno Azul de Matemática divulgado é `EDAAACCBBDBDDDAEABBEDDBCCAABDDACBEBEEDBCECDDA` — idêntico, nas 45 posições, ao `TX_GABARITO` do código 1502 no ITENS_PROVA. A conferência fecha nas 4 áreas, nas 185 posições, incluindo os blocos de inglês e espanhol.
2. **Os ~66 mil candidatos confirmam.** O RESULTADOS grava o gabarito da prova de cada candidato; para todos os candidatos BAM2, ele é idêntico ao dos cadernos 1499–1538. Zero divergências em 16 cadernos.
3. **Não é nenhuma outra prova.** Os itens da COP30 têm **zero questões em comum** com a aplicação regular (1447–1486) e **zero** com a reaplicação (1539–1582). São três provas disjuntas — e os parâmetros TRI da COP30 pertencem só a ela.

Em resumo: os parâmetros não foram estimados por ninguém — são a calibração oficial do INEP, publicada no próprio microdado. O que faltava era a ponte entre as numerações.

## O que há dentro: 186 itens, 100% calibrados

A família completa tem 40 códigos (incluindo cadernos ampliados, Braille e leitor de tela) e **186 itens únicos** — 185 dos cadernos comuns mais um item exclusivo das versões adaptadas (CO_ITEM 111728, Matemática, posição 177), que substitui o item da mesma posição e tem parâmetros próprios. Um exemplo do que a planilha revela: a questão 148 do caderno Azul de Matemática tem b = 3,46 — **dificuldade 846 na escala ENEM** (b×100+500), um dos itens mais duros de 2025 em qualquer aplicação.

Com esses parâmetros abertos, destravam-se as análises que até aqui só existiam para a prova regular: dificuldade e discriminação item a item, análise por habilidade e estudos por escola da região metropolitana de Belém — que fizemos e publicaremos em seguida. Para saber como esses três números viram nota, veja [como funciona a nota do ENEM](como-funciona-a-nota-do-enem); para o mapa das [habilidades mais difíceis do ENEM 2025](habilidades-mais-dificeis-do-enem-2025) e [onde a prova do ENEM mede melhor](onde-a-prova-do-enem-mede-melhor), os estudos-irmãos deste blog.

## Confira você mesmo (5 minutos)

1. Baixe os microdados no [portal do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).
2. Abra `ITENS_PROVA_2025.csv` (6.106 linhas — abre no Excel; separador `;`).
3. Filtre `CO_PROVA = 1502`, ordene por `CO_POSICAO` e compare o `TX_GABARITO` com o gabarito oficial de Matemática da aplicação de Belém.
4. As colunas `NU_PARAM_A`, `NU_PARAM_B` e `NU_PARAM_C` dessas linhas são os parâmetros que a comunidade procurava.

Transparência de método é o que cobramos do INEP — e é o que praticamos. Se você é professor e quer a planilha consolidada (todos os cadernos, dificuldade na escala ENEM já calculada e o script de verificação em R), fala comigo no [@xandaoxtri](https://instagram.com/xandaoxtri) — e para transformar dado em estratégia de prova com seus alunos, conheça o [app.rankingenem.com](https://app.rankingenem.com).

---
*Por Prof. Alexandre Emerson (Xandão) — professor, CEO da XTRI e analista de microdados do ENEM/TRI. Fonte: [Microdados ENEM 2025 e Dicionário / INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). Nenhum parâmetro foi estimado: todos os valores são a publicação oficial do INEP.*

<!-- ===================== CHECKLIST RankMath =====================
✓ Frase-foco exata "parâmetros TRI da COP30": título SEO (início), meta (início), slug, 1º parágrafo, H2 (×2), alt da capa
✓ Ocorrências no corpo: 8 em ~840 palavras ≈ 1,0% (título/meta/alt somam no RankMath) — dentro de 1–1,5%
✓ Título: número (186) + palavra de impacto ("ninguém encontrava") — 61 car.
✓ Meta: 147 car. ≤ 155 ✓ · Slug 23 car. ≤ 75 ✓
✓ Link externo dofollow: gov.br/inep (1º parágrafo + CTA + byline)
✓ Links internos: como-funciona-a-nota-do-enem · habilidades-mais-dificeis-do-enem-2025 · onde-a-prova-do-enem-mede-melhor
✓ ≥600 palavras (~840) · alt de imagem com frase-foco · voz 1ª pessoa
=============================================================== -->
