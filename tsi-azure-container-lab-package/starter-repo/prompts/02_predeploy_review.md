# Prompt 02 - Revision antes de desplegar

Revisa el proyecto como si fuera a desplegarse en Azure Container Apps.

No modifiques archivos ni ejecutes acciones Azure destructivas.

Comprueba, cuando las herramientas esten disponibles: tests, Dockerfile, .dockerignore, variables, manejo de secretos, usuario no-root, /health, /ready, /predict, modelo, smoke tests y escaneo de imagen.

Devuelve una tabla con: check, evidencia ejecutada, resultado, riesgo y accion. Finaliza con READY FOR DEPLOYMENT o BLOCKED. No uses como evidencia una afirmacion de la propia IA.
