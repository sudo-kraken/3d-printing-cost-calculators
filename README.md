# 3D Print Calculators

Flask application that provides cost calculators for resin and FDM 3D printing. The project is managed and run with `uv`.

## Features

- Resin and FDM cost calculators with clear inputs and results
- Simple and advanced pages for each calculator
- Configurable branding, logo and favicon
- Single business control for default profit margin
- Health endpoint for containers and uptime checks
- Tests with `pytest` and coverage
- Dockerfile and an example Docker Compose file
- Works with `uv` locally and in CI

## Requirements

- Python 3.13 or later
- `uv` (https://docs.astral.sh/uv/)
- Docker and Docker Compose

> Tip: keep your local Python version in sync with CI and Docker. This repo targets Python 3.13 right now.

## Quick start (local, without Docker)

Install and run with `uv`:

```sh
# Install dependencies into a virtual environment
uv sync --all-extras

# Run in debug with Flask
uv run flask --app app:app run --debug --host 0.0.0.0 --port "${PORT:-6969}"
```

Run with Gunicorn:

```sh
uv run gunicorn -w 2 -b 0.0.0.0:"${PORT:-6969}" app:app
```

Run tests:

```sh
uv run pytest -q
# with coverage
uv run pytest --cov
```

## Configuration

Branding and one business policy value are configurable via environment variables.

| Variable | Purpose | Default |
|---|---|---|
| `APP_BRAND_NAME` | Site title and header | `3D Print Calculators` |
| `APP_LOGO_URL` | Logo image URL used in templates | `/static/logo.png` |
| `APP_FAVICON_URL` | Favicon URL used in templates | `/static/favicon.ico` |
| `APP_DEFAULT_PROFIT_MARGIN` | Default profit margin percent if the request omits `profit_margin` | `20` |
| `PORT` | Port to bind | `6969` |

Only `profit_margin` is read from the environment for calculations. All other calculator inputs must be provided by the request or via the UI.

## Port behaviour

- The container binds Gunicorn to `${PORT}`
- Compose maps `"${PORT}:${PORT}"`

Compose snippet:

```yaml
environment:
  - PORT=${PORT:-6969}
ports:
  - "${PORT:-6969}:${PORT:-6969}"
healthcheck:
  test: ["CMD-SHELL", "curl -fsS http://localhost:${PORT:-6969}/health || exit 1"]
```

Example:

```sh
export PORT=7070
docker compose up -d
# Container and host both serve on 7070
```

Note: `EXPOSE 6969` in the Dockerfile is a documentation hint only. Explicit `ports:` mappings and the Gunicorn bind address control what actually happens at runtime.

## Docker

Build and run directly:

```sh
docker build -t 3d-printing-cost-calculators .
docker run --rm -e PORT=8080 -p 8080:8080 3d-printing-cost-calculators
```

The image honours `PORT` and `WEB_CONCURRENCY` at runtime.

Reproducible builds: if you commit `uv.lock`, you can use `uv sync --frozen` in Docker builds to pin exact versions.

## Docker Compose

See `docker-compose.example.yml`. Example run on host port 7070:

```sh
export PORT=7070
docker compose up -d
```

Example compose service:

```yaml
version: '3.9'
services:
  3d-printing-cost-calculators:
    image: ghcr.io/sudo-kraken/3d-printing-cost-calculators:latest
    # build: .  # uncomment to build locally
    environment:
      - APP_BRAND_NAME=${APP_BRAND_NAME:-3D Print Calculators}
      - APP_LOGO_URL=${APP_LOGO_URL:-/static/logo.png}
      - APP_FAVICON_URL=${APP_FAVICON_URL:-/static/favicon.ico}
      - APP_DEFAULT_PROFIT_MARGIN=${APP_DEFAULT_PROFIT_MARGIN:-20}
      - PORT=${PORT:-6969}
    ports:
      - "${PORT:-6969}:${PORT:-6969}"
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://localhost:${PORT:-6969}/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

## API

- `GET /` renders the index page
- `GET /resin-calculator` and `GET /resin-simple`
- `GET /fdm-calculator` and `GET /fdm-simple`
- `POST /calculate-resin` runs a resin calculation. If `profit_margin` is not provided, `APP_DEFAULT_PROFIT_MARGIN` is applied
- `POST /calculate-fdm` runs a filament calculation. Same rule for `profit_margin`
- `GET /health` returns `{ "ok": true }`
