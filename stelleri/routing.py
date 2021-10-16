# This "routing.py" file specifies routes to websocket consumers:

from django.urls import path, re_path #For regular-expression handling
from django.conf.urls import url
from . import consumers #import all the methods in consumers.py

# We call the as_asgi() classmethod in order to get an ASGI application that will instantiate
# an instance of our consumer for each user-connection. This is similar to Django’s as_view(),
# which plays the same role for per-request Django view instances.
websocket_urlpatterns = [
    re_path(r'^ws/devices/(?P<device_id>[0-9]+)$', consumers.DeviceConsumer.as_asgi()),
    #re_path(r'^ws/devices/(?P<device_id>[0-9]+)$', consumers.DeviceConsumer.as_asgi()),
    #re_path(r'ws/stelleri/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]