#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mediana real da nota TRI por area, 2024 e 2025 (unica fonte com microdado individual no disco).
Histograma bin=1 -> mediana. Streaming."""
import csv, json, sys
csv.field_size_limit(10_000_000)
FILES={
 2024:("/Volumes/HD/apps/RANKING ENEM/microdados-2024/MICRODADOS_ENEM_2024.csv", {"CN":22,"CH":23,"LC":24,"MT":25}),
 2025:("/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv",       {"CN":22,"CH":23,"LC":24,"MT":25}),
}
NB=1101
def fnum(s):
    s=s.strip().replace(",",".")
    if not s: return None
    try: return float(s)
    except ValueError: return None
out={}
for year,(path,idx) in FILES.items():
    hist={a:[0]*NB for a in idx}; n=0
    with open(path, encoding="latin-1", newline="") as fh:
        rd=csv.reader(fh, delimiter=";"); next(rd)
        for row in rd:
            n+=1
            for a,i in idx.items():
                if i<len(row):
                    v=fnum(row[i])
                    if v and v>0:
                        b=int(round(v))
                        if 0<=b<NB: hist[a][b]+=1
            if n%1_000_000==0: print(f"[{year}] {n:,}", file=sys.stderr, flush=True)
    med={}
    for a in idx:
        tot=sum(hist[a][a2] for a2 in range(NB)); half=tot/2; c=0; m=None
        for b in range(NB):
            c+=hist[a][b]
            if c>=half: m=b; break
        med[a]=m
    out[str(year)]=med
    print(f"[{year}] mediana:", med)
json.dump(out, open("/Volumes/Kingston 1/microdados_enem_2025/estudo_serie_historica/mediana_2024_2025.json","w"))
print("OK")
