#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dificuldade por sequencia — PPL / 2a aplicacao (caderno Azul).
Sem taxa de acerto observada (INEP nao divulga p/ PPL): DIF e acerto vem do MODELO 3PL (a,b,c reais).
DIF_TRI = 100*(1-P(theta=0)); acerto_esperado = 100*P(theta=0) do aluno mediano."""
import csv, math, json, os
BASE="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025"
OUT=f"{BASE}/estudo_dificuldade_ppl"; os.makedirs(OUT,exist_ok=True)
CODES={"CH":("1539",45),"LC":("1549",0),"MT":("1559",135),"CN":("1569",90)}

raw={a:{} for a in CODES}
with open(f"{BASE}/DADOS/ITENS_PROVA_2025.csv",encoding="latin-1") as f:
    r=csv.reader(f,delimiter=';'); next(r)
    for row in r:
        if row[10]!="AZUL": continue
        for ar,(code,off) in CODES.items():
            if row[11]==code:
                pos=int(row[0])-off; ling=row[12]
                # LC lingua: posicoes 1-5 tem ingles(0)/espanhol(1) -> usa ingles(0); demais ling vazio
                if pos in raw[ar] and ling=="1": continue
                aban = row[5]=="1" or row[7]==""
                rec=dict(pos=pos,hab="H"+row[4],aban=aban)
                if not aban:
                    a,b,c=float(row[7]),float(row[8]),float(row[9])
                    P0=c+(1-c)/(1+math.exp(a*b))
                    rec.update(a=a,b=b,c=c,dif=100*(1-P0),esp=100*P0,
                               tier=("A+" if a>=2.5 else "A" if a>=1.35 else "A-"))
                raw[ar][pos]=rec

CAT=["Fácil","Médio","Difícil","Muito difícil"]
data={}
for ar in CODES:
    items=[raw[ar][p] for p in sorted(raw[ar])]
    valid=[x for x in items if not x["aban"]]
    difs=sorted(x["dif"] for x in valid)
    import statistics as st
    q=[difs[int(len(difs)*k/4)] for k in range(1,4)]  # cortes de quartil
    def cat(d):
        return CAT[0] if d<=q[0] else CAT[1] if d<=q[1] else CAT[2] if d<=q[2] else CAT[3]
    for x in valid: x["cat"]=cat(x["dif"])
    dist={c:sum(1 for x in valid if x["cat"]==c) for c in CAT}
    data[ar]=dict(items=items, media_a=st.mean(x["a"] for x in valid),
                  media_dif=st.mean(x["dif"] for x in valid), n_valid=len(valid),
                  n_aban=sum(1 for x in items if x["aban"]), dist=dist)

json.dump(data,open(f"{OUT}/ppl_sequencia_data.json","w"),ensure_ascii=False,indent=1)
with open(f"{OUT}/ppl_sequencia_dificuldade.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["area","pos_area","habilidade","aban","a","b","DIF_TRI","acerto_esperado_θ0","tier","categoria"])
    for ar in CODES:
        for x in data[ar]["items"]:
            if x["aban"]: w.writerow([ar,x["pos"],x["hab"],"SIM","","","","","",""])
            else: w.writerow([ar,x["pos"],x["hab"],"",f'{x["a"]:.3f}',f'{x["b"]:.3f}',
                              f'{x["dif"]:.0f}',f'{x["esp"]:.0f}',x["tier"],x["cat"]])
for ar in CODES:
    d=data[ar]; print(f"{ar}: {d['n_valid']} validas, {d['n_aban']} anuladas, A medio {d['media_a']:.2f}, DIF medio {d['media_dif']:.0f}, dist={d['dist']}")
print("salvo JSON + CSV")
