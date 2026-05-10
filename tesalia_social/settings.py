from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if value and ((value[0] == value[-1]) and value[0] in {"'", '"'}):
            value = value[1:-1]
        if key not in os.environ or os.environ.get(key) in (None, ""):
            os.environ[key] = value


_load_dotenv(BASE_DIR / ".env")


def _parse_database_url(database_url: str) -> dict:
    database_url = (database_url or "").strip()
    if "://" in database_url:
        scheme, rest = database_url.split("://", 1)
        authority_end = len(rest)
        for sep in ("/", "?", "#"):
            idx = rest.find(sep)
            if idx != -1:
                authority_end = min(authority_end, idx)
        authority = rest[:authority_end]
        tail = rest[authority_end:]
        if "@" in authority:
            userinfo, hostport = authority.rsplit("@", 1)
            userinfo = userinfo.replace("[", "%5B").replace("]", "%5D")
            database_url = f"{scheme}://{userinfo}@{hostport}{tail}"

    parsed = urlparse(database_url)
    if parsed.scheme not in {"postgres", "postgresql"}:
        raise ValueError("Solo se soporta DATABASE_URL tipo postgres/postgresql")
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": (parsed.path or "").lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "",
        "PORT": str(parsed.port or ""),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {"sslmode": os.getenv("PGSSLMODE", "require")},
    }


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-secret-key-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [h for h in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "club",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tesalia_social.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "tesalia_social.wsgi.application"
ASGI_APPLICATION = "tesalia_social.asgi.application"

_db_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
if _db_url:
    DATABASES = {"default": _parse_database_url(_db_url)}
else:
    if os.getenv("ALLOW_SQLITE_FALLBACK", "0") == "1":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
    else:
        raise RuntimeError(
            "Falta SUPABASE_DB_URL (o DATABASE_URL). Configúrala en el archivo .env y reinicia el servidor."
        )

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "club.User"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/feed/"
LOGOUT_REDIRECT_URL = "/"

ALLOW_PUBLIC_PROFILE_VIEW = os.getenv("ALLOW_PUBLIC_PROFILE_VIEW", "1") == "1"
