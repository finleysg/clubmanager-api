"""
Django local settings, changed per environment
"""
try:
    from .settings_base import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u85qoa@x3h71r6hi%b#$81e0lv4b^1g6f9_t#ki(ul-he7_3+o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
