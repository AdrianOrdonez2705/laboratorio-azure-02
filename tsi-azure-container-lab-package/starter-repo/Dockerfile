FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    APP_ENV=production \
    APP_VERSION=1.0 \
    MODEL_PATH=/app/model/model.joblib \
    LOG_LEVEL=INFO

WORKDIR /app

# Install runtime dependencies before copying application code to maximize layer cache reuse.
COPY pyproject.toml /app/pyproject.toml
RUN python - <<'PY'
import subprocess, sys, tomllib
with open('/app/pyproject.toml', 'rb') as fh:
    deps = tomllib.load(fh)['project']['dependencies']
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', *deps])
PY

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup app /app/app
COPY --chown=appuser:appgroup model /app/model

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()" || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
