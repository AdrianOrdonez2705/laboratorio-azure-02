from pathlib import Path


STARTER_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = STARTER_ROOT.parent


def test_student_readme_points_to_real_lab_assets():
    text = (STARTER_ROOT / "README.md").read_text()
    for token in (
        "python scripts/train_model.py",
        "python -m pytest -v",
        "docker build -t tsi-intelligent-api:v1 .",
        "scripts/smoke_local.ps1",
        "docs/azure-deployment-runbook-template.md",
        ".claude/skills/azure-deploy-check/SKILL.md",
    ):
        assert token in text


def test_quick_start_exists_above_starter_repo_and_names_word_guide():
    text = (PACKAGE_ROOT / "README_INICIO_RAPIDO.md").read_text()
    assert "Guia_Estudiante_Lab_Azure_ContainerApps_IA_TSI.docx" in text
    assert "starter-repo" in text
