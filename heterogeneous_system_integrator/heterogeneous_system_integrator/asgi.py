"""
ASGI config for Heterogeneous_system_integrator project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from heterogeneous_system_integrator import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.__name__)

application = get_asgi_application()
