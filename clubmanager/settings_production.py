"""
Django local settings, changed per environment
"""
try:
    from .settings_base import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gm0*hh0w@&gj6yx3coa1!mt!radzx5gceg-no#dljk$7zc74wp'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost','.pythonanywhere.com',]

ADMINS = [('finleysg', 'finleysg@gmail.com')]

# Database
# EB instance admin = stuart
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'finleysg$bhmc',
        'USER': 'finleysg',
        'PASSWORD': 'Fl0werP0t',
        'HOST': 'finleysg.mysql.pythonanywhere-services.com',
        'PORT': 3306,
    }
}

# ses-smtp-user.20160131-205034 settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = '56723e8f5a3d7e935'
EMAIL_HOST_PASSWORD = '4daeee33d627a7'
EMAIL_PORT = '2525'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False


# Amazon S3 config courtesy of
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}
AWS_S3_FILE_OVERWRITE = True
AWS_STORAGE_BUCKET_NAME = 'bhmc'
AWS_ACCESS_KEY_ID = 'AKIAJHKSYOGCFFG5G2PA'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
