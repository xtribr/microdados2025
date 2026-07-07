#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dificuldade por HABILIDADE - ENEM 2025 (Regular P1 nacional)
Combina % de acerto empirico (microdados reais) com parametros TRI A e B.
Dados reais ou nada. Nenhum dado sintetico.
"""
import csv, json, time, os
from collections import defaultdict

BASE = "/sessions/funny-kind-hawking/mnt/microdados_enem_2025/DADOS"
OUT  = "/sessions/funny-kind-hawking/mnt/microdados_enem_2025/analises_primi_2025_cop30/outputs"
ITENS = os.path.join(BASE, "ITENS_PROVA_2025.csv")
RES   = os.path.join(BASE, "RESULTADOS_2025.csv")
LOG   = os.path.join(OUT, "dificuldade_habilidades_progress.log")
JOUT  = os.path.join(OUT, "dificuldade_habilidades_2025.json")

# Cadernos padrao da 1a aplicacao nacional (Regular P1) - mesma definicao da auditoria COP30
REG = {
    'CN': {'1483','1484','1485','1486'},
    'CH': {'1447','1448','1449','1450'},
    'LC': {'1459','1460','1461','1462'},
    'MT': {'1471','1472','1473','1474'},
}
BASE_POS = {'LC':1, 'CH':46, 'CN':91, 'MT':136}  # CO_POSICAO global do 1o item da area

def log(msg):
    with open(LOG, 'a') as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")

# ---------- 1. Carregar itens ----------
# item_info[item] = {area, hab, A, B, C, aban}
item_info = {}
# slots[(area,prova)] = lista de 45; cada elemento:
#   nao-LC e LC-comum: ('S', item, gabchar, aban)
#   LC-lingua:         ('L', {'0':(item,gab,aban), '1':(item,gab,aban)})
slots = {}

def fnum(s):
    s = (s or '').strip().replace(',', '.')
    try: return float(s)
    except: return None

raw = defaultdict(list)  # (area,prova) -> list of dict rows
with open(ITENS, encoding='latin-1') as f:
    r = csv.DictReader(f, delimiter=';')
    for row in r:
        a = row['SG_AREA']; p = row['CO_PROVA']
        item = row['CO_ITEM']
        aban = row['IN_ITEM_ABAN'] == '1'
        item_info[item] = {
            'area': a, 'hab': row['CO_HABILIDADE'],
            'A': fnum(row['NU_PARAM_A']), 'B': fnum(row['NU_PARAM_B']),
            'C': fnum(row['NU_PARAM_C']), 'aban': aban,
        }
        raw[(a,p)].append({
            'pos': int(row['CO_POSICAO']), 'item': item,
            'gab': row['TX_GABARITO'], 'ling': row['TP_LINGUA'], 'aban': aban,
        })

for (a,p), rows in raw.items():
    if a not in REG or p not in REG[a]:
        continue
    base = BASE_POS[a]
    sl = [None]*45
    if a != 'LC':
        for rw in rows:
            i = rw['pos'] - base
            if 0 <= i < 45:
                sl[i] = ('S', rw['item'], rw['gab'], rw['aban'])
    else:
        # LC: posicoes 1-5 tem 2 itens (ling 0 e 1); 6-45 comuns (ling '')
        lang = defaultdict(dict)  # pos -> {ling: row}
        for rw in rows:
            if rw['ling'] in ('0','1'):
                lang[rw['pos']][rw['ling']] = rw
        for rw in rows:
            if rw['ling'] == '':  # comum
                i = rw['pos'] - 1   # pos 6..45 -> idx 5..44
                if 0 <= i < 45:
                    sl[i] = ('S', rw['item'], rw['gab'], rw['aban'])
        for pos in range(1,6):
            i = pos - 1
            d = {}
            for ln in ('0','1'):
                if ln in lang.get(pos,{}):
                    rw = lang[pos][ln]
                    d[ln] = (rw['item'], rw['gab'], rw['aban'])
            sl[i] = ('L', d)
    slots[(a,p)] = sl

log(f"itens carregados: {len(item_info)} | provas regulares mapeadas: {len(slots)}")

# ---------- 2. Stream RESULTADOS ----------
# acumula por item: [acertos, total_presentes]
agg = defaultdict(lambda: [0,0])
present = defaultdict(int)  # area -> n presentes regulares

with open(RES, encoding='latin-1') as f:
    header = f.readline().rstrip('\n').split(';')
    idx = {c:i for i,c in enumerate(header)}
    iPres = {a: idx['TP_PRESENCA_'+a] for a in REG}
    iProva= {a: idx['CO_PROVA_'+a] for a in REG}
    iResp = {a: idx['TX_RESPOSTAS_'+a] for a in REG}
    iLing = idx['TP_LINGUA']
    n=0
    t0=time.time()
    for line in f:
        n+=1
        c = line.rstrip('\n').split(';')
        if len(c) < len(header):
            continue
        for a in REG:
            if c[iPres[a]] != '1':
                continue
            p = c[iProva[a]]
            sl = slots.get((a,p))
            if sl is None:
                continue
            resp = c[iResp[a]]
            if len(resp) < 45:
                continue
            present[a]+=1
            ling = c[iLing]
            for i in range(45):
                s = sl[i]
                if s is None: continue
                if s[0]=='S':
                    _,item,gab,aban = s
                    if aban: continue
                    ent = agg[item]
                    ent[1]+=1
                    if resp[i]==gab: ent[0]+=1
                else:  # LC lingua
                    d = s[1]
                    rw = d.get(ling)
                    if rw is None: continue
                    item,gab,aban = rw
                    if aban: continue
                    ent = agg[item]
                    ent[1]+=1
                    if resp[i]==gab: ent[0]+=1
        if n % 250000 == 0:
            log(f"linhas={n} | presentes LC={present['LC']} CH={present['CH']} CN={present['CN']} MT={present['MT']} | {n/(time.time()-t0):.0f} l/s")
    log(f"FIM stream. linhas totais={n}")

# ---------- 3. Salvar agregados por item ----------
out_items = {}
for item, (ac, tot) in agg.items():
    info = item_info.get(item, {})
    out_items[item] = {
        'area': info.get('area'), 'hab': info.get('hab'),
        'A': info.get('A'), 'B': info.get('B'), 'C': info.get('C'),
        'acertos': ac, 'total': tot,
        'p': (ac/tot) if tot else None,
    }

result = {
    'meta': {
        'populacao': 'ENEM Regular P1 (cadernos padrao 1a aplicacao nacional)',
        'criterio_presenca': 'TP_PRESENCA_AREA == 1',
        'codigos_prova': REG,
        'itens_anulados': 'excluidos do calculo (IN_ITEM_ABAN=1)',
        'fonte': 'Microdados ENEM 2025 / INEP',
        'p': 'proporcao de acerto; branco conta como erro; denominador = presentes que viram o item',
    },
    'presentes_por_area': dict(present),
    'itens': out_items,
}
with open(JOUT, 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
log(f"JSON salvo: {JOUT} | itens com dados={len(out_items)}")
print("OK")
