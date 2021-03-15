from django.urls import path
from devstagram.chat.views import CreateOrGetChatRoom, SendMessage

urlpatterns = [
    path('chat/<str:slug>/', CreateOrGetChatRoom.as_view(), name='chatroom'),
    path('send/', SendMessage.as_view(), name='sendmsg'),
]