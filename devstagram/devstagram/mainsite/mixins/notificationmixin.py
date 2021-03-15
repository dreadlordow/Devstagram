from operator import attrgetter

from devstagram.mainsite.models import FriendRequest, Picture


class NotificationMixin:
    @staticmethod
    def get_notifications(user):
        notifications = FriendRequest.objects.filter(receiver=user)
        pictures = Picture.objects.filter(user_id=user.id)
        likes = []
        for like in pictures:
            for l in like.like_set.all():
                likes.append(l)
        for notif in notifications:
            likes.append(notif)
        likes = sorted(likes, key=attrgetter('time'), reverse=True)
        return likes
