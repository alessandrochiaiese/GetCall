"""
WSGI config for getref project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

# Percorso del progetto
path = "/home/getcall/getref"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getref.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
