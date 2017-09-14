"""
WSGI config for royl8 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# GETTING-STARTED: change 'royl8' to your project name:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "royl8.settings")

application = get_wsgi_application()
