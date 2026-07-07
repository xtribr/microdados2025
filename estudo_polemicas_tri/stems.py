#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, re
PB="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/PROVAS E GABARITOS"
D1=f"{PB}/ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf"; D2=f"{PB}/ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf"
def qtext(pdf):
    raw=subprocess.run(["pdftotext",pdf,"-"],capture_output=True).stdout.decode("utf-8","ignore")
    raw=re.sub(r"[ \t]+"," ",raw)
    # split por marcador de questao
    parts=re.split(r"(Quest[ãa]o\s*0*\d{1,3})", raw)
    out={}
    for i in range(1,len(parts),2):
        mm=re.search(r"(\d{1,3})",parts[i]); q=int(mm.group(1))
        body=re.sub(r"\s+"," ",parts[i+1]).strip() if i+1<len(parts) else ""
        if q not in out or len(out[q])<len(body): out[q]=body
    return out
Q={}; Q.update(qtext(D1)); Q.update(qtext(D2))
want={"CN":[96,98,100,101,106,109,119,122,130],"MT":[139,141,143,146,150,159,163,165],
      "LC":[7,15,16,19,24,35,41,45],"CH":[49,53,56,57,61,63,65,71,77,81]}
for ar,qs in want.items():
    print(f"\n================= {ar} =================")
    for q in qs:
        t=Q.get(q,"")[:430]
        print(f"\n--- Q{q} ---\n{t}")
