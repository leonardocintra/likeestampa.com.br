import environ

from likeestampa.settings.base import *

env = environ.Env()

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["likeestampa.com.br", "www.likeestampa.com.br"]

DATABASES = {
    "default": env.db(),
}


MERCADO_PAGO_PRIVATE_KEY = env("MERCADO_PAGO_PRIVATE_KEY")
MERCADO_PAGO_PUBLIC_KEY = env("MERCADO_PAGO_PUBLIC_KEY")

MAXIMO_ITENS_CARRINHO = env.int("MAXIMO_ITENS_CARRINHO")
PEOPLE_SOFT_API = env("PEOPLE_SOFT_API")
PEOPLE_SOFT_API_TOKEN = ''

