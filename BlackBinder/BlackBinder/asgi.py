"""
ASGI config for BlackBinder project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
from django_nextjs.proxy import NextJSProxyHttpConsumer, NextJSProxyWebsocketConsumer
from django.urls import path, re_path
from django.conf import settings
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BlackBinder.settings')

asgi_application = get_asgi_application()


http_routes = [re_path(r"", asgi_application)]
websocket_routers = []

if settings.DEBUG:
    http_routes.insert(0, re_path(r"^(?:_next|__next|next).*", NextJSProxyHttpConsumer.as_asgi()))
    websocket_routers.insert(0, path("_next/webpack-hmr", NextJSProxyWebsocketConsumer.as_asgi()))


application = ProtocolTypeRouter(
    {
        "http": URLRouter(http_routes),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_routers)),
    }
)
