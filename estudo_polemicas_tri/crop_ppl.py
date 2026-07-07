#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, re, os
from PIL import Image
PB="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/PROVAS E GABARITOS"
PDF={"P2D1":f"{PB}/ENEM_2025_P2_CAD_01_DIA_1_AZUL.pdf","P2D2":f"{PB}/ENEM_2025_P2_CAD_07_DIA_2_AZUL.pdf"}
OUT="/sessions/brave-sharp-fermi/mnt/outputs/crops"; DPI=200
def words(pdf,page):
    xml=subprocess.run(["pdftotext","-bbox","-f",str(page),"-l",str(page),pdf,"-"],capture_output=True).stdout.decode("utf-8","ignore")
    pw=re.search(r'<page width="([\d.]+)" height="([\d.]+)"',xml); W,H=float(pw.group(1)),float(pw.group(2))
    ws=[(float(a),float(b),float(c),float(d),e) for a,b,c,d,e in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',xml)]
    return W,H,ws
def headers(ws):
    hs=[]
    for i,(x0,y0,x1,y1,t) in enumerate(ws):
        if re.match(r'quest[ãa]o',t,re.I):
            for j in range(i+1,min(i+3,len(ws))):
                m=re.match(r'0*(\d{1,3})$',ws[j][4])
                if m: hs.append((int(m.group(1)),x0,y0)); break
    return hs
def crop(key,page,q,out):
    pdf=PDF[key]; W,H,ws=words(pdf,page); hs=headers(ws)
    t=[h for h in hs if h[0]==q][0]; _,hx,hy=t; left=hx<W/2
    xs0,xs1=(0.045*W,0.490*W) if left else (0.505*W,0.915*W)
    ybot=H-0.075*H
    for n,x,y in hs:
        if (x<W/2)==left and y>hy+5 and y<ybot: ybot=y
    ytop=max(0,hy-0.008*H)
    pref=f"{OUT}/_pgp_{key}_{page}"; subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-r",str(DPI),"-png",pdf,pref],capture_output=True)
    img=[f for f in os.listdir(OUT) if f.startswith(f"_pgp_{key}_{page}")][0]
    im=Image.open(f"{OUT}/{img}"); s=DPI/72.0
    im.crop((int(xs0*s),int(ytop*s),int(xs1*s),int(ybot*s))).save(f"{OUT}/{out}.png")
    print("ok",out, "page",page,"L" if left else "R")
crop("P2D2",4,98,"PPL01_biologia_Q98")
crop("P2D1",29,79,"PPL02_ch_Q79")
