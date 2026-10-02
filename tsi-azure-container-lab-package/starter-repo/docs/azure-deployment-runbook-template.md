# Runbook - Docker local -> ACR -> Azure Container Apps

> Esta guia usa Azure CLI y privilegia identidad administrada para que Container Apps lea una imagen privada de ACR sin incrustar credenciales. Los nombres, regiones, cuotas, SKUs y opciones del portal pueden cambiar. Use solo recursos autorizados por el docente.

## 0. Preparar Azure CLI para Container Apps

Instale o actualice la extension oficial antes del pre-flight:

```powershell
az extension add --name containerapp --upgrade
```

## 0B. Variables del laboratorio - PowerShell

```powershell
$env:AZ_SUBSCRIPTION="REEMPLAZAR-ID-SUSCRIPCION"
$env:RESOURCE_GROUP="rg-tsi-lab-equipo01"
$env:LOCATION="eastus"
$env:ACR_NAME="tsiacrequipo01"   # solo letras/numeros, globalmente unico
$env:CONTAINER_APP_ENV="cae-tsi-equipo01"
$env:CONTAINER_APP_NAME="ca-tsi-equipo01"
$env:IDENTITY_NAME="id-tsi-equipo01"
$env:IMAGE_NAME="tsi-intelligent-api"
```

En Bash use las mismas variables con `export NOMBRE=valor`.

## 1. Iniciar sesion, registrar proveedores y ejecutar el pre-flight

```powershell
az login
az account set --subscription "$env:AZ_SUBSCRIPTION"
az account show --output table

az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait
```

Ejecute ahora el pre-flight:

```powershell
.\scripts\azure_preflight.ps1
```

En Bash use `bash scripts/azure_preflight.sh`. Debe finalizar con `PRE-FLIGHT OK` antes de crear recursos.

## 2. Crear un unico Resource Group

```powershell
az group create --name "$env:RESOURCE_GROUP" --location "$env:LOCATION"
```

Checkpoint: todo el laboratorio debe quedar dentro de este grupo para facilitar control de costos y limpieza.

## 3. Crear Azure Container Registry

```powershell
az acr create `
  --resource-group "$env:RESOURCE_GROUP" `
  --name "$env:ACR_NAME" `
  --sku Basic `
  --admin-enabled false

az acr login --name "$env:ACR_NAME"
$env:LOGIN_SERVER = az acr show --name "$env:ACR_NAME" --resource-group "$env:RESOURCE_GROUP" --query loginServer -o tsv
```

No continue si Azure muestra un SKU/costo no autorizado por el docente.

## 4. Etiquetar y publicar v1

```powershell
docker tag tsi-intelligent-api:v1 "$env:LOGIN_SERVER/$env:IMAGE_NAME:v1"
docker push "$env:LOGIN_SERVER/$env:IMAGE_NAME:v1"
az acr repository show-tags --name "$env:ACR_NAME" --repository "$env:IMAGE_NAME" --output table
```

## 5. Crear identidad administrada y otorgar AcrPull

```powershell
az identity create `
  --resource-group "$env:RESOURCE_GROUP" `
  --name "$env:IDENTITY_NAME"

$env:IDENTITY_ID = az identity show -g "$env:RESOURCE_GROUP" -n "$env:IDENTITY_NAME" --query id -o tsv
$env:PRINCIPAL_ID = az identity show -g "$env:RESOURCE_GROUP" -n "$env:IDENTITY_NAME" --query principalId -o tsv
$env:ACR_ID = az acr show -g "$env:RESOURCE_GROUP" -n "$env:ACR_NAME" --query id -o tsv

az role assignment create `
  --assignee-object-id "$env:PRINCIPAL_ID" `
  --assignee-principal-type ServicePrincipal `
  --scope "$env:ACR_ID" `
  --role AcrPull
```

Si Azure informa propagacion de permisos, espere brevemente y reintente la creacion del Container App; no cambie a credenciales incrustadas.

## 6. Crear Container Apps Environment

```powershell
az containerapp env create `
  --name "$env:CONTAINER_APP_ENV" `
  --resource-group "$env:RESOURCE_GROUP" `
  --location "$env:LOCATION"
```

## 7. Crear Container App desde la imagen privada

```powershell
az containerapp create `
  --name "$env:CONTAINER_APP_NAME" `
  --resource-group "$env:RESOURCE_GROUP" `
  --environment "$env:CONTAINER_APP_ENV" `
  --image "$env:LOGIN_SERVER/$env:IMAGE_NAME:v1" `
  --target-port 8000 `
  --ingress external `
  --user-assigned "$env:IDENTITY_ID" `
  --registry-identity "$env:IDENTITY_ID" `
  --registry-server "$env:LOGIN_SERVER" `
  --cpu 0.25 `
  --memory 0.5Gi `
  --min-replicas 0 `
  --max-replicas 1 `
  --env-vars APP_ENV=production APP_VERSION=1.0 MODEL_PATH=/app/model/model.joblib LOG_LEVEL=INFO
