#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carrossel IG — O MAPA DA PROVA POR TEMA (ENEM 2025), 1 card por área + capa + como usar.
Adaptação 4:5 (feed) e 9:16 (story) dos mapas da palestra (fonte: mapeamento_2025 do RStudio).
Dados: dificuldade oficial (b×100+500, ITENS_PROVA/INEP) + tema/matéria classificados pela XTRI.
Marca XTRI: Outfit/JetBrains, fundo claro, cores de dificuldade da marca, xtri.online."""
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

RS = "/Volumes/Kingston 1/microdados no R Studio"
REPO = "/Volumes/Kingston 1/microdados_enem_2025"
FD = ("/Volumes/Kingston/Library/Application Support/Claude/local-agent-mode-sessions/"
      "skills-plugin/173c3dab-6f51-4ed6-920d-43825f73e36c/"
      "a32ba23c-1f19-4aa1-8eaf-390193971d87/skills/canvas-design/canvas-fonts")
OUT = Path(REPO) / "posts_mapa_tema"; OUT.mkdir(exist_ok=True)

# ---- marca ----
BG = (241, 241, 242); CARD = (255, 255, 255); INK = (29, 29, 32); GRAY = (140, 146, 152)
GRID = (234, 234, 238); CORAL = (250, 82, 48); CORALd = (232, 67, 31)
CYAN = (31, 175, 239); CYANd = (21, 151, 216)
# dificuldade (paleta da marca): fácil cyan-claro · média cinza · difícil coral
DF = (86, 194, 242); DM = (150, 156, 163); DD = (250, 82, 48)
HL = (254, 233, 227); HLB = (232, 67, 31)          # realce erro-surpresa (coral claro)
AREAS = [("LC", "Linguagens", (44, 111, 187)), ("CH", "Ciências Humanas", (214, 51, 108)),
         ("CN", "Ciências da Natureza", (46, 158, 79)), ("MT", "Matemática", (217, 138, 31))]
SURPRISE = {11, 14, 28, 31, 41, 43, 58, 61, 62, 82, 100, 101, 102, 107, 129, 142, 143, 154, 161}


def F(name, sz):
    return ImageFont.truetype(f"{FD}/{name}.ttf", sz)


def band(d):
    return DF if d < 550 else (DM if d < 650 else DD)


# ---- dados ----
tema = {int(r["num"]): r["tema"] for r in csv.DictReader(open(f"{RS}/mapeamento_2025/tema_1palavra.csv", encoding="utf-8"))}
rows = list(csv.DictReader(open(f"{RS}/mapeamento_2025/MAPEAMENTO_ENEM_2025.csv", encoding="utf-8")))
pts = {a: [] for a, _, _ in AREAS}
for r in rows:
    if r["dificuldade"] == "" or (r["area"] == "LC" and r["versao"] == "Espanhol"):
        continue
    n = int(r["num"]); pts[r["area"]].append((n, float(r["dificuldade"]), tema[n], r["materia"]))

W = 2160  # 1080 * 2


def base_canvas(H):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    return im, d


def logo(im, x, y, h=86):
    lg = Image.open(f"{REPO}/logo_xtri_marca_real.png").convert("RGBA")
    w = int(lg.width * h / lg.height); lg = lg.resize((w, h), Image.LANCZOS)
    im.paste(lg, (x, y), lg)
    return w


def footer(im, d, H, pg, nota):
    y = H - 120
    d.text((128, y), nota, font=F("JetBrainsMono-Regular", 26), fill=GRAY)
    # assinatura colorida
    fB = F("Outfit-Bold", 32); yy = y + 46; xx = 128
    for s, c in [("Transformamos ", INK), ("dados", (31, 175, 239)), (" em ", INK), ("aprovações", CORAL), (".", INK)]:
        d.text((xx, yy), s, font=fB, fill=c); xx += d.textlength(s, font=fB)
    d.text((W - 128, yy + 6), f"@xandaoxtri · xtri.online", font=F("JetBrainsMono-Regular", 26), fill=GRAY, anchor="ra")
    d.text((W - 128, y), pg, font=F("JetBrainsMono-Bold", 28), fill=GRAY, anchor="ra")


def legenda_niveis(d, lx, ly, fs=30):
    fL = F("Outfit-Bold", fs); fitem = F("Outfit-Regular", fs)
    for col, lab in [(DF, "fácil (dif < 550)"), (DM, "média (550–650)"), (DD, "difícil (650+)")]:
        d.ellipse([lx, ly + 6, lx + 26, ly + 32], fill=col)
        d.text((lx + 38, ly), lab, font=fitem, fill=INK)
        lx += d.textlength(lab, font=fitem) + 92
    d.ellipse([lx, ly + 3, lx + 32, ly + 35], outline=INK, width=5)
    d.ellipse([lx + 10, ly + 13, lx + 22, ly + 25], fill=(120, 120, 128))
    d.text((lx + 46, ly), "pegadinha: fácil que os 700+ erram", font=fitem, fill=INK)


def overlap(a, b, m=8):
    return not (a[2] + m < b[0] or b[2] + m < a[0] or a[3] + m < b[1] or b[3] + m < a[1])


# ---------- card do mapa (1 por área) ----------
def card_mapa(area, nome, accent, idx, H, suffix):
    im, d = base_canvas(H)
    logo(im, 128, 96, 86)
    d.text((W - 128, 128), "MAPA DA PROVA POR TEMA", font=F("JetBrainsMono-Bold", 28), fill=GRAY, anchor="rm")
    d.text((128, 226), nome.upper(), font=F("Outfit-Bold", 84), fill=accent)
    d.text((128, 330), "o tema de cada questão, pela posição e dificuldade", font=F("Outfit-Regular", 38), fill=(107, 112, 118))
    legenda_niveis(d, 128, 398, 30)
    # cartão do plot
    PX0, PX1 = 176, W - 130
    PY0 = 520; PY1 = H - 300
    d.rounded_rectangle([100, PY0 - 30, W - 100, PY1 + 96], radius=28, fill=CARD)
    P = sorted(pts[area], key=lambda t: t[0])
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    xmin, xmax = min(xs) - 1, max(xs) + 1; ymin, ymax = min(ys) - 38, max(ys) + 50

    def X(v): return PX0 + (v - xmin) / (xmax - xmin) * (PX1 - PX0)
    def Y(v): return PY1 - (v - ymin) / (ymax - ymin) * (PY1 - PY0)
    # faixas de fundo
    for lo, hi, col in [(ymin, 550, DF), (550, 650, (200, 203, 208)), (650, ymax, DD)]:
        lo, hi = max(lo, ymin), min(hi, ymax)
        if hi > lo:
            tint = tuple(int(c * 0.05 + 255 * 0.95) for c in col)
            d.rectangle([PX0, Y(hi), PX1, Y(lo)], fill=tint)
    fax = F("JetBrainsMono-Regular", 28)
    yt = int(ymin // 50 * 50) + 50
    while yt < ymax:
        d.line([(PX0, Y(yt)), (PX1, Y(yt))], fill=GRID, width=2)
        d.text((PX0 - 18, Y(yt)), str(yt), font=fax, fill=GRAY, anchor="rm"); yt += 50
    for b in (550, 650):
        if ymin < b < ymax:
            d.line([(PX0, Y(b)), (PX1, Y(b))], fill=(168, 168, 176), width=3)
    xt = int(xmin // 5 * 5) + 5
    while xt < xmax:
        d.line([(X(xt), PY0), (X(xt), PY1)], fill=GRID, width=2)
        d.text((X(xt), PY1 + 16), str(xt), font=fax, fill=GRAY, anchor="mt"); xt += 5
    d.text(((PX0 + PX1) / 2, PY1 + 62), "posição na prova (número da questão)", font=fax, fill=INK, anchor="mt")

    # ---- rótulos sem colisão (mesma lógica da palestra, gaps ampliados p/ retrato) ----
    fT = F("Outfit-Bold", 38); fM = F("JetBrainsMono-Regular", 24)
    dots = [(X(p[0]), Y(p[1])) for p in P]
    cand = []
    for gap in (14, 50, 90, 134, 182, 236, 296, 360):
        for side in ('b', 'a'):
            for sh in (0, 0.7, -0.7, 1.4, -1.4, 2.2, -2.2):
                cand.append((side, gap, sh))
    for gap in (16, 66, 130, 190):
        for side in ('r', 'l'):
            cand.append((side, gap, 0))

    def crowd(i):
        px, py = dots[i]
        return sum(1 for j, (ox, oy) in enumerate(dots) if j != i and abs(ox - px) < 180 and abs(oy - py) < 130)
    order = sorted(range(len(P)), key=lambda i: (-crowd(i), dots[i][1]))
    placed = []; boxes = {}
    for i in order:
        px, py = dots[i]; tem = P[i][2]; mat = P[i][3]
        tw = d.textlength(tem, font=fT); mw = d.textlength(mat, font=fM)
        w = max(tw, mw); h = 40 + 28 + 6
        chosen = None
        for side, gap, sh in cand:
            cx = px + sh * (w * 0.5 + 18)
            if side == 'b': x0, y0 = cx - w / 2, py + gap
            elif side == 'a': x0, y0 = cx - w / 2, py - gap - h
            elif side == 'r': x0, y0 = px + gap, py - h / 2
            else: x0, y0 = px - gap - w, py - h / 2
            box = [x0, y0, x0 + w, y0 + h]
            if box[0] < PX0: box = [PX0, box[1], PX0 + w, box[3]]
            if box[2] > PX1: box = [PX1 - w, box[1], PX1, box[3]]
            if box[1] < PY0 or box[3] > PY1: continue
            bad = any(overlap(box, pb) for pb in placed)
            if not bad:
                for (ox, oy) in dots:
                    if box[0] - 3 < ox < box[2] + 3 and box[1] - 3 < oy < box[3] + 3:
                        bad = True; break
            if not bad:
                chosen = box; break
        if chosen is None:
            chosen = [px - w / 2, py + 14, px + w / 2, py + 14 + h]
        # pegadinhas ganham moldura depois: reservar a folga da moldura na colisão
        pad = 26 if P[i][0] in SURPRISE else 0
        placed.append([chosen[0] - pad, chosen[1] - pad, chosen[2] + pad, chosen[3] + pad])
        boxes[i] = chosen
    for i in order:  # conectores
        px, py = dots[i]; box = boxes[i]
        ax = (box[0] + box[2]) / 2; ay = box[1] if box[1] > py else box[3]
        if abs(ay - py) > 18 or abs(ax - px) > 18:
            d.line([(px, py), (ax, ay)], fill=(203, 203, 210), width=2)
    for (px, py), p in zip(dots, P):  # bolinhas
        if p[0] in SURPRISE:
            d.ellipse([px - 19, py - 19, px + 19, py + 19], outline=INK, width=5)
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=band(p[1]), outline=(255, 255, 255), width=3)
    for i in order:  # textos
        box = boxes[i]; tem = P[i][2]; mat = P[i][3]; cx = (box[0] + box[2]) / 2
        if P[i][0] in SURPRISE:
            d.rounded_rectangle([box[0] - 12, box[1] - 6, box[2] + 12, box[3] + 2], radius=10, fill=HL, outline=HLB, width=3)
        d.text((cx, box[1]), tem, font=fT, fill=INK, anchor="ma")
        d.text((cx, box[1] + 42), mat, font=fM, fill=GRAY, anchor="ma")
    footer(im, d, H, f"{idx}/6", "Fonte: Microdados ENEM 2025 / INEP (dificuldade oficial b×100+500, caderno Azul) · temas: classificação XTRI")
    fp = OUT / f"c{idx}_{area}{suffix}.png"
    im.resize((1080, int(H / 2)), Image.LANCZOS).save(fp)
    print("ok:", fp.name, len(P), "itens")


# ---------- capa ----------
def capa(H, suffix):
    im, d = base_canvas(H)
    logo(im, 128, 96, 86)
    d.text((W - 128, 128), "ENEM 2025 · TRI", font=F("JetBrainsMono-Bold", 28), fill=GRAY, anchor="rm")
    ty = (H - 2700) // 2 + 640
    fH = F("Outfit-Bold", 128)
    d.text((128, ty), "O MAPA DA", font=fH, fill=INK)
    d.text((128, ty + 152), "PROVA,", font=fH, fill=INK)
    d.text((128 + d.textlength("PROVA, ", font=fH), ty + 152), "TEMA", font=fH, fill=(21, 151, 216))
    d.text((128, ty + 304), "POR", font=fH, fill=INK)
    d.text((128 + d.textlength("POR ", font=fH), ty + 304), "TEMA", font=fH, fill=CORAL)
    fS = F("Outfit-Regular", 42)
    d.text((128, ty + 490), "As 175 questões do ENEM 2025 num mapa só: o tema de", font=fS, fill=(107, 112, 118))
    d.text((128, ty + 548), "cada uma, o quão difícil foi, e onde estão as pegadinhas.", font=fS, fill=(107, 112, 118))
    # cartão legenda
    cy = ty + 680
    d.rounded_rectangle([128, cy, W - 128, cy + 340], radius=26, fill=CARD)
    d.rounded_rectangle([128, cy, 148, cy + 340], radius=10, fill=CORAL)
    d.text((188, cy + 52), "Como ler", font=F("Outfit-Bold", 44), fill=INK)
    legenda_niveis(d, 188, cy + 134, 32)
    d.text((188, cy + 218), "Cada bolinha é uma questão real, com o tema e a matéria —", font=F("Outfit-Regular", 34), fill=INK)
    d.text((188, cy + 266), "direto do microdado oficial.", font=F("Outfit-Regular", 34), fill=INK)
    # chips das 4 áreas (o que vem no carrossel)
    gy = cy + 420
    d.text((128, gy), "DESLIZE PARA VER", font=F("JetBrainsMono-Bold", 30), fill=GRAY)
    chip_w = (W - 2 * 128 - 3 * 28) / 4
    labels = [("Linguagens", "45 questões"), ("Humanas", "45 questões"), ("Natureza", "42 questões"), ("Matemática", "43 questões")]
    for k, ((a, _, accent), (nm, qn)) in enumerate(zip(AREAS, labels)):
        x0 = 128 + k * (chip_w + 28)
        d.rounded_rectangle([x0, gy + 64, x0 + chip_w, gy + 244], radius=22, fill=CARD)
        d.rounded_rectangle([x0, gy + 64, x0 + chip_w, gy + 84], radius=10, fill=accent)
        d.text((x0 + chip_w / 2, gy + 124), nm, font=F("Outfit-Bold", 37), fill=INK, anchor="ma")
        d.text((x0 + chip_w / 2, gy + 182), qn, font=F("JetBrainsMono-Regular", 26), fill=GRAY, anchor="ma")
    footer(im, d, H, "1/6", "Fonte: Microdados ENEM 2025 / INEP · caderno Azul, 1ª aplicação · temas: classificação XTRI")
    fp = OUT / f"c1_capa{suffix}.png"
    im.resize((1080, int(H / 2)), Image.LANCZOS).save(fp)
    print("ok:", fp.name)


# ---------- fecho: como usar ----------
def fecho(H, suffix):
    im, d = base_canvas(H)
    logo(im, 128, 96, 86)
    d.text((W - 128, 128), "COMO USAR O MAPA", font=F("JetBrainsMono-Bold", 28), fill=GRAY, anchor="rm")
    ty = (H - 2700) // 2 + 560
    fH = F("Outfit-Bold", 96)
    d.text((128, ty), "COMO USAR", font=fH, fill=INK)
    d.text((128, ty + 118), "ESSE MAPA", font=fH, fill=CORAL)
    itens = [
        (DF, "Garanta as claras (fácil, dif < 550)", "quase todo mundo acerta — errar essas é o que mais derruba a nota na TRI."),
        (DM, "Viva na faixa do meio (550–650)", "é aqui que a nota sobe: são as questões que separam quem fica no 600 de quem chega no 700."),
        (DD, "Respeite as corais (650+)", "só brigue com elas depois de garantir o resto — até quem tira 700+ erra muitas."),
        (HLB, "Cuidado com as marcadas", "são as pegadinhas: questões fáceis que até os 700+ erram. Leia com calma redobrada."),
    ]
    yy = ty + 300
    for col, tit, sub in itens:
        d.rounded_rectangle([128, yy, W - 128, yy + 214], radius=24, fill=CARD)
        d.ellipse([176, yy + 52, 176 + 40, yy + 92], fill=col if col != HLB else CARD, outline=INK if col == HLB else None, width=5 if col == HLB else 0)
        d.text((256, yy + 40), tit, font=F("Outfit-Bold", 42), fill=INK)
        d.text((256, yy + 108), sub, font=F("Outfit-Regular", 33), fill=(90, 94, 99))
        yy += 244
    d.text((128, yy + 40), "Quer o raio-X completo da sua nota?", font=F("Outfit-Regular", 38), fill=(107, 112, 118))
    d.text((128, yy + 96), "xtri.online", font=F("JetBrainsMono-Bold", 52), fill=CYANd)
    footer(im, d, H, "6/6", "Fonte: Microdados ENEM 2025 / INEP · caderno Azul, 1ª aplicação · temas: classificação XTRI")
    fp = OUT / f"c6_como_usar{suffix}.png"
    im.resize((1080, int(H / 2)), Image.LANCZOS).save(fp)
    print("ok:", fp.name)


if __name__ == "__main__":
    for H, suf in [(2700, ""), (3840, "_story")]:
        capa(H, suf)
        for k, (a, nome, accent) in enumerate(AREAS, start=2):
            card_mapa(a, nome, accent, k, H, suf)
        fecho(H, suf)
