#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, re, csv, unicodedata
PB="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/PROVAS E GABARITOS"
D1=f"{PB}/ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf"   # LC 1-45, CH 46-90
D2=f"{PB}/ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf"   # CN 91-135, MT 136-180

def pages(pdf):
    out=subprocess.run(["pdftotext","-layout",pdf,"-"],capture_output=True).stdout.decode("utf-8","ignore")
    return out.split("\f")

def qmap(pdf):
    m={}  # qnum -> (page, text)
    pgs=pages(pdf)
    cur=None; buf=[]; curpage=None
    flat=[]
    for pi,pg in enumerate(pgs,1):
        for line in pg.split("\n"):
            mm=re.search(r"Quest[ãa]o\s+(\d{2,3})", line)
            if mm:
                if cur is not None: m[cur]=(curpage," ".join(buf))
                cur=int(mm.group(1)); curpage=pi; buf=[line]
            elif cur is not None:
                buf.append(line)
    if cur is not None: m[cur]=(curpage," ".join(buf))
    return m

Q={};
for pdf in (D1,D2):
    Q.update(qmap(pdf))

def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').lower()

KW={
 "Biologia":["celul","dna","gene","protein","ecossist","organism","especie","fotossint","enzim","sangue","virus","bacteri","micro-organ","vacina","hormon","planta","metabol","biodivers","sinapse","neuron","tecido"],
 "Quimica":["mol ","reacao","atomo","molecul","acido","base ","ph ","ion","oxida","combust","ligacao","solucao","concentracao","elemento quimico","composto","hidrogenio","carbono","metal","sal ","gas ","quimic"],
 "Fisica":["forca","energia","velocidade","aceleracao","corrente","tensao","circuito","onda","luz","calor","temperatura","potencia","campo","movimento","frequencia","resistencia","eletric","newton","joule","watt","massa "],
 "Geometria":["area","volume","perimetro","triangulo","circulo","circunferencia","angulo","retangulo","cubo","esfera","cilindro","semelhanc","pitagoras","poligono","coordenada","quadrado","losango","trapezio","raio","diametro"],
 "MatBasica":["porcentagem","por cento","%","razao","proporcao","regra de tres","media","juros","fracao","equacao","funcao","grafico","tabela","probabilidade","conjunto","sequencia","numero"],
 "Literatura":["poema","poesia","verso","soneto","romance","modernism","conto","narrador","eu lirico","literatura","estrofe","cronica literaria","drummond","machado","quintana","bandeira"],
 "Artes":["pintura","obra de arte","artista","escultura","musica","danca","teatro","performance","instalacao","quadro","tela","fotografia","grafite","cinema","arquitetura","artes visuais"],
 "Historia":["seculo","guerra","revolucao","imperio","colonial","escrav","republica","ditadura","vargas","idade media","feudal","iluminism","independencia","golpe","monarquia"],
 "Geografia":["clima","relevo","urban","territorio","regiao","agricultura","industri","migrac","globaliz","recursos","bioma","hidrograf","populacao","fronteira","economi","desmatament"],
}
def guess(t):
    n=" "+norm(t)+" "; sc={}
    for k,ws in KW.items():
        sc[k]=sum(n.count(w) for w in ws)
    best=sorted(sc.items(),key=lambda x:-x[1])
    return best[0][0] if best[0][1]>0 else "?", best[:3]

rows=list(csv.DictReader(open("/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/estudo_polemicas_tri/ranking_polemica_TRI.csv")))
print("=== Candidatas (top IPT) com tema-palpite, por area ===")
for ar in ["CN","MT","LC","CH"]:
    print(f"\n##### {ar} #####")
    sub=[r for r in rows if r["area"]==ar][:14]
    for r in sub:
        pos=int(r["pos_azul"]) if r["pos_azul"] else 0
        pg,txt=Q.get(pos,(None,""))
        g,top=guess(txt)
        sn=re.sub(r"\s+"," ",txt)[:120]
        print(f'  IPT{r["IPT"]:>5} it{r["CO_ITEM"]} Q{pos:>3} pg{pg} hab{r["hab"]} a={r["a"]} c={r["c"]} p={r["p_obs"]} -> {g:10} | {sn}')
