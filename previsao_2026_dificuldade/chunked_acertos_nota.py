#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processa RESULTADOS_2025.csv em pedacos de bytes (resumivel entre chamadas separadas,
ja que o ambiente mata processos apos ~45s e ha um teto de tempo por chamada).
Cada execucao le CHUNK_BYTES a partir do offset salvo, processa, atualiza o checkpoint
(offset + acumulador de nota por acertos/area), e sai. Rodar repetidas vezes ate acabar.
"""
import json, os, sys

SRC = "/sessions/kind-gracious-heisenberg/mnt/microdados_enem_2025/DADOS/RESULTADOS_2025.csv"
CKPT = "/sessions/kind-gracious-heisenberg/mnt/outputs/previsao_2026/checkpoint_acertos.json"
CHUNK_BYTES = 260_000_000  # ~260MB por chamada

# indices 0-based no split por ';'
IDX = {
    "CN": {"pres": 14, "nota": 22, "resp": 26, "gab": 31},
    "CH": {"pres": 15, "nota": 23, "resp": 27, "gab": 32},
    "LC": {"pres": 16, "nota": 24, "resp": 28, "gab": 33},
    "MT": {"pres": 17, "nota": 25, "resp": 29, "gab": 34},
}
AREAS = ["CN", "CH", "LC", "MT"]

def load_ckpt():
    if os.path.exists(CKPT):
        with open(CKPT, encoding="utf-8") as f:
            return json.load(f)
    with open(SRC, "rb") as f:
        header = f.readline()
    return {"offset": len(header), "acc": {}, "lines_done": 0, "done": False}

def save_ckpt(ck):
    with open(CKPT, "w", encoding="utf-8") as f:
        json.dump(ck, f)

def process_lines(lines, acc):
    import numpy as np
    for area in AREAS:
        ix = IDX[area]
        acertos_list = []
        nota_list = []
        for ln in lines:
            parts = ln.split(";")
            if len(parts) <= max(ix.values()):
                continue
            if parts[ix["pres"]] != "1":
                continue
            resp = parts[ix["resp"]]
            gab = parts[ix["gab"]]
            nota_s = parts[ix["nota"]]
            if not resp or not gab or not nota_s:
                continue
            try:
                nota = float(nota_s)
            except ValueError:
                continue
            if area == "LC":
                if len(resp) < 45 or len(gab) < 50:
                    continue
                r = resp[5:45]
                g = gab[10:50]
            else:
                if len(resp) < 45 or len(gab) < 45:
                    continue
                r = resp[:45]
                g = gab[:45]
            ac = sum(1 for x, y in zip(r, g) if x == y)
            acertos_list.append(ac)
            nota_list.append(nota)
        if not acertos_list:
            continue
        ac_arr = np.array(acertos_list)
        nota_arr = np.array(nota_list)
        for ac in np.unique(ac_arr):
            mask = ac_arr == ac
            notas = nota_arr[mask]
            key = f"{area}|{int(ac)}"
            if key not in acc:
                acc[key] = [0.0, 0, None, None]
            s = acc[key]
            s[0] += float(notas.sum())
            s[1] += int(notas.size)
            mn = float(notas.min()); mx = float(notas.max())
            s[2] = mn if s[2] is None else min(s[2], mn)
            s[3] = mx if s[3] is None else max(s[3], mx)

def main():
    ck = load_ckpt()
    if ck.get("done"):
        print("JA CONCLUIDO. offset=", ck["offset"], "lines_done=", ck["lines_done"])
        return

    total_size = os.path.getsize(SRC)
    offset = ck["offset"]
    with open(SRC, "rb") as f:
        f.seek(offset)
        buf = f.read(CHUNK_BYTES)

    is_last = (offset + len(buf)) >= total_size
    if not is_last:
        last_nl = buf.rfind(b"\n")
        if last_nl == -1:
            print("ERRO: chunk sem newline, aumentar CHUNK_BYTES")
            return
        usable = buf[:last_nl]
        new_offset = offset + last_nl + 1
    else:
        usable = buf
        new_offset = total_size

    text = usable.decode("latin-1")
    lines = text.split("\n")
    lines = [ln for ln in lines if ln]

    process_lines(lines, ck["acc"])
    ck["offset"] = new_offset
    ck["lines_done"] = ck.get("lines_done", 0) + len(lines)
    ck["done"] = is_last
    save_ckpt(ck)
    pct = 100.0 * new_offset / total_size
    print(f"offset={new_offset:,}/{total_size:,} ({pct:.1f}%) | linhas processadas nesta chamada={len(lines):,} | total linhas={ck['lines_done']:,} | done={is_last}")

if __name__ == "__main__":
    main()
