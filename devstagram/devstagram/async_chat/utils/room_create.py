from itertools import chain

from django.contrib.auth.models import User

from devstagram.async_chat.models import ChatRoom


def create_room(user_one, user_two):
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

    messages = list(chain(chatroom.message_set.all(),chatroom.postmessage_set.all()))
    messages = sorted(messages, key=lambda x: x.timestamp)
    context = {
        'room_name': room_name,
        'messages': messages,
        'user_one': user_one.username,
        'user_two': user_two.username,
        'user_two_': user_two,
        'chatroom': chatroom
    }
    return context