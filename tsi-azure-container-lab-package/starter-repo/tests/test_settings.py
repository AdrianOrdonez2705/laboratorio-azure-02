from app.settings import get_settings


def test_settings_use_safe_defaults(monkeypatch):
    for name in ("APP_ENV", "APP_VERSION", "MODEL_PATH", "LOG_LEVEL"):
        monkeypatch.delenv(name, raising=False)

    settings = get_settings()

    assert settings.app_env == "development"
    assert settings.app_version == "1.0"
    assert settings.model_path == "model/model.joblib"
    assert settings.log_level == "INFO"


def test_environment_overrides_settings(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("APP_VERSION", "2.0")
    monkeypatch.setenv("MODEL_PATH", "/tmp/custom-model.joblib")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")

    settings = get_settings()

    assert settings.app_env == "production"
    assert settings.app_version == "2.0"
    assert settings.model_path == "/tmp/custom-model.joblib"
    assert settings.log_level == "WARNING"
