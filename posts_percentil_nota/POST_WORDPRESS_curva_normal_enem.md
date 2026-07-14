<!-- ===================== SEO / RankMath ===================== -->
**Focus keyphrase:** curva normal do ENEM

**Prova de ineditismo — frases-foco já usadas ou reservadas (nenhuma colide):**
- questões em branco no ENEM · reaplicação do ENEM · ordem das questões no ENEM · como funciona a nota do ENEM · questões mais chutáveis do ENEM · TRI das questões do ENEM 2025 · abstenção no ENEM 2025 · questões anuladas do ENEM 2025 · habilidades mais difíceis do ENEM 2025 · questões mais difíceis ENEM 2025 · parâmetros TRI da COP30 · como funciona a TRI do ENEM (engavetada)
- **curva normal do ENEM** é inédita: nenhum post trata da construção estatística da escala 0–1000 nem de percentis empíricos por área.

**Título SEO (H1):** Curva normal do ENEM: por que 700 é top 0,4% em Linguagens e top 10,4% em Matemática
**Slug:** curva-normal-do-enem *(20 caracteres — ≤ 75 ✓)*
**Meta description (152 caracteres):** Curva normal do ENEM: como a escala 0–1000 foi desenhada (500 = média, 100 = 1 desvio) e os percentis reais de 2025 por área, com dados do INEP.
**Keyphrases secundárias:** escala do ENEM · percentil da nota · desvio-padrão · z-score · nota 700 · TRI · microdados ENEM 2025
**Categoria:** Microdados ENEM · **Tags:** ENEM 2025, TRI, curva normal, estatística, percentil, nota 700, INEP, microdados, escala
**Imagem destacada:** `posts_percentil_nota/capa_wp_curva_normal_1200x630.png` (1200×630) — *alt:* "Curva normal do ENEM: a escala 0–1000 e os percentis reais de 2025 — XTRI."
<!-- schema Article · author: Prof. Alexandre Emerson (XTRI) · datePublished -->
<!-- ====================================================== -->

# Curva normal do ENEM: por que 700 é top 0,4% em Linguagens e top 10,4% em Matemática

A **curva normal do ENEM** não é força de expressão: a escala de 0 a 1000 foi literalmente desenhada sobre a distribuição normal. Quando o INEP construiu a métrica atual, definiu que **500 é a média** e que **cada 100 pontos equivalem a 1 desvio-padrão** da população de referência (os concluintes de escola pública que fizeram o [ENEM 2009, conforme documentação do INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)). Neste post, mostro a matemática dessa construção — e depois confronto o desenho teórico com os **percentis reais de 2025**, que calculei varrendo os microdados dos 3,4 milhões de presentes da aplicação regular. A diferença entre a teoria e o dado é onde mora a informação que interessa a professor e aluno.

## A construção da escala: um z-score vestido de 0 a 1000

A TRI estima, para cada candidato, uma proficiência **θ** (theta) numa métrica padronizada: média 0, desvio-padrão 1 — exatamente um **z-score**. A nota divulgada é uma transformação linear disso:

```
nota = 500 + 100·θ
```

É o mesmo esqueleto do T-score clássico da psicometria (T = 50 + 10·z), só que com fator 100. Consequências diretas da definição:

- **500** = média da população de referência;
- **600** = 1 desvio acima da média; **700** = 2 desvios; **800** = 3 desvios;
- a proficiência θ vem do modelo logístico de **3 parâmetros** (discriminação *a*, dificuldade *b* e acerto casual *c* de cada item) — por isso a dificuldade de um item também se expressa na escala da nota: **dificuldade = b×100 + 500**.

Sobre a curva normal do ENEM, as faixas clássicas da estatística viram uma régua de leitura imediata: **68,2%** da referência entre 400 e 600; só **15,9%** acima de 600; só **2,3%** acima de 700; e acima de 800, **1 em cada mil** (0,13%).

## A curva normal do ENEM na prática: o que 2025 mostra de verdade

A referência é de 2009 — e a população que faz a prova hoje não é a de 2009, nem cada prova mede igual em toda a régua. Varri o `RESULTADOS_2025.csv` inteiro (presentes com nota válida da 1ª aplicação regular, incluindo cadernos de acessibilidade) e calculei média, desvio e percentil empírico de cada área:

| Área | n | Média | Desvio-padrão | Máxima 2025 |
|---|---|---|---|---|
| Linguagens | 3.388.360 | 533,2 | **71,0** | 794,5 |
| Humanas | 3.381.817 | 512,9 | 84,2 | 856,4 |
| Natureza | 3.196.706 | 500,4 | 78,2 | 858,7 |
| Matemática | 3.196.596 | 520,8 | **127,6** | 980,3 |

