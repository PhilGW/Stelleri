"""
ASGI config for mystelleri project (for Websockets)

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter  # for Channels
from django.core.asgi import get_asgi_application
#Need to include the routing file from the app:
import stelleri.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mystelleri.settings')

# This root routing configuration specifies that when a connection is made to the Channels development server,
# the ProtocolTypeRouter will first inspect the type of connection.
# If it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.
# The AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user,
# similar to how Django’s AuthenticationMiddleware populates the request object of a view function with the currently
# authenticated user. (Scopes will be discussed later in this tutorial.) Then the connection will be given to the URLRouter.
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    #Reference the routing.py in the app:
    "websocket": AuthMiddlewareStack(
        URLRouter(stelleri.routing.websocket_urlpatterns)
    ),
})