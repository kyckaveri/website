""" WSGI config for kycwebsite project. """

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kycwebsite.settings')

application = get_wsgi_application()
