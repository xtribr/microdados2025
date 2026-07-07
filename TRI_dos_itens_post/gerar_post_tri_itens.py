#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o post WordPress 'TRI das questões do ENEM 2025' com tabelas reais do TRI_ITENS_AZUL_ENEM2025.xlsx."""
import openpyxl, os
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"
OUT=f"{BASE}/TRI_dos_itens_post"; os.makedirs(OUT,exist_ok=True)
wb=openpyxl.load_workbook(f"{BASE}/TRI_ITENS_AZUL_ENEM2025.xlsx", data_only=True)
ws=wb["TRI_itens"]; rows=list(ws.iter_rows(values_only=True))[1:]
AREAS=[("Linguagens","Linguagens e Códigos","1 a 45"),
       ("Ciências Humanas","Ciências Humanas","46 a 90"),
       ("Ciências da Natureza","Ciências da Natureza","91 a 135"),
       ("Matemática","Matemática","136 a 180")]
def tier(a):
    if a is None: return "—"
    if a>=1.70: return "muito alta"
    if a>=1.35: return "alta"
    if a>=0.65: return "moderada"
    return "baixa"
data={}
for r in rows:
    n,area,ling,co,hab,gab,a,b,c,tri,pac,nresp,anul=r
    if area=="Linguagens" and ling=="Espanhol": continue   # LC = Inglês p/ 1-5
    data.setdefault(area,[]).append((n,tri,a,pac,bool(anul)))
def fmt(v,suf=""):
    return f"{v:.1f}{suf}".replace(".",",") if isinstance(v,(int,float)) else "—"
def media(area):
    vs=[x[1] for x in data[area] if isinstance(x[1],(int,float))]; return sum(vs)/len(vs)

L=[]
def w(s=""): L.append(s)
w("<!-- ===================== SEO / RankMath ===================== -->")
w("**Título SEO (H1):** TRI das questões do ENEM 2025: as 180, da fácil à brutal")
w("**Slug:** tri-das-questoes-do-enem-2025")
w("**Meta description (155):** A TRI das questões do ENEM 2025, item a item: dificuldade, discriminação e % de acerto das 180 questões nos microdados do INEP. Da mais fácil à mais brutal.")
w("**Focus keyphrase:** TRI das questões do ENEM 2025")
w("**Keyphrases secundárias:** dificuldade das questões ENEM 2025 · questão mais difícil do ENEM · parâmetros TRI itens · discriminação Baker · microdados ENEM 2025")
w("**Categoria:** Microdados ENEM · **Tags:** ENEM 2025, TRI, dificuldade, discriminação, microdados, itens")
w("**Imagem destacada:** `xtri_tri_itens_capa.png` (1200×630) — *alt:* \"TRI das questões do ENEM 2025: dificuldade das 180 questões por área — XTRI.\"")
w("<!-- schema Article + FAQPage · author: Xandão (XTRI) · datePublished -->")
w("<!-- ====================================================== -->\n")
w("# TRI das questões do ENEM 2025: as 180, da fácil à brutal\n")
w("Qual foi a questão mais difícil do ENEM? E a mais fácil? A **TRI das questões do ENEM 2025** responde com precisão. "
  "Usando os [**microdados do ENEM 2025** (INEP)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem), "
  "medimos as **180 questões** pela Teoria de Resposta ao Item — dificuldade, discriminação e taxa de acerto — questão por questão, área por área.\n")
