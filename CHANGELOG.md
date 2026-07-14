---
runme:
  id: 01HJQ7JXMD6NADWWC23SR9W42S
  version: v3
---

# RELEASE

## [1.0.0] - 2026-07-13
### ⚠️ BREAKING CHANGE (nivel Dockerfile)
- La imagen Docker deja de ser la imagen de runtime de la librería `aia-utils` y
  pasa a ser la **imagen base reutilizable** `keitarodxs/aia-utils-base` para los
  proyectos del ecosistema aia (ej. aia-mcp).
- **Base**: `python:3.11` (con `iputils-ping`/`vim`) → `python:3.13-slim` (mínima).
- **Instalador**: `pip install poetry` → se añade `uv` (`uv pip install --system`,
  10-100x más rápido). Poetry se mantiene solo para `poetry export`.
- **Sistema**: se añaden `git`, `curl`, `ca-certificates`, `build-essential`, `gcc`
  (requeridos por los proyectos hijo).
- **Node**: se añade Node.js 20 + `drawio-mcp-server@2.2.0` (requerido por aia-mcp).
- **No instala** el paquete `aia-utils` ni sus deps: cada proyecto hijo lo hace en
  su propio `Dockerfile` con `FROM keitarodxs/aia-utils-base:<tag>`.
- Workflow `docker-image.yml`: publica `keitarodxs/aia-utils-base` con `TAG_NAME`
  del release y multi-arquitectura (`linux/amd64,linux/arm64`).
- Se genera `poetry.lock` (faltaba en el repo).

## [0.4.6] - 2024-06-18
### Added
- ✨ Feature: Add TTL (Time To Live) support for HTTP cache
- 🔧 New environment variable AIA_HTTP_CACHE_TTL to configure cache expiration time

## [0.4.5] - 2024-06-17
### Added
- ✅ Build version 0.4.3
- ✅ This version now supports Python 3.11

## [0.4.0] - 2025-06-16
### Added
- ✨ Feature: Add MongoDB caching support to AiaHttpClient
- 🔄 Update Python version to 3.13.5
- 🔄 Update dependencies to latest compatible versions
- 🧪 Enhanced test coverage for AiaHttpClient

## [0.3.13] - 2025-06-16
### Updated
- 🔄 Update GithubActions to use pypa/gh-action-pypi-publish@v1.8.0
- 🔄 Update GithubActions Python version to 3.13.5
- 🔄 Update GithubActions Poetry version to 2.1.1

## [0.3.8] - 2025-06-16
### Fixed
- 🐞 Fix Github Actions python publish

## [0.3.7] - 2025-06-16
### Added
- 🔄 Updated Python version to 3.13.5 in the Dockerfile.
- 🔄 Updated confluent-kafka version to 2.5.3.
- 🔄 Updated pillow version to 10.2.0.
- 🔃 Migrated dev-dependencies to the recommended Poetry section.

## [0.3.6] - 2025-06-16
### Added
- 🧪 Test AiaHttpClient (gemini ia url)
- 🔄 Updated Python version to 3.13.
- 🔄 Updated confluent-kafka version to 2.5.3.
- 🔄 Updated pillow version to 10.2.0.
- 🔃 Migrated dev-dependencies to the recommended Poetry section.

## [0.3.5] 26-sep-2024

- 🔄 Updating confluent-kafka (2.3.0 -> 2.5.3)

## [0.3.4] 25-sep-2024

- ✨ Feature: Add mqtt consumer topic

## [0.3.3] 13-ago-2024

- 🔥 Hotfix add config 'auto.offset.reset': 'earliest' to queue Consumer

## [0.3.2] 13-ago-2024

- 🔥 Hotfix config ConsumerKafka, add group clientId to NO auth

## [0.3.1] 13-ago-2024

- ✨🔧 Add support Queue no auth using env var CLOUDKAFKA_ANONIMOUS_ACCESS=True

## [0.3.0] 12-ago-2024

- ✨ Feature: Add clientId in queue->KafkaClient
- 🆕 Feature: AiaHttpClient

## [0.2.2] 01-ago-2024

## [0.2.1] 31-jul-2024

- 🔄 Update: get_aia_version
- ✨ Feature: Add mqtt client

## [0.1.16] 29-ene-2024

- ✨ Feature: generate_manifest

## [0.1.15] 28-ene-2024

- 🔄 Dockerfile: Add poetry, vim, ping

## [0.1.14] 24-ene-2024

- 🔧 Change docker hub repo to keitarodxs/aia-utils:<tag>
- ✨ Githubactions -> Add new dockerhub push

## [0.1.13] 23-ene-2024

- ✨ Githubactions -> add workflow to publish to pypi

## [0.1.12] 22-ene-2024

- ✨ Feature: Add getVersion(file_toml)

## [0.1.11] 21-ene-2024

- ✨ Feature: Add queue listener flag validateJson default True

## [0.1.8] 10-ene-2024

- ✨ Feature: html2img return img obj
- 🐛🔧 Fix: add log.error in Queue

## [0.1.7] 08-ene-2024

- ✨ Feature: html2img

## [0.1.6] First Version 28-dic-2023

- ✨ Feature: aia msg repo
- ✨ Feature: aia semantic repo
- ✨ logger Feature
- ✨ Queue Kafka Producer-Consumer
- ✨ Add AIA Model

## [0.4.7] - 2024-06-18
### Added
- ✅ Add tests for HTTP cache with TTL
- 🐛 Fix datetime handling in cache expiration
- 🚫 Skip OpenAI test by default


