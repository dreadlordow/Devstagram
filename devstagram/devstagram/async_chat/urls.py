from django.urls import path

from devstagram.async_chat.views import chatroom

urlpatterns = [
    path('asyncchat/<str:user_one>/<str:user_two>/', chatroom, name='asyncroom')
]