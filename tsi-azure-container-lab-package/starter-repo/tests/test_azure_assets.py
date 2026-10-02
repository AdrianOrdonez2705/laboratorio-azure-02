from pathlib import Path


def test_preflight_scripts_require_names_before_resource_creation():
    ps = Path("scripts/azure_preflight.ps1").read_text()
    sh = Path("scripts/azure_preflight.sh").read_text()
    for name in ("RESOURCE_GROUP", "LOCATION", "ACR_NAME", "CONTAINER_APP_ENV", "CONTAINER_APP_NAME"):
        assert name in ps
        assert name in sh
    assert "az group create" not in ps
    assert "az group create" not in sh


def test_runbook_uses_managed_identity_and_has_guarded_cleanup():
    text = Path("docs/azure-deployment-runbook-template.md").read_text()
    assert "az identity create" in text
    assert "AcrPull" in text
    assert "--registry-identity" in text
    assert "SOLO CON AUTORIZACION DEL DOCENTE" in text
    assert "az group delete" in text


def test_cloud_smoke_scripts_only_call_https_api():
    ps = Path("scripts/smoke_cloud.ps1").read_text()
    sh = Path("scripts/smoke_cloud.sh").read_text()
    assert "https://" in ps
    assert "https://" in sh
    assert "/health" in ps and "/ready" in ps and "/predict" in ps
    assert "/health" in sh and "/ready" in sh and "/predict" in sh


def test_runbook_prepares_container_apps_cli_and_resource_providers():
    runbook = Path("docs/azure-deployment-runbook-template.md").read_text()
    ps = Path("scripts/azure_preflight.ps1").read_text()
    sh = Path("scripts/azure_preflight.sh").read_text()
    assert "az extension add --name containerapp --upgrade" in runbook
    assert "az provider register --namespace Microsoft.App" in runbook
    assert "az provider register --namespace Microsoft.OperationalInsights" in runbook
    assert "az containerapp --help" in ps
    assert "az containerapp --help" in sh


def test_runbook_runs_preflight_after_login_and_provider_registration():
    text = Path("docs/azure-deployment-runbook-template.md").read_text()
    preflight = text.index("azure_preflight.ps1")
    assert text.index("az login") < preflight
    assert text.index("az provider register --namespace Microsoft.App --wait") < preflight
