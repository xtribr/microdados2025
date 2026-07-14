# Textos prontos — "Sua redação caiu num corretor mais duro?" (A6)

Tema (A6 do roadmap): divergência entre os dois corretores independentes da redação e o sistema de desempate (3º/4º avaliador).
Base: Microdados ENEM 2025 / INEP — `RESULTADOS_2025.csv`, 3.457.555 redações com dupla correção independente (`NU_NOTA_AV1` vs `NU_NOTA_AV2` e as 5 competências de cada avaliador).
Achado-chave: os dois corretores concordam muito — em 67,5% das redações ficam a ≤80 pontos um do outro (escala 0–1000) e em 20,4% dão nota idêntica. A divergência média é de ~85 pontos. Quando passa do limite, 1 em cada 3 redações (33,1%) vai a um 3º corretor, e 5,4% à banca (4º). A competência onde mais divergem é Proposta de intervenção (C5: 26,3 pts); onde mais concordam é Norma culta (C1: 20,7 pts).
Arte (padrão visual XTRI): `card_corretores_A6.png` (feed 1080×1350) + `story_corretores_A6.png` (story 1080×1920) · gerados juntos por `build_corretores_cards.py`.

---

## 1) Instagram — legenda do feed

📝 "Será que minha redação caiu num corretor mais rígido?" Os dados do ENEM 2025 respondem.

Toda redação é corrigida por dois avaliadores que não se falam. Cruzamos as duas notas de 3,46 milhões de redações do ENEM 2025 — e o medo do "azar de corretor" tem menos espaço do que parece:

✅ Em 67,5% das redações, os dois ficaram a no máximo 80 pontos um do outro (numa escala que vai até 1000).
✅ Em 1 a cada 5 (20,4%), a nota dos dois foi idêntica.
⚖️ E quando eles discordam de verdade? 1 em cada 3 redações (33%) vai para um 3º corretor, e os casos mais extremos (5,4%) vão para uma banca. A sua nota é a média de quem corrige — não a sorte de um.

🔎 Curiosidade: a competência onde os corretores mais divergem é a Proposta de intervenção (a do "respeito aos direitos humanos") — a mais avaliativa. Onde mais concordam é a norma culta (a mais objetiva). Faz sentido.

📌 Recado: escreva sua melhor redação e confie no processo. O "azar de corretor" tem limite — e, quando ele aparece, existe rede de proteção.

Salva pra lembrar na reta final e marca quem vive com esse medo 👇

Fonte: Microdados ENEM 2025 / INEP.

Hashtags (1º comentário):
`#ENEM #ENEM2025 #Redação #RedaçãoENEM #Vestibular #Estudos #DicasENEM #FocoNoENEM #RumoAoEnem #XTRI`

Alt text: Card com o dado de que em 67,5% das redações do ENEM 2025 os dois corretores ficaram a no máximo 80 pontos um do outro, e barras da divergência média por competência (de 20,7 a 26,3 pontos).

---

## 2) LinkedIn — post do feed

O "azar de corretor" na redação do ENEM existe? Medimos nos microdados.

Cada redação do ENEM é avaliada por dois corretores independentes. Cruzamos as duas notas de 3,46 milhões de redações de 2025, competência por competência:

🔹 Em 67,5% dos casos, os dois avaliadores ficaram a ≤ 80 pontos um do outro (escala 0–1000); em 20,4%, deram nota idêntica. A divergência média é de ~85 pontos.
🔹 O sistema tem desempate: quando a diferença passa de 100 pontos no total (ou 80 em uma competência), entra um 3º corretor — foi o caso de 33% das redações. Os 5,4% mais divergentes vão a uma banca.
🔹 Onde os corretores mais divergem: Proposta de intervenção (26,3 pts), a competência mais avaliativa. Onde mais concordam: norma culta (20,7 pts), a mais objetiva.

A leitura para quem estuda (e para quem ensina): a nota da redação é a média de avaliações independentes com revisão — não o humor de uma pessoa. Transformar esse receio difuso em número é o tipo de trabalho que tira ansiedade do aluno e devolve confiança no processo.

📊 Fonte: Microdados ENEM 2025 / INEP — análise XTRI (método auditável, sem dado estimado).

\#ENEM #Educação #DadosEducacionais #ENEM2025 #Redação #INEP #AnáliseDeDados

---

## 3) WordPress — post curto (SEO)

Título: Redação do ENEM 2025: o "azar de corretor" tem limite (o que dizem os microdados)

Slug: redacao-enem-2025-divergencia-corretores

Meta (155): Em 67,5% das redações do ENEM 2025, os dois corretores ficaram a ≤80 pontos um do outro. Veja a divergência por competência e como funciona o 3º corretor.

Corpo:
Uma das maiores angústias de quem presta o ENEM é achar que a redação "caiu num corretor mais rígido". Analisamos as notas dos dois avaliadores independentes em 3,46 milhões de redações dos Microdados ENEM 2025 (INEP).

Os corretores concordam mais do que o medo sugere: em 67,5% das redações eles ficaram a no máximo 80 pontos um do outro (escala 0–1000) e em 20,4% deram nota idêntica. A diferença média é de cerca de 85 pontos.

E existe rede de proteção: quando a diferença ultrapassa 100 pontos no total — ou 80 pontos em uma única competência —, a redação é corrigida por um terceiro avaliador. Isso aconteceu em 1 a cada 3 redações (33%); os casos mais divergentes (5,4%) foram para uma banca. A nota final é a média, não a opinião de uma só pessoa.

A divergência também varia por competência: é maior na Proposta de intervenção (26,3 pontos), a mais avaliativa, e menor na norma culta (20,7 pontos), a mais objetiva.

Fonte: Microdados ENEM 2025 / INEP. Análise XTRI.

---

## Metodologia & verificação (auditável)

- População: linhas de `RESULTADOS_2025.csv` com `NU_NOTA_AV1` e `NU_NOTA_AV2` preenchidas = 3.457.555 redações (idêntico ao total de redações com nota final — toda redação válida recebeu dupla correção). Total de linhas do arquivo: 4.810.772 (confere com o oficial).
- Concordância (total): |`NU_NOTA_AV1` − `NU_NOTA_AV2`|. Resultados: ≤80 pts = 67,55% · idêntica (=0) = 20,37% · média = 84,9 · mediana = 80.
- 3º/4º corretor: fração com `NU_NOTA_AV3` preenchida = 33,10% (1.144.614); com `NU_NOTA_AV4` = 5,38% (185.926).
- Checagem de consistência: redações com diferença total >100 pts = 1.121.964 ≈ acionamentos de 3º corretor (1.144.614); a pequena diferença (~22,6 mil) corresponde à regra de >80 pts em uma única competência. Confirma a regra oficial de desempate.
- Por competência (média |AVx_comp1..5|, escala 0–200): C1 Norma culta 20,7 · C2 Compreensão do tema 21,5 · C3 Argumentação 22,0 · C4 Coesão 24,2 · C5 Proposta de intervenção 26,3.
- Integridade: dois engines independentes (gawk e mawk) deram os mesmos números. Nenhum valor estimado; nulos não foram preenchidos. Redação é múltiplo de 20; competências em passos de 40.
- Reprodutível: `build_corretores_cards.py` (gera feed + story no padrão XTRI) e `div_corretores.awk` (varredura) nesta pasta.
