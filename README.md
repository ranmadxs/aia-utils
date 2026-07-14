---
runme:
  id: 01HJV60F4EW988YE9KMJFSTDTY
  version: v3
---

# aia-utils

AIA Utils repo (Notifications, Errors, Helpers) for Amanda Inteligence Artificial

git ls-remote --get-url origin
git remote set-url origin git@github_ranmadxs:ranmadxs/aia-utils.git

## Use local dev

```sh {"id":"01HJV60F4EW988YE9KMGH6GQ66"}

poetry add ../aia-utils/

poetry run pip install -U aia-utils==$AIA_TAG_UTILS

```

### Result

```python {"id":"01HJV60F4EW988YE9KMHTHYHH2"}
[tool.poetry.dependencies]
aia-utils = {path = "../my/path", develop = true}
```

### Publish

```python {"id":"01HKNX07Y6Y05A7PQ1W95AGV8K"}
poetry build 
poetry publish
```

### GIT

```sh {"id":"01HKS37PDVKE6JX3EZ4TVSAYYF"}
git push --tags
```

### Docker

> ⚠️ **Breaking change (nivel Dockerfile) en 1.0.0**: la imagen deja de ser la
> imagen de runtime de la librería y pasa a ser la **imagen base reutilizable**
> `keitarodxs/aia-utils-base` para los proyectos del ecosistema aia (ej. aia-mcp).
> Ya no instala el paquete `aia-utils` ni sus dependencias; eso lo hace cada
> proyecto hijo en su propio `Dockerfile`.

```python {"id":"01HJV66J6EV6K8ECD6KNMET9KM"}
#set var entorno
export AIA_TAG_UTILS=1.0.0
```

```sh {"id":"01HJV64NSH238T2X9KXSA1A4FW"}
#build
docker build . --platform linux/amd64 -t keitarodxs/aia-utils-base:$AIA_TAG_UTILS

#push
docker push keitarodxs/aia-utils-base:$AIA_TAG_UTILS
```

#### Usar la imagen base en un proyecto hijo (ej. aia-mcp)

```dockerfile
FROM keitarodxs/aia-utils-base:1.0.0

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --without-hashes --with dev -o /tmp/requirements.txt \
    && uv pip install --system -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

COPY . .
RUN uv pip install --system .
```

La imagen base incluye: Python 3.13-slim, git, curl, ca-certificates,
build-essential/gcc, Poetry (para `poetry export`), `uv` (instalador rápido) y
Node.js 20 + `drawio-mcp-server@2.2.0`.
