from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str
    app_version: str
    model_path: str
    log_level: str


def get_settings() -> Settings:
    """Read runtime configuration from environment variables with safe defaults."""
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        app_version=os.getenv("APP_VERSION", "1.0"),
        model_path=os.getenv("MODEL_PATH", "model/model.joblib"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
