"""
Django settings for college_finder_app project.

Environment-driven configuration — all behaviour is controlled via .env (or
real environment variables). See .env.example for a full list of supported
variables and their defaults.

Database:
  DATABASE_URL not set  →  SQLite (local dev default)
  DATABASE_URL=postgres://…  →  PostgreSQL (staging / production)

Static files:
  Always served by WhiteNoise middleware.
  USE_WHITENOISE_MANIFEST=True  →  compressed + hashed manifest (production)
  USE_WHITENOISE_MANIFEST=False →  plain static files (fast reload in dev)

Media files:
  Served from the local filesystem (MEDIA_ROOT = components/media/).
  In DEBUG mode Django's dev server serves them via urls.py.
  In production WhiteNoise does NOT serve media — gunicorn + a path rule is
  used instead (see urls.py SERVE_MEDIA_IN_PRODUCTION setting).
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Helper — typed env reader
# ---------------------------------------------------------------------------

def _env(key, default=None, cast=None):
    """Read an env var with optional type casting."""
    val = os.environ.get(key, default)
    if cast is None or val is None:
        return val
    if cast is bool:
        return str(val).strip().lower() in ('true', '1', 'yes', 'on')
    return cast(val)


def _env_list(key, default='', sep=','):
    """Read an env var as a list split by *sep*."""
    raw = os.environ.get(key, default)
    return [item.strip() for item in raw.split(sep) if item.strip()]


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env **before** reading any os.environ calls below
load_dotenv(BASE_DIR / '.env')

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', '')
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is not set. Add it to your .env file or environment."
    )

DEBUG = _env('DEBUG', default='False', cast=bool)

ALLOWED_HOSTS = _env_list('ALLOWED_HOSTS', default='localhost,127.0.0.1')

ADMINS = [('College Finder', os.environ.get('ADMIN_EMAIL', 'admin@example.com'))]

# ---------------------------------------------------------------------------
# Installed apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # WhiteNoise: disable Django's dev-server static handler so WhiteNoise
    # takes over in *all* modes (dev + prod) — this is the recommended setup.
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'social_django',
    'taggit',
    'mathfilters',

    # Local apps
    'dashboard.apps.DashboardConfig',
    'universities.apps.UniversitiesConfig',
    'college_comparison.apps.CollegeComparisonConfig',
    'bookmarks.apps.BookmarksConfig',
    'blogs.apps.BlogsConfig',
    'faqs.apps.FaqsConfig',
    'users.apps.UsersConfig',
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must come right after SecurityMiddleware and before everything
    # else — it intercepts static file requests before Django processes them.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'college_finder_app.urls'

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'components' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'college_finder_app.wsgi.application'

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
]

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY', '')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
# If DATABASE_URL is set → use it (PostgreSQL or any other URL-based DB).
# Otherwise → fall back to SQLite in the project root.
_database_url = os.environ.get('DATABASE_URL', '').strip()

if _database_url:
    _db_config = dj_database_url.config(
        default=_database_url,
        conn_max_age=_env('DB_CONN_MAX_AGE', default='600', cast=int),
        conn_health_checks=True,
    )
    # Add SSL mode if requested (e.g. Render / Railway require sslmode=require)
    if _env('DB_SSL_REQUIRE', default='False', cast=bool):
        _db_config.setdefault('OPTIONS', {})['sslmode'] = 'require'
    DATABASES = {'default': _db_config}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------------------------------
# Static Files — WhiteNoise (recommended settings for hobby/free deployment)
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'components' / 'static']

# USE_WHITENOISE_MANIFEST:
#   True  → CompressedManifestStaticFilesStorage via storage.py
#            Files are gzip/brotli compressed and get a hash in their filename.
#            Ideal for production — browsers can cache files aggressively.
#   False → Plain StaticFilesStorage
#            Faster collectstatic; no hash renaming. Good for quick dev.
_use_manifest = _env('USE_WHITENOISE_MANIFEST', default=str(not DEBUG), cast=bool)

if _use_manifest:
    # storage.py sets manifest_strict=False to prevent 500 errors when a
    # template references a file that was not collected (e.g. external libs).
    STATICFILES_STORAGE = 'storage.WhiteNoiseStaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Tell browsers they can cache static files for up to 1 year in production.
# WhiteNoise will also add ETags automatically.
WHITENOISE_MAX_AGE = 31_536_000 if not DEBUG else 0

# Don't try to compress already-compressed formats
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'avif',
    'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br', 'zst',
    'woff', 'woff2',   # fonts are already compressed
]

# ---------------------------------------------------------------------------
# Media Files
# ---------------------------------------------------------------------------
# Media is stored on the local filesystem.  On a free-tier host (Render,
# Railway, Fly.io) the disk is ephemeral — uploads won't survive a redeploy.
# For a hobby project that's acceptable; for persistence add an S3/R2 bucket
# later (django-storages makes it a one-line config change).
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'components' / 'media'

# SERVE_MEDIA_IN_PRODUCTION:
#   True  → Django serves /media/ files even when DEBUG=False (hobby default).
#            Fine for low-traffic hobby sites; not for high-load production.
#   False → You must configure a web server / CDN to serve MEDIA_ROOT.
SERVE_MEDIA_IN_PRODUCTION = _env(
    'SERVE_MEDIA_IN_PRODUCTION', default='True', cast=bool
)

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
if os.environ.get('EMAIL_HOST_USER'):
    EMAIL_BACKEND = os.environ.get(
        'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend'
    )
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = _env('EMAIL_PORT', default='587', cast=int)
    EMAIL_USE_TLS = _env('EMAIL_USE_TLS', default='True', cast=bool)
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
else:
    # No email credentials → print emails to the console (handy for dev)
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ---------------------------------------------------------------------------
# CSRF / Trusted Origins
# ---------------------------------------------------------------------------
# Required when running behind a reverse proxy or on a non-localhost domain.
# Comma-separated list, e.g.: https://myapp.onrender.com,https://www.myapp.com
_csrf_origins = _env_list('CSRF_TRUSTED_ORIGINS', default='')
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = _csrf_origins

# ---------------------------------------------------------------------------
# Security hardening (applied always — not just in production)
# ---------------------------------------------------------------------------
# Prevent clickjacking
X_FRAME_OPTIONS = 'DENY'

# Prevent MIME-type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer header policy
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Cookies always httpOnly (JS cannot access them)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Production-only HTTPS settings
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # HSTS — tells browsers to use HTTPS for 1 year (only send after you have
    # HTTPS fully working, otherwise you can lock yourself out)
    SECURE_HSTS_SECONDS = _env('SECURE_HSTS_SECONDS', default='31536000', cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Redirect HTTP → HTTPS (set False if your proxy already handles this)
    SECURE_SSL_REDIRECT = _env('SECURE_SSL_REDIRECT', default='True', cast=bool)

    # Trust the X-Forwarded-Proto header from Render / Railway / etc.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Sentry (optional) — set SENTRY_DSN in your environment to enable
_sentry_dsn = os.environ.get('SENTRY_DSN', '').strip()
if _sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=_sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0,
        send_default_pii=False,
    )
