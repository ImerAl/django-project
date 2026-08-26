# IMPROVE

Lista de mejoras planificadas para el proyecto. Objetivos: entorno moderno, nombres claros, sin datos sensibles hardcodeados, y base para poder testear y desplegar de forma reproducible.

Decisiones tomadas: app renombrada a `finanzas`, **Python 3.13 + Django 5.2 LTS**, **SQLite por defecto + Postgres opt-in**, UI en español con identificadores/comentarios en inglés.

---

## 1. Entorno y dependencias

- [ ] Eliminar el venv roto `activate/` del control de versiones (`git rm -r --cached activate`) y añadirlo a `.gitignore` (hoy solo lista `venv`; el venv real se llama `activate/` y está commiteado).
- [ ] Recrear el venv con Python 3.13 (`py -3.13 -m venv .venv`) — el `pyvenv.cfg` actual apunta a un Python 3.9 que ya no existe.
- [ ] Actualizar `requirements.txt`:
  - `Django==4.2` → `Django==5.2` (LTS, soporta Python 3.13).
  - Eliminar `numpy==1.24.3` y `pandas==2.0.1`: se importan en `views.py:14-15` pero **no se usan**; además bloqueaban Python 3.12+.
  - Eliminar `unicorn==2.0.1.post1` (paquete accidental, no relacionado).
  - Mantener `dj-database-url`, `psycopg2-binary`, `whitenoise`, `gunicorn`.

## 2. Renombrado y convenciones

- [ ] Renombrar la app `moneyflow` → `finanzas`:
  - Carpeta `moneyflow/` → `finanzas/`.
  - `INSTALLED_APPS` en `mysite/settings.py:46`.
  - `apps.py`: clase `InsertdataConfig` (nombre obsoleto de un rename anterior) → `FinanzasConfig`.
  - Imports en `mysite/urls.py` y `admin.py`.
- [ ] Regenerar las migraciones desde cero (no hay datos de producción y `db.sqlite3` está ausente): borrar `finanzas/migrations/` y crear una sola `0001_initial` limpia. Las 12 migraciones actuales tienen ida y vuelta innecesario (ej. `pay_date` agregado/eliminado/re-agregado).
- [ ] Modelos (`models.py`):
  - `TypeC` → `CardType`.
  - `Cut_Off` → `CutOff`.
  - `GeneralCategory` → `Category`.
  - Campo `type` (FK) → `card_type` (hoy sombrea el builtin `type`).
  - `detained` → `is_withheld`.
  - `transaction_type` → `is_income` (mantener boolean: `1` = ingreso, `0` = egreso).
- [ ] Vistas/funciones: `log_in`→`login_view`, `log_out`→`logout_view`, `add_batch`→`create_batch`, `Insert_Amount`→`InsertAmount`, `Update_Moneyflow`→`UpdateAmount`, `move_detail`→`detail`, `general`→`categories`.
- [ ] URLs: añadir `name=` a todos los `path()` en `finanzas/urls.py` y usar `reverse()` en vistas y `{% url %}` en templates (hoy hay rutas hardcodeadas: `redirect('/show/')`, `redirect('/insert/')`, `action="/signup/"`, etc.).
- [ ] `LANGUAGE_CODE='es'` en `settings.py` (hoy `en-us` aunque toda la UI es español).

## 3. Configuración y base de datos

- [ ] `DATABASES` en `settings.py:84-90`: por defecto SQLite (`BASE_DIR / 'db.sqlite3'`) y usar `DATABASE_URL` solo si está definida (Render/Postgres). Así el proyecto corre localmente sin variables.
- [ ] Gestión de configuración por entorno: `python-decouple` o `django-environ`; crear `.env.example` con las variables necesarias; añadir `.env` a `.gitignore`.

## 4. Seguridad y datos sensibles

- [ ] `SECRET_KEY` hardcodeado con default (`settings.py:25`): leerlo de variable de entorno y **fallar si no existe en producción**; generar una clave nueva, no commitear.
- [ ] FKs a `User` con `default=1` (`models.py:39,46`): quitar el default y asignar `request.user` al guardar (el flujo de `insert` ya lo hace).
- [ ] IDOR: `update` y `move_detail` (`views.py:128-151`) hacen `get_object_or_404(MoneyInformation, pk=id)` **sin filtrar `user`** — cualquier usuario autenticado puede ver/editar movimientos ajenos. Filtrar `user=request.user` (el `delete` ya lo hace).
- [ ] Corregir mensaje de error de login `'Vanpiro no esite'` (`views.py:232`) → texto correcto en español.
- [ ] `pay_date = models.DateField(default=datetime.datetime.now)` (`models.py:40`): pasa un `datetime` a un `DateField`; usar `timezone.now` (y reconsiderar `auto_now_add`).

## 5. Bugs y calidad de código

- [ ] `get_balance` (`views.py:161`): `if total_outcome is None and total_outcome is None:` comprueba la misma variable dos veces → corregir a `total_income is None`.
- [ ] Las vistas GET de `insert`, `signup` y `login` (`views.py:32,202,222`) pasan la **clase** del formulario en vez de una instancia (`Insert_Amount`, `UserCreationForm`, `AuthenticationForm`) → instanciar (`Insert_Amount()`).
- [ ] Eliminar `credit = TypeC.objects.get(name="Credito")` en `insert` (`views.py:37`): variable sin uso y nombre hardcodeado.
- [ ] `signup` (`views.py:215`): `except:` desnudo → capturar `IntegrityError`/`ValidationError` y mostrar un mensaje real.
- [ ] `add_batch` genera el número con `random.randint` (posibles colisiones) → usar UUID o constraint único en `batch_number`.
- [ ] Reemplazar `from .models import *` y `from .forms import *` por imports explícitos (`forms.py:6`, `views.py:11,16`) — el acoplamiento actual rompe en silencio al refactorizar.
- [ ] Unificar `Insert_Amount` y `Update_Moneyflow` (`forms.py:9,36`): misma `Meta`/fields, extraer una clase base.
- [ ] Eliminar código muerto/comentado: `about` (`views.py:244`), placeholder de `index`, bloques de comentarios de urls/settings, imports sin usar (`random` queda, revisar el resto).
- [ ] `.idea/` está trackeado en git → añadir a `.gitignore` y hacer `git rm -r --cached .idea`.
- [ ] `staticfiles/` (generado por `collectstatic`) → añadir a `.gitignore`.

## 6. Tests y CI

- [ ] `tests.py` está vacío → añadir tests: querysets de modelos (ingreso/egreso, retenidos), validación de formularios, y vistas (auth, insert, update, show, y el caso IDOR).
- [ ] Añadir `ruff` (lint + format) con config en `pyproject.toml` o `ruff.toml`.
- [ ] CI con GitHub Actions: `ruff check` + `python manage.py test` contra SQLite.

## 7. Documentación

- [ ] Actualizar `AGENTS.md` tras los cambios: nombre de app, comandos, `DATABASE_URL` ya no obligatoria localmente, versión de Python/Django.
