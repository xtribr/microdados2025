# LinkedIn — Parâmetros TRI da COP30 (texto simples, sem markdown na publicação)

A comunidade inteira do ENEM procurou os parâmetros TRI da prova da COP30 — e concluiu que o INEP não tinha publicado.

Eu também concluí isso. Estávamos todos errados.

Os parâmetros a, b e c dos 186 itens da prova aplicada em Belém, Ananindeua e Marituba estão públicos nos microdados desde o dia da divulgação. O problema: estão sob códigos de prova diferentes dos que identificam os candidatos.

No RESULTADOS_2025, quem fez a prova da COP30 tem códigos 1583 a 1634 ("BAM2" no Dicionário). Esses códigos têm ZERO linhas no ITENS_PROVA_2025 — a busca natural morre aí.

Mas os mesmos cadernos estão no ITENS_PROVA sob os códigos 1499 a 1538, com os 3 parâmetros preenchidos em 100% dos itens. Na regular e na reaplicação, a numeração bate entre os dois arquivos. Só na COP30 ela quebra — e foi isso que escondeu os dados de todo mundo.

Como eu sei que são mesmo os itens da COP30, e não de outra prova?

1. O gabarito oficial divulgado da aplicação de Belém (PDF público do INEP) é idêntico, letra por letra, ao gabarito desses cadernos no ITENS_PROVA — 185 posições, incluindo inglês e espanhol.

2. O gabarito gravado no RESULTADOS para os 66 mil candidatos da COP30 confere com os 16 cadernos. Zero divergências.

3. Esses itens não aparecem em nenhuma outra prova de 2025: zero questões em comum com a regular e com a reaplicação.

Ou seja: ninguém estimou nada. É a calibração oficial do INEP — só faltava a ponte entre as numerações, que agora está validada e documentada.

Dois detalhes para quem for reproduzir: em Ciências da Natureza a correspondência não segue a ordem crescente (Verde é 1621→1514 e Cinza é 1622→1513), e existe um 186º item que só aparece nos cadernos adaptados (ampliada/Braille/leitor de tela), com parâmetros próprios.

Isso destrava análise item a item, dificuldade, discriminação e estudo por escola para toda a região metropolitana de Belém — o que até semana passada parecia impossível.

O passo a passo completo de verificação (dá para conferir no Excel em 5 minutos) está no blog, e a planilha consolidada com o script de validação em R eu envio para qualquer professor que pedir.

Transformamos dados em aprovações.

Fonte: Microdados ENEM 2025 e Dicionário / INEP.

#ENEM #ENEM2025 #TRI #COP30 #microdados #INEP #educação #psicometria
