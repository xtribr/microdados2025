# Série AUTÓPSIA TRI — legendas dos 3 posts (anuladas pela TRI)

> Ordem sugerida de publicação: MT (1/3, a mais forte) → CN (2/3) → CH (3/3). Artes: `xtri_anulada_{MT,CN,CH}_{feed,story}.png`.

## 1/3 — MT (convergência) · legenda

Os melhores alunos do país marcaram D. O gabarito oficial dizia A. E a TRI anulou a questão.

Essa é a autópsia mais impressionante do ENEM 2025. Uma questão de Matemática foi anulada com o motivo oficial "problema de convergência" — registrado pelo INEP nos próprios microdados. Fui ver o que o modelo viu.

Construí a curva empírica de cada alternativa: em cada faixa de 50 pontos de nota, o % de alunos que marcou cada letra (3,18 milhões de respostas). O resultado:

— A marcação do gabarito oficial A CAI conforme a nota sobe: 15% entre os mais fracos, 8% entre os melhores. Isso é discriminação NEGATIVA: acertar o "gabarito" era mais comum entre quem sabia menos.

— Enquanto isso, a alternativa D dispara: 73% dos alunos de nota mais alta convergem nela.

Tecnicamente: no modelo de 3 parâmetros, a curva característica do item (ICC) tem que crescer com a proficiência — o parâmetro A precisa ser positivo. Quando o padrão real contradiz isso, o estimador de máxima verossimilhança não fecha: "problema de convergência". Sem A, B e C estáveis, o item não pode pontuar ninguém.

Não estou afirmando que o gabarito estava errado — estou mostrando o que 3 milhões de marcações mostram. A TRI viu o mesmo, e o item saiu da régua. Ninguém perdeu ponto: questão anulada não entra na conta de ninguém.

É para isso que existe a etapa estatística do ENEM. Ela funciona.

Fonte: Microdados ENEM 2025 / INEP, 1ª aplicação regular. Transformamos dados em aprovações.

#enem #enem2025 #tri #psicometria #matematica #microdados #vestibular

## 2/3 — CN (convergência) · legenda

Existe uma curva que o modelo do ENEM proíbe. E uma questão de Ciências da Natureza de 2025 desenhou exatamente ela.

Motivo oficial da anulação (microdados INEP): "problema de convergência". A autópsia mostra o porquê: a marcação do gabarito B faz um U pela escala de nota — 26% entre os mais fracos, cai para 18% no meio da régua (ABAIXO do chute puro, 20%), e explode para 69% só no topo.

Por que isso mata o item? A ICC do modelo de 3 parâmetros é monotônica por construção: a probabilidade de acerto só pode SUBIR com a proficiência (theta). O aluno médio não pode acertar menos que o aluno fraco. Quando os dados desenham um U, nenhuma combinação de A, B e C ajusta a curva — a calibração não converge.

Esse padrão costuma ser assinatura de item com dupla interpretação: uma leitura "ingênua" que leva o fraco ao gabarito por caminho errado, uma leitura intermediária que leva o mediano à distratora, e a leitura completa que só o topo faz.

A TRI não sabe o que a questão dizia — ela só viu que o comportamento era incompatível com uma medida honesta. Anulou. Ciências da Natureza valeu com 42 itens em 2025.

Fonte: Microdados ENEM 2025 / INEP, 1ª aplicação regular, 3,18 milhões de respostas ao item. Transformamos dados em aprovações.

#enem #enem2025 #tri #psicometria #ciencias #microdados #vestibular

## 3/3 — CH (Bis<0,01) · legenda

"Bis<0,01". Três caracteres nos microdados do INEP que condenaram uma questão de Ciências Humanas do ENEM 2025.

Tradução: a correlação bisserial do item — a relação entre acertar aquela questão e ir bem na prova — era menor que 0,01. Zero, na prática. Acertar essa questão não tinha NADA a ver com saber Ciências Humanas.

Essa anulada é diferente das outras: ela só apareceu na 2ª aplicação (a reaplicação de dezembro), feita por 309 pessoas. A autópsia por grupo de nota mostra o caos:

— Alunos de nota baixa: 25% marcaram o gabarito D.
— Alunos de nota média: 12%.
— Alunos de nota alta: 18% — e a preferida deles foi E, com 51%.

O gabarito não lidera em nenhum grupo. Os fracos o marcam MAIS que os fortes. Numa amostra pequena, um item assim não é só inútil — ele contamina a medida dos outros itens.

A bisserial é o filtro mais antigo da psicometria, anterior até à TRI: se acertar o item não correlaciona com a proficiência, o item não mede o que a prova mede. O INEP aplicou o filtro, o item morreu, e os 309 candidatos foram avaliados pelos 44 itens restantes.

Detalhe que quase ninguém sabe: as anuladas do ENEM não são todas iguais. Essa morreu de bisserial; duas morreram de convergência; três, por vazamento. Cada uma deixou uma assinatura diferente nos dados — e está tudo nos microdados, público, para quem quiser conferir.

Fonte: Microdados ENEM 2025 / INEP, 2ª aplicação, n = 309. Transformamos dados em aprovações.

#enem #enem2025 #tri #psicometria #cienciashumanas #microdados #vestibular

## Alt-texts (acessibilidade)

- MT: Gráfico de linhas mostrando o percentual de marcação de cada alternativa de uma questão de Matemática anulada no ENEM 2025, por faixa de nota. A linha do gabarito oficial A cai de 15% para 8% conforme a nota sobe, enquanto a alternativa D sobe até 73% entre os alunos de nota mais alta.
- CN: Gráfico de linhas de uma questão de Ciências da Natureza anulada no ENEM 2025. A linha do gabarito B forma um U: 26% entre alunos fracos, 18% no meio da escala e 69% no topo.
- CH: Barras com o percentual de marcação das alternativas A a E em três grupos de nota (baixa, média e alta) de uma questão de Ciências Humanas anulada na 2ª aplicação do ENEM 2025. O gabarito D não lidera em nenhum grupo; no grupo de nota alta, a alternativa E recebe 51%.
