# Estudo — Série histórica das mínimas e máximas da nota TRI (ENEM 2015–2025)

Gráfico das **mínimas e máximas de cada edição do ENEM, por área**, na última década.
Mostra o **piso e o teto da escala TRI efetivamente alcançados** em cada prova.

## Pergunta
Qual a menor e a maior nota TRI possível de fato em cada prova, e como isso variou de 2015 a 2025?

## Fontes (100% dado real — nada estimado, ver [[no-fake-data-enem-microdados]])
- **2015–2023**: arquivo do usuário `TRI ENEM DE 2009 A 2023 MIN MED E MAX.xlsx` (Área de Trabalho),
  aba `resumo2009_2022 (2)` — colunas `area, acertos, min, max, media, ano` (min/máx da nota TRI por
  número de acertos). A mín/máx geral por área/ano = `min(min)` e `max(max)` sobre todos os acertos.
  Esse arquivo foi compilado pela XTRI a partir dos microdados oficiais INEP. (Cobre também 2009.)
- **2024**: microdados INEP locais (`/Volumes/HD/apps/RANKING ENEM/microdados-2024/MICRODADOS_ENEM_2024.csv`),
  varridos por `minmax_year.py` → `minmax_2024.json`.
- **2025**: `DADOS/RESULTADOS_2025.csv` (este projeto) → `minmax_2025.json`.

> O crawl direto do INEP (`crawl_inep.sh`) foi abandonado: o portal limita este ambiente a ~80 KB/s
> (ETA ~1 dia para 10 anos). Os dados vieram dos arquivos que o usuário já tinha — mais rápido e idêntico.

## Método
`minmax_year.py`: streaming latin-1 `;`, acha `NU_NOTA_{CN,CH,LC,MT,REDACAO}` pelo nome; calcula
**min (entre quem fez, nota > 0)** e **max** por área. A nota 0/branco é ausência, não desempenho.
`chart_serie_historica.py`: monta a série e plota 4 painéis (uma área cada) com a faixa min–max por ano,
2025 destacado.

## Achados (reais)
| Área | Teto típico | Maior teto da década | Menor teto | Amplitude do teto |
|---|---|---|---|---|
| **Matemática** | ~960–1000 | **1008 (2015)** | 953 (2021) | **55 pts** |
| Ciências da Natureza | ~855–885 | 886 (2017) | 855 (2020) | 31 pts |
| Ciências Humanas | ~820–870 | 868 (2017/2023) | 820 (2024) | ~49 pts |
| **Linguagens** | ~788–826 | 826 (2015/2021) | 788 (2023) | 38 pts |

- **Matemática é a única área que encosta em 1000** (1008 em 2015) e tem o teto mais alto e volátil.
- **Linguagens tem o teto mais baixo** (~790–826): é a escala mais "comprimida" — tirar nota muito alta é estruturalmente mais difícil.
- O **teto muda a cada ano** (amplitude de 31 a 55 pts) porque a TRI é **calibrada por edição** — não existe "nota máxima fixa".
- **Mínimas** são mais ruidosas (270–394): o piso depende do padrão de respostas dos que menos acertaram.
- **2025**: MT máx 980 (alto, no padrão), LC máx 794 (baixo, no padrão), pisos ~310.

## Arquivos
- `SERIE_minmax_TRI_2015_2025.png` — gráfico principal (4 áreas).
- `minmax_year.py` · `chart_serie_historica.py` · `minmax_2024.json` · `minmax_2025.json` — reprodutível.
- `crawl_inep.sh` — crawler INEP (fallback, lento neste ambiente).

## Mediana (NÃO está no gráfico)
- **Removida do gráfico a pedido** (só havia dado para 2024–2025, ficava desbalanceada). Os valores reais
  ficam salvos em `mediana_2024_2025.json` caso se queira no futuro: 2024 CN 488 · CH 516 · LC 532 · MT 499;
  2025 CN 498 · CH 513 · LC 539 · MT 500 (`mediana_2024_2025.py`, histograma bin=1).
- **2015–2023 não têm mediana**: o xlsx do usuário traz min/máx/média **por nº de acertos**, sem a
  contagem de alunos por acerto → impossível derivar a mediana global sem o microdado por aluno
  (que não está no disco; só ENEM-por-escola 2005–2015, nível-escola). Nunca estimada ([[no-fake-data-enem-microdados]]).
  Para uma futura linha de mediana em todos os anos: colocar o microdado individual 2015–2023 numa pasta (como o de 2024).

## Crédito / marca
Estudo por **Alexandre Emerson Melo de Araújo** · X-TRI · contato@xtri.online · xtri.online.
Gráfico com marca d'água do logo X-TRI e rodapé padrão.

## Observações
- Redação foi omitida do gráfico de tendência: é limitada a **0–1000 por construção da grade** (mín/máx triviais).
- 2009 também está disponível no xlsx (com lacuna 2010–2014) caso se queira uma visão de 16 anos.
</content>
