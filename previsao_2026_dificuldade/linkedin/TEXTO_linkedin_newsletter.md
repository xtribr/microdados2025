# Newsletter LinkedIn — O ENEM fica mais difícil a cada ano?

Capa: `capa_linkedin_previsao_2026_1280x720.png` (1280×720)
Gráficos (nesta ordem): `wp_inline_dificuldade_2026.png` · `wp_metodologia_regressao_2026.png`

---

## Título
O ENEM fica mais difícil a cada ano? 16 anos de dados dizem que não

## Subtítulo
Puxei o parâmetro oficial de dificuldade da TRI de 16 edições do ENEM (2010-2025) para responder com dado, não com sensação de quem acabou de sair da prova. Primeiro post da minha série de previsões e simulações — e ele começa desmontando a própria pergunta.

---

## Corpo

Toda edição do ENEM, ouço a mesma frase de aluno e de professor: "esse ano ficou mais difícil". Em vez de discordar ou concordar por sensação, fui direto aos microdados oficiais do INEP e ao parâmetro b (dificuldade) do modelo TRI de 16 edições, 2010 a 2025, área por área. Rodei regressão linear com intervalo de confiança de 95% em cada uma das quatro áreas. A resposta direta: não existe tendência real de aumento em nenhuma delas.

> [GRÁFICO 1 — wp_inline_dificuldade_2026.png]

### 1. Os números, sem cortar nenhum ano

Converti o parâmetro b de cada item para a escala que uso em todo post — Dificuldade TRI = b×100+500 — e tirei a média por área em cada edição (banco Regular, caderno Azul, itens não anulados). O resultado é uma faixa estável, não uma linha subindo:

- Linguagens: oscila entre 560 e 619 nos 16 anos da série.
- Ciências Humanas: entre 541 e 649.
- Ciências da Natureza: entre 608 e 665.
- Matemática: entre 639 e 737 — a área com a faixa mais alta, e de longe.

### 2. R² é a parte que ninguém mostra quando fala de "tendência"

Rodei a regressão de dificuldade contra o ano, área por área. O R² — quanto da variação a simples passagem do tempo explica — ficou em 0,003 (Linguagens), 0,049 (Ciências Humanas), 0,005 (Ciências da Natureza) e 0,042 (Matemática). Todas abaixo de 0,05: menos de 5% da variação tem a ver com o ano que passou. O resto é oscilação normal de edição para edição — não é tendência disfarçada de ruído, é ruído mesmo.

> [GRÁFICO 2 — wp_metodologia_regressao_2026.png]

### 3. A pergunta certa não é "mais difícil", é "qual área"

Isso não quer dizer que todas as áreas pesam igual. Nos 16 anos completos da série, Matemática teve a Dificuldade TRI mais alta das quatro áreas em todos os 16 anos, sem uma única exceção — de 639 em 2012 a 737 em 2018. Linguagens foi a mais baixa em 14 dessas 16 edições (as duas exceções foram para Ciências Humanas, por margem pequena, em 2011 e 2023). Essa hierarquia entre áreas é a constante real; o "ano a ano fica mais difícil" é o mito.

### 4. O ano que eu fui atrás e recuperei

Ao montar a série 2010-2024, encontrei os parâmetros de 2018 fora de qualquer escala plausível na cópia que eu tinha — dificuldade acima de 70 em módulo e discriminação acima de 19, quando o esperado é próximo de -3 a +3 e 0,5 a 3, respectivamente. Em vez de excluir o ano ou estimar um número, fui direto ao zip oficial do INEP, baixei só a tabela de parâmetros de item de 2018 (108KB, conferida por CRC32) e recalculei com a mesma metodologia dos outros 15 anos. Bateu certinho na faixa esperada: Linguagens 617, Ciências Humanas 649, Ciências da Natureza 649, Matemática 737 — o novo teto da série inteira. A conclusão (oscilação, sem tendência) se sustenta igual, agora com os 16 anos completos.

### 5. O que isso muda para quem estuda para 2027

Se não existe tendência, a estratégia certa não é torcer para uma prova mais fácil nem se blindar para uma mais difícil — é se preparar para a faixa histórica inteira de cada área, porque qualquer ponto dela é plausível na próxima edição. E, especificamente: tratar Matemática como a área estruturalmente mais exigente pela TRI não é pessimismo, é o que 16 anos de dado mostram sem exceção.

---

Fonte: banco de parâmetros de item por edição (2010-2024, Supabase) + `ITENS_PROVA_2018.csv` e `ITENS_PROVA_2025.csv` oficiais do INEP. Regressão OLS com IC de 95%, R² calculado por área. 2018 recuperado direto da fonte oficial depois de encontrar corrupção na cópia usada — recalculado, não estimado.

#enem #enem2026 #tri #psicometria #previsao #microdados #vestibular #professor

## Texto alternativo (acessibilidade)

Gráfico com 4 painéis, um por área do ENEM (Linguagens, Ciências Humanas, Ciências da Natureza, Matemática), mostrando a Dificuldade TRI de 2010 a 2025, 16 anos completos, e uma faixa esperada para 2026 igual à faixa histórica real de cada área. Segundo gráfico: regressão linear com intervalo de confiança de 95% por área, mostrando faixas largas e R² baixo (abaixo de 0,05) em todas as quatro áreas — evidência de que não há tendência linear real de aumento na dificuldade.

## Notas de integridade
- Parâmetro b oficial do modelo 3PL da TRI (não é proxy/estimativa) — banco Regular, caderno Azul, itens não anulados.
- Série 2010-2024 filtrada por reaplicação e itens não convergentes (`|b| ≤ 6`); 2018 e 2025 recalculados direto dos arquivos oficiais do INEP, mesma metodologia.
- 2018 estava corrompido na cópia usada originalmente (Supabase) — recuperado direto do zip oficial do INEP, com verificação de integridade por CRC32, e recalculado do zero. Nenhum valor estimado ou preenchido.
- Fonte: Microdados ENEM / INEP.
