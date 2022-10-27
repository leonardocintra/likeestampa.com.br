import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from likeestampa.settings.base import *

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# SECURE SSL (HTTPS Sempre)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["PGDATABASE"],
        'USER': os.environ["PGUSER"],
        'PASSWORD': os.environ["PGPASSWORD"],
        'HOST': os.environ["PGHOST"],
        'PORT': os.environ["PGPORT"],
    }
}

# MERCADO PAGO
MERCADO_PAGO_PRIVATE_KEY = env("MERCADO_PAGO_PRIVATE_KEY")
MERCADO_PAGO_PUBLIC_KEY = env("MERCADO_PAGO_PUBLIC_KEY")

# MELHOR ENVIO
MELHOR_ENVIO_TOKEN = env("MELHOR_ENVIO_TOKEN")
MELHOR_ENVIO_BASE_URL = "https://melhorenvio.com.br"

# LIKE ESTAMPA
MAXIMO_ITENS_CARRINHO = env.int("MAXIMO_ITENS_CARRINHO")


# ANYMAIL
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": "mg.likeestampa.com.br"
}
DEFAULT_FROM_EMAIL = "likeestampa@gmail.com"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# DIMONA
DIMONA_KEY = env("DIMONA_KEY")

# TELEGRAM
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN")

# SENTRY
if not DEBUG:
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )
