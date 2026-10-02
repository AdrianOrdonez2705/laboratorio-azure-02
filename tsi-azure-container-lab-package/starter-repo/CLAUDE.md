# Reglas del proyecto TSI

## Flujo de trabajo
- Leer primero `README.md`, la tarea del laboratorio y los archivos que se van a modificar.
- Antes de editar, inspeccionar el repositorio, explicar riesgos y proponer un plan corto.
- Implementar cambios pequeños y verificables; no reescribir archivos sin necesidad.
- Reportar siempre archivos modificados, comandos ejecutados, resultado exacto y errores pendientes.

## Seguridad
- No leer, copiar, mostrar ni escribir secretos reales.
- No crear ni versionar `.env` con credenciales.
- No incrustar tokens, passwords, connection strings ni claves API en Dockerfile, codigo o documentacion.
- No ejecutar borrado de recursos Azure sin autorizacion explicita del estudiante/docente.
- No usar modos que omitan permisos o confirmaciones de seguridad.

## Verificacion
Antes de declarar un cambio listo, segun corresponda:
1. `python -m pytest -v`
2. `python scripts/train_model.py`
3. `docker build -t tsi-intelligent-api:v1 .`
4. ejecutar `scripts/smoke_local.ps1` o `.sh`
5. ejecutar `trivy image tsi-intelligent-api:v1` o escaner equivalente

"La IA dice que funciona" no es evidencia. La evidencia es la salida verificable de pruebas, build, smoke tests, escaneo, Azure CLI/Portal, logs y URL HTTPS.
