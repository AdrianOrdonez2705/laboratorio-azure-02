from pathlib import Path


def test_dockerfile_has_required_safety_and_health_properties():
    text = Path("Dockerfile").read_text()
    assert "FROM python:3.12-slim" in text
    assert "USER appuser" in text
    assert "EXPOSE 8000" in text
    assert "HEALTHCHECK" in text
    assert "/health" in text
    assert "COPY . ." not in text


def test_dockerignore_excludes_sensitive_and_transient_files():
    entries = set(Path(".dockerignore").read_text().splitlines())
    for required in {".env", ".git", ".venv", "__pycache__", ".pytest_cache", "tests"}:
        assert required in entries
