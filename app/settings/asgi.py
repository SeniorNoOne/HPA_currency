import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing as urls


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                urls.websocket_urlpatterns
            )
        )
    }
)
