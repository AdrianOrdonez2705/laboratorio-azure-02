param(
    [string]$BaseUrl = "http://localhost:8000"
)
$ErrorActionPreference = "Stop"

Write-Host "[1/3] GET $BaseUrl/health"
Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get | ConvertTo-Json -Compress

Write-Host "[2/3] GET $BaseUrl/ready"
Invoke-RestMethod -Uri "$BaseUrl/ready" -Method Get | ConvertTo-Json -Compress

Write-Host "[3/3] POST $BaseUrl/predict"
$body = @{ feature_1 = 0.25; feature_2 = 0.75; feature_3 = -0.10 } | ConvertTo-Json
Invoke-RestMethod -Uri "$BaseUrl/predict" -Method Post -ContentType "application/json" -Body $body | ConvertTo-Json -Compress
