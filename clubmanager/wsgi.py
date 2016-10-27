"""
WSGI config for clubmanager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

import logging_tree
from django.core.wsgi import get_wsgi_application

settings_file = os.environ.get("DJANGO_SETTINGS_FILE", "clubmanager.settings_development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_file)

application = get_wsgi_application()

# logging_tree.printout(node=None)
