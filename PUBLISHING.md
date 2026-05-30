# Publish courier to PyPI

Package: **nkscoder-courier** (Django app name stays `courier`)  
PyPI account: [pypi.org/manage/account](https://pypi.org/manage/account/)

> **Note:** The name `courier` is already taken on PyPI by another project. This package publishes as **`nkscoder-courier`**.

---

## 1. Create a PyPI account

1. Register at [pypi.org/account/register](https://pypi.org/account/register/)
2. Verify your email
3. Open [pypi.org/manage/account](https://pypi.org/manage/account/)

---

## 2. Create an API token

1. Go to [pypi.org/manage/account/token](https://pypi.org/manage/account/token/)
2. Click **Add API token**
3. Scope: **Entire account** (first upload) or project `nkscoder-courier` after first upload
4. Copy the token (`pypi-...`) — you will not see it again

---

## 3. Add token to GitHub

1. Open https://github.com/nkscoder/courier  
2. **Settings** → **Secrets and variables** → **Actions**  
3. **New repository secret**  
   - Name: `PYPI_API_TOKEN`  
   - Value: your PyPI token  
4. Save  

---

## 4. Publish

### Option A — GitHub Actions (recommended)

**Actions** → **Publish to PyPI** → **Run workflow**

Or create a release with tag `v1.1.1` matching `version` in `pyproject.toml`.

### Option B — Upload from your machine

```bash
pip install build twine
python -m build
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
twine upload dist/*
```

Check: https://pypi.org/project/nkscoder-courier/

---

## Install after publish

```bash
pip install nkscoder-courier
```

```python
INSTALLED_APPS = ["courier"]
```
