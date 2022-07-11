from .base import *
from .base import SETTING_FILE

ALLOWED_HOSTS = ["*"]

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

WSGI_APPLICATION = 'common.wsgi.local.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': SETTING_FILE['MYSQL']['BUILD']['HOST'],
        'USER': SETTING_FILE['MYSQL']['BUILD']['USER'],
        'NAME': SETTING_FILE['MYSQL']['BUILD']['DATABASE'],
        'PASSWORD': SETTING_FILE['MYSQL']['BUILD']['PASSWORD'],
        'PORT': SETTING_FILE['MYSQL']['BUILD']['PORT']
    }
}

REDIS = {
    'URL': SETTING_FILE['REDIS']['BUILD']['URL'],
    'PASSWORD': SETTING_FILE['REDIS']['BUILD']['PASSWORD'],
    'PORT': SETTING_FILE['REDIS']['BUILD']['PORT']
}


# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