w("![TRI das questões do ENEM 2025: dificuldade vs acerto das 180 questões, por área](xtri_tri_itens_scatter.png)")
w("*Cada ponto é uma questão: quanto maior a dificuldade TRI, menor o acerto observado (correlação −0,83). Fonte: Microdados ENEM 2025 / INEP, análise XTRI.*\n")
w("## O que a TRI mede em cada questão\n")
w("Na TRI das questões do ENEM 2025, três números contam a história de cada item:\n")
w("- **Dificuldade TRI** (escala `b×100+500`, a mesma da sua nota): quanto maior, mais difícil. 500 é a média da escala.")
w("- **Discriminação** (parâmetro `a`, faixas de Baker): o quanto a questão separa quem sabe de quem não sabe — *muito alta, alta, moderada*.")
w("- **% de acerto observado**: a proporção real de acerto entre os presentes.\n")
w("## Os extremos na TRI das questões do ENEM 2025\n")
w("- **A mais brutal de toda a prova:** Matemática **Q160**, dificuldade TRI **923,7** — só **15% de acerto**.")
w("- **A mais fácil:** Linguagens **Q26**, TRI **440,4** — **87% de acerto**.")
w("- **A que mais separa os candidatos:** Natureza **Q120**, discriminação `a = 6,00` (curva quase vertical).")
w("- **Os menores acertos:** MT **Q140 (9,1%)** e CN **Q108 (9,4%)**.")
w("- No geral, **dificuldade e acerto andam juntos ao contrário**: correlação **−0,83** entre TRI e % de acerto.\n")
for area,label,faixa in AREAS:
    items=data[area]; valid=[x for x in items if not x[4] and isinstance(x[1],(int,float))]
    md=max(valid,key=lambda x:x[1]); mf=min(valid,key=lambda x:x[1])
    top=sorted(valid,key=lambda x:-x[1])[:10]
    w(f"## TRI das questões de {label} (Q{faixa})\n")
    w(f"Na {label}, a dificuldade TRI média foi **{fmt(media(area))}**. A mais difícil é a "
      f"**Q{md[0]} ({fmt(md[1])}, {fmt(md[3],'%')} de acerto)**; a mais fácil, a **Q{mf[0]} ({fmt(mf[1])}, {fmt(mf[3],'%')})**. "
      f"Veja as **10 mais difíceis** da área:\n")
    w("| Nº | Dificuldade TRI | Discriminação | % de acerto |")
    w("|---|---|---|---|")
    for n,tri,a,pac,anul in top:
        w(f"| {n} | {fmt(tri)} | {tier(a)} | {fmt(pac,'%')} |")
    w("")
w("> A **TRI das questões do ENEM 2025** completa — as 180, item a item — está no carrossel da XTRI e "
  "na planilha de dados; aqui destacamos as mais difíceis de cada área.\n")
w("## Dificuldade × acerto na TRI das questões do ENEM 2025\n")
w("A correlação entre a dificuldade TRI e o acerto observado é de **−0,83**: quanto mais difícil o item pela TRI, "
  "menor o acerto real — exatamente o esperado de uma calibração consistente. Quando os dois discordam (item "
  "\"fácil\" pela TRI com acerto baixo, ou vice-versa), é sinal de um item que se comporta de forma atípica — "
  "tema que exploramos em outro estudo. É essa coerência que faz a TRI das questões do ENEM 2025 ser uma régua confiável.\n")
w("## Perguntas frequentes\n")
w("**Qual foi a questão mais difícil do ENEM 2025?** Na TRI das questões do ENEM 2025, a campeã é a Q160 de Matemática (dificuldade 923,7 na escala da nota), com apenas 15% de acerto.\n")
w("**O que é a dificuldade TRI de uma questão?** É o parâmetro `b` do item levado para a escala da nota (`b×100+500`). Quanto maior, mais difícil; 500 é a média.\n")
w("**O que significa a discriminação de um item?** É o quanto ele separa quem domina de quem não domina o conteúdo (parâmetro `a`, faixas de Baker). Alta discriminação = a questão \"pesa\" mais na nota TRI.\n")
w("**Acerto alto significa questão fácil?** Quase sempre — a correlação é −0,83 —, mas não é regra absoluta: discriminação e chute também influenciam.\n")
w("---\n")
w("Conhecer a TRI das questões do ENEM 2025 ajuda você a entender onde a prova foi dura — e por que a sua nota é o que é.\n")
w("*Por Xandão — professor e CEO da XTRI, especialista em ENEM, TRI e análise de microdados. "
  "Leia também: [Microdados do ENEM: o guia completo](microdados-do-enem-guia-completo) e "
  "[As questões mais chutáveis do ENEM 2025](questoes-mais-chutaveis-do-enem-2025). "
  "Fonte: Microdados ENEM 2025 / INEP (caderno Azul).*\n")
w("*Dados reais ou nada.*")
open(f"{OUT}/POST_WORDPRESS_tri_itens.md","w").write("\n".join(L))
print("post gerado. médias:", {a:round(media(a),1) for a,_,_ in [(x[0],0,0) for x in AREAS]})
PY=0
