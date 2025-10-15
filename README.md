# 3D Print Calculators

Flask application that provides cost calculators for resin and FDM 3D printing. Managed with uv and container friendly.

## Features
- Resin and FDM cost calculators with simple and advanced views
- Configurable branding, logo and favicon
- Single business control for default profit margin
- `/health` endpoint for liveness checks
- Tests with pytest and coverage
- Works with uv locally or Docker

## Requirements
- Python 3.13 with [uv](https://docs.astral.sh/uv/)
- Docker optional

## Quick start with uv
```bash
uv sync --all-extras
uv run flask --app app:app run --host 0.0.0.0 --port ${PORT:-6969}
# or Gunicorn
uv run --no-dev gunicorn -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:${PORT:-6969} app:app
```

## Docker
```bash
docker run --rm -e PORT=6969 -p 6969:6969 ghcr.io/sudo-kraken/3d-printing-cost-calculators:latest
# For compose use see the repo example
```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PORT | no | 6969 | Port to bind |
| WEB_CONCURRENCY | no | 2 | Gunicorn workers |
| APP_BRAND_NAME | no |  | Branding in templates |
| APP_LOGO_URL | no |  | Logo used in templates |
| APP_FAVICON_URL | no |  | Favicon |
| APP_DEFAULT_PROFIT_MARGIN | no |  | Default profit margin percent |

## Health and readiness
- `GET /health` returns `{ "ok": true }`.

## Endpoints
- `GET /` index
- `GET /resin-calculator`, `GET /resin-simple`
- `GET /fdm-calculator`, `GET /fdm-simple`
- `POST /calculate-resin` and `POST /calculate-fdm`

## Project layout
```
3d-printing-cost-calculators/
  app/
  templates/
  static/
  Dockerfile
  pyproject.toml
  tests/
```

## Development
```bash
uv run ruff check --fix .
uv run ruff format .
uv run pytest --cov
```

## Licence
See [LICENSE](LICENSE)

## Security
See [SECURITY.md](SECURITY.md)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support
Open an [issue](/../../issues)
