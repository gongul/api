from .base import *
from .base import SETTING_FILE

ALLOWED_HOSTS = ["*"]

DEBUG = False

WSGI_APPLICATION = 'common.wsgi.production.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': SETTING_FILE['MYSQL']['PRODUCTION']['HOST'],
        'USER': SETTING_FILE['MYSQL']['PRODUCTION']['USER'],
        'NAME': SETTING_FILE['MYSQL']['PRODUCTION']['DATABASE'],
        'PASSWORD': SETTING_FILE['MYSQL']['PRODUCTION']['PASSWORD'],
        'PORT': SETTING_FILE['MYSQL']['PRODUCTION']['PORT']
    }
}

REDIS = {
    'URL': SETTING_FILE['REDIS']['PRODUCTION']['URL'],
    'PASSWORD': SETTING_FILE['REDIS']['PRODUCTION']['PASSWORD'],
    'PORT': SETTING_FILE['REDIS']['PRODUCTION']['PORT']
}
