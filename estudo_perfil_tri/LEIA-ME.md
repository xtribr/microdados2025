# Estudo E1 — "A prova mede melhor quem?" Função de Informação × rede de ensino

Primeiro estudo da série **TRI × perfil do aluno** (ver `../ROADMAP3_estudos_TRI_x_perfil.md`).
Une o conceito mais central da TRI — a **precisão da medida** — ao único perfil que pode cruzar
com a nota: a **rede de ensino** (`TP_DEPENDENCIA_ADM_ESC`, que vive em `RESULTADOS`, mesma linha da nota).

## Pergunta
Em que faixa da escala o ENEM mede com nitidez — e quem cai nessa faixa?

## Método (100% dado real INEP, nada estimado)
1. **Função de Informação do Teste `I(θ)`** por área, montada com os parâmetros 3PL dos itens do
   **caderno Azul regular** (`CO_PROVA`: CN 1483 · CH 1447 · LC 1459 · MT 1471), modelo de Birnbaum **D=1**
   (convenção ENEM). Itens anulados removidos (`IN_ITEM_ABAN==1`): CN 3, MT 2. LC = 40 comuns + 5 inglês
   (língua majoritária; 45 itens). Fórmula: `Iᵢ(θ)=aᵢ²·((Pᵢ−cᵢ)/(1−cᵢ))²·((1−Pᵢ)/Pᵢ)`, com
   `Pᵢ(θ)=cᵢ+(1−cᵢ)/(1+e^{−aᵢ(θ−bᵢ)})`. Erro-padrão da medida `SE(θ)=1/√I(θ)`; em pontos ENEM `=100/√I`.
   → `e1_informacao_x_rede.py` (lê `ITENS_PROVA_2025.csv`).
2. **Densidade da nota por rede**: 1 passada streaming sobre `RESULTADOS_2025.csv` (4,81 mi linhas),
   histograma de `NU_NOTA_{área}` por `TP_DEPENDENCIA_ADM_ESC` (bin 2 pts), só presentes.
   → `hist_nota_por_rede.py` → `hist_nota_por_rede.json`.
3. Sobreposição: curva `I(θ)` + densidade de cada rede na mesma escala; medianas e erro-padrão nas medianas.

## Trava de integridade (respeitada)
- Só `RESULTADOS` + `ITENS`. **Nada de `PARTICIPANTES`** (renda/raça/sexo não cruzam nota).
- Rede de ensino é recorte INEP-publicável (mesma linha da nota), não socioeconômico inferido.
- Campos de escola só existem no **subset com escola declarada = 36,1%** (1.739.028 linhas;
  estadual 79,5% · privada 15,7% · federal 4,3% · municipal 0,5% — municipal omitida do gráfico por n e ruído).
- `a,b,c` são do item (idênticos entre cores); a cor só fixa a seleção/ordem dos 45 itens.

## Achados (reais)
Pico de informação (faixa de medida mais precisa) e erro-padrão nas medianas de cada rede:

| Área | Pico de precisão | Mediana estadual → erro | Mediana privada → erro |
|---|---|---|---|
| Ciências da Natureza | ≈ 630 | 473 → ±49 pts | 555 → ±27 pts |
| Ciências Humanas | ≈ 603 | 483 → ±38 pts | 577 → ±19 pts |
| Linguagens | ≈ 588 | 517 → ±22 pts | 583 → ±15 pts |
| Matemática | ≈ 698 | 463 → ±67 pts | 627 → ±26 pts |

**Leitura:** em todas as áreas o pico de informação fica **acima** de onde está a maioria da rede estadual.
O caso extremo é **Matemática**: a prova "enxerga" com nitidez perto de 698, mas a mediana estadual (463)
está na cauda — ali o erro de medida é **±67 pts**, contra **±26 pts** no aluno mediano da privada (627).
Ou seja, a mesma prova mede o topo com lupa e a base com régua grossa — não é "azar", é desenho do teste.

## Arquivos
- `E1_informacao_x_rede.png` — figura principal (4 áreas).
- `e1_informacao_x_rede.py` · `hist_nota_por_rede.py` (+ `.json`) — reprodutível.
- `anchor_nota_por_perfil_*` — médias por rede/UF/localização/língua (base das âncoras do ROADMAP3).
- `TEXTOS_E1.md` — legenda/SEO para publicação.
</content>
