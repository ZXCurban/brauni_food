"""
Django settings for Brauni Food.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- Secrets -----------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-key-change-in-production",
)

# ---- Debug -------------------------------------------------------------
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"

# ---- Hosts -------------------------------------------------------------
DEFAULT_ALLOWED_HOSTS = "localhost,127.0.0.1,testserver" if DEBUG else ""

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(",")
    if host.strip()
]

# Railway / Render provide the app domain via env
_RAILWAY_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
_RENDER_DOMAIN = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
for _d in (_RAILWAY_DOMAIN, _RENDER_DOMAIN):
    if _d and _d not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_d)

CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" for host in ALLOWED_HOSTS if host not in ("localhost", "127.0.0.1", "testserver")
]
CSRF_TRUSTED_ORIGINS.extend(["http://localhost:5173", "http://127.0.0.1:5173"])

# ---- Apps --------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django_vite",
    "apps.products",
    "apps.categories",
    "apps.vacancies",
    "apps.company",
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.company.context_processors.company_info",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---- Database ----------------------------------------------------------
# Support DATABASE_URL (Railway / Render) and individual env vars

_db_url = os.environ.get("DATABASE_URL", "")
if _db_url and _db_url.startswith("postgres"):
    import re
    _m = re.match(
        r"postgres(?:ql)?://(?P<USER>[^:]+):(?P<PASSWORD>[^@]+)"
        r"@(?P<HOST>[^:/]+):?(?P<PORT>\d+)?/(?P<NAME>.+)",
        _db_url,
    )
    if _m:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": _m["NAME"],
                "USER": _m["USER"],
                "PASSWORD": _m["PASSWORD"],
                "HOST": _m["HOST"],
                "PORT": _m["PORT"] or "5432",
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "brauni_db"),
            "USER": os.environ.get("POSTGRES_USER", "zxcurban"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", ""),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

# ---- Password validation -----------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---- Internationalization ----------------------------------------------
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# ---- Static & Media ----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise (production static serving)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# ---- CORS --------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]

# ---- Django-Vite -------------------------------------------------------
DJANGO_VITE = {
    "default": {
        "dev_mode": os.environ.get("DJANGO_VITE_DEV_MODE", "false").lower() == "true",
        "dev_server_host": "127.0.0.1",
        "dev_server_port": 5173,
        "manifest_path": BASE_DIR / "static" / "dist" / ".vite" / "manifest.json",
    }
}

# ---- Production security -----------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "true").lower() == "true"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
