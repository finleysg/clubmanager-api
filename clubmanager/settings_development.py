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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = '56723e8f5a3d7e935'
EMAIL_HOST_PASSWORD = '4daeee33d627a7'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'var/www/static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'var/www/media')

MEDIA_URL = '/media/'
