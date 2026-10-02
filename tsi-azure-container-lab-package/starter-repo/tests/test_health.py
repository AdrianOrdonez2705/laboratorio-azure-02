from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


def test_health_is_independent_of_model(tmp_path):
    settings = Settings("test", "1.0", str(tmp_path / "missing.joblib"), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
