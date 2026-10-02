---
name: azure-deploy-check
description: Revisar si el laboratorio TSI esta preparado para publicar una imagen Docker en Azure Container Registry y desplegarla en Azure Container Apps, sin ejecutar despliegues ni borrados automaticamente.
---

# Azure Deploy Check

Inspeccionar el repositorio y producir un gate de predespliegue basado en evidencia.

## Revisar
1. `python -m pytest -v` y existencia de `model/model.joblib`.
2. `Dockerfile`: Python 3.12 slim, usuario no-root, puerto 8000, `HEALTHCHECK`, ausencia de secretos.
3. `.dockerignore`: `.env`, `.git`, `.venv`, caches y tests excluidos.
4. Configuracion: `.env.example` solo contiene valores ficticios; secretos reales no estan versionados.
5. API: `/health`, `/ready`, `/predict` y validaciones de entrada.
6. Smoke test local y, si existe imagen, resultado del escaneo.
7. Variables de Azure requeridas: suscripcion, Resource Group, region, ACR, Container Apps Environment y Container App.
8. Plantilla de evidencia y runbook actualizados.

## Reglas
- No ejecutar despliegues Azure automaticamente.
- No eliminar recursos Azure automaticamente.
- No leer ni revelar secretos.
- No afirmar que un check paso si no se ejecuto.
- Si Docker, Trivy o Azure CLI no estan disponibles, marcar el check como NO EJECUTADO.

## Salida obligatoria
Terminar con uno de estos estados:

`READY FOR DEPLOYMENT`

solo si los checks criticos ejecutables estan verdes y no faltan entradas obligatorias; o:

`BLOCKED`

seguido por una lista numerada de bloqueos, evidencia observada y accion recomendada.
