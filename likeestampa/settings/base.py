"""
Django settings for likeestampa project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import environ
import os
import dj_database_url
from pathlib import Path

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_&%r6!rao1dl+&wkye8f9bu#mc7gr#^$bn!6^@_5oiurzgkw1j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    # DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # TERCEIROS
    'cloudinary',
    'localflavor',
    'mathfilters',
    'widget_tweaks',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'anymail',
    'fontawesomefree',

    # LOCAL
    'apps.core',
    'apps.catalogo',
    'apps.checkout',
    'apps.evento',
    'apps.pagamento',
    'apps.pedido',
    'apps.seller',
    'apps.usuario',
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
]

ROOT_URLCONF = 'likeestampa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'likeestampa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        'NAME': env("MYSQL_NAME"),
        'USER': env("MYSQL_USER"),
        'PASSWORD': env("MYSQL_PASSWORD"),
        'HOST': env("MYSQL_HOST"),
        'PORT': env("MYSQL_PORT"),
    }
}


# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Sessions
# SESSION_EXPIRE_AT_BROWSER_CLOSE=True
# SESSION_COOKIE_AGE = 20


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CLOUDINARY CONFIGS
CLOUDINARY = {
    'cloud_name': env('CLOUDINARY_CLOUD_NAME'),
    'api_key': env('CLOUDINARY_API_KEY'),
    'api_secret': env('CLOUDINARY_API_SECRET'),
}


# MERCADO PAGO
MERCADO_PAGO_PUBLIC_KEY = env("MERCADO_PAGO_PUBLIC_KEY")
MERCADO_PAGO_PRIVATE_KEY = env("MERCADO_PAGO_PRIVATE_KEY")

# MELHOR ENVIO
MELHOR_ENVIO_TOKEN = env("MELHOR_ENVIO_TOKEN")
MELHOR_ENVIO_BASE_URL = env("MELHOR_ENVIO_BASE_URL")

MAXIMO_ITENS_CARRINHO = 10


# Django All Auth
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_SIGNUP_FORM_CLASS = 'apps.usuario.forms.SignupForm'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
LOGIN_REDIRECT_URL = "/usuario/"


# Django Crispy Form
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# DIMONA
DIMONA_KEY = 'f9bb66ac5feaebd7b97206198866a898'

# TELEGRAM
TELEGRAM_TOKEN = '508627689:AAEuLPKs-EhrjrYGnz60bnYNZqakf6HJxc0'
