from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings
from scripts.train_model import train_and_save


def test_ready_reports_false_when_model_missing(tmp_path):
    settings = Settings("test", "1.0", str(tmp_path / "missing.joblib"), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.get("/ready")
    assert response.status_code == 503
    assert response.json() == {"detail": {"status": "not_ready", "model_loaded": False}}


def test_ready_reports_true_when_model_loaded(tmp_path):
    model_path = train_and_save(tmp_path / "model.joblib")
    settings = Settings("test", "1.0", str(model_path), "INFO")
    with TestClient(create_app(settings)) as client:
        response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "model_loaded": True}
