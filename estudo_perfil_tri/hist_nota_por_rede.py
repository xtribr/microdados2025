#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Histograma da nota TRI por (area x rede) — 1 passada streaming sobre RESULTADOS.
Para o overlay E1 (densidade por rede sob a curva de informacao)."""
import csv, sys, json
PATH = "/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv"
I = dict(DEP=7, CN=22, CH=23, LC=24, MT=25)
AREAS = ["CN","CH","LC","MT"]
REDES = ["1","2","3","4"]
BINW = 2.0; NB = 525  # 0..1050
# hist[area][rede] = list de contagens
hist = {a:{r:[0]*NB for r in REDES} for a in AREAS}
n=0
def fnum(s):
    if not s: return None
    s=s.strip().replace(",",".")
    if not s: return None
    try: return float(s)
    except ValueError: return None
with open(PATH, encoding="latin-1", newline="") as fh:
    rd=csv.reader(fh, delimiter=";")
    next(rd)
    for row in rd:
        n+=1
        try: dep=row[I["DEP"]].strip()
        except IndexError: continue
        if dep not in REDES: continue
        for a in AREAS:
            v=fnum(row[I[a]])
            if v is None or v<=0: continue
            b=int(v//BINW)
            if 0<=b<NB: hist[a][dep][b]+=1
        if n%500000==0: print(f"... {n:,}", file=sys.stderr, flush=True)
def median_from_hist(counts):
    tot=sum(counts)
    if tot==0: return None
    half=tot/2; c=0
    for i,k in enumerate(counts):
        c+=k
        if c>=half: return round((i+0.5)*BINW,1)
    return None
out={"binw":BINW,"nb":NB,"areas":AREAS,"redes":REDES,
     "hist":hist,
     "totais":{a:{r:sum(hist[a][r]) for r in REDES} for a in AREAS},
     "medianas":{a:{r:median_from_hist(hist[a][r]) for r in REDES} for a in AREAS}}
p="/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/eea62195-d399-4434-8338-95d5d92b8bac/scratchpad/hist_nota_rede.json"
json.dump(out, open(p,"w"))
print("OK", p)
print("medianas:", json.dumps(out["medianas"], ensure_ascii=False))
print("totais:", json.dumps(out["totais"], ensure_ascii=False))
