# Verificacion del paquete - Laboratorio Azure Container Apps + IA

Fecha de verificacion: 2026-09-28

## Alcance

Este informe registra las comprobaciones ejecutadas sobre el paquete docente antes de su entrega. Se distingue entre verificaciones realmente ejecutadas en este entorno y actividades cloud que requieren herramientas o credenciales externas.

## Verificaciones ejecutadas

### 1. Generacion del modelo y suite automatizada

Comandos:

```bash
cd starter-repo
python scripts/train_model.py
python -m pytest -v
```

Resultado:

- Modelo generado en `model/model.joblib`.
- 23 pruebas ejecutadas.
- 23 pruebas aprobadas.
- Cobertura funcional de configuracion, carga/prediccion del modelo, `/health`, `/ready`, `/predict`, validacion de entradas, Dockerfile/.dockerignore, activos de IA, activos Azure y consistencia documental.

Nota de entorno: la ejecucion de verificacion se realizo con Python 3.13.5 porque este entorno no dispone de Python 3.12. El proyecto entregado declara y documenta Python `>=3.12,<3.13`, que es la version objetivo del laboratorio para estudiantes.

### 2. Smoke test real de la API sin Docker

Se inicio Uvicorn localmente y se ejecuto `scripts/smoke_local.sh` contra `http://127.0.0.1:8012`.

Respuestas observadas:

```text
GET /health  -> {"status":"ok"}
GET /ready   -> {"status":"ready","model_loaded":true}
POST /predict -> {"prediction":"high","confidence":0.6431863601214319,"model_version":"1.0"}
```

Los tres endpoints respondieron HTTP 200.

### 3. Auditoria estatica de Docker y scripts

- Pruebas estaticas de `Dockerfile` y `.dockerignore`: aprobadas.
- El runbook exige actualizar la extension `containerapp` y registrar `Microsoft.App` y `Microsoft.OperationalInsights`; los pre-flight validan la disponibilidad de `az containerapp` y el estado de proveedores.
- Dockerfile usa imagen Python 3.12 slim, usuario no-root, `HEALTHCHECK`, puerto 8000 y copias acotadas de `app/` y `model/`.
- `.dockerignore` excluye `.env`, Git, entornos virtuales, caches, tests y documentos que no deben formar parte de la imagen.
- Sintaxis Bash de los scripts `.sh`: verificada con `bash -n`.

### 4. Auditoria de secretos y dependencias de maquina

Comprobaciones realizadas sobre los archivos de texto del paquete:

- No existe un archivo `.env` real.
- No se encontraron archivos `.pem`, `.key`, `.pfx` o `.p12`.
- No se encontraron marcadores de clave privada.
- No se encontraron rutas internas del entorno de generacion ni perfiles de usuario locales en los archivos que recibiran los estudiantes.
- Los valores sensibles se representan mediante variables o placeholders.
- `CLAUDE.md` y la Skill prohiben exponer secretos a la IA.

### 5. Guia Word

Archivo:

`Guia_Estudiante_Lab_Azure_ContainerApps_IA_TSI.docx`

La guia fue renderizada a PNG mediante el flujo de QA de documentos. La version final contiene 11 paginas. Se verifico visualmente que no existan textos recortados, tablas rotas, objetos superpuestos ni paginas residuales en blanco.

## Limitaciones del entorno de generacion

Las siguientes verificaciones NO se marcaron como exitosas porque las herramientas no estan instaladas o requeririan credenciales Azure:

- Docker Engine/CLI: no disponible; no se pudo ejecutar `docker build` ni `docker run`.
- Trivy: no disponible; no se pudo ejecutar el escaneo real de la imagen.
- Azure CLI (`az`): no disponible; no se crearon ACR, identidad administrada, Container Apps Environment ni Container App.
- PowerShell (`pwsh`): no disponible; los scripts `.ps1` fueron revisados de forma estatica, pero no ejecutados.
- No se realizaron acciones contra una suscripcion Azure ni se generaron costos.

Estas limitaciones estan declaradas expresamente para evitar presentar resultados no ejecutados como evidencia.

## Criterio de entrega

El paquete queda preparado para que el estudiante complete en su propia estacion de trabajo las verificaciones que requieren Docker, Trivy, PowerShell y Azure. La guia exige guardar evidencia real de esos comandos y no aceptar como prueba una afirmacion generada por la IA.

## Estado previo al empaquetado

APROBADO para ensamblar el ZIP, sujeto a la inspeccion final del archivo comprimido y a confirmar que no incluya caches, entornos virtuales, carpetas QA, metadata Git ni archivos internos de ejecucion.

## Inspeccion del ZIP distribuible

Se creo una version preliminar del ZIP, se extrajo en una carpeta temporal y se repitieron las comprobaciones desde los bytes extraidos:

- 23/23 pruebas aprobadas desde `starter-repo` extraido.
- Smoke test extraido: `/health`, `/ready` y `/predict` respondieron correctamente.
- El archivo contiene la guia Word, README de inicio rapido, reporte de verificacion, starter repo, prompts, Skill, runbook, scripts, pruebas y modelo.
- No se incluyeron `.git`, `.superpowers`, carpetas de render QA, `.venv`, `.pytest_cache`, `__pycache__`, `.ruff_cache` ni archivos `.pyc`.
- No se incluyeron `.env` reales, claves privadas ni archivos de credenciales.

Estado final: **APROBADO para entrega**, con las limitaciones de ejecucion Docker/Azure declaradas anteriormente.
