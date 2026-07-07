#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Item CH 152715 (Bis<0,01, 2ª aplicação): coleta (nota CH, marcação) de todos os respondentes."""
import csv, json
from pathlib import Path
BASE = Path("/Volumes/Kingston 1/microdados_enem_2025")
POS = {"1539":62,"1540":53,"1541":57,"1542":76,"1543":57,"1544":57,"1545":57,"1546":57,"1548":57,"1579":57}
pares=[]
lidas=0
with (BASE/"DADOS/RESULTADOS_2025.csv").open(encoding="latin-1",newline="") as f:
    for row in csv.DictReader(f,delimiter=";"):
        lidas+=1
        if lidas%1_000_000==0: print(f"  {lidas:,}...",flush=True)
        prova=(row.get("CO_PROVA_CH") or "").strip()
        if prova not in POS or row.get("TP_PRESENCA_CH")!="1": continue
        resp=row.get("TX_RESPOSTAS_CH") or ""
        try: nota=float((row.get("NU_NOTA_CH") or "").replace(",","."))
        except ValueError: continue
        if nota<=0 or not resp: continue
        idx=POS[prova]-46
        if 0<=idx<len(resp):
            ch=resp[idx].upper()
            pares.append([round(nota,1), ch if ch in "ABCDE" else "outros"])
(BASE/"palestra_2025/ch_bis_pares.json").write_text(json.dumps(pares))
print("respondentes:",len(pares))
