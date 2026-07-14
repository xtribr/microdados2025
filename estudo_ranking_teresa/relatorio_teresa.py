#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relatório PDF (A4, marca XTRI) — posição do Colégio Teresa (CO_ESCOLA 24085081) no ENEM 2025.
Fonte: Microdados ENEM 2025 / INEP + nomes do Censo Escolar 2025. Sem dado inventado.
Benchmark = média SIMPLES das escolas do RN (cada escola pesa igual). 6 páginas + PNGs de conferência."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
import matplotlib.image as mpimg
import sys
sys.path.insert(0, "/Volumes/Kingston 1/microdados_enem_2025/palestra_2025")
from xtri_deck import outfitB, outfit, mono, monoB, LOGO
INK="#1D1D20"; GRAY="#8C9298"; BG="#F1F1F2"; CARD="#FFFFFF"
CORAL="#FA5230"; CORALd="#E8431F"; CYAN="#1FAFEF"; CYANd="#1597D8"; HL="#FFF0EC"; LINE="#E2E3E6"

D = Path("/Volumes/Kingston 1/microdados_enem_2025/estudo_ranking_teresa")
SRC = str(D/"escolas_rn_2025_agregado.csv")
NOMES = str(D/"nomes_escolas_rn.csv")
TERESA="24085081"; MIN=10
AREAS=[("LC","Linguagens"),("CH","Humanas"),("CN","Natureza"),("MT","Matemática"),("RED","Redação")]
DEPS={"1":"Fed.","2":"Est.","3":"Mun.","4":"Priv."}

# ---------------- dados ----------------
rows=[]
with open(SRC,encoding="latin-1") as f:
    for d in csv.DictReader(f,delimiter=";"):
        d["N"]=int(d["N"])
        for k in ("LC","CH","CN","MT","RED","MEDIA5"): d[k]=float(d[k])
        rows.append(d)
elig=[r for r in rows if r["N"]>=MIN]
ter=next(r for r in rows if r["CO_ESCOLA"]==TERESA)
nome={}
for ln in open(NOMES,encoding="latin-1"):
    p=ln.rstrip("\n").split(";")
    if len(p)>=2 and p[0]!="CO_ESCOLA": nome[p[0]]=p[1]

def rk(pool,key):
    pool=sorted(pool,key=lambda r:-r[key])
    for i,r in enumerate(pool,1):
        if r["CO_ESCOLA"]==TERESA: return i,len(pool)
    return None,len(pool)
parn=[r for r in elig if r["MUNICIPIO"]=="Parnamirim" and r["DEP"]=="4"]  # ranking de Parnamirim = só rede privada
SCOPES=[("Parnamirim (rede privada)",parn),
        ("RN (todas as redes)",elig),
        ("RN (rede privada)",[r for r in elig if r["DEP"]=="4"])]
RANK={full:{k:rk(pool,k) for k in ("MEDIA5","RED","LC","CH","CN","MT")} for full,pool in SCOPES}
# benchmark = média SIMPLES das escolas do RN (cada escola pesa igual)
RNAVG={a:sum(r[a] for r in elig)/len(elig) for a,_ in AREAS}
RNAVG["MEDIA5"]=sum(r["MEDIA5"] for r in elig)/len(elig)
pos_rn,n_rn=RANK["RN (todas as redes)"]["MEDIA5"]
PERC=100*(n_rn-pos_rn)/n_rn
PP,NPV=RANK["Parnamirim (rede privada)"]["MEDIA5"]  # Teresa entre as privadas de Parnamirim

ABBR=[("Centro De Educacao Integrada","CEI"),("Escola Estadual","EE"),("Professora","Profa."),
      ("Professor","Prof."),("Doutor","Dr.")]
ACC={"Educacao":"Educação","Ciencias":"Ciências","Sao":"São","Jose":"José","Fenix":"Fênix",
     "Genesis":"Gênesis","Icaro":"Ícaro","Contemporaneo":"Contemporâneo","Colgio":"Colégio",
     "Colegio":"Colégio","Antonio":"Antônio","Basilio":"Basílio","Arsenio":"Arsênio",
     "Ifrn":"IFRN","Ceep":"CEEP","Ph3":"PH3","Facex":"FACEX","Ejax":"EJAX"}
