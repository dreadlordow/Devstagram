from django.contrib.auth.models import User
from django.shortcuts import render

from devstagram.async_chat.models import ChatRoom
from devstagram.async_chat.utils.room_create import create_room


def room(request, user_one, user_two):
    context = create_room(user_one, user_two)
    return render(request, 'async/chatroom.html', context)
