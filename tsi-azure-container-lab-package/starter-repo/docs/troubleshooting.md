# Troubleshooting del laboratorio

## Docker build falla
1. Lea el primer error real, no solo la ultima linea.
2. Verifique que esta en la raiz del repositorio.
3. Ejecute `python -m pytest -v` antes de volver a construir.
4. Compruebe que `model/model.joblib` existe.
5. Pida a la IA un diagnostico, no una reescritura completa.

## `az acr login` falla
- Confirme `az login` y `az account show`.
- Verifique que el nombre usado es el nombre del recurso ACR, no una URL completa.
- Compruebe permisos sobre el registro.

## `docker push` devuelve UNAUTHORIZED
- Ejecute nuevamente `az acr login --name <ACR_NAME>`.
- Confirme que la imagen esta etiquetada con el `loginServer` correcto.
- No active el usuario admin solo para "hacer que funcione" sin autorizacion docente.

## Container App no arranca
- Revise `az containerapp logs show`.
- Verifique puerto objetivo 8000.
- Verifique `MODEL_PATH=/app/model/model.joblib`.
- Compruebe que la identidad administrada tiene `AcrPull` sobre el ACR.

## `/health` funciona pero `/ready` falla
La aplicacion esta viva, pero el modelo no esta cargado. Revise `MODEL_PATH`, contenido de la imagen y logs de inicio.

## `/predict` devuelve 422
La API rechazo el payload. Los tres campos son obligatorios, numericos y deben estar entre -10 y 10.

## Cambio v2 no aparece
- Confirme que hizo push de `:v2`.
- Confirme que `az containerapp update` apunta al tag v2.
- Liste revisiones con `az containerapp revision list`.
- Consulte la URL nuevamente y revise `/` o `/predict` para observar la version.
