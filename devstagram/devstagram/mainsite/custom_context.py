from itertools import chain
from operator import attrgetter

from django.contrib.auth.models import User
from django.db.models import Case, When

from devstagram.async_chat.models import ChatRoom
from devstagram.mainsite.models import FriendRequest, Picture, Friendship


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
        pairs_user_ids = chatrooms.values_list('user_one', 'user_two')
        user_ids = []
        for pair in pairs_user_ids:
            pair = list(pair)
            pair.remove(user.id)
            if pair:
                user_ids.append(pair[0])
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(user_ids)])
        users = User.objects.filter(pk__in=user_ids).order_by(preserved)
        return {'chats': chatrooms, 'users': users, 'chatroom_user': zip(chatrooms, users)}
    return {}


def get_friends(request):
    user = request.user
    if not user.is_anonymous:

        friendships = Friendship.objects.filter(friend_one=user)|Friendship.objects.filter(friend_two=user)
        friend_ids = set(chain(*friendships.values_list('friend_one', 'friend_two')))
        friend_ids.remove(user.id)
        friends = User.objects.filter(id__in=friend_ids)
        return {'friends': friends}
    return {}


