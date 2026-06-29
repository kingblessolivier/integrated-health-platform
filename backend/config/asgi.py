import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# Channels routing for vitals-streaming WebSockets is added here (see docs 49, 07).
application = get_asgi_application()
