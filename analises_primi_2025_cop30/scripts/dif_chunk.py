#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Processa UM bloco de bytes do RESULTADOS_2025.csv. Uso: dif_chunk.py K NK"""
import csv, json, sys, os, time
from collections import defaultdict

K  = int(sys.argv[1]); NK = int(sys.argv[2])
BASE = "/sessions/funny-kind-hawking/mnt/microdados_enem_2025/DADOS"
OUT  = "/sessions/funny-kind-hawking/mnt/microdados_enem_2025/analises_primi_2025_cop30/outputs"
ITENS= os.path.join(BASE,"ITENS_PROVA_2025.csv")
RES  = os.path.join(BASE,"RESULTADOS_2025.csv")

REG = {'CN':{'1483','1484','1485','1486'},'CH':{'1447','1448','1449','1450'},
       'LC':{'1459','1460','1461','1462'},'MT':{'1471','1472','1473','1474'}}
BASE_POS={'LC':1,'CH':46,'CN':91,'MT':136}

def fnum(s):
    s=(s or '').strip().replace(',','.')
    try:return float(s)
    except:return None

# itens
item_info={}; raw=defaultdict(list)
with open(ITENS,encoding='latin-1') as f:
    for row in csv.DictReader(f,delimiter=';'):
        a=row['SG_AREA'];p=row['CO_PROVA'];item=row['CO_ITEM']
        aban=row['IN_ITEM_ABAN']=='1'
        item_info[item]={'area':a,'hab':row['CO_HABILIDADE'],'A':fnum(row['NU_PARAM_A']),
                         'B':fnum(row['NU_PARAM_B']),'C':fnum(row['NU_PARAM_C']),'aban':aban}
        raw[(a,p)].append({'pos':int(row['CO_POSICAO']),'item':item,'gab':row['TX_GABARITO'],'ling':row['TP_LINGUA'],'aban':aban})

# slots por (area,prova): 45 entradas. gab em bytes.
slots={}
for (a,p),rows in raw.items():
    if a not in REG or p not in REG[a]: continue
    base=BASE_POS[a]; sl=[None]*45
    if a!='LC':
        for rw in rows:
            i=rw['pos']-base
            if 0<=i<45: sl[i]=('S',rw['item'],rw['gab'].encode(),rw['aban'])
    else:
        lang=defaultdict(dict)
        for rw in rows:
            if rw['ling'] in ('0','1'): lang[rw['pos']][rw['ling']]=rw
        for rw in rows:
            if rw['ling']=='':
                i=rw['pos']-1
                if 0<=i<45: sl[i]=('S',rw['item'],rw['gab'].encode(),rw['aban'])
        for pos in range(1,6):
            d={}
            for ln in ('0','1'):
                if ln in lang.get(pos,{}):
                    rw=lang[pos][ln]; d[ln.encode()]=(rw['item'],rw['gab'].encode(),rw['aban'])
            sl[pos-1]=('L',d)
    slots[(a,p)]=sl

# header -> indices
with open(RES,'rb') as f:
    header=f.readline().rstrip(b'\n').split(b';')
idx={c.decode():i for i,c in enumerate(header)}
iPres={a:idx['TP_PRESENCA_'+a] for a in REG}
iProva={a:idx['CO_PROVA_'+a] for a in REG}
iResp={a:idx['TX_RESPOSTAS_'+a] for a in REG}
iLing=idx['TP_LINGUA']
REGb={a:set(x.encode() for x in REG[a]) for a in REG}
slotsb={(a.encode(),p.encode()):v for (a,p),v in slots.items()}
areasb=[(a,a.encode()) for a in REG]

size=os.path.getsize(RES)
start=K*size//NK; end=(K+1)*size//NK
agg=defaultdict(lambda:[0,0]); present=defaultdict(int)
t0=time.time(); n=0
with open(RES,'rb') as f:
    if K==0:
        f.readline()  # header
    else:
        f.seek(start); f.readline()  # descarta linha parcial
    while True:
        line=f.readline()
        if not line: break
        n+=1
        c=line.rstrip(b'\n').split(b';')
        if len(c)<len(header):
            if f.tell()>=end: break
            continue
        ling=c[iLing]
        for a,ab in areasb:
            if c[iPres[a]]!=b'1': continue
            if c[iProva[a]] not in REGb[a]: continue
            sl=slotsb.get((ab,c[iProva[a]]))
            if sl is None: continue
            resp=c[iResp[a]]
            if len(resp)<45: continue
            present[a]+=1
            for i in range(45):
                s=sl[i]
                if s is None: continue
                if s[0]=='S':
                    _,item,gab,aban=s
                    if aban: continue
                    e=agg[item]; e[1]+=1
                    if resp[i]==gab[0]: e[0]+=1
                else:
                    rw=s[1].get(ling)
                    if rw is None: continue
                    item,gab,aban=rw
                    if aban: continue
                    e=agg[item]; e[1]+=1
                    if resp[i]==gab[0]: e[0]+=1
        if f.tell()>=end: break

part={'K':K,'NK':NK,'n_linhas':n,'present':dict(present),
      'agg':{k:v for k,v in agg.items()},'secs':round(time.time()-t0,1)}
with open(os.path.join(OUT,f"dif_part_{K}.json"),'w') as f:
    json.dump(part,f)
print(f"chunk {K}/{NK} linhas={n} secs={part['secs']} present={dict(present)}")