def fit(s,n=42): return s if len(s)<=n else s[:n].rsplit(" ",1)[0]+"…"
def clean(cod):
    if cod==TERESA: return "Colégio Teresa"
    s=nome.get(cod,"(sem nome)")
    for j in [" LTDA ME"," LTDA"," - S A"," S A"," ME"," EPP"," EIRELI"]:
        s=s.replace(j,"")
    s=s.title()
    for a,b in ABBR: s=s.replace(a,b)
    for a,b in ACC.items(): s=s.replace(a,b)
    return s.replace("  "," ").strip()

def rowify(pool):
    pool=sorted(pool,key=lambda r:-r["MEDIA5"])
    return [(i,clean(r["CO_ESCOLA"]),r["MUNICIPIO"],DEPS[r["DEP"]],r["N"],r["MEDIA5"]) for i,r in enumerate(pool,1)]
RN_ROWS=rowify(elig); PARN_ROWS=rowify(parn)
RN_TOP=[x for x in RN_ROWS if x[0]<=20]; TER_RN=next(x for x in RN_ROWS if x[0]==pos_rn)
parn_sorted=sorted(parn,key=lambda r:-r["MEDIA5"])

def vir(x,d=1): return f"{x:.{d}f}".replace(".",",")

# ---------------- helpers A4 (coord = pontos, 595x842) ----------------
W,H=595,842; M=46
def page(pdf,draw,tag):
    fig=plt.figure(figsize=(W/72,H/72),dpi=200)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle="square,pad=0",fc=BG,ec="none",zorder=0))
    def tw(s,fp,sz):
        t=ax.text(0,0,s,fontproperties=fp,fontsize=sz); fig.canvas.draw()
        wd=t.get_window_extent(fig.canvas.get_renderer()).width/(fig.dpi/72); t.remove(); return wd
    def txt(x,y,s,fp,sz,c=INK,ha="left",va="baseline",z=5):
        return ax.text(x,y,s,fontproperties=fp,fontsize=sz,color=c,ha=ha,va=va,zorder=z)
    def rrect(x,y,ww,hh,rad,fc,z=2,ec="none",lw=0):
        ax.add_patch(FancyBboxPatch((x+rad,y+rad),ww-2*rad,hh-2*rad,boxstyle=f"round,pad={rad}",fc=fc,ec=ec,lw=lw,zorder=z))
    def line(x1,y,x2,c=LINE,lw=1.0): ax.plot([x1,x2],[y,y],color=c,lw=lw,zorder=3,solid_capstyle="round")
    def logo(x,y,zoom=0.045):
        try: ax.add_artist(AnnotationBbox(OffsetImage(mpimg.imread(LOGO),zoom=zoom),(x,y),frameon=False,box_alignment=(0,0.5),zorder=8))
        except Exception: pass
    def sig(y):
        txt(M,y,"Transformamos ",outfitB,9.5,INK); xx=M+tw("Transformamos ",outfitB,9.5)
        txt(xx,y,"dados",outfitB,9.5,CYAN); xx+=tw("dados",outfitB,9.5)
        txt(xx,y," em ",outfitB,9.5,INK); xx+=tw(" em ",outfitB,9.5)
        txt(xx,y,"aprovações",outfitB,9.5,CORAL); xx+=tw("aprovações",outfitB,9.5); txt(xx,y,".",outfitB,9.5,INK)
        txt(W-M,y,"@xandaoxtri · xtri.online",mono,7.5,GRAY,ha="right")
    hp=dict(ax=ax,fig=fig,txt=txt,tw=tw,rrect=rrect,line=line,logo=logo,sig=sig)
    logo(M,64,0.045); txt(W-M,66,tag,mono,7.5,GRAY,ha="right",va="center"); line(M,92,W-M)
    draw(hp)
    fig.savefig(str(D/f"_pg_{draw.__name__}.png"),dpi=150,facecolor=BG)
    pdf.savefig(fig,facecolor=BG); plt.close(fig)
