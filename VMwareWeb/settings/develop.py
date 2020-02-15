"""开发环境的项目配置 pycharm设置 DJANGO_SETTINGS_MODULE"""

from .base import *  # NOQA


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'VMwareWeb',
        'USER': 'root',
        'PASSWORD': 'MuXu2014@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': None,
    }
}