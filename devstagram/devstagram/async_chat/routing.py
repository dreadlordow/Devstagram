from django.urls import re_path

from devstagram.async_chat import consumers

websocket_urlpatterns =[
    re_path(r'ws/chat/(?P<user_one>\w+/(?P<user_two>\w+))$', consumers.ChatRoomConsumer),
]