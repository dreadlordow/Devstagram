from django.contrib.auth.models import User
from django.shortcuts import render

from devstagram.async_chat.models import ChatRoom


def room(request, user_one, user_two):
    room_name_v1 = user_one + '-' + user_two
    room_name_v2 = user_two + '-' + user_one
    user_one = User.objects.get(username=user_one)
    user_two = User.objects.get(username=user_two)


    chatroom = ChatRoom.objects.filter(user_one=user_one, user_two=user_two)
    room_name = room_name_v1
    if not chatroom:
        chatroom = ChatRoom.objects.filter(user_one=user_two, user_two=user_one)
        room_name = room_name_v2
        if not chatroom:
            chatroom = ChatRoom.objects.create(user_one=user_one, user_two=user_two)

            room_name = room_name_v1
        else:
            chatroom = chatroom[0]
    else:
        chatroom = chatroom[0]

    messages = chatroom.message_set.all().order_by('timestamp')
    context = {
        'room_name':room_name,
        'messages': messages,
        'user_one': user_one.username,
        'user_two': user_two.username,
        'user_two_': user_two
    }
    return render(request, 'async/chatroom.html', context)
