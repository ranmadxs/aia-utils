# ─────────────────────────────────────────────────────────────────────────────
# aia-utils — IMAGEN BASE (Dockerfile)
#
# ⚠️  BREAKING CHANGE (nivel Dockerfile): esta imagen deja de ser la imagen de
# runtime de la librería aia-utils y pasa a ser la IMAGEN BASE reutilizable para
# los proyectos del ecosistema aia (ej. aia-mcp).
#
# Cambios respecto a versiones <1.0.0 del Dockerfile:
#   - Base: python:3.11 (con ping/vim)  ->  python:3.13-slim (mínima)
#   - pip install poetry                ->  uv (instalador 10-100x más rápido)
#   - Se añaden git, curl, ca-certificates (requeridos por los proyectos hijos)
#   - Se añade Node.js 20 + drawio-mcp-server (requerido por aia-mcp)
#   - Ya NO instala el paquete aia-utils ni sus deps: eso lo hace cada proyecto
#     hijo en su propio Dockerfile usando `FROM keitarodxs/aia-utils-base:<tag>`.
#
# Uso en un proyecto hijo (ej. aia-mcp):
#   FROM keitarodxs/aia-utils-base:1.0.0
#   COPY pyproject.toml poetry.lock ./
#   RUN poetry export -f requirements.txt --without-hashes --with dev -o /tmp/requirements.txt \
#       && uv pip install --system -r /tmp/requirements.txt \
#       && rm -f /tmp/requirements.txt
#   COPY . .
#   RUN uv pip install --system .
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.13-slim

# Evita prompts interactivos y writes .pyc
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1

# Dependencias del sistema comunes a los proyectos del ecosistema aia:
# - git: requerido por shell server y mangadex-downloader
# - curl / ca-certificates: descargas y TLS
# - build-essential / gcc: compilación de extensiones C (pymongo, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        git \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Poetry: se mantiene solo para `poetry export` (generar requirements.txt desde
# el lock del proyecto hijo). No se usa para instalar deps en la imagen base.
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# uv: instalador de paquetes en Rust, 10-100x más rápido que pip. Los proyectos
# hijos instalan sus deps con `uv pip install --system -r requirements.txt`.
RUN pip install --no-cache-dir uv

# ── Node.js + npm (prerequisito para drawio-mcp-server, usado por aia-mcp) ────
# NodeSource para tener una versión reciente de Node en Debian/Ubuntu slim.
RUN set -eux; \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -; \
    apt-get install -y --no-install-recommends nodejs; \
    rm -rf /var/lib/apt/lists/*; \
    node --version; npm --version

# drawio-mcp-server (global): expone MCP Streamable HTTP en :3000 y WebSocket de
# extensión en :3333. Versión fijada para evitar sorpresas con @latest.
RUN npm install -g drawio-mcp-server@2.2.0 \
    && drawio-mcp-server --help >/dev/null 2>&1 || true

# La imagen es SOLO base: no define CMD/ENTRYPOINT ni copia código. Cada
# proyecto hijo define su propio arranque.