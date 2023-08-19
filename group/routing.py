
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

from group import LikeConsumer
from . import consumers

websocket_urlpatterns =[
       path('ws/group/<int:group_id>/', consumers.ChatConsumer.as_asgi()),
]