import os
import sys
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ── 密钥 & 调试模式 ──────────────────────────────────────────
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-exam-system-dev-key-change-in-production"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "http://127.0.0.1:8000,https://*.up.railway.app"
).split(",")

# ── 应用 ──────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "exams",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",          # 静态文件
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "exam_system.urls"

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
    },
]

WSGI_APPLICATION = "exam_system.wsgi.application"

# ── 数据库 ──────────────────────────────────────────────────────
# 优先使用 DATABASE_URL 环境变量（Railway / Heroku 自动注入）
# 如果没有，fallback 到 SQLite 开发模式
_DATABASE_URL = os.environ.get("DATABASE_URL")
if _DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=_DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    # 如果是 MySQL 引擎，设置 utf8mb4
    if "mysql" in _DATABASE_URL:
        DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4"}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ── 密码验证 ──────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# ── 国际化 ──────────────────────────────────────────────────
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

# ── 静态文件（Whitenoise） ──────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ── 登录 ──────────────────────────────────────────────────
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"