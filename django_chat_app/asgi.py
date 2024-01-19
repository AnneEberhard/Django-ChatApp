"""
ASGI config for django_chat_app project.
ASGI (Asynchrnonous Server Gateway Interface) is a spirtual successor to WSGI,
intended to provede a standard interface between async-capable, Python web servers, frameworks, and applications.

Where WSGI proveded a standard for synchronous Üython apps, ASGI provides one for both asynchronous and synchronous apps

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat_app.settings')

application = get_asgi_application()
