FROM ghcr.io/astral-sh/uv:0.9-python3.13-bookworm-slim@sha256:60d8ee2c1f7ffce050822adcb44907514e39f29d2d7b37732e8fca9f4f6113af

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" --home /nonroot --uid 10001 appuser
 
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY app ./app

RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=6969 \
    WEB_CONCURRENCY=2
    
EXPOSE 6969

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -fsS "http://127.0.0.1:${PORT}/health" || exit 1
  
CMD ["sh", "-c", "uv run gunicorn -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:${PORT:-6969} app:app"]
