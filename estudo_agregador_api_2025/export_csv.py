#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, csv, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(f"{OUT_DIR}/agregador_tri_habilidade_2025.json", encoding="utf-8") as f:
    d = json.load(f)

cols = ["id","index","discipline","language","area","skill_code","skill_label",
        "param_a","param_b","param_c","anulado","motivo_anulacao",
        "gabarito_confere_api","observacao"]

MOTIVOS = {(a,i,None if t=='' else ('ingles' if t=='0' else 'espanhol')): mo
           for a,i,t,mo in [(x['area'],x['index'],x['tp_lingua'],x['motivo']) for x in d['itens_anulados_csv']]}

with open(f"{OUT_DIR}/agregador_tri_habilidade_2025.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(cols)
    for r in d["registros"]:
        skill = r["skill"] or {}
        obs = ""
        if r["anulado"]:
            obs = "item anulado - sem parametro TRI (NUNCA preencher, conforme dado oficial INEP)"
        elif not r["gabarito_confere"]:
            obs = "API tem bug conhecido: correctAlternative da vaga 'espanhol' replica o da 'ingles' nesta posicao; skill/param_b aqui SAO os reais do item espanhol (TP_LINGUA=1)"
        motivo = MOTIVOS.get((r["area"], r["index"], r["language"]), "")
        w.writerow([
            r["id"], r["index"], r["discipline"], r["language"] or "", r["area"],
            (skill.get("code") or ""), (skill.get("label") or ""),
            r["param_a"] if r["param_a"] is not None else "",
            r["param_b"] if r["param_b"] is not None else "",
            r["param_c"] if r["param_c"] is not None else "",
            "1" if r["anulado"] else "0",
            motivo,
            "1" if r["gabarito_confere"] else "0",
            obs,
        ])

print("CSV salvo:", f"{OUT_DIR}/agregador_tri_habilidade_2025.csv")

# contagens finais para o relatorio
n_anulado = sum(1 for r in d["registros"] if r["anulado"])
n_com_param = sum(1 for r in d["registros"] if r["param_b"] is not None)
n_sem_skill = sum(1 for r in d["registros"] if not r["skill"])
print("registros:", d["total_registros"], "| com param_b real:", n_com_param,
      "| anulados (sem param, por regra):", n_anulado, "| sem skill:", n_sem_skill)
