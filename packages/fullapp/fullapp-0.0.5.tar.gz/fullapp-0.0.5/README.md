![PyPI](https://img.shields.io/pypi/v/fullapp)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fullapp)
![GitHub all releases](https://img.shields.io/github/downloads/grumbit/fullapp/total)
[![GitHub license](https://img.shields.io/github/license/grumbit/fullapp)](https://github.com/grumbit/fullapp/blob/master/LICENSE)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/fullapp)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/fullapp)
![PyPI - Status](https://img.shields.io/pypi/status/fullapp)
[![GitHub issues](https://img.shields.io/github/issues/grumbit/fullapp)](https://github.com/grumbit/fullapp/issues)
[![GitHub forks](https://img.shields.io/github/forks/grumbit/fullapp)](https://github.com/grumbit/fullapp/network)
[![GitHub stars](https://img.shields.io/github/stars/grumbit/fullapp)](https://github.com/grumbit/fullapp/stargazers)

# Fullapp Notes  
<!-- omit in toc -->

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Fullapp Notes](#fullapp-notes)
- [Development log](#development-log)
  - [Create minimal app](#create-minimal-app)
    - [Python packages](#python-packages)
    - [Docker test db](#docker-test-db)
    - [Alembic setup](#alembic-setup)
    - [FastAPI setup](#fastapi-setup)
- [Installing](#installing)
- [Usage](#usage)
  - [FastAPI app server](#fastapi-app-server)
- [Notes](#notes)
  - [Connecting to the test DB](#connecting-to-the-test-db)
- [Releasing to PyPI](#releasing-to-pypi)
  - [How I did it this time](#how-i-did-it-this-time)
    - [Initial upload to Test PyPI](#initial-upload-to-test-pypi)
    - [Set up project specific token](#set-up-project-specific-token)
    - [Test uploaded project](#test-uploaded-project)
    - [Add the TestPyPi and PyPi API tokens to the repo](#add-the-testpypi-and-pypi-api-tokens-to-the-repo)

<!-- /code_chunk_output -->

---

This combines the learning from these repos into one app;

- fastapi_play
- alembic_play
- sqlalchemy_play
- pydantic_play

# Development log

## Create minimal app

### Python packages

- Added the following to `requirements.in`;

```txt
alembic
fastapi[all]
pydantic
psycopg2
SQLAlchemy
sqlalchemy[mypy]
```

- Then ran;

```bash
pip-compile requirements.in
pip-compile requirements_dev.in
pip-sync requirements.txt requirements_dev.txt 
```

### Docker test db

- Created `docker-compose.yml` - see the "Connecting to the test DB" section below

- Created the app's test db;

```bash
docker-compose up
```

- Add `db/pgdata` to `.gitignore`

### Alembic setup

- Initialise Alembic;

```bash
alembic init alembic
```

- In `alembic.ini` update config for docker DB;

```ini
sqlalchemy.url = postgresql+psycopg2://play:play@localhost:5440/alembicplay
```

- In `alembic.ini` uncomment file_template line as migration file default naming is pretty awful

```ini
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
```

- Setup Alembic to find the app's ORM by changing `target_metadata = None` in `alembic/env.py` to;

```python
from src.fullapp.apporm import Base
target_metadata = Base.metadata
```

- Added initial ORM file; `src/fullapp/apporm.py`

- Auto-generated migration using metadata created in apporm.py and apply it;

```bash
alembic revision --autogenerate -m "Bring in initial app orm"
alembic upgrade head
```

### FastAPI setup

- Added this to `src/fullapp/myapp.py`;

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

# Installing

- Run;

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install wheel pip-tools
pip-sync requirements.txt requirements_dev.txt
```

- Create the app db;

```bash
docker-compose up
alembic upgrade head
```

# Usage

## FastAPI app server

- Run the app server;

```bash
uvicorn src.fullapp.myapp:app --reload
```

- Open the app server on <http://127.0.0.1:8000>

- Open the auto docs on;
- Interactive: <http://127.0.0.1:8000/docs>
- Redoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

# Notes

## Connecting to the test DB

- Can connect using;

```bash
psql -hlocalhost -p5444 -dtestdb -Uappuser # with password 'generic'
```

- Can also connect using Adminer using; <http://localhost:8095/?pgsql=fullapp&username=appuser&db=testdb&ns=public>

# Releasing to PyPI

- See [GitHub Actions CI/CD workflows](https://github.com/grumBit/python_packaging_example/blob/master/README.md#github-actions-cicd-workflows)

## How I did it this time

### Initial upload to Test PyPI

- Upload using Test PyPI global scope API key;

```bash
python3 -m pip install --upgrade twine # Maybe I should add twine to requirements_dev.in?
python3 -m build
python3 -m twine upload --repository testpypi dist/*
    # user name = __token__
    # For p/w, get "API token - Global scope" in 1Password "TestPyPI - grumBit" item 
```

### Set up project specific token

- Create a new token specifically for the project;
  - Head to [Test PtPI](https://test.pypi.org/manage/projects/) -> `Manage` for fullapp -> `Settings` -> `Create a token for fullapp`
  - Set `Token name` to fullapp
  - Change the `Scope` to "Project: fullapp`
  - Click `Add Token`
  - Add the generated token in a new password field named '🔑 API Token - "fullapp"' in the 1Password "TestPyPI - grumBit" item
- Test the new token by running `python3 -m pip install --upgrade twine` again, but with the new token

### Test uploaded project

- In a new directory, create a new python venv;

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install wheel pip-tools
```

- Install the new project;

```bash
package_name="fullapp"
python3 -m pip install --index-url https://test.pypi.org/simple/ --pre ${package_name}  # Check the package can be installed
python3 -c "from fullapp import myapp" # Check package functions
```

### Add the TestPyPi and PyPi API tokens to the repo

- Open the [repo on github](https://github.com/grumBit/fullapp) -> `Settings` -> `Secrets and variables` -> `Actions` -> `New respository secret`
- Name = "TEST_PYPI_API_TOKEN"
- Secret = The project's API token form the 1Password "TestPyPI - grumBit" item
