#!/bin/bash
# Crawl INEP microdados ENEM 2015-2024, extrai min/max das notas por ano, limpa.
# 2025 vem do arquivo local ja existente. Roda em background.
set -u
WORK="/Volumes/Kingston 1/_enem_crawl_tmp"
PROJ="/Volumes/Kingston 1/microdados_enem_2025"
OUT="$PROJ/estudo_serie_historica"
mkdir -p "$WORK" "$OUT"
PY="$OUT/minmax_year.py"

log(){ echo "[$(date +%H:%M:%S)] $*"; }

YEARS="2015 2016 2017 2018 2019 2020 2021 2022 2023 2024"
for y in $YEARS; do
  if [ -f "$OUT/minmax_$y.json" ]; then log "$y ja processado, pulando"; continue; fi
  zip="$WORK/enem_$y.zip"
  url="https://download.inep.gov.br/microdados/microdados_enem_$y.zip"
  log "==== $y : baixando ===="
  curl -L -C - --retry 6 --retry-delay 5 --max-time 3600 -s -o "$zip" "$url"
  if [ ! -s "$zip" ]; then log "$y FALHA no download"; continue; fi
  log "$y baixado ($(du -h "$zip" | cut -f1)). Localizando CSV de notas..."
  member=$(unzip -Z1 "$zip" | grep -iE 'DADOS/.*(RESULTADOS|MICRODADOS).*\.csv$' | head -1)
  if [ -z "$member" ]; then
    member=$(unzip -Z1 "$zip" | grep -iE '\.csv$' | grep -ivE 'ITENS|ITEN' | head -1)
  fi
  log "$y membro: $member"
  rm -rf "$WORK/$y"; mkdir -p "$WORK/$y"
  unzip -o -j "$zip" "$member" -d "$WORK/$y" >/dev/null 2>&1
  csv=$(ls "$WORK/$y"/*.csv 2>/dev/null | head -1)
  if [ -z "$csv" ]; then log "$y FALHA ao extrair CSV"; rm -f "$zip"; continue; fi
  log "$y processando $(basename "$csv") ($(du -h "$csv" | cut -f1))..."
  python3 "$PY" "$csv" "$y" "$OUT/minmax_$y.json"
  rm -rf "$WORK/$y" "$zip"
  log "$y DONE, limpo."
done

# 2025 local
if [ ! -f "$OUT/minmax_2025.json" ]; then
  log "==== 2025 : arquivo local ===="
  python3 "$PY" "$PROJ/DADOS/RESULTADOS_2025.csv" 2025 "$OUT/minmax_2025.json"
fi
log "TUDO CONCLUIDO. JSONs em $OUT"
ls -1 "$OUT"/minmax_*.json