Repare no desvio-padrão: **a régua de Matemática (127,6) é quase o dobro da de Linguagens (71,0)**. A escala de MT "estica" — a nota máxima chegou a 980,3 — enquanto a de LC é curta e comprimida (máxima 794,5). Isso não é acidente: é consequência da distribuição de dificuldade e discriminação dos itens de cada prova, que concentram informação em trechos diferentes da régua.

## Percentil empírico: onde cada nota cai de verdade

Com a distribuição real, dá para responder sem assumir normalidade nenhuma — percentil observado, candidato contado um a um:

| Nota | Linguagens | Humanas | Natureza | Matemática |
|---|---|---|---|---|
| 600 | top 16,5% | top 16,1% | top 10,2% | top 26,5% |
| 650 | top 3,4% | top 5,1% | top 3,5% | top 17,5% |
| 700 | **top 0,4%** | top 1,1% | top 1,1% | **top 10,4%** |
| 750 | <0,1% | top 0,1% | top 0,2% | top 5,5% |
| 800 | — | — | — | top 2,5% |

A leitura teórica da curva normal do ENEM diria "700 = top 2,3%" em qualquer área. O dado real de 2025 mostra **top 0,4% em Linguagens e top 10,4% em Matemática** — uma razão de 26 vezes entre as áreas para a mesma nota. Em Linguagens, 700 é um evento de 4 em mil; em Matemática, 104 em mil chegam lá.

## Por que a teoria e o dado divergem (tecnicamente)

1. **População ≠ referência.** A média de 2025 não é 500 em todas as áreas (LC está em 533,2), porque a população atual difere da coorte de 2009 — a escala preserva o significado histórico, não a simetria anual.
2. **Assimetria e cauda.** As distribuições reais têm assimetria positiva — especialmente MT, cuja cauda direita longa é sustentada por itens de dificuldade altíssima (há item com b = 3,46, dificuldade 846 na escala). Onde há item difícil e discriminativo, a prova consegue separar candidatos no topo; onde não há, a escala satura.
3. **Teto de medida.** Nenhuma nota encosta em 1000: os máximos de 2025 variam de 794,5 (LC) a 980,3 (MT). O teto de cada área é o ponto em que a prova esgota sua capacidade de informação — tema que tratei no estudo da nota máxima.
4. **O z-score continua valendo — dentro da área.** Comparar posições relativas entre áreas ("estou em +1,5 desvio em MT e +0,3 em LC") é legítimo e útil; comparar notas brutas entre áreas, não, porque os construtos medidos são diferentes. E o percentil deve ser o **empírico**, não o da normal teórica.

## O que fazer com isso (professor e aluno)

Para o aluno: não existe "700 é sempre elite" — existe percentil por área, e é ele que entra na conta da concorrência real do seu curso. Para o professor: a métrica certa para comparar simulados, turmas e anos é a posição relativa dentro da distribuição da área, nunca a nota crua entre áreas. É exatamente essa lógica que uso para estimar chance de aprovação no [app.rankingenem.com](https://app.rankingenem.com).

Para se aprofundar: [como funciona a nota do ENEM](como-funciona-a-nota-do-enem) (o mecanismo da TRI item a item), [onde a prova do ENEM mede melhor](onde-a-prova-do-enem-mede-melhor) (informação do teste ao longo da régua) e [habilidades mais difíceis do ENEM 2025](habilidades-mais-dificeis-do-enem-2025).

---
*Por Prof. Alexandre Emerson (Xandão) — professor, CEO da XTRI e analista de microdados do ENEM/TRI. Fonte: [Microdados ENEM 2025 / INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) — 1ª aplicação regular, presentes com nota válida; percentis empíricos calculados sobre 3,4 milhões de candidatos. Nenhum valor estimado.*

<!-- ===================== CHECKLIST RankMath =====================
✓ Frase-foco "curva normal do ENEM": título SEO (início), meta (início), slug, 1º parágrafo, H2 ("A curva normal do ENEM na prática…"), alt da capa
✓ Ocorrências no corpo: 6 em ~1.010 palavras + título/meta/alt ≈ 1,0-1,2% — dentro de 1–1,5%
✓ Título: números (700 · 0,4% · 10,4%) + contraste de impacto — frase-foco no início
✓ Meta: 152 car. ≤ 155 ✓ · Slug 20 car. ≤ 75 ✓
✓ Link externo dofollow: gov.br/inep (1º parágrafo + byline)
✓ Links internos: como-funciona-a-nota-do-enem · onde-a-prova-do-enem-mede-melhor · habilidades-mais-dificeis-do-enem-2025
✓ ≥600 palavras (~1.010) · alt de imagem com frase-foco · voz 1ª pessoa · 2 tabelas de dados reais
=============================================================== -->
