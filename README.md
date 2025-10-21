<div align="center">
<img src="docs/assets/logo.png" align="center" width="144px" height="144px"/>

### 3D Print Cost Calculators

_A small Flask application that provides cost calculators for resin and FDM 3D printing. Built with uv for reproducible Python environments and designed to run locally or in a container._
</div>

<div align="center">

[![Docker](https://img.shields.io/github/v/tag/sudo-kraken/3d-printing-cost-calculators?label=docker&logo=docker&style=for-the-badge)](https://github.com/sudo-kraken//3d-printing-cost-calculators/pkgs/container//3d-printing-cost-calculators) [![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fsudo-kraken%2F/3d-printing-cost-calculators%2Fmain%2Fpyproject.toml&logo=python&logoColor=yellow&color=3776AB&style=for-the-badge)](https://github.com/sudo-kraken/3d-printing-cost-calculators/blob/main/pyproject.toml)
</div>

<div align="center">

[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/sudo-kraken/3d-printing-cost-calculators?label=openssf%20scorecard&style=for-the-badge)](https://scorecard.dev/viewer/?uri=github.com/sudo-kraken/3d-printing-cost-calculators)

</div>

## Demo
<div align="center">
  
![Demo](docs/assets/preview.gif)  
*Animation shows the basic functionality of the application*
</div>

## Contents

- [Overview](#overview)
- [Architecture at a glance](#architecture-at-a-glance)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
- [Docker](#docker)
- [Configuration](#configuration)
- [Health](#health)
- [Endpoints](#endpoints)
- [Production notes](#production-notes)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Licence](#licence)
- [Security](#security)
- [Contributing](#contributing)
- [Support](#support)

## Overview

This service exposes simple web pages to calculate material and job costs for resin and FDM 3D prints. It includes a basic health endpoint for orchestration systems and uses a plain Flask entry point that works with Flask’s dev server or Gunicorn in production.

## Architecture at a glance

- Flask app factory with a top level `app:app` WSGI target
- Stateless HTTP endpoints and HTML templates
- Optional branding via environment variables
- Health endpoint `GET /health` for liveness checks

## Features

- Resin and FDM cost calculators with simple and advanced views
- Configurable branding, logo and favicon
- Single business control for default profit margin
- Clean `app:app` entry point compatible with Flask and Gunicorn
- `/health` endpoint for liveness checks
- Reproducible local development with uv
- Ready to run via a prebuilt container image

## Prerequisites

- [Docker](https://www.docker.com/) / [Kubernetes](https://kubernetes.io/)
- Alternatively [uv](https://docs.astral.sh/uv/) and Python 3.13 for local development

## Quick start

Local development with uv

```bash
uv sync --all-extras
uv run flask --app app:app run --host 0.0.0.0 --port ${PORT:-6969}
```

## Docker

Pull and run

```bash
docker pull ghcr.io/sudo-kraken/3d-printing-cost-calculators:latest
docker run --rm -p 6969:6969 \
  -e PORT=6969 \
  ghcr.io/sudo-kraken/3d-printing-cost-calculators:latest
```
## Kubernetes (Helm)

You can deploy the app on Kubernetes using the published Helm chart:

```bash
helm install 3d-printing-cost-calculators oci://ghcr.io/sudo-kraken/helm-charts/3d-printing-cost-calculators \
  --namespace 3d-printing-cost-calculators --create-namespace
```

Docker Compose example

```yaml
services:
  calculators:
    image: ghcr.io/sudo-kraken/3d-printing-cost-calculators:latest
    environment:
      PORT: 6969
      WEB_CONCURRENCY: 2
    ports:
      - "6969:6969"
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:6969/health"]
      interval: 30s
      timeout: 5s
      retries: 3
```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PORT | no | 6969 | Port to bind |
| WEB_CONCURRENCY | no | 2 | Gunicorn worker processes |
| APP_BRAND_NAME | no |  | Branding string used in templates |
| APP_LOGO_URL | no |  | Logo URL used in templates |
| APP_FAVICON_URL | no |  | Favicon URL |
| APP_DEFAULT_PROFIT_MARGIN | no |  | Default profit margin percentage |

`.env` example

```dotenv
PORT=6969
WEB_CONCURRENCY=2
APP_BRAND_NAME="My Print Shop"
APP_DEFAULT_PROFIT_MARGIN=20
```

## Health

- `GET /health` returns `{ "ok": true }`

## Endpoints

- `GET /` home
- `GET /resin-calculator` and `GET /resin-simple`
- `GET /fdm-calculator` and `GET /fdm-simple`
- `POST /calculate-resin`
- `POST /calculate-fdm`

## Production notes

- Prefer Gunicorn with multiple workers for CPU bound tasks. For simple IO bound routes the default of 2 workers is fine.
- Expose the `/health` endpoint to your load balancer or orchestrator for liveness checks.

## Development

```bash
uv run ruff check --fix .
uv run ruff format .
uv run pytest --cov
```

## Troubleshooting

- If templates fail to load, ensure the `templates/` and `static/` folders are included in the container image.
- If you change dependencies, regenerate `uv.lock` with `uv lock` and commit it.

## Licence

This project is licensed under the MIT Licence. See the [LICENCE](LICENCE) file for details.

## Security

If you discover a security issue, please review and follow the guidance in [SECURITY.md](SECURITY.md), or open a private security-focused issue with minimal details and request a secure contact channel.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions or improvements.  
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

Open an [issue](/../../issues) with as much detail as possible, including your environment details and relevant logs or output.
