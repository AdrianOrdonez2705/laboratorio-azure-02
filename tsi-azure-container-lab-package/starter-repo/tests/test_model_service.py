from pathlib import Path

from app.model_service import ModelService
from scripts.train_model import train_and_save


def test_missing_model_is_not_ready(tmp_path):
    service = ModelService(tmp_path / "missing.joblib")
    service.load()
    assert service.is_ready() is False


def test_generated_model_loads_and_predicts(tmp_path):
    model_path = tmp_path / "model.joblib"
    train_and_save(model_path)

    service = ModelService(model_path)
    service.load()
    prediction, confidence = service.predict([0.25, 0.75, -0.10])

    assert service.is_ready() is True
    assert prediction in {"low", "high"}
    assert isinstance(confidence, float)
    assert 0.0 <= confidence <= 1.0
