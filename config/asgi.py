import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализация Django
django.setup()

from messenger.middleware import WebSocketAuthMiddleware
from messenger.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebSocketAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})

