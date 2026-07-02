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
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.accounts.apps.AccountsConfig",
    "apps.audit",
    "apps.consent",
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
    "apps.stock",
    "apps.hr",
    "apps.pbf",
    "apps.cbhi",
    "apps.supply",
    "apps.regulatory",
    "apps.maternity",
    "apps.integrations",
    "apps.security",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Sets PostgreSQL session GUCs (app.tenant_id/user_id) so RLS applies per request.
    "apps.common.middleware.TenantContextMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"postgres://{env('POSTGRES_USER', default='inhp')}:{env('POSTGRES_PASSWORD', default='inhp')}@{env('POSTGRES_HOST', default='localhost')}:{env('POSTGRES_PORT', default='5432')}/{env('POSTGRES_DB', default='inhp')}",
    )
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "apps.security.authentication.BlacklistAwareJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("apps.accounts.permissions.HoldsCommand",),
    "EXCEPTION_HANDLER": "apps.security.exceptions.audited_exception_handler",
}

# JWT carries the four-axis scope (role/commands, geo, tenant, sensitivity). RS256 in prod.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=8),
    "ALGORITHM": env("JWT_ALG", default="HS256"),  # switch to RS256 with keys in prod
}

# In production set JWT_ALG=RS256 and provide the keys (private key stays in the HSM, docs/08).
if SIMPLE_JWT["ALGORITHM"] == "RS256":
    SIMPLE_JWT["SIGNING_KEY"] = env("JWT_PRIVATE_KEY", default="")
    SIMPLE_JWT["VERIFYING_KEY"] = env("JWT_PUBLIC_KEY", default="")

# Argon2id password hashing (docs/08) — memory-hard, GPU-resistant.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

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
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