```

Obtenga el FQDN:

```powershell
$env:FQDN = az containerapp show -g "$env:RESOURCE_GROUP" -n "$env:CONTAINER_APP_NAME" --query properties.configuration.ingress.fqdn -o tsv
$env:BASE_URL = "https://$env:FQDN"
Write-Host $env:BASE_URL
```

## 8. Configurar health probes explicitamente

Azure Container Apps soporta Startup, Liveness y Readiness. Para este laboratorio configure en Azure Portal, dentro del Container App y su contenedor:

- Liveness: HTTP, puerto 8000, ruta `/health`, periodo sugerido 30 s.
- Readiness: HTTP, puerto 8000, ruta `/ready`, periodo sugerido 10 s.
- Startup (opcional): HTTP, puerto 8000, ruta `/ready`, con margen suficiente para cargar el modelo.

Una respuesta HTTP 2xx/3xx indica exito de una probe HTTP. Guarde evidencia de la configuracion. Si la interfaz cambia, busque la configuracion de **Health probes** del contenedor; no sustituya readiness por una simple captura de que el proceso esta "Running".

## 9. Smoke test cloud

```powershell
.\scripts\smoke_cloud.ps1 -BaseUrl $env:BASE_URL
```

Pruebe tambien desde un navegador o telefono si es posible.

## 10. Ver logs y provocar un error controlado

```powershell
az containerapp logs show -g "$env:RESOURCE_GROUP" -n "$env:CONTAINER_APP_NAME" --follow
```

En otra terminal envie un payload invalido:

```powershell
Invoke-WebRequest `
  -Uri "$env:BASE_URL/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"feature_1":99,"feature_2":0,"feature_3":0}' `
  -SkipHttpErrorCheck
```

Espere HTTP 422. Distinga error de validacion de un fallo de despliegue.

## 11. Crear y publicar v2

Construya localmente la misma aplicacion cambiando solo la configuracion de version al ejecutar/desplegar; la imagen se etiqueta v2:

```powershell
docker build -t tsi-intelligent-api:v2 .
docker tag tsi-intelligent-api:v2 "$env:LOGIN_SERVER/$env:IMAGE_NAME:v2"
docker push "$env:LOGIN_SERVER/$env:IMAGE_NAME:v2"

az containerapp update `
  --name "$env:CONTAINER_APP_NAME" `
  --resource-group "$env:RESOURCE_GROUP" `
  --image "$env:LOGIN_SERVER/$env:IMAGE_NAME:v2" `
  --set-env-vars APP_VERSION=2.0
```

Un cambio de imagen o de variables con alcance de revision genera una nueva revision. Liste revisiones:

```powershell
az containerapp revision list -g "$env:RESOURCE_GROUP" -n "$env:CONTAINER_APP_NAME" --output table
```

Vuelva a ejecutar el smoke test y compruebe `model_version: "2.0"` en `/predict`.

## 12. Rollback conceptual

No se ejecuta automaticamente. Identifique el tag v1 y explique como restauraria la imagen anterior mediante `az containerapp update --image ...:v1 --set-env-vars APP_VERSION=1.0`. Si el docente pide practicarlo, registre antes y despues las revisiones.

## 13. Evidencia y runbook
Complete `docs/evidence-template.md` con comandos realmente ejecutados, resultados, URL, tags, revisiones, logs y decisiones humanas.

# PELIGRO - SOLO CON AUTORIZACION DEL DOCENTE

## 14. Limpieza final

**SOLO CON AUTORIZACION DEL DOCENTE.** Este comando elimina el Resource Group completo y todos los recursos del laboratorio:

```powershell
az group delete --name "$env:RESOURCE_GROUP" --yes --no-wait
```

Luego verifique que el grupo desaparecio antes de cerrar la evidencia.

## Referencias oficiales
- Azure Container Registry - autenticacion y push: https://learn.microsoft.com/azure/container-registry/container-registry-get-started-docker-cli
- Azure Container Apps CLI: https://learn.microsoft.com/cli/azure/containerapp
- Health probes: https://learn.microsoft.com/azure/container-apps/health-probes
- Revisiones: https://learn.microsoft.com/azure/container-apps/revisions-manage