def footer(hp,nota,pg):
    hp["line"](M,H-96,W-M); hp["txt"](M,H-74,nota,mono,7.5,GRAY); hp["sig"](H-52)
    hp["txt"](W-M,H-30,pg,mono,7.5,GRAY,ha="right")

# ---------------- p1: capa / resumo ----------------
def p1_resumo(hp):
    txt=hp["txt"]; rrect=hp["rrect"]
    txt(M,150,"Colégio Teresa",outfitB,34,INK)
    txt(M,178,"Ensino Médio · Parnamirim / RN · rede privada",outfit,12.5,GRAY)
    txt(M,196,"Desempenho no ENEM 2025 e posição entre as escolas.",outfit,12.5,GRAY)
    rrect(M,228,W-2*M,120,12,CARD,z=2); rrect(M,228,7,120,3.5,CORAL,z=3)
    txt(M+28,262,"MÉDIA GERAL NO ENEM 2025",mono,9,GRAY)
    txt(M+28,318,vir(ter["MEDIA5"]),outfitB,46,CORAL)
    txt(M+28+150,318,"pontos",outfit,13,GRAY)
    txt(M+28+150,296,f"média das 5 provas · {ter['N']} alunos",mono,8.5,GRAY)
    txt(W-M-28,300,"TOP 10% DO RN",outfitB,15,CYANd,ha="right")
    txt(W-M-28,320,f"melhor que {PERC:.0f}% das escolas",mono,8.5,GRAY,ha="right")
    cw=(W-2*M-2*16)/3; y0=372
    prp,nrp=RANK["RN (rede privada)"]["MEDIA5"]
    minis=[(f"{PP}º",f"de {NPV}","Parnamirim (privadas)"),(f"{prp}º",f"de {nrp}","RN (privadas)"),(f"{pos_rn}º",f"de {n_rn}","RN (todas as redes)")]
    for i,(a,b,c) in enumerate(minis):
        x=M+i*(cw+16); rrect(x,y0,cw,92,10,CARD,z=2)
        txt(x+cw/2,y0+42,a,outfitB,30,INK,ha="center"); txt(x+cw/2,y0+60,b,mono,9,GRAY,ha="center")
        txt(x+cw/2,y0+80,c,outfit,10,INK,ha="center")
    txt(M,506,"Em uma frase",outfitB,13,INK); ly=528
    for ln in [f"A escola está entre as 10% melhores do RN e é a {PP}ª entre as escolas",
               "privadas de Parnamirim. Seu ponto forte é Linguagens (3º) e Humanas (4º)",
               "entre as privadas da cidade; Natureza e Matemática são as áreas a evoluir.",
               f"A redação é a maior nota da escola: {vir(ter['RED'])}."]:
        txt(M,ly,ln,outfit,11,INK); ly+=19
    footer(hp,"Fonte: Microdados ENEM 2025 / INEP · escolas do RN com 10 ou mais alunos presentes.","1 / 6")

