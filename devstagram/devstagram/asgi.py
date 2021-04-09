import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from devstagram.async_chat.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devstagram.settings')

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('notifications/', NotificationConsumer.as_asgi()),
    ])
})
