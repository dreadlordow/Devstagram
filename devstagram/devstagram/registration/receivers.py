from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from devstagram.mainsite.models import ProfilePicture, UserFriends

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_picks(sender, instance, created, *args, **kwargs):
    if created:
        print('true')
        pfp = ProfilePicture(user=instance)
        pfp.save()
        userfriend = UserFriends(user=instance)
        userfriend.save()

