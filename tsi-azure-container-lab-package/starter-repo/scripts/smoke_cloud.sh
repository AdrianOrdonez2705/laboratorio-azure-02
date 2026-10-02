#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:-https://REEMPLAZAR.azurecontainerapps.io}"
if [[ "$BASE_URL" != https://* ]] || [[ "$BASE_URL" == *REEMPLAZAR* ]]; then
  echo "Uso: $0 https://<fqdn>.azurecontainerapps.io" >&2
  exit 2
fi
curl -fsS "$BASE_URL/health"; echo
curl -fsS "$BASE_URL/ready"; echo
curl -fsS -X POST "$BASE_URL/predict" -H 'Content-Type: application/json' \
  -d '{"feature_1":0.25,"feature_2":0.75,"feature_3":-0.10}'; echo
