from .staging import *  # noqa

ALLOWED_HOSTS = ['live.domain']


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5)  # noqa
}
