# Psicometria didática — ENEM 2025 (TRI na prática)

Quatro visualizações que explicam **como a TRI funciona**, usando os parâmetros reais dos itens
(microdados INEP 2025, caderno **Azul** regular) e o desempenho observado.

## Modelo (oficial INEP)
Logístico de 3 parâmetros de Birnbaum (1968), **sem fator D=1,7**:

```
P(acerto | θ) = c + (1 − c) / (1 + e^(−a·(θ − b)))
escala da nota: nota = 100·θ + 500   (escala 500,100)
```

- **a** = discriminação (inclinação) · **b** = dificuldade · **c** = acerto ao acaso (assíntota inferior).

## Figuras
1. **`01_CCI_itens_reais.png`** — Curvas Características do Item de 5 itens reais escolhidos para
   ilustrar cada parâmetro: fácil (b baixo), o mais difícil da prova (MT Q160, b=4,24),
   discrimina muito (CN Q120, a=6,00 — quase vertical), discrimina pouco (CN Q102, a=0,67 — plana),
   e chute alto (CN Q95, c=0,40 — piso em 40%).
2. **`02_informacao_teste.png`** — Função de Informação do teste por área (onde a prova mede melhor).
   Picos: **LC ~589** (altíssima precisão na faixa média), CH ~604, CN ~630, **MT ~698**
   (mede melhor os alunos de nota alta, com menos precisão).
3. **`03_modelo_vs_observado.png`** — Validação: % de acerto **previsto** pelo modelo (integrando
   θ~N(0,1)) vs **observado** no microdado. **r = 0,955 · erro médio = 4,1 p.p.** → confirma o
   modelo (D=1) e a transformação de escala.
4. **`04_paradoxo_acertos_nota_MT.png`** — Mesmo nº de acertos, notas diferentes. Em MT (amostra
   Regular P1, 100 mil), quem fez **15 acertos** tirou de **353 a 635** (282 pontos de diferença):
   a nota depende do **padrão** de respostas, não só da quantidade.

## Fontes
- `DADOS/ITENS_PROVA_2025.csv` (parâmetros a, b, c; caderno Azul: LC 1459 · CH 1447 · CN 1483 · MT 1471).
- `analises_primi_2025_cop30/outputs/dificuldade_consolidado.json` (% de acerto observado).
- `analises_primi_2025_cop30/outputs/amostra_xtri_2025_MT.csv` (acertos × nota, Regular P1).

## Nota de integridade (parâmetros reais excedem limites assumidos)
Nos dados reais de 2025, **a chega a 7,35** (134 linhas com a>4,0) e **c chega a 0,40** (49 linhas com c>0,35).
Ou seja, os limites `a≤4,0` e `c≤0,35` da skill `data-integrity` são apertados demais para o ENEM 2025 —
valores reais, não erros. (Análoga à correção de redação = múltiplo de 20.)
