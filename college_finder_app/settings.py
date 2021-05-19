"""
Django settings for college_finder_app project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import django_heroku
import psycopg2
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
load_dotenv()
DEBUG = os.environ['DEBUG_MODE']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = ['collegefinderapp.herokuapp.com', '127.0.0.1']

ADMINS = [('College Finder', 'collegefinderapplication@gmail.com')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'social_django',
    'taggit',
    'mathfilters',

    'dashboard.apps.DashboardConfig',
    'universities.apps.UniversitiesConfig',
    'college_comparison.apps.CollegeComparisonConfig',
    'bookmarks.apps.BookmarksConfig',
    'blogs.apps.BlogsConfig',
    'faqs.apps.FaqsConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR) / "components" / "templates"],
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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2'
]
# Social Authentications


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'components/media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'components/static'),
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
EMAIL_PORT = os.environ['EMAIL_PORT']

SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Sentry
sentry_sdk.init(
    dsn="https://b5b99558b8844a5c8c04ce2ddae45344@o673374.ingest.sentry.io/5768124",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

# Activate Django-Heroku.
django_heroku.settings(locals())
