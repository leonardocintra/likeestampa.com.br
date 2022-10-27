import environ
env = environ.Env()

from likeestampa.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'NAME': os.environ["MYSQL_NAME"],
        'USER': os.environ["MYSQL_USER"],
        'PASSWORD': os.environ["MYSQL_PASSWORD"],
        'HOST': os.environ["MYSQL_HOST"],
        'PORT': os.environ["MYSQL_PORT"],
    }
}