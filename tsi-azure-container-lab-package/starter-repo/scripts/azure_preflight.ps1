$ErrorActionPreference = "Stop"

$required = @("AZ_SUBSCRIPTION", "RESOURCE_GROUP", "LOCATION", "ACR_NAME", "CONTAINER_APP_ENV", "CONTAINER_APP_NAME")
$missing = @()
foreach ($name in $required) {
    $value = [Environment]::GetEnvironmentVariable($name)
    if ([string]::IsNullOrWhiteSpace($value)) { $missing += $name }
}
if ($missing.Count -gt 0) {
    throw "Faltan variables requeridas: $($missing -join ', ')"
}

foreach ($tool in @("az", "docker")) {
    if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "$tool no esta instalado o no esta en PATH"
    }
}

az containerapp --help *> $null
if ($LASTEXITCODE -ne 0) {
    throw "Falta la extension de Azure Container Apps. Ejecute: az extension add --name containerapp --upgrade"
}

try { $account = az account show | ConvertFrom-Json } catch { throw "No hay sesion Azure activa. Ejecute: az login" }
if ($account.id -ne $env:AZ_SUBSCRIPTION) {
    throw "La suscripcion activa no coincide. Ejecute: az account set --subscription `"$env:AZ_SUBSCRIPTION`""
}

foreach ($provider in @("Microsoft.App", "Microsoft.OperationalInsights")) {
    $state = az provider show --namespace $provider --query registrationState -o tsv
    if ($LASTEXITCODE -ne 0 -or $state.Trim() -ne "Registered") {
        throw "Proveedor $provider no registrado. Ejecute: az provider register --namespace $provider --wait"
    }
}

docker info *> $null
if ($LASTEXITCODE -ne 0) { throw "Docker esta instalado pero el daemon no responde." }

Write-Host "PRE-FLIGHT OK"
Write-Host "Subscription: $env:AZ_SUBSCRIPTION"
Write-Host "Resource Group: $env:RESOURCE_GROUP"
Write-Host "Location: $env:LOCATION"
Write-Host "ACR: $env:ACR_NAME"
Write-Host "Container Apps Environment: $env:CONTAINER_APP_ENV"
Write-Host "Container App: $env:CONTAINER_APP_NAME"
