from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')
    last_msg_time = models.DateTimeField(auto_now=True)

    def update_last_msg_time(self):
        self.last_msg_time = timezone.now()


class Message(models.Model):
    message = models.TextField(max_length=500)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msgsender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msgreceiver')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
