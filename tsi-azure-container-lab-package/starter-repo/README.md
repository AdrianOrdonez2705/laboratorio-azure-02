# Laboratorio TSI - Docker local a Azure Container Apps con IA

Este repositorio es el punto de partida del laboratorio. El objetivo no es construir un modelo complejo: es aprender a convertir un componente inteligente pequeño en un servicio probado, contenerizado, publicado en Azure Container Registry y ejecutado en Azure Container Apps.

## Flujo

`modelo -> FastAPI -> pytest -> Docker -> Trivy -> ACR -> Container Apps -> HTTPS -> logs -> v2`

## 1. Abrir en VS Code

Abra la carpeta `starter-repo` como carpeta de trabajo. Use una terminal integrada PowerShell en Windows o Bash en Linux/macOS.

## 2. Preparar Python 3.12

Opcion recomendada con `uv`:

```powershell
uv venv --python 3.12
.\.venv\Scripts\Activate.ps1
uv sync --dev
```

En Bash:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv sync --dev
```

## 3. Generar el modelo y ejecutar pruebas

```powershell
python scripts/train_model.py
python -m pytest -v
```

## 4. Ejecutar la API sin Docker

```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

En otra terminal ejecute `scripts/smoke_local.ps1`:

```powershell
.\scripts\smoke_local.ps1
```

## 5. Revisar con Claude Code u otra IA

Claude Code puede usar las reglas de `CLAUDE.md` y la Skill:

`.claude/skills/azure-deploy-check/SKILL.md`

Con otra IA copie los prompts de `prompts/`. El principio es el mismo: primero analizar y planificar; luego editar; siempre verificar con comandos reales.

## 6. Construir Docker

```powershell
docker build -t tsi-intelligent-api:v1 .
docker run --rm -p 8000:8000 tsi-intelligent-api:v1
```

Smoke test:

```powershell
.\scripts\smoke_local.ps1
```

Escaneo:

```powershell
trivy image tsi-intelligent-api:v1
```

## 7. Desplegar en Azure

Siga paso a paso:

`docs/azure-deployment-runbook-template.md`

Prepare primero la extension de Container Apps y los proveedores requeridos como indica el runbook. Luego, antes de crear recursos, ejecute:

```powershell
.\scripts\azure_preflight.ps1
```

La secuencia cloud es ACR -> identidad administrada -> Container Apps Environment -> Container App -> probes -> HTTPS -> logs -> v2.

## 8. Evidencia

Complete `docs/evidence-template.md`. La IA no es evidencia: use resultados de tests, build, smoke tests, escaneo, Azure CLI/Portal, logs y URL HTTPS.

## 9. Seguridad

- No versionar `.env`.
- No pegar secretos en prompts.
- No activar credenciales administrativas de ACR para evitar un problema de permisos sin autorizacion docente.
- No eliminar el Resource Group hasta que el docente autorice.
