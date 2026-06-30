"""
Django settings — skeleton for the Integrated National Health Platform API.
Reads configuration from the environment (see backend/.env.example).
"""
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-only-not-secret")
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "apps.accounts",
    "apps.audit",
    "apps.patients",
    "apps.clinical",
    "apps.pharmacy",
    "apps.billing",
    "apps.community",
    "apps.emergency",
    "apps.claims",
    "apps.interop",
    "apps.surveillance",
    "apps.diagnostics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Sets PostgreSQL session GUCs (app.tenant_id/user_id) so RLS applies per request.
    "apps.common.middleware.TenantContextMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="inhp"),
        "USER": env("POSTGRES_USER", default="inhp"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="inhp"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("apps.accounts.permissions.HoldsCommand",),
}

# JWT carries the four-axis scope (role/commands, geo, tenant, sensitivity). RS256 in prod.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=8),
    "ALGORITHM": env("JWT_ALG", default="HS256"),  # switch to RS256 with keys in prod
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
    }
}

CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
LANGUAGE_CODE = "en"
TIME_ZONE = "Africa/Kigali"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
