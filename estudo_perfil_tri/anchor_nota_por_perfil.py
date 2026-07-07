#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anchor empírico: nota média TRI por dimensões de PERFIL que VIVEM em RESULTADOS
(joináveis com a nota, mesma linha) — tipo de escola, localização, UF, língua.
Uma única passada streaming sobre RESULTADOS_2025.csv (~2.1 GB).
Respeita a trava: NÃO toca em PARTICIPANTES (renda/raça/sexo não cruzam nota)."""
import csv, sys, json
from collections import defaultdict

PATH = "/Volumes/Kingston 1/microdados_enem_2025/DADOS/RESULTADOS_2025.csv"

# índices (0-based) conferidos no header
I = dict(DEP=7, LOC=8, UFESC=6, UFPROVA=13, CN=22, CH=23, LC=24, MT=25, LING=30, RED=41)
AREAS = ["CN","CH","LC","MT","RED"]

def fnum(s):
    if not s: return None
    s = s.strip().replace(",", ".")
    if s == "" : return None
    try:
        v = float(s)
    except ValueError:
        return None
    return v

# acumuladores: chave -> area -> [soma, n]
def newacc(): return {a:[0.0,0] for a in AREAS}
by_dep   = defaultdict(newacc)
by_loc   = defaultdict(newacc)
by_uf    = defaultdict(newacc)   # UF da PROVA
by_ling  = defaultdict(newacc)   # só LC interessa
overall  = newacc()
n_rows = 0
n_with_school = 0

with open(PATH, encoding="latin-1", newline="") as fh:
    rd = csv.reader(fh, delimiter=";")
    header = next(rd)
    for row in rd:
        n_rows += 1
        try:
            dep  = row[I["DEP"]].strip()
            loc  = row[I["LOC"]].strip()
            uf   = row[I["UFPROVA"]].strip()
            ling = row[I["LING"]].strip()
        except IndexError:
            continue
        if dep:
            n_with_school += 1
        vals = {a: fnum(row[I[a]]) for a in AREAS}
        for a in AREAS:
            v = vals[a]
            if v is None:
                continue
            # nota objetiva 0 = ausência/anômalo -> ignorar p/ média de presentes; redação 0 é real
            if a != "RED" and v <= 0:
                continue
            s_n = overall[a]; s_n[0]+=v; s_n[1]+=1
            if dep:
                d=by_dep[dep][a]; d[0]+=v; d[1]+=1
                l=by_loc[loc][a]; l[0]+=v; l[1]+=1
            if uf:
                u=by_uf[uf][a]; u[0]+=v; u[1]+=1
            if a=="LC" and ling in ("0","1"):
                g=by_ling[ling][a]; g[0]+=v; g[1]+=1
        if n_rows % 500000 == 0:
            print(f"... {n_rows:,} linhas", file=sys.stderr, flush=True)

def summarize(acc):
    out={}
    for k,areas in acc.items():
        out[k]={a:(round(s/n,1) if n else None, n) for a,(s,n) in areas.items()}
    return out

result = {
    "n_rows": n_rows,
    "n_with_school": n_with_school,
    "pct_with_school": round(100*n_with_school/n_rows,1),
    "overall": {a:(round(s/n,1) if n else None, n) for a,(s,n) in overall.items()},
    "by_dependencia": summarize(by_dep),   # 1 fed 2 est 3 mun 4 priv
    "by_localizacao": summarize(by_loc),   # 1 urbana 2 rural
    "by_lingua": summarize(by_ling),       # 0 ing 1 esp (LC)
    "by_uf_prova": summarize(by_uf),
}
out_path = "/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/eea62195-d399-4434-8338-95d5d92b8bac/scratchpad/anchor_perfil_tri.json"
json.dump(result, open(out_path,"w"), ensure_ascii=False, indent=2)
print("OK ->", out_path)
print("linhas:", n_rows, "| com escola:", n_with_school, f"({result['pct_with_school']}%)")
print("DEP médias (CN,CH,LC,MT,RED):")
for k in sorted(by_dep):
    a=result["by_dependencia"][k]
    print(f"  dep={k}: " + " ".join(f"{x}={a[x][0]}(n={a[x][1]})" for x in AREAS))
print("LINGUA LC:", {k: result['by_lingua'][k]['LC'] for k in result['by_lingua']})
