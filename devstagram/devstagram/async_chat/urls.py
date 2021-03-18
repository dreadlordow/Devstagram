from django.urls import path

from devstagram.async_chat.views import room

urlpatterns = [
    path('asyncchat/<str:user_one>-<str:user_two>', room, name='asyncroom')
]