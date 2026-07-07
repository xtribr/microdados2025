#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Indice de Polemica TRI (IPT) — itens REGULARES (P1).
Fontes reais: dificuldade_consolidado.json (a,b,c,p por CO_ITEM) + ITENS_PROVA_2025.csv (posicao no caderno Azul)."""
import json, csv, math, os
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"
J=json.load(open(f"{BASE}/analises_primi_2025_cop30/outputs/dificuldade_consolidado.json"))
items=J["items"]

# --- posicao/gabarito no caderno AZUL regular (CO_PROVA: CH1447 LC1459 CN1483 MT1471) ---
AZUL={"CH":"1447","LC":"1459","CN":"1483","MT":"1471"}
pos={}  # CO_ITEM -> (posicao, gabarito) no Azul
with open(f"{BASE}/DADOS/ITENS_PROVA_2025.csv", encoding="latin-1") as f:
    r=csv.reader(f,delimiter=';'); h=next(r)
    iPOS,iAREA,iITEM,iGAB,iCOR,iPROVA,iLING=0,1,2,3,10,11,12
    for row in r:
        if row[iCOR]=="AZUL" and row[iPROVA]==AZUL.get(row[iAREA],""):
            # LC: pegar a versao base (lingua vazia) p/ posicao; itens 1-5 sao lingua
            pos.setdefault(row[iITEM],(row[iPOS],row[iGAB]))

def Ppred(a,b,c):
    # proporcao de acerto prevista pelo 3PL (D=1) integrando theta~N(0,1)
    s=0.0; n=0
    x=-4.0
    while x<=4.0001:
        w=math.exp(-x*x/2)/math.sqrt(2*math.pi)
        p=c+(1-c)/(1+math.exp(-a*(x-b)))
        s+=w*p; n+=1; x+=0.02
    # normaliza pelos pesos (passo constante)
    # soma dos pesos ~ integral da normal no grid
    return s/ (sum(math.exp(-(xx)*(xx)/2)/math.sqrt(2*math.pi) for xx in [ -4+0.02*k for k in range(0,int(8/0.02)+1)]))

rows=[]
for co,d in items.items():
    if d.get("aban"): continue
    a,b,c,p=d["A"],d["B"],d["C"],d["p"]
    Pp=Ppred(a,b,c)
    misfit=abs(p-Pp)
    posg=pos.get(co,("",""))
    rows.append(dict(co=co,area=d["area"],hab=d["hab"],a=a,b=b,c=c,p=p,Pp=Pp,
                     misfit=misfit,pos=posg[0],gab=posg[1],acertos=d.get("acertos"),total=d.get("total")))

n=len(rows)
def pct_rank(vals):
    order=sorted(range(len(vals)),key=lambda i:vals[i])
    pr=[0.0]*len(vals)
    for rank,i in enumerate(order): pr[i]=100.0*rank/(len(vals)-1)
    return pr
# componentes: baixa discriminacao (-a), chute alto (c), desajuste (misfit)
pa=pct_rank([-x["a"] for x in rows])     # a baixo -> percentil alto
pc=pct_rank([x["c"] for x in rows])      # c alto -> percentil alto
pm=pct_rank([x["misfit"] for x in rows]) # misfit alto -> percentil alto
for i,x in enumerate(rows):
    x["pa"]=pa[i]; x["pc"]=pc[i]; x["pm"]=pm[i]
    x["IPT"]=round((pa[i]+pc[i]+pm[i])/3,1)

rows.sort(key=lambda x:-x["IPT"])
os.makedirs(f"{BASE}/estudo_polemicas_tri",exist_ok=True)
out=f"{BASE}/estudo_polemicas_tri/ranking_polemica_TRI.csv"
with open(out,"w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["rank","CO_ITEM","area","hab","pos_azul","gab","a","b","c","p_obs","P_pred","misfit","pctA(disc)","pctC(chute)","pctMisfit","IPT"])
    for k,x in enumerate(rows,1):
        w.writerow([k,x["co"],x["area"],x["hab"],x["pos"],x["gab"],
                    f'{x["a"]:.3f}',f'{x["b"]:.3f}',f'{x["c"]:.3f}',f'{x["p"]:.3f}',f'{x["Pp"]:.3f}',
                    f'{x["misfit"]:.3f}',f'{x["pa"]:.0f}',f'{x["pc"]:.0f}',f'{x["pm"]:.0f}',x["IPT"]])
print(f"itens avaliados={n} (regular, nao-anulados) | csv salvo")
print("\n=== TOP 20 IPT (geral) ===")
print(f'{"#":>2} {"item":>7} {"ar":>2} {"h":>2} {"pos":>3} {"a":>5} {"b":>6} {"c":>5} {"p":>5} {"Pp":>5} {"mis":>5} {"IPT":>5}')
for k,x in enumerate(rows[:20],1):
    print(f'{k:>2} {x["co"]:>7} {x["area"]:>2} {x["hab"]:>2} {x["pos"]:>3} {x["a"]:>5.2f} {x["b"]:>6.2f} {x["c"]:>5.2f} {x["p"]:>5.2f} {x["Pp"]:>5.2f} {x["misfit"]:>5.2f} {x["IPT"]:>5.1f}')
print("\n=== TOP 6 por AREA ===")
for ar in ["CN","MT","LC","CH"]:
    sub=[x for x in rows if x["area"]==ar][:6]
    print(f"-- {ar} --")
    for x in sub:
        print(f'  item {x["co"]} pos{x["pos"]} hab{x["hab"]} a={x["a"]:.2f} b={x["b"]:.2f} c={x["c"]:.2f} p={x["p"]:.2f} Pp={x["Pp"]:.2f} mis={x["misfit"]:.2f} IPT={x["IPT"]}')
