#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai min/max (e media) das notas TRI de um CSV de microdados ENEM de qualquer ano.
Streaming, latin-1, ';'. Acha as colunas NU_NOTA_* pelo nome (robusto entre anos)."""
import csv, sys, json
csv.field_size_limit(10_000_000)

def fnum(s):
    if s is None: return None
    s=s.strip()
    if not s: return None
    s=s.replace(",", ".")
    try: return float(s)
    except ValueError: return None

def main():
    path, year, out = sys.argv[1], sys.argv[2], sys.argv[3]
    NOTAS=["NU_NOTA_CN","NU_NOTA_CH","NU_NOTA_LC","NU_NOTA_MT","NU_NOTA_REDACAO"]
    with open(path, encoding="latin-1", newline="") as fh:
        rd=csv.reader(fh, delimiter=";")
        header=next(rd)
        idx={c:(header.index(c) if c in header else None) for c in NOTAS}
        print(f"[{year}] cols achadas:", {k:v for k,v in idx.items()}, flush=True)
        acc={c:{"max":None,"min_all":None,"min_pos":None,"sum":0.0,"n":0,"sum_pos":0.0,"n_pos":0} for c in NOTAS}
        nrow=0
        for row in rd:
            nrow+=1
            for c in NOTAS:
                i=idx[c]
                if i is None or i>=len(row): continue
                v=fnum(row[i])
                if v is None: continue
                a=acc[c]
                a["n"]+=1; a["sum"]+=v
                if a["max"] is None or v>a["max"]: a["max"]=v
                if a["min_all"] is None or v<a["min_all"]: a["min_all"]=v
                if v>0:
                    a["n_pos"]+=1; a["sum_pos"]+=v
                    if a["min_pos"] is None or v<a["min_pos"]: a["min_pos"]=v
            if nrow%1_000_000==0: print(f"[{year}] ... {nrow:,} linhas", file=sys.stderr, flush=True)
    res={"year":int(year),"nrows":nrow,"notas":{}}
    for c in NOTAS:
        a=acc[c]
        res["notas"][c]={
            "max": a["max"], "min_all": a["min_all"], "min_pos": a["min_pos"],
            "n": a["n"], "n_pos": a["n_pos"],
            "mean_pos": round(a["sum_pos"]/a["n_pos"],1) if a["n_pos"] else None,
        }
    json.dump(res, open(out,"w"), ensure_ascii=False, indent=2)
    print(f"[{year}] OK -> {out}")
    for c in NOTAS:
        n=res["notas"][c]
        print(f"   {c:16} min(>0)={n['min_pos']}  max={n['max']}  media={n['mean_pos']}  n>0={n['n_pos']:,}")

if __name__=="__main__":
    main()
