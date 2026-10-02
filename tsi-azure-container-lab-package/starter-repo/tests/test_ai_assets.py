from pathlib import Path


def test_deploy_skill_has_required_gate_language():
    text = Path(".claude/skills/azure-deploy-check/SKILL.md").read_text()
    assert "READY FOR DEPLOYMENT" in text
    assert "BLOCKED" in text
    assert "No ejecutar despliegues" in text
    assert "No eliminar recursos" in text


def test_generic_prompts_are_vendor_neutral_and_plan_first():
    prompt_dir = Path("prompts")
    prompts = sorted(prompt_dir.glob("*.md"))
    assert len(prompts) == 4
    combined = "\n".join(p.read_text() for p in prompts)
    assert "Claude Code" not in combined
    assert "No modifiques" in combined
    assert "evidencia" in combined.lower()


def test_ai_assets_do_not_contain_obvious_secrets():
    paths = [Path("CLAUDE.md"), *Path("prompts").glob("*.md"), Path(".claude/skills/azure-deploy-check/SKILL.md")]
    text = "\n".join(p.read_text() for p in paths)
    lowered = text.lower()
    assert "sk-" not in text
    assert "password=" not in lowered
    assert "api_key=" not in lowered
