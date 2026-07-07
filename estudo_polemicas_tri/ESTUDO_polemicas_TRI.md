# As 10 questões mais polêmicas do ENEM 2025 pela TRI

**Base:** Microdados ENEM 2025 / INEP — `dificuldade_consolidado.json` (a, b, c e taxa de acerto real *p* por item) + `ITENS_PROVA_2025.csv` (posição no caderno). Aplicação **regular (P1)**, **caderno Azul**. 180 itens não anulados avaliados.

## O que é "polêmica" aqui — Índice de Polêmica TRI (IPT)

Um item é problemático quando **mede mal**. O IPT combina, em pé de igualdade, três sinais clássicos de mau comportamento psicométrico, cada um convertido em **percentil (0–100)** dentro dos 180 itens e depois calculado a média:

1. **Baixa discriminação** (parâmetro `a` baixo) → a questão quase não separa quem sabe de quem não sabe.
2. **Chute alto** (parâmetro `c` alto) → dá para acertar sem dominar o conteúdo.
3. **Desajuste modelo × realidade** (resíduo `|p_obs − P_previsto|`) → o acerto observado foge do que a TRI previa (P previsto = 3PL integrado sobre θ~N(0,1), D=1, mesmo método validado no estudo de psicometria, r=0,955).

`IPT = média(percentil_a_baixo, percentil_c_alto, percentil_misfit)` — 0 a 100. Quanto maior, mais "polêmica".

> Transparência: pesos iguais (escolha deliberada e auditável). Os três componentes ficam no `ranking_polemica_TRI.csv` para qualquer reanálise. Nenhum valor foi estimado; itens anulados ficaram de fora.

## As 10 selecionadas (a mais polêmica de cada tema)

Tema escolhido entre as de maior IPT, com o **enunciado conferido no caderno** (print real).

| # | Tema | Área | Questão (Azul/P1) | a | Dific. TRI | c (chute) | Acerto | IPT |
|---|---|---|---|---|---|---|---|---|
| 1 | Matemática básica | MT | Q146 — diferença 10,00−9,58 s (Usain Bolt) | 1,25 | 585 | 21% | 53% | **83,6** |
| 2 | Interpretação de textos | LC | Q35 — o corpo da mulher "vigiado" | 1,26 | 631 | 28% | 47% | **79,9** |
| 3 | Física | CN | Q122 — fogão de indução (campo magnético) | 2,30 | 665 | 32% | 29% | **76,9** |
| 4 | Química | CN | Q100 — água destilada (purificação) | 1,13 | 478 | 21% | 60% | **76,7** |
| 5 | Biologia | CN | Q96 — sapinhos-ponta-de-flecha (toxinas) | 1,40 | 506 | 18% | 67% | **76,4** |
| 6 | Literatura | LC | Q16 — soneto simbolista "Símbolos" | 1,64 | 596 | 19% | 47% | **73,2** |
| 7 | Geografia | CH | Q63 — exportações/agronegócio (ranking 2019) | 1,86 | 615 | 26% | 45% | **72,6** |
| 8 | Artes | LC | Q15 — retrato na pintura / história da arte | 2,04 | 574 | 21% | 48% | **68,0** |
| 9 | Geometria | MT | Q139 — lagoa circular / ciclovia (cobertura 200 m) | 1,01 | 791 | 31% | 37% | **67,2** |
| 10 | História | CH | Q53 — teatro/dança e os imperadores cristãos (séc. IV) | 2,13 | 601 | 19% | 32% | **59,4** |

*(Dific. TRI = b×100+500.)*

### Por que cada uma "pegou"
- **Q146 (mat. básica, IPT 83,6 — a mais polêmica da prova):** é uma **subtração de decimais** (10,00 − 9,58 = 0,42), mas discrimina pouco (a=1,25) e o acerto real (53%) ficou acima do previsto — item fácil que se comporta de modo instável.
- **Q35 (interpretação):** baixa discriminação (a=1,26) somada a **chute alto (28%)**.
- **Q122 (física):** boa discriminação, mas **c=32%** — quase 1 em 3 acerta no chute — e desajuste com o observado.
- **Q100 (química):** **discriminação baixa (a=1,13)** para um item fácil (acerto 60%).
- **Q96 (biologia):** maior **desajuste** do grupo — modelo previa ~58%, saíram 67%.
- **Q139 (geometria):** o "pior item" estrutural — **discriminação baixíssima (a=1,01)**, muito difícil (TRI 791) e **chute alto (31%)**.
- **Q63 (geografia) / Q35 / Q122:** puxadas por **chute alto** (c entre 26% e 32%).

## Escopo e ressalva PPL
- Análise completa (a, b, c **e** taxa de acerto) só é possível na **aplicação regular (P1)**, onde temos o `p` observado.
- Para **PPL / reaplicação (P2)** existem os parâmetros TRI (a, b, c) no microdado, mas **não** a taxa de acerto no nosso RESULTADOS regular — então 1–2 cards de PPL, se incluídos, mostram apenas a TRI, com aviso explícito no card. (A definir na próxima etapa.)

## Arquivos
- `ranking_polemica_TRI.csv` — os 180 itens ranqueados, com a, b, c, p, P_previsto, resíduo, os 3 percentis e o IPT.
- `compute_polemica.py` — cálculo do IPT. `crop_questions.py` — recorte dos prints. `_crops_tmp/` — os 10 prints.
- Cards: `cards/` (feed 1080×1350 + story 1080×1920, padrão XTRI).
