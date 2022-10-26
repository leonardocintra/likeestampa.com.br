from likeestampa.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "likeestampa",
        "USER": "likeestampa",
        "PASSWORD": "likeestampa",
        "HOST": "0.0.0.0",
        "PORT": 3306
    }
}