"""
Django settings for '{{ cookiecutter.project_name }}' project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import sys
import environ
import os
from django.utils.translation import gettext_lazy as _
from email.utils import getaddresses
from io import StringIO

IS_TESTING = "test" in sys.argv
project_root = environ.Path(__file__) - 2
project_path = environ.Path(__file__) - 1

# read enviroment variables
env = environ.FileAwareEnv()
if os.path.isfile(project_root(".env")):
    env.read_env(project_root(".env"))

# read .env from enviroment variable
ENV_FILE = env("ENV_FILE", default=None)
if ENV_FILE:
    env.read_env(StringIO(ENV_FILE))

# environment settings
ENVIRONMENT = env("ENVIRONMENT", default="develop")
DEBUG = env.bool("DEBUG", default=True)

# application host name
VIRTUAL_HOST = env.str("VIRTUAL_HOST", default="localhost")

# secuirty settings
SECRET_KEY = env.str("SECRET_KEY", default="dummy")
INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1", VIRTUAL_HOST])
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = "SAMEORIGIN"
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[VIRTUAL_HOST])
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=[f"https://{VIRTUAL_HOST}"]
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    # aditional apps
    "storages",
    # project apps
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [project_path("templates")],
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

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"
DATABASE_URL = env("DATABASE_URL", default="sqlite:///db.sqlite3")
DATABASES = {"default": env.db(default="sqlite:///db.sqlite3")}
CACHES = {"default": env.cache(default="locmemcache://")}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
LANGUAGES = [("pt-br", _("Potuguês Brasil"))]
TIME_ZONE = env("TIME_ZONE", default="America/Recife")
USE_I18N = True
USE_TZ = True

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
STATIC_ROOT = env("STATIC_ROOT", default=project_root("staticfiles"))
STATIC_URL = env("STATIC_URL", default="/static/")

# {% if cookiecutter.whitenoise_static %}
# Whitenoiise
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# {% endif %}

# Media files
MEDIA_ROOT = env.url("MEDIA_ROOT", default=project_root("media"))
MEDIA_URL = env("MEDIA_URL", default="media")
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024**2  # max upload data 20 MB
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644
S3_MEDIA_BUCKET_URL = env.url("S3_MEDIA_BUCKET_URL", default=None)
if S3_MEDIA_BUCKET_URL is not None:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_PRIVATE_QUERYSTRING_AUTH = True
    AWS_ACCESS_KEY_ID = S3_MEDIA_BUCKET_URL.username
    AWS_SECRET_ACCESS_KEY = S3_MEDIA_BUCKET_URL.password
    AWS_STORAGE_BUCKET_NAME = S3_MEDIA_BUCKET_URL.path.strip("/")
    AWS_PRIVATE_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
    AWS_QUERYSTRING_EXPIRE = 3600
    AWS_S3_ENDPOINT_URL = (
        f"{S3_MEDIA_BUCKET_URL.scheme or 'https'}://{S3_MEDIA_BUCKET_URL.netloc}"
    )

# Email config
ADMINS = getaddresses([env("ADMINS", default="")])
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=None)
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
vars().update(env.email_url("EMAIL_URL", default="consolemail://"))

# Sets default for primary key IDs
# See https://docs.djangoproject.com/en/4.1/ref/models/fields/#bigautofield
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# logging - Enable log to console
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Sentry error reporter
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
if SENTRY_DSN:  # sentry is configured
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration, RedisIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), RedisIntegration()],
        environment=ENVIRONMENT,
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
# develop environment settings
if DEBUG:
    # allow localhost access
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

    # enable debug toolbar if available
    try:
        import debug_toolbar
    except ModuleNotFoundError:
        pass
    else:
        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
