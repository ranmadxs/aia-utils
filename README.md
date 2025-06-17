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

```python {"id":"01HJV66J6EV6K8ECD6KNMET9KM"}
#set var entorno
export AIA_TAG_UTILS=0.4.0
```

```sh {"id":"01HJV64NSH238T2X9KXSA1A4FW"}
#build
docker build . --platform linux/arm64/v8 -t keitarodxs/aia-utils:$AIA_TAG_UTILS

#push
docker push keitarodxs/aia-utils:$AIA_TAG_UTILS
```
