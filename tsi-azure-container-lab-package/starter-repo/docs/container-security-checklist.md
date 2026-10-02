# Checklist de seguridad y reproducibilidad del contenedor

Antes de publicar una imagen del laboratorio, compruebe:

- [ ] La base usa Python 3.12 slim y no una imagen de desarrollo completa.
- [ ] Las dependencias se instalan antes de copiar el codigo para aprovechar cache de capas.
- [ ] `.dockerignore` excluye `.env`, `.git`, `.venv`, caches y archivos de prueba.
- [ ] El Dockerfile no contiene tokens, passwords, connection strings ni claves API.
- [ ] La aplicacion se ejecuta como usuario no-root (`appuser`).
- [ ] El puerto expuesto es 8000.
- [ ] `HEALTHCHECK` consulta `/health`.
- [ ] `/ready` valida que el modelo realmente fue cargado.
- [ ] `docker build -t tsi-intelligent-api:v1 .` finaliza sin error.
- [ ] `scripts/smoke_local.ps1` o `.sh` valida `/health`, `/ready` y `/predict`.
- [ ] Se ejecuta `trivy image tsi-intelligent-api:v1` (o escaner equivalente) y se interpretan los hallazgos.

## Como interpretar Trivy

No se exige "cero vulnerabilidades" como consigna automatica. Registre severidad, paquete afectado, version instalada, version corregida si existe y la decision del equipo. Priorice vulnerabilidades explotables y dependencias realmente usadas por la aplicacion.
