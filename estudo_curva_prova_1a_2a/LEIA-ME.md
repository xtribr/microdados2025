# Curva da prova — Função de Informação: 1ª aplicação × 2ª aplicação (reaplicação/PPL) · ENEM 2025

Comparação da **curva psicométrica da prova** (Test Information Function, TIF) entre a prova da
**1ª aplicação** (regular) e a prova da **2ª aplicação** (reaplicação/PPL). As duas são equalizadas
para a **mesma escala TRI** — a curva mostra em que faixa cada prova mede com mais precisão.

## Por que esta comparação (e não "notas de PPL")
O microdado do INEP **não separa PPL de reaplicação**: a 2ª aplicação (16–17/dez/2025) é a
"Prova de reaplicação/Pessoas Privadas de Liberdade" — uma prova só para os dois grupos
(confirmado no `Leia_Me_Enem_2025.pdf` e `ENEM_Procedimentos_de_Analise.pdf`). Além disso, no
RESULTADOS_2025 o grupo de 2ª aplicação é minúsculo (~300–665/área) e pontua **mais** que a 1ª
(média CH 562 vs 513) — ou seja, é **reaplicação**, não PPL. Logo, uma "curva de notas de PPL" é
**impossível** com este dado ([[no-fake-data-enem-microdados]]). O que é factível e honesto é comparar a
**curva da PROVA** (itens), que independe das notas dos participantes.

## Método
- 3PL de Birnbaum, D=1 (convenção ENEM): `P(θ)=c+(1-c)/(1+e^{-a(θ-b)})`.
- `I(θ)=Σ aᵢ²·((Pᵢ-cᵢ)/(1-cᵢ))²·((1-Pᵢ)/Pᵢ)`; eixo convertido p/ nota `=100θ+500`.
- Caderno Azul de cada aplicação (params do item são intrínsecos): 1ª = CN 1483·CH 1447·LC 1459·MT 1471;
  2ª = CN 1569·CH 1539·LC 1549·MT 1559. Anulados removidos; LC = 40 comuns + 5 inglês.
- `curva_prova_1a_vs_2a.py` → `CURVA_prova_1a_vs_2a_TIF.png`.

## Achados (reais)
| Área | Pico 1ª / 2ª | Imáx 1ª / 2ª | b̄ (TRI) 1ª / 2ª | Leitura |
|---|---|---|---|---|
| Natureza | 630 / 638 | 27,9 / **41,6** | 619 / 619 | 2ª mede **bem mais preciso** na mesma faixa |
| Humanas | 603 / 587 | **27,7** / 20,3 | 607 / 583 | 2ª mais **fácil** e mede pior (menos discriminação) |
| Linguagens | 588 / 572 | **43,6** / 27,8 | 572 / 567 | 1ª mede **muito mais preciso** (prova regular forte) |
| Matemática | 698 / 720 | 21,2 / **31,7** | 674 / 690 | 2ª mais **difícil** e mede melhor no **topo** |

- Não há um padrão único: a 2ª aplicação não é "mais fácil" nem "mais difícil" em bloco — varia por área.
- CN e MT: a 2ª aplicação mede com mais nitidez (pico de informação mais alto), MT deslocado para cima.
- LC: a prova da 1ª aplicação é a que mais discrimina (pico 43,6) — a 2ª mede bem menos.

## Honestidade / limites
- Isto compara a **prova** (itens), não os participantes PPL. A 2ª aplicação mistura reaplicação e PPL
  na mesma prova; o INEP não permite isolar PPL.
- Crédito: estudo por **Alexandre Emerson Melo de Araújo** · X-TRI · contato@xtri.online · xtri.online.
</content>
