#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recriacao vetorial do logo X-TRI (marca + wordmark) -> logo_xtri.png (fundo transparente)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import numpy as np

AZUL="#28ABE3"; LARANJA="#F1572B"
for p in ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
    fm.fontManager.addfont(p)
plt.rcParams['font.family']='Liberation Sans'

def heart_path(cx,cy,s):
    t=np.linspace(0,2*np.pi,200)
    x=16*np.sin(t)**3
    y=13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
    x=x/17.0; y=y/17.0
    # gira ~ -20deg para apontar como no logo (coração levemente inclinado)
    ang=np.radians(-18); xr=x*np.cos(ang)-y*np.sin(ang); yr=x*np.sin(ang)+y*np.cos(ang)
    verts=np.column_stack([cx+xr*s, cy+yr*s])
    return Path(verts, closed=True)

fig=plt.figure(figsize=(8,8),dpi=100)
fig.patch.set_alpha(0)
ax=fig.add_axes([0,0,1,1]); ax.axis('off'); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_aspect('equal')

C=(0.5,0.575); LW=78
# arms esquerda (azul)
ax.add_line(Line2D([C[0],0.14],[C[1],0.95],lw=LW,color=AZUL,solid_capstyle='round',zorder=2))
ax.add_line(Line2D([C[0],0.14],[C[1],0.20],lw=LW,color=AZUL,solid_capstyle='round',zorder=2))
# arms direita (laranja)
ax.add_line(Line2D([C[0],0.86],[C[1],0.95],lw=LW,color=LARANJA,solid_capstyle='round',zorder=3))
ax.add_line(Line2D([C[0]+0.04,0.70],[C[1]-0.02,0.20],lw=LW,color=LARANJA,solid_capstyle='round',zorder=3))
# coracao no encaixe direito
ax.add_patch(PathPatch(heart_path(0.70,0.58,0.085),fc=LARANJA,ec='none',zorder=4))

# wordmark X-TRI
ax.text(0.265,0.085,"X",fontsize=70,fontweight='bold',color=AZUL,ha='center',va='center')
ax.text(0.34,0.085,"-",fontsize=70,fontweight='bold',color=LARANJA,ha='center',va='center')
ax.text(0.58,0.085,"TRI",fontsize=70,fontweight='bold',color=LARANJA,ha='center',va='center')

fig.savefig("/sessions/funny-kind-hawking/mnt/microdados_enem_2025/logo_xtri.png",
            dpi=100,transparent=True)
# versao so-marca (sem wordmark) para o cabecalho do post
fig2=plt.figure(figsize=(8,8),dpi=100); fig2.patch.set_alpha(0)
ax2=fig2.add_axes([0,0,1,1]); ax2.axis('off'); ax2.set_xlim(0,1); ax2.set_ylim(0,1); ax2.set_aspect('equal')
C2=(0.5,0.5); LW2=92
ax2.add_line(Line2D([C2[0],0.13],[C2[1],0.92],lw=LW2,color=AZUL,solid_capstyle='round',zorder=2))
ax2.add_line(Line2D([C2[0],0.13],[C2[1],0.08],lw=LW2,color=AZUL,solid_capstyle='round',zorder=2))
ax2.add_line(Line2D([C2[0],0.87],[C2[1],0.92],lw=LW2,color=LARANJA,solid_capstyle='round',zorder=3))
ax2.add_line(Line2D([C2[0]+0.05,0.70],[C2[1]-0.03,0.08],lw=LW2,color=LARANJA,solid_capstyle='round',zorder=3))
ax2.add_patch(PathPatch(heart_path(0.71,0.5,0.10),fc=LARANJA,ec='none',zorder=4))
fig2.savefig("/sessions/funny-kind-hawking/mnt/microdados_enem_2025/logo_xtri_marca.png",
             dpi=100,transparent=True)
print("logos salvos")
