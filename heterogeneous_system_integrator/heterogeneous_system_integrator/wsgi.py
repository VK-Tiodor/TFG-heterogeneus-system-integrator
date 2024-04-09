"""
WSGI config for Heterogeneous_system_integrator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from heterogeneous_system_integrator import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.__name__)

application = get_wsgi_application()
