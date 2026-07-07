#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, re, csv
PB="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/PROVAS E GABARITOS"
PDF={"D1":f"{PB}/ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf","D2":f"{PB}/ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf"}
def pmap(pdf):
    txt=subprocess.run(["pdftotext",pdf,"-"],capture_output=True).stdout.decode("utf-8","ignore")
    pages=txt.split("\f"); m={}
    for pi,pg in enumerate(pages,1):
        for mm in re.finditer(r"quest[ãa]o\s*0*(\d{1,3})", pg, re.I):
            q=int(mm.group(1)); m.setdefault(q,pi)
    return m,len(pages)
M={}; npages={}
for k,p in PDF.items():
    mm,n=pmap(p); M[k]=mm; npages[k]=n
print("paginas: D1=",npages["D1"]," D2=",npages["D2"])
rows=list(csv.DictReader(open("/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/estudo_polemicas_tri/ranking_polemica_TRI.csv")))
def pdfkey(area): return "D1" if area in ("LC","CH") else "D2"
print("\nCANDIDATAS (top 10/area) -> pagina no caderno Azul:")
for ar in ["CN","MT","LC","CH"]:
    print(f"\n## {ar} ({'Dia2' if ar in ('CN','MT') else 'Dia1'})")
    for r in [x for x in rows if x["area"]==ar][:10]:
        q=int(r["pos_azul"]) if r["pos_azul"] else 0
        pg=M[pdfkey(ar)].get(q,"?")
        print(f'  IPT{r["IPT"]:>5} Q{q:>3} pg{pg:>3} it{r["CO_ITEM"]} hab{r["hab"]} a={r["a"]} b={r["b"]} c={r["c"]} p={r["p_obs"]} mis={r["misfit"]}')
