#!/usr/bin/env bash
set -euo pipefail

required_vars=(AZ_SUBSCRIPTION RESOURCE_GROUP LOCATION ACR_NAME CONTAINER_APP_ENV CONTAINER_APP_NAME)
missing=0
for name in "${required_vars[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "ERROR: falta variable $name" >&2
    missing=1
  fi
done
if [[ "$missing" -ne 0 ]]; then
  exit 2
fi

for tool in az docker; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "ERROR: $tool no esta instalado o no esta en PATH" >&2
    exit 3
  fi
done

if ! az containerapp --help >/dev/null 2>&1; then
  echo "ERROR: falta la extension de Azure Container Apps. Ejecute: az extension add --name containerapp --upgrade" >&2
  exit 7
fi

az account show >/dev/null 2>&1 || {
  echo "ERROR: no hay sesion Azure activa. Ejecute: az login" >&2
  exit 4
}

current_sub=$(az account show --query id -o tsv)
if [[ "$current_sub" != "$AZ_SUBSCRIPTION" ]]; then
  echo "AVISO: la suscripcion activa no coincide con AZ_SUBSCRIPTION."
  echo "Ejecute: az account set --subscription \"$AZ_SUBSCRIPTION\""
  exit 5
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker esta instalado pero el daemon no responde." >&2
  exit 6
fi

echo "PRE-FLIGHT OK"
echo "Subscription: $AZ_SUBSCRIPTION"
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"
echo "ACR: $ACR_NAME"
echo "Container Apps Environment: $CONTAINER_APP_ENV"
echo "Container App: $CONTAINER_APP_NAME"
