#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEASER (proposta) — nota media ENEM 2025 por rede de ensino (dado REAL, mesma linha que a nota).
Respeita a trava: TP_DEPENDENCIA_ADM_ESC vive em RESULTADOS -> joinavel. Nao cruza socioeconomico."""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

d = json.load(open("/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/eea62195-d399-4434-8338-95d5d92b8bac/scratchpad/anchor_perfil_tri.json"))
dep = d["by_dependencia"]
areas = ["CN","CH","LC","MT","RED"]
albl  = ["Natureza","Humanas","Linguagens","Matemática","Redação"]
redes = [("2","Estadual","#6BAED6"),("3","Municipal","#9E9AC8"),("1","Federal","#FD8D3C"),("4","Privada","#41AB5D")]

fig, ax = plt.subplots(figsize=(11,6.2), dpi=150)
fig.patch.set_facecolor("#FFFFFF"); ax.set_facecolor("#FFFFFF")
x = np.arange(len(areas)); w = 0.2
for i,(code,name,col) in enumerate(redes):
    vals = [dep[code][a][0] for a in areas]
    bars = ax.bar(x + (i-1.5)*w, vals, w, label=name, color=col, edgecolor="white", linewidth=0.6)
    for b,v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+4, f"{v:.0f}", ha="center", va="bottom", fontsize=7.5, color="#333")

ax.set_xticks(x); ax.set_xticklabels(albl, fontsize=11)
ax.set_ylabel("Nota média (escala TRI 0–1000)", fontsize=11)
ax.set_ylim(440, 770)
fig.suptitle("ENEM 2025 — nota média por rede de ensino", fontsize=16, weight="bold", color="#1F4E78", y=0.99)
ax.text(0.0, 1.10, "Entre os 36% dos inscritos com escola declarada (1,74 mi). Gap Privada–Estadual: +140 em Matemática, +203 na Redação.",
        transform=ax.transAxes, fontsize=9.5, color="#555")
ax.legend(loc="upper left", ncol=4, frameon=False, fontsize=10, bbox_to_anchor=(0,1.06))
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#E5E5E5", linewidth=0.8)
ax.set_axisbelow(True)
fig.text(0.99, 0.01, "Fonte: Microdados ENEM 2025 (INEP) · X-TRI — TEASER de proposta", ha="right", fontsize=7.5, color="#999")
fig.tight_layout(rect=[0,0.02,1,1])
out="/private/tmp/claude-502/-Volumes-Kingston-1-microdados-enem-2025/eea62195-d399-4434-8338-95d5d92b8bac/scratchpad/TEASER_nota_por_rede.png"
fig.savefig(out, facecolor=fig.get_facecolor()); print("OK ->", out)
