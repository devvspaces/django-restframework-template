# flake8: noqa

from .dev import *

SECRET_KEY = "fake-key"

INSTALLED_APPS += [
    "tests"
]

DB_DEFAULT = config("DB_DEFAULT", default="sqlite")

if DB_DEFAULT == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': "trip_testing_fake_db",
            'USER': config("TEST_DB_USER"),
            'PASSWORD': config("TEST_DB_PASSWORD"),
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test.db.sqlite3',
        },
    }

# use default loc mem cache for tests
CACHES['default']["BACKEND"] = 'django.core.cache.backends.locmem.LocMemCache'
