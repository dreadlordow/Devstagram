from hashlib import sha256

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class UserAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    two_factor_auth = models.BooleanField(blank=True)


class TwoFactorAuthMsg(models.Model):
    hash_url = models.CharField(max_length=1000)
    two_factor_code = models.IntegerField()


class Picture(models.Model):
    picture = models.ImageField(blank=False, upload_to='pictures')
    description = models.TextField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now=True)

    def likes_as_flat_list(self):
        return self.like_set.all().values_list('user_id', flat=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    accepted = models.BooleanField(default=False,blank=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender.username} sent you a friend request.'


class Friendship(models.Model):
    friend_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_one')
    friend_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_two')


class UserFriends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.IntegerField(default=0)


class Like(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)


class ProfilePicture(models.Model):
    image = models.ImageField(upload_to='profile_pictures', default='profile_pictures/default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
