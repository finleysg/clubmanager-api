"""
Django local settings, changed per environment
"""
import logging.config

try:
    from .settings_base import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u85qoa@x3h71r6hi%b#$81e0lv4b^1g6f9_t#ki(ul-he7_3+o'

STRIPE_SECRET_KEY = 'sk_test_Qwz0pIFtX92mU2kBBE9Tqfh8'
STRIPE_PUBLIC_KEY = 'pk_test_huMlHToXOZcuNXb9eQ7viBvY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
ADMIN_URL = 'http://localhost:8000'

# CORS_ORIGIN_WHITELIST = (
#     'localhost:3000'
# )

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'club',
        'USER': 'clubmanager',
        'PASSWORD': 'nicklaus',
        'HOST': 'localhost',
        'PORT': 3306,
        'TIME_ZONE': 'America/Chicago'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'var/www/static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'var/www/media')

MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/debug.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
            'propagate': True,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
logging.config.dictConfig(LOGGING)
