# AGENTS.md

Django 4.2 money-tracking app. `mysite/` holds project config; `moneyflow/` is the only app and is mounted at `/` via `mysite/urls.py`. UI text and code comments are in Spanish — keep new ones in Spanish.

## Setup / run

- The committed venv at `activate/` is **broken**: its `pyvenv.cfg` points to a Python 3.9 install that no longer exists, so `python`/`py` fail. The venv is tracked in git (`.gitignore` only lists `venv`, not `activate`) — do not commit further venv changes.
- To run locally, recreate a venv with **Python 3.8–3.11**: pinned `numpy==1.24.3` and `pandas==2.0.1` do not build on 3.12+.
- `DATABASES` uses `dj_database_url.config()` with no default, so local runs need `DATABASE_URL` set, e.g. `DATABASE_URL=sqlite:///db.sqlite3`. `db.sqlite3` is gitignored and absent.
- Commands (from repo root): `python manage.py runserver`, `python manage.py makemigrations`, `python manage.py migrate`, `python manage.py test`.
- No tests exist (`tests.py` is empty), and there is no linter, formatter, or CI config.

## Domain quirks (easy to get wrong)

- `MoneyInformation.transaction_type` is a `BooleanField`: `1` = ingreso (income), `0` = egreso (expense).
- `MoneyInformation.detained` is a `BooleanField`: `1` = withheld. Active rows are filtered as `detained=0`.
- `insert` view calls `add_batch()` (in `views.py`), which creates a new `Batch` row on every insert.
- `views.py` only sees models like `TypeC`/`MoneyInformation` via the import chain `from .forms import *` → `forms.py`'s `from .models import *`. Refactoring imports in either file can silently break the other.

## Deploy (Render)

- `build.sh` runs `pip install -r requirements.txt`, `collectstatic --no-input`, `migrate`.
- `DEBUG = 'RENDER' not in os.environ`; `ALLOWED_HOSTS` gets `RENDER_EXTERNAL_HOSTNAME`.
- Static files are served by whitenoise in prod from `staticfiles/` (created by collectstatic). Vendored Bootstrap lives in `moneyflow/static/style/`; templates use a Bootstrap 4 CDN in `layouts/base.html`.
- `requirements.txt` lists both `gunicorn` and `unicorn` — `unicorn` is an unrelated/accidental package; gunicorn is the WSGI server.
