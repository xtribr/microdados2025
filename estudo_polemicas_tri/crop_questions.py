#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recorta a regiao de cada questao do PDF do caderno (2 colunas) usando bbox de palavras."""
import subprocess, re, os
from PIL import Image
PB="/sessions/brave-sharp-fermi/mnt/microdados_enem_2025/PROVAS E GABARITOS"
PDF={"D1":f"{PB}/ENEM_2025_P1_CAD_01_DIA_1_AZUL.pdf","D2":f"{PB}/ENEM_2025_P1_CAD_07_DIA_2_AZUL.pdf"}
OUT="/sessions/brave-sharp-fermi/mnt/outputs/crops"; os.makedirs(OUT,exist_ok=True)
DPI=200

def words_page(pdf,page):
    xml=subprocess.run(["pdftotext","-bbox","-f",str(page),"-l",str(page),pdf,"-"],
                       capture_output=True).stdout.decode("utf-8","ignore")
    pw=re.search(r'<page width="([\d.]+)" height="([\d.]+)"',xml)
    W,H=float(pw.group(1)),float(pw.group(2))
    ws=[]
    for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',xml):
        ws.append((float(m.group(1)),float(m.group(2)),float(m.group(3)),float(m.group(4)),m.group(5)))
    return W,H,ws

def headers(ws,W):
    hs=[]
    for i,(x0,y0,x1,y1,t) in enumerate(ws):
        if re.match(r'quest[ãa]o',t,re.I):
            # proximo token numero
            num=None
            for j in range(i+1,min(i+3,len(ws))):
                mm=re.match(r'0*(\d{1,3})$',ws[j][4])
                if mm: num=int(mm.group(1)); break
            if num: hs.append((num,x0,y0))
    return hs

def crop(pdfkey,page,qnum,outname):
    pdf=PDF[pdfkey]; W,H,ws=words_page(pdf,page); hs=headers(ws,W)
    tgt=[h for h in hs if h[0]==qnum]
    if not tgt: print(f"  !! Q{qnum} header nao achado p{page}"); return None
    _,hx,hy=tgt[0]
    col_left = hx < W/2
    xs0,xs1 = (0.045*W, 0.490*W) if col_left else (0.505*W, 0.915*W)
    # proximo header na mesma coluna abaixo (evita rodape/numero de pagina)
    ybot=H-0.075*H
    for (n,x,y) in hs:
        same = (x<W/2)==col_left
        if same and y>hy+5 and y<ybot: ybot=y
    ytop=max(0, hy-0.008*H)
    # render pagina e recorta
    pref=f"{OUT}/_pg_{pdfkey}_{page}"
    subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-r",str(DPI),"-png",pdf,pref],
                   capture_output=True)
    img=[f for f in os.listdir(OUT) if f.startswith(f"_pg_{pdfkey}_{page}")][0]
    im=Image.open(f"{OUT}/{img}"); s=DPI/72.0
    box=(int(xs0*s),int(ytop*s),int(xs1*s),int(ybot*s))
    cr=im.crop(box); cr.save(f"{OUT}/{outname}.png")
    print(f"  Q{qnum} p{page} {'L' if col_left else 'R'} -> {outname}.png  {cr.size}")
    return f"{OUT}/{outname}.png"

# (pdfkey, pagina, qnum, nome)
SEL=[("D2",3,96,"01_biologia_Q96"),("D2",4,100,"02_quimica_Q100"),("D2",10,122,"03_fisica_Q122"),
     ("D2",19,146,"04_matbasica_Q146"),("D2",18,139,"05_geometria_Q139"),
     ("D1",9,16,"06_literatura_Q16"),("D1",9,15,"07_artes_Q15"),("D1",15,35,"08_interpretacao_Q35"),
     ("D1",24,53,"09_historia_Q53"),("D1",26,63,"10_geografia_Q63")]
for k,pg,q,name in SEL: crop(k,pg,q,name)
print("DONE")
