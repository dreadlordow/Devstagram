from django import template
from devstagram.mainsite.models import Friendship

register = template.Library()


@register.filter(name='get_friends')
def get_friends(user):
    friends = Friendship.objects.filter(friend_one=user) | Friendship.objects.filter(friend_two=user)
    return len(friends)