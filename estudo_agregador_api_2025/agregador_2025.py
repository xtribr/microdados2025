#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agregador_2025.py — camada de dados reutilizável para o ENEM 2025 (TRI + habilidade)

Uso em qualquer script novo do projeto (posts, gráficos, dashboards, simulações):

    from agregador_2025 import load, by_area, get

    dados = load()                    # lista de 182 dicts (1 por questão/idioma da API)
    lc = by_area("LC")                # só Linguagens (50 registros, com variantes de idioma)
    item = get(index=21, area="CN")   # 1 registro específico

Cada registro tem: id, index, discipline, language, area, skill (dict ou None),
param_a, param_b, param_c (float ou None se item anulado), anulado (bool),
gabarito_confere (bool — False só nos 4 casos conhecidos do bug de idioma da API, ver README).

Fonte: Microdados ENEM 2025/INEP (ITENS_PROVA_2025.csv), caderno AZUL aplicação regular (P1).
Nunca inventa dado: item anulado → param_a/b/c = None, sempre.
"""
import json, os

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agregador_tri_habilidade_2025.json")
_cache = None

def load():
    global _cache
    if _cache is None:
        with open(_PATH, encoding="utf-8") as f:
            _cache = json.load(f)["registros"]
    return _cache

def by_area(area):
    return [r for r in load() if r["area"] == area.upper()]

def get(index, area, language=None):
    for r in load():
        if r["index"] == index and r["area"] == area.upper() and r["language"] == language:
            return r
    return None

def sem_anulados():
    """Atalho pra excluir itens anulados (uso comum em rankings/gráficos)."""
    return [r for r in load() if not r["anulado"]]

if __name__ == "__main__":
    d = load()
    print(f"{len(d)} registros carregados.")
    print(f"Com param_b real: {sum(1 for r in d if r['param_b'] is not None)}")
    print(f"Anulados: {sum(1 for r in d if r['anulado'])}")
