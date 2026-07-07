#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Serie historica das MINIMAS e MAXIMAS da nota TRI por area e por ano (ENEM).
Fontes REAIS: 2015-2023 do arquivo do usuario 'TRI ENEM DE 2009 A 2023 MIN MED E MAX.xlsx'
(min = menor nota; max = maior nota, por area/ano); 2024 e 2025 calculados dos microdados INEP."""
import json, os, math
from collections import defaultdict
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT="/Volumes/Kingston 1/microdados_enem_2025/estudo_serie_historica"
XLSX="/Volumes/Kingston/Desktop/TRI ENEM DE 2009 A 2023 MIN MED E MAX.xlsx"
AREAS=["CN","CH","LC","MT"]
ANOME={"CN":"Ciências da Natureza","CH":"Ciências Humanas","LC":"Linguagens e Códigos","MT":"Matemática"}
ACOR ={"CN":"#2E8B57","CH":"#C0504D","LC":"#1F6FB2","MT":"#E08214"}

# --- 1) min/max 2015-2023 do xlsx ---
import openpyxl
wb=openpyxl.load_workbook(XLSX, data_only=True)
ws=wb["resumo2009_2022 (2)"]
mm=defaultdict(lambda:{"min":None,"max":None})
for r in list(ws.iter_rows(values_only=True))[1:]:
    area,ac,mn,mx,med,ano=r[:6]
    if area is None or ano is None: continue
    try: mn=float(mn); mx=float(mx); ano=int(ano)
    except (TypeError,ValueError): continue
    a=str(area).strip().upper()
    if a not in AREAS: continue
    d=mm[(ano,a)]
    if d["min"] is None or mn<d["min"]: d["min"]=mn
    if d["max"] is None or mx>d["max"]: d["max"]=mx

# --- 2) 2024 e 2025 dos JSONs calculados ---
for y in (2024,2025):
    p=os.path.join(OUT,f"minmax_{y}.json")
    if os.path.exists(p):
        j=json.load(open(p))
        for a in AREAS:
            n=j["notas"].get(f"NU_NOTA_{a}")
            if n and n.get("min_pos") is not None:
                mm[(y,a)]={"min":n["min_pos"],"max":n["max"]}

# --- mediana REAL (so anos com microdado individual no disco: 2024, 2025) ---
MED={}
mp=os.path.join(OUT,"mediana_2024_2025.json")
if os.path.exists(mp):
    mj=json.load(open(mp))
    for y in (2024,2025):
        d=mj.get(str(y),{})
        for a in AREAS:
            if d.get(a) is not None: MED[(int(y),a)]=float(d[a])

# --- 3) montar serie 2015..2025 ---
ANOS=list(range(2015,2026))
have2024 = (2024,"MT") in mm
print("anos com dados:", sorted({y for (y,a) in mm if 2015<=y<=2025}))

plt.rcParams.update({"font.size":10})
fig,axes=plt.subplots(2,2,figsize=(13.5,9),dpi=150)
fig.patch.set_facecolor("white")
for ax,a in zip(axes.flat,AREAS):
    ax.set_facecolor("white")
    xs,ymin,ymax=[],[],[]
    for y in ANOS:
        d=mm.get((y,a))
        xs.append(y)
        ymin.append(d["min"] if d else np.nan)
        ymax.append(d["max"] if d else np.nan)
    xs=np.array(xs); ymin=np.array(ymin,float); ymax=np.array(ymax,float)
    col=ACOR[a]
    # banda
    valid=~np.isnan(ymin)&~np.isnan(ymax)
    ax.fill_between(xs, ymin, ymax, where=valid, color=col, alpha=0.13, zorder=1)
    ax.plot(xs, ymax, "-o", color=col, lw=2.4, ms=5, zorder=3, label="máxima")
    ax.plot(xs, ymin, "-o", color=col, lw=2.0, ms=4, alpha=0.6, zorder=3, label="mínima")
    # rotulos de min e max em TODOS os anos
    for y,vmax,vmin in zip(xs,ymax,ymin):
        if np.isnan(vmax): continue
        bold = "bold" if y in (2015,2025) else "normal"
        ax.annotate(f"{vmax:.0f}", (y,vmax), textcoords="offset points", xytext=(0,7), ha="center", fontsize=7.2, color=col, weight=bold)
        ax.annotate(f"{vmin:.0f}", (y,vmin), textcoords="offset points", xytext=(0,-12), ha="center", fontsize=7.0, color=col, weight=bold)
    # destaca 2025
    d25=mm.get((2025,a))
    if d25:
        ax.scatter([2025,2025],[d25["max"],d25["min"]], s=80, facecolor="white", edgecolor=col, lw=2, zorder=4)
    ax.set_title(ANOME[a], fontsize=13, weight="bold", color="#1F4E78")
    ax.set_xlim(2014.4,2025.6); ax.set_xticks(range(2015,2026))
    ax.set_xticklabels([str(y) for y in range(2015,2026)], rotation=45, fontsize=8.5)
    ax.set_ylim(np.nanmin(ymin)-55, np.nanmax(ymax)+55)
    ax.set_ylabel("Nota TRI", fontsize=9.5)
    ax.grid(axis="y", color="#EEE", lw=0.7); ax.set_axisbelow(True)
    for s in ["top","right"]: ax.spines[s].set_visible(False)
    amp_hi=int(np.nanmax(ymax)); amp_lo=int(np.nanmin(ymin))
    teto_amp=int(np.nanmax(ymax))-int(np.nanmin([v for v in ymax if not np.isnan(v)]))
    ax.text(0.5,0.50,f"amplitude do teto: {teto_amp} pts\nfaixa usada: {amp_lo}–{amp_hi}",
            transform=ax.transAxes, ha="center", va="center", fontsize=8.0, color="#9a9a9a")
    if not have2024:
        ax.axvspan(2023.5,2024.5, color="#bbbbbb", alpha=0.10, zorder=0)

fig.suptitle("ENEM — mínimas e máximas da nota TRI por edição (2015–2025)", fontsize=17, weight="bold", color="#1F4E78", y=0.985)
fig.text(0.5,0.945,"Cada faixa mostra o piso e o teto da escala TRI efetivamente alcançados em cada prova. O teto varia de ano para ano porque a TRI é calibrada por edição.",
         ha="center", fontsize=10, color="#555")
# rodapé: fonte preservada + nota da mediana + contato/site/autor
fig.text(0.5,0.040,"Fontes: min/máx 2015–2023 (arquivo XTRI a partir dos microdados INEP)  ·  2024–2025 microdados INEP",
         ha="center", fontsize=8.0, color="#888")
fig.text(0.5,0.013,"contato@xtri.online    ·    xtri.online    ·    estudo por Alexandre Emerson Melo de Araújo",
         ha="center", fontsize=9.2, color="#1F4E78", weight="bold")
fig.tight_layout(rect=[0,0.060,1,0.93])
# marca d'água XTRI (logo, faint, centro da figura)
try:
    from PIL import Image
    lg=Image.open("/Volumes/Kingston 1/microdados_enem_2025/logo_xtri_marca_real.png").convert("RGBA")
    w0=380; lg=lg.resize((w0,int(w0*lg.size[1]/lg.size[0])))
    arr=np.asarray(lg).astype(float)/255.0; arr[...,3]*=0.08
    fw,fh=(fig.get_size_inches()*fig.dpi)
    fig.figimage(arr, xo=(fw-arr.shape[1])/2.0, yo=(fh-arr.shape[0])/2.0, zorder=10)
except Exception as e:
    print("watermark falhou:", e)
out=os.path.join(OUT,"SERIE_minmax_TRI_2015_2025.png")
fig.savefig(out, facecolor="white"); print("OK ->", out)
# tabela resumo
print("\nano  " + "  ".join(f"{a:>11}" for a in AREAS))
for y in ANOS:
    cells=[]
    for a in AREAS:
        d=mm.get((y,a)); cells.append(f"{d['min']:.0f}-{d['max']:.0f}" if d else "   --   ")
    print(f"{y}  " + "  ".join(f"{c:>11}" for c in cells))