# ---------------- p2: desempenho por área ----------------
def p2_areas(hp):
    txt=hp["txt"]
    txt(M,132,"Nota por área — Teresa x média das escolas do RN",outfitB,16,INK)
    txt(M,152,"Nota média da escola, comparada à média das escolas do Rio Grande do Norte.",outfit,11,GRAY)
    axc=hp["fig"].add_axes([M/W,0.30,(W-2*M)/W,0.40])
    labs=[n for _,n in AREAS]; xs=range(len(AREAS)); tv=[ter[a] for a,_ in AREAS]; rv=[RNAVG[a] for a,_ in AREAS]; bw=0.38
    axc.bar([x-bw/2 for x in xs],tv,bw,color=CORAL,zorder=3,label="Colégio Teresa")
    axc.bar([x+bw/2 for x in xs],rv,bw,color="#C7CBD0",zorder=3,label="Média das escolas do RN")
    for x,v in zip(xs,tv): axc.text(x-bw/2,v+8,vir(v,0),ha="center",va="bottom",fontproperties=monoB,fontsize=8.5,color=CORALd)
    for x,v in zip(xs,rv): axc.text(x+bw/2,v+8,vir(v,0),ha="center",va="bottom",fontproperties=mono,fontsize=8,color=GRAY)
    axc.set_xticks(list(xs)); axc.set_xticklabels(labs,fontproperties=outfit,fontsize=10,color=INK)
    axc.set_ylim(0,860); axc.set_yticks([200,400,600,800])
    for lab in axc.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(8); lab.set_color(GRAY)
    for s in ["top","right","left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_color("#CFD2D5"); axc.tick_params(length=0); axc.grid(axis="y",color="#ECEDEF",lw=0.8); axc.set_axisbelow(True)
    axc.legend(prop=outfit,fontsize=9,loc="upper left",frameon=False,ncol=2,bbox_to_anchor=(0,1.10))
    ry=640; txt(M,ry,"Como ler",outfitB,13,INK); ry+=20
    for ln in [f"• Cinza = média SIMPLES das 429 escolas do RN ({vir(RNAVG['MEDIA5'])}): cada escola pesa igual.",
               "• O Teresa supera essa média em todas as áreas — mas ela é um piso baixo, puxado",
               "  por muitas escolas com desempenho menor.",
               "• A comparação dura é o ranking (páginas seguintes): entre as escolas fortes, CN e",
               "  MT ainda são o ponto a evoluir."]:
        txt(M,ry,ln,outfit,10.5,INK); ry+=18
    footer(hp,"Fonte: Microdados ENEM 2025 / INEP · média simples das escolas do RN (10+ alunos).","2 / 6")

# ---------------- p3: posição (tabela + distribuição) ----------------
def p3_ranking(hp):
    txt=hp["txt"]; rrect=hp["rrect"]
    txt(M,132,"Onde o Teresa ficou",outfitB,17,INK)
    txt(M,152,"Colocação (lugar / total de escolas) em cada recorte. Menor é melhor.",outfit,11,GRAY)
    cols=["Recorte","Média","Redação","LC","CH","CN","MT"]; keys=["MEDIA5","RED","LC","CH","CN","MT"]
    x0=M; twid=W-2*M
    cx=[x0+8,x0+twid*0.42,x0+twid*0.52,x0+twid*0.635,x0+twid*0.72,x0+twid*0.81,x0+twid*0.90]
    y=188; rowh=33
    rrect(x0,y,twid,rowh,6,INK,z=2)
    txt(cx[0],y+rowh/2+1,"Recorte",monoB,9,"#FFF",va="center")
    for j,c in enumerate(cols[1:],1): txt(cx[j],y+rowh/2+1,c,monoB,9,"#FFF",va="center",ha="center")
    y+=rowh
    for si,(full,pool) in enumerate(SCOPES):
        rrect(x0,y,twid,rowh,6,CARD if si%2==0 else "#F7F7F8",z=2)
        txt(cx[0],y+rowh/2+1,full,outfit,9.5,INK,va="center")
        for j,k in enumerate(keys,1):
            p,n=RANK[full][k]; hot=k=="MEDIA5"
            txt(cx[j],y+rowh/2+1,f"{p}º",outfitB if hot else outfit,11 if hot else 10,CORALd if hot else INK,va="center",ha="center")
        y+=rowh
    txt(M,y+52,f"Ranking de Parnamirim — rede privada ({len(parn)} escolas com 10+ alunos)",outfitB,13,INK)
    axc=hp["fig"].add_axes([M/W,0.205,(W-2*M)/W,0.225])
    vals=[r["MEDIA5"] for r in parn_sorted]
    colors=[CORAL if r["CO_ESCOLA"]==TERESA else "#CBD0D5" for r in parn_sorted]
    axc.bar(range(len(vals)),vals,color=colors,zorder=3,width=0.82)
    ti=[i for i,r in enumerate(parn_sorted) if r["CO_ESCOLA"]==TERESA][0]
    axc.annotate(f"Colégio Teresa\n{PP}º de {NPV} · {vir(ter['MEDIA5'])}",xy=(ti,vals[ti]),xytext=(ti+2.0,vals[ti]+135),
                 fontproperties=monoB,fontsize=8.5,color=CORALd,ha="left",arrowprops=dict(arrowstyle="-",color=CORALd,lw=1.1))
    axc.set_ylim(0,820); axc.set_yticks([200,400,600,800])
    for lab in axc.get_yticklabels(): lab.set_fontproperties(mono); lab.set_fontsize(8); lab.set_color(GRAY)
    axc.set_xticks([])
    for s in ["top","right","left"]: axc.spines[s].set_visible(False)
    axc.spines["bottom"].set_color("#CFD2D5"); axc.tick_params(length=0); axc.grid(axis="y",color="#ECEDEF",lw=0.8); axc.set_axisbelow(True)
    axc.text(0.5,-0.13,"cada barra = uma escola privada de Parnamirim · ordenadas da maior para a menor média",
             transform=axc.transAxes,ha="center",fontproperties=mono,fontsize=7.5,color=GRAY)
    footer(hp,"Fonte: Microdados ENEM 2025 / INEP · escolas com 10 alunos ou mais presentes nos 2 dias.","3 / 6")

# ---------------- tabela de ranking nomeada (p4 e p5) ----------------
def rank_table(hp,titulo,sub,data,cols,widths,pg,hi=None,sep_before=None,rowh=23,fs=9):
    txt=hp["txt"]; rrect=hp["rrect"]; x0=M; twid=W-2*M
    txt(M,132,titulo,outfitB,17,INK); txt(M,152,sub,outfit,11,GRAY)
    xpos=[]; acc=x0
    for w in widths: xpos.append(acc); acc+=w*twid
    y=182
    rrect(x0,y,twid,rowh+1,6,INK,z=2)
    for c,xp,w in zip(cols,xpos,widths):
        ha="left" if c in ("Escola","#") else ("right" if c=="Média" else "center")
        px=xp+6 if ha=="left" else (xp+w*twid-6 if ha=="right" else xp+w*twid/2)
        txt(px,y+(rowh+1)/2+1,c,monoB,8.5,"#FFF",va="center",ha=ha)
    y+=rowh+1
    for k,r in enumerate(data):
        rank=r[0]; hot=(hi is not None and rank==hi)
        if sep_before is not None and rank==sep_before:
            txt(x0+twid/2,y+9,"· · ·",mono,10,GRAY,ha="center"); y+=15
        rrect(x0,y,twid,rowh,4,HL if hot else (CARD if k%2==0 else "#F7F7F8"),z=2)
        if hot: rrect(x0,y,4,rowh,2,CORAL,z=3)
        for val,c,xp,w in zip(r[1:],cols[1:],xpos[1:],widths[1:]):
            ha="left" if c=="Escola" else ("right" if c=="Média" else "center")
            px=xp+6 if ha=="left" else (xp+w*twid-6 if ha=="right" else xp+w*twid/2)
            fp=outfitB if (hot and c in ("Escola","Média")) else (outfit if c=="Escola" else mono)
            col=CORALd if (hot and c=="Média") else (INK if c=="Escola" else GRAY)
            s=vir(val) if c=="Média" else str(val)
            if c=="Escola": s=fit(s)
            txt(px,y+rowh/2+1,s,fp,fs if c=="Escola" else 8,col,va="center",ha=ha)
        txt(xpos[0]+6,y+rowh/2+1,f"{rank}",outfitB if hot else mono,9 if hot else 8.5,CORALd if hot else INK,va="center")
        y+=rowh
    footer(hp,"Fonte: Microdados ENEM 2025 / INEP · nomes do Censo Escolar 2025 · escolas com 10+ alunos.",pg)

def p4_rn_list(hp):
    data=RN_TOP+[TER_RN]
    rank_table(hp,"Ranking — Rio Grande do Norte","As 20 melhores médias do RN, mais a posição do Teresa (entre 429 escolas).",
               data,["#","Escola","Cidade","Rede","Alunos","Média"],[0.06,0.44,0.18,0.10,0.10,0.12],"4 / 6",
               hi=pos_rn,sep_before=pos_rn,rowh=23,fs=9)

def p5_parn_list(hp):
    rank_table(hp,"Ranking — Parnamirim (rede privada)",
               f"As {len(parn)} escolas privadas de Parnamirim com 10 ou mais alunos, da maior para a menor média.",
               PARN_ROWS,["#","Escola","Cidade","Rede","Alunos","Média"],[0.06,0.46,0.16,0.10,0.10,0.12],"5 / 6",
               hi=PP,rowh=24,fs=9.5)

# ---------------- p6: metodologia ----------------
def p6_metodo(hp):
    txt=hp["txt"]; rrect=hp["rrect"]
    txt(M,140,"Como esse ranking foi feito",outfitB,17,INK); y=176
    itens=[("Fonte oficial","Microdados do ENEM 2025 (INEP, gov.br/inep) e nomes das escolas no Censo Escolar 2025. Nenhum valor foi estimado ou alterado."),
           ("Escola","Colégio Teresa de Lisieux — Ensino Médio, CO_ESCOLA 24085081, Parnamirim/RN, rede privada. No Censo a entidade do médio consta como “EJAX – Teresa de Lisieux”, mas registra 87 matrículas de Ensino Médio regular (EJA = 0)."),
           ("Quem entra na conta","Alunos presentes nos dois dias, com as 5 notas válidas (LC, CH, CN, MT e Redação), vinculados à escola pelo código CO_ESCOLA. Foram 29 alunos."),
           ("Nota da escola e média do RN","Nota da escola = média simples das notas dos seus alunos. A “média do RN” usada na comparação é a média simples das 429 escolas (cada escola pesa igual) = 516,4 pontos."),
           ("Corte de tamanho","Só entram no ranking escolas com 10 ou mais alunos, para uma turma pequena não distorcer a colocação."),
           ("Ressalva honesta","O microdado não permite separar “concluinte” de “treineiro” no arquivo de notas (o status de conclusão está em outro arquivo que o INEP não deixa cruzar). É a média dos alunos vinculados à escola, não apenas dos formandos de 2025."),
           ("Recortes","Comparações dentro de Parnamirim, de todo o Rio Grande do Norte e da rede privada.")]
    for t,c in itens:
        rrect(M,y,7,7,2,CYAN,z=3); txt(M+18,y+7,t,outfitB,11.5,INK); yy=y+24
        words=c.split(); ln=""; lines=[]
        for w in words:
            if hp["tw"]((ln+" "+w).strip(),outfit,10)>(W-2*M-18): lines.append(ln); ln=w
            else: ln=(ln+" "+w).strip()
        lines.append(ln)
        for L in lines: txt(M+18,yy,L,outfit,10,"#3A3A3D"); yy+=15.5
        y=yy+11
    footer(hp,"Relatório gerado por XTRI · Prof. Alexandre Emerson · dados abertos do INEP.","6 / 6")

D.mkdir(exist_ok=True)
with PdfPages(str(D/"Relatorio_Colegio_Teresa_ENEM2025.pdf")) as pdf:
    for fn,tag in [(p1_resumo,"RELATÓRIO · RANKING ENEM 2025"),(p2_areas,"DESEMPENHO POR ÁREA"),
                   (p3_ranking,"POSIÇÃO NO RANKING"),(p4_rn_list,"RANKING · RIO GRANDE DO NORTE"),
                   (p5_parn_list,"RANKING · PARNAMIRIM (PRIVADAS)"),(p6_metodo,"METODOLOGIA E FONTE")]:
        page(pdf,fn,tag)
print("ok: Relatorio_Colegio_Teresa_ENEM2025.pdf (6 págs)")
print("RNAVG simples:",{k:round(v,1) for k,v in RNAVG.items()})
print("ranks:",{k:RANK[k]["MEDIA5"] for k in RANK})
