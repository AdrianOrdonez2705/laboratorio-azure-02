param([string]$BaseUrl = "https://REEMPLAZAR.azurecontainerapps.io")
$ErrorActionPreference = "Stop"
if (-not $BaseUrl.StartsWith("https://") -or $BaseUrl.Contains("REEMPLAZAR")) {
    throw "Uso: .\scripts\smoke_cloud.ps1 -BaseUrl https://<fqdn>.azurecontainerapps.io"
}
Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "$BaseUrl/ready" -Method Get | ConvertTo-Json -Compress
$body = @{ feature_1 = 0.25; feature_2 = 0.75; feature_3 = -0.10 } | ConvertTo-Json
Invoke-RestMethod -Uri "$BaseUrl/predict" -Method Post -ContentType "application/json" -Body $body | ConvertTo-Json -Compress
