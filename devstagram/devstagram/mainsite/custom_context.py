from itertools import chain
from operator import attrgetter

from django.contrib.auth.models import User

from devstagram.async_chat.models import ChatRoom
from devstagram.mainsite.models import FriendRequest, Picture


def get_notifications(request):
    user = request.user

    if not user.is_anonymous:
        notifications = FriendRequest.objects.filter(receiver=user)
        pictures = Picture.objects.filter(user_id=user.id)

        likes = []
        for like in pictures:
            for l in like.like_set.all():
                likes.append(l)
        for notif in notifications:
            likes.append(notif)
        likes = sorted(likes, key=attrgetter('time'), reverse=True)
        return {'notifications': likes, 'notifslen': len(likes)}
    return {}


def get_chats(request):
    user = request.user
    if not user.is_anonymous:
        chatrooms = ChatRoom.objects.filter(user_one_id=user.id) | ChatRoom.objects.filter(user_two_id=user.id)
        chatrooms = chatrooms.order_by('-last_msg_time')
        user_ids = chatrooms.values_list('user_one', 'user_two')
        user_ids = set(chain(*user_ids))
        if user.id in user_ids:
            user_ids.remove(user.id)
        users = User.objects.filter(id__in=user_ids)
        return {'chats': chatrooms, 'users': users, 'chatroom_user': zip(chatrooms, users)}
    return {}