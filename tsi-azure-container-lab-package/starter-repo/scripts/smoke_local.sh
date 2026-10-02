#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:-http://localhost:8000}"

echo "[1/3] GET $BASE_URL/health"
curl -fsS "$BASE_URL/health"; echo

echo "[2/3] GET $BASE_URL/ready"
curl -fsS "$BASE_URL/ready"; echo

echo "[3/3] POST $BASE_URL/predict"
curl -fsS -X POST "$BASE_URL/predict" \
  -H 'Content-Type: application/json' \
  -d '{"feature_1":0.25,"feature_2":0.75,"feature_3":-0.10}'; echo
