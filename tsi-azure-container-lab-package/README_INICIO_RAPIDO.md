# Inicio rapido - Laboratorio Azure Container Apps + IA

## Contenido del paquete

- `Guia_Estudiante_Lab_Azure_ContainerApps_IA_TSI.docx`: guia didactica completa.
- `starter-repo/`: proyecto listo para abrir en VS Code.
- `starter-repo/prompts/`: prompts para Claude Code u otra IA.
- `starter-repo/.claude/skills/azure-deploy-check/SKILL.md`: Skill de revision de predespliegue para Claude Code.
- `starter-repo/docs/`: runbook, evidencia, troubleshooting y seguridad.

## Secuencia minima

1. Descomprima el paquete.
2. Abra `starter-repo` en VS Code.
3. Prepare Python 3.12 y dependencias.
4. Ejecute `python scripts/train_model.py`.
5. Ejecute `python -m pytest -v`.
6. Ejecute la API y el smoke test local.
7. Revise el proyecto con IA en modo analisis/plan.
8. Construya `docker build -t tsi-intelligent-api:v1 .`.
9. Ejecute el contenedor y `scripts/smoke_local.ps1`.
10. Siga la guia Word para ACR y Azure Container Apps.

No cree recursos Azure si el costo, region o SKU no estan autorizados por el docente.
