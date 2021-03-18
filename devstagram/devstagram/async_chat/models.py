from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ChatRoom(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_user_two')
    last_msg_time = models.DateTimeField(auto_now=True)

    def update_last_msg_time(self):
        self.last_msg_time = timezone.now()


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.TimeField(auto_now=True)
